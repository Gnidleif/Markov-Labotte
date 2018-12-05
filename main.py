import re, os, random

DEFAULT_FILENAME = "trump.txt"
DEFAULT_WORDCOUNT = 50
DEFAULT_PRECISION = 3

class MarkovChain:
    alphas = re.compile(r'([!.:;,?-])')

    def __init__(self, words, precision):
        self.prec = precision
        keys = words.split()
        self.chain = {}
        for i in range(len(keys)-precision):
            jump = i+precision
            key = ' '.join(keys[i:jump])
            if key not in self.chain:
                self.chain[key] = []
            self.chain[key].append(keys[jump])

    def generate(self, length):
        words = [self.get_random()]
        for i in range(length):
            key = ' '.join(words[i:i+self.prec])
            if key not in self.chain:
                key = self.get_random()
            words.append(random.choice(self.chain[key]))
        return ' '.join(words)

    def get_random(self):
        return random.choice(list(self.chain.keys()))

def readFile(filename):
    path = os.path.abspath(__file__)
    scr_name = os.path.basename(__file__)
    with open(path.replace(scr_name, filename), 'r', encoding="utf-8") as f:
        words = f.read()
    return words

def handleFlags(args):
    try:
        wordcount = int(args[1]) if len(args) >= 2 else DEFAULT_WORDCOUNT
        if wordcount <= 0:
            wordcount = DEFAULT_WORDCOUNT
    except ValueError as ve:
        wordcount = DEFAULT_WORDCOUNT

    try:
        precision = int(args[2]) if len(args) >= 3 else DEFAULT_PRECISION
        if precision <= 0:
            precision = DEFAULT_PRECISION
    except ValueError as ve:
        precision = DEFAULT_PRECISION

    filename = args[0] if len(args) >= 1 else DEFAULT_FILENAME

    return wordcount, precision, filename

def main(args):
    if args is None:
        print("usage: {} <filename>, <word count>, <precision>".format(__file__))
        exit(1337)
    if type(args) is not list:
        args = [args]

    wc, prec, fn = handleFlags(args)

    try:
        words = readFile(fn)
    except FileNotFoundError as fne:
        words = readFile(DEFAULT_FILENAME)

    chain = MarkovChain(words, prec)
    result = chain.generate(wc)
    print(result)

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])