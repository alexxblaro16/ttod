from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class AuthUser(BaseModel):
    id: str
    email: str
    role: Literal["admin", "user"]


class AuthLoginRequest(BaseModel):
    email: str = Field(min_length=3, max_length=254)
    password: str = Field(min_length=1, max_length=1024)


class AuthLoginResponse(BaseModel):
    access_token: str
    token_type: Literal["Bearer"] = "Bearer"
    expires_in: int
    user: AuthUser


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


class OracleResponseChunk(BaseModel):
    mode: Literal["grounded", "creative"]
    citedQuoteIds: list[str] | None = None
    themes: list[str] | None = None
    tags: list[str] | None = None
    text: str

