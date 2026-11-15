"""Cited educational application context, separate from financial evidence."""

from datetime import date
from typing import Literal

from pydantic import Field, field_validator, model_validator

from semiconductor_research.config.settings import ROOT
from semiconductor_research.sources.directory import Record, load_directory, public_url

FunctionId = Literal["compute", "sense", "communicate", "control", "power"]
SceneId = Literal["ai", "car", "city", "robot", "plane", "design", "energy", "health", "connected"]


class ChipFunction(Record):
    id: FunctionId
    label: str
    description: str
    color: str = Field(pattern=r"^#[0-9a-fA-F]{6}$")


class ApplicationReference(Record):
    id: str
    publisher: str
    title: str
    url: str
    reviewed_on: date
    support: str
    company_id: str | None
    publication_date: date | None
    link_status: int | None = Field(ge=100, le=599)
    link_checked_on: date | None
    access_note: str | None
    validate_url = field_validator("url")(public_url)


class ApplicationStep(Record):
    id: str
    label: str
    task: str
    functions: list[FunctionId] = Field(min_length=1)
    chips: list[str] = Field(min_length=1)
    explanation: str
    company_ids: list[str]
    source_ids: list[str] = Field(min_length=1)
    economic_question: str


class ApplicationWorld(Record):
    id: str
    label: str
    short_label: str
    scene: SceneId
    color: str = Field(pattern=r"^#[0-9a-fA-F]{6}$")
    summary: str
    functions: list[FunctionId] = Field(min_length=1)
    source_ids: list[str] = Field(min_length=1)
    depth: Literal["guided_story", "overview"]
    steps: list[ApplicationStep] = Field(min_length=2, max_length=6)


class Footprint(Record):
    id: str
    region: str
    location: str
    role: str
    company_id: str
    description: str
    source_ids: list[str] = Field(min_length=1)


class ApplicationCatalog(Record):
    version: str
    reviewed_on: date
    human_reviewed: Literal[False]
    scope: str
    functions: list[ChipFunction]
    sources: list[ApplicationReference]
    worlds: list[ApplicationWorld]
    footprints: list[Footprint]

    @model_validator(mode="after")
    def references_resolve(self):
        def unique(items):
            ids = [item.id for item in items]
            if len(ids) != len(set(ids)):
                raise ValueError("Duplicate application catalog ID")

        for collection in (self.functions, self.sources, self.worlds, self.footprints):
            unique(collection)
        functions = {f.id for f in self.functions}
        sources = {s.id: s for s in self.sources}
        companies = {c["id"] for c in load_directory()["companies"]}
        if functions != {"compute", "sense", "communicate", "control", "power"}:
            raise ValueError("All five chip functions must be defined")
        for source in self.sources:
            if source.link_status in {401, 403, 429} and not source.access_note:
                raise ValueError("Restricted references require a visible access note")
            if source.company_id is not None and source.company_id not in companies:
                raise ValueError("Unknown reference company")
            if source.reviewed_on > self.reviewed_on:
                raise ValueError("Reference review date exceeds catalog date")

        def check_refs(ids):
            if len(ids) != len(set(ids)) or not set(ids) <= sources.keys():
                raise ValueError("Unknown or duplicate application source reference")

        for world in self.worlds:
            unique(world.steps)
            check_refs(world.source_ids)
            if (
                len(world.functions) != len(set(world.functions))
                or not set(world.functions) <= functions
            ):
                raise ValueError("Unknown or duplicate world function")
            if world.depth == "guided_story" and len(world.steps) < 3:
                raise ValueError("A guided story requires multiple system steps")
            for step in world.steps:
                check_refs(step.source_ids)
                if not set(step.functions) <= set(world.functions):
                    raise ValueError("Step functions must belong to the application world")
                supported = {sources[s].company_id for s in step.source_ids}
                if not set(step.company_ids) <= companies or not set(step.company_ids) <= supported:
                    raise ValueError("Portfolio examples require a matching company reference")
        for footprint in self.footprints:
            check_refs(footprint.source_ids)
            if footprint.company_id not in companies or footprint.company_id not in {
                sources[s].company_id for s in footprint.source_ids
            }:
                raise ValueError("Geographic example requires a matching company reference")
        return self


def load_applications():
    return ApplicationCatalog.model_validate_json(
        (ROOT / "data/catalog/application-worlds.json").read_text()
    ).model_dump(mode="json")
