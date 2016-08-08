#!/usr/bin/env python

from __future__ import print_function

import sys
import os


# Directory in which to store presentation data.
PRESENT_DIR_NAME = os.environ.get('PRESENT_DIR')
PRESENT_DIR_NAME = PRESENT_DIR_NAME if PRESENT_DIR_NAME else '.present'

# Scratch file to save presentation state.
SCRATCH_FILE_NAME = '.scratch'

USER_HOME_DIR = os.path.expanduser('~')

PRESENT_DIR_PATH = os.path.join(USER_HOME_DIR, PRESENT_DIR_NAME)
SCRATCH_FILE_PATH = os.path.join(PRESENT_DIR_PATH, SCRATCH_FILE_NAME)

USAGE_TEXT = '''
usage: present file [start]
       present [-hrs]
'''.strip()

HELP_TEXT = '''
present is a tool for presenting command line tasks.

To start a presentation, run:
  present file [start]
where:
  'file'  is the presentation file to use.
  'start' is the line number (zero-indexed) to start the presentation from.
          Default is 0.

When a presentation is already running, the following commands can be used:
  -h, --help    Print this help message.
  -r, --reset   Reset the presentation to the beginning.
  -s, --status  Print the current status of the presentation.
'''.strip()


class Scratch:
    ''' Wrapper around the presentation scratch file.

        Scratch file format:
         1 presentation_file_name
         2 starting position (line number)
         3 current position (line number)
         4 direction
    '''

    @staticmethod
    def write(presentation_file, start, current, direction):
        ''' Write data to the scratch file. '''

        with open(SCRATCH_FILE_PATH, 'w') as scratch:
            content = '{}\n{}\n{}\n{}'.format(presentation_file, start, current,
                                              direction)
            scratch.write(content)

    @staticmethod
    def read():
        ''' Read data from the scratch file. '''
        with open(SCRATCH_FILE_PATH, 'r') as scratch:
            lines = [line.strip() for line in scratch.readlines()]
        presentation_file = lines[0]
        start = int(lines[1])
        current = int(lines[2])
        direction = lines[3]
        return presentation_file, start, current, direction


class Presentation(object):
    ''' Wrapper around a presentation file. '''

    DIRECTION_NEXT = '0'
    DIRECTION_PREV = '1'

    def __init__(self, path, start, current, direction):
        # Presentation metadata.
        self.path = path
        self.start = start
        self.current = current
        self.direction = direction

        # Read in presentation data.
        with open(path, 'r') as src:
            lines = [line.strip() for line in src.readlines()]

        # Process the lines, removing blanks and comments.
        self.lines = [line for line in lines if len(line) > 0 and line[0] != '#']

    @staticmethod
    def load():
        ''' Load a presentation from the scratch file. '''
        presentation_file, start, current, direction = Scratch.read()
        return Presentation(presentation_file, start, current, direction)

    @staticmethod
    def new(path, start):
        ''' Start a presentation from passed arguments. '''
        presentation = Presentation(path, start, start,
                                    Presentation.DIRECTION_NEXT)

        # Copy the presentation to the '.present' directory.
        dest_path = os.path.join(PRESENT_DIR_PATH, path)
        with open(path, 'r') as src:
            data = src.read()
        with open(dest_path, 'w') as dest:
            dest.write(data)

        return presentation

    def bound(self):
        ''' Bound the current position within permissible limits. '''
        if self.current < -1:
            self.current = -1
        elif self.current > len(self.lines):
            self.current = len(self.lines)

    def next(self):
        ''' Move forward one line in the presentation. '''
        if self.direction == Presentation.DIRECTION_PREV:
            self.current += 1
        else:
            self.current += 1
        self.bound()
        self.direction = Presentation.DIRECTION_NEXT

    def prev(self):
        ''' Move back one line in the presentation. '''
        if self.direction == Presentation.DIRECTION_NEXT:
            self.current -= 1
        else:
            self.current -= 1
        self.bound()
        self.direction = Presentation.DIRECTION_PREV

    def get(self):
        ''' Get the current line of the presentation. '''
        if self.current >= len(self.lines) or self.current < 0:
            return ''
        return self.lines[self.current]

    def status(self):
        ''' Generate a message on the current status of the presentation. '''
        line = self.get()

        if self.start == self.current:
            return 'At start of \'{}\':\n $ {}'.format(self.path, line)
        return 'Presenting \'{}\' at line {}:\n $ {}'.format(self.path,
                                                             self.current,
                                                             line)

    def reset(self):
        ''' Reset the presentation back to the beginning. '''
        self.current = self.start
        self.direction = Presentation.DIRECTION_NEXT

    def save(self):
        ''' Save the current state of the presentation back to a scratch file. '''
        Scratch.write(self.path, self.start, self.current, self.direction)


def main(args):
    if len(args) == 0:
        print(USAGE_TEXT)
        return

    if args[0] in ['-h', '--help']:
        print(HELP_TEXT)
    elif args[0] == '--prev-and-get':
        pres = Presentation.load()
        pres.prev()
        print(pres.get())
        pres.save()
    elif args[0] == '--next-and-get':
        pres = Presentation.load()
        pres.next()
        print(pres.get())
        pres.save()
    elif args[0] in ['-r', '--reset']:
        pres = Presentation.load()
        pres.reset()
        pres.save()
    elif args[0] in ['-s', '--status']:
        print(Presentation.load().status())
    else:
        presentation_file = args[0]
        start = (int(args[1]) if len(args) > 1 else 0) - 1

        if os.path.isfile(presentation_file):
            # Remove existing files from the $PRESENT dir.
            for f in os.listdir(PRESENT_DIR_PATH):
                os.remove(os.path.join(PRESENT_DIR_PATH, f))

            Presentation.new(presentation_file, start).save()
        else:
            print('Error: No such file: \'{}\'.'.format(presentation_file))
            return 1

if __name__ == '__main__':
    main(sys.argv[1:])
