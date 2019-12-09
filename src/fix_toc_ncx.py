#!/usr/bin/env python3
import argparse
from bs4 import BeautifulSoup


def read_toc_xhtml(toc_xhtml):
    with open(toc_xhtml, 'r') as toc_xhtml_f:
        soup = BeautifulSoup(toc_xhtml_f, 'html.parser')

        # Create a dictionary with toc entries (with link and text)
        entries = [{'src': entry.get('href'), 'text': entry.string}
                   for entry in soup.find_all('a')]

        return entries


def write_output(soup, out_toc_ncx):
    with open(out_toc_ncx, 'wb') as out_toc_ncx_f:
        raw_soup = soup.encode('utf-8')
        out_toc_ncx_f.write(raw_soup)


def run():
    # Parse input arguments
    parser = argparse.ArgumentParser(description='fix_toc_ncx')
    parser.add_argument('toc_xhtml',
                        help='input toc.xhtml file to process')
    parser.add_argument('in_toc_ncx',
                        help='input toc.ncx file to process')
    parser.add_argument('out_toc_ncx',
                        help='output toc.ncx file to write to')

    args = parser.parse_args()

    with open(args.in_toc_ncx, 'r') as in_toc_ncx_f:
        soup = BeautifulSoup(in_toc_ncx_f, 'xml')

        entries = read_toc_xhtml(args.toc_xhtml)

        for navpoint in soup.find_all('navPoint'):
            src = navpoint.content.get('src')

            # Retrieve correct text entries from toc_xhtml
            # by matching src values
            text = next((entry['text'] for entry in entries
                         if entry['src'] == src), None)

            # Replace the text string
            if text:
                navpoint.find('text').string.replace_with(text)

        write_output(soup, args.out_toc_ncx)


if __name__ == '__main__':
    run()
