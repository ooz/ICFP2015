#!/usr/bin/python
# coding: utf-8

import argparse as AP
from game import Game


def main(args):
    if args.file:
        [process(f) for f in args.file]

def process(f):
    game = Game(f)
    print game.solve()

if __name__ == "__main__":
    parser = AP.ArgumentParser(description="Hexagon tetris bot.")
    parser.add_argument("-f", "--file", metavar="file",
                        type=str, action="append",
                        help="File containing JSON encoded input")
    parser.add_argument("-t", "--time", type=int,
                        help="Time limit, in seconds, to produce output")
    parser.add_argument("-m", "--memory", type=int,
                        help="Memory limit, in megabytes, to produce output")
    parser.add_argument("-c", "--cores", type=int,
                        help="Number of processor cores available")
    parser.add_argument("-p", "--power", metavar="phrase",
                        type=str, action="append",
                        help="Phrase of power")
    args = parser.parse_args()
    main(args)
