# Changelog - Embedding System Updates

## Cập nhật: Kết hợp nhiều cột và dimension

### Thay đổi chính

1. **Dimension**: Cập nhật từ 384 → **768** (theo model `keepitreal/vietnamese-sbert`)

2. **Kết hợp nhiều cột**: Script giờ tự động kết hợp các cột sau để tạo embedding có ý nghĩa hơn:
   - `van_ban`: Tên văn bản
   - `loai_heading`: Loại heading
   - `tieu_de`: Tiêu đề
   - `noi_dung`: Nội dung

### Format kết hợp

```
Văn bản: {van_ban}
Loại: {loai_heading}
Tiêu đề: {tieu_de}
Nội dung: {noi_dung}
```

### Cách sử dụng

**Mặc định (khuyến nghị)**: Kết hợp tất cả các cột
```bash
python create_embeddings_simple.py
# hoặc
python -m libs.create_embeddings
```

**Chỉ dùng noi_dung**: 
```bash
python -m libs.create_embeddings --no-combine-fields
```

### Vector Index MongoDB

Cập nhật dimension khi tạo vector index:

```javascript
db.VNLawsCollection.createSearchIndex({
  "name": "vector_index",
  "definition": {
    "mappings": {
      "dynamic": true,
      "fields": {
        "embedding": {
          "type": "knnVector",
          "dimensions": 768,  // ← Cập nhật từ 384
          "similarity": "cosine"
        }
      }
    }
  }
})
```

### Lợi ích

1. **Embedding có ý nghĩa hơn**: Kết hợp context từ nhiều cột giúp vector search chính xác hơn
2. **Tìm kiếm tốt hơn**: Query có thể match với cả văn bản, tiêu đề, và nội dung
3. **Semantic search tốt hơn**: Model hiểu được mối quan hệ giữa các phần của document

### Files đã cập nhật

- `libs/create_embeddings.py`: Thêm hàm `combine_text_fields()`, cập nhật dimension
- `libs/EMBEDDING_GUIDE.md`: Cập nhật hướng dẫn
- `libs/README.md`: Cập nhật dimension
- `create_embeddings_simple.py`: Sử dụng `combine_fields=True`

