#!/usr/bin/env python3
from bs4 import BeautifulSoup
import argparse
import os
from urllib.parse import urlsplit

def get_h1_text(file_path):
    with open(file_path, 'r') as section:
        file_soup = BeautifulSoup(section, 'html.parser')

        class_list = ["heading1", "heading1-aut"]
        h1 = file_soup.find_all('h1', class_=class_list)

        if len(h1) == 1:
            return file_soup.h1.get_text()

        elif len(h1) > 1:
            print("[WARNING] {} has multiple h1 tags" \
                  .format(os.path.basename(file_path)))
            return h1.pop(0).get_text()

        else:
            return False

def write_output(soup, output_file):
    with open(output_file, 'wb') as output:
        raw_soup = soup.encode('utf-8')
        output.write(raw_soup)

def sanitize_href(href):
    """
    Strips fragment from href.
    i.e. 'index.xhtml#my_anchor' -> 'index.xhtml'
    
    urlsplit(file_path)[2] returns the path attribute of a URL.
    """
    clean_href = urlsplit(href)[2]

    return clean_href

def run():
    # Parse input arguments
    parser = argparse.ArgumentParser(description='fix_toc_xhtml')
    parser.add_argument('input_file',
                        help = 'Input file to process')
    parser.add_argument('output_file',
                        help = 'Output file')

    args = parser.parse_args()

    # Dictionary with known filenames and relative section name
    known = {
        # Front matters
        'front-cover.xhtml': 'Front Cover',
        'half-title.xhtml': 'Half Title',
        'title.xhtml': 'Title',
        'copyright.xhtml': 'Copyright',
        'dedication.xhtml': 'Dedication',
        'contents.xhtml': 'Contents',

        # Back matters
        'back-page.xhtml': 'Back Page',
        'back-cover.xhtml': 'Back Cover'
    }

    with open(args.input_file, 'r') as sf:
        soup = BeautifulSoup(sf, 'html.parser')

        for link in soup.find_all('a'):

            href = link.get('href')

            # Sanitize href by stripping URL fragment
            clean_href = sanitize_href(href)

            if href != clean_href:
                link['href'] = clean_href
                print('[INFO] {} sanitized to {}'.format(href, clean_href))

            # Replace strings in 'known' filenames
            if clean_href in known:
                link.string.replace_with(known[clean_href])
                continue

            # Replace string in 'uncertain' filenames
            file_path = os.path.join(os.path.dirname(args.input_file), \
                                     clean_href)
            h1_text = get_h1_text(file_path)

            if h1_text:
                link.string.replace_with(h1_text)
                continue

            # If no match found, string is unchanged
            print("[INFO] No title found for {}; fallback" \
                  .format(clean_href))

        write_output(soup, args.output_file)

if __name__ == '__main__':
    run()
