from typing import List
from langchain.retrievers import ElasticSearchBM25Retriever
from langchain.docstore.document import Document
from haystack.document_stores import ElasticsearchDocumentStore
from haystack.nodes import BM25Retriever, SentenceTransformersRanker
from haystack import Pipeline


class BM25RetrieverRanker(ElasticSearchBM25Retriever):
    def __init__(
        self,
        document_store: ElasticsearchDocumentStore,
        retriever_top_k: int = 15,
        ranker_top_k: int = 5,
    ):
        self.document_store = document_store
        self.retriever_top_k = retriever_top_k
        self.ranker_top_k = ranker_top_k

    def _make_retriever_ranker_pipeline(self) -> Pipeline:
        """Builds a pipeline composed of a BM25 retriever and a cross-encoder ranker

        Returns:
            Pipeline
        """
        retriever = BM25Retriever(
            document_store=self.document_store, top_k=self.retriever_top_k
        )
        ranker = SentenceTransformersRanker(
            model_name_or_path="cross-encoder/ms-marco-MiniLM-L-12-v2",
            top_k=self.ranker_top_k,
        )
        pipeline = Pipeline()
        pipeline.add_node(component=retriever, name="Retriever", inputs=["Query"])
        pipeline.add_node(component=ranker, name="Ranker", inputs=["Retriever"])
        return pipeline

    def get_relevant_documents(self, query: str) -> List[Document]:
        """Retrieves relevant documents using the retriever-ranker pipeline

        Args:
            query (str): query to use for document retrieval

        Returns:
            List[Document]: relevant documents for the given query
        """
        pipeline = self._make_retriever_ranker_pipeline()
        res = pipeline.run(query)
        docs = []
        for doc in res["documents"]:
            metadata = {
                "company": doc.meta["company"],
                "year": doc.meta["year"],
                "source": doc.meta["filename"],
            }
            docs.append(Document(page_content=doc.content, metadata=metadata))
        return docs
