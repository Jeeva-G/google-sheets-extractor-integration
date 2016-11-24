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
from newsdriver.extractor import ExtractorGet
from newsdriver.extractor import ExtractorGetUrlList
from newsdriver.extractor import ExtractorPutUrlList
from newsdriver.extractor import ExtractorStart
from newsdriver.extractor import ExtractorStatus

EXTRACTOR_ID = '9dd8b560-70c1-43f1-902d-567ac2e2cf3f'


class TestExtractorGet(TestCase):
    def test_constructor(self):
        api = ExtractorGet(extractor_id=EXTRACTOR_ID)
        e = api.get()
        self.assertIsNotNone(e)
        self.assertEquals(EXTRACTOR_ID, e['guid'])

    def test_get(self):
        api = ExtractorGet(extractor_id=EXTRACTOR_ID)
        e = api.get()
        self.assertIsNotNone(e)
        self.assertEquals(EXTRACTOR_ID, e['guid'])


class TestExtractorGetUrList(TestCase):
    def test_constructor(self):
        api = ExtractorGetUrlList(extractor_id=EXTRACTOR_ID)
        self.assertIsNotNone(api)

    def test_get_url_list(self):
        api = ExtractorGetUrlList(extractor_id=EXTRACTOR_ID)
        urls = api.get()
        self.assertIsNotNone(urls)

    def test_get_url_list_count(self):
        api = ExtractorGetUrlList(extractor_id=EXTRACTOR_ID)
        urls = api.get()
        self.assertEquals(10, len(urls))

    def test_get_url_list_values(self):
        api = ExtractorGetUrlList(extractor_id=EXTRACTOR_ID)
        urls = api.get()
        for i in range(0, 10):
            self.assertEquals("http://www.ikea.com/us/en/search/?query=chairs&pageNumber={0}".format(i + 1),
                              urls[i])


class TestExtractorPutUrlList(TestCase):
    def test_constructor(self):
        api = ExtractorPutUrlList
        self.assertIsNotNone(api)

    def test_put_url_list(self):
        api = ExtractorPutUrlList(extractor_id=EXTRACTOR_ID)
        urls = [
            'http://www.ikea.com/us/en/search/?query=chairs&pageNumber=1',
            'http://www.ikea.com/us/en/search/?query=chairs&pageNumber=2',
            'http://www.ikea.com/us/en/search/?query=chairs&pageNumber=3',
            'http://www.ikea.com/us/en/search/?query=chairs&pageNumber=4',
            'http://www.ikea.com/us/en/search/?query=chairs&pageNumber=5',
            'http://www.ikea.com/us/en/search/?query=chairs&pageNumber=6',
            'http://www.ikea.com/us/en/search/?query=chairs&pageNumber=7',
            'http://www.ikea.com/us/en/search/?query=chairs&pageNumber=8',
            'http://www.ikea.com/us/en/search/?query=chairs&pageNumber=9',
            'http://www.ikea.com/us/en/search/?query=chairs&pageNumber=10'
        ]

        api.put(urls)


class TestExtractorStart(TestCase):

    def test_constructor(self):
        api = ExtractorStart()
        self.assertIsNotNone(api)

    def test_extractor_start(self):
        self.assertTrue(False)


class TestExtractorStatus(TestCase):

    def test_constructor(self):
        api = ExtractorStatus()
        self.assertIsNotNone(api)

    def test_extractor_status(self):
        self.assertTrue(False)
