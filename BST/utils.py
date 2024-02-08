from Node import Node
from flask import Flask, request
from Tree import Tree
import logging
from Mongo import *
# Initializing server and BST variables
app = Flask(__name__)
bst = Tree()
table = start_connection()
# Create and configure logger
logging.basicConfig(filename="log.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

# Creating an object
logger = logging.getLogger()
logger.setLevel(0)
def is_float(string):
    if string[0] == "-":
        string = string[1:]
    if string.replace(".", "").isnumeric():
        return True
    else:
        return False