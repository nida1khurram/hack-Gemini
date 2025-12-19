#!/usr/bin/env python3
"""
Script to check the local Qdrant storage directly
"""

import os
from qdrant_client import QdrantClient

def check_local_storage():
    print("Checking local Qdrant storage...")

    try:
        # Connect to the local persistent storage
        client = QdrantClient(path="./qdrant_local")

        # Get collections
        collections = client.get_collections()
        print(f"Available collections: {[col.name for col in collections.collections]}")

        # Check our specific collection
        try:
            collection_info = client.get_collection("ai_textbook_chapters")
            print(f"Collection 'ai_textbook_chapters' info:")
            print(f"  Points count: {collection_info.points_count}")
            print(f"  Vector size: {collection_info.config.params.vectors.size}")

            # Get some points to see the content
            if collection_info.points_count > 0:
                points = client.scroll(
                    collection_name="ai_textbook_chapters",
                    limit=2
                )
                print(f"\nSample points from collection:")
                for i, (point, _) in enumerate(points[0]):
                    print(f"  Point {i+1}:")
                    print(f"    ID: {point.id}")
                    print(f"    Title: {point.payload.get('title', 'N/A')}")
                    print(f"    Content preview: {point.payload.get('content', '')[:100]}...")
                    print(f"    Vector dimension: {len(point.vector) if point.vector else 'N/A'}")

        except Exception as e:
            print(f"Collection 'ai_textbook_chapters' not found: {e}")

    except Exception as e:
        print(f"Error accessing local Qdrant storage: {e}")
        if "already accessed" in str(e):
            print("Note: This error occurs when another process is using the local storage.")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_local_storage()