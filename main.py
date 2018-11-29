import re
from random import randint

def makeChain(words):
    rgx = re.compile(r'[^A-Za-z]')
    keys = [rgx.sub('', key) for key in words.split(' ')]

    chain = {
        "START": [keys[0]]
    }
    for i in range(len(keys)-1):
        if keys[i] not in chain:
            chain[keys[i]] = []
        if i+1 >= len(keys):
            break
        chain[keys[i]].append(keys[i+1])

    return chain

def generate(chain, length):
    key = "START"
    sentence = []
    while(len(sentence) < length):
        word = chain[key][randint(0, len(chain[key]) - 1)]
        sentence.append(word)
        key = word
        if key not in chain:
            key = "START"
    return ' '.join(sentence)

def run(args):
    words = "hi my name is Banana and I live in a box that I like very much and I can live there as long as I want"
    chain = makeChain(words)
    sentence = generate(chain, 30)
    print(sentence)

if __name__ == "__main__":
    import sys
    run(sys.argv[1:])