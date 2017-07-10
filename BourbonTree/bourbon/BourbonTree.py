# python

from bourbon import lumberjack
from BourbonTreeNode import BourbonTreeNode

class BourbonTree(lumberjack.Lumberjack):

    # Lumberjack use this method for creating nodes.
    # Need to be redefined to create right type node
    def create_child_node(self, **kwargs):
        return BourbonTreeNode(**kwargs)