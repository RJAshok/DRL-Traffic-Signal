import random
import traci
def add_vehicle_on_random_edge(veh_id, starting_edges, depart_time):
    """
    Add a vehicle on a randomly selected starting edge and on a randomly chosen lane.
    A simple route is created for the vehicle.
    
    :param veh_id: Unique vehicle identifier.
    :param starting_edges: List of candidate starting edge IDs.
    :param depart_time: Simulation time at which the vehicle should be added.
    :return: The edge ID on which the vehicle was added.
    """
    edge_id = random.choice(starting_edges)
    routeID = f"route_{veh_id}"
    traci.route.add(routeID, [edge_id])
    
    num_lanes = traci.edge.getLaneNumber(edge_id)
    if num_lanes == 0:
        raise ValueError(f"No lanes found for edge {edge_id}")
    
    depart_lane = str(random.choice(range(num_lanes)))
    traci.vehicle.add(
        vehID=veh_id,
        routeID=routeID,
        typeID="DEFAULT_VEHTYPE",  # Ensure this type exists in your SUMO configuration.
        depart=str(depart_time),
        departLane=depart_lane
    )
    print(f"Vehicle {veh_id} added on edge {edge_id} using lane {edge_id}_{depart_lane} at time {depart_time}")
    return edge_id