from src.retriever import BM25RetrieverRanker
from src import settings
from haystack.document_stores import ElasticsearchDocumentStore
from langchain.memory import ChatMessageHistory
from langchain.schema import BaseMessage
from typing import List, Dict


def make_retriever() -> BM25RetrieverRanker:
    """Creates a BM25RetrieverRanker instance.

    Returns:
        BM25RetrieverRanker
    """
    document_store = ElasticsearchDocumentStore(
        host=settings.ELASTICSEARCH_HOST,
        username="",
        password="",
        index="document",
    )
    return BM25RetrieverRanker(document_store)


def build_message_history(messages: List[Dict[str, str]]) -> List[BaseMessage]:
    """Builds a list of langchain human and AI messages
    from list of dicts containing messages

    Args:
        messages (List[Dict[str, str]]): list of dicts containing messages
        from the chat history. Each dict should contain the role of the message
        (user or assistant) and the content of the message.
        Example:
        [
            {
                "role": "user",
                "content": "Hello"
            },
            {
                "role": "assistant",
                "content": "Hi"
            }
        ]

    Returns:
        List[BaseMessage]
    """
    history = ChatMessageHistory()
    for message in messages:
        if message["role"] == "user":
            history.add_user_message(message["content"])
        else:
            history.add_ai_message(message["content"])
    return history.messages
