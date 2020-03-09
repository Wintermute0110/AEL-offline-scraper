#!/usr/bin/python -B
# -*- coding: utf-8 -*-

# Updates the JSON index file for the Offline Scraper.
# Place the output file in AEL_DIR/data/GameDB_info.json

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

# --- Python standard library ---
from __future__ import unicode_literals
import os
import sys

# --- AEL modules ---
if __name__ == "__main__" and __package__ is None:
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'AEL'))
    print('Adding to sys.path {}'.format(path))
    sys.path.append(path)
from resources.utils import *
from resources.disk_IO import *
from resources.rom_audit import *
from resources.platforms import *

# --- Constants -----------------------------------------------------------------------------------
GAMEDB_XML_DIR = FileName('./output_AOS_xml_v1/')
GAMEDB_JSON_BASE_NOEXT = 'AOS_GameDB_info'

# --- main() --------------------------------------------------------------------------------------
set_log_level(LOG_DEBUG)
gamedb_info_dic = {}
for platform in AEL_platform_list:
    if platform == PLATFORM_UNKNOWN_LONG: continue
    # print('Processing platform "{}"'.format(platform))
    pobj = AEL_platforms[platform_long_to_index_dic[platform]]

    # Open XML file and count ROMs
    xml_file = GAMEDB_XML_DIR.pjoin(platform + '.xml').getPath()
    # print('Loading XML "{}"'.format(xml_file))
    games = audit_load_OfflineScraper_XML(xml_file)

    # Count ROMs and add to dictionary
    platform_info = {
        'numROMs' : 0,
        'aliasof' : None,
    }
    platform_info['numROMs'] = len(games)
    platform_info['aliasof'] = pobj.aliasof
    # print('numROMs = {}'.format(platform_info['numROMs']))
    gamedb_info_dic[platform] = platform_info
# print('Saving JSON index file...')
fs_write_JSON_file(FileName('./'), GAMEDB_JSON_BASE_NOEXT, gamedb_info_dic)
sys.exit(0)
