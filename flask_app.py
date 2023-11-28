from flask import Flask, request, render_template
from markupsafe import escape
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from config import index_dir



app = Flask(__name__)

@app.route('/')
def home():
    return render_template('WebHTML.html')

@app.route('/search')
def search():
    query = request.args.get('q', '')
    ix = open_dir(index_dir)
    qp = QueryParser("content", schema=ix.schema)
    q = qp.parse(escape(query))
    
    results_list = []
    with ix.searcher() as searcher:
        results = searcher.search(q)
        for result in results:
            results_list.append({
                'url': result['url'],
                'title': result['title'],
                'teaser': result['teaser']
            })
    print(results_list)
    return render_template('ResultHTML.html', results_list=results_list)

if __name__ == '__main__':
    app.run(debug=True)
