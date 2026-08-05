"""
Example hierarchical RAG pipeline using LlamaIndex concepts.
This is an illustrative script showing how to assemble a hierarchical retriever and perform a query.
"""
from typing import List

# Placeholder classes to illustrate pipeline construction. Replace with llama_index imports in real code.
class Node:
    def __init__(self, text: str, metadata: dict = None):
        self.text = text
        self.metadata = metadata or {}

class SimpleIndex:
    def __init__(self, nodes: List[Node]):
        self.nodes = nodes

    def hierarchical_retrieve(self, query: str, top_k: int = 5):
        # Very naive retrieval: return first top_k nodes containing any query token
        tokens = set(query.lower().split())
        scored = []
        for n in self.nodes:
            score = len(tokens.intersection(set(n.text.lower().split())))
            if score > 0:
                scored.append((score, n))
        scored.sort(reverse=True, key=lambda x: x[0])
        return [n for _, n in scored[:top_k]]

# Construct nodes using sentence-window chunking
def sentence_window_chunks(text: str, window: int = 3):
    sentences = [s.strip() for s in text.split('.') if s.strip()]
    chunks = []
    for i in range(len(sentences)):
        start = max(0, i - (window-1))
        chunk = '. '.join(sentences[start:i+1])
        chunks.append(Node(chunk))
    return chunks

if __name__ == '__main__':
    doc = """Machine learning models require careful tuning. Hierarchical retrieval helps find relevant passages quickly. Sentence window chunking preserves context across breaks."""
    nodes = sentence_window_chunks(doc, window=3)
    idx = SimpleIndex(nodes)
    results = idx.hierarchical_retrieve('hierarchical retrieval context', top_k=3)
    for r in results:
        print('---')
        print(r.text)
