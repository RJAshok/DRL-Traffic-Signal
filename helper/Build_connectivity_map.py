import sumolib
def build_connectivity_map(net_file):
    """
    Parses the network file using sumolib and builds a dictionary mapping each edge to its outgoing edges.
    It also builds a list of starting edges.
    :param net_file: Path to the SUMO network file
    :return: (connectivity_map, starting_edges)
             connectivity_map: dictionary where the keys are edge IDs and values are lists of outgoing edge IDs.
             starting_edges: list of edge IDs that have at least one outgoing connection.
    """
    net = sumolib.net.readNet(net_file)
    connectivity_map = {}
    starting_edges = []
    
    for edge in net.getEdges():
        edge_id = edge.getID()
        # It skips internal edges which start with ':'
        if edge_id.startswith(':'):
            continue

        outgoing_edges = set()
        for lane in edge.getLanes():
            # Gets outgoing connection objects.
            connections = lane.getOutgoing()
            for connection in connections:
                target_lane = connection.getToLane()
                target_edge = target_lane.getEdge().getID()
                outgoing_edges.add(target_edge)
        connectivity_map[edge_id] = list(outgoing_edges)
        # Considers this edge as a candidate for starting edge
        if outgoing_edges:
            starting_edges.append(edge_id)
    
    return connectivity_map, starting_edges