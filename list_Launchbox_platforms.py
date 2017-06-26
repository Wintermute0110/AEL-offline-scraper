#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2017 Wintermute0110 <wintermute0110@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# --- Python standard library ---
from __future__ import unicode_literals
import copy

# --- Import AEL modules ---
from AEL.resources.utils import *
from AEL.resources.rom_audit import *

# --- Functions -----------------------------------------------------------------------------------
def count_games(platform, games_dic):
    num_games = 0
    for game_key in games_dic:
        if games_dic[game_key]['Platform'] == platform:
            num_games += 1

    return num_games

# --- Main ----------------------------------------------------------------------------------------
set_log_level(LOG_DEBUG)
LB_metadata_FN = FileName('./data_launchbox/Metadata.xml')

# --- Load Launchbox main XML file ---
games_dic = {}
platforms_dic = {}
gameimages_dic = {}
audit_load_LB_metadata_XML(LB_metadata_FN, games_dic, platforms_dic, gameimages_dic)
# print("Games       {0}".format(len(games_dic)))
# print("Platforms   {0}".format(len(platforms_dic)))
# print("Game images {0}".format(len(gameimages_dic)))

# --- List platforms ---
for p_name in sorted(platforms_dic):
    # >> Count games in platform
    num_games = count_games(p_name, games_dic)
    print("Platform {0:>38} has {1:5d} games".format(p_name, num_games).encode('utf-8'))
sys.exit(0)
