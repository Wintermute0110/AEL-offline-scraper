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

print('*** ArcadeDatabase search game *************************************************************')
ArcadeDB = asset_ArcadeDB()

results = ArcadeDB.get_search('dino', 'dino', 'MAME')
# results = ArcadeDB.get_search('aliens', 'aliens', 'MAME')
# results = ArcadeDB.get_search('spang', 'spang', 'MAME')
# results = ArcadeDB.get_search('toki', 'toki', 'MAME')

# --- Print list of games found ---
print_games_search(results)

# --- Print list of assets found ---
print('*** ArcadeDatabase found images *************************************************************')
print_game_image_list(ArcadeDB, results, ASSET_TITLE)
print_game_image_list(ArcadeDB, results, ASSET_SNAP)
print_game_image_list(ArcadeDB, results, ASSET_BANNER)
# print_game_image_list(ArcadeDB, results, ASSET_CLEARLOGO)
# print_game_image_list(ArcadeDB, results, ASSET_BOXFRONT)
# print_game_image_list(ArcadeDB, results, ASSET_BOXBACK)
# print_game_image_list(ArcadeDB, results, ASSET_CARTRIDGE)
# print_game_image_list(ArcadeDB, results, ASSET_FLYER)
# print_game_image_list(ArcadeDB, results, ASSET_MANUAL)
