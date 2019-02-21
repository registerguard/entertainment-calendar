import argparse
import re
import sys

# events_register_guard_template_no_description.txt
# https://github.com/newsdev/fec2json/blob/master/utils/process_filing.py

def clean_whole_thing(dirty):
    cleaned = dirty

    # compile the regexes, just 'cause
    eugene_zips = re.compile(r', Eugene, 974\d\d')
    other_zips = re.compile(r', \d{5}(\.)$', re.MULTILINE)
    am_pm_inline = re.compile(r'(\d) ([a|p])m([^\.])')
    am_pm_end_of_sentence = re.compile(r'(\d) ([a|p])m\.')
    hult_center = re.compile(r'(1|One) Eugene Center')
    street_end = re.compile(r'Street\.$', re.MULTILINE)
    avenue_end = re.compile(r'Avenue\.$', re.MULTILINE)
    directional = re.compile(r'(\d) ([NESW])(orth|ast|outh|est) ')

    # straight-up replace
    cleaned = cleaned.replace(u':00', u'')
    cleaned = cleaned.replace(u'\n\n', u'\n')
    cleaned = cleaned.replace(u'-', u'—')
    # regexes
    cleaned = eugene_zips.sub(u'', cleaned)
    cleaned = other_zips.sub(u'\\1', cleaned)
    cleaned = am_pm_inline.sub(u'\\1 \\2.m.\\3', cleaned)
    cleaned = am_pm_end_of_sentence.sub(u'\\1 \\2.m.', cleaned)
    cleaned = hult_center.sub(u'Seventh Avenue and Willamette Street', cleaned)
    cleaned = street_end.sub(u'St.', cleaned)
    cleaned = avenue_end.sub(u'Ave.', cleaned)
    cleaned = directional.sub(u'\\1 \\2. ', cleaned)
    
    # back to a straight-up replace, 'cause order of things
    cleaned = cleaned.replace(u'12 p.m.', 'noon')
    cleaned = cleaned.replace(u'12 a.m.', 'midnight')

    return cleaned

def process_file(path):
    with open(path, 'r') as f:
        dirty_copy = f.read()
        return clean_whole_thing(dirty_copy)

def main():
    # argparse!
    # https://towardsdatascience.com/learn-enough-python-to-be-useful-argparse-e482e1764e05
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', help='path to the file we want to fix')
    args = parser.parse_args()
    output = process_file(args.path)
    sys.stdout.write(output)

if __name__=='__main__':
    main()
