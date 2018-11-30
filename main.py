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
    alphas = re.compile(r'([.!?:;,]+)')

    def __init__(self, filename, precision):
        words = self.readFile(filename)

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

    def readFile(self, filename):
        path = os.path.abspath(__file__)
        scr_name = os.path.basename(__file__)
        try:
            with open(path.replace(scr_name, filename), 'r', encoding="utf-8") as f:
                words = f.read()
        except FileNotFoundError as fne:
            print("File error: {0}".format(fne))
            raise
        return words

    def generate(self, length):
        key = "START"
        count = 0
        output = ""
        while(count < length):
            word = self.chain[key][randint(0, len(self.chain[key]) - 1)]
            if not self.alphas.match(word):
                output += " " + word
            else:
                output += word
            key = word
            if key not in self.chain or len(self.chain[key]) == 0:
                if count / length >= 0.75:
                    break
                key = "END" if len(self.chain["END"]) > 0 else "START"
            count += 1

        return output

def run(args):
    if args is None:
        print("usage: {} <filename>, <word count>, <precision>".format(__file__))
        exit(1337)
    if type(args) is not list:
        args = [args]

    filename = args[0] if len(args) >= 1 else "lamotte.txt"
    wordcount = int(args[1]) if len(args) >= 2 else 30
    precision = int(args[2]) if len(args) >= 3 else 1

    chain = MarkovChain(filename, precision)
    print(chain.generate(wordcount))

if __name__ == "__main__":
    import sys
    run(sys.argv[1:])