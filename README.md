# drng_pw

These programs demonstrate the use of the RDRAND and RDSEED
instructions available for newer Intel CPUs (eg. Ivy Bridge).

The drng_pw.py program uses RDRAND to generate passwords consisting of
randomly selected words from an input word list.

## To SETUP:

```
$ ./configure
$ make libdrng
```

Then add the current directory to LD_LIBRARY_PATH.

## To RUN:

```
$ python drng_pw.py pwwords
```

# Custom Word Lists

The filter_words.py program is included to assist in filtering word
lists to obtain lists consisting only of words containing only
alphabet characters a-z, all lowercase.

## To FILTER: (for example)

```
$ python filter_words.py words -o pwwords
```