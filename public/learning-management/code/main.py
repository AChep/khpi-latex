import matplotlib.pyplot as plt

import spacy
import json

# Load English tokenizer, tagger, parser, NER and word vectors
nlp = spacy.load("en_core_web_sm")

def plot_freq(freq):
    y = sorted([v for k, v in freq.items()])
    x = list(range(len(y)))
    plt.plot(x, y)
    plt.show()

def process_freq(dataset, clickbaitness):
    freq = dict()
    
    nlp_dataset = map(lambda x: nlp(x.lower()), dataset)
    lemma_dataset = list(map(lambda x: [token.lemma_ for token in x], nlp_dataset))

    q_global = 1.0 / len(lemma_dataset)

    for i, lemmas in enumerate(lemma_dataset):
        for lemma in lemmas:
            # The clickbaitness of the words
            q = q_global / len(lemmas) 
            q *= clickbaitness[i] * 2.0 - 1.0

            # Add up the frequencies  
            if lemma in freq:
                freq[lemma] += q
            else:
                freq[lemma] = q

    freq_values = [abs(v) for k, v in freq.items()]
    freq_values_avg = sum(freq_values) / len(freq_values) * 2
    
    # Plot the frequency before 
    # trimming.
    if True:
        plot_freq(freq)

    # clean up
    freq = {k: v for k, v in freq.items() if abs(v) >= freq_values_avg}
    
    # Plot the frequency after 
    # trimming.
    if True:
        plot_freq(freq)

    return freq

def clickbaitness(freq, title):
    def aa(word):
        sum = 0.0
        lemma = word.lemma_

        # Sum all of the frequences.
        if lemma in freq:
            sum += freq[lemma]
        
        return sum

    nlp_title = nlp(title)
    return sum(map(lambda x: aa(x), nlp_title))

train_dataset = open('train_dataset.jsonl').readlines()
train_truth = open('train_truth.jsonl').readlines()

train_dataset_processed = list(map(
    lambda x: json.loads(x)['targetTitle'],
    train_dataset
))
train_truth_processed = list(map(
    lambda x: float(json.loads(x)['truthMean']),
    train_truth
))

out = []
for i in range(len(train_dataset_processed)):
    j = {
        "text": train_dataset_processed[i],
        "label": "clickbait" if train_truth_processed[i] > 0.5 else "normal"
    }
    s = json.dumps(j)
    out.append(s)

with open('somefile.txt', 'a') as the_file:
    the_file.write('\n'.join(out))

import csv

with open('somefile_2.csv', mode='w') as employee_file:
    employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for i in range(len(train_dataset_processed)):
        employee_writer.writerow([
            train_dataset_processed[i],
            "clickbait" if train_truth_processed[i] > 0.5 else "normal"
        ])

quit()

x = process_freq(train_dataset_processed, train_truth_processed)
# print(x)

l = 0
m = 0

for i in range(len(train_dataset_processed)):
    a = clickbaitness(x, train_dataset_processed[i]) > 0
    b = train_truth_processed[i] > 0.5
    if a == b:
        # print('Success')
        l += 1
    else:
        # print('Fail')
        m += 1

print(l)
print(m)

print(clickbaitness(x, 'wtf'))

