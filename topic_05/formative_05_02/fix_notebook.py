import json
import re

# Read the notebook
with open('sem3_topic5_sna_formative2.ipynb', 'r') as f:
    nb = json.load(f)

# Define replacements for each TODO
replacements = {
    1: '''    # Step 1: Create the initial circle network (each node connected to 4 nearest neighbors)
    # This creates a regular network structure where nodes are arranged in a circle
    G = nx.Graph()
    
    # Add all nodes to the graph
    for i in range(num_nodes):
        G.add_node(i)
    
    # Connect each node to its 4 nearest neighbors (2 on each side)
    # This creates a regular lattice structure in a circular arrangement
    for i in range(num_nodes):
        # Connect to immediate neighbor (i+1 mod num_nodes wraps around)
        G.add_edge(i, (i + 1) % num_nodes)
        # Connect to second neighbor (i+2 mod num_nodes)
        G.add_edge(i, (i + 2) % num_nodes)
    
    # Calculate total number of edges in the initial network
    total_edges = G.number_of_edges()
    
    # Step 2: Initialize lists to track our measurements
    fractions = []  # Will store the fraction of edges that have been randomized
    lengths = []    # Will store the average shortest path length at each step
    threshold_fraction = None  # Will store the fraction when target path length is reached
    
    # Step 3: Iteratively randomize edges and measure the effect
    for iteration in range(max_iterations):
        # Get all current edges as a list (we need to convert to list to sample from it)
        edges_list = list(G.edges())
        
        # If no edges remain, break (shouldn't happen, but safety check)
        if len(edges_list) == 0:
            break
        
        # Randomly select an edge to remove
        # This edge represents a local connection in our circle network
        edge_to_remove = random.choice(edges_list)
        node1, node2 = edge_to_remove
        
        # Remove the selected edge from the network
        # This breaks a local connection
        G.remove_edge(node1, node2)
        
        # Step 4: Add a new random edge to replace the removed one
        # This creates a "long-range" connection that can dramatically reduce path lengths
        # We need to ensure we don't create self-loops or duplicate edges
        all_nodes = list(G.nodes())
        
        # Find two random nodes that are not already connected
        # Keep trying until we find a valid pair
        attempts = 0
        while attempts < 100:  # Safety limit to avoid infinite loops
            new_node1 = random.choice(all_nodes)
            new_node2 = random.choice(all_nodes)
            
            # Check if this is a valid new edge:
            # - Nodes must be different (no self-loops)
            # - Edge must not already exist
            if new_node1 != new_node2 and not G.has_edge(new_node1, new_node2):
                G.add_edge(new_node1, new_node2)
                break
            attempts += 1
        
        # Step 5: Calculate the average shortest path length after this randomization
        # This measures how "small" the world has become (how many steps on average to reach any node)
        # Note: This can be computationally expensive for large networks
        if nx.is_connected(G):  # Only calculate if network is still connected
            avg_path_length = nx.average_shortest_path_length(G)
        else:
            # If network is disconnected, we can't calculate average path length
            # In this case, we'll use a large value or skip this iteration
            avg_path_length = float('inf')
        
        # Step 6: Calculate what fraction of edges have been randomized so far
        # We divide by total_edges to get a fraction between 0 and 1
        fraction_randomized = (iteration + 1) / total_edges
        
        # Store our measurements
        fractions.append(fraction_randomized)
        lengths.append(avg_path_length)
        
        # Step 7: Check if we've reached the target path length
        # This is the "small world" threshold - when path length drops significantly
        if threshold_fraction is None and avg_path_length <= target_path_length:
            threshold_fraction = fraction_randomized
    ''',
    2: '''    # Step 3: Calculate total number of edges we want to add
    # If each node should have num_edges_per_node edges on average,
    # then total edges = num_nodes * num_edges_per_node
    total_edges_to_add = num_nodes * num_edges_per_node
    
    # Step 4: Add random edges until we reach the target number
    # We use a while loop because some random pairs might already be connected
    edges_added = 0
    max_attempts = total_edges_to_add * 10  # Safety limit to avoid infinite loops
        
    while edges_added < total_edges_to_add and max_attempts > 0:
        # Randomly select two different nodes
        node1 = random.randint(0, num_nodes - 1)
        node2 = random.randint(0, num_nodes - 1)
        
        # Make sure nodes are different (no self-loops)
        if node1 == node2:
            max_attempts -= 1
            continue
        
        # Check if this edge already exists
        # If not, add it to the graph
        if not G.has_edge(node1, node2):
            G.add_edge(node1, node2)
            edges_added += 1
        
        max_attempts -= 1
    
    # Note: Due to randomness, we might not reach exactly total_edges_to_add
    # if the network becomes very dense, but this is fine for our purposes
    ''',
    3: '''    # Step 1: Calculate the degree of each node in the network
    # The degree of a node is simply the number of neighbors it has
    # NetworkX provides G.degree() which returns a view of (node, degree) pairs
    
    # Extract just the degree values (not the node IDs)
    # We iterate through all nodes and get their degree
    degrees = [degree for node, degree in G.degree()]
    
    # Alternative approach (more explicit):
    # degrees = []
    # for node in G.nodes():
    #     degree = G.degree(node)  # Number of edges connected to this node
    #     degrees.append(degree)
    ''',
    4: '''    # Step 1: Initialize the network with a small starting structure
    # We start with just 2 nodes connected by an edge
    # This gives us a base to build upon
    G = nx.Graph()
    G.add_node(0)
    G.add_node(1)
    G.add_edge(0, 1)
    
    # Step 2: Add nodes one by one using preferential attachment
    # This simulates how networks grow in real life (e.g., people joining a social network)
    for new_node_id in range(2, num_nodes):
        # Add the new node to the network
        G.add_node(new_node_id)
        
        # Step 3: Implement preferential attachment
        # The new node will connect to num_edges_per_node existing nodes
        # The probability of connecting to an existing node is proportional to its degree
        # This means popular nodes (with many connections) are more likely to get new connections
        
        # We need to sample existing nodes with probability proportional to their degree
        # One way to do this is to create a list where each node appears as many times
        # as its degree, then randomly sample from that list
        
        # Get all existing nodes (all nodes except the one we just added)
        existing_nodes = list(range(new_node_id))
        
        # Create a list for weighted random sampling
        # Each existing node appears in the list a number of times equal to its degree
        # This makes nodes with higher degree more likely to be selected
        weighted_node_list = []
        for node in existing_nodes:
            degree = G.degree(node)
            # Add this node to the list 'degree' times
            # If a node has degree 0, it won't be added (isolated nodes can't be selected)
            weighted_node_list.extend([node] * degree)
        
        # If no nodes have edges yet (shouldn't happen after initial setup), 
        # just connect to random nodes
        if len(weighted_node_list) == 0:
            # Fallback: connect to random existing nodes
            targets = random.sample(existing_nodes, min(num_edges_per_node, len(existing_nodes)))
        else:
            # Step 4: Sample nodes from the weighted list
            # We sample without replacement to avoid duplicate edges
            # If we need more connections than available nodes, we take all available
            num_connections = min(num_edges_per_node, len(weighted_node_list))
            selected_targets = random.sample(weighted_node_list, num_connections)
            
            # Remove duplicates (in case same node was selected multiple times)
            targets = list(set(selected_targets))
            
            # If we still need more connections (after removing duplicates),
            # add more random nodes from existing nodes
            while len(targets) < num_edges_per_node and len(targets) < len(existing_nodes):
                additional_target = random.choice(existing_nodes)
                if additional_target not in targets:
                    targets.append(additional_target)
        
        # Step 5: Add edges from the new node to the selected target nodes
        for target in targets:
            G.add_edge(new_node_id, target)
    ''',
    5: '''    # Step 1: Initialize dictionary to store results for each network type
    # Each entry will contain the time series of S, I, R values
    results = {}
    
    # Step 2: Define the four network types we want to compare
    # Each network has 1000 nodes for fair comparison
    networks = {
        "Scale-Free Network": nx.barabasi_albert_graph(1000, 2),
        # Barabási-Albert: Preferential attachment, creates hub nodes
        # Parameter 2 means each new node connects to 2 existing nodes
        
        "Small-World Network": nx.watts_strogatz_graph(1000, 4, 0.1),
        # Watts-Strogatz: Starts as regular lattice, then randomizes some edges
        # Parameter 4: each node connected to 4 nearest neighbors initially
        # Parameter 0.1: 10% of edges are randomized
        
        "Random Network": nx.erdos_renyi_graph(1000, 0.05),
        # Erdős-Rényi: Completely random connections
        # Parameter 0.05: probability of edge between any two nodes is 5%
        
        "Network with Communities": nx.connected_caveman_graph(10, 100)
        # Connected Caveman: Creates 10 communities of 100 nodes each
        # Nodes are highly connected within communities, sparsely between
    }
    
    # Step 3: Run SIR simulation on each network type
    # We'll use the SIR_simulation function that was already defined earlier
    for network_name, network_graph in networks.items():
        # Create a copy of the network for this simulation
        # This is important because SIR_simulation modifies the graph (adds node attributes)
        G_copy = network_graph.copy()
        
        # Step 4: Randomly select initial infected nodes
        # We want to start with the same number of infected nodes for fair comparison
        all_nodes = list(G_copy.nodes())
        initial_infected = random.sample(all_nodes, min(initial_infected_count, len(all_nodes)))
        
        # Step 5: Run the SIR simulation
        # This will return three lists: S (susceptible count over time),
        # I (infected count over time), and R (recovered count over time)
        S, I, R = SIR_simulation(G_copy, initial_infected, infection_prob, recovery_prob)
        
        # Step 6: Store the results
        # We store as a tuple so we can easily unpack it later for analysis
        results[network_name] = (S, I, R)
    
    # Step 7: Return all results for comparison
    # The caller can then plot or analyze these time series to see differences
    ''',
    6: '''    # Step 1: Load the power grid network
    # This network represents the structure of the electricity grid
    G = initialize_grid()
    
    # Step 2: Precompute neighbor lists for efficiency
    # This avoids repeatedly calling G.neighbors() during the cascade
    # We create a dictionary mapping each node to its list of neighbors
    neighbors_dict = {node: list(G.neighbors(node)) for node in G.nodes}
    
    # Step 3: Initialize list to store cascade outcomes
    # Each outcome is the total number of nodes that failed in that simulation
    outcomes = []
    
    # Step 4: Run multiple simulations with different random starting points
    # This gives us a distribution of possible cascade sizes
    for simulation in range(num_simulations):
        # Step 5: Reset the grid to its initial state for each simulation
        # This ensures each simulation starts with the same grid configuration
        # (all nodes have their original load and capacity, none have failed)
        reset_grid(G)
        
        # Step 6: Randomly select a node to fail initially
        # This simulates a random failure event (e.g., equipment malfunction, attack)
        all_nodes = list(G.nodes)
        initial_failure_node = random.choice(all_nodes)
        
        # Step 7: Trigger the initial failure
        # This redistributes the failed node's load to its neighbors
        fail_node(G, neighbors_dict, initial_failure_node)
        
        # Step 8: Run the cascade simulation
        # This function continues the cascade until no more nodes fail
        # It returns the number of additional nodes that failed (excluding the initial one)
        additional_failures = cascade_failure(G, neighbors_dict)
        
        # Step 9: Calculate total failures (initial + cascading)
        # The initial failure counts as 1, plus all the cascading failures
        total_failures = 1 + additional_failures
        
        # Step 10: Store the outcome
        outcomes.append(total_failures)
    
    # Step 11: Return all outcomes
    # This list can be used to create a histogram showing the distribution
    # of cascade sizes, calculate statistics (mean, median, max), etc.
    ''',
    7: '''    # Step 1: Load the power grid network
    # This is the network structure we'll be testing
    G = initialize_grid()
    
    # Step 2: Precompute neighbor lists for efficiency
    # This speeds up the cascade simulation by avoiding repeated neighbor lookups
    neighbors_dict = {node: list(G.neighbors(node)) for node in G.nodes}
    
    # Step 3: Initialize dictionary to store cascade outcomes
    # Key: node ID, Value: total number of nodes that fail when this node fails
    outcomes = {}
    
    # Step 4: Test each node in the network
    # We systematically fail each node and measure the resulting cascade
    for node_to_test in G.nodes():
        # Step 5: Reset the grid to initial state for this test
        # Each test must start with the same grid configuration
        reset_grid(G)
        
        # Step 6: Fail the node we're testing
        # This triggers the initial failure and redistributes its load
        fail_node(G, neighbors_dict, node_to_test)
        
        # Step 7: Run the cascade simulation
        # This continues the cascade until no more nodes fail
        # It returns the number of additional nodes that failed (cascading failures)
        additional_failures = cascade_failure(G, neighbors_dict)
        
        # Step 8: Calculate total failures for this node
        # Total = 1 (the initial failure) + all cascading failures
        total_failures = 1 + additional_failures
        
        # Step 9: Store the result for this node
        outcomes[node_to_test] = total_failures
    '''
}

# Process each cell
for cell in nb['cells']:
    if cell['cell_type'] == 'code' and 'source' in cell:
        source_text = ''.join(cell['source'])
        
        # Check for each TODO
        for todo_num, replacement in replacements.items():
            pattern = f'# TODO {todo_num}:'
            if pattern in source_text:
                # Find the TODO section
                lines = cell['source']
                new_lines = []
                in_todo_section = False
                skip_until_solution = False
                
                for i, line in enumerate(lines):
                    if f'# TODO {todo_num}:' in line:
                        in_todo_section = True
                        skip_until_solution = True
                        # Add replacement code
                        replacement_lines = replacement.split('\n')
                        for rl in replacement_lines:
                            if rl.strip():  # Skip empty lines
                                new_lines.append('    ' + rl + '\n')
                            else:
                                new_lines.append(rl + '\n')
                        continue
                    elif skip_until_solution and '#. Your solution here' in line:
                        skip_until_solution = False
                        in_todo_section = False
                        continue
                    elif skip_until_solution:
                        continue
                    else:
                        new_lines.append(line)
                
                cell['source'] = new_lines
                break

# Write back
with open('sem3_topic5_sna_formative2.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)

print('All TODOs replaced successfully!')

