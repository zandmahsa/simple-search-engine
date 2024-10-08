
from flask import Flask, request, render_template, url_for 
from markupsafe import escape
from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser, PhrasePlugin
from whoosh.scoring import BM25F 
from config import index_dir


# Creates an instance
app = Flask(__name__) 

# Decorator for defines the route of homepage 
@app.route('/')

# For homepage
def home(): 

    # Renders the WebHTML.html template after homepage is accessed
    return render_template('WebHTML.html', search_url = url_for('search'))  


# Route for the search
@app.route('/search') 

# To handles search requests
def search(): 

    # Retrieves the search query from the request's query parameters q
    query = request.args.get('q', '')

    # Opens the Whoosh index directory
    ix = open_dir(index_dir)
   
    # consider multiple aspects of the documentsthat users can find relevant results based on matches in either the title or the content
    qp = MultifieldParser(["title", "content"], schema=ix.schema)

    # Parse phrase queries
    qp.add_plugin(PhrasePlugin())  

    # Parses the sanitized user query
    q = qp.parse(escape(query))

    # An empty list to store search results
    results_list = []

    # Searching and Processing Results
    # weighting=BM25F(B=0.5, K1=1.5) Opens a searcher with custom BM25F settings for weighting
    # B=0.5: it adjusts how much the length of a field influences its relevance score
    # K1=1.5: it controls how the term frequency influences the score

    with ix.searcher(weighting=BM25F(B=0.5, K1=1.5)) as searcher:
        results = searcher.search(q)
        for result in results:
            results_list.append({
                'url': result['url'],
                'title': result['title'],
                'teaser': result['teaser']
            })
    # Returning Search Results
    return render_template('ResultHTML.html', results_list=results_list)

if __name__ == '__main__':
    #Runs the Flask app with debug mode enabled (for  detailed error messages and live reloading)
   app.run(debug=True)
