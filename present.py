#!/usr/bin/env python

from __future__ import print_function

import os
import shutil
import sys


# Directory in which to store presentation data.
PRESENT_DIR_NAME = os.environ.get('PRESENT_DIR')
PRESENT_DIR_NAME = PRESENT_DIR_NAME if PRESENT_DIR_NAME else '.present'

# Scratch file to save presentation state.
SCRATCH_FILE_NAME = '.scratch'

USER_HOME_DIR = os.path.expanduser('~')

PRESENT_DIR_PATH = os.path.join(USER_HOME_DIR, PRESENT_DIR_NAME)
SCRATCH_FILE_PATH = os.path.join(PRESENT_DIR_PATH, SCRATCH_FILE_NAME)

USAGE_TEXT = '''
usage: present file name [start]
       present [-hrs]
'''.strip()

HELP_TEXT = '''
present is a tool for presenting command line tasks.

To start a presentation, run:
  present file name [start]
where:
  'file'  is the presentation file to use.
  'name'  is the name of the presentation.
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
    '''

    @staticmethod
    def write(pres):
        ''' Write data to the scratch file. '''
        with open(SCRATCH_FILE_PATH, 'w') as scratch:
            content = '\n'.join([pres.name, pres.path, str(pres.start),
                                 str(pres.current)])
            scratch.write(content)

    @staticmethod
    def read():
        ''' Read data from the scratch file. '''
        with open(SCRATCH_FILE_PATH, 'r') as scratch:
            lines = [line.strip() for line in scratch.readlines()]
        name = lines[0]
        path = lines[1]
        start = int(lines[2])
        current = int(lines[3])
        return Presentation(name, path, start, current)


class Presentation(object):
    ''' Wrapper around a presentation file. '''

    def __init__(self, name, path, start, current):
        # Presentation metadata.
        self.name = name
        self.path = path
        self.start = start
        self.current = current

        # Read in presentation data.
        with open(os.path.join(PRESENT_DIR_PATH, path), 'r') as src:
            lines = [line.strip() for line in src.readlines()]

        # Process the lines, removing blanks and comments.
        self.lines = [line for line in lines if len(line) > 0 and line[0] != '#']

    @staticmethod
    def load():
        ''' Load a presentation from the scratch file. '''
        return Scratch.read()

    @staticmethod
    def new(name, path, start):
        ''' Start a presentation from passed arguments. '''
        shutil.copy(path, PRESENT_DIR_PATH)
        presentation = Presentation(name, os.path.basename(path), start, start)
        return presentation

    def next(self):
        ''' Move forward one line in the presentation. '''
        if self.current < len(self.lines):
            self.current += 1

    def prev(self):
        ''' Move back one line in the presentation. '''
        if self.current > -1:
            self.current -= 1

    def get(self):
        ''' Get the current line of the presentation. '''
        if self.current >= len(self.lines) or self.current < 0:
            return ''
        return self.lines[self.current]

    def status(self):
        ''' Generate a message on the current status of the presentation. '''
        # Since next() is always called before calling get(), we need to
        # artificially call next() here and then go back after calling get().
        self.next()
        line = self.get()
        self.prev()

        if self.current == self.start:
            return 'At start of \'{}\':\n {}'.format(self.name, line)
        elif self.current + 1 == len(self.lines):
            return 'At end of \'{}\'.'.format(self.name)
        else:
            return 'Presenting \'{}\' at line {}:\n {}'.format(self.name,
                                                               self.current + 1,
                                                               line)

    def reset(self):
        ''' Reset the presentation back to the beginning. '''
        self.current = self.start

    def save(self):
        ''' Save the current state of the presentation back to a scratch file. '''
        Scratch.write(self)


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
        if len(args) < 2:
            print(USAGE_TEXT)
            return

        # Parse args.
        path = os.path.realpath(os.path.expanduser(args[0]))
        name = args[1]
        start = (int(args[2]) if len(args) > 2 else 0) - 1

        if os.path.isfile(path):
            # Remove existing files from the $PRESENT dir.
            for f in os.listdir(PRESENT_DIR_PATH):
                os.remove(os.path.join(PRESENT_DIR_PATH, f))

            Presentation.new(name, path, start).save()
        else:
            print('Error: No such file: \'{}\'.'.format(path))
            return 1

if __name__ == '__main__':
    main(sys.argv[1:])
