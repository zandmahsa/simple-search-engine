from flask import Flask, request, render_template_string, escape
from whoosh.index import open_dir
from whoosh.qparser import QueryParser

app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string("""
        <form action="/search">
            <input type="text" name="q" placeholder="Search here...">
            <input type="submit" value="Search">
        </form>
    """)

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

    return render_template_string("""
        <h1>Search Results</h1>
        {% for item in results_list %}
        <p><a href="{{ item.url }}">{{ item.title }}</a><br>{{ item.teaser }}</p>
        {% endfor %}
    """, results_list=results_list)

if __name__ == '__main__':
    app.run(debug=True)
