import requests
from bs4 import BeautifulSoup
from db import save_to_mongo


def scrape_article(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        title_tag = soup.find('h1', class_='entry-title')
        title = title_tag.text.strip() if title_tag else "Title not found"

        hat_img = soup.find('figure', class_='article-hat-img')
        thumbnail = "Thumbnail not found"
        if hat_img:
            img_tag = hat_img.find('img')
            thumbnail = img_tag['src'] if img_tag and 'src' in img_tag.attrs else "Thumbnail not found"

        post_content = soup.find('div', class_='article-terms')
        subcategory_list = post_content.find_all('li') if post_content else [] 
        subcategory = []
        for subcategory_tag in subcategory_list:
            subcategory_text = subcategory_tag.find('a')
            if subcategory_text:
                subcategory.append(subcategory_text.text.strip())
            
        
        summary_tag = soup.find('div', class_='article-hat')
        summary_p = summary_tag.find('p') if summary_tag else None 
        summary = summary_p.text.strip() if summary_tag else "Summary not found"

        meta_info = soup.find('div', class_='article-social-content')
        author_tag = meta_info.find('span', class_='byline') if meta_info else None
        author = author_tag.text.strip() if author_tag else "Author not found"

        date_tag = meta_info.find('time', class_='entry-date') if meta_info else None
        date_published = date_tag['datetime'][:10] if date_tag and 'datetime' in date_tag.attrs else "Date not found"


        images = {}
        for img_tag in soup.find_all('img'):
            img_url = img_tag.get('src')
            img_alt = img_tag.get('alt', 'No description')
            if img_url:
                images[img_url] = img_alt


        article_data = {
            'title': title,
            'thumbnail': thumbnail,
            'subcategory': subcategory,
            'summary': summary,
            'date_published': date_published,
            'author': author,
            'images': images
        }


        save_to_mongo(article_data)
        print("Article saved successfully:", article_data)

    except Exception as e:
        print(f"Error scraping the article: {e}")
        
# Exemple d'URL d'article
article_url = "https://www.blogdumoderateur.com/edits-astuces-maitriser-application-montage-instagram/"
scrape_article(article_url)