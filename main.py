import re, os
from random import randint

ALPHAS = re.compile(r'([.!?:;,]+)')

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
        count = 0
        output = ""
        while(count < length):
            word = self.chain[key][randint(0, len(self.chain[key]) - 1)]

            # makes sure there's no spacing before an alpha
            if not self.alphas.match(word):
                output += " " + word
            else:
                if count / length >= 0.75:
                    break
                output += word

            # handles edge cases where the encountered word isn't in the chain
            # or the provided word doesn't have any associated follow ups
            if word not in self.chain or len(self.chain[word]) == 0:
                word = "END" if len(self.chain["END"]) > 0 else "START"

            key = word
            count += 1

        return output[1:]

def run(args):
    if args is None:
        print("usage: {} <filename>, <word count>, <precision>".format(__file__))
        exit(1337)
    if type(args) is not list:
        args = [args]

    filename = args[0] if len(args) >= 1 else "lamotte.txt"
    wordcount = int(args[1]) if len(args) >= 2 else 30
    precision = int(args[2]) if len(args) >= 3 else 1

    words = readFile(filename)
    chain = MarkovChain(words, precision)
    print(chain.generate(wordcount))

def readFile(filename):
    path = os.path.abspath(__file__)
    scr_name = os.path.basename(__file__)
    try:
        with open(path.replace(scr_name, filename), 'r', encoding="utf-8") as f:
            words = f.read()
    except FileNotFoundError as fne:
        print("File error: {0}".format(fne))
        raise
    return words

if __name__ == "__main__":
    import sys
    run(sys.argv[1:])