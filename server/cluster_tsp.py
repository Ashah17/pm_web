from .mapping import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cvxpy as cp
from geopy import distance
from sklearn.cluster import KMeans
import folium


def solve_tsp_on_clusters(place, attractions, k):

    #attractions is list of places AND restaurants
    #k is number of days you have to visit all attractions (k clusters)

    attractions_defined = [] #def to location

    for attr in attractions:
        #append the place to attractions so that limited to that place
        attractions_defined.append(str(attr) + " " + str(place))
    

    coords = places_to_coords(attractions_defined) #pass in the attractions defined list

    #coords has centroid in beginning as well

    #create k clusters for these coords

    coords = np.array(coords) #np array

    clusters = k_means(k, coords)

    # Solve TSP for each cluster and print results

    
    # Initialize map centered around the points

    map_data = {} #sending data to frontend

    m = folium.Map(location=[np.mean(coords[:, 0]), np.mean(coords[:, 1])], zoom_start=13)

    # Solve TSP for each cluster and plot results
    for cluster_id, cluster_points in clusters.items():
        route_indices = tsp(cluster_points)
        route_points = [np.mean(cluster_points, axis=0)] + [cluster_points[i - 1] for i in route_indices[1:]]

        map_data[cluster_id] = {
            'points': cluster_points.tolist(),
            'centroid': np.mean(cluster_points, axis=0).tolist(),
            'route': [list(point) for point in route_points]
        }
        
        # Plot the points
        for point in cluster_points:
            folium.Marker(location=[point[0], point[1]], popup=f"Cluster {cluster_id}").add_to(m)
        
        # Plot the centroid
        centroid = np.mean(cluster_points, axis=0)
        folium.Marker(location=[centroid[0], centroid[1]], popup=f"Cluster {cluster_id} Centroid", icon=folium.Icon(color='red')).add_to(m)
        
        # Plot the route
        folium.PolyLine(locations=[[point[0], point[1]] for point in route_points], color='blue').add_to(m)

    map_name = str(place) + "_map.html"
    m.save(map_name)

    #do all the saving above to backend html files AND then send data to frontend too:

    return map_data

    




# def tsp(coords):
#     # locs, coords = map_return()

#     # first_place_coords = coords[0] #first place, for trial

#     #add the centroid as first element of list to use as origin

#     n = len(coords) #set n
#     k = 2 #do 2 days for each place for now

#     distance_matrix = dist_matrix(coords) #make distance mat

#     X = cp.Variable(distance_matrix.shape, boolean=True) #boolean x variable: if edge exists or not
#     u = cp.Variable(n, integer=True) #the edge weight (cost of edge)

#     ones = np.ones((n, 1))

#     objective = cp.Minimize(cp.sum(cp.multiply(distance_matrix, X))) #objective function

#     constraints = []
#     constraints += [X @ ones == ones]
#     constraints += [X.T @ ones == ones]
#     constraints += [cp.diag(X) == 0]
#     constraints += [u[1:] >= 2]
#     constraints += [u[1:] <= n] #bounding the # of edges of everything except origin to 1
#     constraints += [u[0] == 1]

#     for i in range(1, n):
#         for j in range(1, n):
#             if i != j:
#                 constraints += [u[i] - u[j] + 1 <= (n - 1) * (1 - X[i, j])]

#     prob = cp.Problem(objective, constraints)
#     prob.solve() #solve it

#     X_sol = np.argwhere(X.value == 1)
#     orden = [X_sol[0, 0]]

#     for i in range(1, n):
#         row = orden[-1]
#         next_node = X_sol[row, 1]
#         if next_node in orden:
#             break
#         orden.append(next_node)

#     return orden


def tsp(coords):
    n = len(coords)  # Number of coordinates

    print("THESE R COORDS")
    print(coords)

    if n < 2:
        raise ValueError("At least two coordinates are required.")

    distance_matrix = dist_matrix(coords)  # Distance matrix

    X = cp.Variable((n, n), boolean=True)  # Boolean variable for edge existence
    u = cp.Variable(n, integer=True)  # Integer variable for node degrees

    ones = np.ones(n)

    # Objective function: Minimize the total distance
    objective = cp.Minimize(cp.sum(cp.multiply(distance_matrix, X)))

    constraints = [
        X @ ones == ones,  # Each node must be visited exactly once
        X.T @ ones == ones,
        cp.diag(X) == 0,  # No self-loops
        u[1:] >= 2,  # Constraints on the node degrees
        u[1:] <= n,
        u[0] == 1  # The degree of the starting node
    ]

    # Subtour elimination constraints
    for i in range(1, n):
        for j in range(1, n):
            if i != j:
                constraints.append(u[i] - u[j] + 1 <= (n - 1) * (1 - X[i, j]))

    prob = cp.Problem(objective, constraints)
    prob.solve()  # Solve the problem

    # Check if a solution was found
    if prob.status != cp.OPTIMAL:
        raise ValueError(f"No optimal solution found: {prob.status}")

    # Extract solution
    X_value = X.value
    if X_value is None:
        raise ValueError("No solution value found for X.")

    X_sol = np.argwhere(X_value > 0.5)  # Use a threshold to handle numerical precision

    if X_sol.size == 0:
        raise ValueError("No solution found.")

    # Create the route from the solution
    orden = [X_sol[0, 0]]  # Start with the first node

    for _ in range(n - 1):
        row = orden[-1]
        # Find the next node in the tour
        next_nodes = X_sol[X_sol[:, 0] == row, 1]
        if next_nodes.size == 0:
            raise ValueError(f"No valid path found from node {row}")
        next_node = next_nodes[0]
        if next_node in orden:
            break
        orden.append(next_node)

    return orden


def dist_matrix(coords):
    #creating distance matrix

    n = len(coords)
    mat = np.zeros((n,n)) #n by n zeroes

    for i in range(0, n):
        for j in range(0, n):
            mat[i, j] = distance.distance(coords[i], coords[j]).km

    return mat


def k_means(k, coords):
    #pass in the # of clusters

    points = np.array(coords) #make np array

    kmeans = KMeans(n_clusters=k, random_state=0).fit(points) #k means
    labels = kmeans.labels_

    clusters = {i: points[labels == i] for i in range(k)} #creating the clusters as a dict

    return clusters


# solve_tsp_on_clusters()