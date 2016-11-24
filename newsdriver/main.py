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
from newsdriver import ExtractorPutUrlList
import logging

CMD_COPY_URLS = 'copy-urls'
CMD_EXTRACT = 'extract'
CMD_EXTRACTOR_RUN = 'extract-run'
CMD_EXTRACTOR_STATUS = 'extract-status'
CMD_EXTRACTOR_URLS = 'extractor-urls'
CMD_SHEET_URLS = 'sheet-urls'

DESCRIPTION = "Web Extractor for News Driver"

logger = logging.getLogger(__name__)


class NewsDriver(object):
    """
    Implements command line utitlity the encompasses the extraction requirements for NewsDriver which includes:

    1. Extract the target URLs from a Google Spreadsheet
    2. Add the extracted URLs to the Extractor
    3. Execute the Extractor
    """

    def __init__(self):
        self._version = __version__
        self._debug = False
        self._command = None
        self._extractor_id = None
        self._spread_sheet_id = None
        self._range = None

    def add_extractor_id_argument(self, parser):
        parser.add_argument('-e', '--extractor-id', metavar='extractor_id',
                            dest="extractor_id", action='store', required=True,
                            help='Import.io extractor id or GUID')

    def add_debug_argument(self, parser):
        parser.add_argument('-d', '--debug', dest="debug", action='store_true',
                            help="Enables debug logging")

    def add_spread_sheet_id_argument(self, parser):
        parser.add_argument('-i', '--sheet-id', dest="sheet_id", action='store', required=True,
                            help="Google spreadsheet identifier")

    def add_range_argument(self, parser):
        parser.add_argument('-r', '--range', dest="range", action='store', required=False,
                            help="Range identifying the list of URLs")

    def handle_arguments(self):
        """
        Processes the command line arguments for each of the sub-commands
        :return:
        """

        logger.info("Process command line arguments")

        parser = argparse.ArgumentParser(description=DESCRIPTION)
        subparser = parser.add_subparsers(help='commands')

        #
        # COPY URLS
        #
        copy_urls = subparser.add_parser(CMD_COPY_URLS, help='Copies URLs from google sheet to an extractor')
        self.add_debug_argument(copy_urls)
        self.add_extractor_id_argument(copy_urls)
        self.add_spread_sheet_id_argument(copy_urls)

        #
        # EXTRACTOR
        #
        extract = subparser.add_parser(CMD_EXTRACT, help='Runs the full extraction process')
        self.add_debug_argument(extract)
        self.add_extractor_id_argument(extract)
        self.add_spread_sheet_id_argument(extract)
        extract.set_defaults(which=CMD_EXTRACT)

        #
        # EXTRACTOR START
        #
        extractor_run = subparser.add_parser(CMD_EXTRACTOR_RUN, help='Starts an extractor')
        self.add_debug_argument(extractor_run)
        self.add_extractor_id_argument(extractor_run)
        self.add_spread_sheet_id_argument(extractor_run)

        #
        # EXTRACTOR URLS
        #
        extractor_urls = subparser.add_parser('extractor-urls', help='Displays the URLs from an extractor')
        self.add_debug_argument(extractor_urls)
        self.add_extractor_id_argument(extractor_urls)
        extractor_urls.set_defaults(which=CMD_EXTRACTOR_URLS)

        #
        # SHEET URLS
        #
        sheet_urls = subparser.add_parser(CMD_SHEET_URLS, help='Displays the URLs from a google sheet')
        self.add_debug_argument(sheet_urls)
        self.add_spread_sheet_id_argument(sheet_urls)
        sheet_urls.add_argument('-r', '--range', dest="range", action='store', required=False)
        sheet_urls.set_defaults(which=CMD_SHEET_URLS)

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

    def copy_urls(self):
        logger.info("Copy URLs from Google Sheet: {0} from range: {1} to Extractor: {2}".format(
            self._sheet_id, self._range, self._extractor_id))
        sheet = GoogleSheet(spreadsheet_id=self._spread_sheet_id, range=self._range)
        sheet.initialize_service()
        urls = sheet.get_urls()
        extractor = ExtractorPutUrlList(extractor_id=self._extractor_id)
        extractor.put(urls)

    def extract(self):
        """
        Extracts the URLs from the specified Google Sheet and range, adds to the
        specified Extractor and then run the Extractor
        :return:
        """
        logger.info("Pull URLs from Google Sheet: {0} from range: {1} to Extractor: {2} and run".format(
            self._sheet_id, self._range, self._extractor_id))

        self.copy_urls()
        self.extractor_run()

    def extractor_run(self):
        logger.info("Running extractor: {0}".format(self._extractor_id))
        extractor = ExtractorRun()

    def extractor_status(self):
        logger.info("Status for extractor: {0}".format(self._extractor_id))
        extractor = ExtractorStatus()


    def extractor_urls(self):
        """
        Display the URLs associated with the given extractor
        :return: None
        """
        logger.info("Display URLs from Extractor: {0}".format(self._extractor_id))
        api = ExtractorGetUrlList(extractor_id=self._extractor_id)
        urls = api.get()
        for url in urls:
            print(url)

    def sheet_urls(self):
        """
        Display the URLs associated with the given Google Sheet and range
        :return:
        """
        logger.info("Display URLs from Google Sheet: {0} from range: {1}".format(
            self._sheet_id, self._range))
        sheet = GoogleSheet(spreadsheet_id=self._spread_sheet_id, range=self._range)
        sheet.initialize_service()
        urls = sheet.get_urls()
        for url in urls:
            print(url[0])

    def dispatch_sub_command(self):
        """
        Dispatch sub-command based on command line arguments
        :return:
        """
        if self._debug:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.ERROR)
        logger.info("Running command: {0}".format(self._command))

        if self._command == CMD_COPY_URLS:
            self.copy_urls()
        elif self._command == CMD_EXTRACT:
            self.extract()
        elif self._command == CMD_EXTRACTOR_RUN:
            self.extractor_run()
        elif self._command == CMD_EXTRACTOR_STATUS:
            self.extractor_status()
        elif self._command == CMD_EXTRACTOR_URLS:
            self.extractor_urls()
        elif self._command == CMD_SHEET_URLS:
            self.extractor_urls()

    def execute(self):
        """
        Execute the functionality of the command line utility
        :return: None
        """
        self.handle_arguments()
        self.dispatch_sub_command()


def main():
    """
    Main entry point for command line tool
    :return:
    """
    ns = NewsDriver()
    ns.execute()


if __name__ == '__main__':
    main()
