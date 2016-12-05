#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Test AEL metadata scraper
#

# --- Python standard library ---
from __future__ import unicode_literals

# --- AEL modules ---
from AEL.resources.scrap import *
from AEL.resources.utils import *

# --- Print list of all scrapers currently in AEL ---
set_log_level(LOG_DEBUG) # >> LOG_INFO, LOG_VERB, LOG_DEBUG
print_scraper_list(scrapers_metadata)

# --- main ----------------------------------------------------------------------------------------
print('*** Online GameFAQs *********************************************')
GameFAQs = metadata_GameFAQs()

# results = GameFAQs.get_search('Castlevania', '', 'Nintendo SNES')
# results = GameFAQs.get_search('Metroid', '', 'Nintendo SNES')
# results = GameFAQs.get_search('Zelda', '', 'Nintendo SNES')
results = GameFAQs.get_search('Super Mario World', '', 'Nintendo SNES')
# results = GameFAQs.get_search('super street fighter', '', 'Nintendo SNES')

# --- Print list of fames found ---
print_games_search(results)
print_game_metadata(GameFAQs, results)
