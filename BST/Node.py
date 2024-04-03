from enum import Enum
import math
from math import inf


class TreeConstants(Enum):
    LEFT = "left"
    RIGHT = "right"
    EXISTS = ""
    FAIL = ""
    PRE_ORDER = "pre-order"
    IN_ORDER = "in-order"
    POST_ORDER = "post-order"


class Node:
    """
    Returns a pointer to a new node

    Args: a float which represents the node's treasure
    """
    def __init__(self, value):
        self.left = None
        self.right = None
        self.treasure = value

    """
    Returns a list with contents based on whether the node exists or not
    
    Args: a float which describes the treasure we want to find
    
    Return Value: if the node is in the tree then return [<'Exists'>,<the node>,<the node's parent>(if the node is not a root)]
    if the node is not in the tree then return [<'Left/Right'>,<the node which would be the parent if the node we searched for existed>
    ,the node which would be the grand parent if the node we searched for existed>(isn't used)]
    """
    def search(self, treasure):
        # Returning if node is found
        if float(treasure) == self.treasure:
            return [TreeConstants.EXISTS, self]
        # Progressing down the tree or returning if the end has been reached
        if float(treasure) < self.treasure:
            if not self.left:
                return [TreeConstants.LEFT, self]
            node_placement = self.left.search(treasure)
            if len(node_placement) < 3:
                node_placement.append(self)
            return node_placement
        if not self.right:
            return [TreeConstants.RIGHT, self]
        node_placement = self.right.search(treasure)
        if len(node_placement) < 3:
            node_placement.append(self)
        return node_placement

    """
    Returns a list with contents based on the successor of the calling node
    
    Return Value: Return [<the node>,<the node's parent>(if the node is not the child of the calling node)]
    """
    def find_successor(self):
        # Going left until finding a node without a left child
        if not self.left:
            return [self]
        node_placement = self.left.find_successor()
        if len(node_placement) < 2:
            node_placement.append(self)
        return node_placement

    """
        Returns a list which contains all of the tree's nodes which are ordered based on the input

        Args: the order which the pass is based on, the list which contains the nodes
    """
    def bst_pass(self, order, node_list):
        if order == TreeConstants.PRE_ORDER:
            node_list.append(self.treasure)
        if self.left:
            node_list = self.left.bst_pass(order, node_list)
        if order == TreeConstants.IN_ORDER:
            node_list.append(self.treasure)
        if self.right:
            node_list = self.right.bst_pass(order, node_list)
        if order == TreeConstants.POST_ORDER:
            node_list.append(self.treasure)
        return node_list

    """
        Returns the depth of the subtree if it's valid or infinite if it's not

        Args: the depth of the current node
    """
    def validate(self, depth):
        if (self.left and self.left.treasure > self.treasure)\
                or (self.right and self.right.treasure < self.treasure):
            return inf
        if not self.left and not self.right:
            return depth
        if not self.left:
            return self.right.validate(depth + 1)
        if not self.right:
            return self.left.validate(depth + 1)
        return max(self.right.validate(depth + 1), self.left.validate(depth + 1))

    """
        Returns the matrix visualization after adding the subtree's structure to it

        Args: the updated visualization matrix (a list of strings), the current row, the current column
    """
    def visualize_pass(self, vis_matrix, row, column):
        if self.left:
            (vis_matrix, column) = self.left.visualize_pass(vis_matrix, row + 1, column)
        else:
            # Advancing the column based on the size of the node's empty left subtree
            column += int(math.pow(2, len(vis_matrix) - row - 1) - 1) * 3
        (vis_matrix, column) = self.add_value_to_vis(vis_matrix, row, column)
        if self.right:
            return self.right.visualize_pass(vis_matrix, row + 1, column)
        else:
            # Advancing the index based on the size of the node's empty right subtree
            return vis_matrix, column + int(math.pow(2, len(vis_matrix) - row - 1) - 1) * 3

    """
        Returns the matrix visualization after adding the current node to it

        Args: the updated visualization matrix (a list of strings), the current row, the current column
    """
    def add_value_to_vis(self, vis_matrix, row, column):
        if self.treasure > 0:
            prefix = "+"
            if self.treasure < 10:
                prefix += "0" + str(self.treasure)
            else:
                prefix += str(self.treasure)
        else:
            prefix = "-"
            if self.treasure > -10:
                prefix += "0" + str(self.treasure)
            else:
                prefix += str(self.treasure)
        # Adding the current node to the visualization based on its row and column in an in-order pass
        vis_matrix[row] = vis_matrix[row][:column] + prefix + vis_matrix[row][column + 3:]
        return vis_matrix, column + 3