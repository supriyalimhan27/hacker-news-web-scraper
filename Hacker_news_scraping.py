from bs4 import BeautifulSoup
import requests
import pandas as pd


def scrape_hacker_news():
    """
    Scrapes Hacker News homepage and returns a DataFrame
    containing article details.
    """
    url = "https://news.ycombinator.com/"

    # Fetch page
    page = requests.get(url)

    # Parse HTML
    soup = BeautifulSoup(page.content, "html.parser")

    # Extract all news rows and sublines
    all_news = soup.find_all("tr", class_="athing")
    all_subline = soup.find_all("td", class_="subtext")

    news_data = []

    # Loop through articles
    for news, subline in zip(all_news, all_subline):

        # Title (remove domain in brackets)
        title = news.find(class_="titleline").text.split(" (")[0]

        # Article link
        article_link = news.find(class_="titleline").a["href"]
        if article_link.startswith("item?id="):
            article_link = url + article_link

        # Author
        author_tag = subline.find(class_="hnuser")
        author = author_tag.text if author_tag else "NA"

        # Date/time
        date_of_post_tag = subline.find(class_="age")
        date_of_post = date_of_post_tag.text if date_of_post_tag else "NA"

        # Comments
        comments_count = subline.find_all("a")[-1].text.replace("\xa0", " ")

        # Append to list
        news_data.append({
            "Title": title,
            "Author": author,
            "Date_of_Post": date_of_post,
            "Comments_Count": comments_count,
            "Article_URL": article_link
        })

    # Convert to DataFrame
    df = pd.DataFrame(news_data)

    return df


    # Run scraper
    df = scrape_hacker_news()
    print(df.head())

    # Save to CSV
    df.to_csv("hacker_news.csv", index=False)
