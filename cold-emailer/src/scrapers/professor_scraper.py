import requests
from bs4 import BeautifulSoup
import arxiv
import time
import random
import logging

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
            logger.info(f"Response content: {response.text[:500]}...")  # Log first 500 characters of the response
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            for result in soup.find_all('div', class_='g'):
                logger.info(f"Found result: {result}")
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
        # Simple keyword extraction (you might want to improve this)
        keywords = ['machine learning', 'artificial intelligence', 'data science', 'computer vision', 'natural language processing']
        return [kw for kw in keywords if kw in text.lower()]

    def get_publications(self, professor_name):
        try:
            search = arxiv.Search(query=professor_name, max_results=5)
            return [result.title for result in self.arxiv_client.results(search)]
        except Exception as e:
            print(f"Error fetching publications: {str(e)}")
            return []