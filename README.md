# obp-epub-fixup
Collection of scripts to fix epub files programmatically

Work in progress

## Contents
These scripts refer specifically to our InDesing -> ePub workflow. Assumptions given here might be inaccurate in different settings.

### ./src/fix_toc_xhtml.py
As sections in `toc.xhtml` are named after filenames, this script parse each section of the book, looking for the content of `<h1 class="heading1">` tags and write these back to the _toc file_.

Special sections (such as the _copyright_ page) which might not include `<h1>` tags are named after pre-determined, convectional terms (hardcoded in a python dictionary).

### ./src/fix_toc_ncx.py
This script follows the same principle as `./src/fix_toc_xhtml.py`, but changes apply to `toc.ncx` files. To ensure consistency, section names are parsed from the `toc.xhtml` file rather than fish out `<h1 class="heading1">` tags from the book sections a second time.

### ./src/fix_title_tag.py
The content of the `<title>` tag is updated with the more accurate string stored in `toc.xhtml`. This process is repeated for all the book sections which appear in the `toc.xhtml` file.
