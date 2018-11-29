import re
from random import randint

def run(args):
    words = "hi my name is Banana and I live in a box that I like very much and I can live there as long as I want"
    rgx = re.compile(r'[^A-Za-z]')
    keys = [rgx.sub('', key) for key in words.split(' ')]

    chain = {}
    for i in range(len(keys)-1):
        if keys[i] not in chain:
            chain[keys[i]] = []
        chain[keys[i]].append(keys[i+1])

    print(' '.join([chain[word][randint(0, len(chain[word])-1)] for word in chain]))

if __name__ == "__main__":
    import sys
    run(sys.argv[1:])