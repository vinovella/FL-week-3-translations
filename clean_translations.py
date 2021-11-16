#!/usr/bin/python3
#!/usr/bin/env python
import os, sys, codecs, shutil
from datetime import datetime

def get_pidgin_files_content():
    temp = {}
    for f in PIDGIN_FILES:
        with (open(PIDGIN_FOLDER  + f, encoding='utf-8') if is_python3 else codecs.open(PIDGIN_FOLDER + f, encoding='utf-8')) as fp:
            temp[f] = fp.readlines()
    return(temp)

def get_pidgin_lines_to_translate():
    temp                = {}
    dialogue_markers    = ["translate {} ".format(PIDGIN_LANG), "    old ", "translate {} strings:".format(PIDGIN_LANG)]
    for f in PIDGIN_FILES_CONTENT:
        lines       = PIDGIN_FILES_CONTENT[f]
        dictionary  = {"dialogue":{}, "menu":{}}
        for i in range(len(lines)-1):
            if lines[i].startswith(dialogue_markers[0]):
                if lines[i].startswith(dialogue_markers[2]):
                    continue
                dictionary["dialogue"][i] = lines[i].rstrip()
            elif lines[i].startswith(dialogue_markers[1]):
                dictionary["menu"    ][i] = lines[i].rstrip()
        temp[f] = dictionary
    return(temp)

def get_dictionary(folder):
    lang = folder[2:]
    dictionary = {"dialogue":{}, "menu":{}}
    dialogue_markers = ["translate {} ".format(lang), "    old ", "translate {} strings:".format(lang)]
    path = os.path.join(folder  + ".bck/code/")
    files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(path) for f in filenames if os.path.splitext(f)[1] == '.rpy']
    for f in files:
        with (open(f, encoding='utf-8') if is_python3 else codecs.open(f, encoding='utf-8')) as fp:
            lines = fp.readlines()
            for i in range(len(lines)-1):
                if lines[i].startswith(dialogue_markers[0]):
                    if lines[i].startswith(dialogue_markers[2]):
                        continue
                    dictionary["dialogue"][lines[i].rstrip()] = lines[i+3].rstrip()
                elif lines[i].startswith(dialogue_markers[1]):
                    dictionary["menu"    ][lines[i].rstrip()] = lines[i+1].rstrip()
    return dictionary

def move_translation(folder, dictionary):
    lang = folder[2:]
    dialogue_markers = ["translate {} ".format(lang), "    old ", "translate {} strings:".format(lang)]
    for f in PIDGIN_FILES:
        with (open(folder + f, 'w', encoding='utf-8') if is_python3 else codecs.open(folder + f, 'w', encoding='utf-8')) as fp:
            lines = [ l.replace(PIDGIN_LANG, lang) for l in PIDGIN_FILES_CONTENT[f] ]
            for i in range(len(lines)-1):
                stripped_line = lines[i].rstrip()
                if i in PIDGIN_LINES_TO_TRANSLATE[f]["dialogue"]:
                    if stripped_line in dictionary["dialogue"]:
                        lines[i+3] = dictionary["dialogue"][stripped_line] + "\n"
                elif i in PIDGIN_LINES_TO_TRANSLATE[f]["menu"]:
                    if stripped_line in dictionary["menu"]:
                        lines[i+1] = dictionary["menu"    ][stripped_line] + "\n"
            fp.writelines(lines)

is_python3 = (sys.version_info > (3, 0))
folders = ("./deutsch", "./italian", "./russian")

PIDGIN_FOLDER               = "./pidgin"
PIDGIN_LANG                 = PIDGIN_FOLDER[2:]
PIDGIN_DIRS                 = [(os.path.join(dp, d))[len(PIDGIN_FOLDER):] for dp, dn, filenames in os.walk(PIDGIN_FOLDER) for d in dn]
PIDGIN_FILES                = [(os.path.join(dp, f))[len(PIDGIN_FOLDER):] for dp, dn, filenames in os.walk(PIDGIN_FOLDER) for f in filenames if os.path.splitext(f)[1] == '.rpy']
PIDGIN_FILES_CONTENT        = get_pidgin_files_content()
PIDGIN_LINES_TO_TRANSLATE   = get_pidgin_lines_to_translate()

# Step 0:   open Ren'py SDK and generate the file translation for the 'pidgin' language

# Step 1:   check if the 'pidgin' folder exists
if not os.path.isdir(PIDGIN_FOLDER):
    sys.exit("Error: {} folder not found".format(PIDGIN_LANG))

# Step 2:   verify that no backup folder already exists
for i in folders:
    if os.path.isdir(i+".bck"):
        sys.exit("Error: the folder '{0}' already exists".format(i[2:] + ".bck"))

for folder in folders:

    # Step 3:   backup the folders with the previous translations and name them LANGUAGE.bck
    os.rename(folder, folder + ".bck")

    # Step 4:   for each language, duplicate recursively the 'pidgin' folder tree (directories only)
    os.mkdir(folder)
    for d in PIDGIN_DIRS:
        os.mkdir(folder + d)

    # Step 5:   build a dictionary with the previous translations (divide into dialogues and menu)
    dictionary = get_dictionary(folder)

    # Step 6:   move recursively the previous translations into the new, clean directory
    move_translation(folder, dictionary)

# Issue: some translations are generated on extended files. Duplicate the strings with a comment and you're done.