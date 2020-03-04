#!/usr/bin/python -B
# -*- coding: utf-8 -*-

# Updated GameDBInfo XML (copies them to correct place).

# Copyright (c) 2016-2020 Wintermute0110 <wintermute0110@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.

# --- INSTRUCTIONS --------------------------------------------------------------------------------
# AOS XML files must have the following fields. All fields are strings.
#
# <game ROM="ROM file name">
#     <title />
#     <year />
#     <genre />
#     <publisher />
#     <developer />
#     <rating />    (ESRB rating or other rating)
#     <nplayers />
#     <score />     (Score is how good is the game)
#     <plot />
# </game>"
#
# Some databases need to be merged, for example "NEC PC Engine.csv" and "NEC TurboGrafx 16.csv"
#
# As usual MAME is a special case. Plots should be extracted from the CSV and merged with
# the MAME_raw.xml and catver.ini files.
# -------------------------------------------------------------------------------------------------

# --- Python standard library ---
from __future__ import unicode_literals
import csv
import glob
import os
import re
import shutil
import sys

# --- Import AEL modules ---
if __name__ == "__main__" and __package__ is None:
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'AEL'))
    print('Adding to sys.path {}'.format(path))
    sys.path.append(path)
from resources.utils import *
from resources.platforms import *

# --- List of CVS files that will be converted ----------------------------------------------------
# If a CSV/platform long_name is not here then it uses parser 1
CSV_parser_dic = {
    'Sega Mega Drive' : 2,
}

# DEBUG list of platforms
# AEL_platform_list = [ 'Nintendo SNES', ]

# --- Main ----------------------------------------------------------------------------------------
curr_dir   = os.getcwd()
source_dir = curr_dir + '/data_gamedb_info_csv/'
dest_dir   = curr_dir + '/output_AOS_xml_v1/'
print('Current directory is     "{}"'.format(curr_dir))
print('Source directory is      "{}"'.format(source_dir))
print('Destination directory is "{}"'.format(dest_dir))

# --- Traverse list of CVS files ---
# * CSV basename is the same as AEL platform long_name
# * If the CSV cannot be opened then create an empty XML file, just with the header.
#
# Traverse list of platforms, open CSV files, parse them and write XML.
for platform_long_name in AEL_platform_list:
    print('')
    pobj = AEL_platforms[platform_long_to_index_dic[platform_long_name]]

    # Skip alias platforms (use parent XML).
    if pobj.aliasof is not None:
        print('Platform {} is alias of {}. Skipping.'.format(pobj.compact_name, pobj.compact_name))
        continue

    # Skip Unknown platform
    if pobj.long_name == PLATFORM_UNKNOWN_LONG:
        print('Skipping Unknown platform.')
        continue

    # Skip MAME.
    if pobj.long_name == 'MAME':
        print('Skipping MAME platform.')
        continue

    # Determine file names
    csv_basename = pobj.long_name
    xml_basename = pobj.long_name
    csv_filename = os.path.join(source_dir, csv_basename + '.csv')
    xml_filename = os.path.join(dest_dir, xml_basename + '.xml')
    print('Processing "{}"'.format(csv_filename))
    print('into       "{}"'.format(xml_filename))

    # Determine parser type.
    if csv_basename in CSV_parser_dic:
        parser_type = CSV_parser_dic[csv_basename]
    else:
        print('Using default parser type.')
        parser_type = 1
    print('Using parser_type {}'.format(parser_type))

    # Test if CSV file exists
    csv_text_list = []
    if os.path.exists(csv_filename):
        print('CSV file found. Reading it.')
        with open(csv_filename, 'rb') as f:
            reader = csv.reader(f, delimiter = str('>'))
            for row in reader: csv_text_list.append(row)
    else:
        print('CSV file NOT found. Creating empty XML file.')

    # Create XML data
    str_list = []
    str_list.append('<?xml version="1.0" encoding="utf-8" standalone="yes"?>\n')
    str_list.append('<menu>\n')
    str_list.append('<header>\n')
    str_list.append(XML_text('listname', csv_basename))
    str_list.append('  <lastlistupdate></lastlistupdate>\n')
    str_list.append('  <listversion>V1</listversion>\n')
    str_list.append('  <exporterversion>V1 GameDBInfo converter</exporterversion>\n')
    str_list.append('</header>\n')

    # Write game info
    num_line = 0
    for csv_row in csv_text_list:
        num_line += 1
        num_fields = len(csv_row)

        # --- Parser 1 (default). Example for the SNES. ---
        # 0 | ROM       | 2020 Super Baseball (USA)>
        # 1 | title     | 2020 Super Baseball>
        # 2 | year      | 1993>
        # 3 | rating    | ESRB - RP (Rating Pending)>
        # 4 | publisher | Tradewest>
        # 5 | developer | Pallas>
        # 6 | genre     | Sports/Baseball>
        # 7 | rating    | 4.6>
        # 8 | nplayers  | 1-2 Players>
        # 9 | plot      | In the year 2020, baseball finally evolved...
        if parser_type == 1:
            ROM_str = text_str_2_Uni(csv_row[0])
            str_list.append('<game ROM="{}">\n'.format(text_escape_XML(ROM_str)))
            if num_fields > 1: str_list.append(XML_text('title', text_str_2_Uni(csv_row[1])))
            if num_fields > 2: str_list.append(XML_text('year', text_str_2_Uni(csv_row[2])))
            if num_fields > 6: str_list.append(XML_text('genre', text_str_2_Uni(csv_row[6])))
            if num_fields > 4: str_list.append(XML_text('publisher', text_str_2_Uni(csv_row[4])))
            if num_fields > 5: str_list.append(XML_text('developer', text_str_2_Uni(csv_row[5])))
            if num_fields > 3: str_list.append(XML_text('rating', text_str_2_Uni(csv_row[3])))
            if num_fields > 8: str_list.append(XML_text('nplayers', text_str_2_Uni(csv_row[8])))
            if num_fields > 7: str_list.append(XML_text('score', text_str_2_Uni(csv_row[7])))
            if num_fields > 9: str_list.append(XML_text('plot', text_str_2_Uni(csv_row[9])))
            str_list.append('</game>\n')
            continue

        # --- Parser 2. Example from Mega Drive. ---
        # 0 | ROM       | Alisia Dragoon (USA)>
        # 1 | year      | 1992>
        # 2 | rating    | HSRS - GA (General Audience)>
        # 3 | title     | Alisia Dragoon>
        # 4 | publisher | SEGA of America, Inc.>
        # 5 | developer | Game Arts Co., Ltd.>
        # 6 | genre     | Action>
        # 7 | score     | 3.8>
        # 8 | nplayers  | 1 Player>
        # 9 | plot      | Alisia Dragoon is the female protagonist ...
        elif parser_type == 2:
            ROM_str = text_str_2_Uni(csv_row[0])
            str_list.append('<game ROM="{}">\n'.format(text_escape_XML(ROM_str)))
            if num_fields > 3: str_list.append(XML_text('title', text_str_2_Uni(csv_row[3])))
            if num_fields > 1: str_list.append(XML_text('year', text_str_2_Uni(csv_row[1])))
            if num_fields > 6: str_list.append(XML_text('genre', text_str_2_Uni(csv_row[6])))
            if num_fields > 4: str_list.append(XML_text('publisher', text_str_2_Uni(csv_row[4])))
            if num_fields > 5: str_list.append(XML_text('developer', text_str_2_Uni(csv_row[5])))
            if num_fields > 7: str_list.append(XML_text('rating', text_str_2_Uni(csv_row[7])))
            if num_fields > 8: str_list.append(XML_text('nplayers', text_str_2_Uni(csv_row[8])))
            if num_fields > 7: str_list.append(XML_text('score', text_str_2_Uni(csv_row[7])))
            if num_fields > 9: str_list.append(XML_text('plot', text_str_2_Uni(csv_row[9])))
            str_list.append('</game>\n')
            continue

        else:
            print('Unknown parser type = {}'.format(parser_type))
            sys.exit(1)
    str_list.append('</menu>\n')

    # Write XML file
    full_string = ''.join(str_list).encode('utf-8')
    file_obj = open(xml_filename, 'w')
    file_obj.write(full_string)
    file_obj.close()
print('*** Finished ***')
