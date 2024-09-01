import flask
from flask import Flask, render_template
import pandas as pd
import plotly
import plotly.express as px
import json
import os

from utils import score_news, visualize_sentiment

# Define base path relative to current file's location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '../assets/data')

# Load the datasets using dynamic paths
def load_data(data_path):
    full_path = os.path.join(DATA_DIR, data_path)
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"The file at {full_path} does not exist.")
    df = pd.read_csv(full_path, parse_dates=['date'])
    return df

# Load the datasets
def data():
    try:
        df = load_data('raw_analyst_ratings.csv')
        return df
    except FileNotFoundError as e:
        print(e)

df = data()
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sentiment', methods=['POST'])
def sentiment():
    print("I'm here /sentiment")
    ticker = flask.request.form['ticker'].upper()
    print(f"I'm here /sentiment2 {ticker}")

    parsed_and_scored_news = score_news(df)
    print("I'm here /sentiment")

    visualize = visualize_sentiment(parsed_and_scored_news, ticker)
    graphJSON = json.dumps(visualize, cls=plotly.utils.PlotlyJSONEncoder)

    header= "Sentiment Analysis of {} Stock".format(ticker)

    return render_template('sentiment.html', graphJSON=graphJSON, header=header)

if __name__ == '__main__':
    app.run(debug=True)