import wikipedia
import spacy

nlp = spacy.load('en')

word = nlp('John is a Singaporean politician who is the current President of Singapore.')
doc = nlp(u'San Francisco considers banning sidewalk delivery robots')
for token in word:
    print(token.text, token.dep_, token.head.text, token.head.pos_,
          [child for child in token.children])