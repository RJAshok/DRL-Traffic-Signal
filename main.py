import traci
import random
from helper.Add_vehicle import add_vehicle_on_random_edge
from helper.Build_connectivity_map import build_connectivity_map

def main():
    # Build the connectivity map and list of starting edges.
    net_file = "Sumo_env/t.net.xml"  # Update with your network file.
    connectivity_map, starting_edges = build_connectivity_map(net_file)
    print("Connectivity map built:", connectivity_map)
    print("Candidate starting edges:", starting_edges)
    
    # Start the SUMO simulation.
    sumo_cmd = ["sumo-gui", "-c", "Sumo_env/t.sumocfg"] 
    traci.start(sumo_cmd)
    
    # Add a vehicle on a random starting edge.
    current_edge = add_vehicle_on_random_edge("veh0", starting_edges, depart_time=0)
    
    # Run the simulation until no vehicles remain.
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        
        for veh_id in traci.vehicle.getIDList():
            # Get the current edge of the vehicle.
            current_edge = traci.vehicle.getRoadID(veh_id)
            # Retrieve the list of connecting (outgoing) edges.
            possible_turns = connectivity_map.get(current_edge, [])
            if possible_turns:
                # Randomly choose the next edge.
                next_edge = random.choice(possible_turns)
                # Update the vehicle's route dynamically.
                traci.vehicle.changeTarget(veh_id, next_edge)
                print(f"Vehicle {veh_id} on {current_edge} changing target to {next_edge}")
    
    traci.close()

if __name__ == "__main__":
    main()
