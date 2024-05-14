#!/usr/bin/env python3
"""
hey
"""
from pymongo import MongoClient


def main():
    """
    Python script that
    provides some stats about Nginx
    logs stored in MongoDB:
    """
    client = MongoClient('localhost', 27017)
    db = client['logs']
    collection = db['nginx']

    total_logs = collection.count_documents({})
    print(f"{total_logs} logs")

    methods_counts = {
        "GET": 0,
        "POST": 0,
        "PUT": 0,
        "PATCH": 0,
        "DELETE": 0
    }
    for doc in collection.find({}, {"method": 1}):
        methods_counts[doc["method"]] += 1

    print("Methods:")
    for method, count in methods_counts.items():
        print(f"\tmethod {method}: {count}")

    get_status_count = collection.count_documents({"method": "GET", "path": "/status"})
    print(f"{get_status_count} status check")

if __name__ == "__main__":
    main()
