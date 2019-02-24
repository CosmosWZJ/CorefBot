import wikipedia
import spacy
import wikicrawler
from gensim.summarization import summarize

nlp = spacy.load('en_coref_md')
Name = "Lee Hsien Loong"
Name2 = "Halimah Yacob"
Name3 = "Jay Chou"
text = wikicrawler.replaceRefer(Name3)
text1 = text
docx = wikipedia.page(Name3).content
print("rank with clean==============================================")
wikicrawler.summarizer(text)
print("rank without clean==============================================")
wikicrawler.summarizer(docx)
print("==============================================")
print(summarize(text1))
print("==============================================")
print(summarize(docx))


