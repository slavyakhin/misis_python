'''
Count words (tokens) in files.

Usage:
    python3 text_report.py [--in] <input path>...

    You may pass multiple paths. Script creates a report for each file and summary report.
'''

import argparse
from pathlib import Path
from src.lab04.io_txt_csv import read_text, write_csv
from src.lib.text import normalize, tokenize, count_freq, top_n
from src.lib.merge_sort import merge_sorted
from src.lab03.text_stats import print_summary

ENCODING = "utf-8"
OUTPUT_DIR_PATH = "./data"
PER_FILE_PATH = "./data/report_per_file.csv"
TOTAL_PATH = "./data/report_total.csv"
HEADER_TOTAL = ("word", "count")
HEADER_PER_FILE = ("file", "word", "count")

TOP_QUANTITY = 5 # number of lines in logging top-n

def main():
    '''
    Analyze file(s). Make csv report(s) with columns: word, count
    '''

    parser = argparse.ArgumentParser(description="Count words (tokens) in files. Make csv report(s) with columns: word, count")
    parser.add_argument("--encoding", required=False, default=ENCODING, help=f"ecnoding, {ENCODING} by default")
    parser.add_argument("-o", "--output-dir", dest="output_dir", required=False, default=OUTPUT_DIR_PATH, help=f'output dir path, "{OUTPUT_DIR_PATH}" by default')
    parser.add_argument("--per-file", dest="per_file_path", required=False, default=PER_FILE_PATH, help=f'per file output path, "{PER_FILE_PATH}" by default')
    parser.add_argument("--total", dest="total_path", required=False, default=TOTAL_PATH, help=f'total output path, "{TOTAL_PATH}" by default')
    parser.add_argument("--in", dest="in_list", nargs='+', required=True, help="input path(s)")
    args = parser.parse_args()

    in_path_list = list(map(Path, args.in_list))

    output_dir_path = Path(args.output_dir)

    multiple_files = (len(in_path_list) > 1)
    per_file_freqs = list()

    sum_freqs = dict()

    for cur_in_path in in_path_list:
        cur_str = read_text(cur_in_path, args.encoding)
        cur_str = normalize(cur_str)

        cur_tokens = tokenize(cur_str)
        cur_freqs = count_freq(cur_tokens)

        per_file_freqs.extend([(cur_in_path.name, word, count) for word, count in cur_freqs.items()])

        for word, count in cur_freqs.items():
            sum_freqs[word] = sum_freqs.get(word, 0) + count


    if multiple_files:
        per_file_freqs = merge_sorted(per_file_freqs, key= lambda x: (x[0], -x[2], x[1]))

        per_file_path = Path(args.per_file_path)
        write_csv(rows=per_file_freqs, path=per_file_path, header=HEADER_PER_FILE)


    sum_top = top_n(sum_freqs, len(sum_freqs))

    total_path = Path(args.total_path)
    write_csv(rows=sum_top, path=total_path, header=HEADER_TOTAL)

    print(total_path.name)
    print_summary(total_tokens=sum(sum_freqs.values()),
                  unique_tokens=len(sum_freqs),
                  table=sum_top[:TOP_QUANTITY])


if __name__ == "__main__":
    main()
