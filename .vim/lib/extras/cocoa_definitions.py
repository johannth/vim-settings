#!/usr/bin/python
'''Creates a folder containing text files of Cocoa keywords.'''
import os, commands, re
from sys import argv

def find(searchpath, ext):
    '''Mimics the "find searchpath -name *.ext" unix command.'''
    results = []
    for path, dirs, files in os.walk(searchpath):
        for filename in files:
            if filename.endswith(ext):
                results.append(os.path.join(path, filename))
    return results

def find_headers(frameworks):
    '''Returns list of the header files for the given frameworks.'''
    headers = []
    for framework in frameworks:
        headers.extend(find('/System/Library/Frameworks/%s.framework'
                            % framework, '.h'))
    return headers

def default_headers():
    '''Headers for common Cocoa frameworks.'''
    frameworks = ('Foundation', 'AppKit', 'AddressBook', 'CoreData',
                  'PreferencePanes', 'QTKit', 'ScreenSaver', 'SyncServices',
                  'WebKit')
    return find_headers(frameworks)

def match_output(command, regex, group_num):
    '''
    Returns an ordered list of all matches of the supplied regex for the
    output of the given command.
    '''
    results = []
    for line in commands.getoutput(command).split("\n"):
        match = re.search(regex, line)
        if match and not match.group(group_num) in results:
            results.append(match.group(group_num))
    results.sort()
    return results

def get_functions(header_files):
    '''Returns list of Cocoa Functions.'''
    lines = match_output(r"grep -h '^[A-Z][A-Z_]* [^;]* \**NS\w\+ *(' "
                         + header_files, r'NS\w+\s*\(.*?\)', 0)
    for i in range(len(lines)):
        lines[i] = lines[i].replace('NSInteger', 'int')
        lines[i] = lines[i].replace('NSUInteger', 'unsigned int')
        lines[i] = lines[i].replace('CGFloat', 'float')
    return lines

def get_types(header_files):
    '''Returns a list of Cocoa Types.'''
    return match_output(r"grep -h 'typedef .* _*NS[A-Za-z]*' "
                          + header_files, r'(NS[A-Za-z]+)\s*(;|{)', 1)

def get_constants(header_files):
    '''Returns a list of Cocoa Constants.'''
    return match_output(r"awk '/^(typedef )?enum .*\{/ {pr = 1;} /\}/ {pr = 0;}"
                        r"{ if(pr) print $0; }' " + header_files,
                        r'^\s*(NS[A-Z][A-Za-z0-9_]*)', 1)

def get_notifications(header_files):
    '''Returns a list of Cocoa Notifications.'''
    return match_output(r"grep -h '\*NS.*Notification' "
                        + header_files, r'NS\w*Notification', 0)

def write_file(filename, lines):
    '''Attempts to write list to file or exits with error if it can't.'''
    try:
        f = open(filename, 'w')
    except IOError, error:
        raise SystemExit(argv[0] + ': %s' % error)
    f.write("\n".join(lines))
    f.close()

def extract_files_to(dirname=None):
    '''Extracts .txt files to given directory or ./cocoa_indexes by default.'''
    if dirname is None:
        dirname = './cocoa_indexes'
    if not os.path.isdir(dirname):
        os.mkdir(dirname)
    headers = ' '.join(default_headers())

    write_file(dirname + '/functions.txt',     get_functions    (headers))
    write_file(dirname + '/types.txt',         get_types        (headers))
    write_file(dirname + '/constants.txt',     get_constants    (headers))
    write_file(dirname + '/notifications.txt', get_notifications(headers))

if __name__ == '__main__':
    extract_files_to(argv[1] if len(argv) > 1 else None)
