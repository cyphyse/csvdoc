# -*- coding: <utf-8>
# intern
import config
from csvdoc.document_transform import DocumentTransform
# testing
import unittest
# logging
import logging
logger = logging.getLogger(__name__)


class TestDocumentValidation(unittest.TestCase):

    def test(self):
        def rows(data, start, end):
            return "".join(config.yaml_data.splitlines(True)[start:end])
        # init test
        config.cnt_step = 1
        # init SUT
        transform = DocumentTransform()
        # init data
        yo = config.yaml_data
        doc_full_origin = yo + config.md_text
        yaml_data_wo_first_sep = rows(config.yaml_data, 1, None)
        doc_full_wo_first_sep = yaml_data_wo_first_sep + config.md_text
        yaml_data_wo_second_sep = rows(config.yaml_data, 0, -1)
        doc_full_wo_second_sep = yaml_data_wo_second_sep + config.md_text
        yaml_data_wo_sep = rows(config.yaml_data, 1, -1)
        doc_full_origin = config.yaml_data
        config.disp("Preparation (doc_full_origin)", doc_full_origin)
        config.disp("Preparation (doc_full_wo_first_sep)", doc_full_wo_first_sep)
        config.disp("Preparation (doc_full_wo_second_sep)", doc_full_wo_second_sep)
        # full documents
        res = transform.valid_fields(doc_full_origin, doc_full_wo_first_sep)
        self.assertTrue(res)
        res = transform.valid_fields(doc_full_origin, doc_full_wo_second_sep)
        self.assertFalse(res)
        # data only
        res = transform.valid_fields(yo, yaml_data_wo_first_sep)
        self.assertTrue(res)
        res = transform.valid_fields(yo, yaml_data_wo_second_sep)
        self.assertTrue(res)
        res = transform.valid_fields(yo, yaml_data_wo_sep)
        self.assertTrue(res)
        res = transform.valid_fields(yaml_data_wo_sep, yaml_data_wo_first_sep)
        self.assertTrue(res)
        res = transform.valid_fields(yaml_data_wo_sep, yaml_data_wo_second_sep)
        self.assertTrue(res)
        res = transform.valid_fields(yo, rows(yo, 2, -1))
        self.assertFalse(res)
