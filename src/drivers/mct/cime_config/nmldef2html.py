#!/usr/bin/env python

"""Generator of html file for POP namelists
"""

# Typically ignore this.
# pylint: disable=invalid-name

# Disable these because this is our standard setup
# pylint: disable=wildcard-import,unused-wildcard-import,wrong-import-position

import os, sys, re

CIMEROOT = os.environ.get("CIMEROOT")
if CIMEROOT is None:
    raise SystemExit("ERROR: must set CIMEROOT environment variable")
sys.path.append(os.path.join(CIMEROOT, "scripts", "Tools"))

from standard_script_setup import *
from CIME.utils import expect
from CIME.XML.entry_id import GenericXML
from output_modelnl import print_header, print_start_table, print_row, print_end_table

logger = logging.getLogger(__name__)

###############################################################################
def _main_func(nmldoc_dir):
###############################################################################

    """Construct a `NamelistDefinition` from an XML file."""

    # Create a definition object from the xml file
    filename = "./namelist_definition_drv.xml"
    expect(os.path.isfile(filename), "File %s does not exist"%filename)
    definition = GenericXML(infile=filename)

    # Print the header for the html page
    print_header(nmldoc_dir)

    # Create a dictionary with a category key and a list of all entry nodes for each key
    category_dict = {}
    for node in definition.get_nodes("entry"):
        category = definition.get_element_text("category", root=node)
        if category in category_dict:
            category_dict[category].append(node)
        else:
            category_dict[category] = [ node ]

    # Loop over each category
    for category in category_dict:

        # Create a dictionary of with a group key and an array of group nodes for each key
        groups_dict = {}
        for node in category_dict[category]:
            group = definition.get_element_text("group", root=node)
            if group in groups_dict:
                groups_dict[group].append(node)
            else:
                groups_dict[group] = [ node ]

        # Loop over the keys
        for group_name in groups_dict:

            # Start the table for the group
            category_name = category
            category_heading = '<a name=\"%s\"   >Driver:  %s</a>' %(category_name, category_name)
            print_start_table(category_name, category_heading)

            # Loop over the nodes in each group
            for node in groups_dict[group_name]:

                # Determine the name
                # @ is used in a namelist to put the same namelist variable in multiple groups
                # in the write phase, all characters in the namelist variable name after 
                # the @ and including the @ should be removed
                name = node.get("id")
                if "@" in name:
                    name = re.sub('@.+$', "", name)

                # Create the information for this node - start with the description
                doc = ""
                desc = definition.get_element_text("desc", root=node)
                if desc is not None: 
                    doc += desc

                # add group name
                doc += "\n group name: %s " %group_name
                

                # add type
                entry_type = definition.get_element_text("type", root=node)
                doc +=  "\n\n type: %s " %(entry_type)

                # add valid_values
                valid_values = definition.get_element_text("valid_values", root=node)
                if valid_values is not None:
                    valid_values = valid_values.split(',')
                    doc += "\n valid_values:  %s" %valid_values
                    
                # add default values
                value_nodes = definition.get_nodes('value', root=node)
                if value_nodes is not None and len(value_nodes) > 0:
                    for value_node in value_nodes:
                        value = value_node.text.strip()
                        if value_node.attrib:
                            doc += "\n value is %s for: %s" %(value, value_node.attrib)
                        else:
                            doc += "\n\n default value: %s " %(value)

                # Print the information for the node
                print_row(name, doc, group_name, nmldoc_dir);

            # End the table for the group
            print_end_table()

###############################################################################

if __name__ == "__main__":

    # TODO: make these arguments that could be changed depending on where the page will be seen
    nmldoc_dir=os.path.join(CIMEROOT,"scripts","Tools","nmldoc_dir")

    _main_func(nmldoc_dir)




