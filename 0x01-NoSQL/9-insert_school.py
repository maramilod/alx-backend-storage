#!/usr/bin/env python3
"""
hey
"""



def insert_school(mongo_collection, **kwargs):
    """
    a Python function that inserts a new document
    in a collection based on kwargs:
    """
    return mongo_collection.insert(kwargs).inserted_id
