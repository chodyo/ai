import os, random, string

class nGram:
    def __init__(self, n=1, infile="texts/2009-Obama.txt", outlen=100):
        self.model = {}
        self.input_file = infile
        self.default_context = [""] * n
        self.output_length = outlen

    def parse_text(self):
        context = tuple(self.default_context)

        with open(self.input_file, 'r') as in_file:
            input_str = in_file.read().translate(string.maketrans("",""), string.punctuation).lower()

            for w in input_str.split():
                counts = self.model.setdefault(context, {w: 0})
                count = counts.setdefault(w, 0)
                counts[w] = count+1

                # move context forward 1
                context = tuple((list(context) + [w])[1:])

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

        word_low = word_high = 0
        for w in counts:
            word_low = word_high
            word_high = word_low + counts[w]

            if word_low < num <= word_high:
                return w

        return counts.keys()[0]


if __name__ == '__main__':
    n_gram = nGram(n=1)
    n_gram.parse_text()

    print
    for w in n_gram.generate_output():
    	print w,
    print
    print
