# -*- coding: <utf-8>
# intern
import config
from csvdoc.multi_document_row_transform import MultiDocumentRowTransform
from csvdoc.table_collection import TableCollection
# testing
import unittest
# logging
import logging
logger = logging.getLogger(__name__)


class TestTableCollection(unittest.TestCase):

    def test(self):
        # init test
        config.cnt_step = 1
        # init SUT
        collection = TableCollection(
            files=config.HYBRID_DATABASE_NAME
        )
        # test basics
        collection.load()
        collection.get_document_shaped()[0].to_csv("test_result_1.csv", index=False)
        collection.get_columns_shaped()[0].to_csv("test_result_2.csv", index=False)
        # test transfomation
        transform = MultiDocumentRowTransform()
        df = collection.get_columns_shaped()[0]
        df = transform.col_dps_to_multi_doc(df)
        df.to_csv("test_result_3.csv", index=False)
        df = transform.multi_doc_to_col_dps(df)
        df.to_csv("test_result_4.csv", index=False)
