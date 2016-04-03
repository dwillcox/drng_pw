#!/usr/bin/python
"""Copyright (c) 2016, Donald E. Willcox
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

1. Redistributions of source code must retain the above copyright
notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright
notice, this list of conditions and the following disclaimer in the
documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
contributors may be used to endorse or promote products derived from
this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

--------------------------------------------------------------------------------

This program reads a text file (eg. 'words') and filters it to output
a text file (eg. 'filtered_words'). 

'words' and 'filtered_words' are both newline-delimited lists of words.

Lines beginning in # are considered comments.

'filtered_words' contains the words in 'words' that match the following
regular expression: '\A[a-z]*\Z' (ie. all lowercase, purely
alphabetical characters).

A good way to get a list of words to start from is to create a
symbolic link in the current directory to /usr/share/dict/words
on a Unix-like system.

To call this program with an input file 'words' to produce the file 'pwwords':
>python filter_words.py words -o pwwords
"""
import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('infile', type=str, help='Input file to filter')
parser.add_argument('-o','--outfile', type=str, help='Output file to produce. If nothing is given, the default behavior is to prepend \'filtered_\' to the input file name.')
args = parser.parse_args()

try:
    fi = open(args.infile,'r')
except:
    print 'ERROR: \'{}\' could not be opened for reading!'.format(args.infile)
    exit()

if args.outfile:
    outfile = args.outfile
else:
    outfile = 'filtered_' + args.infile
    
try:
    fo = open(outfile,'w')
except:
    print 'ERROR: \'{}\' could not be opened for writing!'.format(outfile)
    exit()


for l in fi:
    if l[0] != '#':
        ls = l.strip()
        if( re.match('\A[a-z]*\Z',ls) ):
            fo.write(ls + '\n')

fi.close()
fo.close()
