# -*- coding: <utf-8>
# intern
import config
from csvdoc.document_transform import DocumentTransform
# testing
import unittest
# logging
import logging
logger = logging.getLogger(__name__)


class TestDocumentTransform(unittest.TestCase):

    def test(self):
        # init test
        config.cnt_step = 1
        # init SUT
        transform = DocumentTransform()
        # init data
        doc = config.yaml_data + config.md_text
        config.disp("Preparation (as full document)", doc)
        dat = transform.to_dict(doc)
        config.disp("Test (as dictionary)", dat)
        if config.TEST_VARIANT == 1:
            self.assertEqual(doc, transform.to_doc(dat))
        if config.TEST_VARIANT == 2:
            self.assertEqual(doc.replace("---\n---\n", ""), transform.to_doc(dat))



        # init data
        doc = config.yaml_data
        config.disp("Preparation (as only data document)", doc)
        dat = transform.to_dict(doc)
        config.disp("Test (as dictionary)", dat)
        if config.TEST_VARIANT == 1:
            self.assertEqual(doc, transform.to_doc(dat))
        if config.TEST_VARIANT == 2:
            self.assertEqual(doc.replace("---\n---\n", ""), transform.to_doc(dat))
