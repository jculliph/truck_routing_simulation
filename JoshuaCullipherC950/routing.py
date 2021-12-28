import floyd_warshall
import csv
from hash_table import HashMap
import datetime


# The following converts the distance_list into a usable format for the algorithm O(N^2)
def distance_list_to_edge_vertex_list(distances):
    # Gets a list of weighted edges from the distances -> O(N^2)
    edges_list = list()
    for distance in distances:
        item_edges = list()
        for i in range(2, len(distance)):
            item_edges.append(distance[i])
        edges_list.append(item_edges)

    # Removes initial None value from list -> O(N)
    edges_list = list(filter(None, edges_list))

    # Makes all edges values the same length -> O(N)
    max_len = max(map(len, edges_list))
    for edge in edges_list:
        edge.extend(edges_list[j][edges_list.index(edge)] for j in range(edges_list.index(edge) + 1, max_len))

    # Converts all edges into float -> O(N^2)
    for edge in edges_list:
        for k in range(0, len(edge)):
            edge[k] = float(edge[k])

    return edges_list


# Gets the shortest route as distance, next destination tuples given a list of package ids and a list of distances ->
# O(N^2)
def get_route(package_ids, distances):
    # Creates a hash map of destinations matching package_ids -> O(N^2)
    destinations_hash_map = HashMap()
    package_list = [packages.map[j] for j in package_ids]
    for package in package_list:
        if package is not None:
            for distance in distances:
                if distance is not None:
                    if package[0][1] in distance[0]:
                        destinations_hash_map.add(distances.index(distance), distance[0])

    # Converts the destinations_hash_map into a list and gets a hash map of the shortest_path -> O(N)
    shortest_path_hash_map = HashMap()
    destinations_list = list()
    for destination in destinations_hash_map.map:
        if destination is not None:
            destinations_list.append(destination[0][0])
            shortest_path_hash_map.add(destination[0][0], shortest_path[destination[0][0]])

    # Gets a list of the closest next destinations -> O(N)
    shortest_route = list()
    for shortest in shortest_path_hash_map.map:
        if shortest is not None:
            shortest_route.append(shortest)

    # Gets a list of destinations as distance, destination tuples -> O(N^2)
    shortest_route_sorted = sorted(shortest_route, key=(lambda x: x[0][1][0]))
    remaining_deliveries = list(j[0][0] for j in shortest_route_sorted)
    ideal_route = list()
    ideal_route.append(shortest_path_hash_map.map[remaining_deliveries[0]])
    initial_distance = min([j for j in shortest_route_sorted[0][0][1] if j != 0])
    distance_destination = list()
    distance_destination.append((initial_distance, shortest_route_sorted[0][0][0]))
    remaining_deliveries = list(filter(lambda x: x != shortest_route_sorted[0][0][0], remaining_deliveries))
    while remaining_deliveries:
        next_distances = ideal_route[-1][0][1]
        min_distance = min([(k, j) for j, k in enumerate(next_distances) if (j in set(remaining_deliveries)) &
                            (k != 0)])
        next_destination = min_distance[1]
        distance_destination.append((min_distance[0], next_destination))
        ideal_route.append(shortest_path_hash_map.map[next_destination])
        remaining_deliveries = list(filter(lambda x: x != next_destination, remaining_deliveries))

    # Adds the return trip to the hub onto the list -> O(1)
    distance_destination.append((shortest_path_hash_map.get(distance_destination[-1][1])[0], 0))

    return distance_destination


# Updates the position of all packages at a given time -> O(N^3)
def update_package_position(time):
    time_delta = datetime.timedelta(hours=time.hour, minutes=time.minute)
    first_truck_travel_time = time_delta - first_truck_start_delta
    second_truck_travel_time = time_delta - second_truck_start_delta
    third_truck_travel_time = time_delta - third_truck_start_delta
    first_time_in_hours = first_truck_travel_time.total_seconds()/3600
    second_time_in_hours = second_truck_travel_time.total_seconds()/3600
    third_time_in_hours = third_truck_travel_time.total_seconds()/3600
    distance_first_truck = first_time_in_hours * 18
    distance_second_truck = second_time_in_hours * 18
    distance_third_truck = third_time_in_hours * 18
    current_stop_first_route = 0
    current_distance_first_driver = 0
    current_stop_second_route = 0
    current_distance_second_driver = 0
    current_stop_third_route = 0

    # Updates package status based on time -> O(N^2)
    update_package(first_time_in_hours, 1)
    update_package(second_time_in_hours, 2)
    update_package(third_time_in_hours, 3)

    # Updates packages arriving at 9:05 am -> O(N^3)
    if time_delta == datetime.timedelta(hours=9, minutes=5):
        for j in [6, 25, 28, 32]:
            packages.update_at(str(j), "at the hub", 7)

    # Updates deliveries based on elapsed time and distance -> O(N^3)
    while current_distance_first_driver < distance_first_truck:
        current_distance_first_driver += route_one[current_stop_first_route][0]
        current_time_first_driver = first_truck_start_delta + datetime.timedelta(hours=current_distance_first_driver/18)

        for item in package_destination:
            if (route_one[current_stop_first_route][1] == item[1]) & (int(item[0]) in first_truck_indices) & \
                    (current_time_first_driver < time_delta):
                delivery_string = "delivered at " + str(current_time_first_driver)
                packages.update_at(item[0], delivery_string, 7)

        current_stop_first_route += 1
        if current_stop_first_route == len(route_one):
            break

    while current_distance_second_driver < distance_second_truck:
        current_distance_second_driver += route_two[current_stop_second_route][0]
        current_time_second_driver = second_truck_start_delta + datetime.timedelta(
            hours=current_distance_second_driver / 18)

        for item in package_destination:
            if (route_two[current_stop_second_route][1] == item[1]) & (int(item[0]) in second_truck_indices) & \
                    (current_time_second_driver < time_delta):
                delivery_string = "delivered at " + str(current_time_second_driver)
                packages.update_at(item[0], delivery_string, 7)

        current_stop_second_route += 1
        if current_stop_second_route == len(route_two):
            break

    # Sends the first truck back out if it finished the first route -> O(N^3)
    if current_stop_first_route == len(route_one):
        current_distance_first_driver = 0
        while current_distance_first_driver < distance_third_truck:
            current_distance_first_driver += route_three[current_stop_third_route][0]
            current_time_first_driver = third_truck_start_delta + datetime.timedelta(
                hours=current_distance_first_driver / 18)

            for item in package_destination:
                if (route_three[current_stop_third_route][1] == item[1]) & (int(item[0]) in third_truck_indices) & \
                        (current_time_first_driver < time_delta):
                    delivery_string = "delivered at " + str(current_time_first_driver)
                    packages.update_at(item[0], delivery_string, 7)

            current_stop_third_route += 1
            if current_stop_third_route == len(route_three):
                break


# Updates package status based on time -> O(N^2)
def update_package(time_in_hours, truck_num):
    indices = list()
    if truck_num == 1:
        indices = first_truck_indices
    elif truck_num == 2:
        indices = second_truck_indices
    elif truck_num == 3:
        indices = third_truck_indices

    if time_in_hours > 0:
        for j in indices:
            packages.update_at(str(j), "en route", 7)
    elif time_in_hours == 0:
        for j in indices:
            packages.update_at(str(j), "at the hub", 7)


# Gets the total distance for all routes -> O(N)
def get_total_distance():
    sum_1 = sum([j[0] for j in route_one])
    sum_2 = sum([j[0] for j in route_two])
    sum_3 = sum([j[0] for j in route_three])

    return sum_1 + sum_2 + sum_3


# Prints information about a specific package -> O(N)
def print_package(key):
    print("Package ID".ljust(10),
          "Address".ljust(40),
          "City".ljust(20),
          "State".ljust(5),
          "Zip".ljust(10),
          "Delivery Deadline".ljust(20),
          "Kilos".ljust(5),
          "Special Notes".ljust(70),
          "Location".ljust(1))
    print(packages.get_all(str(key))[0].ljust(10),
          packages.get_all(str(key))[1].ljust(40),
          packages.get_all(str(key))[2].ljust(20),
          packages.get_all(str(key))[3].ljust(5),
          packages.get_all(str(key))[4].ljust(10),
          packages.get_all(str(key))[5].ljust(20),
          packages.get_all(str(key))[6].ljust(5),
          packages.get_all(str(key))[7].ljust(70),
          packages.get_all(str(key))[8].ljust(1),
          )


# Prints information about all packages -> O(N^2)
def print_all_packages():
    print("Package ID".ljust(10),
          "Address".ljust(40),
          "City".ljust(20),
          "State".ljust(5),
          "Zip".ljust(10),
          "Delivery Deadline".ljust(20),
          "Kilos".ljust(5),
          "Special Notes".ljust(70),
          "Location".ljust(1))
    for j in range(1, 41):
        print(packages.get_all(str(j))[0].ljust(10),
              packages.get_all(str(j))[1].ljust(40),
              packages.get_all(str(j))[2].ljust(20),
              packages.get_all(str(j))[3].ljust(5),
              packages.get_all(str(j))[4].ljust(10),
              packages.get_all(str(j))[5].ljust(20),
              packages.get_all(str(j))[6].ljust(5),
              packages.get_all(str(j))[7].ljust(70),
              packages.get_all(str(j))[8].ljust(1),
              )


# Creates the packages hash table -> O(N^2)
with open('WGUPSPackageFile.csv') as csvfile:
    package_file = csv.reader(csvfile, delimiter=',')

    packages = HashMap()

    for row in package_file:
        for i in range(1, len(row)):
            packages.add(row[0], row[i])

# Creates the destination distance list -> O(N)
with open('WGUPSDistanceTable.csv') as csvfile:
    distance_list = list(csv.reader(csvfile, delimiter=','))

# Gets the shortest paths between all destinations -> O(N^3)
edges = distance_list_to_edge_vertex_list(distance_list)
shortest_path = floyd_warshall.shortest_path(len(edges), edges)

# Lists the packages for the first truck load
first_truck_indices = [1, 5, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 19, 20, 31, 34]

# Lists the packages for the second truck load
second_truck_indices = [2, 3, 6, 18, 21, 22, 23, 24, 26, 28, 29, 30, 36, 37, 38, 40]

# Lists the packages for the third truck load
third_truck_indices = [4, 9, 25, 27, 32, 33, 35, 39]

# Gets lists of distance, destination tuples for the package lists -> O(N^3)
route_one = get_route(first_truck_indices, distance_list)
route_two = get_route(second_truck_indices, distance_list)
route_three = get_route(third_truck_indices, distance_list)

# Gets a list of package id, destination id tuples -> O(N^2)
package_destination = list()
package_list = [packages.map[j] for j in list(range(1, 41))]
for package in package_list:
    if package is not None:
        for distance in distance_list:
            if distance is not None:
                if package[0][1] in distance[0]:
                    package_destination.append((package[0][0], distance_list.index(distance)))

# Sets the times for the trucks to leave the hub -> O(1)
first_truck_start = datetime.time(8, 0)
second_truck_start = datetime.time(9, 5)
third_truck_start = datetime.time(10, 20)
first_truck_start_delta = datetime.timedelta(hours=first_truck_start.hour, minutes=first_truck_start.minute)
second_truck_start_delta = datetime.timedelta(hours=second_truck_start.hour, minutes=second_truck_start.minute)
third_truck_start_delta = datetime.timedelta(hours=third_truck_start.hour, minutes=third_truck_start.minute)
