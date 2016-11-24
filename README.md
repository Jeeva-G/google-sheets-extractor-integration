# NewsDriver Web Extraction Solution

This repository includes a script solution that uses URLs taken from a Google sheet
and copies to an existing Import.io Extractor, then lastly executes the Extractor
to collect data from the supplied URLs.

The command script is implemented using Python, which can be executed on any
operating system that supports a Python version 3.5 or later.

## Installation

The command requires the installation of Python 3.5 or later with some additional
third-party packages that can be installed using [pip](https://pip.pypa.io/en/stable/).


### Download the software package

```
$ git clone https://github.com/import-io/postsales_news-driver.git
```

### Change directory

```
$ cd postsales_news-driver
```

### Run setup.py

```
$ python setup.py
```

## Operation

The command has 6 different sub-commands that are invoked similiarly as follows:

```
$ newsdriver <sub-command>
```

where `sub-command` is one of the following:

- _copy-urls_ - Copies URLs from a specified Google sheet to designated Extractor.
- _extractor-start_ - Initiates a crawl-run of an Extractor.
- _extractor-status_ - Provides a status of the crawl-run(s) of an Extractor.
- _extractor-urls_ - Displays the list of URLs associated with an Extractor.
- _extract_ - Performs the complete extraction operation from copying the URLs from the Google
sheet to running the Extractor to extract data from web pages.
- _sheet-urls_ - Displays a list of the URLs in a Google sheet given the sheet id and range.

### copy-urls

Copy the URLs in the Google Sheet to the Extractor URLs

```
$ newsdriver copy-urls -i <spreasdheet_id> -r <spreadsheet_range> -e <extractor_id>
```

### extractor-start

Initiate a crawl-run on a specific Extractor

```
$ newsdriver extractor-start -e <extractor_id>
```

### extractor-status

Display the status of a crawl-run(s) on a specific Extractor

```
$ newsdriver extractor-status  -e <extractor id>
```

### extractor-urls

Displays the URLs associated with a specific Extractor

```
$ newsdriver extractor-urls  -e <extractor id>
```

### extract

Runs the complete operation of copying URLs from a Google sheet to an Extractor, and starting the Extractor

```
$ newsdriver extract -i <spreasdheet_id> -r <spreadsheet_range> -e <extractor_id>
```

### sheet-urls

Displays the URLs from a specifice Google sheet and range

```
$ newsdriver sheeturls -i <spreasdheet_id> -r <spreadsheet_range>
```

## Programmatic Execution

The same operations as listed above can performed programmatically from Python similar to the following
example:

```python
from newsdriver import NewsDriver

newsdriver = NewsDriver()
newsdriver.extractor_start(extractor_id=<extractor_id>)

```
