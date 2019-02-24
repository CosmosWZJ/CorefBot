import wikipedia
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
from gensim.summarization import summarize

stopwords = list(STOP_WORDS)

nlp = spacy.load('en_coref_md')

def wikiParser(name):
    page = wikipedia.page(name)
    content = nlp(page.content)
    print(content)
    sentences = [sent.string.strip() for sent in content.sents]
    for text in sentences:
        doc = nlp(text)
        relations = extractRelations(doc)
        for r1, r2 in relations:
            print('{:<10}\t{}\t{}'.format(r1.text, r2.ent_type_, r2.text))


def extractRelations(doc):
    # merge entities and noun chunks into one token
    spans = list(doc.ents) + list(doc.noun_chunks)
    for span in spans:
        span.merge()

    relations = []
    for noun in filter(lambda w: w.ent_type_ == '', doc):
        if noun.dep_ in('attr', 'dobj'):
            subject = [w for w in noun.head.lefts if w.dep_ == 'nsubj']
            if subject:
                subject = subject[0]
                relations.append((subject, noun))
            elif noun.dep_ == 'pobj' and noun.head.dep_ == 'prep':
                relations.append((noun.head.head, noun))

    return relations


def replaceRefer(name):
    page = wikipedia.page(name)
    doc = page.content
    firstPara = page.summary

    # next section is to remove the content in the bracket in the first sentence
    # in order to avoid error
    # ---------------------------------------------------------------------
    i = 0
    j = 0

    startIndexOfBracket = 0
    endIndexOfBracket = 0
    for char in firstPara:
        if char == '(':
            startIndexOfBracket = i
            break
        i += 1
    for c in firstPara:
        if c == ')':
            endIndexOfBracket = j
            break
        j += 1
    empty = ''
    doc = replace_str_index(doc, startIndexOfBracket, endIndexOfBracket+2, empty)
    # ---------------------------------------------------------------------------

    doc = nlp(doc) # doc and doc1 are clean text, doc1 is used to output the result
    origin = doc
    resolved = doc._.coref_resolved
    resolved = nlp(resolved)
    sentences = [sent.string.strip() for sent in resolved.sents]
    originSentences = [sent.string.strip() for sent in origin.sents]
    splitName = name.split(" ")
    newdoc = ""
    newdoc1 = ""
    i = 0
    indexes = []
    for sent in sentences:
        if name in sent or splitName[0] in sent or splitName[-1] in sent:
            newdoc += sent
            indexes.append(i)
        i += 1

    j = 0
    k = 0
    # now use the indexes to find original sentences
    for se in originSentences:
        if k < len(indexes) and j == indexes[k]:
            newdoc1 += se
            k += 1
        elif k >= len(indexes):
            break
        j += 1
    print("length of original text:" + str(len(page.content)))
    print("length of newdoc:" + str(len(newdoc1)))
    print(newdoc1)

    return newdoc1


def summarizer(text):
    docx = nlp(text)
    mytokens = [token.text for token in docx]
    # Build Word Frequency
    # word.text is tokenization in spacy
    word_frequencies = {}
    for word in docx:
        if word.text not in stopwords:
            if word.text not in word_frequencies.keys():
                word_frequencies[word.text] = 1
            else:
                word_frequencies[word.text] += 1
    # Maximum Word Frequency
    maximum_frequency = max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word] / maximum_frequency)
    # frequency table = word_frequency
    sentence_list = [sentence for sentence in docx.sents]
    # Sentence Score via comparing each word with sentence
    sentence_scores = {}
    for sent in sentence_list:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if len(sent.text.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word.text.lower()]
                    else:
                        sentence_scores[sent] += word_frequencies[word.text.lower()]

    summarized_sentences = nlargest(7, sentence_scores, key=sentence_scores.get)
    print(summarized_sentences)




def replace_str_index(text, index=0, end=0, replacement=''):
    return '%s%s%s'%(text[:index], replacement, text[end:])









