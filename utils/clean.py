#! /usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import re
import sys

# The file argument is generally going to be:
# events_register_guard_template_no_description.txt
# 
# In general, the layout of this app inspired by:
# https://github.com/newsdev/fec2json/blob/master/utils/process_filing.py

def title_it(matchobj):
        return matchobj.group(0).title()

def clean_whole_thing(dirty):
    cleaned = dirty.decode('utf-8')

    # compile the regexes, just 'cause
    eugene_zips = re.compile(r', Eugene, 974\d\d')
    other_zips = re.compile(r', \d{5}(\.) ')
    am_pm_inline = re.compile(r'(\d) ([a|p])m([^\.])')
    am_pm_end_of_sentence = re.compile(r'(\d) ([a|p])m\.')
    hult_center = re.compile(r'(1|One) Eugene Center')
    street_end = re.compile(r' Street\.')
    street_mid = re.compile(r' Street,')
    avenue_end = re.compile(r' Avenue\.')
    avenue_mid = re.compile(r' Avenue,')
    phone_no = re.compile(r'( \d{3}) ?(\d{3}) ?(\d{4})([\.\,])')
    directional = re.compile(r'(\d) ([NESW])(orth|ast|outh|est) ')
    all_caps = re.compile(r'([A-Z]{3}[A-Z]+)') #Three or more all caps
    # This is just the start of this one.
    # Currently turns "Weekday, Month Date, Year" => "Weekday, Month Date"
    # but later will have to also abbreviate the month AP Style 
    date_style = re.compile(r'^(\w+, \w+ \d{1,2}), \d{4}$', re.MULTILINE)

    # straight-up replace
    cleaned = cleaned.replace(u':00', u'')
    cleaned = cleaned.replace(u'\n\n', u'\n')
    cleaned = cleaned.replace(u' - ', u' — ')
    # turns out CND scripts really prefer ':' to '—'
    cleaned = cleaned.replace(u' — ', u': ')

    # regexes
    cleaned = eugene_zips.sub(u'', cleaned)
    cleaned = other_zips.sub(u'. ', cleaned)
    cleaned = am_pm_inline.sub(u'\\1 \\2.m.\\3', cleaned)
    cleaned = am_pm_end_of_sentence.sub(u'\\1 \\2.m.', cleaned)
    cleaned = hult_center.sub(u'Seventh Avenue and Willamette Street', cleaned)
    cleaned = street_end.sub(u' St.', cleaned)
    cleaned = street_mid.sub(u' St.,', cleaned)
    cleaned = avenue_end.sub(u' Ave.', cleaned)
    cleaned = avenue_mid.sub(u' Ave.,', cleaned)
    cleaned = phone_no.sub(u'\\1-\\2-\\3\\4', cleaned)
    cleaned = directional.sub(u'\\1 \\2. ', cleaned)
    cleaned = all_caps.sub(title_it, cleaned) # function makes changes to backreference
    cleaned = date_style.sub(u'\\1', cleaned)

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
    parser.add_argument('path', help='path to the file we want to fix')
    args = parser.parse_args()
    output = process_file(args.path)
    sys.stdout.write(output)

if __name__ == '__main__':
    main()
