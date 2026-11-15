import hashlib
from typing import Protocol
from urllib.request import urlopen

import numpy as np

from semiconductor_research.config.settings import settings

FILES = {
    "model.onnx": (
        "onnx/model_quint8_avx2.onnx",
        "b941bf19f1f1283680f449fa6a7336bb5600bdcd5f84d10ddc5cd72218a0fd21",
    ),
    "tokenizer.json": (
        "tokenizer.json",
        "be50c3628f2bf5bb5e3a7f17b1f74611b2561a3a27eeab05e5aa30f411572037",
    ),
}


class EmbeddingProvider(Protocol):
    identifier: str

    def encode(self, texts: list[str]) -> list[list[float]]: ...


def validate_model_config(conf):
    if (
        conf.embedding_model != "sentence-transformers/all-MiniLM-L6-v2"
        or conf.embedding_revision != "1110a243fdf4706b3f48f1d95db1a4f5529b4d41"
    ):
        raise ValueError("This milestone supports only the pinned 384-dimensional MiniLM model")


def prepare_model():
    conf = settings()
    validate_model_config(conf)
    conf.model_directory.mkdir(parents=True, exist_ok=True)
    for local, (remote, checksum) in FILES.items():
        target = conf.model_directory / local
        if target.exists() and hashlib.sha256(target.read_bytes()).hexdigest() == checksum:
            continue
        temporary = target.with_suffix(".tmp")
        try:
            url = f"https://huggingface.co/{conf.embedding_model}/resolve/{conf.embedding_revision}/{remote}"
            with urlopen(url, timeout=120) as response:
                body = response.read(30_000_000)
            if hashlib.sha256(body).hexdigest() != checksum:
                raise ValueError("Embedding artifact hash mismatch")
            temporary.write_bytes(body)
            temporary.replace(target)
        except Exception:
            temporary.unlink(missing_ok=True)
            raise RuntimeError(
                "Pinned model download failed; retry preparation with network access"
            ) from None


class MiniLM:
    def __init__(self):
        conf = settings()
        validate_model_config(conf)
        for name, (_, checksum) in FILES.items():
            path = conf.model_directory / name
            if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != checksum:
                raise RuntimeError("Embedding assets missing or changed. Run: semi prepare-model")
        import onnxruntime as ort
        from tokenizers import Tokenizer

        ort.disable_telemetry_events()
        options = ort.SessionOptions()
        options.intra_op_num_threads = options.inter_op_num_threads = 1
        options.enable_cpu_mem_arena = False
        self.session = ort.InferenceSession(
            str(conf.model_directory / "model.onnx"), options, providers=["CPUExecutionProvider"]
        )
        self.tokenizer = Tokenizer.from_file(str(conf.model_directory / "tokenizer.json"))
        self.tokenizer.enable_truncation(max_length=256)
        self.identifier = f"{conf.embedding_model}@{conf.embedding_revision}:uint8:mean:l2:256"

    def encode(self, texts: list[str]) -> list[list[float]]:
        vectors = []
        for text in texts:
            item = self.tokenizer.encode(text)
            inputs = {
                "input_ids": np.array([item.ids], dtype=np.int64),
                "attention_mask": np.array([item.attention_mask], dtype=np.int64),
                "token_type_ids": np.array([item.type_ids], dtype=np.int64),
            }
            output = self.session.run(
                None, {i.name: inputs[i.name] for i in self.session.get_inputs()}
            )[0]
            mask = inputs["attention_mask"][..., None]
            pooled = (output * mask).sum(axis=1) / mask.sum(axis=1)
            norm = np.linalg.norm(pooled)
            if norm == 0 or not np.isfinite(pooled).all():
                raise RuntimeError("Invalid embedding output")
            vectors.append((pooled[0] / norm).astype(np.float32).tolist())
        return vectors
