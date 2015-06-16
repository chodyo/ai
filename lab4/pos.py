import os, sys, time, datetime
from math import log
from pprint import pprint

DEFAULT_PROB = 0.0000000001

TOTAL = '#####'


class POSLabeler:
    def __init__(self, train, test):
        self.train_file = train
        self.test_file = test
        self.default_context = [""]
        self.confusion_matrix = {}

        self.default_context = [""]

        self.transition = {}
        self.emission = {}
        self.initial = {}

        self.token_count = 0

    def train(self):
        context = tuple(self.default_context)

        with open(self.train_file, 'r') as in_file:
            input_str = in_file.read()

            tokens = input_str.split()
            for token in tokens:
                self.token_count += 1
                w,pos = token.split('_')
                self.update_emission(pos, w)
                self.update_transition(context, pos)
                context = tuple((list(context) + [next])[1:])

        # perform some model post-processing
        self.compute_initial_probabilities()

    def update_emission(self, pos, w):
        word_counts = self.emission.setdefault(pos, {w: 0, TOTAL: 0})
        word_count = word_counts.setdefault(w, 0)

        word_counts[w] = word_count + 1
        word_counts[TOTAL] += 1

    def update_transition(self, context, pos):
        pos_counts = self.transition.setdefault(context, {pos: 0, TOTAL: 0})
        pos_count = pos_counts.setdefault(pos, 0)

        pos_counts[pos] = pos_count + 1
        pos_counts[TOTAL] += 1

    def test(self):
        v = {}

        for pos_tag in self.initial:
            v[pos_tag] = log(self.initial[pos_tag])

        with open(self.test_file, 'r') as test_file:
            input_str = test_file.read()

            tokens = input_str.split()
            for token in tokens:
                w,pos = token.split('_')
                best_pos = None
                best_prob = -sys.maxsize - 2
                for tag in self.emission:
                    emit_term = log(float(self.emission[tag].setdefault(w, DEFAULT_PROB)) /
                                    float(self.emission[tag][TOTAL]))

                    for prev in self.transition:
                        prev_tag = prev[-1]

                        v_term = v.setdefault(prev_tag, log(DEFAULT_PROB))
                        trans_term = log(float(self.transition[prev].setdefault(tag, DEFAULT_PROB)) /
                                         float(self.transition[prev][TOTAL]))

                        best_prob, best_pos = max((best_prob, best_pos), (v_term + trans_term + emit_term, tag))

                        v[tag] = best_prob

                # update confusion matrix
                confusion_counts = self.confusion_matrix.setdefault(pos, {})
                confusion_count = confusion_counts.setdefault(best_pos, 0)
                self.confusion_matrix[pos][best_pos] = confusion_count + 1

            pprint(self.confusion_matrix)

    def compute_initial_probabilities(self):
        print
        print "POS Tag  POS Tokens  POS Probability"
        print "=======  ==========  ==============="

        for pos in self.emission:
            pos_token_count = self.emission[pos][TOTAL]
            pos_probability = float(pos_token_count) / float(self.token_count)
            self.initial[pos] = pos_probability
            print " %5s    %7s    %12.13f" % (pos, pos_token_count, pos_probability)

if __name__ == '__main__':

    labeler = POSLabeler("texts/training_dataset_mini.txt", "texts/training_dataset_sentence.txt")
    labeler.train()
    labeler.test()
