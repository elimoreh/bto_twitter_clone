from django.shortcuts import render, redirect, get_object_or_404
from .models import Tweet, TweetMedia, Reply, ReplyMedia
from .forms import TweetForm, ReplyForm
from django.contrib import messages
from django.views import generic
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from collections import Counter
import re
import nltk
from nltk.corpus import stopwords
from django.http import JsonResponse
# Create your views here.

STOP_WORDS = set(stopwords.words('english'))


# cache this so it's only updated every three minutes.
def _get_trending_topics() -> list[tuple]:
    # scope our trending tweets to the last 3 hours only
    datetime_bound = datetime.now() - timedelta(hours=3)
    # [{ "content": 'tweet content' }, {}]
    tweet_contents = Tweet.objects.filter(updated__gte=datetime_bound).values_list("content")

    words = []
    for tweet_content in tweet_contents:
        tweet = tweet_content['content']
        # Extract words from post content and filter out stop words
        words.extend([
            word.lower() for word in re.findall(r'\w+', tweet.content)
            if word.lower() not in STOP_WORDS
        ])
        # Extract hashtags from post content
        hashtags = re.findall(r'#\w+', tweet.content)
        words.extend(hashtags)
        word_count = Counter(words)
    return word_count.most_common(10)




def trendingView(request):
    trending_words = _get_trending_topics()
       
    trending_tweets_count = []
    for word in trending_words:
        # filter tweets to include only last 3 hours
        # Get tweets that contain any of the words and group them by their content in-memory
        count = Tweet.objects.filter(content__icontains=word[0]).count()
        trending_tweets_count.append(count)

    # this is not an HTTP response object or a JSON object for AJAX call
    return zip(trending_words, trending_tweets_count)


def tweetUpload(request):
    new_tweet = None
    tweet_form = TweetForm()
    if request.method == 'POST':
        tweet_form = TweetForm(request.POST)
        images = request.FILES.getlist('file')
        if tweet_form.is_valid():
            # we can assign the user in the TweetForm
            new_tweet = tweet_form.save(commit=False)
            new_tweet.author = request.user
            new_tweet.save()

            # saving the tweet and its media should be transactional
            for i in images:
                tweet_image = TweetMedia(tweet=new_tweet, image=i)
                tweet_image.save()
            messages.success(request, "Tweet has been uploaded ")
            return redirect("index")
            # In the case of a failed save, show the user an error message
        else:
            pass # return if tweet is not valid


def tweetDetail(request, username, pk):
    user = User.objects.get(username=username)
    tweet = get_object_or_404(Tweet, author=user, id=pk)
    replies = tweet.replies.all()
    new_reply = None
    reply_form = ReplyForm()
    images = request.FILES.getlist('file')
    now = datetime.now()
    yesterday = (now - timedelta(days=1)).date()

    if request.method == 'POST':
        reply_form = ReplyForm(request.POST)

        if reply_form.is_valid():
            new_reply = reply_form.save(commit=False)
            new_reply.author = request.user
            new_reply.tweet = tweet
            new_reply.save()

            for i in images:
                reply_media = ReplyMedia(reply=new_reply, image=i)
                reply_media.save()

            messages.success(request, 'messages has been uploaded')
            return redirect('tweet_detail', username, pk)

    return render(
        request, 'tweet_detail.html', {
            'tweet': tweet,
            'replies': replies,
            'reply_form': reply_form,
            'now': now,
            'yesterday': yesterday
        })
