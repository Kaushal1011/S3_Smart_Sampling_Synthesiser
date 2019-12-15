#!/usr/bin/env python3

import contextlib
from os import system

import S3DataUtils
import S3GuiMain
import S3SignalUtils
import S3Synth
import S3SynthMain
import S3Utils

with open('help.md', 'w') as f:
    f.write('<pre>\n')

    with contextlib.redirect_stdout(f):
        help(S3DataUtils)
        help(S3GuiMain)
        help(S3Synth)
        help(S3SignalUtils)
        help(S3Utils)
        help(S3SynthMain)

    f.write('</pre>\n')

system('pandoc -f markdown -t html help.md -o help.html')
