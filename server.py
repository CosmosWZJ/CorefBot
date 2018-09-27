from flask import Flask, render_template, request, jsonify
import spacy
# from Query import naive_output


nlp = spacy.load('en_coref_md')

app = Flask(__name__)
# app.config['JSON_SORT_KEYS'] = False


@app.route('/', methods=['POST', 'GET'])
def index():

    errors = []
    results = {}

    if request.method == "POST":
        text = request.form['text']
        doc = nlp(text)
        # mentions = [{'start': mention.start_char,
        #              'end': mention.end_char,
        #              'text': mention.text,
        #              'resolved': cluster.main.text
        #              }
        #             for cluster in doc._.coref_clusters
        #             for mention in cluster.mentions]
        # clusters = [{'cluster': cluster.main.text
        #              }
        #             for cluster in doc._.coref_clusters]
        #
        # resolved = doc._.coref_resolved
        # r = request.get(text)
        # print(r.text)
        if doc._.has_coref:
            # results = [{'start': mention.start_char,
            #             'end': mention.end_char,
            #             'text': mention.text,
            #             'resolved': cluster.main.text
            #             }
            #            for cluster in doc._.coref_clusters
            #            for mention in cluster.mentions]
            results = [[mention for mention in cluster.mentions]
                       for cluster in doc._.coref_clusters]
            return render_template('home.html', errors=errors, results=results)
        else:
            errors.append("Query: \""+text+" \"")
            errors.append("No coreference or input in the query.")
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