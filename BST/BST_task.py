
from Node import Node
from flask import Flask, request
from pymongo import MongoClient
from Tree import Tree


# Initializing server and BST variables
app = Flask(__name__)
client = MongoClient("localhost", 27017)
db = client["bst_db"]
table = db["bst_table12"]
bst = Tree()

# Function empties MongoDB and the in-program tree
@app.route('/delete_all_treasures', methods=['DELETE'])
def delete_all_treasures():
    table.delete_many({})
    bst.root = None
    return "Success", 200

@app.route('/insert_treasure', methods=['POST'])
def insert_treasure():
    val_json = request.get_json()
    val = val_json["value"]
    if bst.insert(Node(val), table):
        return "Success", 200
    else:
        return "Error", 400

@app.route('/get_treasures')
def get_treasures():
    val = bst.bst_pass("in-order")
    if val is None:
        return "Error", 400
    else:
        return {"treasures" : val}, 200

@app.route('/delete_treasure', methods=['DELETE'])
def delete_treasure():
    val_json = request.get_json()
    val = val_json["value"]
    if bst.delete(val, table):
        return "Success", 200
    else:
        return "Error", 400

@app.route('/search_treasure', methods=['GET'])
def search_treasure():
    val = request.args.get("value")
    if bst.search(val):
        return {"message" : "Treasure found!"}, 200
    else:
        return {"message" : "Treasure not found"}, 400

@app.route('/pre_order_traversal', methods=['GET'])
def pre_order_traversal():
    val = bst.bst_pass("pre-order")
    if val is None:
        return "Error", 400
    else:
        return {"traversal_result": val}, 200

@app.route('/in_order_traversal', methods=['GET'])
def in_order_traversal():
    val = bst.bst_pass("in-order")
    if val is None:
        return "Error", 400
    else:
        return {"traversal_result": val}, 200

@app.route('/post_order_traversal', methods=['GET'])
def post_order_traversal():
    val = bst.bst_pass("post-order")
    if val is None:
        return "Error", 400
    else:
        return {"traversal_result": val}, 200

@app.route('/validate_bst')
def validate_bst():
    if bst.validate_and_visualize(table):
        return {"message" : "BST is valid"}, 200
    else:
        return {"message" : "BST is not valid"}, 400

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