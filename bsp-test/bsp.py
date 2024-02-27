
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None



def insert(node, value):
    if value < node.value:
        if node.left:
            insert(node.left, value)
        else:
            node.left = Node(value)
    
    elif value > node.value:
        if node.right:
            insert(node.right, value)
        else:
            node.right = Node(value)

def traverse(node, player):
    if node:
        if node.value > player:
            traverse(node.left, player)
            print(node.value, end=' ')
            traverse(node.right, player)
        else:
            traverse(node.right, player)
            print(node.value, end=" ")
            traverse(node.left, player)

if __name__ == "__main__":
    objs = [6, 12, -8, 20, -15]
    root = Node(0)
    for obj in objs: 
        insert(root, obj)
    traverse(root, 4)


