# -*- coding: <utf-8>
# intern
import config
from csvdoc.multi_document_row_transform import MultiDocumentRowTransform
# extern
import pandas as pd
# testing
import unittest
# logging
import logging
logger = logging.getLogger(__name__)


class TestMultiDocumentRowTransform(unittest.TestCase):

    def test(self):
        # init test
        config.cnt_step = 1
        # init SUT
        transform = MultiDocumentRowTransform()
        # init data
        doc = config.yaml_data + config.md_text
        # test onversion functions
        config.disp(
            "Preparation 1 (markdown document with yaml frontmatter):",
            doc
        )
        data = [doc, doc]
        dfs = []
        dfs.append(pd.DataFrame(data, columns=["custom1"]))
        dfs.append(pd.DataFrame(data, columns=["custom2"]))
        df_origin = pd.concat(dfs, axis=1, ignore_index=True)
        df_origin.columns = ["custom1", "custom2"]
        config.disp(
            "Preparation 1 (multiple documents per row):",
            df_origin
        )
        df_tmp1 = transform.multi_doc_to_col_dps(df_origin, ["custom2"])
        config.disp(
            "Test 1 (transform 1 doc):",
            df_tmp1
        )
        df_tmp2 = transform.col_dps_to_multi_doc(df_tmp1, ["custom2"])
        config.disp(
            "Test 2 (transform 1 doc back):",
            df_tmp2
        )
        if config.TEST_VARIANT == 1:
            self.assertTrue(df_tmp2.equals(df_origin))
        if config.TEST_VARIANT == 2:
            df_tmp3 = df_origin
            df_tmp3["custom2"] = df_tmp3["custom2"].str.replace("---\n---\n", "")
            self.assertTrue(df_tmp2.equals(df_tmp3))
