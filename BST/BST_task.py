from http import HTTPStatus
from Node import Node
from flask import Flask, request
from pymongo import MongoClient
from Tree import Tree
import logging

# Initializing server and BST variables
app = Flask(__name__)
client = MongoClient("localhost", 27017)
db = client["bst_db"]
table = db["bst_table12"]
bst = Tree()

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

# Function empties MongoDB and the in-program tree
@app.route('/delete_all_treasures', methods=['DELETE'])
def delete_all_treasures():
    amount = table.count_documents({})
    res = table.delete_many({})
    if amount == res.deleted_count:
        bst.root = None
        logger.info("Deleted table content")
        return "Success", HTTPStatus.OK
    logger.error("Table content deletion failed")
    return "Error - Delete query has failed", HTTPStatus.BAD_REQUEST


@app.route('/insert_treasure', methods=['POST'])
def insert_treasure():
    val_json = request.get_json()
    if "value" not in val_json or not is_float(str(val_json["value"])):
        logger.error("Error, input does not contain treasure")
        return "Error, input does not contain treasure", HTTPStatus.BAD_REQUEST
    val = val_json["value"]
    res = bst.insert(Node(val), table)
    if res[0]:
        logger.info("Treasure " + str(val) + " was inserted successfully")
        return "Success", HTTPStatus.OK
    else:
        logger.error(res[1])
        return "Error - " + res[1], HTTPStatus.BAD_REQUEST


@app.route('/get_treasures')
def get_treasures():
    val = bst.bst_pass("in-order")
    logger.info("The pass was a success")
    return {"treasures": val}, HTTPStatus.OK


@app.route('/delete_treasure', methods=['DELETE'])
def delete_treasure():
    val_json = request.get_json()
    if "value" not in val_json or not is_float(str(val_json["value"])):
        logger.error("Error, input does not contain treasure")
        return "Error, input does not contain treasure", HTTPStatus.BAD_REQUEST
    val = val_json["value"]
    res = bst.delete(val, table)
    if res[0]:
        logger.info("Treasure " + str(val) + " was deleted successfully")
        return "Success", HTTPStatus.OK
    else:
        logger.error(res[1])
        return "Error - " + res[1], HTTPStatus.BAD_REQUEST


@app.route('/search_treasure', methods=['GET'])
def search_treasure():
    val = request.args.get("value")
    if not val or not is_float(str(val)):
        logger.error("Error, input does not contain treasure")
        return "Error, input does not contain treasure", HTTPStatus.BAD_REQUEST
    if bst.search(val):
        logger.info("treasure " + str(val) + " is in the bst")
        return {"message" : "Treasure found!"}, HTTPStatus.OK
    else:
        logger.error("treasure " + str(val) + " is not in the bst")
        return {"message" : "Treasure not found"}, HTTPStatus.BAD_REQUEST


@app.route('/pre_order_traversal', methods=['GET'])
def pre_order_traversal():
    val = bst.bst_pass("pre-order")
    logger.info("The pass was a success")
    return {"traversal_result": val}, HTTPStatus.OK


@app.route('/in_order_traversal', methods=['GET'])
def in_order_traversal():
    val = bst.bst_pass("in-order")
    logger.info("The pass was a success")
    return {"traversal_result": val}, HTTPStatus.OK


@app.route('/post_order_traversal', methods=['GET'])
def post_order_traversal():
    val = bst.bst_pass("post-order")
    logger.info("The pass was a success")
    return {"traversal_result": val}, HTTPStatus.OK


@app.route('/validate_bst')
def validate_bst():
    if bst.validate_and_visualize(table):
        logger.info("The BST is valid")
        return {"message" : "BST is valid"}, HTTPStatus.OK
    else:
        logger.error("The BST is not valid")
        return {"message" : "BST is not valid"}, HTTPStatus.BAD_REQUEST

if __name__ == "__main__":
    app.run()


"""
bst = rebuild(table)
    get_vis(table)
    bst.insert(Node(3), table)
    bst.insert(Node(6), table)
    bst.insert(Node(2), table)
    bst.insert(Node(5), table)
    bst.insert(Node(10), table)
    bst.insert(Node(1), table)
    bst.search(5)
    bst.search(1)
    bst.search(9)
    treasure = bst.root.treasure
    bst.root.treasure = 200
    bst.validate_and_visualize(table)
    bst.root.treasure = treasure
    bst.validate_and_visualize(table)
    get_vis(table)
    bst.bst_pass("pre-order")
    bst.bst_pass("in-order")
    bst.bst_pass("post-order")
    bst.bst_pass("order")
    bst.delete(5, table)
    bst.delete(2, table)
    bst.delete(3, table)
    bst.delete(3, table)
    bst.validate_and_visualize(table)
    bst.search(2)
    bst.search(7)
    bst.search(6)
    bst.bst_pass("pre-order")
    bst.bst_pass("in-order")
    bst.bst_pass("post-order")
    bst.bst_pass("order")
"""