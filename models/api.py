from models.models import (
    Document,
    DocumentMetadataFilter,
    Query,
    QueryResult,
)
from pydantic import BaseModel
from typing import List, Optional


class UpsertRequest(BaseModel):
    documents: List[Document]


class UpsertResponse(BaseModel):
    ids: List[str]


class QueryRequest(BaseModel):
    queries: List[Query]


class QueryResponse(BaseModel):
    results: List[QueryResult]


class DeleteRequest(BaseModel):
    ids: Optional[List[str]] = None
    filter: Optional[DocumentMetadataFilter] = None
    delete_all: Optional[bool] = False


class DeleteResponse(BaseModel):
    success: bool


class GitSearchRequest(BaseModel):
    url: str
    query: Optional[str] = None
    limit: int = 10


class GitSearchResponse(BaseModel):
    results: List[str]


class GitSearchListRequest(BaseModel):
    include_files: Optional[bool] = None


class GitSearchListResponse(BaseModel):
    results: List[str] | List[Tuple[str, str]]


class GitSearchAddRequest(BaseModel):
    urls: str | List[str]
    filter: Optional[str] = None


class GitSearchAddResponse(BaseModel):
    total_added: int


class GitSearchResetDbRequest(BaseModel):
    pass


class GitSearchResetDbResponse(BaseModel):
    success: bool

