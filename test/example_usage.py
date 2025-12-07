# -*- coding: utf-8 -*-
"""
Example usage of the RAG system
This file demonstrates how to use the LegalRAGSystem
Chạy: python example_usage.py
"""
from libs.search import LegalRAGSystem, search_legal_documents, ask_legal_question

def example_basic_search():
    """Example: Basic search functionality"""
    print("=" * 50)
    print("Example 1: Basic Search")
    print("=" * 50)
    
    # Initialize RAG system
    rag = LegalRAGSystem(num_results=3)
    
    # Search with different modes
    query = "trợ cấp hưu trí"
    
    print(f"\nQuery: {query}")
    
    # Semantic search
    print("\n--- Semantic Search ---")
    try:
        results = rag.search(query, mode="semantic")
        if results:
            print(f"Tìm thấy {len(results)} kết quả:\n")
            for i, result in enumerate(results, 1):
                print(f"{i}. {result['tieu_de']}")
                print(f"   Score: {result['score']:.4f}")
                print(f"   Văn bản: {result['van_ban']}")
                print()
        else:
            print("⚠️  Không tìm thấy kết quả nào!")
            print("   Kiểm tra:")
            print("   - Vector index 'vector_index' đã được tạo chưa?")
            print("   - Documents đã có embedding chưa?")
            print("   - Kết nối MongoDB có đúng không?")
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()
    
    # Keyword search
    print("\n--- Keyword Search ---")
    try:
        results = rag.search(query, mode="keyword")
        if results:
            print(f"Tìm thấy {len(results)} kết quả:\n")
            for i, result in enumerate(results, 1):
                print(f"{i}. {result['tieu_de']}")
                print(f"   Score: {result['score']:.4f}")
                print()
        else:
            print("⚠️  Không tìm thấy kết quả nào!")
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()
    
    # Hybrid search
    print("\n--- Hybrid Search ---")
    try:
        results = rag.search(query, mode="hybrid")
        if results:
            print(f"Tìm thấy {len(results)} kết quả:\n")
            for i, result in enumerate(results, 1):
                print(f"{i}. {result['tieu_de']}")
                print(f"   Score: {result['score']:.4f}")
                print()
        else:
            print("⚠️  Không tìm thấy kết quả nào!")
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()


def example_qa():
    """Example: Question answering with RAG"""
    print("=" * 50)
    print("Example 2: Question Answering")
    print("=" * 50)
    
    rag = LegalRAGSystem(num_results=5)
    
    questions = [
        "Điều kiện để được hưởng trợ cấp hưu trí là gì?",
        "Ai được tham gia bảo hiểm xã hội bắt buộc?",
    ]
    
    for question in questions:
        print(f"\nQuestion: {question}")
        print("-" * 50)
        
        # Generate answer with hybrid search
        result = rag.generate_answer(question, mode="hybrid")
        
        print(f"Answer: {result['answer']}")

        print(f"\nSources ({len(result['sources'])} documents):")
        for i, source in enumerate(result['sources'], 1):
            print(f"   {i}. {source['tieu_de']} (Score: {source['score']:.4f})")
            print(f"   Văn bản: {source['van_ban']}")
            print(f"   Loại: {source['loai_heading']}")
            print(f"   Nội dung: {source['noi_dung'][:500]}...")
            print()


def example_convenience_functions():
    """Example: Using convenience functions"""
    print("=" * 50)
    print("Example 3: Convenience Functions")
    print("=" * 50)
    
    # Simple search
    results = search_legal_documents(
        query="trợ cấp hưu trí",
        mode="semantic",
        limit=3
    )
    
    print(f"Found {len(results)} results")
    for result in results:
        print(f"- {result['tieu_de']}")
    
    # Simple Q&A
    answer = ask_legal_question(
        question="Trợ cấp hưu trí gồm những gì?",
        mode="hybrid",
        limit=5
    )
    
    print(f"\nAnswer: {answer['answer']}")


if __name__ == "__main__":
    print("=" * 60)
    print("RAG SYSTEM - EXAMPLE USAGE")
    print("=" * 60)
    print("\nChọn example để chạy:")
    print("1. Basic Search (tìm kiếm cơ bản)")
    print("2. Question Answering (hỏi đáp với RAG)")
    print("3. Convenience Functions (hàm tiện ích)")
    print("\nHoặc uncomment function trong code để chạy tự động.")
    print("\n" + "=" * 60)
    
    # Uncomment example bạn muốn chạy:
    
    # example_basic_search()
    example_qa()
    # example_convenience_functions()
    
    print("\n⚠️  Lưu ý:")
    print("1. Đảm bảo đã tạo file .env với MongoDB và Azure OpenAI credentials")
    print("2. Đã cài đặt dependencies: pip install -r requirements.txt")
    print("3. MongoDB collection có vector index 'vector_index' trên field 'embedding'")
    print("4. Uncomment một trong các hàm example_*() ở trên để chạy")
    print("\n" + "=" * 60)

