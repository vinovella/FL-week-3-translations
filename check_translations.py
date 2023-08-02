import os
import sys
import codecs
from datetime import datetime


def open_report(lang, is_python3):
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = "./{}_{}.txt".format(timestamp, lang)
    if is_python3:
        output_file = open(filename, 'w', encoding='utf-8')
    else:
        output_file = codecs.open(filename, 'w', encoding='utf-8')
    return output_file


def find_missing_strings(f, fp, lang_folder, lang):
    lines = fp.readlines()
    untranslated_lines = []
    for i in range(len(lines) - 1):
        if lines[i].startswith("    # "):
            if lines[i].startswith("    # game/"):
                continue
            if lines[i + 1][4:].strip() == lines[i][6:].strip():
                untranslated_lines.append(i + 2)
        elif lines[i].startswith("    old"):
            if lines[i + 1][8:].strip() == lines[i][8:].strip():
                untranslated_lines.append(i + 2)
        elif lines[i].strip().endswith(' ""'):
            untranslated_lines.append(i + 1)
    if len(untranslated_lines) > 0:
        rel_path = os.path.relpath(f, lang_folder)
        output_file.write(u"File: {0}/{1}\n\n".format(lang, rel_path))
        for i in untranslated_lines:
            line = lines[i - 1].strip()
            try:
                output_file.write(u"{0}: {1}\n".format(i, line))
            except:
                output_file.write(u"{0}: unparsed line\n".format(i))
        output_file.write(u"\n")


is_python3 = (sys.version_info > (3, 0))
script_dir = os.path.dirname(os.path.abspath(__file__))
folders = os.listdir(script_dir)

for folder in folders:
    if not os.path.isdir(os.path.join(script_dir, folder)) or folder == "media" or folder == "none" or folder == ".git":
        continue
    output_file = open_report(folder, is_python3)
    output_file.write(u"{1} Language: {0} {1}\n\n".format(folder, "=" * 30))
    lang_folder = os.path.join(script_dir, folder)
    lang = folder.capitalize()
    for root, dirs, files in os.walk(lang_folder):
        for f in files:
            if os.path.splitext(f)[1] == ".rpy":
                file_path = os.path.join(root, f)
                with (open(file_path, encoding="utf-8") if is_python3 else codecs.open(file_path, encoding="utf-8")) as fp:
                    find_missing_strings(file_path, fp, lang_folder, lang)
    output_file.close()
