import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# NLTK vader for sentiment analysis
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def get_first_ten_data(df):
    return df.head(10)

def score_news(df):
    print("I'm here /score_news")

    # Instantiate the analyzer
    vader = SentimentIntensityAnalyzer()

    # Iterate through the headlines and ger score
    scores = df['headline'].apply(vader.polarity_scores).tolist()
    # Convert the 'scores' list of dicts into a DataFrame
    scores_df = pd.DataFrame(scores)
    print("I'm here /score_news scores_df")

    # Join the DataFrames of the news and the list of dicts
    parsed_and_scored_news = df.join(scores_df, rsuffix='_right')
    print("I'm here /score_news scores_df join")

    # parsed_and_scored_news = parsed_and_scored_news.set_index('datetime')
    # Convert the date column from string to datetime
    parsed_and_scored_news['date'] = pd.to_datetime(parsed_and_scored_news.date, errors='coerce').dt.date
    print("I'm here /score_news last")

    return parsed_and_scored_news

def visualize_sentiment(parsed_and_scored_news, ticker):
    num_columns = ['neg', 'neu', 'pos', 'compound']
    if parsed_and_scored_news[parsed_and_scored_news['stock'] == ticker].empty:
        return "No data available for this ticker."
    else:
        # Filter the data for the given ticker
        ticker_data = parsed_and_scored_news[parsed_and_scored_news['stock'] == ticker]

        # Group by date and calculate the mean
        mean_scores = ticker_data.groupby('date')[num_columns].mean().reset_index()

        # Plot using Plotly
        fig = px.bar(mean_scores, x='date', y=['neg', 'neu', 'pos', 'compound'], 
                     title=f'Sentiment Scores for {ticker}', 
                     labels={'value':'Sentiment Score', 'variable':'Sentiment Type'})

        return fig