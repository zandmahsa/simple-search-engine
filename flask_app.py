from flask import Flask, request, render_template
from markupsafe import escape
from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser, PhrasePlugin
from whoosh.scoring import BM25F 
from config import index_dir




app = Flask(__name__)

# How many views we need: first one for homepage and second one for search

@app.route('/') # first view for showing the homepage 
def home(): # for homepage
    return render_template('WebHTML.html') 

@app.route('/search')
def search():
    query = request.args.get('q', '')
    ix = open_dir(index_dir)
   
    qp = MultifieldParser(["title", "content"], schema=ix.schema)
    qp.add_plugin(PhrasePlugin())  # Add support for phrase searching

    q = qp.parse(escape(query))

    results_list = []
    with ix.searcher(weighting=BM25F(B=0.5, K1=1.5)) as searcher:
        results = searcher.search(q)
        for result in results:
            results_list.append({
                'url': result['url'],
                'title': result['title'],
                'teaser': result['teaser']
            })

    return render_template('ResultHTML.html', results_list=results_list)

if __name__ == '__main__':
    app.run(debug=True)
