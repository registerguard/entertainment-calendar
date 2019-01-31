import argparse

# events_register_guard_template_no_description.txt
# https://github.com/newsdev/fec2json/blob/master/utils/process_filing.py

def process_file(path):
    with open(path, 'r') as f:
        dirty_copy = f.read()
        return dirty_copy

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', help='path to the file we want to fix')
    args = parser.parse_args()
    output = process_file(args.path)
    sys.stdout.write(output)

if __name__=='__main__':
    main()
