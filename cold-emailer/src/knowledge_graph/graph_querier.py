import networkx as nx
from typing import List, Dict

class KnowledgeGraphQuerier:
    def __init__(self, graph_path: str):
        self.graph = nx.read_gexf(graph_path)

    def find_related_professors(self, interest: str, limit: int = 5) -> List[Dict]:
        professors = []
        for node in self.graph.neighbors(interest):
            if self.graph.nodes[node]['type'] == 'professor':
                professors.append(self.graph.nodes[node])
                if len(professors) >= limit:
                    break
        return professors

    def get_professor_interests(self, professor_name: str) -> List[str]:
        interests = []
        for node in self.graph.neighbors(professor_name):
            if self.graph.nodes[node]['type'] == 'interest':
                interests.append(node)
        return interests

    def get_professor_publications(self, professor_name: str) -> List[Dict]:
        publications = []
        for node in self.graph.neighbors(professor_name):
            if self.graph.nodes[node]['type'] == 'publication':
                publications.append(self.graph.nodes[node])
        return publications

if __name__ == "__main__":
    querier = KnowledgeGraphQuerier("../../data/knowledge_graph.gexf")
    related_professors = querier.find_related_professors("Machine Learning")
    print(f"Professors related to Machine Learning: {related_professors}")
