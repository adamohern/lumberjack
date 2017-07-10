# Lumberjack
### A Tree View wrapper for MODO.

Lumberjack makes tree views in MODO much quicker, easier, and more robust. It can build full-featured tree views with icons, text formatting, drag-and-drop reordering, attribute nodes that show up under a (+) plus sign in the tree, and any parent/child tree structure using the normal (>) carrot twirl icon.

# Quickstart

1. Install the `BourbonTree` kit in your MODO search path.
2. Start MODO and run `bourbon.add` in the command line. Hit `enter` to accept the default values. The tree should be populated with the newly-added values.

Congratulations! You have a working tree view.

The easiest way to get started with lumberjack is to use the BourbonTree kit as a starting point for your own kit.

If you want to integrate Lumberjack with an existing kit, the Lumberjack python package is in `BourbonTree/bourbon/lumberjack`. (Be sure to nest it inside your own python package, lest your version of Lumberjack conflict with one from a different kit.)

# Overview

The BourbonTree kit does several things:

- Includes a `bourbon` package that imports the `lumberjack` package. (We always nest `lumberjack` within
  a kit-specific package to avoid conflicts when multiple kits use lumberjack at the same time.)

- Creates a subclass of `lumberjack.Lumberjack` called `BourbonTree`. (Again, we do this to avoid conflicts, but also to allow for customization of the lumberjack object.)

- Blesses `BourbonTree` in `lxserv/bourbon_bless.py`. This is where the details of the treeview are defined.

- Modifies the tree view using `lxserv/bourbon_add.py`. Modifications can be done from anywhere, including the interactive script editor within MODO.

# Lumberjack Class

`Lumberjack` is a metaclass containing everything necessary to create
and manage a working treeview in MODO.

TreeView object must be blessed in order to be available in MODO.
Several parameters are required as a prerequisite of blessing, see
bless() method for more. TreeView can only be blessed
once per session.

`Lumberjack().bless({})`

The Lumberjack() root node is available with the `.root` property, but
all of its methods are also available on the Lumberjack() object itself
for convenience and readability.

`Lumberjack().root # gets root node`
`Lumberjack().add_child(**kwargs) # equiv of .root.add_child()`
`Lumberjack().tail_commands = [TreeNode()] # add UI commands to bottom of children`

Nodes have methods for various manipulations and properties for meta
properties like row color. Note that input mapping regions can be added
to rows or individual values (i.e. cells) as needed.

`Lumberjack().children[n].selectable = False`
`Lumberjack().children[n].selected = True`
`Lumberjack().children[n].setParent(node)`
`Lumberjack().children[n].clear_children(node)`
`Lumberjack().children[n].delete()`
`Lumberjack().children[n].delete_descendants()`
`Lumberjack().children[n].row_color = row_color_string`
`Lumberjack().children[n].input_region = region_name`
`Lumberjack().children[n].children`
`Lumberjack().children[n].descendants # children, grandchildren, etc.`
`Lumberjack().children[n].ancestors # parents, grandparents, etc.`
`Lumberjack().children[n].tier # returns number of ancestors`

Nodes have a `values` property containing keys for each column in the
TreeView. The value property has set/get built-in, but also contains
properties for metadata like color, font_weight, font_style, etc.
An optional display_value overrides the value parameter for display
in the TreeView UI, but the `value` is always used internally.

`Lumberjack().children[n].columns[col_name] = value`
`Lumberjack().children[n].columns[col_name].value = value # equiv of above`
`Lumberjack().children[n].columns[col_name].display_value = display_value`
`Lumberjack().children[n].columns[col_name].input_region = region_name`
`Lumberjack().children[n].columns[col_name].color.set_with_hex("#ffffff")`
`Lumberjack().children[n].columns[col_name].font.set_bold()`
`Lumberjack().children[n].columns[col_name].font.set_italic()`

Attributes are TreeNodes that appear under the `+` sign in the MODO UI.
They have the same columns as other nodes, but are separate from the
node's children.

`Lumberjack().children[n].addAttribute(**kwargs)`
`Lumberjack().children[n].attribute[attribute_name] = attribute_value`

Various tree-wide properties and methods are available for the TreeView
from the Lumberjack object itself.

`Lumberjack().selected # list of selected nodes`
`Lumberjack().primary # most recently selected node (usually)`
`Lumberjack().all_nodes # all nodes in tree`
`Lumberjack().find(column_name, search_term) # list of matches`
`Lumberjack().clear_selection()`

Rebuild and Refresh methods are built into the various manipulation
methods in Lumberjack, so there is no need to manually Refresh or Rebuild
the treeview.

# Lumberjack().bless()

Blesses the TreeView into existence in the MODO GUI.

Requires seven arguments.

`:param viewport_type:`
category in the MODO UI popup
vpapplication, vp3DEdit, vptoolbars, vpproperties, vpdataLists,
vpinfo, vpeditors, vputility, or vpembedded

`:param nice_name:`       
display name for the treeview in window title bars, etc
should ideally be a message table lookup '@table@message@'

`:param internal_name:`   
name of the treeview server (also used in config files)

`:param ident:`           
arbitrary unique four-letter all-caps identifier (ID4)

`:param column_definitions:`
A dictionary containing, at minimum, a key called 'list' containing a list
of dictionaries corresponding to each column in the view. The 'name' strings
for each column must correspond with the value entries for each node.

Columns are semi-static in the Python API: they can be changed, but those
changes only update when a new treeview is initiated. Don't expect to change
columns on the fly.

Example:

```
column_definitions = {
    'primary_position': 1,
    'list': [
            {
                'name':'name',
                # negative integers are summed and then divided for relative widths.
                # in this example, -1 + -3 == -4, so -1/-4 is 25%.
                'width':-1
            }, {
                'name':'enable',
                # positive integers are pixel values (i.e. 20px)
                'width':20
            }, {
                'name':'value',
                'width':-3
            }
        ]
}
```

Somewhat confusingly, the "primary" column (i.e. the one with the carrot twirldown
for revealing child nodes) is not necessarily the left-most column. The items
list is a good example of this.

The TreeView API wants us to provide the "primary" column as the first item
in the list, but then _move_ it to a different slot using the `treeview_PrimaryColumnPosition()`
method. Confusing. As. Hell. And apparently it works differently internally.
Grumble grumble.

So we hack it. In the above example, we might want to move the 'name' column
to the right of the 'enable' column using the 'primary_position' key, which sets the
value returned by `treeview_PrimaryColumnPosition()`.

`:param input_regions:`   
list of regions for input remapping. These can be implemented from
within the data object itself as described in TreeData(), and used
in InputRemapping config files, like this:

```
<atom type="InputRemapping">
    <hash type="Region" key="treeViewConfigName+(contextless)/(stateless)+regionName@rmb">render</hash>
</atom>
```

NOTE: slot zero [0] in the list is reserved for the .anywhere region.
Don't use it.

```
[
    '(anywhere)',       # 0 reserved for .anywhere
    'regionNameOne',    # 1
    'regionNameTwo'     # 2
]
```

`:param notifiers:`       
Returns a list of notifier tuples for auto-updating the tree. Optional.
```
[
    ("select.event", "polygon +ldt"),
    ("select.event", "item +ldt")
]
```
