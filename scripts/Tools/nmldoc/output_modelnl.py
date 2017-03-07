#!/usr/bin/env python

"""Utilities to generate an html web page of model namelists
"""
import os

def print_header(nmldoc_dir):

    print '''

    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

    <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>CESM Component Models Namelist Definitions </title>
    <link rel="stylesheet" type="text/css" href="/models/cesm1.0/cam/docs/namelist/nl_style_sheet.css" />
    '''

    print "<script src=%s/showinfo.js> </script>" %nmldoc_dir

    print '''
    </head>

    <body>

    <h2>Search or Browse POP2 Component Model Namelist Variables</h2>
    <p>
    This page contains the complete list of POP2 namelist variables available.  They are grouped
    by categories designed to aid browsing.  Clicking on the name of a variable will display descriptive
    information.  If search terms are entered in the text box below, the list will be condensed to contain
    only matched variables.
    </p>

    <form id="filter_form" name="filter_form" style="margin: 0px; padding: 0px;" action="javascript:void(0);">
      <table border="0" cellpadding="2" cellspacing="1">
        <tbody>
          <tr>
            <td valign="top">
              <input id="filter_text" name="filter_text" size="40"
                     onkeydown="if (event.keyCode==13) applyFilter(document.getElementById('filter_text').value);"
                     type="text">
              <input id="btn_search" value="Search Variable Names"
                     onclick="applyFilter(document.getElementById('filter_text').value);"
    		 type="button">
              <input id="btn_show_all" value="Show All Variable Names" onclick="clearFilter();return false;" type="button">
              <br>
              <label>
                <input id="logical_operator_and" name="logical_operator" value="AND" type="radio" checked> AND
              </label>
              <label>
                <input id="logical_operator_or" name="logical_operator" value="OR" type="radio"> OR
              </label>
              (separate search terms with spaces)
              <br>
              <label>
                <input id="search_help_text" name="search_help_text" type="checkbox"> Also search help text
              </label>
            </td>
          </tr>
        </tbody>
      </table>
    </form>

    <div id="filter_matches" style="visibility: hidden; margin-bottom: 10px;">
      Found <span id="filter_matches_num"></span> standard names matching query: <span id="filter_matches_query"></span>
    </div>

    <p>

    <center>
    <input id="btn_expand_help" value="Show All Help Text"  onclick="expandAllHelp();return false;"  type="button">
    <input id="btn_collapse_help" value="Collapse All Help Text" onclick="collapseAllHelp();return false;" type="button">
    </center>
    '''

def print_start_table(category, hdr):

    print "<h3><span style=\"background-color: #00FFFF\" font color=\"purple\">%s</h3></span>" %(hdr)
    print "<table id=\"%s_table\" border=\"1\" width=\"100%%\" cellpadding=\"2\" cellspacing=\"0\">" %(category)
    print '''
    <th width="80%">Namelist Variable</th>
    '''

def print_row(name, doc, group, nmldoc_dir):

    image_dir = os.path.join(nmldoc_dir,"images")

    print "<tr id=\"%s_tr\">" %name
    print "<td><a name=\"%s_%s\"></a>" %(name,group)
    print "<img id=\"%s_arrow\" src=\"%s/arrow_right.gif\">" %(name, image_dir)
    print "<code class=\"varname\">"
    print "<a href=\"javascript:void(0)\" onclick=\"toggleHelp('%s_%s')\">%s</a> " %(name, group, name)
    print "</code>"
    print "<div id=\"%s_%s_help\" style=\"display: none; padding-left: 16px; margin-top: 4px; border-top: 1px dashed  #cccccc;\">" %(name, group)
    print "<pre>%s</pre>" %(doc)
    print "</div>"
    print "</td>"
    print "</tr>"

def print_end_table():

    print '''
    </table>
    '''
