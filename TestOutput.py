import spacy
from spacy import displacy
nlp = spacy.load('en')

text = nlp("By 2020 the telecom company Orange, will relocate from Turkey to Orange County in the U.S. close to Apple. It will cost them about 2 million dollars.")
doc1 = nlp("There are two cup of Oolong milk tea, the first one is sweet, the second one is salt")
for word in doc1:
    print(word.text, word.pos_, word.dep_)

# displacy.render(text, style = "ent", jupyter = False)
displacy.serve(doc1, style='dep')
displacy.render(doc1, style='dep',jupyter=True)