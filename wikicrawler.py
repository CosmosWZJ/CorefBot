import wikipedia
import spacy

nlp = spacy.load('en_coref_md')


def wikiParser(name):
    text = wikipedia.summary(name)
    text = nlp(text)

    Chunks = list(text.noun_chunks)
    result = []
    tempChunk = Chunks[0]
    for chunk in Chunks:
        if chunk.root.head.text == "is" or chunk.root.head.text == "was" or chunk.root.head.text == tempChunk.text:
            print(chunk.text)
            result.append(chunk.text)
        tempChunk = chunk

    return result


'''find the relationship with person and noun
    if 'he is a musician', then musician is the person, which is preferred
    Dependency parse
'''