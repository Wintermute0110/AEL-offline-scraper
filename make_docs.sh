#!/usr/bin/bash
pandoc NOTES.md -s -f markdown -t html -o NOTES.html
pandoc README.md -s -f markdown -t html -o README.html
