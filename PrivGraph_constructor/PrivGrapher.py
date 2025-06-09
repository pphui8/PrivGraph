import argparse
import json
import networkx as nx
import matplotlib.pyplot as plt
import pickle

# Based on the intermediate output
# construct the PrivGraphs
# calculate SLF

PII_map = {
    "name": 0,
    "date_of_birth": 1,
    "gender": 1,
    "marital_status": 1,
    "nationality": 1,
    "age": 1,
    "home_address": 1,
    "email_address": 1,
    "phone_number": 1,
    "identify_number": 0,
    "social_security_number": 0,
    "passport_number": 0,
    "driver_license_ID": 0,
    "tax_identification_ID": 0,
    "student_ID": 0,
    "GPS_coordinates": 1,
    "work_place": 1,
    "travel_history": 1,
    "zip_code": 1,
    "IP_address": 1,
    "mac_address": 1,
    "cookies": 1,
    "usernames": 1,
    "blood_type": 0,
    "illness_symptoms": 1,
    "medical_diagnosis": 1,
    "religious_beliefs": 1,
    "political_opinions": 1,
    "education_background":1, 
    "employment_history": 1,
    "financial_information": 1,
    "cultural_affiliation": 1,  # wrong spell in the NLP model, remember to fix it.
}

# Data type sensitivity
# 0: non-sensitive
# 1: sensitive
PII_DTS = {
    "name": .9,
    "date_of_birth": .7,
    "gender": .3,
    "marital_status": .2,
    "nationality": .3,
    "age": .6,
    "home_address": .8,
    "email_address": .8,
    "phone_number": 1,
    "identify_number": 1,
    "social_security_number": 1,
    "passport_number": 1,
    "driver_license_ID": 1,
    "tax_identification_ID": 1,
    "student_ID": .9,
    "GPS_coordinates": .8,
    "work_place": .5,
    "travel_history": .2,
    "zip_code": .4,
    "IP_address": .4,
    "mac_address": .8,
    "cookies": .7,
    "usernames": .2,
    "blood_type": .2,
    "illness_symptoms": .8,
    "medical_diagnosis": .9,
    "religious_beliefs": .8,
    "political_opinions": .8,
    "education_background":.4, 
    "employment_history": .7,
    "financial_information": .8,
    "cultural_affiliation": .4,  # wrong spell in the NLP model, remember to fix it.
}

def merge_graphs(text, graph1, graph2):
    """
    Merge graph2 into graph1 and remove graph2 from text.
    Nodes and edges from graph2 are added to graph1 if not present.
    """
    for node, attrs in graph2.nodes(data=True):
        if not graph1.has_node(node):
            graph1.add_node(node, **attrs)
        else:
            # Optionally, update attributes (e.g., count)
            if 'count' in attrs and 'count' in graph1.nodes[node]:
                graph1.nodes[node]['count'] += attrs['count']

    for u, v, attrs in graph2.edges(data=True):
        if not graph1.has_edge(u, v):
            graph1.add_edge(u, v, **attrs)

    # Remove graph2 from text
    if graph2 in text:
        text.remove(graph2)

def enrich_graph_with_ontology(individual_graph, ontology_graph):
    # Create a new graph for the enriched result
    enriched_graph = individual_graph.copy()

    # Identify the individual entity node
    individual_entity = [node for node in individual_graph.nodes() if individual_graph.nodes[node].get('type') == 'individual'][0]

    # For each data node in the individual graph (except the individual entity)
    for node in individual_graph.nodes():
        if node != individual_entity and node in ontology_graph:
            ancestors = nx.ancestors(ontology_graph, node)
            
            enriched_graph.add_nodes_from(ancestors)
            
            for ancestor in ancestors:
                paths = nx.all_simple_paths(ontology_graph, source=ancestor, target=node)
                for path in paths:
                    for i in range(len(path) - 1):
                        enriched_graph.add_edge(path[i], path[i+1], relationship='parent_of')

    return enriched_graph

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract columns from SQL file')
    parser.add_argument('--intermediate_file', type=str, default='./intermediate_output.jsonl', help='Intermediate file to extracted columns')
    parser.add_argument('--output_file', type=str, default='./output/PrivGraphs.pkl', help='Output file to save the result')
    parser.add_argument('--datatype_file', type=str, default='./output/Datatype.pkl', help='Datatype file to extracted columns')
    args = parser.parse_args()

    with open(args.intermediate_file, 'r') as file:
        data = json.load(file)

    print('number of records:', len(data))

    # graphs_number = 0
    # for text in data:
    #     for graph in text:
    #         graphs_number += 1
    # print('number of graphs:', graphs_number)

    segmented_data_with_graphs = []
    for text in data:
        PrivGraphs = []
        for graph in text:
            G = nx.DiGraph()
            G.add_node("Individual", type="individual")
            for key in graph.keys():
                label = graph[key]['label'].lower()
                # wrong spell of "cultural_affiliation"
                if label == "cultural_affiliation":
                    label = "cultural_affillation"
                
                # if exists, increase the count
                if G.has_node(label):
                    G.nodes[label]['count'] += 1
                    break

                # if is a direct PII
                G.add_node(label, color="red", type="PII", count=0, content=graph[key]['text'])
                G.add_edge(label, "Individual", color="red", type="owns")
            PrivGraphs.append(G)
        segmented_data_with_graphs.append(PrivGraphs)

    # merge the graphs]
    # rule: merge PrivGraph that contains same unique PII records
    # find the graph from other text that contains the same unique PII records
    # if found, merge the two graphs
    for text in segmented_data_with_graphs:
        for graph in text:
            for node in graph.nodes():
                if graph.nodes[node].get('type') == 'PII':
                    for other_text in segmented_data_with_graphs:
                        if other_text != text:
                            for other_graph in other_text:
                                for other_node in other_graph.nodes():
                                    if other_graph.nodes[other_node].get('type') == 'PII':
                                        if graph.nodes[node].get('content') == other_graph.nodes[other_node].get('content'):
                                            # merge the two graphs
                                            merge_graphs(text, graph, other_graph)
                                            break


    # read the data type file
    with open(args.datatype_file, 'rb') as f:
        Ontology = pickle.load(f)

    # enrich the graph
    for i in range(len(segmented_data_with_graphs)):
        for j in range(len(segmented_data_with_graphs[i])):
            segmented_data_with_graphs[i][j] = enrich_graph_with_ontology(segmented_data_with_graphs[i][j], Ontology)

    # merge the graphs
    # for i in range(len(segmented_data_with_graphs)):
    #     segmented_data_with_graphs[i] = merge_graphs(segmented_data_with_graphs[i])
    
    # show the first graph
    # nx.draw(segmented_data_with_graphs[0][0], with_labels=True, font_weight='bold')
    # plt.show()


    # print("Saving to", args.output_file)
    # # output to Pickled
    # with open(args.output_file, 'wb') as f:
    #     pickle.dump(segmented_data_with_graphs, f)