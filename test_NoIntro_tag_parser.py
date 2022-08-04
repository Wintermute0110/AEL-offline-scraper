#!/usr/bin/python
# -*- coding: utf-8 -*-

# Traverses NoIntro Parent/Clone DATs and makes a histogram or region, language and other tags.
# Tests the No-Intro filename parser.

# Copyright (c) 2020 Wintermute0110 <wintermute0110@gmail.com>
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
import re
import sys

# --- Import AEL modules ---
if __name__ == "__main__" and __package__ is None:
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'AEL'))
    print('Adding to sys.path {}'.format(path))
    sys.path.append(path)
from resources.platforms import *
from resources.utils import *
from resources.rom_audit import *

# --- Data structures -----------------------------------------------------------------------------
region_histo_dic = {}
language_histo_dic = {}
other_dic = {}


# --- Functions -----------------------------------------------------------------------------
# Currently regular expressions are used to extract the tags at the end of the funcion.
# I think this can be improved by using a lexical analyser to decompose the name into
# tokens and then analyse the tokens. For example, a No-Intro name is composed of
# (region token tag is mandatory):
#
# 1) TOKEN_ROMNAME TOKEN_SPACE TOKEN_TAG (TOKEN_SPACE TOKEN_TAG)*
# 2) TOKEN_BIOS TOKEN_SPACE TOKEN_ROMNAME TOKEN_SPACE TOKEN_TAG (TOKEN_SPACE TOKEN_TAG)*
#
# Token BIOS is optional. With this aproach we can parse correctly the few games that include
# ( or ) characters in the ROM_name.
#
# Returns a dictionary {
#     tokens : [TOKEN_ID, TOKEN_ID, ...],
#     strings : [string, string, ...],
# }
#
# See https://www.pythonmembers.club/2018/05/01/building-a-lexer-in-python-tutorial/
# for ideas about making a lexical analizer. After the lexical analyzer decomposes
# the filename in tokens the parser determines if the tokens are a valid No-Intro filename.
#
TOKEN_ROMNAME = 100
TOKEN_SPACE   = 200
TOKEN_TAG     = 300
TOKEN_BIOS    = 400
TOKEN_ERROR   = 500
def parse_NoIntro_filename(basename):
    lexeme_name_list = []
    lexeme_list = []
    lexeme = ''
    for i, char in enumerate(basename):
        print('char {:3d} : {}'.format(i, char))
        if char == ' ':
            lexeme_list.append('<space>')
            lexeme = ''
            continue
        lexeme += char # adding a char each time
        # Check next character.
        if i+1 < len(basename):
            if basename[i+1] == ' ': # if next char == '('
                lexeme_list.append(lexeme)
                lexeme = ''
        else:
            # Last character of string
            lexeme_list.append(lexeme)
    print('Lexeme {}'.format(lexeme_list))

# --- Main -----------------------------------------------------------------------------
set_log_level(LOG_DEBUG)
NOINTRO_PATH_FN = FileName('./data_nointro_pclone/')
NOINTRO_DAT_list = NOINTRO_PATH_FN.scanFilesInPath('*.dat')
for pobj in AEL_platforms:
    # Skip no No-Intro platforms.
    if pobj.DAT != DAT_NOINTRO: continue
    fname = misc_look_for_NoIntro_DAT(pobj, NOINTRO_DAT_list)
    if fname:
        nointro_xml_FN = FileName(fname)
    else:
        print('No-Intro DAT cannot be auto detected (platform {})'.format(pobj.long_name))
        continue
    nointro_dic = audit_load_NoIntro_XML_file(nointro_xml_FN)

    # Create tags histogram.
    for rom_basename in nointro_dic:
        print('\nROM "{}"'.format(rom_basename))
        parser_dic  = parse_NoIntro_filename(rom_basename)
        break
    break
