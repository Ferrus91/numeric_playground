import random

class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1
        self.balancing_factor = 0

    def __str__(self):
        lines, *_ = self._display_aux()
        return "\n".join(lines)

    # Thanks chatgpt!
    def _display_aux(self):
        """Returns a tuple: (lines, width, height, root_pos) for pretty-printing as ASCII."""
        # No child.
        if self.right is None and self.left is None:
            line = str(self.key)
            width = len(line)
            height = 1
            root_pos = width // 2
            return [line], width, height, root_pos

        # Only left child.
        if self.right is None:
            left_lines, left_width, left_height, left_root_pos = self.left._display_aux()
            s = str(self.key)
            s_width = len(s)
            first_line = (left_root_pos + 1) * ' ' + (left_width - left_root_pos - 1) * '_' + s
            second_line = left_root_pos * ' ' + '/' + (left_width - left_root_pos - 1 + s_width) * ' '
            shifted_lines = [line + s_width * ' ' for line in left_lines]
            return [first_line, second_line] + shifted_lines, left_width + s_width, left_height + 2, left_width + s_width // 2

        # Only right child.
        if self.left is None:
            right_lines, right_width, right_height, right_root_pos = self.right._display_aux()
            s = str(self.key)
            s_width = len(s)
            first_line = s + right_root_pos * '_' + (right_width - right_root_pos) * ' '
            second_line = (s_width + right_root_pos) * ' ' + '\\' + (right_width - right_root_pos - 1) * ' '
            shifted_lines = [s_width * ' ' + line for line in right_lines]
            return [first_line, second_line] + shifted_lines, right_width + s_width, right_height + 2, s_width // 2

        # Two children.
        left_lines, left_width, left_height, left_root_pos = self.left._display_aux()
        right_lines, right_width, right_height, right_root_pos = self.right._display_aux()
        s = str(self.key)
        s_width = len(s)
        first_line = (
            (left_root_pos + 1) * ' '
            + (left_width - left_root_pos - 1) * '_'
            + s
            + right_root_pos * '_'
            + (right_width - right_root_pos) * ' '
        )
        second_line = (
            left_root_pos * ' '
            + '/'
            + (left_width - left_root_pos - 1 + s_width + right_root_pos) * ' '
            + '\\'
            + (right_width - right_root_pos - 1) * ' '
        )
        # Pad heights if necessary
        if left_height < right_height:
            left_lines += [left_width * ' '] * (right_height - left_height)
        elif right_height < left_height:
            right_lines += [right_width * ' '] * (left_height - right_height)
        # Merge lines
        merged_lines = [
            left_line + s_width * ' ' + right_line
            for left_line, right_line in zip(left_lines, right_lines)
        ]
        return [first_line, second_line] + merged_lines, left_width + right_width + s_width, max(left_height, right_height) + 2, left_width + s_width // 2

class AVLTree():
    def __init__(self):
        self.root = None

    def __str__(self):
        return str(self.root)
    
    def insert(self, key):
        self.root = self.__insert_key(self.root, key)

    def delete(self, key):
        self.root = self.__delete_key(self.root, key)

    def has_key(self, root, key):
        key_node = self.__find_key(root, key)
        return key_node is not None

    def __insert_key(self, root, key):
        if root is None:
            return Node(key)
        if key < root.key:
            root.left = self.__insert_key(root.left, key)
        elif key > root.key:
            root.right = self.__insert_key(root.right, key)
        self.__recalculate_balancing_factor(root)
        if abs(root.balancing_factor) > 1:
            return self.__rebalance_tree(root)
        return root

    def __delete_key(self, root, key):
        if root is None:
            return None
        if key < root.key:
            root.left = self.__delete_key(root.left, key)
        elif key > root.key:
            root.right = self.__delete_key(root.right, key)
        else:
            if root.left is None:
                return root.right
            elif root.right is None:
                return root.left
            else:
                in_order_successor = self.__find_in_order_successor(root)
                root.key = in_order_successor.key
                root.right = self.__delete_key(root.right, in_order_successor.key)
        self.__recalculate_balancing_factor(root)
        if abs(root.balancing_factor) > 1:
            return  self.__rebalance_tree(root)
        return root

    def __recalculate_balancing_factor(self, root):
        left_height = root.left.height if root.left is not None else 0
        right_height =  root.right.height if root.right is not None else 0
        root.height = 1 + max(left_height, right_height)
        root.balancing_factor = left_height - right_height

    def __rebalance_tree(self, root):
        if root.balancing_factor > 1:
            if root.left.balancing_factor > 0:
                return self.__rr_rotation(root)
            else:
                return self.__lr_rotation(root)
        elif root.balancing_factor < -1:
            if root.right.balancing_factor < 0:
                return self.__ll_rotation(root)
            else:
                return self.__rl_rotation(root)

    def __rr_rotation(self, root):
        rotated_root = self.__right_rotation(root)
        return rotated_root

    def __lr_rotation(self, root):
        root.left = self.__left_rotation(root.left)
        return self.__right_rotation(root)

    def __ll_rotation(self, root):
        rotated_root = self.__left_rotation(root)
        return rotated_root

    def __rl_rotation(self, root):
        root.right = self.__right_rotation(root.right)
        return self.__left_rotation(root)

    def __left_rotation(self, root):
        rotated_root = root.right
        rotated_root_left = rotated_root.left
        rotated_root.left = root
        root.right = rotated_root_left
        self.__recalculate_balancing_factor(root)
        self.__recalculate_balancing_factor(rotated_root)
        return rotated_root

    def __right_rotation(self, root):
        rotated_root = root.left
        rotated_root_right = rotated_root.right
        rotated_root.right = root
        root.left = rotated_root_right
        self.__recalculate_balancing_factor(root)
        self.__recalculate_balancing_factor(rotated_root)
        return rotated_root

    def __find_key(self, root, key):
        if root is None:
            return None
        if key == root.key:
            return root
        elif key < root.key:
            return self.__find_key(root.left, key)
        else:
            return self.__find_key(root.right, key)

    def __find_in_order_successor(self, root):
        start = root.right
        if start is None:
            return None
        else:
            current_successor = root.right
            while current_successor.left is not None:
                current_successor = current_successor.left
            return current_successor

tree = AVLTree()
tree.insert(random.randint(0, 100))
tree.insert(random.randint(0, 100))
tree.insert(random.randint(0, 100))
tree.insert(random.randint(0, 100))
tree.insert(random.randint(0, 100))
tree.insert(random.randint(0, 100))
tree.insert(random.randint(0, 100))
tree.insert(random.randint(0, 100))
tree.insert(random.randint(0, 100))
tree.insert(random.randint(0, 100))
tree.insert(random.randint(0, 100))
tree.insert(random.randint(0, 100))
tree.insert(random.randint(0, 100))
tree.insert(random.randint(0, 100))
tree.insert(random.randint(0, 100))
tree.insert(random.randint(0, 100))
tree.insert(random.randint(0, 100))
tree.insert(random.randint(0, 100))
tree.insert(random.randint(0, 100))
tree.insert(random.randint(0, 100))
val = random.randint(0, 100)
tree.insert(val)
tree.insert(random.randint(0, 100))
tree.insert(random.randint(0, 100))
tree.insert(random.randint(0, 100))
tree.insert(random.randint(0, 100))
tree.insert(random.randint(0, 100))
tree.insert(random.randint(0, 100))
tree.insert(random.randint(0, 100))
tree.insert(random.randint(0, 100))
tree.insert(random.randint(0, 100))
tree.insert(random.randint(0, 100))
tree.insert(random.randint(0, 100))
tree.insert(random.randint(0, 100))
tree.insert(random.randint(0, 100))
tree.insert(random.randint(0, 100))
tree.insert(random.randint(0, 100))
tree.insert(random.randint(0, 100))
tree.insert(random.randint(0, 100))
tree.insert(random.randint(0, 100))
tree.insert(random.randint(0, 100))
tree.insert(random.randint(0, 100))
tree.insert(random.randint(0, 100))
print(tree)
print('Deleting: ', val)
tree.delete(val)
print(tree)
