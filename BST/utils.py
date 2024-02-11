from Node import Node
from flask import Flask, request
from Tree import Tree
import logging
from Mongo import *
"""
    Returns whether the input is a float

    Args: a string which may represent a float number
"""
def is_float(string):
    if string[0] == "-":
        string = string[1:]
    if string.replace(".", "").isnumeric():
        return True
    else:
        return False