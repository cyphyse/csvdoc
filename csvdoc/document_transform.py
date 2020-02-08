# -*- coding: <utf-8>
# external
import yaml
# logging
import logging
logger = logging.getLogger(__file__)

KEY_MARKDOWN = "markdown"

SEPS = "---\n"
SEP = "\n---\n"


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
            4.) txt ---                         => yaml=txt, md=''
            5.) --- txt                         => yaml='', md=txt
            6.) txt                             => yaml=txt, md=''
        """
        yaml_data, md_text = "", ""
        # ensure common line brakes
        document = document.replace("\r\n", "\n")
        # add chars to ensure common separator search pattern
        document = "\n" + document + "\n"
        # replace doubled seperator
        while SEP + SEPS in document:
            document = document.replace(SEP + SEPS, SEP)
        sections = document.split(SEP)
        if len(sections) == 0:          # 6.)
            yaml_data = document.strip()
            md_text = ""
        else:                           # 1.) to 5.)
            md_text = sections.pop(-1).strip()
            yaml_data = "\n".join(sections).strip()
        return [yaml_data, md_text]

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
