# -*- coding: <utf-8>
# external
import yaml
# logging
import logging
logger = logging.getLogger(__file__)

KEY_MARKDOWN = "markdown"

SEPS = "---\n"
SEP = "\n---\n"


class ValidationResult(object):
    """
    Class to hold data from validation process.
    """

    def __init__(self, kwargs):
        # flag for general validation
        self.valid = kwargs.get("valid", False)
        # flag for modified documents (added separetor)
        self.mod = kwargs.get("mod", False)
        # document which was used as reference
        self.ref = kwargs.get("ref", "")
        # document which was used as sample
        self.cmp = kwargs.get("cmp", "")


class DocumentTransform(object):
    """
    General idea:
    A markdown document with yaml frontmatter can be stored
    as a dictionary with datapoints as key-value pairs and
    an additional key-value-pair for markdown plain text.
    This class provides functions to convert
    markown documents with yaml frontmatter
    into dictionaries and backwards.
    Markdown text will be stored in field 'markdown'.
    So be sure that you do not use this field in your yaml frontmatter.
    """

    def split_document(self, document):
        """
        Returns document separated in yaml and markdown data.
        Following rules will be applied:
            1.) --- txt1 --- ... --- txtn+1     => yaml=txt1+txtn, md=txtn+1
            2.) --- txt1 --- txt2               => yaml=txt1, md=txt2
            3.) txt1 --- txt2                   => yaml=txt1, md=txt2
            4.) --- txt                         => yaml='', md=txt
            5.) txt                             => yaml=txt, md=''
        """
        yaml_data, md_text = "", ""
        # add chars to ensure common separator search pattern
        document = "\n" + document + "\n"
        sections = document.split(SEP)
        if len(sections) == 0:          # 5.)
            yaml_data = document.strip()
            md_text = ""
        else:                           # 1.) to 4.)
            md_text = sections.pop(-1).strip()
            yaml_data = "\n".join(sections).strip()
        return [yaml_data, md_text]

    def get_sep_cleaned_doc(self, document):
        [yaml_data, md_text] = self.split_document(document)
        if len(yaml_data) > 0:
            doc = SEPS + yaml_data + SEP + md_text
        else:
            doc = SEPS + SEPS + md_text
        return doc

    def to_doc(self, dict_to_transform):
        """
        Converts a dictionary to a markdown document with yaml frontmatter.
        """
        md_txt = dict_to_transform.pop(KEY_MARKDOWN, "")
        yaml_data = yaml.dump(
            dict_to_transform,
            default_flow_style=False,
            allow_unicode=True
        )
        frontmatter = ""
        if not yaml_data == "{}\n":
            frontmatter = "---\n" + yaml_data + "---\n"
        return frontmatter + md_txt

    def to_dict(self, doc_to_transform):
        """
        Converts a markown document with yaml frontmatter into a dictionary.
        """
        [yaml_data, md_text] = self.split_document(doc_to_transform)
        doc_dict = {}
        if len(yaml_data) > 1:
            for doc_dp in yaml.load_all(yaml_data):
                if isinstance(doc_dp, dict):
                    doc_dict.update(doc_dp)
                elif doc_dp is not None and len(doc_dp) > 0:
                    md_text = doc_dp + "\n" + md_text
        assert KEY_MARKDOWN not in doc_dict.keys(), \
            "Yaml data key '" + str(KEY_MARKDOWN) + "' is not allowed!"
        doc_dict.update({KEY_MARKDOWN: md_text})
        return doc_dict

    def valid_fields(self, ref_doc_origin, cmp_doc_origin):
        """
        Returns 'ValidationResult' if two given documents with yaml frontmatter
        containing the same keys else 'None'.
        This function also tries to assume the markown part as yaml data part
        to allow a validation, even if separator is missing.
        """
        def get_keys(doc, name):
            try:
                keys = self.to_dict(doc).keys()
            except Exception as err:
                logger.error("Error '" + str(err) + "' occured "
                             + "during parsing of " + name + ": "
                             + str(doc))
                return None
            return keys

        def determin_valid(mod):
            nonlocal ref_doc_origin, cmp_doc_origin, refs, cmps, valid
            if not mod:     # causual validation
                ref_doc, cmp_doc = ref_doc_origin, cmp_doc_origin
            else:           # validation for missing separator
                ref_doc, cmp_doc = ref_doc_origin + SEP, cmp_doc_origin + SEP
            ref_doc = self.get_sep_cleaned_doc(ref_doc)
            cmp_doc = self.get_sep_cleaned_doc(cmp_doc)
            refs = get_keys(ref_doc, "reference")
            cmps = get_keys(cmp_doc, "comparison")
            if refs is not None and cmps is not None:
                if sorted(cmps) == sorted(refs):
                    valid = ValidationResult({
                        "valid": True,
                        "mod": mod,
                        "ref": ref_doc,
                        "cmp": cmp_doc
                    })
        valid = None
        refs, cmps = [], []
        determin_valid(mod=False)
        if not valid:
            determin_valid(mod=True)
        op = " == " if valid else " != "
        refs = [] if refs is None else refs
        cmps = [] if cmps is None else refs
        res_txt = str(sorted(refs)) + op + str(sorted(cmps))
        ref_txt = "\nReference:\n" + str(ref_doc_origin)
        cmp_txt = "\nComparison:\n" + str(ref_doc_origin)
        logger.debug("Data field compare: " + res_txt + ref_txt + cmp_txt)
        return valid
