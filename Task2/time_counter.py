"""
File: linkedbst.py
Author: Ken Lambert
"""

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack

from math import log
import random
import time


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, source_collection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, source_collection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            string = ""
            if node != None:
                string += recurse(node.right, level + 1)
                string += "| " * level
                string += str(node.data) + "\n"
                string += recurse(node.left, level + 1)
            return string

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""
        def recurse(node):
            if item < node.data:
                if node.left == None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            elif node.right == None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)

        if self.isEmpty():
            self._root = BSTNode(item)
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """
        Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self.
        """
        if not item in self:
            raise KeyError("Item not in tree.""")

        def lift_max_in_left_subtree_to_top(top):
            parent = top
            current_node = top.left
            while not current_node.right == None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        if self.isEmpty(): return None

        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        current_node = self._root
        while not current_node == None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = 'L'
                current_node = current_node.left
            else:
                direction = 'R'
                current_node = current_node.right

        if item_removed == None: return None

        if not current_node.left == None \
                and not current_node.right == None:
            lift_max_in_left_subtree_to_top(current_node)
        else:

            if current_node.left == None:
                new_child = current_node.right

            else:
                new_child = current_node.left

            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise.
        """
        probe = self._root
        while probe != None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        """
        Return the height of tree.
        """
        def height1(top):
            """
            Helper function.
            """
            if top is None:
                return -1
            else:
                return 1 + max(height1(top.left), height1(top.right))
        return height1(self._root)

    def is_balanced(self):
        """
        Return True if tree is balanced.
        """
        height = self.height()
        nodes = self._size
        if height < 2 * log(nodes + 1) - 1:
            return True
        return False

    def range_find(self, low, high):
        """
        Returns a list of the items in the tree, where low <= item <= high.
        """
        elements = list(self.inorder())
        res = []
        for element in elements:
            if low <= element <= high:
                res.append(element)
        return res

    def rebalance(self):
        """
        Rebalances the tree.
        """
        elements = sorted(list(self.inorder()))
        self.clear()
        self.help_func(elements)

    def help_func(self, lst):
        """
        Helping function to build a balanced tree.
        """
        mid = len(lst)//2
        self.add(lst[mid])
        lst1, lst2 = lst[:mid], lst[mid+1:]
        if len(lst1) > 0:
            self.help_func(lst1)
        if len(lst2) > 0:
            self.help_func(lst2)

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        """
        elements = sorted(list(self.inorder()))
        for element in elements:
            if element > item:
                return element
        return None

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        """
        elements = sorted(list(self.inorder()))[::-1]
        for element in elements:
            if element < item:
                return element
        return None

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        """
        words = self.read_file(path)

        start1 = time.time()
        self.first_count(words)
        first_time = time.time() - start1
        print(f"The time for searching 10,000 random words\n"
              f" in an alphabetically arranged sequence is {first_time}.")

        start2 = time.time()
        tree2 = LinkedBST()
        for i in range(900):
            tree2.add(words[i])
        self.second_count(tree2)
        second_time = time.time() - start2
        print(f"The time for searching 10,000 random words\n"
              f" in an alphabetically arranged sequence, using binary tree is {second_time}.")

        start3 = time.time()
        tree3 = LinkedBST()
        for i in range(900):
            tree3.add(random.choice(words))
        self.third_count(tree3)
        third_time = time.time() - start3
        print(f"The time for searching 10,000 random words\n"
              f" in an non alphabetic sequence, using binary tree is {third_time}.")

        start4 = time.time()
        tree4 = LinkedBST()
        for i in range(900):
            tree4.add(random.choice(words))
            tree4.rebalance()
        self.fourth_count(tree4)
        fourth_time = time.time() - start4
        print(f"The time for searching 10,000 random words\n"
              f" in an balanced binary tree is {fourth_time}.")

    @staticmethod
    def read_file(path):
        """
        Reads file and returns list with the words.
        """
        res = []
        file = open(path, "r", encoding="utf-8")
        for line in file.readlines():
            res.append(line)
        return res[:900]

    @staticmethod
    def first_count(words):
        """
        Count the time for searching 10,000 random words
        in an alphabetically arranged sequence.
        """
        res = []
        for i in range(10000):
            word = random.choice(words)
            find = words.index(word)
            res.append(find)

    @staticmethod
    def second_count(tree):
        """
        Count the time for searching 10,000 random words
        in an alphabetically arranged sequence, using binary tree.
        """
        res = []
        for i in range(10000):
            lst = list(tree.inorder())
            word = random.choice(lst)
            find = lst.index(word)
            res.append(find)

    @staticmethod
    def third_count(tree):
        """
        Count the time for searching 10,000 random words
        in an non alphabetic sequence, using binary tree.
        """
        res = []
        for i in range(10000):
            lst = list(tree.inorder())
            word = random.choice(lst)
            find = lst.index(word)
            res.append(find)

    @staticmethod
    def fourth_count(tree):
        """
        The time for searching 10,000 random words
        in an balanced binary tree.
        """
        res = []
        for i in range(10000):
            lst = list(tree.inorder())
            word = random.choice(lst)
            find = lst.index(word)
            res.append(find)
