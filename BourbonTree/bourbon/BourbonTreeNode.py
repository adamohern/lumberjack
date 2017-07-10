
import lumberjack, os, lx

class BourbonTreeNode(lumberjack.TreeNode):

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)
        
        self.columns['name'] = lumberjack.TreeValue()
        self.columns['name'].input_region = None
        self.columns['name'].value = ""

        self.columns['price'] = lumberjack.TreeValue()
        self.columns['price'].input_region = None
        self.columns['price'].value = ""
        
    def draggable(self):
        return True

    def canAcceptDrop(self, source_nodes):
        return True
        
    def tooltip(self, columnIndex):
        return self.columns['name'].value