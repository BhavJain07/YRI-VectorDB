from scholarly import ProxyGenerator, scholarly
import arxiv

class ProfessorScraper:
    def __init__(self):
        pg = ProxyGenerator()
        pg.FreeProxies()
        scholarly.use_proxy(pg)
        self.arxiv_client = arxiv.Client()

    def search_professor(self, name):
        search_query = scholarly.search_author(name)
        return next(search_query)

    def get_publications(self, author_name, max_results=20):
        search = arxiv.Search(
            query=f"au:{author_name.replace(' ', '_')}",
            max_results=max_results,
            sort_by=arxiv.SortCriterion.LastUpdatedDate
        )
        results = self.arxiv_client.results(search)
        return [f"Title: {r.title} \n Abstract: {r.summary}" for r in results]

    def search_professors(self, university_name, max_professors=100):
        search_query = scholarly.search_author_by_organization(university_name)
        professors = []
        for i, professor in enumerate(search_query):
            if i >= max_professors:
                break
            professors.append({
                'name': professor['name'],
                'email': professor.get('email', ''),
                'interests': professor.get('interests', []),
                'affiliation': professor.get('affiliation', '')
            })
        return professors