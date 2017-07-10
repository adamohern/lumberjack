# python

from bourbon import BourbonTree


# In order to be available in the GUI, a treeview needs to be "blessed" (same as
# MODO commands.) Lumberjack does all of this automatically with a single
# `bless()` method. It can only be fired once per session.

BourbonTree().bless(

    # :param viewport_type:   category in the MODO UI popup
    #                         vpapplication, vp3DEdit, vptoolbars, vpproperties, vpdataLists,
    #                         vpinfo, vpeditors, vputility, or vpembedded
    viewport_type = 'vpinfo',

    # :param nice_name:       display name for the treeview in window title bars, etc
    #                         should ideally be a message table lookup '@table@message@'
    nice_name = 'Bourbon Tree',

    # :param internal_name:   name of the treeview server (also used in config files)
    # NOTE: must be unique!
    internal_name = 'bourbon_tree',

    # :param ident:           arbitrary unique four-letter all-caps identifier (ID4)
    # NOTE: must be unique!
    ident = 'BBTR',

    # :param column_definitions:    a list of dictionaries, one for each column. Values in each
    #                               node's values dictionary must correspond with these strings
    column_definitions = {
        'primary_position': 0,
        'list': [
                {
                    'name':'name',
                    # negative integers are summed and then divided for relative widths.
                    # in this example, -1 + -3 == -4, so -1/-4 is 25%.
                    'width':-2
                }, {
                    'name':'price',
                    'width':-1
                }
            ]
    },

    # :param input_regions:   list of regions for input remapping. These can be implemented from
    #                         within the data object itself as described in TreeData(), and used
    #                         in InputRemapping config files, like this:
    #
    #                         <atom type="InputRemapping">
    #                             <hash type="Region" key="treeViewConfigName+(contextless)/(stateless)+regionName@rmb">render</hash>
    #                         </atom>
    #
    #                         NOTE: slot zero [0] in the list is reserved for the .anywhere region.
    #                         Don't use it.

    input_regions = [
        '(anywhere)', # 0 is reserved ".anywhere" region index
        'clickable_region_name'
    ],

    # :param notifiers:       Returns a list of notifier tuples for auto-updating the tree. Optional.
    #                            [
    #                                ("select.event", "polygon +ldt"),
    #                                ("select.event", "item +ldt")
    #                            ]

    # No notifiers necessary for this example.
    notifiers = []
)
