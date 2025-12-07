# RAG System Documentation

Hệ thống RAG (Retrieval-Augmented Generation) cho tra cứu văn bản pháp luật.

## Cấu hình

### 1. Tạo file `.env`

Tạo file `.env` trong thư mục gốc của project với các biến môi trường sau:

```env
# MongoDB Configuration
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/?appName=AppName
MONGODB_DB_NAME=VNLawsDB
MONGODB_COLLECTION_NAME=VNLawsCollection

# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment-name
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

### 2. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

## Sử dụng

### Cách 1: Sử dụng class LegalRAGSystem

```python
from libs.search import LegalRAGSystem

# Khởi tạo RAG system
rag = LegalRAGSystem(
    db_name="VNLawsDB",
    collection_name="VNLawsCollection",
    num_results=5
)

# Tìm kiếm với chế độ semantic
results = rag.search("Điều kiện cấp sổ đỏ", mode="semantic")

# Tìm kiếm với chế độ keyword
results = rag.search("Điều kiện cấp sổ đỏ", mode="keyword")

# Tìm kiếm với chế độ hybrid
results = rag.search("Điều kiện cấp sổ đỏ", mode="hybrid")

# Hỏi đáp với RAG
answer = rag.generate_answer(
    "Điều kiện để được cấp sổ đỏ là gì?",
    mode="hybrid"
)
print(answer["answer"])
print(answer["sources"])
```
Kết quả trả về là:
return {
    "answer": answer,
    "sources": sources,
    "query": query,
    "search_mode": mode
}
Data trong sources:
sources =  {
                "van_ban"
                "tieu_de",
                "loai_heading",
                "noi_dung",
                "score",
                "search_type"
            }
        


### Cách 2: Sử dụng convenience functions

```python
from libs.search import search_legal_documents, ask_legal_question

# Tìm kiếm đơn giản
results = search_legal_documents(
    query="Điều kiện cấp sổ đỏ",
    mode="semantic",  # hoặc "keyword" hoặc "hybrid"
    limit=5
)

# Hỏi đáp
answer = ask_legal_question(
    question="Điều kiện để được cấp sổ đỏ là gì?",
    mode="hybrid",
    limit=5
)
```

## Các chế độ tìm kiếm

### 1. Keyword Search (`mode="keyword"`)
- Tìm kiếm dựa trên từ khóa chính xác
- Sử dụng MongoDB text search hoặc regex
- Phù hợp khi người dùng biết chính xác từ khóa cần tìm

### 2. Semantic Search (`mode="semantic"`)
- Tìm kiếm dựa trên ngữ nghĩa
- Sử dụng embedding model `keepitreal/vietnamese-sbert`
- Phù hợp khi người dùng hỏi bằng câu hỏi tự nhiên

### 3. Hybrid Search (`mode="hybrid"`)
- Kết hợp cả keyword và semantic search
- Tính điểm kết hợp: `score = 0.3 * keyword_score + 0.7 * semantic_score`
- Phù hợp cho kết quả tốt nhất

## Cấu trúc dữ liệu MongoDB

Collection trong MongoDB cần có cấu trúc:

```json
{
  "van_ban": "LuatBHXH2024.docx",
  "loai_heading": "luat - Điều 1. Phạm vi điều chỉnh",
  "tieu_de": "Điều 1. Phạm vi điều chỉnh",
  "noi_dung": "Nội dung đầy đủ...",
  "embedding": [0.123, 0.456, ...]  // Vector embedding (1536 dimensions)
}
```

## Embedding Model

- Model: `keepitreal/vietnamese-sbert`
- Model sẽ được tự động tải và lưu vào thư mục `models/` khi chạy lần đầu
- Không cần tải model thủ công

## Tạo Embedding cho Documents

Nếu bạn đã có data trong MongoDB nhưng chưa có cột `embedding`, sử dụng script `create_embeddings.py`:

### Cách 1: Script đơn giản (Khuyến nghị)

```bash
python create_embeddings_simple.py
```

Script sẽ:
- Kiểm tra trạng thái hiện tại
- Hỏi xác nhận trước khi tạo
- Tự động tạo embedding cho documents chưa có
- Hiển thị progress bar

### Cách 2: Script với tùy chọn

```bash
# Chỉ kiểm tra
python -m libs.create_embeddings --verify-only

# Tạo embedding cho documents chưa có
python -m libs.create_embeddings

# Tạo lại tất cả (kể cả đã có embedding)
python -m libs.create_embeddings --update-existing
```

Xem chi tiết trong file `libs/EMBEDDING_GUIDE.md`

## Lưu ý

1. **Vector Index**: Đảm bảo MongoDB có vector index tên `vector_index` trên trường `embedding`
   - Dimension: 768 (cho model `keepitreal/vietnamese-sbert`)
   - Similarity: cosine
2. **Text Index** (tùy chọn): Để sử dụng keyword search tốt hơn, tạo text index trên trường `noi_dung`
3. **Azure OpenAI**: Cần có Azure OpenAI resource với deployment đã tạo sẵn
4. **Embedding Model**: Model sẽ tự động tải và lưu vào `models/` folder khi chạy lần đầu

## Ví dụ sử dụng trong Streamlit

```python
import streamlit as st
from libs.search import LegalRAGSystem

# Khởi tạo RAG system (có thể cache)
@st.cache_resource
def get_rag_system():
    return LegalRAGSystem()

rag = get_rag_system()

# UI
query = st.text_input("Nhập câu hỏi:")
mode = st.selectbox("Chế độ tìm kiếm:", ["semantic", "keyword", "hybrid"])

if st.button("Tìm kiếm"):
    result = rag.generate_answer(query, mode=mode)
    st.write(result["answer"])
    st.write("Nguồn:", result["sources"])
```

