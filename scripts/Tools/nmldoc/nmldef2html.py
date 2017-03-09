#!/usr/bin/env python

"""Generator of html file for component namelists
"""

# Typically ignore this.
# pylint: disable=invalid-name

# Disable these because this is our standard setup
# pylint: disable=wildcard-import,unused-wildcard-import,wrong-import-position

import os, sys, re
import datetime

CIMEROOT = os.environ.get("CIMEROOT")
if CIMEROOT is None:
    raise SystemExit("ERROR: must set CIMEROOT environment variable")
sys.path.append(os.path.join(CIMEROOT, "scripts", "Tools"))

from standard_script_setup import *
from CIME.utils import expect
from CIME.XML.entry_id import GenericXML

# check for  dependency module
try:
    import jinja2
except:
    raise SystemExit("ERROR: nmldef2html.py depends on the jinja2 template module. " /
                     "Install using 'pip --user install jinja2'")

# global variables
_now = datetime.datetime.now().strftime('%Y-%m-%d')
_comps = ['CAM', 'CLM', 'CISM', 'POP2', 'CICE', 'RTM', 'MOSART', 'WW3', 'Driver', 'DATM', 'DLND']
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# commandline_options - parse any command line options                       
# ---------------------------------------------------------------------------
def commandline_options():
    """ Process the command line arguments.                                                                                                                                    
    """
    parser = argparse.ArgumentParser(
        description='Read the component namelist file and generate a corresponding HTML file.')

    CIME.utils.setup_standard_logging_options(parser)

    parser.add_argument('--nmlfile', nargs=1, required=True,
                        help='Fully nquailfied path to input namelist XML file.')

    parser.add_argument('--comp', nargs=1, required=True, choices=_comps, 
                        help='Component name.')

    parser.add_argument('--htmlfile', nargs=1, required=True,
                        help='Fully quailfied path to output HTML file.')

    options = parser.parse_args()

    CIME.utils.handle_standard_logging_options(options)

    return options

# ---------------------------------------------------------------------------
# def _main_func(options, nmldoc_dir)
# ---------------------------------------------------------------------------
    """Construct a `NamelistDefinition` from an XML file."""
def _main_func(options, nmldoc_dir):

    # Create a definition object from the xml file
    filename = options.nmlfile[0]
    expect(os.path.isfile(filename), "File %s does not exist"%filename)
    definition = GenericXML(infile=filename)

    # initialize a variables for the html template
    html_dict = {}
    cesm_version = 'CESM2.0'
    comp = ''
    if options.comp:
        comp = options.comp[0]

    # Create a dictionary with a category key and a list of all entry nodes for each key
    category_dict = {}
    for node in definition.get_nodes("entry"):
        category = definition.get_element_text("category", root=node)
        if category in category_dict:
            category_dict[category].append(node)
        else:
            category_dict[category] = [ node ]

    # Loop over each category and load up the html_dict
    for category in category_dict:

        # Create a dictionary of groups with a group key and an array of group nodes for each key
        groups_dict = {}
        for node in category_dict[category]:
            group = definition.get_element_text("group", root=node)
            if group in groups_dict:
                groups_dict[group].append(node)
            else:
                groups_dict[group] = [ node ]

        # Loop over the keys
        for group_name in groups_dict:
            group_list = list()

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
                raw_desc = definition.get_element_text("desc", root=node)
                if raw_desc is not None: 
                    desc = ' '.join(raw_desc.split())
                    short_desc = desc[:75] + (desc[75:] and '...')
                else:
                    desc = ''

                # add type
                entry_type = definition.get_element_text("type", root=node)

                # add valid_values
                valid_values = definition.get_element_text("valid_values", root=node)
                if valid_values is not None:
                    valid_values = valid_values.split(',')
                    
                # add default values
                value_nodes = definition.get_nodes('value', root=node)
                if value_nodes is not None and len(value_nodes) > 0:
                    for value_node in value_nodes:
                        value = value_node.text.strip()
                        if value_node.attrib:
                            value = "value is %s for: %s" %(value, value_node.attrib)
                        else:
                            value = "default value: %s " %(value)

                # create the node dictionary
                node_dict = { 'name'        : name,
                              'desc'        : desc,
                              'short_desc'  : short_desc,
                              'entry_type'  : entry_type,
                              'valid_values': valid_values,
                              'value'       : value,
                              'group_name'  : group_name}

                # append this node_dict to the group_list
                group_list.append(node_dict)

        # update the group_list for this category in the html_dict
        html_dict[category] = group_list

    # load up jinja template
    templateLoader = jinja2.FileSystemLoader( searchpath='{0}/templates'.format(nmldoc_dir) )
    templateEnv = jinja2.Environment( loader=templateLoader )

    # TODO - get the cesm_version for the CIME root
    tmplFile = 'nmldef2html.tmpl'
    template = templateEnv.get_template( tmplFile )
    templateVars = { 'html_dict'    : html_dict,
                     'today'        : _now,
                     'cesm_version' : cesm_version,
                     'comp'         : comp }
        
    # render the template
    nml_tmpl = template.render( templateVars )

    # may need to check if one already exists or not...
    # write the output file
    with open( options.htmlfile[0], 'w') as html:
        html.write(nml_tmpl)

    return 0

###############################################################################

if __name__ == "__main__":

    options = commandline_options()
    nmldoc_dir = os.path.join(CIMEROOT,"scripts","Tools","nmldoc")
    try:
        status = _main_func(options, nmldoc_dir)
        sys.exit(status)
    except Exception as error:
        print(str(error))
        sys.exit(1)




