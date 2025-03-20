import time
import traci
import random
from helper.Add_vehicle import add_vehicle_on_random_edge
from helper.Build_connectivity_map import build_connectivity_map

v_num = 10  
max_depart_time = 300  
change_probability = 0.00001

def main():
    net_file = "C:/Users/lophi/Dev/TestSumo/try.net.xml" 
    connectivity_map, starting_edges = build_connectivity_map(net_file)
    print("Connectivity map built:", connectivity_map)
    print("Candidate starting edges:", starting_edges)
    
    sumo_cmd = ["sumo-gui", "-c", "C:/Users/lophi/Dev/TestSumo/try.sumocfg"]  
    traci.start(sumo_cmd)
    
    spawn_schedule = {f"veh{i}": random.uniform(0, max_depart_time) for i in range(v_num)}
    print("Spawn schedule:", spawn_schedule)
    
    spawned_vehicles = set()
    vehicle_decisions = {}
    
    while traci.simulation.getMinExpectedNumber() > 0 or len(spawned_vehicles) < v_num:
        current_sim_time = traci.simulation.getTime()
        
        # Spawn vehicles whose departure time has arrived.
        for veh_id, dep_time in spawn_schedule.items():
            if veh_id not in spawned_vehicles and current_sim_time >= dep_time:
                add_vehicle_on_random_edge(veh_id, starting_edges, dep_time)
                spawned_vehicles.add(veh_id)
        
        traci.simulationStep()
        
        # For each vehicle, update its route decision only once per edge,
        # except with a very small probability to change it.
        for veh_id in traci.vehicle.getIDList():
            current_edge = traci.vehicle.getRoadID(veh_id)
            possible_turns = connectivity_map.get(current_edge, [])
            if possible_turns:
                # If this vehicle hasn't made a decision on this edge yet, choose one.
                if veh_id not in vehicle_decisions or vehicle_decisions[veh_id][0] != current_edge:
                    chosen_target = random.choice(possible_turns)
                    vehicle_decisions[veh_id] = (current_edge, chosen_target)
                    traci.vehicle.changeTarget(veh_id, chosen_target)
                    print(f"Vehicle {veh_id} on {current_edge} choosing target {chosen_target}")
                else:
                    # With a very low probability, change the decision.
                    if random.random() < change_probability:
                        chosen_target = random.choice(possible_turns)
                        vehicle_decisions[veh_id] = (current_edge, chosen_target)
                        traci.vehicle.changeTarget(veh_id, chosen_target)
                        print(f"Vehicle {veh_id} on {current_edge} changing target (rare chance) to {chosen_target}")
            else:
                # If no possible turn exists, remove any stored decision.
                if veh_id in vehicle_decisions:
                    del vehicle_decisions[veh_id]
    
    traci.close()

if __name__ == "__main__":
    main()