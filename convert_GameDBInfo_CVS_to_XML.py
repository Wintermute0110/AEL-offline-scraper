#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Updated GameDBInfo XML (copies them to correct place).
#

# Copyright (c) 2016 Wintermute0110 <wintermute0110@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

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

# --- List of CVS files that will be converted ----------------------------------------------------
file_list = [
    ['Atari 2600',      'Atari 2600'],
    ['Atari 5200',      'Atari 5200'],
    ['Atari 7800',      'Atari 7800'],
    ['Atari Jaguar',    'Atari Jaguar'],
    ['Atari Jaguar CD', 'Atari Jaguar CD'],
    ['Atari Lynx',      'Atari Lynx'],
    ['Atari ST',        'Atari ST'],

    ['Colecovision', 'Colecovision'],

    ['Commodore 64',       'Commodore 64'],
    ['commodore amiga',    'Commodore Amiga'],
    ['Commodore 16 Plus4', 'Commodore Plus-4'],
    ['Commodore VIC-20',   'Commodore VIC-20'],
    
    ['Magnavox Odyssey 2', 'Magnavox Odyssey2'],
    # ['Philips VG 5000', 'Philips Videopac+ G7000'],

    # ['Microsoft MSX', 'Microsoft MSX'],
    ['Microsoft MSX2', 'Microsoft MSX 2'],
    ['Microsoft MS-DOS', 'Microsoft MS-DOS'],
    # ['Microsoft Windows 3.x', 'Microsoft Windows'],

    ['NEC PC Engine', 'NEC PC Engine'],
    ['NEC PC Engine-CD', 'NEC PC Engine CDROM2'],
    ['NEC Turbo Graphx 16', 'NEC TurboGrafx 16'],
    ['NEC TurboGrafx-CD', 'NEC TurboGrafx CD'],
    ['NEC SuperGrafx', 'NEC SuperGrafx'],
    ['NEC PC-FX', 'NEC PC-FX'],

    ['Nintendo Game Boy', 'Nintendo GameBoy'],
    ['Nintendo Game Boy Color', 'Nintendo GameBoy Color'],
    ['Nintendo Game Boy Advance', 'Nintendo GameBoy Advance'],
    ['Nintendo DS', 'Nintendo DS'],
    ['Nintendo Famicom Disk System', 'Nintendo Famicom Disk System'],
    ['Nintendo Entertainment System', 'Nintendo NES'],
    ['Super Nintendo Entertainment System', 'Nintendo SNES'],
    ['Nintendo Virtual Boy', 'Nintendo Virtual Boy'],
    ['Nintendo 64', 'Nintendo 64'],
    ['Nintendo GameCube', 'Nintendo GameCube'],
    ['Nintendo Wii', 'Nintendo Wii'],

    ['Panasonic 3DO', 'Panasonic 3DO'],

    ['Sega SG-1000', 'Sega SG-1000'],
    ['Sega Master System', 'Sega Master System'],
    ['Sega Game Gear', 'Sega Game Gear'],
    ['Sega Genesis', 'Sega MegaDrive'],
    ['Sega CD', 'Sega MegaCD'],
    ['Sega 32x', 'Sega 32X'],
    # ['Sega Pico', 'Sega PICO'],
    ['Sega Saturn', 'Sega Saturn'],
    ['Sega Dreamcast', 'Sega Dreamcast'],

    ['Sinclair ZX Spectrum', 'Sinclair ZX Spectrum'],
    
    ['SNK Neo Geo CD',           'SNK Neo-Geo CD'],
    ['SNK Neo Geo Pocket',       'SNK Neo-Geo Pocket'],
    ['SNK Neo Geo Pocket Color', 'SNK Neo-Geo Pocket Color'],

    ['Sony PlayStation',   'Sony PlayStation'],
    ['Sony Playstation 2', 'Sony PlayStation 2'],
    ['Sony PSP',           'Sony PlayStation Portable'],
]

# >> AEL functions. Import AEL module!!!
# Some XML encoding of special characters:
#   {'\n': '&#10;', '\r': '&#13;', '\t':'&#9;'}
#
# See http://stackoverflow.com/questions/1091945/what-characters-do-i-need-to-escape-in-xml-documents
# See https://wiki.python.org/moin/EscapingXml
# See https://github.com/python/cpython/blob/master/Lib/xml/sax/saxutils.py
# See http://stackoverflow.com/questions/2265966/xml-carriage-return-encoding
#
def text_escape_XML(data_str):
    # Ampersand MUST BE replaced FIRST
    data_str = data_str.replace('&', '&amp;')
    data_str = data_str.replace('>', '&gt;')
    data_str = data_str.replace('<', '&lt;')

    data_str = data_str.replace("'", '&apos;')
    data_str = data_str.replace('"', '&quot;')
    
    # --- Unprintable characters ---
    data_str = data_str.replace('\n', '&#10;')
    data_str = data_str.replace('\r', '&#13;')
    data_str = data_str.replace('\t', '&#9;')

    return data_str

def XML_text(tag_name, tag_text):
    tag_text = text_escape_XML(tag_text)
    line = '  <{0}>{1}</{2}>\n'.format(tag_name, tag_text, tag_name)

    return line

def text_str_2_Uni(str):
    unicode_str = str.decode('ascii', errors = 'replace')
    # print(type(str))
    # print(type(unicode_str))

    return unicode_str

# --- Main ----------------------------------------------------------------------------------------
curr_dir   = os.getcwd()
source_dir = curr_dir + '/data_gamedb_info/'
dest_dir   = curr_dir + '/input_xml/'
print('Current directory is     "{0}"'.format(curr_dir))
print('Source directory is      "{0}"'.format(source_dir))
print('Destination directory is "{0}"'.format(dest_dir))

# --- Traverse list of CVS files ---
# file_list = glob.glob(source_dir + '*.csv')
for files_tuple in file_list:
    csv_filename = os.path.join(source_dir, files_tuple[0] + '.csv')
    xml_filename = os.path.join(dest_dir, files_tuple[1] + '.xml')
    print('Processing file "{0}"'.format(csv_filename))
    print('           into "{0}"'.format(xml_filename))
    # sys.exit(0)

    # >> Read CVS file
    with open(csv_filename, 'r') as content_file:
        cvs_text_list = content_file.readlines()

    # >> Create XML data
    str_list = []
    str_list.append('<?xml version="1.0" encoding="utf-8" standalone="yes"?>\n')
    str_list.append('<menu>\n')
    str_list.append('<header>\n')
    str_list.append(XML_text('listname', files_tuple[1]))
    str_list.append('  <lastlistupdate></lastlistupdate>\n')
    str_list.append('  <listversion>test</listversion>\n')
    str_list.append('  <exporterversion></exporterversion>\n')
    str_list.append('</header>\n')

    # >> Write game info
    for cvs_line in cvs_text_list:
        # --- 9 data fields ---
        m = re.search('^([^>]*)>([^>]*)>([^>]*)>([^>]*)>([^>]*)>([^>]*)>([^>]*)>([^>]*)>([^>]*)>([^>]*)', cvs_line.strip())
        if m:
            # print('Adding game "{0}"'.format(text_str_2_Uni(m.group(1))))
            temp_str = text_str_2_Uni(m.group(1))
            str_list.append('<game name="{0}">\n'.format(text_escape_XML(temp_str)))
            str_list.append(XML_text('description',  text_str_2_Uni(m.group(2))))
            str_list.append(XML_text('year',         text_str_2_Uni(m.group(3))))
            str_list.append(XML_text('rating',       text_str_2_Uni(m.group(4))))
            str_list.append(XML_text('manufacturer', text_str_2_Uni(m.group(5))))
            str_list.append(XML_text('dev',          text_str_2_Uni(m.group(6))))
            str_list.append(XML_text('genre',        text_str_2_Uni(m.group(7))))
            str_list.append(XML_text('score',        text_str_2_Uni(m.group(8))))
            str_list.append(XML_text('player',       text_str_2_Uni(m.group(9))))
            str_list.append(XML_text('story',        text_str_2_Uni(m.group(10))))
            str_list.append(XML_text('enabled', 'Yes'))
            str_list.append(XML_text('crc', ''))
            str_list.append(XML_text('cloneof', ''))
            str_list.append('</game>\n')
        else:
            # --- 7 data fields ---
            m = re.search('^([^>]*)>([^>]*)>([^>]*)>([^>]*)>([^>]*)>([^>]*)>([^>]*)', cvs_line.strip())
            if m:
                temp_str = text_str_2_Uni(m.group(1))
                str_list.append('<game name="{0}">\n'.format(text_escape_XML(temp_str)))
                str_list.append(XML_text('description',  text_str_2_Uni(m.group(2))))
                str_list.append(XML_text('year',         text_str_2_Uni(m.group(3))))
                str_list.append(XML_text('rating',       text_str_2_Uni(m.group(4))))
                str_list.append(XML_text('manufacturer', text_str_2_Uni(m.group(5))))
                str_list.append(XML_text('dev',          text_str_2_Uni(m.group(6))))
                str_list.append(XML_text('genre',        text_str_2_Uni(m.group(7))))
                str_list.append(XML_text('score', ''))
                str_list.append(XML_text('player', ''))
                str_list.append(XML_text('story', ''))
                str_list.append(XML_text('enabled', 'Yes'))
                str_list.append(XML_text('crc', ''))
                str_list.append(XML_text('cloneof', ''))
                str_list.append('</game>\n')
            else:
                print('Error parsing CSV line')
                print('"{0}"'.format(cvs_line.strip()))
                sys.exit(0)
    str_list.append('</menu>\n')

    # >> Write XML file
    full_string = ''.join(str_list).encode('utf-8')
    file_obj = open(xml_filename, 'w')
    file_obj.write(full_string)
    file_obj.close()
print('*** Finished ***')
