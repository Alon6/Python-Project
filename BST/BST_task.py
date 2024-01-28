import math
from math import inf

import flask
from flask import Flask, request
import json
from pymongo import MongoClient


class Node:
    # Initializing empty node
    def __init__(self, value):
        self.left = None
        self.right = None
        self.treasure = value
    # Function returns the path to a node if exist else return the path to the place in which the node will be added
    def actual_search(self, treasure):
        # Returning if node is found
        if float(treasure) == self.treasure:
            return ["", self]
        # Progressing down the tree or returning if the end has been reached
        if float(treasure) < self.treasure:
            if self.left is None:
                return ["left", self]
            res = self.left.actual_search(treasure)
            res.append(self)
            return res
        if self.right is None:
            return ["right", self]
        res = self.right.actual_search(treasure)
        res.append(self)
        return res
    # Returning the path to the successor in the right subtree of a node
    def find_successor(self):
        # Going left until finding a node without a left child
        if self.left is None:
            return [self]
        res = self.left.find_successor()
        res.append(self)
        return res
    # Passing throughout the tree and printing the nodes based on the input order
    def bst_pass(self, order, node_list):
        if order == "pre-order":
            node_list.append(self.treasure)
            print("current treasure: " + str(self.treasure))
        if self.left is not None:
            node_list = self.left.bst_pass(order, node_list)
        if order == "in-order":
            node_list.append(self.treasure)
            print("current treasure: " + str(self.treasure))
        if self.right is not None:
            node_list = self.right.bst_pass(order, node_list)
        if order == "post-order":
            node_list.append(self.treasure)
            print("current treasure: " + str(self.treasure))
        return node_list

    # Passing throughout the tree, checking if the nodes are ordered correctly and returning the tree's depth
    def validate(self, depth):
        if (self.left is not None and self.left.treasure > self.treasure)\
                or (self.right is not None and self.right.treasure < self.treasure):
            return inf
        if self.left is None and self.right is None:
            return depth
        if self.left is None:
            return self.right.validate(depth + 1)
        if self.right is None:
            return self.left.validate(depth + 1)
        return max(self.right.validate(depth + 1), self.left.validate(depth + 1))
    # Passing through the tree and creating its visualization
    def visualize(self, vis, depth, index):
        if self.left is not None:
            res = self.left.visualize(vis, depth + 1, index)
            vis = res[0]
            index = res[1]
        else:
            # Advancing the index based on the size of the node's empty subtree
            index += int(math.pow(2,len(vis) - depth - 1) - 1) * 2
        val = "0"
        if self.treasure < 10:
            val += str(self.treasure)
        else:
            val = str(self.treasure)
        # Adding the current node to the visualization based on its depth and index in an in-order pass
        vis[depth] = vis[depth][:index] + val + vis[depth][index+2:]
        index += 2
        if self.right is not None:
            return self.right.visualize(vis, depth + 1, index)
        # Advancing the index based on the size of the node's empty subtree
        return (vis, index + int(math.pow(2,len(vis) - depth - 1) - 1) * 2)



class Tree:
    # Initializing an empty tree
    def __init__(self):
        self.root = None
    # Check if the tree is empty, else search the node in the tree
    def actual_search(self, treasure):
        if self.root is None:
            return ["", None]
        return self.root.actual_search(treasure)
    # Search the node, extract it from the path and print a relevant message
    def search(self, treasure):
        res = self.actual_search(treasure)
        if res[0] != "" or res[1] is None:
            print("treasure " + str(treasure) + " is not in the bst")
            return False
        print("treasure " + str(treasure) + " is in the bst")
        return True
    # Search the place in which the node should be inserted and update the tree accordingly
    def insert(self, node, table):
        res = self.actual_search(node.treasure)
        # Check for the case in which the new node is the only node in the tree
        if res[1] is None:
            self.root = node
        # Check for normal cases
        elif res[0] == "left":
            res[1].left = node
        elif res[0] == "right":
            res[1].right = node
        else:
            print("Insertion failed, treasure " + str(node.treasure) + " already exists")
            return False
        insert_db(node, res[1], table, res[0])
        return True
    # Find the node in the tree and delete it
    def delete(self, treasure, table):
        res = self.actual_search(treasure)
        node = res[1]
        parent = None
        if len(res) > 2:
            parent = res[2]
        if res[0] != "" or node is None:
            print("Deletion failed, treasure " + str(treasure) + " does not exist")
            return False
        # If the node has no children then simply delete it
        if node.left is None and node.right is None:
            if parent is None:
                self.root = None
                update_root_db(None, table)
            else:
                swap(node, None, parent)
        # If the node has one child then swap the node with its child
        elif node.left is None or node.right is None:
            child = None
            if node.left is not None:
                child = node.left
            else:
                child = node.right
            if parent is None:
                self.root = child
                update_root_db(child, table)
            else:
                swap(node, child, parent)
        # If the node has two children then swap the node with its successor (and if the successor has a child then
        # replace the successor with its child
        else:
            suc_res = node.right.find_successor()
            suc = suc_res[0]
            suc.left = node.left
            update_node_db(suc, node.left, "left", table)
            if suc.right is None and len(suc_res) > 1:
                suc.right = node.right
                update_node_db(suc, node.right, "right", table)
            else:
                if len(suc_res) > 1:
                    suc_parent = suc_res[1]
                    swap(suc, suc.right, suc_parent)
                    suc.right = node.right
                    update_node_db(suc, node.right, "right", table)
            if parent is None:
                self.root = suc
                update_root_db(suc, table)
            else:
                swap(node, suc, parent)
        delete_db(node, table)
        return True
    # Initiate the pass
    def bst_pass(self, order):
        if self.root is None:
            return []
        if order == "pre-order" or order == "in-order" or order == "post-order":
            print("Beginning " + order + " pass")
            return self.root.bst_pass(order, [])
        else:
            print("Error: order type does not exist")
            return None
    # Check if the tree is a valid BST and if it is then generate its visualization
    def validate_and_visualize(self, table):
        if self.root is None:
            print("The tree is empty")
            return True
        # Check validation
        depth = self.root.validate(1)
        if depth == inf:
            print("The BST is invalid")
            return False
        # Create empty string list based on tree's depth
        vis = []
        for i in range(0, depth):
            str = ""
            for j in range(0, int(math.pow(2,depth))):
                str += "  "
            vis.append(str)
        # Generate visualization
        res = self.root.visualize(vis, 0, 0)
        vis = res[0]
        print("BST visualization: ")
        for row in vis:
            print(row)
        insert_vis(vis, table)
        return True

# Inserting a node from MongoDB
def rebuild_node(value, table):
    new_node = Node(float(value))
    db_node = table.find({"treasure": value})
    for node in db_node:
        if node["left"] != "":
            new_node.left = rebuild_node(str(node["left"]), table)
        if node["right"] != "":
            new_node.right = rebuild_node(str(node["right"]), table)
    return new_node

# Inserting the whole tree from MongoDB
def rebuild(table):
    new_tree = Tree()
    db_tree = table.find({"class": "tree"})
    if table.count_documents({"class": "tree"}) == 0:
        return new_tree
    for tree in db_tree:
        if tree["root"] == "":
            return new_tree
        new_tree.root = rebuild_node(tree["root"], table)
    return new_tree

# Swap the child of a certain node in MongoDB - used for delete function changes (when the old child node is known)
def swap(old_node, new_node, parent):
    new_val = ""
    if new_node is not None:
        new_val = str(new_node.treasure)
    if parent.left is not None and parent.left.treasure == old_node.treasure:
        parent.left = new_node
        query = {"treasure": str(parent.treasure)}
        update = {"$set": {"left": new_val}}
        table.update_one(query, update)
    else:
        parent.right = new_node
        query = {"treasure": str(parent.treasure)}
        update = {"$set": {"right": new_val}}
        table.update_one(query, update)

# Change the root in MongoDB - used for insert/delete changes
def update_root_db(root, table):
    new_val = ""
    if root is not None:
        new_val = str(root.treasure)
    query = {"class": "tree"}
    update = {"$set": {"root": new_val}}
    table.update_one(query, update)

# Update a certain child of a node in MongoDB (when the direction is known)
def update_node_db(node, child, dir, table):
    query = {"treasure": str(node.treasure)}
    update = {"$set": {dir: str(child.treasure)}}
    table.update_one(query, update)

# Inserting a node in MongoDB
def insert_db(new_node, father_node, table, direction):
    db_tree = table.find({"class": "tree"})
    if table.count_documents({"class": "tree"}) == 0:
        table.insert_one({
            "class": "tree",
            "root": "",
        })
        db_tree = table.find({"class": "tree"})
    for tree in db_tree:
        if tree["root"] != "":
            update_node_db(father_node, new_node, direction, table)
        else:
            update_root_db(new_node, table)
        table.insert_one({
            "class": "node",
            "treasure": str(new_node.treasure),
            "left": "",
            "right": "",
        })
    print("Treasure " + str(new_node.treasure) + " was inserted successfully")

# Deleting a node in MongoDB
def delete_db(node, table):
    table.delete_one({"treasure": str(node.treasure)})
    print("Treasure " + str(node.treasure) + " was deleted successfully")
# Saving a visualization format in MongoDB
def insert_vis(vis, table):
    if table.count_documents({"class": "vis"}) == 0:
        table.insert_one({
            "class" : "vis",
            "content" : vis
        })
    query = {"class" : "vis"}
    update = {"$set": {"content": vis}}
    table.update_one(query, update)
# Getting the visualization format from MongoDB
def get_vis(table):
    db_res = table.find({"class": "vis"})
    for res in db_res:
        vis = res["content"]
        print("BST visualization from MongoDB: ")
        for row in vis:
            print(row)
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