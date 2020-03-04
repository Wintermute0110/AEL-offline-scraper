## Advanced Emulator Launcher offline database and scraper

This repository includes the offline ROM metadata dabase of AEL Offline Scraper (AOS). It also
includes a set of tools for online scraper development.

## Generate Offline Scraper XML files (V1 old method)

The first version of the AOS uses XML files to store information. The CSV files from
the GameDBInfo database, stored in `data_gamedb_info_csv`, are converted to XML and stored 
in `data_gamedb_info_xml`. The MAME XML is generated from the output of `mame -listxml`
combined with `catver.ini`.

### Updating AOS XML files

 1. Use `v1_convert_GameDBInfo_CVS_to_AOS_XML.py` to convert the GameDBInfo CSV files into XML.
    This script read files from `./data_gamedb_info_csv/` and outputs files in 
    `./output_AOS_xml/`.

 2. Use `v1_convert_MAME_XML_to_AOS_XML.py` to convert `./data_mame/MAME_raw.xml` and 
    `./data_mame/catver.ini` into `./output_AOS_xml/MAME.xml`.

 3. Copy XML files from `./output_AOS_xml/` into `AEL_DIR/data-AOS/`.

 3. Use `AEL_DIR/dev-scrapers/v1_update_GameDBInfo_json_index.py` to update the AOS index file 
    so AEL can display the AOS contents. The index file is stored in
    `AEL_DIR/data/AOS_GameDB_info.json`. The index must be refreshed every time the XML are
    changed in AEL.

## Generate Offline Scraper XML files (V2 current method)

Same as V1 *but* use **JSON** instead of **XML**. This will increase the loading speed of the
AOS databases a lot.

## Generate Offline Scraper JSON files (V3 new method)

 * The second version of the AOS uses JSON to store information.

 * The database combines XML files with metadata from GameDBInfo (and maybe other
   sources like Tempest INI files) with No-Intro/Redump/Libretro DAT files.

 * The database includes parent/clone, region and language information.

 * The database includes CRC/MD5/SHA1 for ROM audit on selected platforms.

Version 2 of the AOS is still in develpment and some design decisions still to be made.

## Notes

### No-Intro/Redump ROMsets metadata report (Cartridge systems)

```
rom_name
  [DAT | ---]
  [Parent | Clone | -----]
  GameDBInfo | yyyy | genre | studio | nplayers | esrb | plot |
  HyperList  | ---- | ccccc | studio | nplayers | esrb | plot |
  Override   | ---- | ----- | studio | nplayers | esrb | plot |
  [status]   | yyyy | aaaaa | studio | nplayers | esrb | plot |

[status tag]
  [Own Override]
  [Own GameDBInfo]
  [Parent GameDBInfo]
  [Parent Override]
  [Clone GameDBInfo]
  [Clone Override]
  [No metadata]
```

 1. ROM names are sorted alphabetically first and Parent/Clone 1/Clone 2 second.

 2. ROMs not in the No-Intro DAT come from GameDBInfo, Tempest and HyperList 
    or just from GameDBInfo?

 3. Some No-Intro DATs have no PClone information. Example: Atari 2600.

 4. Clone metadata can be used for parent and other clones in the set.

 5. Output of this can be used to build AEL offline scraper DB.

 6. Use example: list_NoIntro_metadata <short_platform_name>

 7. Redump does not include Parent/Clone information.

### No DAT sets

 1. Platforms with no official DAT file: xxxxx.

 2. GameDBInfo will be the DAT used as reference.

### Levenshtein distance search algortihm

 1. Scrapers can be used to do this test: ./test_scraper <platform_short_name> <rom_name>
    Levenshtein distance will be tested on scraper search returned results

 2. A full ROM set from a directory can be used to test the Levenshtein distance in a similar way.

 3. Should ROM tags be removed before submitting search string to scraper??

    ```
    ROM name    "xxxxxxxxxxxxxxxxxxxxxxxxxx"
    Result 01   "xxxxxxxxxxxxxxxxxxxxxxxxxx"  score_1  raw_score_1
    Result 02   "xxxxxxxxxxxxxxxxxxxxxxxxxx"  score_2  raw_score_2
    Result 03   "xxxxxxxxxxxxxxxxxxxxxxxxxx"  score_3  raw_score_3
    ```

[Levenshtein distance in Wikipedia](https://en.wikipedia.org/wiki/Levenshtein_distance)
