import hashlib
from pathlib import Path
from typing import Protocol


class DocumentStorage(Protocol):
    def put(self, content: bytes, suffix: str) -> str: ...
    def get(self, key: str) -> bytes: ...


class LocalStorage:
    def __init__(self, root: Path):
        self.root = root.resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def put(self, content: bytes, suffix: str) -> str:
        if suffix not in {"html", "json", "pdf"}:
            raise ValueError("Unsupported document type")
        key = f"{hashlib.sha256(content).hexdigest()}.{suffix}"
        path = self.root / key
        if path.exists() and path.read_bytes() != content:
            raise ValueError("Immutable document collision")
        if not path.exists():
            temporary = path.with_suffix(path.suffix + ".tmp")
            temporary.write_bytes(content)
            temporary.replace(path)
        return key

    def get(self, key: str) -> bytes:
        path = (self.root / key).resolve()
        if path.parent != self.root:
            raise ValueError("Invalid storage key")
        return path.read_bytes()
