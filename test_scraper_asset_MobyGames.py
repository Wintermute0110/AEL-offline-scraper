#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Test AEL asset scraper
#

# --- Python standard library ---
from __future__ import unicode_literals

# --- AEL modules ---
from AEL.resources.scrap import *
from AEL.resources.utils import *

# --- main ----------------------------------------------------------------------------------------
set_log_level(LOG_DEBUG) # >> LOG_INFO, LOG_VERB, LOG_DEBUG
print_scraper_list(scrapers_asset)

print('*** MobyGames search ***********************************************************************')
MobyGames = asset_MobyGames()

# results = MobyGames.get_search('Castlevania', '', 'Nintendo SNES')
results = MobyGames.get_search('Metroid', '', 'Nintendo SNES')
# results = MobyGames.get_search('Zelda', '', 'Nintendo SNES')
# results = MobyGames.get_search('Super Mario World', '', 'Nintendo SNES')
# results = MobyGames.get_search('super street fighter', '', 'Nintendo SNES')
# results = MobyGames.get_search('chakan', '', 'Mega Drive')

# --- Print list of fames found ---
print_games_search(results)

# --- Print list of assets found ---
print('*** MobyGames found images *****************************************************************')
# print_game_image_list(MobyGames, results, ASSET_TITLE)
print_game_image_list(MobyGames, results, ASSET_SNAP)
# print_game_image_list(MobyGames, results, ASSET_FANART)
# print_game_image_list(MobyGames, results, ASSET_BANNER)
# print_game_image_list(MobyGames, results, ASSET_CLEARLOGO)
# print_game_image_list(MobyGames, results, ASSET_BOXFRONT)
# print_game_image_list(MobyGames, results, ASSET_BOXBACK)
# print_game_image_list(MobyGames, results, ASSET_CARTRIDGE)
# print_game_image_list(MobyGames, results, ASSET_FLYER)
# print_game_image_list(MobyGames, results, ASSET_MAP)
# print_game_image_list(MobyGames, results, ASSET_MANUAL)
# print_game_image_list(MobyGames, results, ASSET_TRAILER)
