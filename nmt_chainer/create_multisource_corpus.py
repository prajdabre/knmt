#!/usr/bin/env python
"""create_multisource_corpus.py: Creates a multisource corpus from given individual source corpora by simply appending the sentences with a space in betweeen."""
__author__ = "Raj Dabre"
__license__ = "undecided"
__version__ = "1.0"
__email__ = "prajdabre@gmail.com"
__status__ = "Development"

import collections
import logging
import codecs
import json
import operator
import os.path
import gzip
import io
import random
import time
from collections import defaultdict

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from utils import ensure_path

if sys.version_info < (3, 0):
  sys.stderr = codecs.getwriter('UTF-8')(sys.stderr)
  sys.stdout = codecs.getwriter('UTF-8')(sys.stdout)
  sys.stdin = codecs.getreader('UTF-8')(sys.stdin)

logging.basicConfig()
log = logging.getLogger("rnns:createdummycorpus")
log.setLevel(logging.INFO)


class CreateMultiSourceCorpus:
	def __init__(self, args):
		log.info("Initializing the Data Generation Pipeline.")
		
		self.args = args
		self.incorpus = args.incorpus
		self.outcorpus = args.outcorpus
		self.verbose = args.verbose
		
		
		log.info("Initialization complete.")
	
	def generate_corpus(self):
		self.incorpus = [io.open(corpus, encoding="utf-8") for corpus in  self.incorpus]
		self.outcorpus = io.open(self.outcorpus, 'w', encoding="utf-8")
		i = 0
		for line in self.incorpus[0]:
			all_lines = [line.strip()]
			for corpus in self.incorpus[1:]:
				all_lines.append(corpus.readline().strip())
			self.outcorpus.write(unicode(" ".join(all_lines) + "\n"))
			if not (i+1)%100000 and self.verbose:
				log.info("Generated %d lines." % (i+1))
		for corpus in self.incorpus:
			corpus.close()
		self.outcorpus.flush()
		self.outcorpus.close()

	def run_pipeline(self):
		log.info("Generating corpus.")
		self.generate_corpus()
		log.info("Done.")



if __name__ == '__main__':
	import sys
	import argparse
	parser = argparse.ArgumentParser(description="Make a multisource corpus from individual source corpora.",
									 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument(
		"--incorpus", nargs = '+', help="The input corpora files.")
	parser.add_argument(
		"--outcorpus", help="The generated corpus output file.")
	parser.add_argument(
		"--verbose", default = False, action = "store_true", help="More details.")
	args = parser.parse_args()
	start = time.time()
	dpp = CreateMultiSourceCorpus(args)

	dpp.run_pipeline()
	end = time.time()
	log.info("Took a total of %d seconds." % (end-start))