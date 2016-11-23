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
import requests
import os
import logging

logger = logging.getLogger(__name__)


class Extractor(object):

    def __init__(self, extractor_id):
        self._extractor_id = extractor_id
        self._api_key = os.environ['IMPORT_IO_API_KEY']


class ExtractorGet(Extractor):

    def __init__(self, extractor_id):
        super(ExtractorGet, self).__init__(extractor_id)

    def get(self):

        url = "https://store.import.io/store/extractor/{0}".format(self._extractor_id)

        querystring = {
            "_apikey": self._api_key
        }

        headers = {
            'cache-control': "no-cache",
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        logger.debug(response.text)
        return response.json()


class ExtractorGetUrlList(Extractor):

    def __init__(self, extractor_id):
        super(ExtractorGetUrlList, self).__init__(extractor_id)

    def get(self):
        api = ExtractorGet(extractor_id=self._extractor_id)

        extractor = api.get()

        url = "https://store.import.io/store/extractor/{0}/_attachment/urlList/{1}".format(
            self._extractor_id, extractor['urlList'])
        querystring = {
            "_apikey": self._api_key
        }

        headers = {
            'accept-encoding': "gzip",
            'cache-control': "no-cache",
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        logger.debug(response.text)
        return response.text.split('\n')

