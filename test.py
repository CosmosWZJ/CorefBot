import wikipedia
import spacy
import wikicrawler
from gensim.summarization import summarize

nlp = spacy.load('en_coref_md')
Name = "Lee Hsien Loong"
Name2 = "Halimah Yacob"
Name3 = "Albert Einstein"

text = wikicrawler.replaceRefer(Name3)
docx = wikipedia.page(Name3).content

print("===========rank with clean==============================================")
wikicrawler.summarizer(text)

print("gensim summarize pure==============================================")
print(summarize(docx))


