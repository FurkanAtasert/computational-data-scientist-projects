class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.key = key


# Insert a node into the tree using Binary Search Tree logic
def insert(root, key):
    if root is None:
        return Node(key)
    if key < root.key:
        root.left = insert(root.left, key)
    else:
        root.right = insert(root.right, key)
    return root


# Preorder Traversal (Root - Left - Right)
def preorder_traversal(root):
    if root:
        print(root.key, end=" ")
        preorder_traversal(root.left)
        preorder_traversal(root.right)


# Inorder Traversal (Left - Root - Right)
def inorder_traversal(root):
    if root:
        inorder_traversal(root.left)
        print(root.key, end=" ")
        inorder_traversal(root.right)


# Postorder Traversal (Left - Right - Root)
def postorder_traversal(root):
    if root:
        postorder_traversal(root.left)
        postorder_traversal(root.right)
        print(root.key, end=" ")


# Create the tree
root = None
keys = [15, 10, 20, 8, 12]  # Elements in the tree

for key in keys:
    root = insert(root, key)

print("Preorder Traversal:")
preorder_traversal(root)

print("\nInorder Traversal:")
inorder_traversal(root)

print("\nPostorder Traversal:")
postorder_traversal(root)