from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import time

# Fonction principale
def main():
    # Entrées utilisateur
    print("Bienvenue sur le scraper Doctolib !")
    postal_code = input("Entrez le code postal ou la ville (ex: 75005) : ").strip()
    medical_query = input("Entrez la spécialité ou le type de praticien (ex: dermatologue, généraliste) : ").strip()
    max_results = int(input("Entrez le nombre maximum de résultats à afficher : ").strip())

    # Configurer Selenium
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    wait = WebDriverWait(driver, 20)
    try:
        driver.get("https://www.doctolib.fr/")

        refuseBtn = wait.until(
            EC.element_to_be_clickable((By.ID,
                "didomi-notice-disagree-button")))
        
        refuseBtn.click()

        wait.until(EC.invisibility_of_element_located((By.ID,
                "didomi-notice-disagree-button")))
    except Exception as e:
        print(f"Erreur lors du chargement de la page ou du traitement du bouton : {e}")

    wait = WebDriverWait(driver, 20)

    # Remplir le champ de recherche pour la spécialité
    query_input = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input.searchbar-input.searchbar-query-input"))
    )
    query_input.clear()
    query_input.send_keys(medical_query)

    # Remplir le champ de recherche pour le lieu
    place_input = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input.searchbar-input.searchbar-place-input"))
    )
    place_input.clear()
    place_input.send_keys(postal_code)

    # Attendre que le code postal soit bien saisi
    wait.until(
        EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "input.searchbar-input.searchbar-place-input"), postal_code)
    )

    # Lancer la recherche
    driver.find_element(By.CSS_SELECTOR, "button.searchbar-submit-button").click()

    # Attendre les résultats
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "body.patient_health_search-search, body.search_results-online_booking_search")))
    except TimeoutException:
        print("La page des résultats n'a pas été trouvée. Vérifiez l'URL ou les sélecteurs.")
        driver.quit()
        return

    # Récupérer les résultats
    # Attendre que la page soit complètement chargée
    wait.until(EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, "div.dl-card-border, article.dl-card.dl-card-bg-white.dl-card-variant-default")
    ))

    # Récupérer les résultats
    results = wait.until(EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, "[data-design-system-component='Card']")
    ))
    print(f"Nombre total de résultats trouvés : {len(results)}")

    for i in range(min(max_results, len(results))):
        try:
            # Recharger les résultats après chaque interaction
            results = wait.until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "div.dl-card-border, article.dl-card.dl-card-bg-white.dl-card-variant-default")
            ))

            # Sélectionner le résultat actuel
            result = results[i]

            # Récupérer les informations nécessaires
            text_elements = result.find_elements(By.CSS_SELECTOR, "[data-design-system-component='Text'], [data-design-system-component='Paragraph']")
            print(f"Éléments trouvés pour le résultat {i + 1}: {[el.text for el in text_elements]}")

            name = text_elements[0].text.strip()  # Le premier élément est le nom
            address_parts = []
            secteur = "Secteur non disponible"

            for el in text_elements[1:]:  # Parcourir les éléments restants
                text = el.text.strip()
                if "RDV" in text:  # Ignorer les résultats contenant "RDV"
                    print(f"{i + 1}. Résultat ignoré (contient 'RDV').")
                    break
                if "Conventionné" in text.lower():  # Si le texte contient "conventionné", c'est le secteur
                    secteur = text
                elif any(char.isdigit() for char in text):  # Si le texte contient des chiffres, c'est une partie de l'adresse
                    address_parts.append(text)

            else:  # Si on n'a pas rencontré "RDV", afficher les informations
                address = ", ".join(address_parts) if address_parts else "Adresse non disponible"
                print(f"{i + 1}. {name} - {address} - Secteur: {secteur}")

        except Exception as e:
            print(f"Erreur lors de l'extraction des informations pour le résultat {i + 1}: {e}")
    # Fermer le navigateur
    time.sleep(60)  # Attendre quelques secondes avant de fermer le navigateur
    driver.quit()

# Exécuter le script
if __name__ == "__main__":
    main()