# import random
import argparse
import os
from math import log
from pprint import pprint
import sys
import time
import datetime

DEFAULT_PROB = 0.0000000001

TOTAL = '#####'


class POSLabeler:
    def __init__(self, train, test):
        self.train_file = None
        self.test_file = None
        self.default_context = [""]
        self.confusion_matrix = {}

        self.transition_probabilities = {}
        self.emission_probabilities = {}
        self.initial_probabilities = {}

        self.token_count = 0

        # parse the command line args
        self.parse_args()

    def parse_args(self):

        # add the <training-data> argument
        parser.add_argument("--training-data",
                            action="store",
                            help="The path to a file containing training data for part-of-speech labeling")

        # add the <training-data> argument
        parser.add_argument("--test-data",
                            action="store",
                            help="The path to a file containing test data for part-of-speech labeling")

        # add the <training-data> argument
        parser.add_argument("--output-file",
                            action="store",
                            help="The path to a file in which to store the results")

        # add the <n> argument
        parser.add_argument("--n",
                            type=int,
                            action="store",
                            default=1,
                            help="the 'n' in n-gram")

        # parse the arguments
        args = parser.parse_args()

        # check the training file
        self.training_file = args.training_data
        if self.training_file is None:
            raise Exception("No training file provided")
        if not os.path.exists(self.training_file):
            raise Exception("Training file %s does not exist" % self.training_file)
        if not os.path.isfile(self.training_file):
            raise Exception("Path %s is not a file" % self.training_file)

        # check the test file
        self.test_file = args.test_data
        if self.test_file is None:
            raise Exception("No test file provided")
        if not os.path.exists(self.training_file):
            raise Exception("Test file %s does not exist" % self.test_file)
        if not os.path.isfile(self.training_file):
            raise Exception("Path %s is not a file" % self.test_file)

        # save the path to the output file
        self.output_file = args.output_file

        # pre-generate the context
        self.default_context = [""] * args.n

    def generate_language_model(self):
        start_time = time.time()

        print
        print "Creating model from %s ..." % self.training_file
        print

        # start with the default context
        context = tuple(self.default_context)

        with open(self.training_file, 'r') as in_file:
            input_str = in_file.read()

            # split the text up into tokens
            tokens = input_str.split()
            for token in tokens:
                # increment the token count
                self.token_count += 1

                # output progress
                progress = int(float(self.token_count) / float(len(tokens)) * 100)
                d_time = datetime.timedelta(seconds=int(time.time() - start_time))
                print '\rProcessing token {3} of {4} in {5}: [{0}{1}] {2}%'.format('#' * progress,
                                                                                   '.' * (100 - progress),
                                                                                   progress,
                                                                                   self.token_count,
                                                                                   len(tokens),
                                                                                   d_time),

                # split the token into word, part-of-speech
                word, pos = token.split('_')

                # update the emission probabilities for the current part-of-speech and word
                self.update_emission_probabilities(pos, word)

                # update the transition probabilities for the current context and part-of-speech
                self.update_transition_probabilities(context, pos)

                # update the context with the current word
                context = self.update_context(context, pos)

        # perform some model post-processing
        self.compute_initial_probabilities()

    def update_emission_probabilities(self, pos, word):
        # get the word counts from the emissions for the part-of-speech (create one if necessary)
        word_counts = self.emission_probabilities.setdefault(pos, {word: 0, TOTAL: 0})

        # get the word count for the current word
        word_count = word_counts.setdefault(word, 0)

        # increment the word count and add it back to the word counts
        word_counts[word] = word_count + 1
        word_counts[TOTAL] += 1

    def update_transition_probabilities(self, context, pos):
        # get the part-of-speech counts for the current context (create one if it doesn't already exist)
        pos_counts = self.transition_probabilities.setdefault(context, {pos: 0, TOTAL: 0})

        # get the part-of-speech count for the current pos
        pos_count = pos_counts.setdefault(pos, 0)

        # increment the word count and add it to the word counts dictionary
        pos_counts[pos] = pos_count + 1
        pos_counts[TOTAL] += 1

    def do_pos_labeling(self):
        start_time = time.time()

        print
        print "Performing Part-of-Speech labeling on %s ..." % self.test_file
        print

        v = {}

        for pos_tag in self.initial_probabilities:
            v[pos_tag] = log(self.initial_probabilities[pos_tag])

        with open(self.test_file, 'r') as test_file:
            input_str = test_file.read()

            # split the text up into tokens
            tokens = input_str.split()
            token_count = 0
            for token in tokens:
                # output progress
                token_count += 1
                progress = int(float(token_count) / float(len(tokens)) * 100)
                d_time = datetime.timedelta(seconds=int(time.time() - start_time))
                print '\rProcessing token {3} of {4} in {5}: [{0}{1}] {2}%'.format('#' * progress,
                                                                                   '.' * (100 - progress),
                                                                                   progress,
                                                                                   token_count,
                                                                                   len(tokens),
                                                                                   d_time),

                # split the token into word and part-of-speech
                word, pos = token.split('_')

                best_pos = None
                best_prob = -sys.maxsize - 2
                for tag in self.emission_probabilities:
                    emit_term = log(float(self.emission_probabilities[tag].setdefault(word, DEFAULT_PROB)) /
                                    float(self.emission_probabilities[tag][TOTAL]))

                    for prev in self.transition_probabilities:
                        prev_tag = prev[-1]

                        v_term = v.setdefault(prev_tag, log(DEFAULT_PROB))
                        trans_term = log(float(self.transition_probabilities[prev].setdefault(tag, DEFAULT_PROB)) /
                                         float(self.transition_probabilities[prev][TOTAL]))

                        best_prob, best_pos = max((best_prob, best_pos), (v_term + trans_term + emit_term, tag))

                        v[tag] = best_prob

                # update confusion matrix
                confusion_counts = self.confusion_matrix.setdefault(pos, {})
                confusion_count = confusion_counts.setdefault(best_pos, 0)
                self.confusion_matrix[pos][best_pos] = confusion_count + 1

            print

            if self.output_file is None:
                pprint(self.confusion_matrix)
            else:
                print "Writing results to %s" % self.output_file

                output_dir = os.path.dirname(self.output_file)
                print "output dir: %s" % output_dir
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                with open(self.output_file, 'w') as output:
                    pprint(self.confusion_matrix, output)

    @staticmethod
    def update_context(context, next):
        return tuple((list(context) + [next])[1:])

    def compute_initial_probabilities(self):
        print
        print "POS Tag  POS Tokens  POS Probability"
        print "=======  ==========  ==============="

        for pos in self.emission_probabilities:
            pos_token_count = self.emission_probabilities[pos][TOTAL]
            pos_probability = float(pos_token_count) / float(self.token_count)
            self.initial_probabilities[pos] = pos_probability
            print " %5s    %7s    %12.13f" % (pos, pos_token_count, pos_probability)

if __name__ == '__main__':
    # try:
    #     labeler = POSLabeler()
    #     labeler.generate_language_model()
    # except Exception, e:
    #     print e.message

    labeler = POSLabeler("training_dataset_mini.txt", "training_dataset_sentence")
    labeler.generate_language_model()
    labeler.do_pos_labeling()