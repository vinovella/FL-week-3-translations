#!/usr/bin/python3
#!/usr/bin/env python
import os, sys, codecs
from datetime import datetime
import check_translations_whitelists as whitelists

def open_report(lang, is_python3):
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = "./{}_{}.txt".format(timestamp, lang)
    if is_python3:
        output_file = open(filename, 'w', encoding='utf-8')
    else:
        output_file = codecs.open(filename, 'w', encoding='utf-8')
    return output_file

def find_missing_strings(f, fp, whitelist):
    lines = fp.readlines()
    j = 0
    untranslated_lines = []
    for i in range(len(lines)-1):
        if lines[i].startswith("    # "):
            if lines[i].startswith("    # game/"):
                continue
            if lines[i+1][4:].strip() == lines[i][6:].strip():
                untranslated_lines.append(i+2)
        elif lines[i].startswith("    old"):
            if lines[i+1][8:].strip() == lines[i][8:].strip():
                untranslated_lines.append(i+2)
    if len(untranslated_lines) > 0:
        output_file.write(u"File: {0}\n\n".format(f))
        for i in untranslated_lines:
            line = lines[i-1].strip()
            if is_whitelisted(line, whitelist):
                continue
            try:
                output_file.write(u"{0}: {1}\n".format(i, line))
            except:
                output_file.write(u"{0}: unparsed line\n".format(i))
        output_file.write(u"\n")

def get_whitelist(lang):
    whitelist = whitelists.whitelists[lang]
    if has_latin_characters[lang]:
        whitelist += whitelists.whitelists["latin"]
    whitelist = ['"{}"'.format(word) for word in whitelist]
    return set(whitelist) # This removes any duplicate

def is_whitelisted(line, whitelist):
    starting_index = line.find(' "') + 1
    return (line[starting_index:] in whitelist)

is_python3 = (sys.version_info > (3, 0))
folders = ("./deutsch", "./italian", "./russian", "./spanish", "./chinese", "./portuguese")
has_latin_characters = {"deutsch":True, "italian":True, "russian":False, "spanish":False, "chinese":False, "portuguese":False}

for folder in folders:
    lang = folder[2:]
    whitelist = get_whitelist(lang)
    output_file = open_report(lang, is_python3)
    output_file.write(u"{1} Language: {0} {1}\n\n".format(lang, "=" * 30))
    path = os.path.join(folder, "code/")
    files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(path) for f in filenames if os.path.splitext(f)[1] == '.rpy']
    for f in files:
        with (open(f, encoding='utf-8') if is_python3 else codecs.open(f, encoding='utf-8')) as fp:
            find_missing_strings(f, fp, whitelist)
    output_file.close()
