import streamlit as st
from back.category_scraper import scrape_category
from back.subcategory_scraper import scrape_subcategory

# Fonction pour afficher les articles
def display_articles(articles):
    if not articles:
        st.warning("Aucun article trouvé.")
        return

    for article in articles:
        # Afficher la miniature et le titre
        st.image(article.get('thumbnail', ''), width=300, caption=article.get('title', 'Article'))
        st.write(f"[Lire l'article]({article.get('link', '#')})")

# Application Streamlit
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Choisissez une page", ["Accueil", "Recherche par catégorie", "Recherche par sous-catégorie"])

    if page == "Accueil":
        st.title("Bienvenue sur le Scraper de Blog")
        st.write("Utilisez la barre de navigation pour rechercher des articles par catégorie ou sous-catégorie.")

    elif page == "Recherche par catégorie":
        st.title("Recherche par catégorie")
        category = st.text_input("Entrez une catégorie (par exemple, 'web', 'marketing') :").strip().lower()

        if st.button("Rechercher"):
            if category:
                category_url = f"https://www.blogdumoderateur.com/{category}/"
                st.write(f"Scraping la catégorie : {category_url}")
                articles = scrape_category(category_url)
                display_articles(articles)
            else:
                st.error("Veuillez entrer une catégorie valide.")

    elif page == "Recherche par sous-catégorie":
        st.title("Recherche par sous-catégorie")
        subcategory = st.text_input("Entrez une sous-catégorie (par exemple, 'ia', 'seo') :").strip().lower()

        if st.button("Rechercher"):
            if subcategory:
                subcategory_url = f"https://www.blogdumoderateur.com/dossier/{subcategory}/"
                st.write(f"Scraping la sous-catégorie : {subcategory_url}")
                articles = scrape_subcategory(subcategory_url)
                display_articles(articles)
            else:
                st.error("Veuillez entrer une sous-catégorie valide.")

if __name__ == "__main__":
    main()