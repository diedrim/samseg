#!/usr/bin/env python

import argparse
import surfa as sf
from samseg import icv

description = '''
Calculates the total intracranial volume of a subject by summing individual volumes computed by samseg. \
A file containing a list of intracranial labelnames can be provided via the '--labels' flag, but if omitted, \
a default list is used. Labelnames must be identical to those defined in the samseg atlas.
'''

def main():
    # parse command line args
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('stats', metavar='FILE', help='Volume stats input file.')
    parser.add_argument('-o', '--out', metavar='FILE', help='Intracranial stats output file.')
    parser.add_argument('-l', '--labels', metavar="FILE", help='File containing a list of intracranial structure labelnames to include in the calculation.')
    args = parser.parse_args()

    # read in structure names and volumes from samseg stats 
    structures = []
    with open(args.input) as fid:
        for line in fid.readlines():
            name, vol, _ = line.split(',')
            _, _, name = name.split(' ')
            structures.append([name.strip(), float(vol)])

    # read in structure names that are considered intra-cranial
    includeStructures = None
    if args.map:
        with open(args.map) as fid: includeStructures = [line.strip() for line in fid.readlines()]

    # compute intra-cranial volume
    sbtiv = icv(structures, includeStructures)

    # write out and exit
    print('intracranial volume: %.6f mm^3' % sbtiv)
    if args.output:
        with open(args.output, 'w') as fid: fid.write('# Measure Intra-Cranial, %.6f, mm^3\n' % sbtiv)


if __name__ == '__main__':
    main()
