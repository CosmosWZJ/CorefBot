import wikipedia
import spacy

nlp = spacy.load('en_coref_md')

def wikiParser(name):
    page = wikipedia.page(name)
    links = page.links
    content = nlp(page.content)
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










# def wikiParser(name):
#     text = wikipedia.summary(name)
#     text = nlp(text)
#
#     Chunks = list(text.noun_chunks)
#     result = []
#     tempChunk = Chunks[0]
#     for chunk in Chunks:
#         if chunk.root.head.text == "is" or chunk.root.head.text == "was" or chunk.root.head.text == tempChunk.text:
#             print(chunk.text)
#             result.append(chunk.text)
#         tempChunk = chunk
#
#     return result


'''find the relationship with person and noun
    if 'he is a musician', then musician is the person, which is preferred
    Dependency parse
'''