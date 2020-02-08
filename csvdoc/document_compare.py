# -*- coding: <utf-8>
# internal
from . document_transform import SEPS, SEP, DocumentTransform
# logging
import logging
logger = logging.getLogger(__file__)


class CompareResult(object):
    """
    Class to hold data from compare process.
    """

    def __init__(self, kwargs):
        # flag for modified documents (added separator)
        self.mod = kwargs.get("mod", False)
        # document which was used as reference
        self.ref = kwargs.get("ref", "")
        # document which was used as sample
        self.cmp = kwargs.get("cmp", "")


class DocumentCompare(object):
    """
    Class to check if two documents containing the same data points.
    """

    def __init__(self):
        self.transform = DocumentTransform()

    def get_sep_cleaned_doc(self, document):
        """
        Returns a document with separators in the right places.
        """
        [yaml_data, md_text] = self.transform.split_document(document)
        assert "---" not in yaml_data, "This library is buggy!"
        assert "---" not in md_text, "This library is buggy!"
        if len(yaml_data) > 0:
            doc = SEPS + yaml_data + SEP + md_text
        else:
            doc = SEPS + SEPS + md_text
        return doc

    def get_keys(self, doc, name):
        """
        Returns the data points in a document
        """
        try:
            keys = self.transform.to_dict(doc).keys()
        except Exception as err:
            logger.error("Error '" + str(err) + "' occured "
                         + "during parsing of " + name + ": "
                         + str(doc))
            return None
        return keys

    def print_compare_result(self, ref_doc, cmp_doc, ref_dps, cmp_dps, cr):
        """Prints the result of the comparision."""
        op = " == " if cr else " != "
        res_txt = str(sorted(ref_dps)) + op + str(sorted(cmp_dps))
        ref_txt = "\nReference:\n" + str(ref_doc)
        cmp_txt = "\nComparison:\n" + str(cmp_doc)
        logger.debug("Data field compare: " + res_txt + ref_txt + cmp_txt)

    def determin_same_fields(self, mod, ref_doc, cmp_doc):
        """
        Returns 'CompareResult' if documents containing the same results
        else 'None' is returned.
        """
        cr = None
        if not mod:     # causual compare
            ref_doc = self.get_sep_cleaned_doc(ref_doc)
            cmp_doc = self.get_sep_cleaned_doc(cmp_doc)
        else:           # compare for missing separator
            ref_doc = self.get_sep_cleaned_doc(ref_doc + SEP)
            cmp_doc = self.get_sep_cleaned_doc(cmp_doc + SEP)
        ref_dps = self.get_keys(ref_doc, "reference")
        cmp_dps = self.get_keys(cmp_doc, "comparison")
        if ref_dps is not None and cmp_dps is not None:
            if sorted(cmp_dps) == sorted(ref_dps):
                a = {"mod": mod, "ref": ref_doc, "cmp": cmp_doc}
                cr = CompareResult(a)
        ref_dps = [] if ref_dps is None else ref_dps
        cmp_dps = [] if cmp_dps is None else cmp_dps
        self.print_compare_result(ref_doc, cmp_doc, ref_dps, cmp_dps, cr)
        return cr

    def fields(self, ref_doc, cmp_doc):
        """
        Returns 'CompareResult' if two given documents with yaml frontmatter
        containing the same data points else 'None' is returned.
        It will be tried to assume the markdown part as yaml part
        if compare failed to allow a compare,
        even if a separator is missing.
        """
        same = self.determin_same_fields(False, ref_doc, cmp_doc)
        if not same:
            same = self.determin_same_fields(True, ref_doc, cmp_doc)
        return same
