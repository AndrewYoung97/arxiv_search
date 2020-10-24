import spacy
import networkx as nx
from collections import Counter

nlp = spacy.load('en_core_web_sm')
# doc = nlp('Finally, we have applied data mining techniques for identifying patterns in the solutions.')
# spacy.displacy.serve(doc, style='dep')
# doc = nlp('Finally, we have applied x for y.')
# spacy.displacy.serve(doc, style='dep')
docs = []
with open('seed.csv', 'r') as f:
    for d in f.readlines():
        if d == '\n':
            continue
        if d[-2] == '.':
            docs.append(d[:-2])
        else:
            docs.append(d[:-1])
docs = docs[1::2]

patterns = []
pos_patterns = []
# Load spacy's dependency tree into a networkx graph
for doc in docs:
    doc = nlp(doc)
    edges = []
    pos_edges = []
    for token in doc:
        for child in token.children:
            edges.append(('{0}'.format(token.lower_),
                          '{0}'.format(child.lower_)))
            if str(token) != 'x' and str(token) != 'y':
                if str(child) != 'x' and str(child)!= 'y':
                    pos_edges.append(('{0}'.format(token.pos_),
                                  '{0}'.format(child.pos_)))
                else:
                    pos_edges.append(('{0}'.format(token.pos_),
                                      '{0}'.format(child)))
            else:
                if str(child) != 'x' and str(child)!= 'y':
                    pos_edges.append(('{0}'.format(token),
                                  '{0}'.format(child.pos_)))
                else:
                    pos_edges.append(('{0}'.format(token),
                                      '{0}'.format(child)))
    graph = nx.Graph(edges)
    graph_pos = nx.Graph(pos_edges)
    # Get the path
    entity1 = 'x'
    entity2 = 'y'
    try:
        pos_patterns.append(tuple(nx.shortest_path(graph_pos, source=entity1, target=entity2)))
        patterns.append(tuple(nx.shortest_path(graph, source=entity1, target=entity2)))
    except:
        print(doc)
print(Counter(patterns))
print(Counter(pos_patterns))
