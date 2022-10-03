import urllib.request
import pdfplumber
import re
import sys
import os
from unicodedata import normalize
import bibtexparser

PDF_name = input("Enter pdf name:\n")
folder = '/Users/lisiqi/Downloads/literature/'
full_path = folder + PDF_name + ".pdf"

#Extract text of PDF first page
with pdfplumber.open(full_path) as pdf:
    first_page = pdf.pages[0]
    PDFtext = first_page.extract_text()
    #print(PDFtext)

#Find doi in extracted text -- There are two different formats: 'doi:' or 'dor.org/'
if bool(re.search('doi:',PDFtext,re.IGNORECASE)):
    find_doi = re.search('doi:',PDFtext,re.IGNORECASE)
    (start,_) = find_doi.span()
    rawinput = PDFtext[start+4:start+40].split()
    PDFdoi= rawinput[0]
else:
    if PDFtext.find('doi.org/') > 0:
        start = PDFtext.find('doi.org/')
        rawinput = PDFtext[start+8:start+40].split()
        PDFdoi = rawinput[0]
    else:
        if bool(re.search('doi',PDFtext,re.IGNORECASE)):
            find_doi = re.search('doi',PDFtext,re.IGNORECASE)
            (start,_) = find_doi.span()
            rawinput = PDFtext[start+3:start+40].split()
            print(rawinput[0])
            if "/" in rawinput[0]:
                PDFdoi= rawinput[0]
            else:
                print("cannot find doi")
                sys.exit()
        else:
            print ('cannot find doi of' + full_path)
            sys.exit()

#Normalize all characters to readable characters
newPDFdoi = normalize('NFKD',PDFdoi)

#Request bibtex info from Crossref api
opener = urllib.request.build_opener()
opener.addheaders = [('Accept','text/bibliography; style=bibtex')]
r = opener.open('http://dx.doi.org/'+newPDFdoi)
bibtex = r.read().decode()

#Parse bibtex into dictionary
bib_database = bibtexparser.loads(bibtex)
bd = bib_database.entries_dict

#Extract info from bibtex dictionary
for key in bd.keys():
    title = bd[key]['title'].split(':',1)[0].replace('/','')
    year = bd[key]['year']
    author = bd[key]['author'].split(",",1)[0]
    journal = bd[key]['journal'].replace(' ','')
# print(year)
# print(title)
# print(author)
# print(journal)

os.rename(full_path,folder + year+'_'+title+'_'+journal+'_'+author+'.pdf')

print("DONE!")




