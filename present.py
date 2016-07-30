#!/usr/bin/env python

from __future__ import print_function

import sys
import os

# take args, write to the scratch file

# present <file> [start]
#
# present --next
# present --prev
# present --get

# Scratch file format:
#   presentation_file_name
#   starting position (line number)
#   current position

# Directory in which to store presentation data.
PRESENT_DIR_NAME = '.present'

# Scratch file to save presentation state.
SCRATCH_FILE_NAME = '.scratch'

USER_HOME_DIR = os.path.expanduser('~')

PRESENT_DIR_PATH = os.path.join(USER_HOME_DIR, PRESENT_DIR_NAME)
SCRATCH_FILE_PATH = os.path.join(PRESENT_DIR_PATH, SCRATCH_FILE_NAME)

class Scratch(object):
    ''' Wrapper around the presentation scratch file. '''
    def __init__(self, file_path):
        self.file_path = file_path # TODO rename to path

    def write(self, presentation_file, start, current):
        ''' Write data to the scratch file. '''
        with open(self.file_path, 'w') as scratch:
            scratch.write(presentation_file)
            scratch.write('\n')
            scratch.write(start)
            scratch.write('\n')
            scratch.write(current)

    def read(self):
        ''' Read data from the scratch file. '''
        with open(self.file_path, 'r') as scratch:
            lines = scratch.readlines()
        presentation_file = lines[0].strip()
        start = lines[1].strip()
        current = lines[2].strip()
        return presentation_file, start, current

    def new(self, presentation_file, start):
        ''' Initialize a new presentation. '''
        self.write(presentation_file, start, start)

    def reset(self):
        ''' Reset the presentation back to the start. '''
        presentation_file, start, current = self.read()
        if start == current:
            return
        self.new(presentation_file, start)

    def next(self):
        ''' Move the presentation to the next line. '''
        presentation_file, start, current = self.read()
        current = str(int(current) + 1)
        self.write(presentation_file, start, current)

    def prev(self):
        ''' Move the presentation back to the previous line. '''
        presentation_file, start, current = self.read()
        current = str(int(current) - 1)
        self.write(presentation_file, start, current)

class Presentation(object):
    ''' Wrapper around a presentation file. '''
    def __init__(self, path, start, current):
        self.path = path
        self.start = start
        self.current = current

    @staticmethod
    def from_scratch():
        ''' Initialize a presentation from a scratch file. '''
        scratch = Scratch(SCRATCH_FILE_PATH)
        presentation_file, start, current = scratch.read()
        return Presentation(presentation_file, start, current)

    @staticmethod
    def from_args(path, start):
        ''' Initialize a presentation from passed arguments. '''
        scratch = Scratch(SCRATCH_FILE_PATH)
        scratch.write(path, start, start)
        return Presentation(path, start, start)

    def read_line_at(self, line_number):
        ''' Read the line of the presentation at the specified line number. '''
        line_number = int(line_number)
        with open(self.path, 'r') as presentation:
            lines = presentation.readlines()
        return lines[line_number].strip()

    def copy(self):
        ''' Copy the presentation into the present directory. '''
        with open(self.path, 'r') as src:
            data = src.read()
        with open(os.path.join(PRESENT_DIR_PATH, self.path), 'w') as dest:
            dest.write(data)

def main(args):
    scratch = Scratch(SCRATCH_FILE_PATH)

    if len(args) == 0:
        presentation_file, start, current = scratch.read()
        current_line = read_current_line(presentation_file, current)
        if start == current:
            print('At start of \'{}\':\n > {}'
                    .format(presentation_file, current_line))
        else:
            print('Presenting \'{}\' at line {}:\n > {}'
                    .format(presentation_file, current, current_line))
        return

    if args[0] == '--next':
        scratch.next()
    elif args[0] == '--prev':
        scratch.prev()
    elif args[0] == '--get':
        presentation_file, _, current = scratch.read()
        current_line = read_current_line(presentation_file, current)
        print(current_line)
    elif args[0] == '--reset':
        scratch.reset()
    else:
        presentation_file = args[0]
        start = args[1] if len(args) > 1 else '0'

        scratch.new(presentation_file, start)
        copy_presentation(presentation_file)

if __name__ == '__main__':
    main(sys.argv[1:])
