# -*- coding: <utf-8>
# internal
from . document_transform import DocumentTransform
# external
import pandas as pd
# logging
import logging
logger = logging.getLogger(__file__)


class SingleDocumentRowTransform(DocumentTransform):
    """
    General idea:
    Specific data fields, also called datapoints (dps),
    can be collected in a markdown document as yaml frontmatter or
    splitted into columns in a table with one document per row.
    This class provides the functions to ether
    collect datapoints from columns to put them into a yaml frontmatter or
    split datapoints from a yaml frontmatter into columns.
    """

    def col_dps_to_single_doc(self, col_dps_df, result_col):
        """
        This function changes the data representation of a data frame.
        It takes a data frame with datapoints in each column and
        a separeate column with markdown text.
        It returns a data frame with one markdown col incl. a yaml frontmatter
        with all datapoints from columns of input data frame."""
        data = []
        for idx, row in col_dps_df.iterrows():
            data_to_convert_to_yamlmd = row.to_dict()
            yamlmd_str = self.to_doc(data_to_convert_to_yamlmd)
            data.append(yamlmd_str)
        return pd.DataFrame(data, columns=[result_col])

    def single_doc_to_col_dps(self, doc_dps_df, select_col):
        """
        This function change the data representation of a data frame.
        It takes a data frame with one column which contains
        markdown text with datapoints in a yaml frontmatter.
        It returns a dataframe with a colmuns for each datapoint
        and an additional column for plain markdown text.
        """
        data = []
        for idx, row in doc_dps_df.iterrows():
            yamlmd_to_convert_to_data = row[select_col]
            data_dict = self.to_dict(yamlmd_to_convert_to_data)
            data.append(data_dict)
        return pd.DataFrame(data)
