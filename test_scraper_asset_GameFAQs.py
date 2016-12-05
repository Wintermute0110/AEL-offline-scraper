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

print('*** GameFAQs search ************************************************************************')
GameFAQs = asset_GameFAQs()

results = GameFAQs.get_search('Castlevania', '', 'Nintendo SNES')
# results = GameFAQs.get_search('Metroid', '', 'Nintendo SNES')

# --- Print list of fames found ---
print_games_search(results)

# --- Print list of assets found ---
print('*** GameFAQs found images *******************************************************************')
print_game_image_list(GameFAQs, results, ASSET_TITLE)
print_game_image_list(GameFAQs, results, ASSET_SNAP)
