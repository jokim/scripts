#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Copyright Joakim Hovlandsvåg
# Licenced by GPLv3.
"""
A simple script for doing a basic analysis of a given ciphertext. It counts up
the number of occurrences of each character, which is usable if the encryption
is done with plain substitutions.
"""
import sys

import CryptoStuff

# Statistical use of Norwegian letters
char_use_no = {
        u'a': 6.1,
        u'b': 1.5,
        u'c': 0.2,
        u'd': 4.3,
        u'e': 15.2,
        u'f': 2.0,
        u'g': 3.8,
        u'h': 1.6,
        u'i': 6.2,
        u'j': 1.0,
        u'k': 3.8,
        u'l': 5.4,
        u'm': 3.3,
        u'n': 8.1,
        u'o': 4.9,
        u'p': 1.9,
        u'q': 0.004,
        u'r': 8.6,
        u's': 6.7,
        u't': 7.9,
        u'u': 1.6,
        u'v': 2.5,
        u'w': 0.1,
        u'x': 0.03,
        u'y': 0.7,
        u'z': 0.03,
        u'æ': 0.2,
        u'ø': 0.9,
        u'å': 1.5,
        }
# Statistical use of Norwegian bigrams
bigrams_use_no = {
        'er': 2.5,
        'en': 3.2,
        'de': 2.6,
        're': 2.3,
        'te': 1.7,
        'et': 1.7,
        'an': 1.6,
        'in': 1.5,
        'ng': 1.4,
        'es': 1.4,
        'nd': 1.3,
        'ge': 1.3,
        'or': 1.3,
        'st': 1.2,
        'ne': 1.1,
        'ti': 1.1,
        'il': 1.1,
        }

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print "Usage: analyze <input-data to analyze>"
        sys.exit(1)
    if '--norwegian' in sys.argv[1:]:
        print "Statistics for Norwegian:"
        print "Chars"
        for c in sorted(char_use_no, key=lambda a: char_use_no[a], reverse=True):
            print u"%5s : %5.4f" % (c, char_use_no[c])
        print "Bigrams"
        for bi in sorted(bigrams_use_no, key=lambda a: bigrams_use_no[a], reverse=True):
            print u"%5s : %5.4f" % (bi, bigrams_use_no[bi])
        sys.exit()

    cipher = ' '.join(unicode(a, 'utf8') for a in sys.argv[1:])
    counts = CryptoStuff.count_chars(cipher)
    print "    Char Occur    Percent"
    for c in sorted(counts, key=lambda a: counts[a], reverse=True):
        print u"%5s : %5d    %1.4f" % (c, counts[c], float(counts[c])/len(cipher))
    print "Total    %5d" % len(cipher)

    # No need of the spaces from here
    cipher = cipher.replace(' ', '')

    print "\nBigrams:"
    bigrams = CryptoStuff.count_bigrams(cipher)
    for bi in sorted(bigrams, key=lambda a: bigrams[a], reverse=True):
        if bigrams[bi] <= 1: # drop single ones, they're not interesting
            break
        print "%5s : %5d" % (bi, bigrams[bi])

    print

    print "Possible key lengths (kasiski):"
    print "(The English language's coincidence index is around 0.065)"
    best_length = 0
    goal = 0.065
    for keylength in CryptoStuff.kasiski(cipher):
        idx = [CryptoStuff.index_of_coincidence(chunk) for chunk 
                                              in CryptoStuff.chunk_split(cipher, keylength)]
        median = sorted(idx)[len(idx) / 2]
        if abs(goal - best_length) > abs(goal - median):
            best_length = keylength
        print "Length %6d : %.4f" % (keylength, median)

    print "\nBest found keylength: %d" % best_length

