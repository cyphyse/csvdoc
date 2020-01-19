# -*- coding: <utf-8>
# internal
from . single_document_row_transform import SingleDocumentRowTransform
# external
import pandas as pd
# logging
import logging
logger = logging.getLogger(__file__)


class MultiDocumentRowTransform(SingleDocumentRowTransform):
    """
    General idea:
    Specific data fields, also called datapoints (dps),
    can be collected in a markdown document as yaml frontmatter or
    splitted into columns in a table with one or more documents per row.
    This class provides the functions to ether
    collect datapoints from columns to put them into a yaml frontmatter or
    split datapoints from a yaml frontmatter into columns.
    """
    def col_dps_to_multi_doc(self, df, pre=[]):
        """
        Creates a pandas data frame with markdown documents in cells.
        The datapoints are inserted as yaml frontmatter.
        Documents are created from those columns,
        which have the prefix given in pre (one doc per prefix).
        """
        data_model = {}
        for col in df.columns:
            data_struct = col.split(".")
            T = data_struct[0]
            if not T in data_model.keys():
                data_model.update({T: {"l": [], "s": []}})
            data_model[T]["l"] += [col]
            data_model[T]["s"] += [".".join(data_struct[1:])]
        if len(pre) == 0:
            pre = list(data_model.keys())
        dfs = []
        cols = []
        for T, data_struct in data_model.items():
            if T in pre:
                tmp = df[data_struct["l"]]
                tmp.columns = data_struct["s"]
                dfs.append(self.col_dps_to_single_doc(tmp, T))
                cols.append(T)
            else:
                dfs.append(df[data_struct["l"]])
                cols += data_struct["l"]
        # concat
        document_df = pd.concat(dfs, axis=1, ignore_index=True)
        document_df.columns = cols
        return document_df

    def multi_doc_to_col_dps(self, df, pre=[]):
        """
        Creates a df with columns from yaml frontmatter.
        Each column datapoint name gets the prefix of the document column name.
        Only those documents are splited, which are in list parameter 'pre'.
        """
        if len(pre) == 0:
            pre = list(df.columns)
        dfs = []
        for ac in df:
            col_as_df = df.loc[:, [ac]]
            if ac in pre:
                partial_columns_df = self.single_doc_to_col_dps(col_as_df, ac)
                partial_columns_df.columns = [ac + "." + col for col in list(partial_columns_df.columns)]
                dfs.append(partial_columns_df)
            else:
                dfs.append(col_as_df)
        # concat
        columns_df = pd.concat(dfs, axis=1)
        return columns_df
