# Binary Search Tree Traversals

This project demonstrates how to build a simple Binary Search Tree (BST) in Python and perform three common tree traversal methods:

- Preorder Traversal
- Inorder Traversal
- Postorder Traversal

## Problem Description

Given a set of integer keys, the program inserts them into a Binary Search Tree and prints the traversal order of the tree using different traversal strategies.

## Algorithm / Approach

The program uses standard Binary Search Tree insertion logic:

- Values smaller than the current node are inserted into the left subtree
- Values greater than or equal to the current node are inserted into the right subtree

After building the tree, the following traversal methods are applied:

- **Preorder**: Root -> Left -> Right
- **Inorder**: Left -> Root -> Right
- **Postorder**: Left -> Right -> Root

## File

- `bst_traversal_demo.py`

## How to Run

    python bst_traversal_demo.py

## Example Input

The following keys are inserted into the tree:

    [15, 10, 20, 8, 12]

## Example Output

    Preorder Traversal:
    15 10 8 12 20

    Inorder Traversal:
    8 10 12 15 20

    Postorder Traversal:
    8 12 10 20 15

## Notes

This is a simple educational example for understanding Binary Search Tree structure and traversal techniques.
