'''
CLI convert utility.

Usage:
    python3 cli_convert.py <subcommand> --in <in path> --out <out path>

Available subcommands:
    json2csv
    csv2json
    csv2xlsx
'''

import argparse
from pathlib import Path
from src.lab05.json_csv import json_to_csv, csv_to_json
from src.lab05.csv_xlsx import csv_to_xlsx


def main():
    '''
    cli convert utility
    '''

    parser = argparse.ArgumentParser(description="cli convert utility")
    subparsers = parser.add_subparsers(dest="subcommand")

    # json2csv
    json2csv_parser = subparsers.add_parser("json2csv", help="json to csv")
    json2csv_parser.add_argument("--in", dest="input", required=True)
    json2csv_parser.add_argument("--out", dest="output", required=True)

    # csv2json
    csv2json_parser = subparsers.add_parser("csv2json", help="csv to json")
    csv2json_parser.add_argument("--in", dest="input", required=True)
    csv2json_parser.add_argument("--out", dest="output", required=True)

    # csv2xlsx
    csv2xlsx_parser = subparsers.add_parser("csv2xlsx", help="csv to xlsx")
    csv2xlsx_parser.add_argument("--in", dest="input", required=True)
    csv2xlsx_parser.add_argument("--out", dest="output", required=True)

    args = parser.parse_args()

    # python 3.10+
    match args.subcommand:
        case "json2csv":
            json_to_csv(args.input, args.output)

        case "csv2json":
            csv_to_json(args.input, args.output)

        case "csv2xlsx":
            csv_to_xlsx(args.input, args.output)


if __name__ == "__main__":
    main()
