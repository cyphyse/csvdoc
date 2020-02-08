# -*- coding: <utf-8>
# intern
import config
from csvdoc.single_document_row_transform import SingleDocumentRowTransform
# extern
import pandas as pd
# testing
import unittest
# logging
import logging
logger = logging.getLogger(__name__)


class TestSingleDocumentRowTransform(unittest.TestCase):

    def test(self):
        # init test
        config.cnt_step = 1
        # init SUT
        transform = SingleDocumentRowTransform()
        # init data
        doc = config.yaml_data + config.md_text
        # test onversion functions
        config.disp(
            "Preparation 1 (markdown document with yaml frontmatter):",
            doc
        )
        data = [doc, doc]
        yaml_df = pd.DataFrame(data, columns=["custom"])
        config.disp(
            "Preparation 2 (2 markdown documents in pandas df):",
            yaml_df
        )
        custom_df = transform.single_doc_to_col_dps(yaml_df, "custom")
        config.disp(
            "Test 1 (unpack document data to columns):",
            custom_df
        )
        self.assertEqual(custom_df.loc[0, "markdown"], config.md_text)
        if config.TEST_VARIANT == 1:
            self.assertEqual(custom_df.loc[0, "b"], 2)
        yaml_df_reverse = transform.col_dps_to_single_doc(custom_df, "custom")
        config.disp(
            "Test 2 (pack columns data to document):",
            yaml_df_reverse
        )
        assert (yaml_df_reverse == yaml_df).all, \
            "Reverse converted data is: \n" + str(yaml_df_reverse)
        # test field compare
        tmp = custom_df.copy()
        tmp.loc[0, "b"] = 6
        yamlmddf_changed = transform.col_dps_to_single_doc(custom_df, "custom")
        reference = yamlmddf_changed.loc[0, "custom"]
        comparison = yaml_df_reverse.loc[0, "custom"]
        self.assertTrue(transform.compare.fields(reference, comparison))
        comparison = "---\nc: 5\nb: 6\n---\n" + config.md_text
        self.assertFalse(transform.compare.fields(reference, comparison))
        custom_df.columns = ["test." + col for col in custom_df.columns]
        for name in config.HYBRID_DATABASE_NAME:
            custom_df.to_csv(name, index=False)
