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

from unittest import TestCase
from newsdriver import GoogleSheet

SPREADSHEET_ID = '1qKTvNZKLaS6hwlC-jt-RYfHfehKziwpJAc6N7yNKWX0'


class TestGoogleSheet(TestCase):

    def test_google_sheet_constructor(self):
        sheet = GoogleSheet(spreadsheet_id=SPREADSHEET_ID)
        self.assertIsNotNone(sheet)

    def test_google_sheet_oauth(self):
        sheet = GoogleSheet(spreadsheet_id=SPREADSHEET_ID)
        credentials = sheet.get_credentials()
        self.assertIsNotNone(credentials)

    def test_get_urls(self):
        sheet = GoogleSheet(spreadsheet_id=SPREADSHEET_ID)
        sheet.initialize_service()
        urls = sheet.get_urls()
        self.assertIsNotNone(urls)
        self.assertEquals(len(urls), 4)

    def test_check_urls(self):
        sheet = GoogleSheet(spreadsheet_id=SPREADSHEET_ID)
        sheet.initialize_service()
        urls = sheet.get_urls()
        self.assertEquals('http://www.zipcodestogo.com/California/', urls[0][0])
        self.assertEquals('http://www.zipcodestogo.com/Georgia/', urls[1][0])
        self.assertEquals('http://www.zipcodestogo.com/Florida/', urls[2][0])
        self.assertEquals('http://www.zipcodestogo.com/Utah/', urls[3][0])

