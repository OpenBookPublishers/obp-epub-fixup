#!/usr/bin/env python3
from bs4 import BeautifulSoup
import argparse
import os

def read_toc_xhtml(toc_xhtml):
    with open(toc_xhtml, 'r') as toc_xhtml_f:
        soup = BeautifulSoup(toc_xhtml_f, 'html.parser')

        # Create a dictionary with toc entries (with link and text)
        entries = [{'src': entry.get('href'), 'text': entry.string} \
                  for entry in soup.find_all('a')]

        return entries

def write_output(soup, out_file):
        with open(out_file, 'wb') as out_file_f:
            raw_soup = soup.encode('utf-8')
            out_file_f.write(raw_soup)

def run():
    # Parse input arguments
    parser = argparse.ArgumentParser(description='fix_title_tag')
    parser.add_argument('toc_xhtml',
                        help = 'input toc.xhtml file to process')
    parser.add_argument('in_folder',
                        help = 'input folder with files to process')
    parser.add_argument('out_folder',
                        help = 'output folder with files to write to')

    args = parser.parse_args()

    entries = read_toc_xhtml(args.toc_xhtml)

    for entry in entries:
        in_file_path = os.path.join(args.in_folder, entry['src'])

        with open(in_file_path, 'r') as in_file_f:
            soup = BeautifulSoup(in_file_f, 'html.parser')

            soup.find('title').string.replace_with(entry['text'])

        out_file_path = os.path.join(args.out_folder, entry['src'])
        write_output(soup, out_file_path)

if __name__ == '__main__':
    run()
