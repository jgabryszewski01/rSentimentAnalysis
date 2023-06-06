from flask import Flask, render_template, request, redirect
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

    if sentiment_score < -0.4:
        sentiment_pol_label = 'negative'
    elif sentiment_score < -0.1:
        sentiment_pol_label = 'slightly negative'
    elif sentiment_score < 0.1:
        sentiment_pol_label = 'neutral'
    elif sentiment_score < 0.35:
        sentiment_pol_label = 'slightly positive'
    else:
        sentiment_pol_label = 'positive'

    if subjectivity_score < 0.08:
        sentiment_sub_label = 'Objective titles'
    elif subjectivity_score < 0.35:
         sentiment_sub_label = 'Not very subjective titles'
    elif subjectivity_score < 0.66:
        sentiment_sub_label = 'Moderly subjective titles'
    else:
        sentiment_sub_label = 'Highly subjective titles'

    return render_template('results.html', 
                            subreddit_name=subreddit_name,
                            top_posts=top_posts,
                            sentiment = round(sentiment_score, 2),
                            sub = round(subjectivity_score, 2),
                            pol_label = sentiment_pol_label,
                            sub_label = sentiment_sub_label)

# Widok komentarzy - strona commentsResults.html
@app.route('/commentsResults/<post_id>')
def comments_results(post_id):
    postID = reddit.submission(id=post_id)
    comments = postID.comments.list()
    
    sentiment_scores = []
    for comment in comments:
        if isinstance(comment, praw.models.Comment):
            sentiment_score = TextBlob(comment.body).sentiment.polarity
            sentiment_scores.append(sentiment_score)
    
    avg_sentiment = sum(sentiment_scores) / len(sentiment_scores)
    sentiment_label = ''

    if avg_sentiment < -0.4:
        sentiment_label = 'negative'
    elif avg_sentiment < -0.1:
        sentiment_label = 'slightly negative'
    elif avg_sentiment < 0.1:
        sentiment_label = 'neutral'
    elif avg_sentiment < 0.35:
        sentiment_label = 'slightly positive'
    else:
        sentiment_label = 'positive'

    return render_template('commentsResults.html', 
                           post=postID, 
                           avg_sentiment=avg_sentiment, 
                           sentiment_label=sentiment_label)

@app.route('/postResults/<post_id>')
def post_results(post_id):
    # Pobierz tekst postu o danym post_id za pomocą API PRAW
    post = reddit.submission(id=post_id)
    post_text = post.selftext
    
    # Przeprowadź analizę sentymentu
    sentiment_score = TextBlob(post_text).sentiment.polarity
    subjectivity_score = TextBlob(post_text).sentiment.subjectivity

    sentiment_pol_label = ''
    if sentiment_score < -0.4:
        sentiment_pol_label = 'negative'
    elif sentiment_score < -0.1:
        sentiment_pol_label = 'slightly negative'
    elif sentiment_score < 0.1:
        sentiment_pol_label = 'neutral'
    elif sentiment_score < 0.35:
        sentiment_pol_label = 'slightly positive'
    else:
        sentiment_pol_label = 'positive'

    sentiment_sub_label = ''
    if subjectivity_score < 0.08:
        sentiment_sub_label = 'Objective titles'
    elif subjectivity_score < 0.35:
         sentiment_sub_label = 'Not very subjective titles'
    elif subjectivity_score < 0.66:
        sentiment_sub_label = 'Moderly subjective titles'
    else:
        sentiment_sub_label = 'Highly subjective titles'

    return render_template('postResults.html', 
                           post_id=post_id, 
                           post_text=post_text, 
                           sentiment=sentiment_score, 
                           pol_label=sentiment_pol_label, 
                           subjectivity=subjectivity_score, 
                           sub_label=sentiment_sub_label)

if __name__ == '__main__':
    app.run(debug=True)
