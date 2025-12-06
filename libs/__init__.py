# -*- coding: utf-8 -*-
"""
RAG System for Legal Document Search
"""

from .search import (
    LegalRAGSystem,
    SearchMode,
    create_rag_system,
    search_legal_documents,
    ask_legal_question
)

from .utils import (
    get_embedding_model,
    get_embedding,
    get_mongodb_connection,
    get_mongodb_collection
)

__all__ = [
    # Main classes
    "LegalRAGSystem",
    "SearchMode",
    
    # Convenience functions
    "create_rag_system",
    "search_legal_documents",
    "ask_legal_question",
    
    # Utility functions
    "get_embedding_model",
    "get_embedding",
    "get_mongodb_connection",
    "get_mongodb_collection",
]

__version__ = "1.0.0"

