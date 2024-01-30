
import math
from math import inf
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
            if not self.left:
                return ["left", self]
            res = self.left.actual_search(treasure)
            res.append(self)
            return res
        if not self.right:
            return ["right", self]
        res = self.right.actual_search(treasure)
        res.append(self)
        return res
    # Returning the path to the successor in the right subtree of a node
    def find_successor(self):
        # Going left until finding a node without a left child
        if not self.left:
            return [self]
        res = self.left.find_successor()
        res.append(self)
        return res
    # Passing throughout the tree and printing the nodes based on the input order
    def bst_pass(self, order, node_list):
        if order == "pre-order":
            node_list.append(self.treasure)
        if self.left:
            node_list = self.left.bst_pass(order, node_list)
        if order == "in-order":
            node_list.append(self.treasure)
        if self.right:
            node_list = self.right.bst_pass(order, node_list)
        if order == "post-order":
            node_list.append(self.treasure)
        return node_list

    # Passing throughout the tree, checking if the nodes are ordered correctly and returning the tree's depth
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
    # Passing through the tree and creating its visualization
    def visualize(self, vis, depth, index):
        if self.left:
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
        if self.right:
            return self.right.visualize(vis, depth + 1, index)
        # Advancing the index based on the size of the node's empty subtree
        return (vis, index + int(math.pow(2,len(vis) - depth - 1) - 1) * 2)