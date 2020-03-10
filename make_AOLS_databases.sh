#!/usr/bin/bash

# Canonial way to generate AEL AOLs databases for current version.

./v1_convert_GameDBInfo_CVS_to_AOS_XML.py
./v1_convert_MAME_XML_to_AOS_XML.py
./v1_update_GameDBInfo_json_index.py
