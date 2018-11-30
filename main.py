import re, os
from random import randint

DEFAULT_FILENAME = "lamotte.txt"
DEFAULT_WORDCOUNT = 30
DEFAULT_PRECISION = 1

'''
todo:
* implement precision
* add twitter functionality
* clean up code:
    * add some neat exception handling
    * implement proper flags
    * comment
'''
class MarkovChain:
    # alpha characters mark the end of a sentence structure
    # these are also handled differently when building the output
    alphas = re.compile(r'([.!?:;,]+)')

    def __init__(self, words, precision):
        keys = (' '.join(self.alphas.split(words))).split()
        
        self.chain = {
            "START": [keys[0]],
            "END": []
        }
        
        for i in range(len(keys)-1):
            word = keys[i+1]
            if keys[i] not in self.chain:
                self.chain[keys[i]] = []
            if self.alphas.match(keys[i]):
                self.chain["START"].append(word)
                self.chain["END"].append(keys[i])
            self.chain[keys[i]].append(word)

    def generate(self, length):
        key = "START"
        output = []
        while(len(output) < length):
            word = self.chain[key][randint(0, len(self.chain[key]) - 1)]

            # makes sure there's no spacing before an alpha
            if not self.alphas.match(word):
                output.append(" " + word)
            else:
                output.append(word)

            key = word
            # handles edge cases where the encountered word isn't in the chain
            # or the provided word doesn't have any associated follow ups
            if key not in self.chain or len(self.chain[key]) == 0:
                key = "END" if len(self.chain["END"]) > 0 else "START"

        result = ''.join(output)
        if re.match(r'^[\W]', result):
            result = result[1:]
        return result

def run(args):
    if args is None:
        print("usage: {} <filename>, <word count>, <precision>".format(__file__))
        exit(1337)
    if type(args) is not list:
        args = [args]

    try:
        wordcount = int(args[1]) if len(args) >= 2 else DEFAULT_WORDCOUNT
        if wordcount <= 0:
            wordcount = DEFAULT_WORDCOUNT
    except ValueError as ve:
        print("ValueError ({}) caught, setting wordcount to {}".format(ve, DEFAULT_WORDCOUNT))
        wordcount = DEFAULT_WORDCOUNT

    try:
        precision = int(args[2]) if len(args) >= 3 else DEFAULT_PRECISION
        if precision <= 0:
            precision = DEFAULT_PRECISION
    except ValueError as ve:
        print("ValueError ({}) caught, setting precision to {}}".format(ve, DEFAULT_PRECISION))
        precision = DEFAULT_PRECISION

    filename = args[0] if len(args) >= 1 else DEFAULT_FILENAME
    try:
        words = readFile(filename)
    except FileNotFoundError as fne:
        print("FileNotFoundError ({}) caught, setting filename to {}".format(fne, DEFAULT_FILENAME))
        words = readFile(DEFAULT_FILENAME)

    chain = MarkovChain(words, precision)
    result = chain.generate(wordcount)
    print("text containing {} words generated with {} precision:\n{}".format(wordcount, precision, result))

def readFile(filename):
    path = os.path.abspath(__file__)
    scr_name = os.path.basename(__file__)
    with open(path.replace(scr_name, filename), 'r', encoding="utf-8") as f:
        words = f.read()
    return words

if __name__ == "__main__":
    import sys
    run(sys.argv[1:])