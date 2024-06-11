import nltk
import json

nltk.download('punkt')

def load_data(file_path):
    lines = open(file_path, encoding='iso-8859-1').read().split('\n')
    return lines

def create_pairs(lines):
    id2line = {}
    for line in lines:
        parts = line.split(' +++$+++ ')
        if len(parts) == 5:
            id2line[parts[0]] = parts[4]

    conversations = open('cornell_movie_dialogs_corpus/movie_conversations.txt', encoding='iso-8859-1').read().split('\n')
    pairs = []
    for convo in conversations:
        parts = convo.split(' +++$+++ ')
        if len(parts) == 4:
            utterance_ids = eval(parts[-1])
            for i in range(len(utterance_ids) - 1):
                input_line = id2line.get(utterance_ids[i], '')
                target_line = id2line.get(utterance_ids[i + 1], '')
                if input_line and target_line:
                    pairs.append((input_line, target_line))

    return pairs

def tokenize_and_save(pairs, output_file):
    tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
    tokenized_pairs = []
    for pair in pairs:
        question = tokenizer.tokenize(pair[0].lower())
        answer = tokenizer.tokenize(pair[1].lower())
        tokenized_pairs.append((question, answer))

    with open(output_file, 'w') as f:
        json.dump(tokenized_pairs, f)

if __name__ == "__main__":
    lines = load_data('cornell_movie_dialogs_corpus/movie_lines.txt')
    pairs = create_pairs(lines)
    tokenize_and_save(pairs, 'tokenized_pairs.json')
