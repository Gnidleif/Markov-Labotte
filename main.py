import re, os
from random import randint

alphas = re.compile(r'([.!?:;,]+)')

def makeChain(words):
    keys = (' '.join(alphas.split(words))).split()

    chain = {
        "START": [keys[0]],
        "END": []
    }

    for i in range(len(keys)-1):
        word = keys[i+1]
        if keys[i] not in chain:
            chain[keys[i]] = []
        if alphas.match(keys[i]):
            chain["START"].append(word)
            chain["END"].append(keys[i])
        chain[keys[i]].append(word)
    
    return chain

def generate(chain, length):
    key = "START"
    sentence = ""
    while(len(sentence) < length):
        word = chain[key][randint(0, len(chain[key]) - 1)]
        if not alphas.match(word):
            sentence += " " + word
        else:
            sentence += word
        key = word
        if key not in chain or len(chain[key]) == 0:
            key = "END" if len(chain["END"]) > 0 else "START"

    return sentence

def run(args):
    path = os.path.abspath(__file__)
    scr_name = os.path.basename(__file__)
    with open(path.replace(scr_name, "words.txt"), 'r', encoding="utf-8") as f:
        words = f.read()

    chain = makeChain(words)
    sentence = generate(chain, 500)
    print(sentence)

if __name__ == "__main__":
    import sys
    run(sys.argv[1:])
