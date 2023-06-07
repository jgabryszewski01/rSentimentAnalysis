from flask import Flask, render_template, request, redirect, jsonify, send_from_directory
from textblob import TextBlob
import praw

app = Flask(__name__)

# Konfiguracja PRAW
reddit = praw.Reddit(client_id='07HBNfIvzlJ9j8PLsQG_ug',
                     client_secret='_ZwsmnYIt0rLjoPFTSXH8YgIUY4eBw',
                     user_agent='my_reddit_scraper')

# Widok główny - strona index.html
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        subreddit_name = request.form['subreddit']
        return redirect('/results/' + subreddit_name)
    return render_template('index.html')

# Funkcja obsługująca żądania dotyczące obrazów
@app.route('/images/<path:path>')
def send_image(path):
    return send_from_directory('images', path)

# Funkcja pomocnicza do oznaczania labeli sentymentu
def get_sentiment_label(sentiment_score):
    if sentiment_score < -0.4:
        return 'Negative'
    elif sentiment_score < -0.1:
        return 'Slightly negative'
    elif sentiment_score < 0.1:
        return 'Neutral'
    elif sentiment_score < 0.35:
        return 'Rather positive'
    else:
        return 'Positive'

# Funkcja pomocnicza do oznaczania labeli sentymentu
def get_sub_label(subjectivity_score):
    if subjectivity_score < 0.08:
        return 'Objective'
    elif subjectivity_score < 0.35:
         return 'Not very subjective'
    elif subjectivity_score < 0.66:
        return 'Moderly subjective'
    else:
        return 'Highly subjective'
    
# Widok wyników - strona results.html
@app.route('/results/<subreddit_name>')
def results(subreddit_name):
    # Pobieramy tytuły top 10 postów z danego subreddita
    subreddit = reddit.subreddit(subreddit_name)
    top_posts = subreddit.hot(limit=10)
    top_posts_r = subreddit.hot(limit=10)
    post_titles = []

    sentiment_sub_label = ''
    sentiment_pol_label = ''

    for post in top_posts_r:
        post_titles.append(post.title)
    
    # Łączymy wszystkie tytuły postów w jednej zmiennej i robimy na nich analize sentymentu
    post_titles_string = ' '.join(post_titles)
    subjectivity_score = TextBlob(post_titles_string).sentiment.subjectivity
    sentiment_score = TextBlob(post_titles_string).sentiment.polarity

    sentiment_pol_label = get_sentiment_label(sentiment_score)
    sentiment_sub_label = get_sub_label(subjectivity_score)

    return render_template('results.html', 
                            subreddit_name=subreddit_name,
                            top_posts=top_posts,
                            sentiment=round(sentiment_score, 2),
                            subjectivity=round(subjectivity_score, 2),
                            pol_label=sentiment_pol_label,
                            sub_label=sentiment_sub_label)

# Widok wyników (50 postów) - strona results50.html
@app.route('/results50/<subreddit_name>')
def results50(subreddit_name):
    # Pobieramy tytuły top 50 postów z danego subreddita
    subreddit = reddit.subreddit(subreddit_name)
    top_posts = subreddit.hot(limit=50)
    top_posts_r = subreddit.hot(limit=50)
    post_titles = []

    sentiment_sub_label = ''
    sentiment_pol_label = ''

    for post in top_posts_r:
        post_titles.append(post.title)
    
    # Łączymy wszystkie tytuły postów w jednej zmiennej i robimy na nich analize sentymentu
    post_titles_string = ' '.join(post_titles)
    subjectivity_score = TextBlob(post_titles_string).sentiment.subjectivity
    sentiment_score = TextBlob(post_titles_string).sentiment.polarity

    sentiment_pol_label = get_sentiment_label(sentiment_score)
    sentiment_sub_label = get_sub_label(subjectivity_score)

    return render_template('results50.html', 
                            subreddit_name=subreddit_name,
                            top_posts=top_posts,
                            sentiment=round(sentiment_score, 2),
                            subjectivity=round(subjectivity_score, 2),
                            pol_label=sentiment_pol_label,
                            sub_label=sentiment_sub_label)

# Widok i analiza sentymentu komentarzy - strona commentsResults.html
@app.route('/commentsResults/<subreddit_name>/<post_id>')
def comments_results(subreddit_name, post_id):
    # Pobieramy komentarze pod postem z danym post_id za pomocą PRAW 
    post = reddit.submission(id=post_id)
    post_title = post.title
    comments = post.comments.list()

    sentiment_scores = []
    subjectivity_scores = []
    comments_text = []

    # Komentarze wrzucamy jako tekst do jednej zmiennej i dokonujemy analizy sentymentu
    for comment in comments:
        if isinstance(comment, praw.models.Comment):
            sentiment_score = TextBlob(comment.body).sentiment.polarity
            sentiment_scores.append(sentiment_score)
            subjectivity_score = TextBlob(comment.body).sentiment.subjectivity
            subjectivity_scores.append(subjectivity_score)
            comments_text.append(comment.body)

    # Ustawiamy labele
    sentiment_pol_label = get_sentiment_label(sentiment_score)
    sentiment_sub_label = get_sub_label(subjectivity_score)

    return render_template('commentsResults.html',
                           subreddit_name=subreddit_name,
                            post_id=post_id,
                            post_title=post_title,
                            sentiment=round(sentiment_score, 2),
                            subjectivity=round(subjectivity_score, 2),
                            pol_label=sentiment_pol_label,
                            sub_label=sentiment_sub_label,
                            comments_text=comments_text)


# Widok i analiza sentymentu postu - strona postResults.html
@app.route('/postResults/<subreddit_name>/<post_id>')
def post_results(subreddit_name, post_id):
    # Pobieramy tekst postu o danym post_id za pomocą PRAW
    post = reddit.submission(id=post_id)
    post_text = post.selftext
    post_title = post.title

    # Jeśli tekst posta jest pusty, używamy tytułu posta jako post_text
    if not post_text:
        post_text = post.title

    # Analiza sentymentu tekstu posta
    sentiment_score = TextBlob(post_text).sentiment.polarity
    subjectivity_score = TextBlob(post_text).sentiment.subjectivity

    # Ustawiamy labele
    sentiment_pol_label = get_sentiment_label(sentiment_score)
    sentiment_sub_label = get_sub_label(subjectivity_score)

    return render_template('postResults.html',
                            subreddit_name=subreddit_name,
                            post_id=post_id,
                            post_title=post_title,
                            post_text=post_text,
                            sentiment=round(sentiment_score, 2),
                            subjectivity=round(subjectivity_score, 2),
                            pol_label=sentiment_pol_label,
                            sub_label=sentiment_sub_label)

if __name__ == '__main__':
    app.run(debug=True)
