"""Discovery metadata, separate from authoritative financial facts and retrieval evidence."""

import ipaddress
import json
from datetime import date, datetime
from typing import Literal
from urllib.parse import urlsplit

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from semiconductor_research.config.settings import ROOT


class Record(BaseModel):
    model_config = ConfigDict(extra="forbid")


def public_url(value):
    if value is None:
        return value
    parts = urlsplit(value)
    if (
        parts.scheme != "https"
        or not parts.hostname
        or parts.username
        or parts.password
        or parts.port not in {None, 443}
        or parts.hostname in {"localhost", "localhost.localdomain"}
        or parts.hostname.endswith((".local", ".localhost", ".internal"))
    ):
        raise ValueError("Directory destinations must be public HTTPS URLs without credentials")
    try:
        ipaddress.ip_address(parts.hostname)
    except ValueError:
        if "." not in parts.hostname:
            raise ValueError("A public DNS name is required") from None
    else:
        raise ValueError("IP-literal directory destinations are not allowed")
    return value


class Category(Record):
    id: str = Field(pattern=r"^[a-z][a-z0-9-]*$")
    label: str
    description: str
    color: str = Field(pattern=r"^#[0-9a-fA-F]{6}$")


class ResourceCategory(Record):
    id: str
    label: str


class Company(Record):
    id: str = Field(pattern=r"^[a-z][a-z0-9-]*$")
    name: str = Field(min_length=1, max_length=100)
    roles: list[str] = Field(min_length=1)
    focus: str = Field(min_length=1, max_length=250)
    website: str
    investor_url: str | None
    financial_company_id: Literal["NVDA", "TSM", "ASML", "MU", "TXN", "AMKR"] | None
    validate_urls = field_validator("website", "investor_url")(public_url)


class Resource(Record):
    id: str
    title: str
    publisher: str
    category: str
    url: str
    description: str
    access: Literal["public", "mixed"]
    roles: list[str]
    validate_url = field_validator("url")(public_url)


class Directory(Record):
    version: str
    catalog_date: date
    scope: str
    financial_coverage_note: str
    categories: list[Category]
    resource_categories: list[ResourceCategory]
    companies: list[Company]
    resources: list[Resource]

    @model_validator(mode="after")
    def valid_references(self):
        roles = {c.id for c in self.categories}
        resource_roles = {c.id for c in self.resource_categories}
        for collection in (
            self.categories,
            self.resource_categories,
            self.companies,
            self.resources,
        ):
            identifiers = [c.id for c in collection]
            if len(identifiers) != len(set(identifiers)):
                raise ValueError("Duplicate directory IDs")
        for company in self.companies:
            if not set(company.roles) <= roles or len(set(company.roles)) != len(company.roles):
                raise ValueError("Unknown or duplicate company role")
        finance_ids = [c.financial_company_id for c in self.companies if c.financial_company_id]
        if len(finance_ids) != len(set(finance_ids)):
            raise ValueError("Duplicate financial company mapping")
        for resource in self.resources:
            if resource.category not in resource_roles or not set(resource.roles) <= roles:
                raise ValueError("Unknown resource category or role")
        return self


def load_directory(financial_companies=()):
    catalog = Directory.model_validate_json(
        (ROOT / "data/catalog/semiconductor-directory.json").read_text()
    ).model_dump(mode="json")
    allowed = {c["website"] for c in catalog["companies"]}
    allowed.update(c["investor_url"] for c in catalog["companies"] if c["investor_url"])
    allowed.update(r["url"] for r in catalog["resources"])
    audit_path = ROOT / "data/catalog/directory-links.json"
    links = []
    if audit_path.exists():
        audit = json.loads(audit_path.read_text())
        for row in audit["results"]:
            if row["url"] not in allowed:
                continue
            if row["state"] not in {
                "responded",
                "redirect",
                "restricted",
                "not_found",
                "error",
                "not_requested",
            }:
                raise ValueError("Invalid link observation state")
            datetime.fromisoformat(row["checked_at"])
            links.append({key: row[key] for key in ("url", "checked_at", "status", "state")})
    catalog["link_observations"] = links
    for company in catalog["companies"]:
        company["financial_loaded"] = company["financial_company_id"] in set(financial_companies)
    return catalog
