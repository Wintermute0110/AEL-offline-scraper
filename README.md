## Advanced Emulator Launcher offline database and scraper ##

This repository includes the offline ROM metadata dabase of AEL's offline scraper.

It also includes a set of tools for online scraper development.

### No-Intro/Redump ROMsets metadata report (Cartridge systems) ###

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

### No DAT sets ###

 1. Platforms with no official DAT file: xxxxx.

 2. GameDBInfo will be the DAT used as reference.

## Levenshtein distance search algortihm ##

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
