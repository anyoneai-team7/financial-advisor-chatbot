from src.retriever import BM25RetrieverRanker
from src import settings
from haystack.document_stores import ElasticsearchDocumentStore
from typing import List, Dict


def make_retriever() -> BM25RetrieverRanker:
    document_store = ElasticsearchDocumentStore(
        host=settings.ELASTICSEARCH_HOST,
        username="",
        password="",
        index="document",
    )
    return BM25RetrieverRanker(document_store)


def build_message_history(messages: List[Dict[str, str]]) -> str:
    history = ""
    if len(messages) > 0:
        history = " \n ".join(
            [f"{item['role']}: {item['content']}" for item in messages]
        )
    return history
