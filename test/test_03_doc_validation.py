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
        md = config.md_text
        # --- data --- markdown
        doc_full_origin = yo + md

        # data => --- data ---
        yaml_wo_sep = rows(yo, 1, -1)
        # --- data => --- data ---
        yaml_w_first_sep = rows(yo, 0, -1)
        # data --- => --- data ---
        yaml_w_second_sep = rows(yo, 1, None)

        # markdown => --- --- markdown
        md_wo_sep = md
        # --- markdown => --- --- markdown
        md_w_one_sep = rows(yo, 0, 1) + md

        # data --- markdown => --- data --- markdown
        doc_w_second_sep = yaml_w_second_sep + md
        # --- data markdown => fail
        doc_w_first_sep = yaml_w_first_sep + md

        cnt = 0
        # clean separator test (VISUAL ONLY)
        def print_sep_test(doc):
            nonlocal cnt
            cnt += 1
            print("Begin of sample [%d]:" % cnt)
            print(doc)
            print("End of sample.")
            res = transform.get_sep_cleaned_doc(doc)
            print("Cleaned data [%d]:" % cnt)
            print(res)
            print("End of cleaned data.")
        logger.warning("START OF MANUAL TEST")
        print_sep_test(doc_full_origin)
        print_sep_test(yaml_wo_sep)
        print_sep_test(yaml_w_first_sep)
        print_sep_test(yaml_w_second_sep)
        print_sep_test(md_wo_sep)
        print_sep_test(md_w_one_sep)
        print_sep_test(doc_w_second_sep)
        print_sep_test(doc_w_first_sep)
        print_sep_test("---\n" + yo + "---\n" + md)
        logger.warning("END OF MANUAL TEST")
        # full document validation
        res = transform.valid_fields(doc_full_origin, doc_w_second_sep)
        self.assertTrue(res)
        res = transform.valid_fields(doc_full_origin, doc_w_first_sep)
        self.assertFalse(res)
        res = transform.valid_fields(md, md)
        self.assertTrue(res)
        # data onlyvalidation
        res = transform.valid_fields(yo, yaml_w_second_sep)
        self.assertTrue(res)
        res = transform.valid_fields(yo, yaml_w_first_sep)
        self.assertTrue(res)
        res = transform.valid_fields(yo, yaml_wo_sep)
        self.assertTrue(res)
        res = transform.valid_fields(yaml_wo_sep, yaml_w_second_sep)
        self.assertTrue(res)
        res = transform.valid_fields(yaml_wo_sep, yaml_w_first_sep)
        self.assertTrue(res)
        res = transform.valid_fields(yo, rows(yo, 2, -1))
        self.assertFalse(res)
