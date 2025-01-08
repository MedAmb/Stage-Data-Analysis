import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def load_and_prepare_data(filepath):
    # Load the JSON data
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Convert JSON data to DataFrame
    df = pd.DataFrame(data)

    # Filter out rows where 'Result' is not 'support', 'oppose', 'neutral', 'not_relevant', or 'unknown'
    df = df[df['Result'].isin(['support', 'oppose', 'neutral', 'not_relevant', 'unknown'])]

    # Convert 'time' column to datetime
    df['time'] = pd.to_datetime(df['time'])

    # Convert interaction columns to numeric
    df['Retweets'] = pd.to_numeric(df['Retweets'], errors='coerce').fillna(0)
    df['Comments'] = pd.to_numeric(df['Comments'], errors='coerce').fillna(0)
    df['likes'] = pd.to_numeric(df['likes'], errors='coerce').fillna(0)

    return df

def calculate_weighted_score(df, retweet_weight, comment_weight, like_weight, use_log=False, normalize=False):
    if use_log:
        # Apply logarithmic scaling to interactions
        df['log_retweets'] = np.log1p(df['Retweets'])
        df['log_comments'] = np.log1p(df['Comments'])
        df['log_likes'] = np.log1p(df['likes'])
        df['weighted_score'] = 1 + (df['log_retweets'] * retweet_weight +
                                    df['log_comments'] * comment_weight +
                                    df['log_likes'] * like_weight)
    elif normalize:
        # Normalize interaction columns
        scaler = MinMaxScaler()
        df[['Retweets', 'Comments', 'likes']] = scaler.fit_transform(df[['Retweets', 'Comments', 'likes']])
        df['weighted_score'] = 1 + (df['Retweets'] * retweet_weight +
                                    df['Comments'] * comment_weight +
                                    df['likes'] * like_weight)
    else:
        # Calculate weighted score with a base score of 1
        df['weighted_score'] = 1 + (df['Retweets'] * retweet_weight +
                                    df['Comments'] * comment_weight +
                                    df['likes'] * like_weight)
    return df

def plot_monthly_counts(df, title, filename):
    # Filter out rows where 'Result' is not 'support', 'oppose', or 'neutral'
    df = df[df['Result'].isin(['support', 'oppose', 'neutral'])]

    # Extract month and year from 'time' column
    df['month'] = df['time'].dt.strftime('%Y-%m')

    # Group by month and Result, summing the weighted scores
    monthly_counts = df.groupby(['month', 'Result'])['weighted_score'].sum().unstack(fill_value=0)

    # Plot the data
    plt.figure(figsize=(12, 6))
    monthly_counts.plot(kind='line', marker='o')
    plt.title(title)
    plt.xlabel('Month')
    plt.ylabel('Weighted Score')
    plt.legend(title='Result')
    plt.grid(True)

    # Increase the precision of the x-axis
    plt.xticks(ticks=range(len(monthly_counts.index)), labels=monthly_counts.index, rotation=45)

    plt.tight_layout()

    # Save the plot
    plt.savefig(filename)

    # Show the plot
    plt.show()

def plot_equal_tweets(df, title, filename):
    # Filter out rows where 'Result' is not 'support', 'oppose', or 'neutral'
    df = df[df['Result'].isin(['support', 'oppose', 'neutral'])]

    # Extract month and year from 'time' column
    df['month'] = df['time'].dt.strftime('%Y-%m')

    # Group by month and Result, counting the number of tweets
    monthly_counts = df.groupby(['month', 'Result']).size().unstack(fill_value=0)

    # Plot the data
    plt.figure(figsize=(12, 6))
    monthly_counts.plot(kind='line', marker='o')
    plt.title(title)
    plt.xlabel('Month')
    plt.ylabel('Number of Tweets')
    plt.legend(title='Result')
    plt.grid(True)

    # Increase the precision of the x-axis
    plt.xticks(ticks=range(len(monthly_counts.index)), labels=monthly_counts.index, rotation=45)

    plt.tight_layout()

    # Save the plot
    plt.savefig(filename)

    # Show the plot
    plt.show()

def plot_histograms(df, title, filename):
    # Filter out rows where 'Result' is not 'support' or 'oppose'
    df = df[df['Result'].isin(['support', 'oppose'])]

    # Extract month and year from 'time' column
    df['month'] = df['time'].dt.strftime('%Y-%m')

    # Group by month, Result, and Language, counting the number of tweets
    monthly_counts = df.groupby(['month', 'Result', 'Language']).size().unstack(fill_value=0)

    # Plot the data
    months = df['month'].unique()
    fig, ax = plt.subplots(figsize=(15, 8))
    bar_width = 0.2
    index = np.arange(len(months))

    support_arabic_counts = []
    support_english_counts = []
    oppose_arabic_counts = []
    oppose_english_counts = []

    for month in months:
        if month in monthly_counts.index:
            data = monthly_counts.loc[month]
            support_arabic_counts.append(data.loc['support', 'AR'])
            support_english_counts.append(data.loc['support', 'EN'])
            oppose_arabic_counts.append(data.loc['oppose', 'AR'])
            oppose_english_counts.append(data.loc['oppose', 'EN'])
        else:
            support_arabic_counts.append(0)
            support_english_counts.append(0)
            oppose_arabic_counts.append(0)
            oppose_english_counts.append(0)

    bar1 = ax.bar(index - 1.5 * bar_width, support_arabic_counts, bar_width, label='Support - Arabic', color='blue')
    bar2 = ax.bar(index - 0.5 * bar_width, support_english_counts, bar_width, label='Support - English', color='lightblue')
    bar3 = ax.bar(index + 0.5 * bar_width, oppose_arabic_counts, bar_width, label='Oppose - Arabic', color='red')
    bar4 = ax.bar(index + 1.5 * bar_width, oppose_english_counts, bar_width, label='Oppose - English', color='pink')

    ax.set_xlabel('Month')
    ax.set_ylabel('Number of Tweets')
    ax.set_title(title)
    ax.set_xticks(index)
    ax.set_xticklabels(months, rotation=45)
    ax.legend()

    plt.tight_layout()
    plt.savefig(filename)
    plt.show()

def get_top_tweets(df, use_weighted_score=True):
    top_tweets = {}
    df['month'] = df['time'].dt.strftime('%Y-%m')
    for month in df['month'].unique():
        top_tweets[month] = {}
        for result in df['Result'].unique():
            if use_weighted_score:
                top_tweets[month][result] = df[(df['month'] == month) & (df['Result'] == result)].nlargest(20, 'weighted_score')[['content', 'tweet link', 'weighted_score']].to_dict(orient='records')
            else:
                top_10_earliest = df[(df['month'] == month) & (df['Result'] == result)].nsmallest(10, 'time')[['content', 'tweet link', 'time']].to_dict(orient='records')
                top_10_latest = df[(df['month'] == month) & (df['Result'] == result)].nlargest(10, 'time')[['content', 'tweet link', 'time']].to_dict(orient='records')
                top_tweets[month][result] = top_10_earliest + top_10_latest
    return top_tweets

def save_top_tweets(result_tweets, filename):
    # Convert Timestamps to strings
    for month in result_tweets:
        for result in result_tweets[month]:
            for tweet in result_tweets[month][result]:
                if 'time' in tweet and isinstance(tweet['time'], pd.Timestamp):
                    tweet['time'] = tweet['time'].isoformat()

    with open(f'{filename}.json', 'w', encoding='utf-8') as f:
        json.dump(result_tweets, f, ensure_ascii=False, indent=4)

def main():
    filepath = '../DataAnalysis/analysis_result/results.json'
    df = load_and_prepare_data(filepath)

    plot_histograms(df.copy(), 'Monthly Support and Opposition Tweets by Language', 'tweets_histogram')

    # Define weights
    retweet_weight = 3
    comment_weight = 2
    like_weight = 1

    # Original weighted score
    df_original = calculate_weighted_score(df.copy(), retweet_weight, comment_weight, like_weight)
    plot_monthly_counts(df_original, 'Evolution of Support and Opposition Tweets (Original)', 'tweets_evolution_original.png')
    top_tweets_original = get_top_tweets(df_original)
    save_top_tweets(top_tweets_original, 'original')

    # Logarithmic scaling
    df_log = calculate_weighted_score(df.copy(), retweet_weight, comment_weight, like_weight, use_log=True)
    plot_monthly_counts(df_log, 'Evolution of Support and Opposition Tweets (Logarithmic Scaling)', 'tweets_evolution_log.png')
    top_tweets_log = get_top_tweets(df_log)
    save_top_tweets(top_tweets_log, 'logarithmic')

    # Normalization
    df_normalized = calculate_weighted_score(df.copy(), retweet_weight, comment_weight, like_weight, normalize=True)
    plot_monthly_counts(df_normalized, 'Evolution of Support and Opposition Tweets (Normalized)', 'tweets_evolution_normalized.png')
    top_tweets_normalized = get_top_tweets(df_normalized)
    save_top_tweets(top_tweets_normalized, 'normalized')

    # Equal tweets (no interaction consideration)
    plot_equal_tweets(df.copy(), 'Evolution of Support and Opposition Tweets (Equal Weight)', 'tweets_evolution_equal.png')
    top_tweets_equal = get_top_tweets(df.copy(), use_weighted_score=False)
    save_top_tweets(top_tweets_equal, 'equal')

    plot_histograms(df.copy(), 'Monthly Support and Opposition Tweets by Language', 'tweets_histogram')

if __name__ == "__main__":
    main()