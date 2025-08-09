"""Service for retrieval"""

import os
from typing import List, Tuple
from jinja2 import Template

from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.documents import Document

from services.llm_service.llm_interface import LLMInterface


class RetrievalService:
    def __init__(self, vector_store: InMemoryVectorStore, llm_interface: LLMInterface):
        self.vector_store = vector_store
        self.llm_interface = llm_interface
        self._prompt_path = os.path.join(os.path.dirname(__file__), "prompt.yaml")

    def _render_prompt(self, query: str, docs_with_scores: List[Tuple[Document, float]]) -> str:
        # Prepare documents for the template
        documents = []
        for doc, score in docs_with_scores:
            meta = doc.metadata or {}
            documents.append(
                {
                    "id": meta.get("id"),
                    "page_content": doc.page_content,
                    "metadata": {
                        "source": meta.get("source") or meta.get("filename") or "unknown",
                        "page": meta.get("page", "n/a"),
                    },
                    "score": score,
                }
            )

        with open(self._prompt_path, "r", encoding="utf-8") as f:
            template_text = f.read()

        # Render the YAML template as plain text
        tmpl = Template(template_text)
        return tmpl.render(query=query, documents=documents)

    async def retrieve(self, query: str, k: int = 5) -> dict:
        # Get documents with scores for better transparency
        docs_with_scores = self.vector_store.similarity_search_with_score(query, k=k)

        # Render the full prompt (system + user sections as one string)
        prompt = self._render_prompt(query, docs_with_scores)

        # Call the LLM
        llm_response = self.llm_interface.generate_response(prompt=prompt)

        # Normalize output to string (AIMessage vs str)
        content = getattr(llm_response, "content", None) or str(llm_response)

        return {
            "query": query,
            "answer": content,
            "num_context": len(docs_with_scores),
        }