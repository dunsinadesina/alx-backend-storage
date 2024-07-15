#!/usr/bin/env python3
"""
This module have a utility function that list all document
"""
import pymongo


def list_all(mongo_collection):
    """
    list all collections
    """
    if mongo_collection is None:
        return []
    return list(mongo_collection.find())
