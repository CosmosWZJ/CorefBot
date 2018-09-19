from flask import Flask, render_template, request, jsonify
import spacy
# from Query import naive_output


nlp = spacy.load('en_coref_md')

app = Flask(__name__)
# app.config['JSON_SORT_KEYS'] = False


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/', methods=['POST', 'GET'])
def my_form_post():
    text = request.form['text']
    if text is not None:
        doc = nlp(text)
        if doc._.has_coref:
            mentions = [{'start': mention.start_char,
                         'end': mention.end_char,
                         'text': mention.text,
                         'resolved': cluster.main.text
                         }
                        for cluster in doc._.coref_clusters
                        for mention in cluster.mentions]
            clusters = doc._.coref_clusters
            resolved = doc._.coref_resolved
            # return render_template('home.html' + jsonify(mentions))
            return jsonify(mentions)
        else:
            # return render_template('home.html')
            return doc.text



@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)