import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from datetime import datetime
import pytz

# URL of the blog page
url = "https://osmosis.zone/blog"

# Send an HTTP GET request to the blog page
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Create an RSS feed
fg = FeedGenerator()
fg.title("Blog RSS Feed")
fg.link(href=url, rel="alternate")
fg.description("Latest articles from the blog")

# Find all article sections in the HTML
article_sections = soup.find_all("div", class_="blog-post-grid")

# Iterate through each article section
for section in article_sections:
    articles = section.find_all("div", class_="w-dyn-item")
    for article in articles:
        title_elem = article.find("h3", class_="h3")
        if title_elem:
            title = title_elem.text
        else:
            title = "No Title"

        description_elem = article.find("div", {"fs-cmsfilter-field": "description"})
        if description_elem:
            description = description_elem.text
        else:
            description = "No Description"

        date_elem = article.find("div", class_="text-block-5")
        if date_elem:
            date_str = date_elem.text
            try:
                # Parse and format the date
                date = datetime.strptime(date_str, "%B %d, %Y")
                date = pytz.timezone("GMT").localize(date)  # Set the timezone
            except ValueError:
                date = datetime.now(pytz.timezone("GMT"))  # Default to current time in case of parsing error
        else:
            date = datetime.now(pytz.timezone("GMT"))  # Default to current time if date is missing

        article_link = article.find("a", class_="blog-post")
        if article_link:
            article_url = article_link.get("href")
        else:
            article_url = ""

        image_elem = article.find("img", class_="image-item")
        if image_elem:
            image_url = image_elem.get("src")
        else:
            image_url = ""

        # Create a new entry in the RSS feed
        fe = fg.add_entry()
        fe.title(title)
        fe.description(description)
        fe.link(href=article_url)
        fe.pubDate(date)
        fe.enclosure(image_url, 0, "image/jpeg")  # Add image URL as enclosure

# Generate the RSS feed
rss_feed = fg.rss_str(pretty=True)

# Save the RSS feed to a file
with open("blog_rss_feed.xml", "wb") as f:
    f.write(rss_feed)

print("RSS feed generated and saved.")
