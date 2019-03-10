from flask import Flask, render_template, request, jsonify, Markup
import markdown
import spacy
import wikicrawler as wk
import wikipedia
# from Query import naive_output


nlp = spacy.load('en_coref_md')

app = Flask(__name__)
# app.config['JSON_SORT_KEYS'] = False


@app.route('/', methods=['POST', 'GET'])
def index():

    errors = []
    num = 7
    ratio = 0.1

    if request.method == "POST":
        name = request.form['text']
        try:
            origin, text = wk.replaceRefer(name)
            doc = wk.summarizer(origin, text, num)
            genDoc = wikipedia.page(name).content
            results = doc
            # gensimResults = []
            # gensimSummary = nlp(wk.summarize(genDoc))
            # i = 0
            # for sent in gensimSummary.sents:
            #     if i < num:
            #         gensimResults.append(sent.text)
            #         i += 1
            #     else:
            #         break
            gensimResults = wk.summary_highlight2(genDoc, ratio)
            results = Markup(markdown.markdown(results))
            gensimResults = Markup(markdown.markdown(gensimResults))
            return render_template('home.html', errors=errors, results=results, gensimResults=gensimResults)

        except ValueError:
            errors.append("Query: \""+name+" \"")
            errors.append("Not correct name, enter again")
            return render_template('home.html', errors=errors)

        except wikipedia.exceptions.DisambiguationError:
            errors.append("Query: \"" + name + " \"")
            errors.append("Ambiguous name, enter again")
            return render_template('home.html', errors=errors)
    else:
        errors.append("No input in the query.")
        return render_template('home.html', errors=errors)





# @app.route('/', methods=['POST', 'GET'])
# def my_form_post():
#     text = request.form['text']
#     if text is not None:
#         doc = nlp(text)
#         if doc._.has_coref:
#             mentions = [{'start': mention.start_char,
#                          'end': mention.end_char,
#                          'text': mention.text,
#                          'resolved': cluster.main.text
#                          }
#                         for cluster in doc._.coref_clusters
#                         for mention in cluster.mentions]
#             clusters = [{'cluster': cluster.main.text
#                          }
#                         for cluster in doc._.coref_clusters]
#
#
#             resolved = doc._.coref_resolved
#             return jsonify(mentions)
#             # return jsonify(clusters)
#         else:
#             # return render_template('home.html')
#             return doc.text


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)