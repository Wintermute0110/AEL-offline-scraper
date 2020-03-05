#!/usr/bin/python
# -*- coding: utf-8 -*-

# Traverses NoIntro Parent/Clone DATs and makes a histogram or region, language and other tags.
# This is used for research.

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

# This is compiled manually from the histogram.
# There are some wrong names ROMs in the No-Intro DATs and this set is used to catch those
# ROMs.
nointro_region_set = {
    "Japan",
    "Europe",
    "USA",
    "Germany",
    "World",
    "France",
    "Brazil",
    "Korea",
    "Taiwan",
    "Asia",
    "Spain",
    "Italy",
    "Australia",
    "China",
    "Netherlands",
    "Sweden",
    "Unknown",
    "Denmark",
    "New Zealand",
    "Canada",
    "United Kingdom",
    "Norway",
    "Hong Kong",
    "Finland",
    "Russia",
    "Mexico",
    "Greece",
    "Argentina",
    "Portugal",
    "Hungary",
}

# Some badly formatted ROMs have a first tag like in this set. Remove those tags.
# Ordered as they appear when reading the NoIntro DATs.
region_exceptions_set = {
    "(Goukaku Tokkou 700)",
    "(Original Game Sound Edition)",
    "(Premium Edition)",
    "(Summer of My Life)",
    "(GBA Mode)",
    "(Tokyo Daigaku)",
    "(Koku San Ri Sha)",
    "(Demo)",
    "(Flight Simulator)",
    "(Akogare Girls Collection)",
    "(SDHC)",
    "(Soccer)",
    "(Nickelodeon Movies)",
    "(Racing)",
    "(Nicktoons)",
    "(Jou)",
    "(Bulletproof)",
    "(NES Test)",
    "(Ge)",
    "(Yi)",
    "(4-28)",
    "(2-1)",
    "(8-13)",
    "(4-7)",
    "(2-1)",
    "(2-8)",
    "(Mine Level)",
    "(Palace Level)",
    "(Woods Level)",
    "(A)",
    "(B)",
    "(C)",
    "(D)",
    "(E)",
    "(F)",
    "(Gensokigou Master)",
    "(Kari)",
}

# This language list is compiled manually from the histogram.
# Top languages are more used.
nointro_language_set = {
    "En",
    "Fr",
    "Es",
    "De",
    "It",
    "Nl",
    "Sv",
    "Da",
    "Pt",
    "Ja",
    "No",
    "Fi",
    "Ru",
    "Ko",
    "Tr",
    "Zh",
    "Pl",
    "El",
    "Cs",
    "Ca",
    "Hu",
    "Hr",
    "Ar",
    "Gd",
}

# --- Functions -----------------------------------------------------------------------------
# "[BIOS] LaserActive (Japan) (v1.02)"
#
# * [BIOS] is optional.
# * Fist tag is Region and it is mandatory.
#
# Returns a tuple (
#     ['region', 'region'],
#     ['language', 'language'],
#     ['(tag)', '(tag)']
# )
def extract_NoIntro_tags(basename):
    # Extract raw tags.
    # Maybe this can be improved because tags must be at the end!
    # "[BIOS] chars chars chars (tag) (tag) (tag)"
    prop_list = re.findall(" (\([^\(]*\))", basename)
    if len(prop_list) > 1:
        # Remove exception tags when the first tag is not really the ROM Region.
        # Remove up to two tags.
        if prop_list[0] in region_exceptions_set: prop_list.pop(0)
        if prop_list[0] in region_exceptions_set: prop_list.pop(0)
        region = prop_list[0]
        tag_list = prop_list[1:]
    else:
        region = prop_list[0]
        tag_list = []

    # Generate region list.
    if not region.startswith('('): raise TypeError
    if not region.endswith(')'): raise TypeError
    region = region[1:-1]
    if region.find(',') > -1:
        region_list = region.split(',')
        region_list = [i.strip() for i in region_list]
    else:
        region_list = [region]

    # Check for languages
    language_list = []
    new_tag_list = []
    for tag in tag_list:
        striped_tag = tag[1:-1]
        if striped_tag.find(',') > -1:
            l_list = striped_tag.split(',')
            l_list = [i.strip() for i in l_list]
            # Some languages are specified as "Es+En", etc. Also, take those into account.
            # Convert "Es+En" into 'Es', 'En' and create a unique list of languages per ROM.
            unique_l_list = []
            all_subtags_language = True
            for l in l_list:
                if len(l) != 2 and len(l) != 5:
                    all_subtags_language = False
                elif len(l) == 5 and l[2] != '+':
                    all_subtags_language = False
                if len(l) == 5 and l[2] == '+':
                    lang1 = l[0:2]
                    if lang1 not in unique_l_list: unique_l_list.append(lang1)
                    lang2 = l[3:5]
                    if lang2 not in unique_l_list: unique_l_list.append(lang2)
                    # print('lang1 {}  lang2 {}'.format(lang1, lang2))
                else:
                    if l not in unique_l_list: unique_l_list.append(l)
            if all_subtags_language:
                language_list.extend(unique_l_list)
                continue
        # Tag is a non-language tag.
        new_tag_list.append(tag)
    tag_list = new_tag_list

    # Remove single language tags in nointro_language_set.
    new_tag_list = []
    for tag in tag_list:
        striped_tag = tag[1:-1]
        if striped_tag in nointro_language_set:
            if striped_tag not in language_list:
                language_list.append(striped_tag)
            continue
        # Tag is a non-language tag.
        new_tag_list.append(tag)
    tag_list = new_tag_list

    return (region_list, language_list, tag_list)

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
        region_list, language_list, tag_list = extract_NoIntro_tags(rom_basename)
        # print('\nROM {}'.format(rom_basename))
        # print('region {} | tag_list {}'.format(region, tag_list))

        # Try to catch wrong/bad No-Intro names
        for region in region_list:
            if region not in nointro_region_set:
                print('ROM "{}", bad region tag\n'.format(rom_basename))

        for region in region_list:
            if region in region_histo_dic:
                region_histo_dic[region] += 1
            else:
                region_histo_dic[region] = 1

        for lang in language_list:
            if lang in language_histo_dic:
                language_histo_dic[lang] += 1
            else:
                language_histo_dic[lang] = 1

        for tag in tag_list:
            if tag in other_dic:
                other_dic[tag] += 1
            else:
                other_dic[tag] = 1
    # break

# Check that the region histogram obtained is the same as the region set we already have.
print('Verifing nointro_region_set...')
for key in region_histo_dic:
    if key not in nointro_region_set:
        print('region_histo_dic key not in nointro_region_set')
for key in nointro_region_set:
    if key not in region_histo_dic:
        print('nointro_region_set key not in region_histo_dic')

# Check that the languages obtained are the same to those we already have.

print('\n[Region histogram]')
sorted_region_histo_dic = sorted(region_histo_dic.iteritems(), key = lambda item: item[1], reverse = True)
for key in sorted_region_histo_dic:
    print('{:6d}  "{}"'.format(key[1], key[0]))

print('\n[Language histogram]')
sorted_language_histo_dic = sorted(language_histo_dic.iteritems(), key = lambda item: item[1], reverse = True)
for key in sorted_language_histo_dic:
    print('{:6d}  "{}"'.format(key[1], key[0]))

print('\n[Other tag histogram]')
sorted_other_dic = sorted(other_dic.iteritems(), key = lambda item: item[1], reverse = True)
for key in sorted_other_dic:
    # Do not print dates.
    if re.search('\(\d\d\d\d-\d\d-\d\d\)', key[0]): continue
    # Do not print version numbers
    if re.search('^\(v\d', key[0]): continue
    # Do not print compilations (very frequent tag)
    if re.search('^\(Compilation', key[0]): continue
    if re.search('^\(Coverdisk', key[0]): continue
    print('{:6d}'.format(key[1]) + '  ' + key[0])
