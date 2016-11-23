#
# Copyright 2016 Import.io
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import sys
import argparse
from newsdriver.version import __version__
from newsdriver import GoogleSheet
from newsdriver import ExtractorGetUrlList
import logging

SHEET_URLS = 'sheet-urls'
EXTRACTOR_URLS = 'extractor-urls'
DESCRIPTION = "Web Extractor for News Driver"

logger = logging.getLogger(__name__)


class NewsDriver(object):

    def __init__(self):
        self._version = __version__
        self._debug = False
        self._command = None
        self._extractor_id = None
        self._sheet_id = None
        self._range = None

    def add_extractor_id_argument(self, parser):
        parser.add_argument('-e', '--extractor-id', dest="extractor_id", action='store', required=True)

    def add_debug_argument(self, parser):
        parser.add_argument('-d', '--debug', dest="debug", action='store_true')

    def handle_arguments(self):

        parser = argparse.ArgumentParser(description=DESCRIPTION)
        subparser = parser.add_subparsers(help='commands')

        sheet_urls = subparser.add_parser(SHEET_URLS, help='sheet-urls')
        self.add_debug_argument(sheet_urls)
        sheet_urls.add_argument('-i', '--sheet-id', dest="sheet_id", action='store', required=True)
        sheet_urls.add_argument('-r', '--range', dest="range", action='store', required=False)
        sheet_urls.set_defaults(which=SHEET_URLS)

        extractor_urls = subparser.add_parser('extractor-urls', help='extractor-urls')
        self.add_extractor_id_argument(extractor_urls)
        self.add_debug_argument(extractor_urls)
        extractor_urls.set_defaults(which=EXTRACTOR_URLS)

        extract = subparser.add_parser('extract', help='extract')
        self.add_extractor_id_argument(extract)
        self.add_debug_argument(extract)
        extract.add_argument('-i', '--sheet-id', dest="sheet_id", action='store')
        extract.set_defaults(which='extract')

        args = parser.parse_args()

        if 'which' in args:
            self._command = args.which

        if 'extractor_id' in args:
            self._extractor_id = args.extractor_id

        if 'sheet_id' in args:
            self._sheet_id = args.sheet_id

        if 'range' in args:
            self._range = args.range

        if 'debug' in args:
            self._debug = args.debug

    def display_extractor_urls(self):
        api = ExtractorGetUrlList(extractor_id=self._extractor_id)
        urls = api.get()
        for url in urls:
            print(url)

    def display_sheet_urls(self):
        sheet = GoogleSheet(spreadsheet_id=self._sheet_id, range=self._range)
        sheet.initialize_service()
        urls = sheet.get_urls()
        for url in urls:
            print(url[0])

    def execute(self):
        self.handle_arguments()
        if self._debug:
            logging.basicConfig(level=logging.DEBUG)
        logger.debug("Running: {0}".format(self._command))
        if self._command == SHEET_URLS:
            self.display_sheet_urls()
        elif self._command == EXTRACTOR_URLS:
            self.display_extractor_urls()


def main():
    ns = NewsDriver()
    ns.execute()


if __name__ == '__main__':
    main()

