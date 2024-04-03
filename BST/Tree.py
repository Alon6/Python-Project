from Mongo import *
import math
import Node
from math import inf
from Node import TreeConstants
class Tree:
    """
        Returns a pointer to a new empty BST
    """
    def __init__(self):
        self.root = None

    """
       Returns a list with contents based on whether the node exists or not

       Args: a float which describes the treasure we want to find

       Return Value: if the node is in the tree then return [<'Exists'>,<the node>,<the node's parent>(if the node is not a root)]
       if the node is not in the tree then return [<'Left/Right'>,<the node which would be the parent if the node we searched for existed>
       ,the node which would be the grand parent if the node we searched for existed>(isn't used)]
       if the tree is empty then return [<'FAIL'>, None]
    """
    def search(self, treasure):
        if not self.root:
            return [TreeConstants.FAIL, None]
        return self.root.search(treasure)

    """
       Returns Whether the requested node is in the tree or not

       Args: a float which describes the treasure we want to find
    """
    def search_query(self, treasure):
        (status, node, *_) = self.search(treasure)
        if str(status.value) or not node:
            return False
        return True

    """
        Inserting a new node to the BST and MongoDB
        
        Args: the node which we want to insert, the object which represents our connection with our MongoDB table

        Return Value: Return whether the insert succeeded or not with a relevant error message
    """
    def insert(self, node, table):
        (dir, parent, *_) = self.search(node.treasure)
        # Check for the case in which the new node is the only node in the tree
        if not parent:
            self.root = node
        # Check for normal cases
        elif dir == TreeConstants.LEFT:
            parent.left = node
        elif dir == TreeConstants.RIGHT:
            parent.right = node
        else:
            return False, "Insertion failed, treasure " + str(node.treasure) + " already exists"
        if table.insert_node_db(node, parent, dir):
            return True, ""
        return False, "Insertion of treasure " + str(node.treasure) + " failed, internal error with MongoDB"

    """
        Deleting a node from the BST and MongoDB

        Args: the node which we want to delete, the object which represents our connection with our MongoDB table

        Return Value: Return whether the delete succeeded or not with a relevant error message
    """
    def delete(self, treasure, table):
        (status, deleted_node, *parent) = self.search(treasure)
        no_error_flag = True
        if len(parent) == 1:
            parent = parent[0]
        else:
            parent = None
        if str(status.value) or not deleted_node:
            return False, "Deletion failed, treasure " + str(treasure) + " does not exist"
        if not deleted_node.left and not deleted_node.right:
            no_error_flag = self.delete_without_children(table, deleted_node, parent, no_error_flag)

        elif not deleted_node.left or not deleted_node.right:
            no_error_flag = self.delete_with_one_child(table, deleted_node, parent, no_error_flag)
        else:
            no_error_flag = self.delete_with_two_children(table, deleted_node, parent, no_error_flag)
        if no_error_flag:
            return True, ""
        return False, "Deletion of treasure " + str(deleted_node.treasure) + " failed, internal error with MongoDB"

    """
        Deleting a new node from the BST and MongoDB in the case it has no children

        Args: the object which represents our connection with our MongoDB table, the node which we want to delete,
        the parent of the node which we want to delete (None if the node is the root),
        the flag which save if all of the MongoDB operations have succeeded

        Return Value: Return whether the delete succeeded or not
    """
    def delete_without_children(self, table, deleted_node, parent, no_error_flag):
        if not parent:
            self.root = None
            return no_error_flag and table.update_root_db(None)
        else:
            return no_error_flag and table.update_node(deleted_node, None, parent)

    """
        Deleting a new node from the BST and MongoDB in the case it has one child

        Args: the object which represents our connection with our MongoDB table, the node which we want to delete,
        the parent of the node which we want to delete (None if the node is the root),
        the flag which save if all of the MongoDB operations have succeeded

        Return Value: Return whether the delete succeeded or not
    """
    def delete_with_one_child(self, table, deleted_node, parent, no_error_flag):
        if deleted_node.left:
            child = deleted_node.left
        else:
            child = deleted_node.right
        if not parent:
            self.root = child
            return no_error_flag and table.update_root_db(child)
        else:
            return no_error_flag and table.update_node(deleted_node, child, parent)

    """
        Deleting a new node from the BST and MongoDB in the case it has two children

        Args: the object which represents our connection with our MongoDB table, the node which we want to delete,
        the parent of the node which we want to delete (None if the node is the root),
        the flag which save if all of the MongoDB operations have succeeded

        Return Value: Return whether the delete succeeded or not
    """
    def delete_with_two_children(self, table, deleted_node, parent, no_error_flag):
        (suc, *suc_parent) = deleted_node.right.find_successor()
        if (len(suc_parent) > 0):
            suc_parent = suc_parent[0]
        else:
            suc_parent = None
        no_error_flag = no_error_flag and table.update_node(suc.left, deleted_node.left, suc, TreeConstants.LEFT)
        if not suc.right and suc_parent:
            no_error_flag = no_error_flag and table.update_node(suc.right, deleted_node.right, suc, TreeConstants.RIGHT)
        elif suc_parent:
                no_error_flag = no_error_flag and table.update_node(suc, suc.right, suc_parent)
                no_error_flag = no_error_flag and table.update_node(suc.right, deleted_node.right, suc)
        if not parent:
            self.root = suc
            no_error_flag = no_error_flag and table.update_root_db(suc)
        else:
            no_error_flag = no_error_flag and table.update_node(deleted_node, suc, parent)
        return no_error_flag and table.delete_node_db(deleted_node)

    """
        Returns a list which contains all of the tree's nodes which are ordered based on the input

        Args: the order which the pass is based on
    """
    def bst_pass(self, order):
        if not self.root:
            return []
        if order == TreeConstants.PRE_ORDER or order == TreeConstants.IN_ORDER or order == TreeConstants.POST_ORDER:
            return self.root.bst_pass(order, [])
        else:
            return None

    """
        Returns whether the BST is valid or not, and if it is then create, print and save the BST's visualization to MongoDB

        Args: the object which represents our connection with our MongoDB table
    """
    def validate_and_visualize(self, table):
        # Check validation
        depth = self.validate()
        if depth == inf:
            return False
        self.visualize(table, depth)
        return True

    """
        Returns whether the BST is valid or not
    """
    def validate(self):
        if not self.root:
            return True
        return self.root.validate(1)

    """
        Creates, prints and saves the BST's visualization to MongoDB

        Args: the object which represents our connection with our MongoDB table, and the tree's depth
    """
    def visualize(self, table, depth):
        # Create empty string list based on tree's depth
        vis_matrix = [''.join("   " for _ in range(0, int(math.pow(2, depth)))) for _ in range(0, depth)]
        # Generate visualization
        res = self.root.visualize_pass(vis_matrix, 0, 0)
        vis_matrix = res[0]
        print("BST visualization: ")
        for row in vis_matrix:
            print(row)
        table.insert_vis(vis_matrix)

    # Functions for testing
    """
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
    """