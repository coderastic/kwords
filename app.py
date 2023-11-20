from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    keyword = request.form['keyword']
    timeframe = request.form['timeframe']
    geo = request.form['geo']
    api_key = 'a66213ebd5f190aa0799cade86ee877fc4bfb8b28f20010b369b20c79fdc5ca8'  # Replace with your actual API key

    keywords = get_trends(keyword, timeframe, geo, api_key)
    return render_template('results.html', keywords=keywords)

def get_trends(keyword, timeframe, geo, api_key):
    params = {
        "engine": "google_trends",
        "q": keyword,
        "hl": "en",
        "geo": geo,
        "timeframe": timeframe,
        "data_type": "RELATED_QUERIES",
        "api_key": api_key
    }
    response = requests.get('https://serpapi.com/search.json', params=params)
    if response.status_code == 200:
        data = response.json()
        related_queries = data.get('related_queries', {}).get('rising', [])
        # Extracting only the 'query' field from each item
        keywords = [item['query'] for item in related_queries][:100]  # Limit to 100 keywords
        return keywords
    else:
        return []

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
