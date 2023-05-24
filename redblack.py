class Node:
    """ A node of the tree, has a key and pointers for its children and parents and a color."""

    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.parent = None
        self.color = 1  # 1 for red, 0 for black


class RedBlackTree:
    """A class which implements a Red-Black tree, a self balancing binary tree.
    Has functions insert(key),delete(key) and search(key)."""
    #Root är svart
    #Varje löv(null barn av en nod) är svart
    #Barnen av en röd nod är svarta
    #Varje väg från en rot till lövet av den roten har lika många svarta noder

    def __init__(self):
        self.null_node = Node(None)  # Represents NULL nodes
        self.null_node.color = 0  # NULL nodes are always black
        self.root = self.null_node

    def insert(self, key):
        """ Inserts element with given value(key) into the tree."""
        new_node = Node(key)
        new_node.left = self.null_node
        new_node.right = self.null_node
        new_node.parent = self.null_node
        new_node.color = 1

        # Insert the node as in a regular BT
        self._bst_insert(new_node)

        # Fix the Red-Black Tree properties after insertion
        self._fix_insert(new_node)

    def delete(self, key):
        """ Delete a given key from the Red-Black tree. Returns none if key doesnt exist"""
        node = self._search_helper(self.root, key)  # Find the node to delete
        if node == self.null_node:
            return
        self._delete_node(node)

    def search(self, key):
        """ Search for a given key if it exists, returns node or none if it doesnt exist."""
        return self._search_helper(self.root, key)

    def _search_helper(self, node, key):
        if node == self.null_node or key == node.key:
            return node
        if key < node.key:
            return self._search_helper(node.left, key)
        else:
            return self._search_helper(node.right, key)

    def _bst_insert(self, node):
        current = self.root
        parent = self.null_node


        while current != self.null_node:
            parent = current
            if node.key < current.key:
                current = current.left
            else:
                current = current.right

        node.parent = parent
        if parent == self.null_node: #Is the tree empty if not check left and right
            self.root = node
        elif node.key < parent.key:
            parent.left = node
        else:
            parent.right = node

    def _fix_insert(self, node):
        while node.parent.color == 1:  # While the parent of the current node is red
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right
                if uncle.color == 1:
                    # Case 1: Both parent and uncle are red
                    node.parent.color = 0
                    uncle.color = 0
                    node.parent.parent.color = 1
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        # Case 2: Node is a right child
                        node = node.parent
                        self._left_rotate(node)
                    # Case 3: Node is a left child
                    node.parent.color = 0
                    node.parent.parent.color = 1
                    self._right_rotate(node.parent.parent)
            else:
                uncle = node.parent.parent.left
                if uncle.color == 1:
                    # Case 1: Both parent and uncle are red
                    node.parent.color = 0
                    uncle.color = 0
                    node.parent.parent.color = 1
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        # Case 2: Node is a left child
                        node = node.parent
                        self._right_rotate(node)
                    # Case 3: Node is a right child
                    node.parent.color = 0
                    node.parent.parent.color = 1
                    self._left_rotate(node.parent.parent)

        self.root.color = 0  # Ensure the root is always black

    def _right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.null_node:
            y.right.parent = x
        y.parent = x.parent
        if x.parent == self.null_node:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def _left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.null_node:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == self.null_node:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def _transplant(self, u, v):
        if u.parent == self.null_node:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def _delete_node(self, node):
        y = node
        y_original_color = y.color  # Store the original color of y

        if node.left == self.null_node:
            x = node.right  # Case 1: Left child is null
            self._transplant(node, node.right)
        elif node.right == self.null_node:
            x = node.left  # Case 2: Right child is null
            self._transplant(node, node.left)
        else:
            y = self._minimum(node.right)  # Case 3: Neither children are null
            y_original_color = y.color
            x = y.right
            if y.parent == node:
                x.parent = y
            else:
                self._transplant(y, x)
                x = node.right
                y.right.parent = y
            self._transplant(node, y)
            y.left = node.left
            y.left.parent = y
            y.color = node.color

        if y_original_color == 0:  # Fix any violations caused by deletion
            self._fix_delete(x)

    def _minimum(self, node):
        while node.left != self.null_node:
            node = node.left
        return node

    def _fix_delete(self, node):
        while node != self.root and node.color == 0:
            if node == node.parent.left:
                sibling = node.parent.right

                if sibling.color == 1:
                    sibling.color = 0
                    node.parent.color = 1
                    self._left_rotate(node.parent)
                    sibling = node.parent.right

                if sibling.left.color == 0 and sibling.right.color == 0:
                    sibling.color = 1
                    node = node.parent
                else:
                    if sibling.right.color == 0:
                        sibling.left.color = 0
                        sibling.color = 1
                        self._right_rotate(sibling)
                        sibling = node.parent.right

                    sibling.color = node.parent.color
                    node.parent.color = 0
                    sibling.right.color = 0
                    self._left_rotate(node.parent)
                    node = self.root
            else:
                sibling = node.parent.left

                if sibling.color == 1:
                    sibling.color = 0
                    node.parent.color = 1
                    self._right_rotate(node.parent)
                    sibling = node.parent.left

                if sibling.right.color == 0 and sibling.left.color == 0:
                    sibling.color = 1
                    node = node.parent
                else:
                    if sibling.left.color == 0:
                        sibling.right.color = 0
                        sibling.color = 1
                        self._left_rotate(sibling)
                        sibling = node.parent.left

                    sibling.color = node.parent.color
                    node.parent.color = 0
                    sibling.left.color = 0
                    self._right_rotate(node.parent)
                    node = self.root

        node.color = 0

# Initialize red-black tree object
rbt = RedBlackTree()

# Testing 

rbt.insert(10)
rbt.insert(5)
rbt.insert(15)
rbt.insert(3)
rbt.insert(7)
rbt.insert(12)
rbt.insert(18)

assert rbt.search(10).key == 10
assert rbt.search(11) == rbt.null_node

rbt.delete(12)
assert rbt.search(12).key != 12

rbt.insert(50)
assert rbt.search(50).key == 50

rbt.delete(100)
rbt.insert(50)
