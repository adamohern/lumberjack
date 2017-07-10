# python

import lx
import lxu.command
from bourbon import BourbonTree


class CommandClass(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__ (self)

        self.dyna_Add ("name", lx.symbol.sTYPE_STRING)
        self.dyna_Add ("price", lx.symbol.sTYPE_FLOAT)

    def cmd_DialogInit(self):
        self.attr_SetString(0, "Wild Turkey")
        self.attr_SetFlt(1, 29.99)

    def basic_Execute(self, msg, flags):

        node = BourbonTree().add_child()
        node.columns['name'].value = self.dyna_String(0)
        node.columns['price'].value = self.dyna_Float(1)

        BourbonTree().rebuild_view()

lx.bless (CommandClass, "bourbon.add")
