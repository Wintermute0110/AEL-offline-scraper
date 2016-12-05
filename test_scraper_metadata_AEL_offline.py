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
print('\n*** Offline scraper ***********************************************')
Offline = metadata_Offline()
Offline.set_addon_dir('/cygdrive/e/AEL-test/AEL-offline-scraper/AEL/')

# First time a platform is used XML database is loaded and cached for subsequent
# calls until object is destroyed or platform is changed.
# results = Offline.get_search('super mario world', 'super mario world', 'Nintendo SNES')
# results = Offline.get_search('castle', 'castle', 'Nintendo SNES')

# Test MAME offline scraper
results = Offline.get_search('dino', 'dino', 'MAME')
# results = Offline.get_search('aliens', 'aliens', 'MAME')
# results = Offline.get_search('spang', 'spang', 'MAME')
# results = Offline.get_search('toki', 'toki', 'MAME')
# results = Offline.get_search('asdfg', 'asdfg', 'MAME')

# --- Print list of fames found ---
print_games_search(results)
print_game_metadata(Offline, results)
