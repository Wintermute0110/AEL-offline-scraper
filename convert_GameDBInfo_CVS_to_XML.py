#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Updated GameDBInfo XML (copies them to correct place).
#

# Copyright (c) 2016 Wintermute0110 <wintermute0110@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# --- INSTRUCTIONS --------------------------------------------------------------------------------
#
# -------------------------------------------------------------------------------------------------

# --- Python standard library ---
import sys
import os
import shutil
import glob

# --- Import AEL modules ---

# --- Main ----------------------------------------------------------------------------------------
curr_dir   = os.getcwd()
source_dir = curr_dir + '/data_gamedb_info/'
dest_dir   = curr_dir + '/data_gamedb_info/xml files/'
print('Current directory is     "{0}"'.format(curr_dir))
print('Source directory is      "{0}"'.format(source_dir))
print('Destination directory is "{0}"'.format(dest_dir))

# --- Traverse list of CVS files ---
file_list = glob.glob(source_dir + '*.csv')
for cvs_file_name in sorted(file_list):
    print('Processing file {0}'.format(cvs_file_name))
    
    # >> Read CVS file
    
    # >> Create XML data
    
    # >> Save XML output filename
