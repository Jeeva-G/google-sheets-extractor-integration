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
import logging

SHEET_URLS = "sheet-urls"

logger = logging.getLogger(__name__)


class NewsDriver(object):

    def __init__(self):
        self._description = "Web Extractor for News Driver"
        self._version = __version__
        self._command = None
        self._sheet_id = None

    def handle_arguments(self):

        parser = argparse.ArgumentParser(description=self._description)
        subparser = parser.add_subparsers(help='commands')

        sheet_parser = subparser.add_parser(SHEET_URLS, help='sheet-urls')
        sheet_parser.add_argument('-i', '--sheet-id', dest="sheet_id", action='store', required=True)
        sheet_parser.add_argument('-r', '--range', dest="range", action='store', required=False)
        sheet_parser.set_defaults(which='sheet-urls')

        extract_parser = subparser.add_parser('extract', help='extract')
        extract_parser.add_argument('-i', '--sheet-id', dest="sheet_id", action='store')
        extract_parser.add_argument('-e', '--extractor-id', dest="extractor_id", action='store')
        extract_parser.set_defaults(which='extract')

        args = parser.parse_args()

        if 'which' in args:
            self._command = args.which

        if self._command == SHEET_URLS:
            self._sheet_id = args.sheet_id
            self._range = args.range

    def display_urls(self):
        sheet = GoogleSheet(spreadsheet_id=self._sheet_id)
        sheet.initialize_service()
        urls = sheet.get_urls()
        for url in urls:
            print(url[0])

    def execute(self):
        self.handle_arguments()
        logger.debug("Running: {0}".format(self._command))
        if self._command == SHEET_URLS:
            self.display_urls()


def main():
    ns = NewsDriver()
    ns.execute()


if __name__ == '__main__':
    main()

