#!/usr/bin/python
# -*- coding: utf-8 -*-

# ?????

# Copyright (c) 2017-2020 Wintermute0110 <wintermute0110@gmail.com>
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
import copy

# --- Import AEL modules ---
from AEL.resources.utils import *
from AEL.resources.rom_audit import *

# --- Data structures -----------------------------------------------------------------------------
systems = {
    # --- SEGA ---
    'genesis' : {
        'platform' : 'Sega Genesis',
        'output'   : 'data_launchbox_xml/Sega Genesis.xml'
    }
}

# --- Main ----------------------------------------------------------------------------------------
set_log_level(LOG_DEBUG)
LB_metadata_FN = FileName('./data_launchbox/Metadata.xml')

# --- Load Launchbox main XML file ---
games_dic = {}
platforms_dic = {}
gameimages_dic = {}
audit_load_LB_metadata_XML(LB_metadata_FN, games_dic, platforms_dic, gameimages_dic)

# --- List platforms ---
for p_name in sorted(platforms_dic):
    print("Platform '{}'".format(p_name))

# --- Write per-platform ROM database ---
system = systems['genesis']
output_FN = FileName('./' + system['output'])
print('Writing {} output XML'.format(system['platform']))

platform_games_dic = {}
num_roms = 0
# num_images = 0
for game_key in games_dic:
    game = games_dic[game_key]
    if game['Platform'] == system['platform']:
        platform_games_dic[game_key] = copy.copy(game)
        num_roms += 1
        # for image_key in gameimages_dic:
        #     image = gameimages_dic[image_key]
        #     if game['Platform'] == image['DatabaseID']:
        #         platform_games_dic[game_key]['image'] = 
        #         platform_games_dic[game_key]['image'] = 
        #         num_images += 1
print('Found {} games'.format(num_roms))
# print('Found {} images'.format(num_images))

# --- Save Offline scraper XML ---
# Create XML data
str_list = []
str_list.append('<?xml version="1.0" encoding="utf-8" standalone="yes"?>\n')
str_list.append('<menu>\n')
str_list.append('  <header>\n')
str_list.append(XML_text('listname', output_FN.getBase_noext(), 4))
str_list.append('    <lastlistupdate></lastlistupdate>\n')
str_list.append('    <listversion></listversion>\n')
str_list.append('    <exporterversion></exporterversion>\n')
str_list.append('  </header>\n')
for rom_key in sorted(platform_games_dic):
    str_list.append('  <game name="{}">\n'.format(text_escape_XML(rom_key)))
    str_list.append(XML_text('Name',              text_str_2_Uni(platform_games_dic[rom_key]['Name']), 4))
    str_list.append(XML_text('ReleaseYear',       text_str_2_Uni(platform_games_dic[rom_key]['ReleaseYear']), 4))
    str_list.append(XML_text('Overview',          text_str_2_Uni(platform_games_dic[rom_key]['Overview']), 4))
    str_list.append(XML_text('MaxPlayers',        text_str_2_Uni(platform_games_dic[rom_key]['MaxPlayers']), 4))
    str_list.append(XML_text('Cooperative',       text_str_2_Uni(platform_games_dic[rom_key]['Cooperative']), 4))
    str_list.append(XML_text('VideoURL',          text_str_2_Uni(platform_games_dic[rom_key]['VideoURL']), 4))
    str_list.append(XML_text('DatabaseID',        text_str_2_Uni(platform_games_dic[rom_key]['DatabaseID']), 4))
    str_list.append(XML_text('CommunityRating',   text_str_2_Uni(platform_games_dic[rom_key]['CommunityRating']), 4))
    str_list.append(XML_text('Platform',          text_str_2_Uni(platform_games_dic[rom_key]['Platform']), 4))
    str_list.append(XML_text('Genres',            text_str_2_Uni(platform_games_dic[rom_key]['Genres']), 4))
    str_list.append(XML_text('Publisher',         text_str_2_Uni(platform_games_dic[rom_key]['Publisher']), 4))
    str_list.append(XML_text('Developer',         text_str_2_Uni(platform_games_dic[rom_key]['Developer']), 4))
    str_list.append(XML_text('ReleaseDate',       text_str_2_Uni(platform_games_dic[rom_key]['ReleaseDate']), 4))
    str_list.append(XML_text('ESRB',              text_str_2_Uni(platform_games_dic[rom_key]['ESRB']), 4))
    str_list.append(XML_text('WikipediaURL',      text_str_2_Uni(platform_games_dic[rom_key]['WikipediaURL']), 4))
    str_list.append(XML_text('DOS',               text_str_2_Uni(platform_games_dic[rom_key]['DOS']), 4))
    str_list.append(XML_text('StartupFile',       text_str_2_Uni(platform_games_dic[rom_key]['StartupFile']), 4))
    str_list.append(XML_text('StartupMD5',        text_str_2_Uni(platform_games_dic[rom_key]['StartupMD5']), 4))
    str_list.append(XML_text('SetupFile',         text_str_2_Uni(platform_games_dic[rom_key]['SetupFile']), 4))
    str_list.append(XML_text('SetupMD5',          text_str_2_Uni(platform_games_dic[rom_key]['SetupMD5']), 4))
    str_list.append(XML_text('StartupParameters', text_str_2_Uni(platform_games_dic[rom_key]['StartupParameters']), 4))
    str_list.append('  </game>\n')
str_list.append('</menu>\n')

# Write XML file
full_string = ''.join(str_list).encode('utf-8')
file_obj = open(output_FN.getPath(), 'w')
file_obj.write(full_string)
file_obj.close()
