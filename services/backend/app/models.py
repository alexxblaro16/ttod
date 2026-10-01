from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class OracleQueryPayload(BaseModel):
    query: str = Field(min_length=1, max_length=8000)
    contextTag: str | None = None
    sessionHistory: list[str] = Field(default_factory=list, max_length=50)
    locale: Literal["en", "es"] | None = None


class OracleProposeRequest(BaseModel):
    query: str = Field(min_length=1, max_length=8000)
    creativeAnswer: str = Field(min_length=1, max_length=16000)
    suggestedSection: str | None = None
    suggestedTags: list[str] | None = None
    locale: Literal["en", "es"] | None = None


class ProposalRequest(BaseModel):
    text: str = Field(min_length=1, max_length=16000)
    section: str = Field(min_length=1)
    level: Literal["beginner", "intermediate", "advanced", "master"] = "intermediate"
    origin: Literal["human", "studio", "blackbox"] = "human"
    lang: Literal["en", "es"] = "en"
    tags: list[str] = Field(default_factory=list)
    teaches: str | None = None
    source: str | None = None


class OracleResponseChunk(BaseModel):
    mode: Literal["grounded", "creative"]
    citedQuoteIds: list[str] | None = None
    themes: list[str] | None = None
    tags: list[str] | None = None
    text: str

