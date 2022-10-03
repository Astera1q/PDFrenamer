# PDFrenamer
Use bash commands to rename downloaded papers into designated forms.

Imported modules:


## To send request to CrossRef for Bibtex from extracted DOI 

import urllib.request

## To read PDF and find DOI of published paper

import pdfplumber
from unicodedata import normalize
import re

## Bash commands for rename and organize PDF files

import sys
import os

## Parse bibtex for renaming purpose
import bibtexparser
