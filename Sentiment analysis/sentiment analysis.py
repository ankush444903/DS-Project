
import streamlit as st
import tweepy
from textblob import TextBlob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import re
import plotly.express as px
import datetime as dt
import datetime
import pytz
import string,time
import gender_guesser.detector as gender



def add_bg_from_url():
    st.markdown(
        f"""
            <style>
            .stApp {{
                background-image: url("https://zeevector.com/wp-content/uploads/Colorful-Background-HD-768x584.png");
                background-attachment: fixed;
                background-size: cover
            }}
            </style>
            """,
        unsafe_allow_html=True
    )
add_bg_from_url()

def add_logo(logo_url):
    st.markdown(
        f"""
        <style>
        .logo {{
            background-image: url("{logo_url}");
            background-repeat: no-repeat;
            background-position: center center;
            width: 250px;
            height: 190px;
            }}
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown('<div class="logo"></div>', unsafe_allow_html=True)

add_logo("data:image/jpeg;base64,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")
st.title("Sentiment-Analysis ")



# Authenticate with Twitter API
consumer_key = 'p9kM0GZhaR5AXAfjMKwM'
consumer_secret = 'O7RjT07Sr3DMgIJQ4D3a9Cu7O7ZnoK62TV6LXyNTHR2e'
access_token = '1636272844KLyraUEZ4RFZOu9DyNi6eK55f7'
access_token_secret = 'FY4EpDeylRWsYrNIlrcJuz3M2NX2ud'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
#twitterAccount = input("Serach hear ")


twitterAccount = st.text_input("Enter Product Name:")
since_date = st.text_input("Start Date to (DD-MM-YYYY):")
until_date = st.text_input("End Date (DD-MM-YYYY):")
search_button = st.button("Search")

if search_button:
    # Convert date strings to datetime objects
    since_date = pd.to_datetime(since_date, format='%d-%m-%Y')
    until_date = pd.to_datetime(until_date, format='%d-%m-%Y')


    # Retrieve tweets
    tweets = api.search_tweets(twitterAccount, count=50, lang='en')  # only english twittes

    if not tweets:
         print('Please enter correct product Name.')
    else:
        tweet_data = []
        today = datetime.datetime.now(pytz.UTC)
        gender_detector = gender.Detector()  # create gender detector object
        df = pd.DataFrame()
        for tweet in tweets:
            gender_guess = gender_detector.get_gender(tweet.user.name.split()[0]) # infer gender from first name
            if gender_guess == "unknown":
                gender_guess = None # set to None if gender cannot be inferred
            data = {
                'Username': tweet.user.screen_name,
                'Name': tweet.user.name,
                'Account Created at': tweet.user.created_at,
                'Age of Account(Days)': (today - tweet.user.created_at.replace(tzinfo=pytz.UTC)).days,
                'Description': tweet.user.description,
                'Followers count': tweet.user.followers_count,
                'Location': tweet.user.location,
                'Date': tweet.created_at,
                'Week': pd.to_datetime(tweet.created_at).week,
                'Month': pd.to_datetime(tweet.created_at).month,
                'Quarter': pd.to_datetime(tweet.created_at).quarter,
                'Tweets': tweet.text,
                'Retweet': tweet.retweet_count,
                'Favorite count(Like)': tweet.favorite_count,
                'Gender': gender_guess

            }
            tweet_data.append(data)
        df = df.append(tweet_data)



        # Define function to clean up tweet text
        def cleanUpTweet(txt):
            txt = re.sub(r'@[A-Za-z0-9_]+', '', txt)
            txt = re.sub(r'#', '', txt)
            txt = re.sub(r'RT: ', '', txt)
            txt = re.sub(r'https?:\/\/[A-Za-z0-9\.\/%\n]+', '', txt)
            return txt
        df['tweets'] = df['Tweets'].apply(cleanUpTweet)

# Clean up tweet text in dataframe
        df['tweets'] = df['tweets'].str.lower()

# Define function to remove punctuation
        exclude = string.punctuation

        df['Gender'] = df['Gender'].replace(['mostly_male'], 'Unknown')
        df['Gender'] = df['Gender'].replace(['mostly_female'], 'Unknown')
        
        def remove_punc1(text):
            return text.translate(str.maketrans('', '', exclude))


        # Remove punctuation in tweet text in dataframe
        df['tweets'] = df['tweets'].apply(remove_punc1)


        # Define function to determine if tweet is fake
        def is_fake_tweet(tweet):
            # Add your criteria for fake tweets here
            if tweet['Username'] == 'fakeuser':
                return True
            else:
                return False


        # Add column indicating whether each tweet is fake
        df['Fake'] = df.apply(is_fake_tweet, axis=1)
        #st.write(df.head(2))
        #

        import emoji  # replace emoji
        df['tweets']=emoji.demojize(df['tweets'])# here replace emoji

        #st.write(df.head(3))
        import nltk
        #
        nltk.download('stopwords')
        # Load the stopwords
        stop_words = set(stopwords.words('english'))
        from nltk.corpus import stopwords
        # Remove stopwords from the tweets column
        df['tweets'] = df['tweets'].apply(lambda x: ' '.join([word for word in x.split() if word.lower() not in stop_words]))
        ps=PorterStemmer
        def stem_words(text):
                   return" ".join([ps.stem(words) for words in text.split()])
        
        import nltk
        nltk.download('punkt')
        # # # Load the stemmer and stopwords
        stemmer = PorterStemmer()
        stop_words = set(nltk.corpus.stopwords.words('english'))
        # #
        # # # Define a function to stem words in a given string
        def stem_words(lda_model):
                  words = nltk.word_tokenize(lda_model)
                  stemmed_words = [stemmer.stem(word) for word in words if word not in stop_words]
                  return ' '.join(stemmed_words)
        # Apply the stem_words function to the tweets column
         df['tweets'] = df['tweets'].apply(stem_words)
        # skip First Tweets Column
        df = df.drop('Tweets', axis=1)
        #st.write(df.head(5))

    def remove_stopwords(text):
     new_text = []

     for word in text.split():
         if word in stopwords.words('english'):
             new_text.append('')
         else:
             new_text.append(word)
     x = new_text[:]
     new_text.clear()
     return " ".join(x)

        df['tweets']=df['tweets'].apply(remove_stopwords)
        df['date'] = df['Date'].dt.date
        df['time'] = df['Date'].dt.time

        # Drop the original datetime column
        df.drop('Date', axis=1, inplace=True)
        df.drop('Username', axis=1, inplace=True)

        def getTextSubjectivity(txt):
            return TextBlob(txt).sentiment.subjectivity
        df['Subjectivity']=df['tweets'].apply(getTextSubjectivity)

        def getTextPolarity(txt):
            return TextBlob(txt).sentiment.polarity
        df['Polarity']=df['tweets'].apply(getTextPolarity)
        def getTextAnalysis(a):
            if a<0:
                return 'Negative'
            elif a==0:
                return  'Neutral'
            else:
                return 'Positive'

        df['score']=df['Polarity'].apply(getTextAnalysis)
       # st.write(df.head(2))
        st.title("Overall Sentiment of Tweets")
        fig = px.pie(df, values=df['score'].value_counts(), names=df['score'].value_counts().index)
        st.plotly_chart(fig)



    if 'Neutral' in df['score'].tolist():
        Neutral = df[df['score'] == 'Neutral']['tweets'].tolist()

        # Combine all Neutral sentences into a single string
        Neutral_text = ' '.join(Neutral)

        # Create a WordCloud object for Neutral sentences
        Neutral_wordcloud = WordCloud(width=800, height=800, background_color='white', min_font_size=10).generate(
            Neutral_text)

        # Display the word cloud for Neutral sentences
        st.title('Neutral Word')
        plt.figure(figsize=(6, 6))
        plt.imshow(Neutral_wordcloud)
        plt.axis("off")
        plt.tight_layout(pad=0)
        st.pyplot(plt)
    else:
        st.write('No Neutral sentiment of your product')


    df_pos = df[df['score'] == 'Neutral']  # filter only Neutral tweets
    df_top5_pos = df_pos.sort_values('Polarity', ascending=False).head(5)  # sort by Polarity and get top 5

    if not df_top5_pos.empty:
        st.title('Top 5 Neutral Tweets')
        #st.dataframe(df_top5_pos)
        st.dataframe(df_top5_pos.loc[:, ['Name','tweets','score']])
    else:
        st.write('No Neutral tweets found')


    if 'Positive' in df['score'].tolist():
        positive = df[df['score'] == 'Positive']['tweets'].tolist()

        # Combine all positive sentences into a single string
        positive_text = ' '.join(positive)

        # Create a WordCloud object for positive sentences
        positive_wordcloud = WordCloud(width=800, height=800, background_color='white', min_font_size=10).generate(
            positive_text)

        # Display the word cloud for positive sentences
        import matplotlib.pyplot as plt

        plt.figure(figsize=(6, 8))
        plt.imshow(positive_wordcloud)
        plt.axis("off")
        plt.tight_layout(pad=0)
        st.title('Positive Word')
        st.pyplot(plt)
    else:
        st.write('No Positive sentiment of your product')



    df_pos = df[df['score'] == 'Positive']  # filter only positive tweets
    df_top5_pos = df_pos.sort_values('Polarity', ascending=False).head(5)  # sort by Polarity and get top 5

    if not df_top5_pos.empty:
        st.title('Top 5 Positive Tweets')
        #st.dataframe(df_top5_pos)
        st.dataframe(df_top5_pos.loc[:, ['Name', 'tweets', 'score']])
    else:
        st.write('No Positive tweets found')

    # Check if there are any negative sentiments in the DataFrame
    if 'Negative' in df['score'].tolist():
        # Filter for negative sentiments
        Negative = df[df['score'] == 'Negative']['tweets'].tolist()

        # Combine all negative sentences into a single string
        Negative_text = ' '.join(Negative)

        # Create a WordCloud object for negative sentences
        Negative_wordcloud = WordCloud(width=800, height=800, background_color='white', min_font_size=10).generate(
            Negative_text)

        # Display the word cloud for negative sentences
        plt.figure(figsize=(6, 8))
        plt.imshow(Negative_wordcloud)
        plt.axis("off")
        plt.tight_layout(pad=0)
        st.title('Negative Word')
        st.pyplot(plt)

    else:
        st.write('No negative sentiment of your product')


    df_neg = df[df['score'] == 'Negative']  # filter only negative tweets
    df_top5_neg = df_neg.sort_values('Polarity', ascending=False).head(5)  # sort by Polarity and get top 5

    if not df_top5_neg.empty:
        st.title('Top 5 Negative Tweets')
        #st.dataframe(df_top5_neg)
        st.dataframe(df_top5_neg.loc[:, ['Name', 'tweets', 'score']])
    else:
        st.write('No Negative tweets found')

            # # Bar chart of score column
            df['Location'] = df['Location'].apply(lambda x: "Other" if x.strip() == "" else x)
            st.title('Location Wise Tweets')
            data = df.groupby('Location')['tweets'].count().reset_index()
            data = data.sort_values('tweets', ascending=False)  # sort by tweet count in descending order
            fig, ax = plt.subplots()
            ax.barh(data['Location'], data['tweets'], color="green")
            ax.set_xlabel('Number of tweets')
            ax.set_ylabel('Location')
            st.pyplot(fig)

    # Pie chart of score column
    fig = px.pie(df, values=df['date'].value_counts(), names=df['date'].value_counts().index)
    st.title("Last Week Tweets")
    st.plotly_chart(fig)

    fig = px.pie(df, values=df['Month'].value_counts(), names=df['Month'].value_counts().index)
    st.subheader("Pie Chart Month wise tweets")
    st.plotly_chart(fig)

    import calendar

    grouped_data = df.groupby('date').count().reset_index()

    # Create a bar chart using Plotly
    grouped_data = df.groupby('Month')['tweets'].count().reset_index()
    grouped_data = grouped_data.rename(columns={'Month': 'Month', 'tweets': 'Number of Tweets'})

    # Replace month numbers with their corresponding names
    grouped_data['Month'] = grouped_data['Month'].apply(lambda x: calendar.month_name[int(x)])

    # Create a bar chart using Plotly
    fig = px.bar(grouped_data, x='Month', y='Number of Tweets', title='Number of Tweets per Month')

    # Display the bar chart using Streamlit
    st.title("Month Wise Tweets")
    st.plotly_chart(fig)

    fig = px.bar(grouped_data, x='Month', y='tweets')
    
    # # Update the x-axis tick labels with month names
    month_names = [calendar.month_name[i] for i in range(1, 13)]
    fig.update_layout(
         xaxis=dict(
             tickmode='array',
             tickvals=list(range(1, 13)),
             ticktext=month_names
         ),
         #title='Month-wise tweets',
         xaxis_title='Month',
         yaxis_title='Number of Tweets'
     )

    #Display the bar chart using Streamlit
    st.title("Month Wise Tweets")
    st.plotly_chart(fig)
    #---------------------
       
    df_sorted = df.sort_values('Favorite count(Like)', ascending=False)

    # Select the top 5 tweets based on the 'like' column
    top_5_tweets = df_sorted.head(5)

    # Display the top 5 tweets in a table format
    st.title('Top 5 Most liked Tweets')
    st.dataframe(top_5_tweets[['tweets', 'Favorite count(Like)','score']])

    df_sorted = df.sort_values('Retweet', ascending=False)

    # Select the top 5 tweets based on the 'retweet' column
    top_5_tweets = df_sorted.head(5)

    # Display the top 5 tweets in a table format
    st.title('Top 5 Most Retweeted Tweets')
    st.dataframe(top_5_tweets[['tweets', 'Retweet','score']])

         #-----
    import altair as alt
    import datetime

    st.title('Time Interval')
    # convert the time column to datetime format
    df['time1'] = pd.to_datetime(df['Account Created at'])

    # create a new column with the hour component as a time object
    df['hour_time'] = df['time1'].apply(lambda x: datetime.time(x.hour, 0))


    # define a function to categorize the hour values
    def categorize_hour(hour):
        if hour < 6:
            return '0-6 AM'
        elif hour < 12:
            return '6-12 AM'
        elif hour < 18:
            return '12-18 PM'
        else:
            return '18-24 PM'


    # apply the function to the hour_time column to create a new column with time interval categories
    df['time_interval'] = df['hour_time'].apply(lambda x: categorize_hour(x.hour))

    # drop the hour_time and time1 columns
    df = df.drop(['hour_time', 'time1'], axis=1)

    # create a bar chart using altair
    chart = alt.Chart(df).mark_bar().encode(
        x='time_interval',
        y='count()',
        color='time_interval'
    ).properties(
        width=500,
        height=500
    )

    # show the chart in streamlit
    st.altair_chart(chart, use_container_width=True)

    st.title('Gender wise Tweets')
    gender_counts = df.groupby('Gender').size()
    colors = ['blue', 'red', 'green']
    # Calculate the percentage of each gender
    gender_percentages = gender_counts / gender_counts.sum() * 100

    # Plot a bar graph of the gender percentages
    fig, ax = plt.subplots(figsize=(6, 3))
    gender_percentages.plot(kind='bar', ax=ax,color=colors)

    # Add axis labels and title
    ax.set_xlabel('Gender')
    ax.set_ylabel('Percentage')
    ax.set_title('Gender Distribution')

    # Display the plot in Streamlit
    st.pyplot(fig)

    from datetime import timedelta

    # Define the time window (4 hours in this case)
    time_window = timedelta(hours=6)

    # Filter the tweets to only include those from the fake user
    fake_tweets = df[df['Username'] == 'fakeuser']

    # Create a dictionary to store the count of tweets for each time
    tweet_counts = {}

    # Loop through the tweets and count the number of tweets within the time window
    for index, row in fake_tweets.iterrows():
        time = row['time']
        count = tweet_counts.get(time, 0)
        tweet_counts[time] = count + 1

    # Filter the tweet counts to only include those with 2 or more tweets within the time window
    fake_tweet_counts = {time: count for time, count in tweet_counts.items() if count >= 2}

    # Filter the original dataframe to only include the tweets with times that appear in the filtered tweet counts
    fake_tweets_2_or_more = fake_tweets[fake_tweets['time'].isin(fake_tweet_counts.keys())]

    # Filter the resulting dataframe to only include tweets with subjectivity less than -0.499
    fake_tweets_final = fake_tweets_2_or_more[fake_tweets_2_or_more['Subjectivity'] < -0.499]

    st.title('Find Fake Tweets')

    # Check if there are any fake tweets found
    if fake_tweets_final.empty:
        st.subheader("Good news! No fake tweets found.")
    else:
        # Display the resulting dataframe
        st.subheader('Fake tweets')
        st.write(fake_tweets_final)




#----------------------------