from pymongo import MongoClient
from http import HTTPStatus
from Node import *
def start_connection():
    client = MongoClient("localhost", 27017)
    db = client["bst_db"]
    return db["bst_table12"]
def delete_all_treasures(table, bst, logger):
    amount = table.count_documents({})
    res = table.delete_many({})
    if amount == res.deleted_count:
        bst.root = None
        logger.info("Deleted table content")
        return "Success", HTTPStatus.OK
    logger.error("Table content deletion failed")
    return "Error - Delete query has failed", HTTPStatus.BAD_REQUEST
# Swap the child of a certain node in MongoDB - used for delete function changes (when the old child node is known)
def swap(old_node, new_node, parent, table):
        try:
            new_val = ""
            if new_node:
                new_val = str(new_node.treasure)
            if parent.left and parent.left.treasure == old_node.treasure:
                parent.left = new_node
                query = {"treasure": str(parent.treasure)}
                update = {"$set": {LEFT: new_val}}
                table.update_one(query, update)
            else:
                parent.right = new_node
                query = {"treasure": str(parent.treasure)}
                update = {"$set": {RIGHT: new_val}}
                table.update_one(query, update)
            return True
        except Exception as e:
            return False
# Change the root in MongoDB - used for insert/delete changes
def update_root_db(root, table):
        try:
            new_val = ""
            if root:
                new_val = str(root.treasure)
            query = {"class": "tree"}
            update = {"$set": {"root": new_val}}
            table.update_one(query, update)
            return True
        except Exception as e:
            return False
# Update a certain child of a node in MongoDB (when the direction is known)
def update_node_db(node, child, dir, table):
        try:
            query = {"treasure": str(node.treasure)}
            update = {"$set": {dir: str(child.treasure)}}
            table.update_one(query, update)
            return True
        except Exception as e:
            return False
# Inserting a node in MongoDB
def insert_db(new_node, father_node, table, direction):
        try:
            if table.count_documents({"class": "tree"}) == 0:
                table.insert_one({
                    "class": "tree",
                    "root": "",
                })
            db_tree = table.find({"class": "tree"})
            for tree in db_tree:
                if tree["root"]:
                    update_node_db(father_node, new_node, direction, table)
                else:
                    update_root_db(new_node, table)
                table.insert_one({
                    "class": "node",
                    "treasure": str(new_node.treasure),
                    LEFT: "",
                    RIGHT: "",
                })
            return True
        except Exception as e:
            return False
# Deleting a node in MongoDB
def delete_db(node, table):
        try:
            table.delete_one({"treasure": str(node.treasure)})
            return True
        except Exception as e:
            return False
# Saving a visualization format in MongoDB
def insert_vis(vis, table):
        if table.count_documents({"class": "vis"}) == 0:
            table.insert_one({
                "class": "vis",
                "content": vis
            })
        query = {"class": "vis"}
        update = {"$set": {"content": vis}}
        table.update_one(query, update)
# Getting the visualization format from MongoDB
def get_vis(table):
        if table.count_documents({"class": "vis"}) == 0:
            print("BST visualization does not exist")
            return
        db_res = table.find({"class": "vis"})
        for res in db_res:
            vis = res["content"]
            print("BST visualization from MongoDB: ")
            for row in vis:
                print(row)
