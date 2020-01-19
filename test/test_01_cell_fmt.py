# -*- coding: <utf-8>
# intern
import config
from csvdoc.cell_format import CellFormat
# testing
import unittest
# logging
import logging
logger = logging.getLogger(__name__)


class TestCellFormat(unittest.TestCase):

    def test(self):
        # init test
        config.cnt_step = 1
        # init SUT
        cell_fmt = CellFormat()
        # init data
        init = [
            {
                "_id": "133-3",
                "string": "string",
                "fnumber": 5.5,
                "inumber": 5,
                "list v 1": "[\"str1\", \"str2\"]",
                "list v 2": "[\'str1\'; \'str2\']",
                "date": "2019-12-01T12:30"
            }
        ]
        origin = init.copy()
        config.disp("Original-Format", origin)
        py = cell_fmt.records_to_py(origin)
        config.disp("Python-Format", py)
        csv = cell_fmt.records_to_db(py)
        config.disp("CSV-Format", csv)
        self.assertEqual(csv, origin)
