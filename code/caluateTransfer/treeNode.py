
class TreeNode():

    def __init__(self,value) -> None:
        self.value = value
        self.leftChild = None
        self.rightChild = None

    def addLeftChild(self,child):
        self.leftChild = child
        return self

    def addRightChild(self,child):
        self.rightChild = child
        return self

    def left(self):
        return self.leftChild

    def right(self):
        return self.rightChild

    def getValue(self):
        return self.value