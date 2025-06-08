const CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSSaeSBT1QzO279wLHndPKaBOqABHMTTDAjE6mkyom3vuoMRF8gYRhPiWQgWiaD07G36PNnekVukoaO/pub?output=csv";

// Fetch tweets from CSV
async function fetchTweets() {
  const res = await fetch(CSV_URL);
  const text = await res.text();
  return text.split('\n').slice(1).map(line => {
    const [tweet] = line.split(',');
    return tweet.trim();
  }).filter(t => t.length > 0);
}

// Choose a random tweet
function getRandomTweet(tweets) {
  return tweets[Math.floor(Math.random() * tweets.length)];
}

// Post the tweet via Twitter Intent
async function postTweet() {
  const tweets = await fetchTweets();
  const tweet = getRandomTweet(tweets);
  chrome.tabs.create({
    url: `https://twitter.com/intent/tweet?text=${encodeURIComponent(tweet)}`
  });
}

// Set up repeating alarm every 2 hours
chrome.runtime.onInstalled.addListener(() => {
  chrome.alarms.create("tweetAlarm", {
    delayInMinutes: 1,          // First run after 1 minute
    periodInMinutes: 120        // Then every 120 minutes (2 hours)
  });
});

// Listen to the alarm
chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === "tweetAlarm") {
    postTweet();
  }
});
