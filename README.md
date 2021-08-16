# KGX-AUB
Given two kgx sets, 
A and B, this program generates a new kgx file that contains:
* All nodes from A
* All edges from A
* All edges from B that have either subject node or object node that exists in A.
* All nodes in B that have connections to nodes in A.

##### Inputs:
  
  - Json-lines kgx files of dataset A 
  - Json-lines kgx files of dataset B
  
#### Outputs:
 
  - Json-lines formatted merged kgx edges and nodes file.
  



#### Usage:

```shell
python main.py -An <path_to_data_set_A_nodes.jsonl> \
               -Ae <path_to_data_set_A_edges.jsonl> \
               -Bn <path_to_data_set_B_nodes.jsonl> \
               -Be <path_to_data_set_B_edges.jsonl> \
               -o <path_to_output_dir>
               

```