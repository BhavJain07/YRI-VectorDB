import requests
from bs4 import BeautifulSoup
import arxiv
import time
import random
import logging
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)

class ProfessorScraper:
    def __init__(self):
        self.arxiv_client = arxiv.Client()

    def search_professors(self, university_name, max_professors=100):
        professors = []
        try:
            logger.info(f"Searching for professors at {university_name}")
            url = f"https://www.google.com/search?q=site:{university_name.replace(' ', '+')}+professor"
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            response = requests.get(url, headers=headers)
            logger.info(f"Response status code: {response.status_code}")
            
            if response.status_code != 200:
                logger.error(f"Failed to fetch data. Status code: {response.status_code}")
                return professors

            soup = BeautifulSoup(response.text, 'html.parser')
            
            for result in soup.find_all('div', class_='g'):
                name = result.find('h3')
                if name:
                    name = name.text.strip()
                    snippet = result.find('div', class_='VwiC3b')
                    interests = self.extract_interests(snippet.text) if snippet else []
                    professors.append({
                        'name': name,
                        'email': '',
                        'interests': interests,
                        'affiliation': university_name
                    })
                    logger.info(f"Found professor: {name} with interests: {interests}")
                if len(professors) >= max_professors:
                    break
                time.sleep(random.uniform(1, 3))  # Add a random delay between requests
            logger.info(f"Found {len(professors)} professors from {university_name}")
            return professors
        except Exception as e:
            logger.error(f"Error scraping professors from {university_name}: {str(e)}", exc_info=True)
            return []

    def extract_interests(self, text):
        keywords = ['machine learning', 'artificial intelligence', 'data science', 'computer vision', 'natural language processing',
                    'robotics', 'deep learning', 'neural networks', 'big data', 'cybersecurity', 'blockchain',
                    'internet of things', 'cloud computing', 'quantum computing', 'bioinformatics']
        return list(set([kw for kw in keywords if kw in text.lower()]))

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def get_publications(self, professor_name):
        try:
            search = arxiv.Search(query=professor_name, max_results=1)
            logger.info(f"get_publications Found {search}")

            client = arxiv.Client()
            results = list(client.results(search))

            #results = self.arxiv_client.results(search)
            logger.info(f"get_publications results Found {results}")
            logger.info(f"Found {len(results)} publications for {professor_name}")
            
            # for x in results:
            #     print(x.title)
            # if results:
            #     logger.info("In thee IF Results")
            #     #return [result.title for result in results]
            # else:
            #     logger.error("No results found for the given query.")
            #     return []

            return [result.title for result in results]
        
        except Exception as e:
            logger.error(f"Error fetching publications for {professor_name}: {str(e)}")
            raise

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    scraper = ProfessorScraper()
    professors = scraper.search_professors("Stanford University", max_professors=5)
    print(f"Found {len(professors)} professors:")
    for prof in professors:
        print(f"Name: {prof['name']}")
        print(f"Interests: {', '.join(prof['interests'])}")
        print("---")
    
    if professors:
        publications = scraper.get_publications(professors[0]['name'])
        print(f"Publications for {professors[0]['name']}:")
        for pub in publications:
            print(f"- {pub}")