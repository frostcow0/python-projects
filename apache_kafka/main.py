#!/usr/bin/env python

import send_record
import receive_record


if __name__ == '__main__':
    print('-------- Sending Record --------')
    send_record()
    print('-------- Receiving Record ------')
    receive_record()
    print('Done.')

# This needs to be a bash script so we can pass the command line arguments to the scripts