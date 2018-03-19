#!/usr/bin/env python
import datetime
import json
import logging

import os
import socket
import sys

import pytz

class CEEFormatter(logging.Formatter):
    cee_token = ' cee: '

    def __init__(self, fmt=None, datefmt=None, tz=None):

        # We don't use super because logging classes are
        # old-style classes on 2.x
        logging.Formatter.__init__(self, fmt, datefmt)

        self.hostname = socket.gethostname()
        self.procname = os.path.basename(sys.argv[0])
        self.tz = tz

    def format(self, record):
        result = logging.Formatter.format(self, record)
        structured = self.format_structured(record)
        if structured:
            result += '%s%s' % (self.cee_token, json.dumps(structured))
        return result

    def get_event_time(self, record):
        return datetime.datetime.fromtimestamp(record.created,
                                               tz=self.tz).isoformat()

    def format_structured(self, record):
        result = {
            'Event': {
                'p_proc': self.procname,
                'p_sys': self.hostname,
                'time': self.get_event_time(record)
            },
        }
        return result

def main():
    if len(sys.argv) > 1:
        try:
            tz = pytz.timezone(sys.argv[1])
        except pytz.UnknownTimeZoneError:
            print('Unknown timezone %r, using Europe/London' % sys.argv[1])
            tz = pytz.timezone('Europe/London')
    else:
        tz = pytz.timezone('Europe/London')

    formatter = CEEFormatter('%(message)s', tz=tz)
    record = logging.makeLogRecord(dict(msg='Hello, world!'))

    print(formatter.format(record))

if __name__ == '__main__':
    sys.exit(main())
