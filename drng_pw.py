#!/usr/bin/python
"""
Copyright (c) 2016, Donald E. Willcox
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

This program uses the Intel DRNG capabilities of newer processors to 
generate a password consisting of space-delimited, randomly selected
words from the english language. 

After each call to the DRNG, 1022 calls are made to force the
hardware generator to refresh its seed.

The word list to choose from is a newline-delimited text file pwwords, 
in which lines beginning with # are regarded as comments.

To run this program using the word list file 'pwwords':
>python drng_pw.py pwwords
"""
from ctypes import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('infile', type=str, help='Name of input word list file.')
args = parser.parse_args()

libdrng = CDLL("libdrng.so.1.0.1")
N_retry = 10   # Number of retry calls recommended by Intel
N_reset = 1022 # Maximum number of integers produced by the Intel DRNG with the same seed.

try:
    fwl = open(args.infile,'r')
except:
    print 'ERROR: Could not open {} for reading!'.format(args.infile)
    exit()
wl = []      # Wordlist
for l in fwl:
    ls = l.strip()
    if ls[0] != '#':
        wl.append(ls)
fwl.close()
M_words = len(wl)  # The number of words available to choose from

def getmaxv(n):
    """
    Returns the maximum value of an unsigned n-bit integer.
    """
    return 2**n - 1

def getrand():
    """
    Returns a random 64-bit unsigned integer by calling Intel's DRNG.
    """
    randint = c_ulonglong() # Holds the value returned by the DRNG.
    success = 0
    numcall = 0
    while not success:
        if ( numcall == N_retry ):
            print 'ERROR: DRNG Failure after {} retries. Possible CPU problem!'.format(numcall)
            exit()
        success = libdrng.rdrand64_step(byref(randint))
        numcall += 1
    return randint.value

def getrand_with_seed_reset():
    """
    Call the getrand() function to get a random 64-bit unsigned integer.
    But first force the Intel DRNG seed to reset by calling it 1022 times.
    """
    for i in xrange(N_reset):
        getrand()
    return getrand()

def getindx(M, Nmax):
    """Returns a random integer in the set [ 0 , M-1 ] suitable
    for indexing. Uses repeated calls to getrand() instead of 
    simply using the modulo to map all values returned by getrand()
    to the range [ 0 , M-1 ] in order to retain a uniform 
    distribution of indexes in the desired set. 

    This presumes, of course, that getrand() returns uniformly
    distributed integers. That is the case for Intel's DRNG.

    Nmax should be the maximum value held in a unsigned N-bit integer,
    where N is the size of the integers obtained from the DRNG.

    NOTE: The word list should be chosen so Nmax > M. In practice this
    isn't hard because Nmax = 2^64-1 for 64-bit unsigned integers and
    all languages have many fewer words.
    """
    ## Find a random integer in the range [ 0 , N-N%M )
    upper_limit = Nmax-Nmax%M
    while True:
        rval = getrand_with_seed_reset()
        if ( rval < upper_limit ):
            return rval%M

if __name__=="__main__":
    Nmax = getmaxv(64)

    M_unique_words = len(list(set(wl)))
    if M_unique_words != M_words:
        print 'WARNING: THERE ARE DUPLICATES IN YOUR WORD LIST!'
        print 'LENGTH OF WORD LIST: {}'.format(M_words)
        print 'NUMBER OF UNIQUE WORD LIST ENTRIES: {}'.format(M_unique_words)
        exit()
        
    print ''
    print 'The length of your password word list is {}'.format(M_words)
    print ''
    print 'NOTE: Preserve the spaces in your password between words,'
    print 'otherwise the possibility of compound words reduces the effective'
    print 'number of available combinations and your security is accordingly reduced.'
    print ''
    while True:
        print '--------------------------------------------------------------------------------'
        num_words_str = raw_input("How many words would you like to use? (Enter 0 to quit) ")
        try:
            num_words = int(num_words_str)
        except:
            continue
        if num_words == 0:
            exit()
        elif num_words < 0:
            continue
        pwlist = []
        print ''
        print '->  ' + ' '.join([ wl[getindx(M_words, Nmax)] for i in xrange(num_words) ])
        print ''
        try:
            ncomb = float(M_words)**float(num_words)
            print 'There are {:1.1e} possible {}-word combinations in this word list.'.format(ncomb, num_words)
            print 'Assuming a brute-force attack with knowledge of your {}-length word list'.format(M_words)
            print 'and the ability to execute 1 trillion guesses per second, it would require'
            print '{:1.1e} years to exhaust all {}-word combinations'.format(ncomb/(1.0e12*3.154e7), num_words)
        except OverflowError:
            pass
