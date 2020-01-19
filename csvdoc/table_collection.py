# -*- coding: <utf-8>
# internal
from . cell_format import CellFormat
from . multi_document_row_transform import MultiDocumentRowTransform
# external
import pandas as pd
# logging
import logging
logger = logging.getLogger(__name__)


class TableCollection(dict):
    """
    Class which provides functions to load, manipulate
    and save a collection of csv files.
    """

    def __init__(self, **kwargs):
        self.files = kwargs.get("files", [])
        self.cell_fmt = CellFormat()
        self.transform = MultiDocumentRowTransform()
        logger.debug(self.files)

    def __str__(self):
        txt = "\n"
        for file, df in self.items():
            txt += str(df) + "\n"
        return txt

    def load(self):
        """
        Reads csv files, converts data
        and stores it in pandas data frames.
        """
        self.clear()
        for file in self.files:
            df = pd.read_csv(
                file, delimiter=",", header=0, keep_default_na=False
            )
            df.fillna('', inplace=True)
            df.sort_index(axis=1, inplace=True)
            df = self.cell_fmt.df_to_py(df)
            self.update({file: df})
            logger.debug("Loaded: " + file)

    def save(self):
        """
        Creates or overwrites csv files
        with back converted data.
        """
        for file, df in self.items():
            df = self.cell_fmt.df_to_db(df)
            df.sort_index(axis=1, inplace=True)
            df.to_csv(file, index=False)
            logger.debug("Saved: " + file)

    def get_columns_shaped(self):
        """
        Returns a list of data frames with
        columns for each YAML value in document.
        """
        return list(self.values())

    def set_columns_shaped(self, filedfs):
        """
        Sets the data via a list for each data frame with
        columns for each YAML value in document.
        """
        assert len(filedfs) == len(self.files), \
            "All data frames have to be set together " + \
            "and according to files list!"
        self.clear()
        for idx, file in enumerate(self.files):
            self.update({file: filedfs[idx]})

    def get_document_shaped(self, pre=[]):
        """
        Returns a list of data frames
        with one cloumn for each document.
        """
        transform = self.transform.col_dps_to_multi_doc
        return [transform(df, pre) for file, df in self.items()]

    def set_document_shaped(self, filedfs, pre=[]):
        """
        Sets the data frames via a list for each data frame with one
        column for each document.
        """
        assert len(filedfs) == len(self.files), \
            "All data frames have to be set together " + \
            "and according to files list!"
        self.clear()
        transform = self.transform.multi_doc_to_col_dps
        for idx, file in enumerate(self.files):
            self.update({file: transform(filedfs[idx], pre)})
