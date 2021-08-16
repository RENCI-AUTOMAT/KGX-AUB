import argparse
import json
import os
from pathlib import Path

def jsonl_file_iterator(file_path):
    with open(file_path, 'r', encoding='utf-8') as stream:
        for line in stream:
            yield json.loads(line)


def main(input, output_dir):
    # first read all nodes from fileset A
    nodes = jsonl_file_iterator(input['A']['node_file'])
    node_ids = set([node['id'] for node in nodes])

    # filter edges from B that contain A

    edges = jsonl_file_iterator(input['B']['edge_file'])
    filtered_edges = [edge for edge in edges
                        if edge['subject'] in node_ids or edge['object'] in node_ids]

    print(f'Found new {len(filtered_edges)} possible edges to add')

    # find node ids that filtered edges from B connect to not present in A

    filtered_edges_node_ids = set()
    for edge in filtered_edges:
        filtered_edges_node_ids.add(edge['subject'])
        filtered_edges_node_ids.add(edge['object'])
    filtered_edges_node_ids = filtered_edges_node_ids - node_ids

    print(f'Found new {len(filtered_edges_node_ids)} node ids that are connected with edges from B')

    # get node data from B

    filtered_nodes_from_B = [node for node in jsonl_file_iterator(input['B']['node_file'])
                             if node['id'] in filtered_edges_node_ids]

    if not Path(output_dir).exists():
        os.makedirs(output_dir)


    # write out nodes
    with open(os.path.join(output_dir, 'merge_nodes.jsonl'), 'w', encoding='utf-8') as stream:
        # write out nodes of A
        for node in jsonl_file_iterator(input['A']['node_file']):
            stream.write(json.dumps(node) + '\n')
        # write new nodes from B
        for node in filtered_nodes_from_B:
            stream.write(json.dumps(node) + '\n')

    # write out edges
    with open(os.path.join(output_dir, 'merge_edges.jsonl'), 'w', encoding='utf-8') as stream:
        # write out edges from A
        for edge in jsonl_file_iterator(input['A']['edge_file']):
            stream.write(json.dumps(edge) + '\n')
        # write out new edges from B
        for edge in filtered_edges:
            stream.write(json.dumps(edge) + '\n')

    print('Done')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="KGX files subset merge cli tool. ")
    parser.add_argument("-An", "--A-nodes", help="Nodes file of dataset A")
    parser.add_argument("-Ae", "--A-edges", help="Edges file of dataset A")
    parser.add_argument("-Bn", "--B-nodes", help="Nodes file of dataset B")
    parser.add_argument("-Be", "--B-edges", help="Edges file of dataset B")
    parser.add_argument("-o", "--output-dir", help="output dir of merged files")

    args = parser.parse_args()

    # some input existence validation
    error = False
    if not Path(args.A_nodes).exists():
        error = True
        print(f"{args.A_nodes} (-An) doesn't exist")

    if not Path(args.B_nodes).exists():
        error = True
        print(f"{args.B_nodes} (-Bn) doesn't exist")

    if not Path(args.A_edges).exists():
        error = True
        print(f"{args.A_edges} (-Ae) doesn't exist")

    if not Path(args.B_edges).exists():
        error = True
        print(f"{args.B_edges} (-Be) doesn't exist")

    if error:
        print("ERROR encountered, some args are not found exiting.")
        exit(1)

    input_files = {
        "A": {
            "node_file": args.A_nodes,
            "edge_file": args.A_edges
        },
        "B": {
            "node_file": args.B_nodes,
            "edge_file": args.B_edges
        }
    }
    main(input_files, args.output_dir)
    exit(0)

