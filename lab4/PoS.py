import random, string

class PoS:
    def __init__(self, n=1, infile="texts/training_dataset_mini.txt", testfile="texts/training_dataset_sentence.txt", outlen=100):
        self.input_file = infile
        self.test_file = testfile
        self.default_context = [""] * n
        self.output_length = outlen

        self.sentence_count = 0
        self.prior = {}
        self.emission = {}
        self.transmission = {}

    def parse_text(self):
        context = tuple(self.default_context)

        with open(self.input_file, 'r') as in_file:
			input_str = in_file.read()
			# punctuation
			# input_str = input_str.translate(string.maketrans("",""), string.punctuation).lower()

			for s in input_str.split("\n"):
				first = s.split()[0]
				w,t = first.split("_")
				# update prior value for first word in sentences
				self.prior[t][w] = self.prior.setdefault(t, {w: 0}).setdefault(w, 0) + 1
				self.sentence_count += 1

				for token in s.split():
					w,t = token.split("_")
					# update emission count
					self.emission[t][w] = self.emission.setdefault(t, {w: 0}).setdefault(w, 0) + 1
					# update transmission count
					self.transmission[context][t] = self.transmission.setdefault(context, {t: 0}).setdefault(t, 0) + 1
					# move context forward 1
					context = tuple((list(context) + [w])[1:])

					# print "Added {0}, {1}".format(w, t)
					# print self.emission
					# print

	def run_test(self):
		context = tuple(self.default_context)

		with open(self.input_file, 'r') as in_file:
			input_str = in_file.read()
			# punctuation
			# input_str = input_str.translate(string.maketrans("",""), string.punctuation).lower()

			for s in input_str.split("\n"):
				pass

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

    # print
    # for w in pos.generate_output():
    # 	print w,
    # print
    # print
