import random, string

class PoS:
    def __init__(self, n=1, infile="texts/training_dataset.txt", testfile="texts/training_dataset_sentence.txt", outlen=100):
        self.input_file = infile
        self.test_file = testfile
        self.default_context = [""] * n
        self.output_length = outlen

        self.sentence_count = 0
        self.token_count = 0

        self.pos = {}
        self.prior = {}
        self.emission = {}
        self.transition = {}

    def parse_text(self):
        with open(self.input_file, 'r') as in_file:
			input_str = in_file.read()
			# punctuation
			# input_str = input_str.translate(string.maketrans("",""), string.punctuation).lower()

			for s in input_str.split("\n"):
				first = s.split()[0]
				w,t = first.split("_")
				# update prior value for first word in sentences
				self.prior[t] = self.prior.setdefault(t, 0) + 1
				self.sentence_count += 1

				self.token_count += 1
				# update part of speech count
				self.pos[t] = self.pos.setdefault(t, 0) + 1
				# update emission count
				self.emission[t][w] = self.emission.setdefault(t, {w: 0}).setdefault(w, 0) + 1
				# update transition count
				self.transition[t]["FIRST"] = self.transition.setdefault(t, {"FIRST": 0}).setdefault("FIRST", 0) + 1
				# move previous part of speech forward
				t_prev = t

				for token in s.split()[1:]:
					w,t = token.split("_")

					self.token_count += 1
					# update part of speech count
					self.pos[t] = self.pos.setdefault(t, 0) + 1
					# update emission count
					self.emission[t][w] = self.emission.setdefault(t, {w: 0}).setdefault(w, 0) + 1
					# update transition count
					self.transition[t][t_prev] = self.transition.setdefault(t, {t_prev: 0}).setdefault(t_prev, 0) + 1
					# move previous part of speech forward
					t_prev = t

    def run_test(self):
		context = tuple(self.default_context)

		with open(self.test_file, 'r') as in_file:
			input_str = in_file.read()
			# punctuation
			# input_str = input_str.translate(string.maketrans("",""), string.punctuation).lower()

			# iterate over every test sentence
			for s in input_str.split("\n"):
				# take care of the first word separately
				first = s.split()[0]
				w,t = first.split("_")

				best_pos = None
				best_prob = 0
				prev_prob = {}

				# i iterated over all keys to set ones that don't exist to zero in prev_prob
				for pos in self.pos.keys():
					try:
						m1 = float(self.emission[pos][w])/self.pos[t]
						m1 *= float(self.prior[pos])/self.sentence_count
					# it's possible there won't be data for a particular part of speech
					except KeyError:
						m1 = 0

					# save calculated probabilities for m_n+1
					prev_prob[pos] = m1

					if m1 > best_prob:
						best_prob = m1
						best_pos = pos

				# the start of the finalized PoS sentence
				parts = [best_pos]
				pos_prev = best_pos

				# take care of the rest of the words after the first
				for token in s.split()[1:]:
					w,t = token.split("_")

					best_pos = None
					best_prob = -1

					# A represents the part of speech of the CURRENT word
					for curr in self.pos.keys():
						mt = float(self.emission[curr][w])/self.pos[curr]

						max_val = 0
						max_pos = None
						# B represents the part of speech of the PREVIOUS word
						for prev in self.pos.keys():
							temp = float(self.transition[curr][prev])

						try:
							print token, pos
							print "\t", mt, float(self.emission[pos][w])/self.pos[pos]
							mt *= float(self.transition[pos][pos_prev])/self.pos[pos]
							print "\t", mt, float(self.transition[pos][pos_prev])/self.pos[pos]
							mt *= prev_prob[pos]
							print "\t", mt, prev_prob[pos]
						except KeyError:
							mt = 0

						# save calculated probabilities for the future
						prev_prob[pos] = mt

						if mt > best_prob:
							best_prob = mt
							best_pos = pos

					print

					# record the part of speech i chose
					parts.append(best_pos)
					pos_prev = best_pos

				print parts

    def generate_output(self):
    	# the sentence to return
    	s = []
    	# pick a random word as the starting point
        context = random.sample(self.model.keys(), 1)[0]

        for i in range(self.output_length):
            w = self.next_word(context)
            s.append(w)
			# move context forward 1
            context = tuple((list(context) + [w])[1:])
        return s

    def next_word(self, context):
        # dictionary of words to choose from
        counts = self.model[context]
        # print context, counts, "\n"
        # speed optimization
        if len(counts) == 1:
        	return counts.keys()[0]

        total_words = sum(counts.values())
        num = random.randint(1, total_words)

        a = 0
        b = 0
        for w in counts:
            a = b
            b = a + counts[w]

            if a < num <= b:
                return w

        return counts.keys()[0]


if __name__ == '__main__':

	pos = PoS(n=1)

	pos.parse_text()

	pos.run_test()