#!/usr/bin/python3 -B
# -*- coding: utf-8 -*-

# Convert MAME output XML into a simplified XML suitable for offline scrapping.

# Copyright (c) 2016-2020 Wintermute0110 <wintermute0110@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# --- INSTRUCTIONS -------------------------------------------------------------
# To create the MAME XML file type
#
# $ mame -listxml > MAME_raw.xml
#
# Place catver.ini in this directory. Then, run this utility,
#
# $ ./v1_convert_MAME_XML_to_AOS_XML.py
#
# The output file will be named MAME.xml

# Download Catver.ini from ProgrettoSnaps: 
# [Web]   http://www.progettosnaps.net/catver/
# [File]  http://www.progettosnaps.net/catver/packs/pS_CatVer.zip
# ------------------------------------------------------------------------------

# --- Python standard library ---
from __future__ import unicode_literals
import io
import json
import re
import sys
import time
import xml.etree.ElementTree

# --- Configuration ------------------------------------------------------------------------------
Catver_ini_filename        = './data_mame/catver.ini'
NPLayers_ini_filename      = './data_mame/nplayers.ini'
MAME_XML_filename          = './data_mame/MAME.xml'
output_filename            = './output_AOS_xml_v1/MAME.xml'
output_filename_BIOS       = './output_AOS_xml_v1/MAME_BIOSes.json'
output_filename_Devices    = './output_AOS_xml_v1/MAME_Devices.json'
output_filename_Mechanical = './output_AOS_xml_v1/MAME_Mechanical.json'
OPTION_COMPACT_JSON = False

# --- Functions ----------------------------------------------------------------------------------
def XML_text(tag_name, tag_text = '', num_spaces = 2):
    if tag_text:
        tag_text = text_escape_XML(tag_text)
        line = '{}<{}>{}</{}>'.format(' ' * num_spaces, tag_name, tag_text, tag_name)
    else:
        line = '{}<{} />'.format(' ' * num_spaces, tag_name)
    return line

def text_escape_XML(data_str):
    # Ampersand MUST BE replaced FIRST
    data_str = data_str.replace('&', '&amp;')
    data_str = data_str.replace('>', '&gt;')
    data_str = data_str.replace('<', '&lt;')
    data_str = data_str.replace("'", '&apos;')
    data_str = data_str.replace('"', '&quot;')
    data_str = data_str.replace('\n', '&#10;')
    data_str = data_str.replace('\r', '&#13;')
    data_str = data_str.replace('\t', '&#9;')

    return data_str

def text_unescape_XML(data_str):
    data_str = data_str.replace('&quot;', '"')
    data_str = data_str.replace('&apos;', "'")
    data_str = data_str.replace('&lt;', '<')
    data_str = data_str.replace('&gt;', '>')
    data_str = data_str.replace('&#10;', '\n')
    data_str = data_str.replace('&#13;', '\r')
    data_str = data_str.replace('&#9;', '\t')
    # Ampersand MUST BE replaced LAST
    data_str = data_str.replace('&amp;', '&')

    return data_str

def fs_write_JSON_file(json_filename, json_data, verbose = True):
    l_start = time.time()
    if verbose:
        print('fs_write_JSON_file() "{}"'.format(json_filename))
    try:
        with io.open(json_filename, 'wt', encoding='utf-8') as file:
            if OPTION_COMPACT_JSON:
                file.write(json.dumps(json_data, ensure_ascii = False, sort_keys = True))
            else:
                file.write(json.dumps(json_data, ensure_ascii = False, sort_keys = True,
                    indent = 1, separators = (',', ':')))
    except OSError:
        kodi_notify('Advanced MAME Launcher',
                    'Cannot write {} file (OSError)'.format(json_filename))
    except IOError:
        kodi_notify('Advanced MAME Launcher',
                    'Cannot write {} file (IOError)'.format(json_filename))
    l_end = time.time()
    if verbose:
        write_time_s = l_end - l_start
        print('fs_write_JSON_file() Writing time {:f} s'.format(write_time_s))

# --- Load catver.ini ----------------------------------------------------------------------------
# Copy this function from AML source code.
print('Parsing ' + Catver_ini_filename)
categories_dic = {}
categories_set = set()
__debug_do_list_categories = False
read_status = 0
try:
    # read_status FSM values
    # 0 -> Looking for '[Category]' tag
    # 1 -> Reading categories
    # 2 -> Categories finished. STOP
    f = open(Catver_ini_filename, 'rt')
    for cat_line in f:
        stripped_line = cat_line.strip()
        if __debug_do_list_categories: print('Line "' + stripped_line + '"')
        if read_status == 0:
            if stripped_line == '[Category]':
                if __debug_do_list_categories: print('Found [Category]')
                read_status = 1
        elif read_status == 1:
            line_list = stripped_line.split("=")
            if len(line_list) == 1:
                read_status = 2
                continue
            else:
                if __debug_do_list_categories: print(line_list)
                machine_name = line_list[0]
                category = line_list[1]
                # Use first category only.
                cat_list = category.split(' / ')
                if len(cat_list) != 2: raise RuntimeError
                category = cat_list[0].strip()
                if machine_name not in categories_dic:
                    categories_dic[machine_name] = category
                categories_set.add(category)
        elif read_status == 2:
            print('Reached end of categories parsing.')
            break
        else:
            print('Unknown read_status FSM value. Aborting.')
            sys.exit(10)
    f.close()
except:
    raise RuntimeError
print('Catver Number of machines   {:6d}'.format(len(categories_dic)))
print('Catver Number of categories {:6d}'.format(len(categories_set)))

# --- Load nplayers.ini --------------------------------------------------------------------------
# Copy this function from AML source code.
__debug_do_list_categories = False
print('mame_load_nplayers_ini() Parsing "{}"'.format(NPLayers_ini_filename))
nplayers_dic = {
    'version' : 'unknown',
    'unique_categories' : True,
    'single_category' : False,
    'isValid' : False,
    'data' : {},
    'categories' : set(),
}

# --- read_status FSM values ---
# 0 -> Looking for '[NPlayers]' tag
# 1 -> Reading categories
# 2 -> Categories finished. STOP
read_status = 0
try:
    f = open(NPLayers_ini_filename, 'rt')
except IOError:
    print('mame_load_nplayers_ini() (IOError) opening "{}"'.format(NPLayers_ini_filename))
    raise RuntimeError
for cat_line in f:
    stripped_line = cat_line.strip()
    if __debug_do_list_categories: log_debug('Line "' + stripped_line + '"')
    if read_status == 0:
        m = re.search(r'NPlayers ([0-9\.]+) / ', stripped_line)
        if m: nplayers_dic['version'] = m.group(1)
        if stripped_line == '[NPlayers]':
            if __debug_do_list_categories: log_debug('Found [NPlayers]')
            read_status = 1
    elif read_status == 1:
        line_list = stripped_line.split("=")
        if len(line_list) == 1:
            read_status = 2
            continue
        else:
            machine_name, current_category = str(line_list[0]), str(line_list[1])
            if __debug_do_list_categories: log_debug('"{0}" / "{1}"'.format(machine_name, current_category))
            nplayers_dic['categories'].add(current_category)
            if machine_name in nplayers_dic['data']:
                # Force a single category to avoid nplayers.ini bugs.
                pass
                # nplayers_dic['data'][machine_name].add(current_category)
                # log_debug('machine "{0}"'.format(machine_name))
                # log_debug('current_category "{0}"'.format(current_category))
                # log_debug('"{0}"'.format(unicode(nplayers_dic['data'][machine_name])))
                # raise ValueError('unique_categories False')
            else:
                nplayers_dic['data'][machine_name] =  [current_category]
    elif read_status == 2:
        print('mame_load_nplayers_ini() Reached end of nplayers parsing.')
        break
    else:
        raise ValueError('Unknown read_status FSM value')
f.close()
nplayers_dic['single_category'] = True if len(nplayers_dic['categories']) == 1 else False
# nplayers.ini has repeated machines, so checking for unique_cateogories is here.
for m_name in sorted(nplayers_dic['data']):
    if len(nplayers_dic['data'][m_name]) > 1:
        nplayers_dic['unique_categories'] = False
        break
# If categories are unique for each machine transform lists into strings
if nplayers_dic['unique_categories']:
    for m_name in nplayers_dic['data']:
        nplayers_dic['data'][m_name] = nplayers_dic['data'][m_name][0]
print('mame_load_nplayers_ini() Machines           {}'.format(len(nplayers_dic['data'])))
print('mame_load_nplayers_ini() Categories         {}'.format(len(nplayers_dic['categories'])))
print('mame_load_nplayers_ini() Version            {}'.format(nplayers_dic['version']))
print('mame_load_nplayers_ini() unique_categories  {}'.format(nplayers_dic['unique_categories']))
print('mame_load_nplayers_ini() single_category    {}'.format(nplayers_dic['single_category']))

# ------------------------------------------------------------------------------------------------
# Incremental Parsing approach B (from [1])
# ------------------------------------------------------------------------------------------------
# Do not load whole MAME XML into memory! Use an iterative parser to
# grab only the information we want and discard the rest.
# See http://effbot.org/zone/element-iterparse.htm [1]
__debug_MAME_XML_parser = False
xml_iter = xml.etree.ElementTree.iterparse(MAME_XML_filename, events=("start", "end"))
event, root = next(xml_iter)
mame_version_str = 'MAME ' + root.attrib['build']
print('MAME version is "{}"'.format(mame_version_str))

# --- Data variables ---
# Create a dictionary of the form,
#   machines = { 'machine_name': machine, ...}
#
# where,
#   machine = {
#     'name' : '', 'description' : '', 'year' : '', 'manufacturer' : ''
#   }
machines = {}
BIOS_set = set()
Devices_set = set()
Mechanical_set = set()
machine_name = ''
num_iteration = 0
num_machines = 0
print('Reading MAME XML file ...')
for event, elem in xml_iter:
    # Debug the elements we are iterating from the XML file
    # print('event "{}"'.format(event))
    # print('elem.tag "{}" | elem.text "{}" | elem.attrib "{}"'.format(elem.tag, elem.text, str(elem.attrib)))

    # Get MAME version
    if event == "start" and elem.tag == "machine":
        machine = {
            'ROM' : '',
            'isBIOS' : False,
            'isDevice' : False,
            'isMechanical' : False,
            'description' : '',
            'year' : '',
            'manufacturer' : '',
        }
        machine_name = elem.attrib['name']
        machine['ROM'] = machine_name
        num_machines += 1
        if __debug_MAME_XML_parser:
            print('New machine      {}'.format(machine_name))

        # Check <machine> attributes.
        if 'isbios' in elem.attrib:
            machine['isBIOS'] = True if elem.attrib['isbios'] == 'yes' else False
        else:
            machine['isBIOS'] = False
        if 'isdevice' in elem.attrib:
            machine['isDevice'] = True if elem.attrib['isdevice'] == 'yes' else False
        else:
            machine['isDevice'] = False
        if 'ismechanical' in elem.attrib:
            machine['isMechanical'] = True if elem.attrib['ismechanical'] == 'yes' else False
        else:
            machine['isMechanical'] = False

        if machine['isBIOS']: BIOS_set.add(machine_name)
        if machine['isDevice']: Devices_set.add(machine_name)
        if machine['isMechanical']: Mechanical_set.add(machine_name)

    elif event == "start" and elem.tag == "description":
        if elem.text is None: print('machine {} description is None'.format(machine_name))
        description = elem.text if elem.text is not None else 'Python None'
        machine['description'] = description
        if __debug_MAME_XML_parser:
            print('     description {}'.format(description))

    elif event == "start" and elem.tag == "year":
        machine['year'] = str(elem.text)
        if __debug_MAME_XML_parser:
            print('            year {}'.format(machine['year']))

    elif event == "start" and elem.tag == "manufacturer":
        if elem.text is None: print('machine {} manufacturer is None'.format(machine_name))
        manufacturer = elem.text if elem.text is not None else 'Python None'
        machine['manufacturer'] = manufacturer
        if __debug_MAME_XML_parser:
            print('    manufacturer {}'.format(machine['manufacturer']))

    elif event == "end" and elem.tag == "machine":
        if __debug_MAME_XML_parser:
            print('Deleting machine {}'.format(machine_name))
        elem.clear()
        machines[machine_name] = machine

    # --- Print something to prove we are doing stuff ---
    num_iteration += 1
    if num_iteration % 200000 == 0:
      print('Processed {:10,d} events ({:6,d} machines so far)...'.format(num_iteration, num_machines))

    # --- Stop after some iterations for debug ---
    # if num_iteration > 200000: break
print('Processed {:,} MAME XML events'.format(num_iteration))
print('Total number of machines {:,}'.format(num_machines))

# --- Now write simplified XML output file -------------------------------------------------------
print('Generating output XML...')
o_sl = []
o_sl.append('<?xml version="1.0" encoding="utf-8" standalone="yes"?>')
o_sl.append('<menu>')
o_sl.append('<header>')
o_sl.append('  <listname>MAME</listname>')
o_sl.append('  <lastlistupdate></lastlistupdate>')
o_sl.append('  <listversion>{}</listversion>'.format(mame_version_str))
o_sl.append('  <exporterversion>v1_convert_MAME_XML_to_AOS_XML.py</exporterversion>')
o_sl.append('</header>')
for key in sorted(machines):
    o_sl.append('<game ROM="{}">'.format(machines[key]['ROM']))
    o_sl.append(XML_text('title', machines[key]['description']))
    o_sl.append(XML_text('year', machines[key]['year']))
    o_sl.append(XML_text('genre', categories_dic[key] if key in categories_dic else '[Not set]'))
    o_sl.append(XML_text('developer', machines[key]['manufacturer']))
    # Do not print unused fields in the XML to save space. They will generated to default ''.
    # o_sl.append(XML_text('publisher'))
    # o_sl.append(XML_text('rating'))
    o_sl.append(XML_text('nplayers', nplayers_dic['data'][key] if key in nplayers_dic['data'] else '[Not set]'))
    # o_sl.append(XML_text('score'))
    # o_sl.append(XML_text('plot'))
    # MAME additional fields. Put them in separate JSON files.
    # o_sl.append(XML_text('isBIOS', unicode(machines[key]['isBIOS'])))
    # o_sl.append(XML_text('isDevice', unicode(machines[key]['isDevice'])))
    # o_sl.append(XML_text('isMechanical', unicode(machines[key]['isMechanical'])))
    o_sl.append('</game>')
o_sl.append('</menu>')

print('Writing file "{}"'.format(output_filename))
with open(output_filename, 'w', encoding='utf-8') as file:
    file.write('\n'.join(o_sl))

print('Writing file "{}"'.format(output_filename_BIOS))
fs_write_JSON_file(output_filename_BIOS, list(sorted(BIOS_set)))

print('Writing file "{}"'.format(output_filename_Devices))
fs_write_JSON_file(output_filename_Devices, list(sorted(Devices_set)))

print('Writing file "{}"'.format(output_filename_Mechanical))
fs_write_JSON_file(output_filename_Mechanical, list(sorted(Mechanical_set)))
