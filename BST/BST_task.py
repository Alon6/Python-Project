from utils import *
app = Flask(__name__)
"""
    Deletes all of the treasures which were previously saved to MongoDB, and resets the bst variable

    Return Value: Returns whether the function has succeeded with the response status
"""
@app.route('/delete_all_treasures', methods=['DELETE'])
def delete_all_treasures_request():
    return table.delete_all_treasures(bst, logger)


"""
    Inserting a new node to the BST and MongoDB

    Args: the node which we want to insert, (needs validation)

    Return Value: Return a response based on the success/failure of the request
"""
@app.route('/insert_treasure', methods=['POST'])
def insert_treasure():
    val_json = request.get_json()
    val = val_json.get("value", "not exists")
    if not is_float(str(val)):
        logger.error("Error, input does not contain treasure")
        return "Error, input does not contain treasure", HTTPStatus.BAD_REQUEST
    (status, message) = bst.insert(Node(val), table)
    if status:
        logger.info("Treasure {} was inserted successfully".format(str(val)))
        return "Success", HTTPStatus.OK
    else:
        logger.error(message)
        return "Error - " + message, HTTPStatus.BAD_REQUEST


"""
    Returns a list which contains all of the tree's nodes which are ordered based on in order pass
"""
@app.route('/get_treasures')
def get_treasures():
    val = bst.bst_pass(TreeConstants.IN_ORDER)
    logger.info("The pass was a success")
    return {"treasures": val}, HTTPStatus.OK


"""
    Deleting a node from the BST and MongoDB

    Args: the node which we want to delete (needs validation)

    Return Value: Return a response based on the success/failure of the request
"""
@app.route('/delete_treasure', methods=['DELETE'])
def delete_treasure():
    val_json = request.get_json()
    val = val_json.get("value", "not exists")
    if not is_float(str(val)):
        logger.error("Error, input does not contain treasure")
        return "Error, input does not contain treasure", HTTPStatus.BAD_REQUEST
    (status, message) = bst.delete(val, table)
    if status:
        logger.info("Treasure {} was deleted successfully".format(str(val)))
        return "Success", HTTPStatus.OK
    else:
        logger.error(message)
        return "Error - " + message, HTTPStatus.BAD_REQUEST


"""
   Returns Whether the requested node is in the tree or not

   Args: a float which describes the treasure we want to find (needs validation)
"""
@app.route('/search_treasure', methods=['GET'])
def search_treasure():
    val = request.args.get("value", "not exists")
    if not is_float(str(val)):
        logger.error("Error, input does not contain treasure")
        return "Error, input does not contain treasure", HTTPStatus.BAD_REQUEST
    if bst.search_query(val):
        logger.info("Treasure {} is in the BST".format(str(val)))
        return {"message" : "Treasure found!"}, HTTPStatus.OK
    else:
        logger.info("Treasure {} is not in the BST".format(str(val)))
        return {"message" : "Treasure not found"}, HTTPStatus.BAD_REQUEST


"""
    Returns a list which contains all of the tree's nodes which are ordered based on pre order pass
"""
@app.route('/pre_order_traversal', methods=['GET'])
def pre_order_traversal():
    val = bst.bst_pass(TreeConstants.PRE_ORDER)
    logger.info("The pass was a success")
    return {"traversal_result": val}, HTTPStatus.OK


"""
    Returns a list which contains all of the tree's nodes which are ordered based on in order pass
"""
@app.route('/in_order_traversal', methods=['GET'])
def in_order_traversal():
    val = bst.bst_pass(TreeConstants.IN_ORDER)
    logger.info("The pass was a success")
    return {"traversal_result": val}, HTTPStatus.OK


"""
    Returns a list which contains all of the tree's nodes which are ordered based on post order pass
"""
@app.route('/post_order_traversal', methods=['GET'])
def post_order_traversal():
    val = bst.bst_pass(TreeConstants.POST_ORDER)
    logger.info("The pass was a success")
    return {"traversal_result": val}, HTTPStatus.OK


"""
    Returns whether the BST is valid or not
"""
@app.route('/validate_bst')
def validate_bst():
    if bst.validate_and_visualize(table):
        logger.info("The BST is valid")
        return {"message" : "BST is valid"}, HTTPStatus.OK
    else:
        logger.error("The BST is not valid")
        return {"message" : "BST is not valid"}, HTTPStatus.BAD_REQUEST
if __name__ == "__main__":
    # Initializing server and BST variables
    bst = Tree()
    table = MongoTable()
    # Create and configure logger
    logging.basicConfig(filename="log.log",
                        format='%(asctime)s %(message)s',
                        filemode='w')

    # Creating an object
    logger = logging.getLogger()
    logger.setLevel(0)
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