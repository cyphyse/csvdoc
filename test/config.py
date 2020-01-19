# -*- coding: <utf-8>
import logging
logging.basicConfig(level=logging.DEBUG)

HYBRID_DATABASE_NAME = ["test_in.csv"]

# TODO: Create a Test Suite and run both variants
TEST_VARIANT = 1

if TEST_VARIANT == 1:
    yaml_data = ""
    yaml_data += "---\n"
    yaml_data += "a: 1\nb: 2\nc: 3\ndate: 2019-12-01T12:30\ntext: Hello World!\n"
    yaml_data += "---\n"
    md_text = "This is a markdown text"
    md_text += " with a few UTF-8 chars like .,;:äüöß%&"
    md_text += "\nand also a line break."

if TEST_VARIANT == 2:
    yaml_data = ""
    yaml_data += "---\n"
    yaml_data += "---\n"
    md_text = "This is a markdown text"
    md_text += " with a few UTF-8 chars like .,;:äüöß%&"
    md_text += "\nand also a line break."

# test step counter for printing
cnt_step = 1

def disp(step, result):
    """Function to provide a clean output"""
    global cnt_step
    if cnt_step == 1:
        print()
        print("-"*70)
        print("-"*70)
    print(str(cnt_step) + ". " + step)
    print("-"*70)
    print(result)
    print("-"*70)
    cnt_step += 1
