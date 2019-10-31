# obp-epub-fixup
Collection of scripts to fix epub files programmatically

Work in progress

## Contents
These scripts refer specifically to our InDesing -> ePub workflow. Assumptions given here might be inaccurate in different settings.

### ./src/fix_toc_xhtml.py
As sections in `toc.xhtml` are named after filenames, this script parse each sections of the ebook, looking for the content of `<h1 class="heading1">` tags and write these back to the toc file.

Special sections (such as the _copyright page_) which might not include `<h1>` tags are named after pre-determined/convectional terms (hardcoded in a python dictionary).

### ./src/fix_toc_xhtml.py
This script follows the same principle as `./src/fix_toc_xhtml.py`, but changes apply to `toc.ncx` files. To ensure consistency, section names are parsed from the `toc.xhtml` file rather than fish out `<h1 class="heading1">` tags from the book sections a second time.
