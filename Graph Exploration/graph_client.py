"""Student client; requires NetworkX."""

import json
from urllib.request import Request, urlopen

import networkx as nx


def get_graph(server_url, netid, timeout=60):
    """Fetch a student's undirected graph, with node labels in G.nodes[v]['label']."""
    request = Request(
        server_url.rstrip('/') + '/graph',
        data=json.dumps({'netid': netid}).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST',
    )
    with urlopen(request, timeout=timeout) as response:
        payload = json.load(response)
    graph = nx.Graph()
    graph.add_nodes_from(
        (node['id'], {k: v for k, v in node.items() if k != 'id'})
        for node in payload['nodes']
    )
    graph.add_edges_from(payload['edges'])
    return graph
