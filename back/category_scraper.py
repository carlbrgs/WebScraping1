import requests
from bs4 import BeautifulSoup
from scraper import scrape_article  # Import de la fonction existante

def scrape_category(category_url):
    try:
        page = 1  # Commencer à la première page

        while page <= 5:  # Limiter à 5 pages pour éviter de scraper trop de données
            # Construire l'URL de la page
            paginated_url = f"{category_url}page/{page}/"
            print(f"Scraping page: {paginated_url}")

            response = requests.get(paginated_url)
            if response.status_code == 404:  # Arrêter si la page n'existe pas
                print("Fin de la pagination.")
                break

            soup = BeautifulSoup(response.text, 'html.parser')

            # Trouver tous les articles de la catégorie
            articles = soup.find_all('article', class_='category-web')
            if not articles:  # Arrêter si aucun article n'est trouvé
                print("Aucun article trouvé sur cette page.")
                break

            # Parcourir chaque article
            for article in articles:
                # Trouver la balise <a> pour obtenir l'URL de l'article
                link_tag = article.find('a', href=True)
                if link_tag:
                    article_url = link_tag['href']
                    print(f"Scraping article: {article_url}")
                    # Appeler la fonction scrape_article pour extraire les données de l'article
                    scrape_article(article_url)

            page += 1

    except Exception as e:
        print(f"Error scraping category: {e}")
    try:
        response = requests.get(category_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Trouver tous les articles de la catégorie
        articles = soup.find_all('article', class_='category-web')
        if not articles:
            print("No articles found in this category.")
            return

        # Parcourir chaque article
        for article in articles:
            # Trouver la balise <a> pour obtenir l'URL de l'article
            link_tag = article.find('a', href=True)
            if link_tag:
                article_url = link_tag['href']
                print(f"Scraping article: {article_url}")
                # Appeler la fonction scrape_article pour extraire les données de l'article
                scrape_article(article_url)

    except Exception as e:
        print(f"Error scraping category: {e}")

# Exemple d'utilisation
if __name__ == "__main__":
    try:
        # Saisie de l'utilisateur
        category = input("Entrez la catégorie (par exemple, 'web', 'marketing', etc.) : ").strip().lower()
        if not category:
            raise ValueError("La catégorie ne peut pas être vide.")

        # Construire l'URL de la catégorie
        category_url = f"https://www.blogdumoderateur.com/{category}/"
        print(f"Scraping category: {category_url}")

        # Appeler la fonction pour scraper la catégorie
        scrape_category(category_url)

    except ValueError as ve:
        print(f"Erreur : {ve}")
    except Exception as e:
        print(f"Une erreur inattendue s'est produite : {e}")