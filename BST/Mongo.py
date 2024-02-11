from pymongo import MongoClient
from http import HTTPStatus
from Node import *
from dotenv import load_dotenv
import os


class MongoTable():
    """
       Returns a pointer to an object which contains the MongoDB table which we are connected to
    """
    def __init__(self):
        load_dotenv()
        client = MongoClient(os.getenv("MONGO_CONNECTION_IP"), int(os.getenv("MONGO_CONNECTION_PORT")))
        db = client[os.getenv("MONGO_DB_NAME")]
        self.table = db[os.getenv("MONGO_TABLE_NAME")]

    """
        Deletes all of the treasures which were previously saved to MongoDB, and resets the bst variable

        Args: the bst variable, the logger for logging info/errors

        Return Value: Returns whether the function has succeeded with the response status
    """
    def delete_all_treasures(self, bst, logger):
        amount = self.table.count_documents({})
        res = self.table.delete_many({})
        if amount == res.deleted_count:
            bst.root = None
            logger.info("Deleted table content")
            return "Success", HTTPStatus.OK
        logger.error("Table content deletion failed")
        return "Error - Delete query has failed", HTTPStatus.BAD_REQUEST

    """
        Executes update of a specific node's child in MongoDB

        Args: the node we are updating, the direction of its child, the new child
    """
    def update_node_query(self, updated_node, dir, new_treasure):
        dir = str(dir.value)
        query = {"treasure": str(updated_node.treasure)}
        update = {"$set": {dir: new_treasure}}
        self.table.update_one(query, update)

    """
        Replaces the child of a node (both in code and in MongoDB)

        Args: the node which we will replace, the node which we will replace to, the node which its child is being replaced,
        the side of the node's child (if we want to swap from None)

        Return Value: Returns whether the update has succeeded
    """
    def update_node(self, old_node, new_node, parent, side = TreeConstants.FAIL):
        try:
            new_val = ""
            if new_node:
                new_val = str(new_node.treasure)
            if (parent.left and parent.left.treasure == old_node.treasure) or side == TreeConstants.LEFT:
                parent.left = new_node
                self.update_node_query(parent, TreeConstants.LEFT, new_val)
            else:
                parent.right = new_node
                self.update_node_query(parent, TreeConstants.LEFT, new_val)
            return True
        except Exception as e:
            return False

    """
        Updates the tree's root in MongoDB

        Args: the new root's treasure

        Return Value: Returns whether the update has succeeded
    """
    def update_root_db(self, root):
        try:
            new_val = ""
            if root:
                new_val = str(root.treasure)
            query = {"class": "tree"}
            update = {"$set": {"root": new_val}}
            self.table.update_one(query, update)
            return True
        except Exception as e:
            return False

    """
        Inserting a new node to MongoDB

        Args: the node which we want to insert, the parent of the new node, the direction the parent's new child

        Return Value: Return whether the insert succeeded or not
    """
    def insert_node_db(self, new_node, father_node, direction):
        try:
            if direction == TreeConstants.LEFT:
                old_node = father_node.left
            elif direction == TreeConstants.RIGHT:
                old_node = father_node.right
            if self.table.count_documents({"class": "tree"}) == 0:
                self.table.insert_one({
                    "class": "tree",
                    "root": "",
                })
            tree = self.table.find({"class": "tree"})[0]
            if tree["root"]:
                self.update_node(old_node, new_node, father_node)
            else:
                self.update_root_db(new_node)
            self.table.insert_one({
                "class": "node",
                "treasure": str(new_node.treasure),
                str(TreeConstants.LEFT.value): "",
                str(TreeConstants.RIGHT.value): "",
            })
            return True
        except Exception as e:
            return False

    """
        Deleting a  node from MongoDB

        Args: the node which we want to delete

        Return Value: Return whether the delete succeeded or not
    """
    def delete_node_db(self, node):
        try:
            self.table.delete_one({"treasure": str(node.treasure)})
            return True
        except Exception as e:
            return False

    """
        Saves the BST's visualization to MongoDB

        Args: the visualization matrix of the BST
    """
    def insert_vis(self, vis):
        if self.table.count_documents({"class": "vis"}) == 0:
            self.table.insert_one({
                "class": "vis",
                "content": vis
            })
        query = {"class": "vis"}
        update = {"$set": {"content": vis}}
        self.table.update_one(query, update)

    """
            Prints the BST's visualization which is saved in MongoDB
        """
    def print_vis(self):
        try:
            db_res = self.table.find({"class": "vis"})[0]
            vis = db_res["content"]
            print("BST visualization from MongoDB: ")
            for row in vis:
                print(row)
        except Exception as e:
            print("BST visualization does not exist")
            return
