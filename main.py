import re, os
from random import randint

ALPHAS = re.compile(r'([.!?:;,]+)')

'''
todo:
* implement precision
* add twitter functionality
'''
def makeChain(words, precision):
    keys = (' '.join(ALPHAS.split(words))).split()
    chain = {
        "START": [keys[0]],
        "END": []
    }
    for i in range(len(keys)-1):
        word = keys[i+1]
        if keys[i] not in chain:
            chain[keys[i]] = []
        if ALPHAS.match(keys[i]):
            chain["START"].append(word)
            chain["END"].append(keys[i])
        chain[keys[i]].append(word)
    
    return chain

def generate(chain, length):
    key = "START"
    count = 0
    sentence = ""
    while(count < length):
        word = chain[key][randint(0, len(chain[key]) - 1)]
        if not ALPHAS.match(word):
            sentence += " " + word
        else:
            sentence += word
        key = word
        if key not in chain or len(chain[key]) == 0:
            if count / length >= 0.75:
                break
            key = "END" if len(chain["END"]) > 0 else "START"
        count += 1

    return sentence

def run(args):
    if args is None:
        print("usage: {} <filename>, <word count>, <precision>".format(__file__))
        exit(1337)
    if type(args) is not list:
        args = [args]

    filename = args[0] if len(args) >= 1 else "lamotte.txt"
    wordcount = int(args[1]) if len(args) >= 2 else 30
    precision = int(args[2]) if len(args) >= 3 else 1

    path = os.path.abspath(__file__)
    scr_name = os.path.basename(__file__)
    with open(path.replace(scr_name, filename), 'r', encoding="utf-8") as f:
        words = f.read()

    chain = makeChain(words, precision)
    sentence = generate(chain, wordcount)
    print(sentence)

if __name__ == "__main__":
    import sys
    run(sys.argv[1:])