import sys
import re
import os
import json

single_modifyer_penalty = 0.5
double_modifyer_penalty = 1.5

with open(os.path.dirname(sys.argv[0]) + "/xmodsymboles.json", 'r', encoding='utf8', errors="ignore") as f:
    xmodsymboles = json.load(f)
def get_mapping(mapping):
    file = os.path.join(os.path.dirname(sys.argv[0]), 'mappings', mapping)
    keymapping = {} # Keycode -> Symboles["nomodifier", "shift", "alt", "shift-alt"]
    with open(file, 'r', encoding='utf8', errors="ignore") as f:
        for line in f:
            if(line.startswith("keycode")):
                symb = line.split()
                for i,s in enumerate(symb):
                    if type(s) == str:
                        s = s.strip()
                        if s in xmodsymboles:
                            s = xmodsymboles[s]
                        symb[i] = s
                if(len(symb)>3):
                    keymapping[int(symb[1])] = symb[3:]
    return keymapping


with open(os.path.dirname(sys.argv[0]) + "/key_score.json", 'r', encoding='utf8', errors="ignore") as f:
    key_score = json.load(f)
def generate_character_scor(keymapping):
    char_scores = {}
    for k,v in keymapping.items():
        if str(k) in key_score:
            score = key_score[str(k)]
        else:
            score = 5
        for i,char in enumerate(v):
            char_score = score
            if i > 0:
                char_score += single_modifyer_penalty
            elif i > 2:
                char_score += double_modifyer_penalty
            if char not in char_scores:
                char_scores[char] = char_score
            else:
                char_scores[char] = min(char_scores[char], char_score)
    return char_scores


def char_scores():
    mapping_scores = {}
    for mapping in os.listdir(os.path.join(os.path.dirname(sys.argv[0]), 'mappings')):
        keymapping = get_mapping(mapping)
        mapping_scores[mapping] = generate_character_scor(keymapping)
    return mapping_scores

# Generate Frequencie of Characters in all files inputed
def freq(files):
    all_freq = {} # character -> frequencie
    sum = 0
    for infile in files:
        with open(infile, "r", encoding='utf8', errors="ignore") as f:
            for i in f.read():
                sum += 1 
                if i in all_freq: 
                    all_freq[i] += 1
                else: 
                    all_freq[i] = 1
    all_freq = {k: v/sum for k, v in sorted(all_freq.items(), key=lambda item: item[1], reverse=True)}
    return all_freq, sum

with open(os.path.dirname(sys.argv[0]) + "/key_posstion.json", 'r', encoding='utf8', errors="ignore") as f:
    key_posstion = json.load(f)
def print_mapping(mapping):
    print(mapping + ":")
    mapping = get_mapping(mapping)
    for line in key_posstion:
        for i in range(2):
            for position in line:
                if position in mapping:
                    char = mapping[position][i]
                    if char in xmodsymboles:
                        print(xmodsymboles[char],end=" ")
                    else:
                        print(char,end=" ")
                else:
                    print("  ",end=" ")
            print("   ", end="")
        print()

char_scores = char_scores()
all_freq, sum = freq(sys.argv[2:])

print("Total number of Characters: " + str(sum))
mapping_score = {}
for mapping, char_score in char_scores.items():
    total_score = .0
    not_found = 0
    for k,v in all_freq.items():
        if k in char_score:
            total_score += char_score[k] * v
        else:
            not_found += 1
            total_score += 5 * v
    mapping_score[mapping] = total_score

ref = mapping_score['qwerty.xmodmap']
mapping_score = {k: v/ref for k, v in sorted(mapping_score.items(), key=lambda item: item[1])}
print("                 \t%s" % ("effort"))
for k,v in mapping_score.items():
    print("%16s:\t%0.3f" % (k, v))

print_mapping("qwerty.xmodmap")