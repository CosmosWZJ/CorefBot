import wikipedia
import spacy

nlp = spacy.load('en_coref_md')
name = "JJ lin"
text = wikipedia.summary(name)
text = nlp(text)

Chunks = list(text.noun_chunks)

tempChunk = Chunks[0]
for chunk in Chunks:
    if chunk.root.head.text == "is" or chunk.root.head.text == "was" or chunk.root.head.text == tempChunk.text:
        print(chunk.text)
    tempChunk = chunk

'''find the relationship with person and noun
    if 'he is a musician', then musician is the person, which is preferred
    Dependency parse
'''