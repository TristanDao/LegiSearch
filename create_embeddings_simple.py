# -*- coding: utf-8 -*-
"""
Script đơn giản để tạo embedding cho MongoDB
Chạy trực tiếp: python create_embeddings_simple.py
"""
from libs.create_embeddings import create_embeddings_for_collection, verify_embeddings

if __name__ == "__main__":
    print("=" * 60)
    print("SCRIPT TẠO EMBEDDING CHO MONGODB")
    print("=" * 60)
    
    # Kiểm tra trạng thái trước
    print("\n1. Kiểm tra trạng thái hiện tại:")
    verify_embeddings()
    
    # Hỏi xác nhận
    print("\n" + "=" * 60)
    response = input("\nBạn có muốn tạo embedding cho các documents chưa có embedding? (y/n): ")
    
    if response.lower() in ['y', 'yes', 'có', 'co']:
        print("\n2. Bắt đầu tạo embedding...")
        print("=" * 60)
        
        # Tạo embedding (chỉ cho documents chưa có)
        # Mặc định sẽ kết hợp: van_ban, loai_heading, tieu_de, noi_dung
        create_embeddings_for_collection(
            batch_size=100,
            combine_fields=True,  # Kết hợp nhiều cột để embedding có ý nghĩa hơn
            update_existing=False  # Chỉ tạo cho documents chưa có embedding
        )
        
        # Kiểm tra lại sau khi tạo
        print("\n3. Kiểm tra lại sau khi tạo:")
        verify_embeddings()
        
        print("\n" + "=" * 60)
        print("HOÀN TẤT!")
        print("=" * 60)
    else:
        print("\nĐã hủy. Không có thay đổi nào được thực hiện.")

