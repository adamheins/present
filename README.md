# present
A command line presentation tool using the zsh line editor (zle).

## Why?
The tool essentially provides an easy way to keep track of a sequence of
terminal commands.

Let's say I want to give a demonstration of a new command line tool I've
written. Naturally, I want to show off a lot of functionality of my tool, so
I'm going to be running it a bunch of times with different combinations of
arguments. That sounds like both a pain to remember and a pain to type while a
bunch of people are watching. Am I the only one who is way worse at typing when
someone else is watching?

This is where **present** comes in. I can record the commands I want to use in
presentation file, and then easily navigate through them during the
presentation without having to type. Easy.

## Requirements
The tool is written in Python, so you're going to need that. Works with recent
versions of both Python 2 and 3.

Since this tool uses the zsh line editor, you must be using zsh as your shell.

## Setup
Clone this git repository, then run:
```
sudo ./install.sh
source present.zsh
```
Add the `source present.zsh` line to your .zshrc if you don't want to have to
do it every time you start a new shell.

## Usage
To start a presentation, run:
```
present <file> [start]
```
where `<file>` is the presentation file you want to use. Optionally, you can
specify `[start]`, which is the line number that marks the start of the
presentation. If not specified, this defaults to the first line of the file.

To navigate through the presentation, use the key bindings provided by
present.zsh. By default, these are Ctrl-O to advance and Ctrl-L to go back.

Other commands are:
```
-h, --help    Print help message.
-r, --reset   Reset the current presentation to the beginning.
-s, --status  Print the status of the current presentation.
```

### Presentation Files
Presentation files are essentially just lists of terminal commands that you
want to show up at your prompt, one per line. Blank lines and lines starting
with a '#' are ignored.

## License
MIT license. See the LICENSE file.
