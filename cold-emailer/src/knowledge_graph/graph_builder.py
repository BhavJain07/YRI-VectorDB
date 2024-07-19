import networkx as nx
import json
from typing import Dict, List

class KnowledgeGraphBuilder:
    def __init__(self):
        self.graph = nx.Graph()

    def add_professor(self, professor: Dict):
        self.graph.add_node(professor['name'], type='professor', **professor)
        for interest in professor['interests']:
            self.graph.add_node(interest, type='interest')
            self.graph.add_edge(professor['name'], interest)

    def add_publication(self, professor_name: str, publication: Dict):
        self.graph.add_node(publication['title'], type='publication', **publication)
        self.graph.add_edge(professor_name, publication['title'])
        for keyword in publication['keywords']:
            self.graph.add_node(keyword, type='keyword')
            self.graph.add_edge(publication['title'], keyword)

    def build_from_data(self, data_path: str):
        with open(data_path, 'r') as f:
            professors = json.load(f)
        for professor in professors:
            self.add_professor(professor)
            for publication in professor.get('publications', []):
                self.add_publication(professor['name'], publication)

    def save_graph(self, output_path: str):
        nx.write_gexf(self.graph, output_path)

if __name__ == "__main__":
    builder = KnowledgeGraphBuilder()
    # Add dummy data
    builder.add_professor({
        'name': 'Dr. John Doe',
        'interests': ['Machine Learning', 'Artificial Intelligence']
    })
    builder.add_professor({
        'name': 'Dr. Jane Smith',
        'interests': ['Natural Language Processing', 'Computer Vision']
    })
    builder.save_graph("../../data/knowledge_graph.gexf")