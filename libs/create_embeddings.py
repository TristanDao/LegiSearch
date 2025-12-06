# -*- coding: utf-8 -*-
"""
Script to create embeddings for existing MongoDB documents
Selects documents without embeddings, creates embeddings, and updates them
"""
import os
from typing import Optional
from tqdm import tqdm
from dotenv import load_dotenv
from libs.utils import get_mongodb_collection, get_embedding

# Load environment variables
load_dotenv()


def combine_text_fields(doc: dict, combine_fields: bool = True) -> str:
    """
    Combine multiple text fields to create a meaningful text for embedding.
    
    Args:
        doc: MongoDB document
        combine_fields: If True, combine van_ban, loai_heading, tieu_de, noi_dung
        
    Returns:
        Combined text string
    """
    if not combine_fields:
        # Only use noi_dung if combine_fields is False
        return doc.get("noi_dung", "").strip()
    
    # Combine multiple fields in a meaningful order
    parts = []
    
    # 1. Văn bản (document name) - provides context about the law
    van_ban = doc.get("van_ban", "").strip()
    if van_ban:
        parts.append(f"Văn bản: {van_ban}")
    
    # 2. Loại heading - provides structural context
    loai_heading = doc.get("loai_heading", "").strip()
    if loai_heading:
        parts.append(f"Loại: {loai_heading}")
    
    # 3. Tiêu đề - main title/heading
    tieu_de = doc.get("tieu_de", "").strip()
    if tieu_de:
        parts.append(f"Tiêu đề: {tieu_de}")
    
    # 4. Nội dung - main content
    noi_dung = doc.get("noi_dung", "").strip()
    if noi_dung:
        parts.append(f"Nội dung: {noi_dung}")
    
    # Combine all parts with newlines for better separation
    combined_text = "\n".join(parts)
    
    # Fallback: if no fields found, return empty string
    if not combined_text.strip():
        return ""
    
    return combined_text


def create_embeddings_for_collection(
    db_name: Optional[str] = None,
    collection_name: Optional[str] = None,
    batch_size: int = 100,
    combine_fields: bool = True,
    update_existing: bool = False
):
    """
    Create embeddings for documents in MongoDB collection.
    Combines multiple fields (van_ban, loai_heading, tieu_de, noi_dung) for better semantic meaning.
    
    Args:
        db_name: MongoDB database name (default from env)
        collection_name: MongoDB collection name (default from env)
        batch_size: Number of documents to process in each batch
        combine_fields: If True, combine van_ban, loai_heading, tieu_de, noi_dung (default: True)
        update_existing: If True, update documents that already have embeddings (default: False)
    """
    collection = get_mongodb_collection(db_name, collection_name)
    
    # Query documents without embeddings or all documents if update_existing=True
    if update_existing:
        query = {}
        print("Mode: Updating ALL documents (including those with existing embeddings)")
    else:
        query = {"embedding": {"$exists": False}}
        print("Mode: Only processing documents WITHOUT embeddings")
    
    # Count total documents to process
    total_docs = collection.count_documents(query)
    print(f"\nTotal documents to process: {total_docs}")
    
    if total_docs == 0:
        print("No documents to process. Exiting.")
        return
    
    # Process documents in batches
    processed = 0
    failed = 0
    
    # Use cursor with batch_size
    cursor = collection.find(query).batch_size(batch_size)
    
    print(f"\nStarting embedding creation...")
    if combine_fields:
        print("Combining fields: van_ban, loai_heading, tieu_de, noi_dung")
    else:
        print("Using only: noi_dung")
    print(f"Batch size: {batch_size}\n")
    
    # Process with progress bar
    with tqdm(total=total_docs, desc="Creating embeddings") as pbar:
        for doc in cursor:
            try:
                # Combine text fields
                text_to_embed = combine_text_fields(doc, combine_fields)
                
                if not text_to_embed or not text_to_embed.strip():
                    print(f"\nWarning: Document {doc.get('_id')} has no text to embed. Skipping.")
                    failed += 1
                    pbar.update(1)
                    continue
                
                # Create embedding
                embedding = get_embedding(text_to_embed)
                
                if embedding is None:
                    print(f"\nWarning: Failed to create embedding for document {doc.get('_id')}")
                    failed += 1
                    pbar.update(1)
                    continue
                
                # Update document with embedding
                collection.update_one(
                    {"_id": doc["_id"]},
                    {"$set": {"embedding": embedding}}
                )
                
                processed += 1
                pbar.update(1)
                
            except Exception as e:
                print(f"\nError processing document {doc.get('_id')}: {e}")
                failed += 1
                pbar.update(1)
                continue
    
    print(f"\n{'='*50}")
    print(f"Embedding creation completed!")
    print(f"Processed: {processed}")
    print(f"Failed: {failed}")
    print(f"Total: {total_docs}")
    print(f"{'='*50}")


def verify_embeddings(
    db_name: Optional[str] = None,
    collection_name: Optional[str] = None
):
    """
    Verify embeddings in collection.
    
    Args:
        db_name: MongoDB database name (default from env)
        collection_name: MongoDB collection name (default from env)
    """
    collection = get_mongodb_collection(db_name, collection_name)
    
    total = collection.count_documents({})
    with_embedding = collection.count_documents({"embedding": {"$exists": True}})
    without_embedding = collection.count_documents({"embedding": {"$exists": False}})
    
    print(f"\n{'='*50}")
    print(f"Embedding Status:")
    print(f"Total documents: {total}")
    print(f"With embedding: {with_embedding}")
    print(f"Without embedding: {without_embedding}")
    print(f"{'='*50}")
    
    # Sample a document with embedding to check dimension
    sample = collection.find_one({"embedding": {"$exists": True}})
    if sample and "embedding" in sample:
        dim = len(sample["embedding"])
        print(f"\nEmbedding dimension: {dim}")
        print(f"Expected dimension: 768 (keepitreal/vietnamese-sbert)")
        if dim != 768:
            print(f"⚠️  Warning: Dimension mismatch! Expected 768, got {dim}")
        print(f"Sample document: {sample.get('tieu_de', 'N/A')[:50]}...")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Create embeddings for MongoDB documents")
    parser.add_argument(
        "--db-name",
        type=str,
        default=None,
        help="MongoDB database name (default: from env MONGODB_DB_NAME)"
    )
    parser.add_argument(
        "--collection-name",
        type=str,
        default=None,
        help="MongoDB collection name (default: from env MONGODB_COLLECTION_NAME)"
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=100,
        help="Batch size for processing (default: 100)"
    )
    parser.add_argument(
        "--no-combine-fields",
        action="store_true",
        help="Only use noi_dung field, don't combine with other fields"
    )
    parser.add_argument(
        "--update-existing",
        action="store_true",
        help="Update documents that already have embeddings"
    )
    parser.add_argument(
        "--verify-only",
        action="store_true",
        help="Only verify embeddings, don't create them"
    )
    
    args = parser.parse_args()
    
    if args.verify_only:
        verify_embeddings(args.db_name, args.collection_name)
    else:
        create_embeddings_for_collection(
            db_name=args.db_name,
            collection_name=args.collection_name,
            batch_size=args.batch_size,
            combine_fields=not args.no_combine_fields,
            update_existing=args.update_existing
        )
        
        # Verify after creation
        print("\n")
        verify_embeddings(args.db_name, args.collection_name)

