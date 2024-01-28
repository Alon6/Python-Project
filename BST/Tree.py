
import math
import Node
from math import inf
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
        self.insert_db(node, res[1], table, res[0])
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
                self.update_root_db(None, table)
            else:
                self.swap(node, None, parent, table)
        # If the node has one child then swap the node with its child
        elif node.left is None or node.right is None:
            child = None
            if node.left is not None:
                child = node.left
            else:
                child = node.right
            if parent is None:
                self.root = child
                self.update_root_db(child, table)
            else:
                self.swap(node, child, parent, table)
        # If the node has two children then swap the node with its successor (and if the successor has a child then
        # replace the successor with its child
        else:
            suc_res = node.right.find_successor()
            suc = suc_res[0]
            suc.left = node.left
            self.update_node_db(suc, node.left, "left", table)
            if suc.right is None and len(suc_res) > 1:
                suc.right = node.right
                self.update_node_db(suc, node.right, "right", table)
            else:
                if len(suc_res) > 1:
                    suc_parent = suc_res[1]
                    self.swap(suc, suc.right, suc_parent, table)
                    suc.right = node.right
                    self.update_node_db(suc, node.right, "right", table)
            if parent is None:
                self.root = suc
                self.update_root_db(suc, table)
            else:
                self.swap(node, suc, parent, table)
        self.delete_db(node, table)
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
        self.insert_vis(vis, table)
        return True

    # Inserting a node from MongoDB
    def rebuild_node(self, value, table):
        new_node = Node(float(value))
        db_node = table.find({"treasure": value})
        for node in db_node:
            if node["left"] != "":
                new_node.left = self.rebuild_node(str(node["left"]), table)
            if node["right"] != "":
                new_node.right = self.rebuild_node(str(node["right"]), table)
        return new_node

    # Inserting the whole tree from MongoDB
    def rebuild(self, table):
        new_tree = Tree()
        db_tree = table.find({"class": "tree"})
        if table.count_documents({"class": "tree"}) == 0:
            return new_tree
        for tree in db_tree:
            if tree["root"] == "":
                return new_tree
            new_tree.root = self.rebuild_node(tree["root"], table)
        return new_tree

    # Swap the child of a certain node in MongoDB - used for delete function changes (when the old child node is known)
    def swap(self, old_node, new_node, parent, table):
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
    def update_root_db(self, root, table):
        new_val = ""
        if root is not None:
            new_val = str(root.treasure)
        query = {"class": "tree"}
        update = {"$set": {"root": new_val}}
        table.update_one(query, update)

    # Update a certain child of a node in MongoDB (when the direction is known)
    def update_node_db(self, node, child, dir, table):
        query = {"treasure": str(node.treasure)}
        update = {"$set": {dir: str(child.treasure)}}
        table.update_one(query, update)

    # Inserting a node in MongoDB
    def insert_db(self, new_node, father_node, table, direction):
        db_tree = table.find({"class": "tree"})
        if table.count_documents({"class": "tree"}) == 0:
            table.insert_one({
                "class": "tree",
                "root": "",
            })
            db_tree = table.find({"class": "tree"})
        for tree in db_tree:
            if tree["root"] != "":
                self.update_node_db(father_node, new_node, direction, table)
            else:
                self.update_root_db(new_node, table)
            table.insert_one({
                "class": "node",
                "treasure": str(new_node.treasure),
                "left": "",
                "right": "",
            })
        print("Treasure " + str(new_node.treasure) + " was inserted successfully")

    # Deleting a node in MongoDB
    def delete_db(self, node, table):
        table.delete_one({"treasure": str(node.treasure)})
        print("Treasure " + str(node.treasure) + " was deleted successfully")

    # Saving a visualization format in MongoDB
    def insert_vis(self, vis, table):
        if table.count_documents({"class": "vis"}) == 0:
            table.insert_one({
                "class": "vis",
                "content": vis
            })
        query = {"class": "vis"}
        update = {"$set": {"content": vis}}
        table.update_one(query, update)

    # Getting the visualization format from MongoDB
    def get_vis(self, table):
        db_res = table.find({"class": "vis"})
        for res in db_res:
            vis = res["content"]
            print("BST visualization from MongoDB: ")
            for row in vis:
                print(row)