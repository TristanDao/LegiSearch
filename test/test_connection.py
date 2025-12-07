# -*- coding: utf-8 -*-
"""
Script kiểm tra kết nối và cấu hình RAG system
Chạy: python test_connection.py
"""
import os
from dotenv import load_dotenv

load_dotenv()

def test_mongodb():
    """Kiểm tra kết nối MongoDB"""
    print("=" * 60)
    print("KIỂM TRA MONGODB")
    print("=" * 60)
    
    try:
        from libs.utils import get_mongodb_collection
        
        mongo_url = os.getenv("MONGODB_URL")
        db_name = os.getenv("MONGODB_DB_NAME", "VNLawsDB")
        collection_name = os.getenv("MONGODB_COLLECTION_NAME", "VNLawsCollection")
        
        print(f"\n1. MongoDB URL: {'✓ Đã cấu hình' if mongo_url else '✗ Chưa cấu hình'}")
        print(f"2. Database: {db_name}")
        print(f"3. Collection: {collection_name}")
        
        if not mongo_url:
            print("\n❌ MONGODB_URL chưa được cấu hình trong .env file!")
            return False
        
        # Test connection
        print("\n4. Đang kiểm tra kết nối...")
        collection = get_mongodb_collection(db_name, collection_name)
        
        # Count documents
        total_docs = collection.count_documents({})
        print(f"   ✓ Kết nối thành công!")
        print(f"   ✓ Tổng số documents: {total_docs}")
        
        # Check documents with embedding - cách đơn giản nhất
        # Tìm một document có embedding để kiểm tra
        sample_with_embedding = collection.find_one({"embedding": {"$exists": True}})
        
        if sample_with_embedding and 'embedding' in sample_with_embedding:
            embedding = sample_with_embedding['embedding']
            if embedding is not None and isinstance(embedding, list) and len(embedding) > 0:
                # Có embedding hợp lệ, đếm tất cả
                docs_with_embedding = collection.count_documents({"embedding": {"$exists": True}})
                print(f"   ✓ Documents có embedding: {docs_with_embedding}")
                print(f"   ✓ Embedding dimension: {len(embedding)}")
            else:
                docs_with_embedding = 0
                print(f"   ⚠️  Documents có field 'embedding' nhưng không hợp lệ")
        else:
            docs_with_embedding = 0
            print(f"   ⚠️  Không tìm thấy document nào có field 'embedding'")
        
        docs_without_embedding = total_docs - docs_with_embedding
        if docs_without_embedding > 0:
            print(f"   ⚠️  Documents chưa có embedding: {docs_without_embedding}")
        
        # Check sample document để debug
        sample = collection.find_one()
        if sample:
            print(f"\n5. Sample document (để debug):")
            print(f"   - _id: {sample.get('_id', 'N/A')}")
            print(f"   - van_ban: {sample.get('van_ban', 'N/A')}")
            print(f"   - tieu_de: {sample.get('tieu_de', 'N/A')[:50]}...")
            
            # Kiểm tra embedding chi tiết
            if 'embedding' in sample:
                embedding = sample['embedding']
                if embedding is None:
                    print(f"   - embedding: ✗ NULL")
                elif not isinstance(embedding, list):
                    print(f"   - embedding: ✗ Không phải array (type: {type(embedding).__name__})")
                elif len(embedding) == 0:
                    print(f"   - embedding: ✗ Array rỗng")
                else:
                    print(f"   - embedding: ✓ Array có {len(embedding)} phần tử")
                    print(f"   - embedding dimension: {len(embedding)}")
                    print(f"   - embedding type: {type(embedding[0]).__name__}")
            else:
                print(f"   - embedding: ✗ Không có field 'embedding'")
            
            # Kiểm tra tất cả fields
            print(f"   - Tất cả fields: {list(sample.keys())}")
        
        if docs_without_embedding > 0 and docs_with_embedding == 0:
            print(f"\n   💡 Chạy: python create_embeddings_simple.py để tạo embedding")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Lỗi kết nối MongoDB: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_vector_index():
    """Kiểm tra vector index bằng cách test trực tiếp vector search"""
    print("\n" + "=" * 60)
    print("KIỂM TRA VECTOR INDEX")
    print("=" * 60)
    
    try:
        from libs.utils import get_mongodb_collection, get_embedding
        
        db_name = os.getenv("MONGODB_DB_NAME", "VNLawsDB")
        collection_name = os.getenv("MONGODB_COLLECTION_NAME", "VNLawsCollection")
        
        collection = get_mongodb_collection(db_name, collection_name)
        
        # Kiểm tra có documents với embedding không - cách đơn giản
        sample_with_embedding = collection.find_one({"embedding": {"$exists": True}})
        
        if not sample_with_embedding or 'embedding' not in sample_with_embedding:
            print("\n⚠️  Không tìm thấy document nào có field 'embedding'!")
            print("   💡 Chạy: python create_embeddings_simple.py để tạo embedding")
            return False
        
        embedding = sample_with_embedding['embedding']
        if embedding is None:
            print("\n⚠️  Document có field 'embedding' nhưng giá trị = NULL!")
            print("   💡 Chạy: python create_embeddings_simple.py để tạo embedding")
            return False
        
        if not isinstance(embedding, list):
            print(f"\n⚠️  Embedding không phải array (type: {type(embedding).__name__})!")
            return False
        
        if len(embedding) == 0:
            print("\n⚠️  Embedding là array rỗng!")
            return False
        
        # Đếm tất cả documents có embedding
        docs_with_embedding = collection.count_documents({"embedding": {"$exists": True}})
        print(f"\n1. Documents có embedding: {docs_with_embedding} ✓")
        print(f"   - Embedding dimension: {len(embedding)}")
        
        # Test vector search trực tiếp (cách tốt nhất để kiểm tra index)
        print("\n2. Đang test vector search...")
        
        # Tạo test embedding
        test_query = "test"
        query_embedding = get_embedding(test_query)
        
        if query_embedding is None:
            print("   ❌ Không tạo được embedding để test")
            return False
        
        print(f"   ✓ Đã tạo test embedding (dimension: {len(query_embedding)})")
        
        # Test vector search pipeline
        try:
            pipeline = [
                {
                    "$vectorSearch": {
                        "index": "vector_index",
                        "path": "embedding",
                        "queryVector": query_embedding,
                        "numCandidates": 10,
                        "limit": 1
                    }
                },
                {
                    "$project": {
                        "_id": 0,
                        "tieu_de": 1,
                        "score": {"$meta": "vectorSearchScore"}
                    }
                }
            ]
            
            results = list(collection.aggregate(pipeline))
            
            if results:
                print(f"   ✓ Vector search thành công!")
                print(f"   ✓ Tìm thấy {len(results)} kết quả test")
                print(f"   ✓ Vector index 'vector_index' đang hoạt động!")
                return True
            else:
                print("   ⚠️  Vector search chạy được nhưng không có kết quả")
                print("   (Có thể do data hoặc query không phù hợp)")
                print("   ✓ Vector index 'vector_index' đang hoạt động!")
                return True
                
        except Exception as e:
            error_msg = str(e).lower()
            
            # Phân tích lỗi
            if "index" in error_msg or "vector_index" in error_msg:
                print(f"   ❌ Lỗi: {e}")
                print("\n   ⚠️  Vector index 'vector_index' chưa tồn tại hoặc chưa sẵn sàng!")
                print("   💡 Tạo vector index trong MongoDB Atlas:")
                print("   1. Vào MongoDB Atlas")
                print("   2. Chọn Database > Search Indexes")
                print("   3. Create Search Index > JSON Editor")
                print("   4. Dán code từ libs/EMBEDDING_GUIDE.md")
                print("   5. Đợi index build xong (có thể mất vài phút)")
            elif "dimension" in error_msg:
                print(f"   ❌ Lỗi dimension: {e}")
                print("   💡 Kiểm tra dimension trong vector index phải là 768")
            else:
                print(f"   ❌ Lỗi không xác định: {e}")
                print("   💡 Kiểm tra lại cấu hình vector index")
            
            return False
        
    except Exception as e:
        print(f"\n❌ Lỗi kiểm tra vector index: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_azure_openai():
    """Kiểm tra Azure OpenAI config"""
    print("\n" + "=" * 60)
    print("KIỂM TRA AZURE OPENAI")
    print("=" * 60)
    
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
    
    print(f"\n1. Endpoint: {'✓ Đã cấu hình' if endpoint else '✗ Chưa cấu hình'}")
    print(f"2. API Key: {'✓ Đã cấu hình' if api_key else '✗ Chưa cấu hình'}")
    print(f"3. Deployment: {'✓ Đã cấu hình' if deployment else '✗ Chưa cấu hình'}")
    print(f"4. API Version: {api_version}")
    
    if all([endpoint, api_key, deployment]):
        print("\n✓ Tất cả thông tin Azure OpenAI đã được cấu hình")
        return True
    else:
        print("\n❌ Thiếu thông tin Azure OpenAI trong .env file!")
        return False


def test_embedding_model():
    """Kiểm tra embedding model"""
    print("\n" + "=" * 60)
    print("KIỂM TRA EMBEDDING MODEL")
    print("=" * 60)
    
    try:
        from libs.utils import get_embedding_model, get_embedding
        
        print("\n1. Đang tải model...")
        model = get_embedding_model()
        print("   ✓ Model đã được tải")
        
        print("\n2. Test tạo embedding...")
        test_text = "trợ cấp hưu trí"
        embedding = get_embedding(test_text)
        
        if embedding:
            print(f"   ✓ Tạo embedding thành công")
            print(f"   ✓ Dimension: {len(embedding)}")
            return True
        else:
            print("   ❌ Không tạo được embedding")
            return False
            
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("RAG SYSTEM - DIAGNOSTIC TOOL")
    print("=" * 60)
    
    results = {
        "MongoDB": test_mongodb(),
        "Vector Index": test_vector_index(),
        "Azure OpenAI": test_azure_openai(),
        "Embedding Model": test_embedding_model()
    }
    
    print("\n" + "=" * 60)
    print("TÓM TẮT")
    print("=" * 60)
    
    for name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{name}: {status}")
    
    all_pass = all(results.values())
    
    if all_pass:
        print("\n✓ Tất cả kiểm tra đều PASS! Hệ thống sẵn sàng.")
    else:
        print("\n⚠️  Một số kiểm tra FAIL. Vui lòng xem chi tiết ở trên.")
        print("\nCác bước tiếp theo:")
        if not results["MongoDB"]:
            print("1. Kiểm tra MONGODB_URL trong .env file")
        if not results["Vector Index"]:
            print("2. Tạo vector index trong MongoDB Atlas")
        if not results["Azure OpenAI"]:
            print("3. Thêm thông tin Azure OpenAI vào .env file")
        if not results["Embedding Model"]:
            print("4. Kiểm tra model embedding có tải được không")
    
    print("\n" + "=" * 60)


