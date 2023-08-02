import re
import os
import sys
import codecs
from datetime import datetime


def open_report(is_python3, report):
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = "./word_count_{}.txt".format(timestamp)
    if is_python3:
        output_file = open(filename, 'w', encoding='utf-8')
    else:
        output_file = codecs.open(filename, 'w', encoding='utf-8')
    output_file.write("Word Count Report - {}\n\n".format(timestamp))
    for lang, subfolders in report.items():
        output_file.write("Language: {}\n\n".format(lang))
        output_file.write("=" * 40 + "\n")
        for subfolder, files in subfolders.items():
            output_file.write("-" * 40 + "\n")
            output_file.write("Subfolder: {}\n".format(subfolder))
            output_file.write("File\t\t\tWord Count\n")
            output_file.write("-" * 40 + "\n")
            for file, count in files.items():
                output_file.write("{}\t\t\t{}\n".format(file, count))
            output_file.write("-" * 40 + "\n")
            output_file.write("Total\t\t\t\t{}\n".format(sum(files.values())))
            output_file.write("\n")
        output_file.write("=" * 40 + "\n\n")
    output_file.close()


def count_english_words(fp):
    lines = fp.readlines()
    word_count = 0
    for line in lines:
        if line.startswith("    # ") or line.startswith("    old "):
            matches = re.findall(r'"([^"]*)"', line)
            for match in matches:
                words = match.split()
                for word in words:
                    if word.isascii():
                        word_count += 1
    return word_count


is_python3 = (sys.version_info > (3, 0))
script_dir = os.path.dirname(os.path.abspath(__file__))
folders = os.listdir(script_dir)
report = {}

for folder in folders:
    if not os.path.isdir(os.path.join(script_dir, folder)) or folder == "media" or folder == "none" or folder == ".git":
        continue
    lang_folder = os.path.join(script_dir, folder)
    lang = folder.capitalize()
    subfolders = {}
    for root, dirs, files in os.walk(lang_folder):
        subfolder = os.path.relpath(root, lang_folder)
        subfolder_files = {}
        for f in files:
            if os.path.splitext(f)[1] == ".rpy":
                file_path = os.path.join(root, f)
                with (open(file_path, encoding="utf-8") if is_python3 else codecs.open(file_path, encoding="utf-8")) as fp:
                    word_count_file = count_english_words(fp)
                    subfolder_files[f] = word_count_file
        if subfolder_files:
            subfolders[subfolder] = subfolder_files
    if subfolders:
        report[lang] = subfolders

open_report(is_python3, report)
