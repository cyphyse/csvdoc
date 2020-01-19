# -*- coding: <utf-8>
# external
import re
import json
import datetime
import dateutil.parser as dtp
# logging
import logging
logger = logging.getLogger(__name__)

ISO8601_DATETIME_PATTERN = "\d{4}[\-]\d{1,2}[\-]\d{1,2}T\d{1,2}:\d{1,2}"


def converter(function):

    def wrapper(self, data):
        logger.debug(function.__name__ + " in: " + str(data))
        try:
            data = function(self, data)
        except Exception as err:
            logger.debug(err)
        logger.debug(function.__name__ + " out: " + str(data))
        return data
    return wrapper


class CellFormatConvert():
    def __init__(self):
        pass

# ------------------------------------------------------------------------------
    @converter
    def stringlist_to_py(self, data):
        if isinstance(data, str) and len(data) >= 2:
            stringlist = None
            if data[0] == "[" and data[-1] == "]":
                stringlist = data[1:-1]
            if data[1] == "[" and data[-2] == "]":
                stringlist = data[2:-3]
            if stringlist is not None:
                logger.debug("Stringlist to py in: " + str(data))
                list_v1 = stringlist.split(',')
                list_v2 = stringlist.split(';')
                if len(list_v2) > len(list_v1):
                    parse = list_v2
                else:
                    parse = list_v1
                data = []
                for entry in parse:
                    data.append(entry.strip(" '\""))
        logger.debug("Stringlist to py out: " + str(data))
        return data

    @converter
    def stringlist_to_db(self, data):
        if isinstance(data, list) and len(data) > 2:
            data = str(data)
        return data

# ------------------------------------------------------------------------------
    @converter
    def number_to_py(self, data):
        if isinstance(data, str) and len(data) > 0:
            if data.isdigit():
                data = int(data)
            else:
                data = float(data)
        return data

    @converter
    def number_to_db(self, data):
        if isinstance(data, float) or isinstance(data, int):
            data = str(data)
        return data

# ------------------------------------------------------------------------------
    @converter
    def json_to_py(self, data):
        if isinstance(data, str) and len(data) > len("{\"0\":0}"):
            data = json.loads(data)
        return data

    @converter
    def json_to_db(self, data):
        if isinstance(data, dict):
            data = json.dumps(data)
        return data

# ------------------------------------------------------------------------------
    @converter
    def date_to_py(self, data):
        if isinstance(data, str):
            if re.match(ISO8601_DATETIME_PATTERN, data):
                data = dtp.parse(data)
        return data

    @converter
    def date_to_db(self, data):
        if isinstance(data, datetime.datetime):
            data = data.isoformat()
        return data


class CellFormat():
    def __init__(self, **kwargs):
        self.repr = CellFormatConvert()
        self.to_py_fcn = [
            self.repr.stringlist_to_py,
            self.repr.number_to_py,
            self.repr.json_to_py,
            self.repr.date_to_py
        ]
        self.to_db_fcn = [
            self.repr.date_to_db,
            self.repr.json_to_db,
            self.repr.number_to_db,
            #self.repr.stringlist_to_db,
        ]

# ------------------------------------------------------------------------------
    def entry_to_py(self, entry):
        logger.debug("Entry to py")
        return self.convert_entry(entry, self.to_py_fcn)

    def entry_to_db(self, entry):
        logger.debug("Entry to db")
        return self.convert_entry(entry, self.to_db_fcn)

    def convert_entry(self, entry, fcns):
        for fcn in fcns:
            try:
                new = fcn(entry)
                if not new == entry:
                    """Ready if one function has converted"""
                    entry = new
                    break
            except Exception as err:
                txt = "Conversion error '" + str(err) + "'"
                txt += " in function \'" + fcn.__name__ + "\'"
                txt += " with entry \'" + str(entry) + "\'"
                raise Exception(txt)
        return entry

# ------------------------------------------------------------------------------
    def doc_to_py(self, doc):
        logger.debug("Document to py")
        return self.convert_doc(doc, self.entry_to_py)

    def doc_to_db(self, doc):
        logger.debug("Document to db")
        return self.convert_doc(doc, self.entry_to_db)

    def convert_doc(self, doc, fcn):
        for k, v in doc.items():
            if isinstance(v, dict):
                doc[k] = self.convert_doc(v, fcn)
            else:
                doc[k] = fcn(v)
        return doc

# ------------------------------------------------------------------------------
    def df_to_py(self, df):
        return df.applymap(self.entry_to_py)

    def df_to_db(self, df):
        return df.applymap(self.entry_to_db)

# ------------------------------------------------------------------------------
    def records_to_py(self, record):
        logger.debug("Records to py ...")
        return self.convert_record(record, self.doc_to_py)

    def records_to_db(self, record):
        logger.debug("Records to db ...")
        return self.convert_record(record, self.doc_to_db)

    def convert_record(self, record, fcn):
        for idx, doc in enumerate(record):
            record[idx] = fcn(doc)
        return record
