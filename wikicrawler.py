from __future__ import unicode_literals
import wikipedia
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
from gensim.summarization.textcleaner import clean_text_by_sentences as _clean_text_by_sentences
from gensim.summarization.summarizer import _format_results
from gensim.summarization.summarizer import summarize

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


def summary_highlight1(origin, summary):
    original_sents = [st.text for st in origin.sents]
    summarized_sents = summary

    index = 0
    for i in original_sents:
        if index >= len(summarized_sents) - 1:
            break
        for sent in summarized_sents:
            try:
                if sent in i:
                    original_index = original_sents.index(i)
                    i = '<mark><em>' + i + '</em></mark>'
                    original_sents[original_index] = i
                    if index < len(summarized_sents) - 1:
                        index += 1

            except IndexError:
                pass
    return " ".join(original_sents)


def summary_highlight2(origin, ratio):
    summarized_sents = summarize(origin, ratio)

    original_sents = _format_results(_clean_text_by_sentences(origin), True)
    extracted_sents = _format_results(_clean_text_by_sentences(summarized_sents), True)

    index = 0
    for i in original_sents:
        try:
            if index >= len(summarized_sents) - 1:
                break
            if i == extracted_sents[index]:
                original_index = original_sents.index(i)
                i = '<mark><em>' + i + '</em></mark>'
                original_sents[original_index] = i
                if index < len(summarized_sents) - 1:
                    index += 1
        except IndexError:
            pass
    return " ".join(original_sents)
# def extractRelations(doc):
#     # merge entities and noun chunks into one token
#     spans = list(doc.ents) + list(doc.noun_chunks)
#     for span in spans:
#         span.merge()
#
#     relations = []
#     for noun in filter(lambda w: w.ent_type_ == '', doc):
#         if noun.dep_ in('attr', 'dobj'):
#             subject = [w for w in noun.head.lefts if w.dep_ == 'nsubj']
#             if subject:
#                 subject = subject[0]
#                 relations.append((subject, noun))
#             elif noun.dep_ == 'pobj' and noun.head.dep_ == 'prep':
#                 relations.append((noun.head.head, noun))
#
#     return relations


def replaceRefer(name):
    page = wikipedia.page(name)
    doc = page.content
    name = page.title
    firstPara = page.summary
    doc = doc.replace('=', '')


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
    #print(newdoc1)

    return origin, newdoc1


def summarizer(origintext, text, ratio):
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
    num_of_sents = 0

    for sent in sentence_list:
        num_of_sents += 1
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                leng = len(sent.text.split(' '))
                if num_of_sents < 2 or leng in range(4, 40):
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word.text.lower()]
                    else:
                        sentence_scores[sent] += word_frequencies[word.text.lower()]

    pos = 0
    for sent in sentence_list:
        if sent in sentence_scores.keys():
            if num_of_sents < 100:
                sentence_scores[sent] += 4 - pos
            else:
                sentence_scores[sent] += 8 - 2*pos
        pos += 1

    summarized_sentences = nlargest(ratio, sentence_scores, key=sentence_scores.get)
    summarized_sentences = [sent.text for sent in summarized_sentences]
    print(summarized_sentences)

    return summary_highlight1(origintext, summarized_sentences)





def replace_str_index(text, index=0, end=0, replacement=''):
    return '%s%s%s'%(text[:index], replacement, text[end:])









