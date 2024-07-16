#!/usr/bin/env python3
"""
script that provides some stats about Nginx logs stored in MongoDB
"""
from pymongo import MongoClient

if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_logs = client.logs.nginx
    
    # Get number of documents in collection
    docs_num = nginx_logs.count_documents({})
    
    # Count documents by method
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    methods_counts = {method: nginx_logs.count_documents({'method': method}) for method in methods}
    
    # Count documents with method GET and path /status
    get_status = nginx_logs.count_documents({'method': 'GET', 'path': '/status'})
    
    # Print stats
    print("{} logs".format(docs_num))
    print("Methods:")
    for method in methods:
        print("\tmethod {}: {}".format(method, methods_counts[method]))
    print("{} status check".format(get_status))
