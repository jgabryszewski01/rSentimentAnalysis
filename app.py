from flask import Flask, render_template, request, redirect, jsonify
from textblob import TextBlob
import praw

# Inicjalizacja aplikacji Flask
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

# Funkcja pomocnicza do oznaczania etykiet sentymentu
def get_sentiment_label(sentiment_score):
    if sentiment_score < -0.4:
        return 'Negative'
    elif sentiment_score < -0.1:
        return 'Slightly negative'
    elif sentiment_score < 0.1:
        return 'Neutral'
    elif sentiment_score < 0.35:
        return 'Slightly positive'
    else:
        return 'Positive'

# Funkcja pomocnicza do oznaczania etykiet sentymentu
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
    subreddit = reddit.subreddit(subreddit_name)
    top_posts = subreddit.hot(limit=10)
    top_posts_r = subreddit.hot(limit=10)
    post_titles = []
    sentiment_sub_label = ''
    sentiment_pol_label = ''
    for post in top_posts_r:
        post_titles.append(post.title)
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

# Widok komentarzy - strona commentsResults.html
@app.route('/commentsResults/<post_id>')
def comments_results(post_id):
    post = reddit.submission(id=post_id)
    post_title = post.title
    comments = post.comments.list()

    sentiment_scores = []
    subjectivity_scores = []
    for comment in comments:
        if isinstance(comment, praw.models.Comment):
            sentiment_score = TextBlob(comment.body).sentiment.polarity
            sentiment_scores.append(sentiment_score)
            subjectivity_score = TextBlob(comment.body).sentiment.subjectivity
            subjectivity_scores.append(subjectivity_score)

    sentiment_pol_label = get_sentiment_label(sentiment_score)
    sentiment_sub_label = get_sub_label(subjectivity_score)

    return render_template('commentsResults.html',
                            post_id=post_id,
                            post_title=post_title,
                            sentiment=round(sentiment_score, 2),
                            subjectivity=round(subjectivity_score, 2),
                            pol_label=sentiment_pol_label,
                            sub_label=sentiment_sub_label)

@app.route('/postResults/<post_id>')
def post_results(post_id):
    # Pobierz tekst postu o danym post_id za pomocą API PRAW
    post = reddit.submission(id=post_id)
    post_text = post.selftext
    post_title = post.title

    # Jeśli tekst posta jest pusty, użyj tytułu posta jako post_text
    if not post_text:
        post_text = post.title

    # Przeprowadź analizę sentymentu
    sentiment_score = TextBlob(post_text).sentiment.polarity
    subjectivity_score = TextBlob(post_text).sentiment.subjectivity

    sentiment_pol_label = get_sentiment_label(sentiment_score)
    sentiment_sub_label = get_sub_label(subjectivity_score)

    return render_template('postResults.html',
                           post_id=post_id,
                           post_title=post_title,
                           post_text=post_text,
                           sentiment=sentiment_score,
                           pol_label=sentiment_pol_label,
                           subjectivity=subjectivity_score,
                           sub_label=sentiment_sub_label)

if __name__ == '__main__':
    app.run(debug=True)
