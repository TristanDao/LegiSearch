# -*- coding: utf-8 -*-
"""
RAG System for Legal Document Search
Supports keyword search, semantic search, and hybrid search
"""
import os
from typing import List, Dict, Optional, Literal
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from .utils import get_embedding, get_mongodb_collection

# Load environment variables
load_dotenv()

# Search mode type
SearchMode = Literal["keyword", "semantic", "hybrid"]


class LegalRAGSystem:
    """
    RAG System for legal document search and question answering.
    """
    
    def __init__(
        self,
        db_name: Optional[str] = None,
        collection_name: Optional[str] = None,
        num_results: int = 5
    ):
        """
        Initialize RAG system.
        
        Args:
            db_name: MongoDB database name (default from env)
            collection_name: MongoDB collection name (default from env)
            num_results: Number of results to return (default: 5)
        """
        self.collection = get_mongodb_collection(db_name, collection_name)
        self.num_results = num_results
        
        # Initialize Azure OpenAI LLM
        self.llm = self._init_llm()
        
        # Initialize prompt template
        self.prompt_template = self._create_prompt_template()
    
    def _init_llm(self) -> AzureChatOpenAI:
        """
        Initialize Azure OpenAI LLM from environment variables.
        
        Returns:
            AzureChatOpenAI: Initialized LLM
        """
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
        azure_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
        api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
        
        if not all([azure_endpoint, azure_api_key, azure_deployment]):
            raise ValueError(
                "Missing Azure OpenAI configuration. Please set in .env file:\n"
                "- AZURE_OPENAI_ENDPOINT\n"
                "- AZURE_OPENAI_API_KEY\n"
                "- AZURE_OPENAI_DEPLOYMENT_NAME\n"
                "- AZURE_OPENAI_API_VERSION (optional, default: 2024-02-15-preview)"
            )
        
        # Ensure all values are strings (not None)
        assert azure_endpoint is not None
        assert azure_api_key is not None
        assert azure_deployment is not None
        
        return AzureChatOpenAI(
            azure_endpoint=azure_endpoint,
            azure_deployment=azure_deployment,
            api_version=api_version,
            api_key=azure_api_key,  # type: ignore
            temperature=0.7
        )
    
    def _create_prompt_template(self) -> ChatPromptTemplate:
        """
        Create prompt template for legal document Q&A.
        
        Returns:
            ChatPromptTemplate: Prompt template
        """
        template = """Bạn là một trợ lý pháp lý chuyên nghiệp, chuyên trả lời các câu hỏi về pháp luật Việt Nam.

Dựa trên các văn bản pháp luật được cung cấp dưới đây, hãy trả lời câu hỏi một cách chính xác và chi tiết.

Nếu câu trả lời không có trong các văn bản được cung cấp, hãy nói rõ rằng bạn không có thông tin để trả lời câu hỏi này.

Các văn bản pháp luật:
{context}

Câu hỏi: {question}

Hãy trả lời câu hỏi dựa trên các văn bản pháp luật được cung cấp. Nếu có thể, hãy trích dẫn điều, khoản cụ thể.
Trả lời:"""
        
        return ChatPromptTemplate.from_template(template)
    
    def keyword_search(
        self,
        query: str,
        limit: Optional[int] = None
    ) -> List[Dict]:
        """
        Perform keyword-based search using MongoDB text search.
        
        Args:
            query: Search query
            limit: Maximum number of results (default: self.num_results)
            
        Returns:
            List of search results with metadata
        """
        limit = limit or self.num_results
        
        # MongoDB text search (requires text index on 'noi_dung' field)
        # If text index doesn't exist, fall back to regex search
        try:
            results = list(
                self.collection.find(
                    {"$text": {"$search": query}},
                    {"score": {"$meta": "textScore"}}
                ).sort([("score", {"$meta": "textScore"})]).limit(limit)
            )
        except Exception:
            # Fallback to regex search if text index doesn't exist
            results = list(
                self.collection.find(
                    {
                        "$or": [
                            {"tieu_de": {"$regex": query, "$options": "i"}},
                            {"noi_dung": {"$regex": query, "$options": "i"}},
                            {"loai_heading": {"$regex": query, "$options": "i"}}
                        ]
                    }
                ).limit(limit)
            )
        
        # Format results
        formatted_results = []
        for result in results:
            formatted_results.append({
                "van_ban": result.get("van_ban", ""),
                "tieu_de": result.get("tieu_de", ""),
                "loai_heading": result.get("loai_heading", ""),
                "noi_dung": result.get("noi_dung", ""),
                "score": result.get("score", 0.0),
                "search_type": "keyword"
            })
        
        return formatted_results
    
    def semantic_search(
        self,
        query: str,
        limit: Optional[int] = None
    ) -> List[Dict]:
        """
        Perform semantic/vector search using embeddings.
        
        Args:
            query: Search query
            limit: Maximum number of results (default: self.num_results)
            
        Returns:
            List of search results with metadata
        """
        limit = limit or self.num_results
        
        # Generate query embedding
        query_embedding = get_embedding(query)
        if query_embedding is None:
            return []
        
        # MongoDB vector search pipeline
        # Syntax theo MongoDB documentation:
        # https://www.mongodb.com/docs/atlas/atlas-vector-search/vector-search-stage/
        vector_search_stage = {
            "$vectorSearch": {
                "index": "vector_index",  # Tên của vector index
                "path": "embedding",  # Trường chứa vector embedding
                "queryVector": query_embedding,  # Vector query để tìm kiếm
                "numCandidates": min(400, limit * 10),  # Số lượng candidates để xem xét
                "limit": limit,  # Số lượng kết quả trả về
            }
        }
        
        unset_stage = {
            "$unset": "embedding"
        }
        
        project_stage = {
            "$project": {
                "_id": 0,
                "van_ban": 1,
                "tieu_de": 1,
                "loai_heading": 1,
                "noi_dung": 1,
                "score": {"$meta": "vectorSearchScore"}
            }
        }
        
        pipeline = [vector_search_stage, unset_stage, project_stage]
        
        try:
            results = list(self.collection.aggregate(pipeline))
        except Exception as e:
            print(f"Error in vector search: {e}")
            print("Make sure vector index 'vector_index' exists in MongoDB.")
            return []
        
        # Format results
        formatted_results = []
        for result in results:
            formatted_results.append({
                "van_ban": result.get("van_ban", ""),
                "tieu_de": result.get("tieu_de", ""),
                "loai_heading": result.get("loai_heading", ""),
                "noi_dung": result.get("noi_dung", ""),
                "score": result.get("score", 0.0),
                "search_type": "semantic"
            })
        
        return formatted_results
    
    def hybrid_search(
        self,
        query: str,
        limit: Optional[int] = None,
        keyword_weight: float = 0.3,
        semantic_weight: float = 0.7
    ) -> List[Dict]:
        """
        Perform hybrid search combining keyword and semantic search.
        
        Args:
            query: Search query
            limit: Maximum number of results (default: self.num_results)
            keyword_weight: Weight for keyword search scores (default: 0.3)
            semantic_weight: Weight for semantic search scores (default: 0.7)
            
        Returns:
            List of search results with combined scores
        """
        limit = limit or self.num_results
        
        # Perform both searches
        keyword_results = self.keyword_search(query, limit * 2)
        semantic_results = self.semantic_search(query, limit * 2)
        
        # Create a dictionary to combine results
        combined_results = {}
        
        # Process keyword results
        for result in keyword_results:
            key = f"{result['van_ban']}_{result['tieu_de']}"
            if key not in combined_results:
                combined_results[key] = result.copy()
                # Normalize keyword score (assuming max score ~1.0)
                combined_results[key]['keyword_score'] = min(result.get('score', 0.0), 1.0)
                combined_results[key]['semantic_score'] = 0.0
            else:
                combined_results[key]['keyword_score'] = max(
                    combined_results[key].get('keyword_score', 0.0),
                    min(result.get('score', 0.0), 1.0)
                )
        
        # Process semantic results
        for result in semantic_results:
            key = f"{result['van_ban']}_{result['tieu_de']}"
            if key not in combined_results:
                combined_results[key] = result.copy()
                combined_results[key]['keyword_score'] = 0.0
                combined_results[key]['semantic_score'] = result.get('score', 0.0)
            else:
                combined_results[key]['semantic_score'] = max(
                    combined_results[key].get('semantic_score', 0.0),
                    result.get('score', 0.0)
                )
        
        # Calculate combined scores
        for key, result in combined_results.items():
            combined_score = (
                keyword_weight * result.get('keyword_score', 0.0) +
                semantic_weight * result.get('semantic_score', 0.0)
            )
            result['score'] = combined_score
            result['search_type'] = 'hybrid'
        
        # Sort by combined score and return top results
        sorted_results = sorted(
            combined_results.values(),
            key=lambda x: x['score'],
            reverse=True
        )
        
        return sorted_results[:limit]
    
    def search(
        self,
        query: str,
        mode: SearchMode = "semantic",
        limit: Optional[int] = None
    ) -> List[Dict]:
        """
        Perform search based on specified mode.
        
        Args:
            query: Search query
            mode: Search mode - "keyword", "semantic", or "hybrid"
            limit: Maximum number of results
            
        Returns:
            List of search results
        """
        if mode == "keyword":
            return self.keyword_search(query, limit)
        elif mode == "semantic":
            return self.semantic_search(query, limit)
        elif mode == "hybrid":
            return self.hybrid_search(query, limit)
        else:
            raise ValueError(f"Invalid search mode: {mode}. Must be 'keyword', 'semantic', or 'hybrid'")
    
    def generate_answer(
        self,
        query: str,
        search_results: Optional[List[Dict]] = None,
        mode: SearchMode = "semantic",
        limit: Optional[int] = None
    ) -> Dict:
        """
        Generate answer using RAG (Retrieval-Augmented Generation).
        
        Args:
            query: User question
            search_results: Pre-computed search results (optional)
            mode: Search mode if search_results not provided
            limit: Number of results to retrieve if search_results not provided
            
        Returns:
            Dictionary with answer and sources
        """
        # Get search results if not provided
        if search_results is None:
            search_results = self.search(query, mode=mode, limit=limit or self.num_results)
        
        if not search_results:
            return {
                "answer": "Xin lỗi, tôi không tìm thấy thông tin liên quan đến câu hỏi của bạn trong cơ sở dữ liệu.",
                "sources": [],
                "query": query
            }
        
        # Format context from search results
        context_parts = []
        for i, result in enumerate(search_results, 1):
            context_part = f"[{i}] {result.get('tieu_de', '')}\n"
            context_part += f"Văn bản: {result.get('van_ban', '')}\n"
            context_part += f"Nội dung: {result.get('noi_dung', '')[:500]}..."  # Limit content length
            context_parts.append(context_part)
        
        context = "\n\n".join(context_parts)
        
        # Generate answer using LLM
        try:
            messages = self.prompt_template.format_messages(
                context=context,
                question=query
            )
            response = self.llm.invoke(messages)
            answer = response.content
        except Exception as e:
            print(f"Error generating answer: {e}")
            answer = "Xin lỗi, có lỗi xảy ra khi tạo câu trả lời. Vui lòng thử lại."
        
        # Format sources
        sources = [
            {
                "van_ban": r.get("van_ban", ""),
                "tieu_de": r.get("tieu_de", ""),
                "loai_heading": r.get("loai_heading", ""),
                "noi_dung": r.get("noi_dung", ""),  # Thêm noi_dung vào sources
                "score": r.get("score", 0.0),
                "search_type": r.get("search_type", mode)
            }
            for r in search_results
        ]
        
        return {
            "answer": answer,
            "sources": sources,
            "query": query,
            "search_mode": mode
        }


# Convenience functions for easy import
def create_rag_system(
    db_name: Optional[str] = None,
    collection_name: Optional[str] = None,
    num_results: int = 5
) -> LegalRAGSystem:
    """
    Create and return a LegalRAGSystem instance.
    
    Args:
        db_name: MongoDB database name
        collection_name: MongoDB collection name
        num_results: Default number of results
        
    Returns:
        LegalRAGSystem instance
    """
    return LegalRAGSystem(db_name, collection_name, num_results)


def search_legal_documents(
    query: str,
    mode: SearchMode = "semantic",
    db_name: Optional[str] = None,
    collection_name: Optional[str] = None,
    limit: int = 5
) -> List[Dict]:
    """
    Search legal documents.
    
    Args:
        query: Search query
        mode: Search mode - "keyword", "semantic", or "hybrid"
        db_name: MongoDB database name
        collection_name: MongoDB collection name
        limit: Number of results
        
    Returns:
        List of search results
    """
    rag = LegalRAGSystem(db_name, collection_name, limit)
    return rag.search(query, mode, limit)


def ask_legal_question(
    question: str,
    mode: SearchMode = "semantic",
    db_name: Optional[str] = None,
    collection_name: Optional[str] = None,
    limit: int = 5
) -> Dict:
    """
    Ask a legal question and get an AI-generated answer.
    
    Args:
        question: User question
        mode: Search mode - "keyword", "semantic", or "hybrid"
        db_name: MongoDB database name
        collection_name: MongoDB collection name
        limit: Number of documents to retrieve
        
    Returns:
        Dictionary with answer and sources
    """
    rag = LegalRAGSystem(db_name, collection_name, limit)
    return rag.generate_answer(question, mode=mode, limit=limit)

