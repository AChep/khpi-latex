
import os
import shutil
from time import sleep

from googlesearch import google

import docx2txt
import re

def process_docx(path):
    txt = docx2txt.process(path)
    txt = re.sub(r'\n{1,}', '\n', txt)  # remove empty lines
    txt = re.sub(r'\[.{1,}\]', '', txt)  # remove references
    # remove extra whitespaces
    txt = re.sub(r' {1,}', ' ', txt)  
    txt = re.sub(r' \.', '.', txt) # remove space before dot  
    txt = re.sub(r' ,', ',', txt) # remove space before comma  
    
    # Make a google search request for first few 
    # words of the first sentence.
    
    glink = 'unknown'
    gresults = google.search(' '.join(txt.split()[:5]), 1)
    if len(gresults) > 0 and gresults[0].link is not None:
        glink = gresults[0].link
    else:
        gresults = google.search(' '.join(txt.split()[:3]), 1)
        if len(gresults) > 0 and gresults[0].link is not None:
            glink = gresults[0].link

    if len(txt) < 20:
        print(path)
        print(txt)
    
    return glink, txt
    

shutil.rmtree('output', ignore_errors=True)
shutil.copytree('input', 'output')

corpus = dict()

# Traverse root directory, and list directories as 
# dirs and files as files.
for root, dirs, files in os.walk("output"):
    path = root.split(os.sep)
    for file in files:
        sleep(2)
        # Process only .docx files
        if file.endswith(".docx"):
            link, text = process_docx(root + os.sep + file)
            
            if link not in corpus:
                corpus[link] = list()
            corpus[link].append(text)

for i, link in enumerate(corpus):
    dir = 'output' + os.sep + str(i)
    if not os.path.exists(dir):
        os.makedirs(dir)

    with open(dir + os.sep + 'readme.txt', 'a') as out:
        out.write(link)
    
    for j, txt in enumerate(corpus[link]):
        with open(dir + os.sep + str(j) + '.txt', 'a') as out:
            out.write(txt)