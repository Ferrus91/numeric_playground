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

def insert(root, key):
    if root is None:
        return Node(key)
    if key < root.key:
        root.left = insert(root.left, key)
    elif key > root.key:
        root.right = insert(root.right, key)
    recalculate_balancing_factor(root)
    if abs(root.balancing_factor) > 1:
        return rebalance_tree(root)
    return root

def delete(root, key):
    if root is None:
        return None
    if key < root.key:
        root.left = delete(root.left, key)
    elif key > root.key:
        root.right = delete(root.right, key)
    else:
        if root.left is None:
            return root.right
        elif root.right is None:
            return root.left
        else:
            in_order_successor = find_in_order_successor(root)
            root.key = in_order_successor.key
            root.right = delete(root.right, in_order_successor.key)
    recalculate_balancing_factor(root)
    if abs(root.balancing_factor) > 1:
        return rebalance_tree(root)
    return root

def recalculate_balancing_factor(root):
    left_height = root.left.height if root.left is not None else 0
    right_height =  root.right.height if root.right is not None else 0
    root.height = 1 + max(left_height, right_height)
    root.balancing_factor = left_height - right_height

def rebalance_tree(root):
    if root.balancing_factor > 1:
        if root.left.balancing_factor > 0:
            return rr_rotation(root)
        else:
            return lr_rotation(root)
    elif root.balancing_factor < -1:
        if root.right.balancing_factor < 0:
            return ll_rotation(root)
        else:
            return rl_rotation(root)

def rr_rotation(root):
    rotated_root = right_rotation(root)
    return rotated_root

def lr_rotation(root):
    root.left = left_rotation(root.left)
    return right_rotation(root)

def ll_rotation(root):
    rotated_root = left_rotation(root)
    return rotated_root

def rl_rotation(root):
    root.right = right_rotation(root.right)
    return left_rotation(root)

def left_rotation(root):
    rotated_root = root.right
    rotated_root_left = rotated_root.left
    rotated_root.left = root
    root.right = rotated_root_left
    recalculate_balancing_factor(root)
    recalculate_balancing_factor(rotated_root)
    return rotated_root

def right_rotation(root):
    rotated_root = root.left
    rotated_root_right = rotated_root.right
    rotated_root.right = root
    root.left = rotated_root_right
    recalculate_balancing_factor(root)
    recalculate_balancing_factor(rotated_root)
    return rotated_root

def has_key(root, key):
    key_node = find_key(root, key)
    return key_node is not None

def find_key(root, key):
    if root is None:
        return None
    if key == root.key:
        return root
    elif key < root.key:
        return find_key(root.left, key)
    else:
        return find_key(root.right, key)

def find_in_order_successor(root):
    start = root.right
    if start is None:
        return None
    else:
        current_successor = root.right
        while current_successor.left is not None:
            current_successor = current_successor.left
        return current_successor

root = Node(random.randint(0, 100))
root = insert(root, random.randint(0, 100))
root = insert(root, random.randint(0, 100))
root = insert(root, random.randint(0, 100))
root = insert(root, random.randint(0, 100))
root = insert(root, random.randint(0, 100))
root = insert(root, random.randint(0, 100))
root = insert(root, random.randint(0, 100))
val = random.randint(0, 100)
root = insert(root, val)
root = insert(root, random.randint(0, 100))
root = insert(root, random.randint(0, 100))
root = insert(root, random.randint(0, 100))
root = insert(root, random.randint(0, 100))
root = insert(root, random.randint(0, 100))
root = insert(root, random.randint(0, 100))
root = insert(root, random.randint(0, 100))
root = insert(root, random.randint(0, 100))
root = insert(root, random.randint(0, 100))
root = insert(root, random.randint(0, 100))
root = insert(root, random.randint(0, 100))
root = insert(root, random.randint(0, 100))
root = insert(root, random.randint(0, 100))
root = insert(root, random.randint(0, 100))
root = insert(root, random.randint(0, 100))
root = insert(root, random.randint(0, 100))
root = insert(root, random.randint(0, 100))
root = insert(root, random.randint(0, 100))
root = insert(root, random.randint(0, 100))
root = insert(root, random.randint(0, 100))
root = insert(root, random.randint(0, 100))
root = insert(root, random.randint(0, 100))
root = insert(root, random.randint(0, 100))
root = insert(root, random.randint(0, 100))
root = insert(root, random.randint(0, 100))
root = insert(root, random.randint(0, 100))
root = insert(root, random.randint(0, 100))
root = insert(root, random.randint(0, 100))
print(root)
print('Deleting: ', val)
root = delete(root, val)
print(root)