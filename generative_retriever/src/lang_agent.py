import os
from langchain.llms import Cohere
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from haystack.document_stores import ElasticsearchDocumentStore
from src.retriever import BM25RetrieverRanker
from langchain.agents import initialize_agent, Tool


def make_retriever():
    document_store = ElasticsearchDocumentStore(
        host=os.environ.get("ELASTICSEARCH_HOST", "localhost"),
        username="",
        password="",
        index="document",
    )
    return BM25RetrieverRanker(document_store)


def make_agent():
    llm = ChatOpenAI(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        model_name="gpt-3.5-turbo",
        temperature=0.0,
    )

    # retrieval qa chain
    qa = RetrievalQA.from_chain_type(
        llm=llm, chain_type="stuff", retriever=make_retriever()
    )

    tools = [
        Tool(
            name="Knowledge Base",
            func=qa.run,
            description=(
                "use this tool when answering general knowledge queries to get "
                "more information about the topic"
            ),
        )
    ]

    agent = initialize_agent(
        agent="chat-conversational-react-description",
        tools=tools,
        llm=llm,
        max_iterations=3,
        early_stopping_method="generate",
    )
    return agent
