#!/usr/bin/python
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
#
# -------------------------------------------------------------------------------------------------

# --- Python standard library ---
from __future__ import unicode_literals
import sys
import os
import shutil
import glob
import re

# --- Import AEL modules ---
from AEL.resources.utils import *
from AEL.resources.rom_audit import *

# --- List of CVS files that will be converted ----------------------------------------------------
file_list = [
    ['Amstrad CPC', 'Amstrad CPC', 1],

    ['Atari 2600',      'Atari 2600', 1],
    ['Atari 5200',      'Atari 5200', 1],
    ['Atari 7800',      'Atari 7800', 1],
    ['Atari Jaguar',    'Atari Jaguar', 1],
    ['Atari Jaguar CD', 'Atari Jaguar CD', 1],
    ['Atari Lynx',      'Atari Lynx', 1],
    ['Atari ST',        'Atari ST', 1],

    ['Colecovision', 'Colecovision', 1],

    ['Commodore 64',       'Commodore 64', 1],
    ['commodore amiga',    'Commodore Amiga', 1],
    ['Commodore 16 Plus4', 'Commodore Plus-4', 1],
    ['Commodore VIC-20',   'Commodore VIC-20', 1],
    
    ['Magnavox Odyssey 2', 'Magnavox Odyssey2', 1],
    # ['Philips VG 5000', 'Philips Videopac+ G7000', 1],

    # ['Microsoft MSX', 'Microsoft MSX', 1],
    ['Microsoft MSX2', 'Microsoft MSX 2', 1],
    ['Microsoft MS-DOS', 'Microsoft MS-DOS', 1],
    # ['Microsoft Windows 3.x', 'Microsoft Windows', 1],

    ['NEC PC Engine', 'NEC PC Engine', 1],
    ['NEC PC Engine-CD', 'NEC PC Engine CDROM2', 1],
    ['NEC Turbo Graphx 16', 'NEC TurboGrafx 16', 1],
    ['NEC TurboGrafx-CD', 'NEC TurboGrafx CD', 1],
    ['NEC SuperGrafx', 'NEC SuperGrafx', 1],
    ['NEC PC-FX', 'NEC PC-FX', 1],

    ['Nintendo Game Boy', 'Nintendo GameBoy', 1],
    ['Nintendo Game Boy Color', 'Nintendo GameBoy Color', 1],
    ['Nintendo Game Boy Advance', 'Nintendo GameBoy Advance', 1],
    ['Nintendo DS', 'Nintendo DS', 1],
    ['Nintendo Famicom Disk System', 'Nintendo Famicom Disk System', 1],
    ['Nintendo Entertainment System', 'Nintendo NES', 1],
    ['Super Nintendo Entertainment System', 'Nintendo SNES', 1],
    ['Nintendo Virtual Boy', 'Nintendo Virtual Boy', 1],
    ['Nintendo 64', 'Nintendo 64', 1],
    ['Nintendo GameCube', 'Nintendo GameCube', 1],
    ['Nintendo Wii', 'Nintendo Wii', 1],

    ['Panasonic 3DO', 'Panasonic 3DO', 1],

    ['Sega SG-1000', 'Sega SG-1000', 1],
    ['Sega Master System', 'Sega Master System', 1],
    ['Sega Game Gear', 'Sega Game Gear', 1],
    ['Sega Genesis', 'Sega MegaDrive', 2],
    ['Sega CD', 'Sega MegaCD', 1],
    ['Sega 32x', 'Sega 32X', 1],
    # ['Sega Pico', 'Sega PICO', 1],
    ['Sega Saturn', 'Sega Saturn', 1],
    ['Sega Dreamcast', 'Sega Dreamcast', 1],

    ['Sinclair ZX Spectrum', 'Sinclair ZX Spectrum', 1],
    
    ['SNK Neo Geo CD',           'SNK Neo-Geo CD', 1],
    ['SNK Neo Geo Pocket',       'SNK Neo-Geo Pocket', 1],
    ['SNK Neo Geo Pocket Color', 'SNK Neo-Geo Pocket Color', 1],

    ['Sony PlayStation',   'Sony PlayStation', 1],
    ['Sony Playstation 2', 'Sony PlayStation 2', 1],
    ['Sony PSP',           'Sony PlayStation Portable', 1],
]

# --- Main ----------------------------------------------------------------------------------------
curr_dir   = os.getcwd()
source_dir = curr_dir + '/data_gamedb_info_csv/'
dest_dir   = curr_dir + '/data_gamedb_info_xml/'
print('Current directory is     "{}"'.format(curr_dir))
print('Source directory is      "{}"'.format(source_dir))
print('Destination directory is "{}"'.format(dest_dir))

# --- Traverse list of CVS files ---
# file_list = glob.glob(source_dir + '*.csv')
for files_tuple in file_list:
    csv_filename = os.path.join(source_dir, files_tuple[0] + '.csv')
    xml_filename = os.path.join(dest_dir, files_tuple[1] + '.xml')
    parser_type  = files_tuple[2]
    print('Processing file "{0}"'.format(csv_filename))
    print('           into "{0}"'.format(xml_filename))
    print('parser_type {0}'.format(parser_type))

    # >> Read CVS file
    with open(csv_filename, 'r') as content_file:
        cvs_text_list = content_file.readlines()

    # >> Create XML data
    str_list = []
    str_list.append('<?xml version="1.0" encoding="utf-8" standalone="yes"?>\n')
    str_list.append('<menu>\n')
    str_list.append('  <header>\n')
    str_list.append(XML_text('listname', files_tuple[1]))
    str_list.append('    <lastlistupdate></lastlistupdate>\n')
    str_list.append('    <listversion>test</listversion>\n')
    str_list.append('    <exporterversion></exporterversion>\n')
    str_list.append('  </header>\n')

    # >> Write game info
    for cvs_line in cvs_text_list:
        if parser_type == 1:
            # --- 10 data fields ---
            m = re.search('^([^>]*)>([^>]*)>([^>]*)>([^>]*)>([^>]*)>([^>]*)>([^>]*)>([^>]*)>([^>]*)>([^>]*)', cvs_line.strip())
            if m:
                # print('Adding game "{0}"'.format(text_str_2_Uni(m.group(1))))
                temp_str = text_str_2_Uni(m.group(1))
                str_list.append('  <game name="{0}">\n'.format(text_escape_XML(temp_str)))
                str_list.append(XML_text('description',  text_str_2_Uni(m.group(2)), 4))
                str_list.append(XML_text('year',         text_str_2_Uni(m.group(3)), 4))
                str_list.append(XML_text('rating',       text_str_2_Uni(m.group(4)), 4))
                str_list.append(XML_text('manufacturer', text_str_2_Uni(m.group(5)), 4))
                str_list.append(XML_text('genre',        text_str_2_Uni(m.group(7)), 4))
                str_list.append(XML_text('player',       text_str_2_Uni(m.group(9)), 4))
                str_list.append(XML_text('story',        text_str_2_Uni(m.group(10)), 4))
                str_list.append('  </game>\n')
                continue

            # --- 9 data fields ---
            m = re.search('^([^>]*)>([^>]*)>([^>]*)>([^>]*)>([^>]*)>([^>]*)>([^>]*)>([^>]*)>([^>]*)', cvs_line.strip())
            if m:
                # print('Adding game "{0}"'.format(text_str_2_Uni(m.group(1))))
                temp_str = text_str_2_Uni(m.group(1))
                str_list.append('  <game name="{0}">\n'.format(text_escape_XML(temp_str)))
                str_list.append(XML_text('description',  text_str_2_Uni(m.group(2)), 4))
                str_list.append(XML_text('year',         text_str_2_Uni(m.group(3)), 4))
                str_list.append(XML_text('rating',       text_str_2_Uni(m.group(4)), 4))
                str_list.append(XML_text('manufacturer', text_str_2_Uni(m.group(5)), 4))
                str_list.append(XML_text('genre',        text_str_2_Uni(m.group(7)), 4))
                str_list.append(XML_text('player',       text_str_2_Uni(m.group(9)), 4))
                str_list.append(XML_text('story', '', 4))
                str_list.append('  </game>\n')
                continue

            # --- 7 data fields ---
            m = re.search('^([^>]*)>([^>]*)>([^>]*)>([^>]*)>([^>]*)>([^>]*)>([^>]*)', cvs_line.strip())
            if m:
                temp_str = text_str_2_Uni(m.group(1))
                str_list.append('  <game name="{0}">\n'.format(text_escape_XML(temp_str)))
                str_list.append(XML_text('description',  text_str_2_Uni(m.group(2)), 4))
                str_list.append(XML_text('year',         text_str_2_Uni(m.group(3)), 4))
                str_list.append(XML_text('rating',       text_str_2_Uni(m.group(4)), 4))
                str_list.append(XML_text('manufacturer', text_str_2_Uni(m.group(5)), 4))
                str_list.append(XML_text('genre',        text_str_2_Uni(m.group(7)), 4))
                str_list.append(XML_text('player', '', 4))
                str_list.append(XML_text('story', '', 4))
                str_list.append('  </game>\n')
                continue

            print('Error parsing CSV line')
            print('"{0}"'.format(cvs_line.strip()))
            sys.exit(0)

        elif parser_type == 2:
            # --- 10 data fields ---
            m = re.search('^([^>]*)>([^>]*)>([^>]*)>([^>]*)>([^>]*)>([^>]*)>([^>]*)>([^>]*)>([^>]*)>([^>]*)', cvs_line.strip())
            # >> https://docs.python.org/2/library/stdtypes.html#str.split
            genre_raw_str = text_str_2_Uni(m.group(7))
            genre_str = genre_raw_str.split('|')[0]
            if m:
                # print('Adding game "{0}"'.format(text_str_2_Uni(m.group(1))))
                temp_str = text_str_2_Uni(m.group(1))
                str_list.append('  <game name="{0}">\n'.format(text_escape_XML(temp_str)))
                str_list.append(XML_text('description',  text_str_2_Uni(m.group(4)), 4))
                str_list.append(XML_text('year',         text_str_2_Uni(m.group(2)), 4))
                str_list.append(XML_text('rating',       text_str_2_Uni(m.group(3)), 4))
                str_list.append(XML_text('manufacturer', text_str_2_Uni(m.group(5)), 4))
                str_list.append(XML_text('genre',        genre_str, 4))
                str_list.append(XML_text('player',       text_str_2_Uni(m.group(9)), 4))
                str_list.append(XML_text('story',        text_str_2_Uni(m.group(10)), 4))
                str_list.append('  </game>\n')
                continue

            print('Error parsing CSV line')
            print('"{0}"'.format(cvs_line.strip()))
            sys.exit(0)
        else:
            print('Unknown parser type = {0}'.format(parser_type))
            sys.exit(0)
    str_list.append('</menu>\n')

    # >> Write XML file
    full_string = ''.join(str_list).encode('utf-8')
    file_obj = open(xml_filename, 'w')
    file_obj.write(full_string)
    file_obj.close()
print('*** Finished ***')
