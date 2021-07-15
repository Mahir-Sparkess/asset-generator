# encoding: utf-8
"""

"""
__author__ = 'Richard Smith'
__date__ = '01 Jun 2021'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

from asset_scanner.core import BaseExtractor
from asset_scanner.core.handler_picker import HandlerPicker

import re
from typing import Optional, List
import logging


LOGGER = logging.getLogger(__name__)


class AssetExtractor(BaseExtractor):
    """
    The central class for the asset extraction process.

    An instance of the class can be used to atomically process files
    passed to its ``process_file`` method.
    """

    PROCESSOR_ENTRY_POINT = 'asset_extractor.media_handlers'

    def get_category(self, string, label, regex):
        """

        :param string:
        :param label:
        :param regex:
        :return:
        """

        m = re.search(regex, string)

        if not m:
            label = 'data'

        return label
    
    def get_categories(self, filepath, source_media, category_conf) -> dict:
        """

        :param filepath:
        :param source_media:
        :param category_conf:
        :return:
        """

        categories = []

        for conf in category_conf:
            label = self.get_category(filepath, **conf)
            if label:
                categories.append(label)

        return categories

    def process_file(self, filepath: str, source_media: str, checksum: Optional[str] = None) -> None:
        """

        :param filepath:
        :param source_media:
        :param checksum:
        :return:
        """

        # Get dataset description file
        description = self.item_descriptions.get_description(filepath)

        processor = self.processors.get_processor(source_media)

        data = processor.run(filepath, source_media, checksum)
        
        categories = self.get_categories(filepath, source_media, description.categories)

        data['body']['categories'] = categories

        self.output(data)