# -*- coding: utf-8 -*-

__author__ = 'itmard'

import sys
import re
import datetime
import time

import click


class SubtitleFixer:
    def __init__(self):
        self.time = '\d\d:\d\d:\d\d,\d\d\d'
        self.number = u'۰۱۲۳۴۵۶۷۸۹'

        self.string = ''

    def fix_encoding(self):
        assert isinstance(self.string, str), repr(self.string)

        try:
            self.string.decode('utf8', 'strict')
            self.string = self.string.decode('utf8')
            return 'utf8'
        except UnicodeError:
            pass

        try:
            self.string.decode('utf16', 'strict')
            self.string = self.string.decode('utf16')
            return 'utf16'
        except UnicodeError:
            pass

        self.string = self.string.decode('windows-1256')
        return 'windows-1256'

    def fix_italic(self):
        self.string = self.string.replace('<i>', '')
        self.string = self.string.replace('</i>', '')

    def fix_arabic(self):
        self.string = self.string.replace(u'ي', u'ی')
        self.string = self.string.replace(u'ك', u'ک')

    def fix_question_mark(self):
        # quistion mark in persina is ؟ not ?
        self.string = self.string.replace('?', u'؟')

    def fix_other(self):
        self.string = self.string.replace(u'\u202B', u'')

        lines = self.string.split('\n')
        string = ''

        for line in lines:
            if re.match('^%s\s-->\s%s$' % (self.time, self.time), line):
                string += line
            elif re.match('^%s\s-->\s%s$' % (self.time, self.time), line[:-1]):
                string += line
            elif line.strip() == '':
                string += line
            elif re.match('^\d+$', line):
                string += line
            elif re.match('^\d+$', line[:-1]):
                string += line
            else:
                # this should be subtitle
                s = re.match('^([\.!?]*)', line)

                try:
                    line = re.sub('^%s' % s.group(), '', line)
                except:
                    pass

                # use persian numbers
                for i in range(0, 10):
                    line = line.replace(str(i), self.number[i])

                # for ltr problems some peoples put '-' on EOL
                # it should be in start
                if len(line) != 0 and line[-1] == '-':
                    line = '- %s' % line[:-1]
                line += s.group()

                # put rtl char in start of line
                # it forces some player to show that line rtl
                string += u'\u202B' + unicode(line)

            # noting to see here
            string += '\n'

            self.string = string

    def decode_string(self, string):
        self.string = string

        self.fix_encoding()

        self.fix_italic()
        self.fix_arabic()
        self.fix_question_mark()
        self.fix_other()

        return self.string


def change_time(hour, minute, second, time_diff):
    """ Changes a time by the amount of seconds specified as time_diff
        Parameters:
            hour: hour value of the time
            minute: minute value
            second: second value
            time_diff: the distance (in seconds) by which to change the time
                       (this can be positive or negative)
    """
    current_time = datetime.datetime(1, 1, 1, hour, minute, second)
    difference = datetime.timedelta(seconds=time_diff)

    try:
        return current_time + difference
    except OverflowError:
        print 'ERROR: Date value out of range.'
        sys.exit()
    except:
        print 'ERROR: Error changing time.'
        return None


def process_time_string(s, time_diff):
    """ Processes a .SRT subtitle time string. Ignores milliseconds.
        Parameters:
            s: the time string. Format: HH:MM:SS,MMS (milliseconds)
            time_diff: the time change to apply (in seconds)

    """

    # Ignore milliseconds
    s = s.split(',')

    # Convert to time object
    dt = time.strptime(s[0], '%H:%M:%S')

    # Apply time difference
    dt = change_time(dt.tm_hour, dt.tm_min, dt.tm_sec, time_diff)

    # Fix formatting for the minutes
    minutes = str(dt.minute)
    seconds = str(dt.second)
    if len(minutes) == 1:
        minutes = '0%s' % (minutes,)
    if len(seconds) == 1:
        seconds = '0%s' % (seconds,)

    new_time_string = '0%s:%s:%s,%s' % (str(dt.hour), minutes, seconds, s[1])
    return new_time_string


def is_time_string(s):
    """ Determines if a string 's' is an SRT file time string
        Format: HH:MM:SS,MMS --> HH:MM:SS,MMS
    """
    if re.match(r'^\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}$', s):
        return True
    return False


@click.command()
@click.argument('input', type=click.Path(exists=True))
@click.argument('output', type=click.Path(), required=False)
@click.option('--fix_persian', is_flag=True, help='Decode Unicode and fix issues with Persian')
@click.option('--shift', type=int, help='The change in seconds to shift the subtitles, e.g. --shift 2 or --shift -5')
def cli(input, output, fix_persian, shift):
    '''
        SubFixer does a bit of string manipulation and datetime math
        to shift your subtitles to match your film and decode string to
        unicode and fix problems with Persian.

    '''
    if input[-4:] not in ('.srt', '.SRT'):
        click.echo('%s is not a srt file.' % click.format_filename(input))
        exit()
    if not fix_persian and not shift:
        raise click.BadParameter('''Enter an option --fix_persian or --shift \
                                \nUse subfixer --help for more info''')

    if fix_persian:
        with open(input, 'r') as f:
            lines = f.read()

        sub_title_fixer = SubtitleFixer()

        lines = sub_title_fixer.decode_string(lines)

        write_file_name = input[:-4] + '_fixed.srt'

        if output:
            write_file_name = output
        with open(write_file_name, 'w') as f:
            f.write(lines.encode('utf-8'))

        click.echo('%s Persian fixed' % input)
        click.echo('New subtitle is on : %s' % write_file_name)

    if shift:
        new_lines = []
        with open(input, 'r') as f:
            for line in f.readlines():
                line = line[:-2]  # removes '\r\n' from line
                if is_time_string(line):
                    times = line.split(' --> ')  # split up the two times
                    new_times = []
                    for t in times:
                        new_times.append(process_time_string(t, shift))
                    line = new_times[0] + ' --> ' + new_times[1]
                new_lines.append(line + '\r\n')  # adds back in '\r\n'

        write_file_name = input[:-4] + '_fixed.srt'

        if output:
            write_file_name = output
        with open(write_file_name, 'w') as f:
            for line in new_lines:
                f.write(line)

        click.echo('%s Time shift done for ' % input)
        click.echo('New subtitle is on : %s' % write_file_name)
