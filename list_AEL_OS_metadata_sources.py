#!/usr/bin/python
# -*- coding: utf-8 -*-

# List metadata from NoIntro DATs and several other sources.
# It prints a table for every ROM, telling where the ROM is found and the metadata.
#
# This file is similar to update_AEL_OS_XML_metadata.py but does not output the final XML.
# This file includes more metadata sources than update_AEL_OS_XML_metadata.py
# This is an experimental script which is currently not working.

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
import os
import sys

# --- Import AEL modules ---
if __name__ == "__main__" and __package__ is None:
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'AEL'))
    print('Adding to sys.path {}'.format(path))
    sys.path.append(path)
from resources.utils import *
from resources.rom_audit import *

# --- Data structures -----------------------------------------------------------------------------
systems = {
    # --- Nintendo ---
    'snes' : {
        'nointro'   : 'data_nointro/Nintendo - Super Nintendo Entertainment System Parent-Clone (20170507-052522).dat',
        'gamedb'    : 'data_gamedb_info_xml/Sega 32X.xml',
        'tempest'   : '',
        'hyperlist' : '',
        'output'    : 'output_xml/Sega 32X.xml'
    },

    # --- SEGA ---
    '32x' : {
        'nointro'   : 'data_nointro_pclone/Sega - 32X Parent-Clone (20161022-095033).dat',
        'gamedb'    : 'data_gamedb_info_xml/Sega 32X.xml',
        'tempest'   : '',
        'hyperlist' : '',
        'output'    : 'output_xml/Sega 32X.xml'
    },
    'genesis' : {
        'nointro'   : 'data_nointro_pclone/Sega - Mega Drive - Genesis Parent-Clone (20170318-044444).dat',
        'gamedb'    : 'data_gamedb_info_xml/Sega MegaDrive.xml',
        'tempest'   : 'data_tempest_ini/Genesis.ini',
        'hyperlist' : 'data_hyperlist/Sega Genesis.xml',
        'output'    : 'output_xml/Sega MegaDrive.xml'
    },

    # --- SONY ---
    'psx' : {
        'nointro'   : 'data_redump/Sony - PlayStation (20170306 02-03-12).dat',
        'gamedb'    : 'data_gamedb_info_xml/Sony PlayStation.xml',
        'tempest'   : 'data_tempest_ini/PlayStation.ini',
        'hyperlist' : '',
        'output'    : 'output_xml/Sony PlayStation.xml'
    }
}

def process_system(system):
    nointro_FN   = FileName('./' + system['nointro'])
    gamedb_FN    = FileName('./' + system['gamedb'])
    tempest_FN   = FileName('./' + system['tempest'])
    hyperlist_FN = FileName('./' + system['hyperlist'])
    output_FN    = FileName('./' + system['output'])

    # --- Load No-Intro PClone DAT file ---
    nointro_dic = audit_load_NoIntro_XML_file(nointro_FN)

    # --- Load GameDBInfo XML ---
    gamedb_dic = audit_load_GameDB_XML(gamedb_FN)

    # --- Load Tempest INI ---
    # tempest_dic = audit_load_Tempest_INI(tempest_FN)

    # --- Load HyperList XML ---
    hyperlist_dic = audit_load_HyperList_XML(hyperlist_FN)
    # return

    # --- Load Overrides XML ---
    # override_dic = audit_load_HyperList_XML(hyperlist_FN)
    override_dic = {}

    # --- Make PClone dictionary ---
    # pclone_dic = { 'Parent_name' : ['Clone 1', 'Clone 2', ...], ... }
    # parents_dic = { 'clone_name' : 'parent_name', ...}
    pclone_dic = audit_make_NoIntro_PClone_dic(nointro_dic)
    parents_dic = audit_make_NoIntro_Parents_dic(nointro_dic)

    # --- Make main ROM dictionary ---
    # >> Allows to know if ROM comes from No-Intro or GameDBInfo quickly.
    # >> main_rom_dic = { 'ROMname' : 'Parent | Clone | Extra', ... }
    # >> Status Parent -> ROM is in the NoIntro file and is a parent
    # >> Status Clone  -> ROM is in the NoIntro file and is a clone
    # >> Status Extra  -> ROM is not in the NoIntro file (is in GameDBInfo)

    # --- Make main ROM list ---
    # >> This list is sorted and is how ROMs will be listed and located in the out XML file.
    # >> main_rom_set = {'rom_name_1', 'rom_name_2', ... }
    main_rom_set = set()

    # Add ROMs from No-Intro DAT and other sources.
    for rom_name in nointro_dic:   main_rom_set.add(rom_name)
    for rom_name in gamedb_dic:    main_rom_set.add(rom_name)
    for rom_name in hyperlist_dic: main_rom_set.add(rom_name)

    # --- Traverse main_rom_list and print all metadata ---
    metadata_dic = {}
    NAME_LENGTH = 64
    CLONE_LENGTH = 6
    DB_LENGTH = 31

    EXISTS_LENGTH    = 5
    ISCLONE_LENGTH   = 5
    YEAR_LENGTH      = 4
    GENRE_LENGTH     = 20
    PUBLISHER_LENGTH = 29
    NPLAYERS_LENGTH  = 11
    ESRB_LENGTH      = 22
    PLOT_LENGTH      = 40
    line_1 = "{0} | {1} | {2} | {3} | {4} | {5} | {6} |"
    line_2 = "{0} | {1} | {2} | {3} | {4} | {5} | {6} |"
    line_3 = "{0} | {1} | {2} | {3} | {4} | {5} | {6} |"
    line_4 = "{0} | {1} | {2} | {3} | {4} | {5} | {6} |"
    for rom_key in sorted(main_rom_set):
        if re.findall(r'^\[BIOS\]', rom_key): continue

        rom_name = text_limit_string(rom_key, NAME_LENGTH)
        dat_str = 'Yes' if rom_key in nointro_dic else 'No'
        if rom_name in nointro_dic:
            clone_str = 'Clone' if nointro_dic[rom_key]['cloneof'] else 'Parent'
        else:
            clone_str = '-----'
        nointro_str = 'NoIntro' if rom_key in nointro_dic else ''
        gamedb_str  = 'GameDBInfo' if rom_key in gamedb_dic else ''
        hl_str      = 'HyperList' if rom_key in hyperlist_dic else ''

        gamedb_year_srt     = gamedb_dic[rom_key]['year'] if rom_key in gamedb_dic else ''
        gamedb_genre_srt    = gamedb_dic[rom_key]['genre'] if rom_key in gamedb_dic else ''
        gamedb_studio_srt   = gamedb_dic[rom_key]['manufacturer'] if rom_key in gamedb_dic else ''
        gamedb_nplayers_srt = gamedb_dic[rom_key]['player'] if rom_key in gamedb_dic else ''
        gamedb_rating_srt   = gamedb_dic[rom_key]['rating'] if rom_key in gamedb_dic else ''
        gamedb_plot_srt     = gamedb_dic[rom_key]['story'] if rom_key in gamedb_dic else ''

        gamedb_genre_srt    = text_limit_string(gamedb_genre_srt, GENRE_LENGTH)
        gamedb_studio_srt   = text_limit_string(gamedb_studio_srt, PUBLISHER_LENGTH)
        gamedb_nplayers_srt = text_limit_string(gamedb_nplayers_srt, NPLAYERS_LENGTH)
        gamedb_rating_srt   = text_limit_string(gamedb_rating_srt, ESRB_LENGTH)
        gamedb_plot_srt     = text_limit_string(gamedb_plot_srt, PLOT_LENGTH)

        hl_year_srt     = hyperlist_dic[rom_key]['year'] if rom_key in hyperlist_dic else ''
        hl_genre_srt    = hyperlist_dic[rom_key]['genre'] if rom_key in hyperlist_dic else ''
        hl_studio_srt   = hyperlist_dic[rom_key]['manufacturer'] if rom_key in hyperlist_dic else ''
        hl_nplayers_srt = ''
        hl_rating_srt   = hyperlist_dic[rom_key]['rating'] if rom_key in hyperlist_dic else ''
        hl_plot_srt     = ''

        print('ROM "{}"'.format(rom_key))
        print(line_1.format(
            nointro_str.ljust(DB_LENGTH), 
            dat_str.ljust(3),
            clone_str.ljust(CLONE_LENGTH),
            '', '', '', '' ))
        print(line_2.format(
            gamedb_str.ljust(DB_LENGTH),
            gamedb_year_srt.ljust(YEAR_LENGTH), gamedb_genre_srt.ljust(GENRE_LENGTH),
            gamedb_studio_srt.ljust(PUBLISHER_LENGTH), gamedb_nplayers_srt.ljust(NPLAYERS_LENGTH),
            gamedb_rating_srt.ljust(ESRB_LENGTH), gamedb_plot_srt.ljust(PLOT_LENGTH) ))
        print(line_3.format(hl_str.ljust(DB_LENGTH), 
            hl_year_srt.ljust(YEAR_LENGTH), hl_genre_srt.ljust(GENRE_LENGTH),
            hl_studio_srt.ljust(PUBLISHER_LENGTH), hl_nplayers_srt.ljust(NPLAYERS_LENGTH),
            hl_rating_srt.ljust(ESRB_LENGTH), hl_plot_srt.ljust(PLOT_LENGTH) ))
        print('')

    # --- Statistics ---
    print('***** Statistics *****')
    print('NoIntro roms    {:,d}'.format(len(nointro_dic)))
    print('GameDB roms     {:,d}'.format(len(gamedb_dic)))
    # print('Tempest roms    {:,d}'.format(len(tempest_dic)))
    print('HyperList roms  {:,d}'.format(len(hyperlist_dic)))

# --- Main ----------------------------------------------------------------------------------------
set_log_level(LOG_DEBUG)
# for system_name in systems: process_system(systems[system_name])
# process_system(systems['32x'])
process_system(systems['genesis'])
