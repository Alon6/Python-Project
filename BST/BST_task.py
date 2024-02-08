from utils import *


# Function empties MongoDB and the in-program tree
@app.route('/delete_all_treasures', methods=['DELETE'])
def delete_all_treasures_request():
    return delete_all_treasures(table, bst, logger)


# Function inserts received treasure to the BST
@app.route('/insert_treasure', methods=['POST'])
def insert_treasure():
    val_json = request.get_json()
    val = val_json.get("value", "not exists")
    if not is_float(str(val)):
        logger.error("Error, input does not contain treasure")
        return "Error, input does not contain treasure", HTTPStatus.BAD_REQUEST
    res = bst.insert(Node(val), table)
    if res[0]:
        logger.info("Treasure {} was inserted successfully".format(str(val)))
        return "Success", HTTPStatus.OK
    else:
        logger.error(res[1])
        return "Error - " + res[1], HTTPStatus.BAD_REQUEST


# Function returns BST's structure via in-order pass
@app.route('/get_treasures')
def get_treasures():
    val = bst.bst_pass("in-order")
    logger.info("The pass was a success")
    return {"treasures": val}, HTTPStatus.OK


# Function deletes received treasure from the BST
@app.route('/delete_treasure', methods=['DELETE'])
def delete_treasure():
    val_json = request.get_json()
    val = val_json.get("value", "not exists")
    if not is_float(str(val)):
        logger.error("Error, input does not contain treasure")
        return "Error, input does not contain treasure", HTTPStatus.BAD_REQUEST
    res = bst.delete(val, table)
    if res[0]:
        logger.info("Treasure {} was deleted successfully".format(str(val)))
        return "Success", HTTPStatus.OK
    else:
        logger.error(res[1])
        return "Error - " + res[1], HTTPStatus.BAD_REQUEST


# Function checks if received treasure exists in the BST
@app.route('/search_treasure', methods=['GET'])
def search_treasure():
    val = request.args.get("value", "not exists")
    if not is_float(str(val)):
        logger.error("Error, input does not contain treasure")
        return "Error, input does not contain treasure", HTTPStatus.BAD_REQUEST
    if bst.search(val):
        logger.info("Treasure {} is in the BST".format(str(val)))
        return {"message" : "Treasure found!"}, HTTPStatus.OK
    else:
        logger.info("Treasure {} is not in the BST".format(str(val)))
        return {"message" : "Treasure not found"}, HTTPStatus.BAD_REQUEST


# Function returns BST's structure via pre-order pass
@app.route('/pre_order_traversal', methods=['GET'])
def pre_order_traversal():
    val = bst.bst_pass("pre-order")
    logger.info("The pass was a success")
    return {"traversal_result": val}, HTTPStatus.OK


# Function returns BST's structure via in-order pass
@app.route('/in_order_traversal', methods=['GET'])
def in_order_traversal():
    val = bst.bst_pass("in-order")
    logger.info("The pass was a success")
    return {"traversal_result": val}, HTTPStatus.OK


# Function returns BST's structure via post-order pass
@app.route('/post_order_traversal', methods=['GET'])
def post_order_traversal():
    val = bst.bst_pass("post-order")
    logger.info("The pass was a success")
    return {"traversal_result": val}, HTTPStatus.OK


# Function returns whether the BST's structure is valid or not
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