#!/usr/bin/env python3
"""
Hyperlinks of the Table of Contents entries are erratic,
and are subject to all sort of undesirable variations
(i.e. entries might not be hyperlinked, attributes missing etc)

This script picks the (reliable) hyperlink destination of the
entry page and fixes the links of the other part of the TOC entry.
"""
import argparse
from bs4 import BeautifulSoup


def write_output(soup, output_file):
    with open(output_file, 'wb') as output:
        raw_soup = soup.encode('utf-8')
        output.write(raw_soup)


def run():
    # Parse input arguments
    parser = argparse.ArgumentParser(description='fix_contents_xhtml')
    parser.add_argument('input_file',
                        help='Input file to process')
    parser.add_argument('output_file',
                        help='Output file')

    args = parser.parse_args()

    with open(args.input_file, 'r') as sf:
        soup = BeautifulSoup(sf, 'html.parser')

        # Find all the table rows of the TOC
        for tr in soup.find_all('tr', {'class': 'invisible-table'}):

            # Get all the column of the parsed row (tr)
            td = tr.find_all('td')

            # Extract the (reliable) filepath from the page number
            # Get the page number entry (located in the last column)
            page_entry = td[-1]

            # Skip if the column is empty (i.e. empty row or author names)
            if not page_entry.text:
                continue

            # Get value of the href attribute
            page_href = page_entry.p.a.get('href')

            # Fix the href values for the entries of all the column
            for counter in td:

                # SKIPS
                # Skip if the column is empty
                if not counter.text:
                    continue

                p = counter.find('p')
                a = counter.find('a')

                # Skip if the column has nested <p><a> tags
                # and the value of the attribute href is set.
                if p and a and a.get('href'):
                    continue

                # SETS
                # If <p> and <a> exist, but href value is empty,
                # Set value to href
                if p and a and (not a.get('href')):
                    a['href'] = page_href

                # If <p> exists but <a> doesen't,
                # Wrap a <a> tag around the content of <p>
                if p and (not a):
                    p.contents[0].wrap(soup.new_tag('a', href=page_href))

        write_output(soup, args.output_file)


if __name__ == '__main__':
    run()
