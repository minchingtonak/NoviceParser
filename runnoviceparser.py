#!/usr/bin/env python3

from noviceparser import NoviceParser
from novicelexer import NoviceLexer
import sys
import json
import argparse


def calc_exposure(train_data, parse_data):
    acc = 0
    for train_val, parse_val in zip(
            train_data.values(), parse_data.values()):
        if isinstance(train_val, int):
            acc += (train_val * parse_val)
        else:
            for tv, pv in zip(train_val.values(), parse_val.values()):
                acc += (tv * pv)
    return acc


if __name__ == '__main__':
    lexer = NoviceLexer()
    parser = NoviceParser()

    argparser = argparse.ArgumentParser(description='Test')
    group = argparser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--train',
        '-t',
        help='Run in training mode',
        action='store_true')
    group.add_argument(
        '--analyze',
        '-a',
        help='Run in analyze mode',
        action='store_true')
    argparser.add_argument(
        '--input',
        '-i',
        nargs='+',  # Must be one or more files supplied
        help='List of input files. In training mode,  treated as code that has been seen before. In analyze mode, an exposure score is calculated for each input file.',
        required=True)

    args = argparser.parse_args()

    if args.analyze:
        train_data = {}
        with open('.train.json', 'r') as f:
            train_data = json.load(f)
        scores = []
        for file in args.input:
            with open(file, 'r') as f:
                parser.parse(lexer.tokenize(f.read()))
            scores.append(calc_exposure(train_data, parser.freq))
            parser.clear_freq()
        for name, val in zip(args.input, scores):
            print("% 20s % 20s" % (name, val))
    elif args.train:
        for file in args.input:
            with open(file, 'r') as f:
                parser.parse(lexer.tokenize(f.read()))
        with open('.train.json', 'w') as f:
            json.dump(parser.freq, f, indent=4)
