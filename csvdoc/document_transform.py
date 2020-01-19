# -*- coding: <utf-8>
# external
import yaml
# logging
import logging
logger = logging.getLogger(__file__)

KEY_MARKDOWN = "markdown"


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
        lines = doc_to_transform.splitlines()
        yaml_data = ""
        md_text = ""
        read_header = True
        for idx, line in enumerate(lines):
            if idx == 0 and line == "---":
                continue
            if idx > 0 and line == "---":
                read_header = False
                continue
            line_break = "\n"
            last_line = idx == len(lines)-1
            if last_line:
                line_break = ""
            if read_header:
                yaml_data += line + line_break
            else:
                md_text += line + line_break
        # did not found a separator
        if read_header:
            md_text = yaml_data
            yaml_data = ""
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


    def valid_fields(self, ref_doc, cmp_doc):
        """
        Return true if two given documents with yaml frontmatter
        containing the same keys.
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
        valid = False
        # preprocess (froce to try to compare)
        if not "\n---" in ref_doc:
            ref_doc += "\n---"
        if not "\n---" in cmp_doc:
            cmp_doc += "\n---"
        refs = get_keys(ref_doc, "reference")
        cmps = get_keys(cmp_doc, "comparison")
        if refs is not None and cmps is not None:
            valid = sorted(cmps) == sorted(refs)
        op = " == " if valid else " != "
        if refs is None:
            refs = []
        if cmps is None:
            cmps = []
        logger.debug("Data field compare"
                     + str(sorted(refs)) + op + str(sorted(cmps))
                     + "\nReference:\n" + str(ref_doc)
                     + "\nComparison:\n" + str(cmp_doc))
        return valid
