import sys
import os
from glob import glob
from collections import Counter

import Mecab

def main():
    input_dir = sys.argv[1]
    tagger = Mecab.Tagger('')
    tagger.parse('')

    frecuency = Counter()
    count_processed = 0

    for path in glob(os.path.join(input_dir, '*', 'wiki_*')):
        print('processing {0}...'.format(path), file=sys.stderr)

        with open(path) as file:
            for content in iter_docs(file):
                tokens = get_tokens(tagger, content)
                frecuency.update(tokens)

                count_processed += 1
                if count_processed % 1000 == 0:
                    print
                
    for tokens, count in frecuency.most_common(30):
        print(token, count)


def iter_docs(file):
    for line in file:
        if line.startswith('<doc'):
            buffer = []
        elif line.startswith('</doc>'):
            content = ''.join(buffer)
            yield content
        else:
            buffer.append(line)


def get_tokens(tagger, content):
    tokens = []
    node = tagger.parseToNode(content)
    while node:
        category, sub_category = node.feature.split(',')[:2]
        if category == '名詞' and sub_category in ('固有名詞', '一般名詞'):
            tokens.append(node.surface)
        node = node.next

    return tokens

if __name__ == '__main__':
    main()