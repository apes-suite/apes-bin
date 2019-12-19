import subprocess
import argparse
import glob
import csv

parser = argparse.ArgumentParser(description='Finding author contributions to files.')
parser.add_argument('files', metavar='FILE', nargs='+', help='files to process')
args = parser.parse_args()

for fname in args.files:
  sources = glob.glob(fname)
  for f in sources:
    print(f)
    hg_out = subprocess.check_output(['hg', 'log', '-f', '--template', r'''{date(date, '%Y')},{author}\n''', f])
    logreader = csv.reader(hg_out.decode('utf-8').split('\n'), delimiter=',')
    authors = {}
    for row in logreader:
      if len(row) == 2:
        author = row[1]
        year = int(row[0])
        if author not in authors:
          authors[author] = set()
        authors[author].add(year)

    for author,years in authors.items():
      ylist = list(years)
      year_order = sorted(ylist)
      year_str = "Copyright (c) {0}".format(year_order[0])
      prev_year = year_order[0]
      lastseq = 0
      for year in year_order[1:]:
        if year == prev_year+1:
          lastseq = year
        elif lastseq > 0:
          year_str = "{0}-{1}, {2}".format(year_str, lastseq, year)
          lastseq = 0
        else:
          year_str = "{0}, {1}".format(year_str, year)
        prev_year = year
      if lastseq > 0:
        year_str = "{0}-{1}".format(year_str, lastseq)
      year_str = "{0} {1}".format(year_str, author)
      print(year_str)
