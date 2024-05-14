#!/usr/bin/env python3
"""
hey
"""


def update_topics(mongo_collection, name, topics):
    """
    a Python function that changes all topics of
    a school document based on the name:
    """
    return mongo_collection.updateMany({'name': name}, {'$set': {'topics': topics}})
