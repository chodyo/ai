import os, sys, time, datetime
from math import log
from pprint import pprint

train_file = "texts/training_dataset.txt"
test_file = "texts/testing_dataset_mini.txt"

first = "FIRST"
defaultprob = 1.0/999999999999.0

class ViterbiLabeler:
    def __init__(self, train, test):
        self.train_file = train
        self.test_file = test
        self.default_context = [""]
        self.confusion_matrix = {}

        self.default_context = [""]

        self.transition = {}
        self.emission = {}
        self.percent = {}

        self.token_count = 0
        self.correct = 0
        self.incorrect = 0

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

        self.update_percents()

    def update_emission(self, pos, w):
        word_counts = self.emission.setdefault(pos, {w: 0, first: 0})
        word_count = word_counts.setdefault(w, 0)

        word_counts[w] = word_count + 1
        word_counts[first] += 1

    def update_transition(self, context, pos):
        pos_counts = self.transition.setdefault(context, {pos: 0, first: 0})
        pos_count = pos_counts.setdefault(pos, 0)

        pos_counts[pos] = pos_count + 1
        pos_counts[first] += 1

    def test(self):
        vit = {}

        for pos_tag in self.percent:
            vit[pos_tag] = log(self.percent[pos_tag])

        with open(self.test_file, 'r') as test_file:
            input_str = test_file.read()

            tokens = input_str.split()
            for token in tokens:
                w,pos = token.split('_')
                best_pos = None
                best_prob = -sys.maxsize - 2
                for tag in self.emission:
                    emit_term = log(float(self.emission[tag].setdefault(w, defaultprob)) / float(self.emission[tag][first]))

                    for prev in self.transition:
                        prev_tag = prev[-1]

                        v_term = vit.setdefault(prev_tag, log(defaultprob))
                        trans_term = log(float(self.transition[prev].setdefault(tag, defaultprob)) / float(self.transition[prev][first]))

                        best_prob, best_pos = max((best_prob, best_pos), (v_term + trans_term + emit_term, tag))

                        vit[tag] = best_prob

                # record my skillz
                print "%s=%s (%s)\t" % (w, best_pos, pos),
                if pos == best_pos:
                    self.correct += 1
                else:
                    self.incorrect += 1

                # update confusion matrix
                confusion_counts = self.confusion_matrix.setdefault(pos, {})
                confusion_count = confusion_counts.setdefault(best_pos, 0)
                self.confusion_matrix[pos][best_pos] = confusion_count + 1

            print
            pprint(self.confusion_matrix)

    def update_percents(self):
        print "   Tag    Count    /%d  " % (self.token_count)
        print "  -----  -------  ---------"

        for pos in self.emission:
            tag_count = self.emission[pos][first]
            tag_prob = float(tag_count) / float(self.token_count)
            self.percent[pos] = tag_prob
            print "  %5s  %7d  %0.5f" % (pos, tag_count, tag_prob)

if __name__ == '__main__':

    p = ViterbiLabeler(train_file, test_file)
    p.train()
    p.test()

    print "correctness:", p.correct, "/", p.correct+p.incorrect