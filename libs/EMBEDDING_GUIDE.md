# Hướng dẫn tạo Embedding cho MongoDB

Script này giúp bạn tạo embedding cho các document đã có trong MongoDB mà chưa có cột `embedding`.

## Cách sử dụng

### 1. Kiểm tra trạng thái hiện tại

```bash
python -m libs.create_embeddings --verify-only
```

Lệnh này sẽ hiển thị:
- Tổng số documents
- Số documents đã có embedding
- Số documents chưa có embedding

### 2. Tạo embedding cho documents chưa có embedding (Khuyến nghị)

```bash
python -m libs.create_embeddings
```

Script sẽ:
- Tự động tìm các documents **chưa có** embedding
- Tạo embedding cho từng document
- Update lại document với embedding mới
- Hiển thị progress bar

### 3. Tạo embedding với tùy chọn

```bash
# Chỉ định database và collection
python -m libs.create_embeddings --db-name VNLawsDB --collection-name VNLawsCollection

# Thay đổi batch size (số documents xử lý mỗi lần)
python -m libs.create_embeddings --batch-size 50

# Chỉ dùng noi_dung, không kết hợp các cột khác
python -m libs.create_embeddings --no-combine-fields

# Update lại tất cả documents (kể cả đã có embedding)
python -m libs.create_embeddings --update-existing
```

### 4. Kết hợp các tùy chọn

```bash
python -m libs.create_embeddings \
    --db-name VNLawsDB \
    --collection-name VNLawsCollection \
    --batch-size 100 \
    --text-field noi_dung
```

## Các tùy chọn

| Tùy chọn | Mô tả | Mặc định |
|----------|-------|----------|
| `--db-name` | Tên database MongoDB | Từ env `MONGODB_DB_NAME` |
| `--collection-name` | Tên collection MongoDB | Từ env `MONGODB_COLLECTION_NAME` |
| `--batch-size` | Số documents xử lý mỗi batch | 100 |
| `--no-combine-fields` | Chỉ dùng noi_dung, không kết hợp các cột khác | False (mặc định kết hợp) |
| `--update-existing` | Update lại documents đã có embedding | False |
| `--verify-only` | Chỉ kiểm tra, không tạo embedding | False |

## Lưu ý

1. **Model embedding**: Script sẽ tự động tải model `keepitreal/vietnamese-sbert` lần đầu chạy và lưu vào `models/` folder

2. **Kết hợp nhiều cột**: Mặc định script sẽ kết hợp các cột sau để tạo embedding có ý nghĩa hơn:
   - `van_ban`: Tên văn bản (context về luật nào)
   - `loai_heading`: Loại heading (context về cấu trúc)
   - `tieu_de`: Tiêu đề (heading chính)
   - `noi_dung`: Nội dung (nội dung chính)
   
   Format kết hợp:
   ```
   Văn bản: {van_ban}
   Loại: {loai_heading}
   Tiêu đề: {tieu_de}
   Nội dung: {noi_dung}
   ```
   
   Nếu muốn chỉ dùng `noi_dung`, dùng flag `--no-combine-fields`

4. **An toàn**: Script chỉ update documents chưa có embedding (trừ khi dùng `--update-existing`), không xóa hay thay đổi data hiện có

5. **Vector index**: Sau khi tạo embedding, đảm bảo tạo vector index trong MongoDB:

   **Option 1: Không có filter (Đơn giản, khuyến nghị cho bắt đầu)**
   ```javascript
   // Trong MongoDB Atlas hoặc MongoDB Shell
   db.VNLawsCollection.createSearchIndex({
     "name": "vector_index",
     "definition": {
       "mappings": {
         "dynamic": true,
         "fields": {
           "embedding": {
             "type": "knnVector",
             "dimensions": 768,  // Dimension của keepitreal/vietnamese-sbert
             "similarity": "cosine"
           }
         }
       }
     }
   })
   ```

   **Option 2: Có filter fields (Nâng cao, cho phép filter kết quả)**
   ```javascript
   // Cho phép filter theo van_ban, loai_heading khi search
   db.VNLawsCollection.createSearchIndex({
     "name": "vector_index",
     "definition": {
       "mappings": {
         "dynamic": true,
         "fields": {
           "embedding": {
             "type": "knnVector",
             "dimensions": 768,
             "similarity": "cosine"
           },
           "van_ban": {
             "type": "token"
           },
           "loai_heading": {
             "type": "token"
           }
         }
       }
     }
   })
   ```

   **Filter field có cần không?**
   - **KHÔNG BẮT BUỘC**: Nếu bạn chỉ cần semantic search đơn giản, không cần filter
   - **NÊN DÙNG** nếu bạn muốn:
     - Filter kết quả theo văn bản cụ thể (ví dụ: chỉ tìm trong "LuatBHXH2024.docx")
     - Filter theo loại heading (ví dụ: chỉ tìm "luat" hoặc "nghị định")
     - Tăng tốc độ search khi có nhiều data
   
   **Ví dụ sử dụng filter trong code:**
   ```python
   # Search với filter theo van_ban
   vector_search_stage = {
       "$vectorSearch": {
           "index": "vector_index",
           "queryVector": query_embedding,
           "path": "embedding",
           "filter": {
               "van_ban": "LuatBHXH2024.docx"  # Chỉ tìm trong văn bản này
           },
           "numCandidates": 400,
           "limit": limit,
       }
   }
   ```

## Ví dụ output

```
Mode: Only processing documents WITHOUT embeddings

Total documents to process: 1500

Starting embedding creation...
Text field: noi_dung
Batch size: 100

Creating embeddings: 100%|████████████| 1500/1500 [05:23<00:00,  4.65it/s]

==================================================
Embedding creation completed!
Processed: 1500
Failed: 0
Total: 1500
==================================================

==================================================
Embedding Status:
Total documents: 1500
With embedding: 1500
Without embedding: 0
==================================================

Embedding dimension: 768
Expected dimension: 768 (keepitreal/vietnamese-sbert)
Sample document: Điều 1. Phạm vi điều chỉnh...
```

## Xử lý lỗi

Nếu gặp lỗi:
1. Kiểm tra kết nối MongoDB trong `.env`
2. Kiểm tra model embedding có tải được không
3. Kiểm tra trường `noi_dung` có tồn tại trong documents không
4. Xem log chi tiết để biết document nào bị lỗi

