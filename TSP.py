import argparse
import random
import math
from time import time
import geopy.distance

def load_cities(input_file):
    cities = {}
    city_list=[]
    with open(input_file, 'r') as f:
        for line in f:
            name, x, y = line.strip().split(',')
            cities[name] = (float(x), float(y))
            city_list.append(name)
    return cities
 

# Calculate the Straight line distance between two cities
def distance(city1, city2):
    x1, y1 = city1
    x2, y2 = city2
    return geopy.distance.geodesic(city1, city2).km
def random_path(cities):
    tour = list(cities.keys())
    #tour=tour[0:16]
    random.shuffle(tour)
    return tour

# Define the tour length function
def tour_length(tour,cities):
    length = 0
    for i in range(len(tour)-1):
        length += distance (cities[tour[i]],cities[tour[i+1]])
    return length
# Swap two cities in a path
def swap(path, i, j):
    path[i], path[j] = path[j], path[i]

# Perform the Hill Climbing algorithm 
def hill_climb(cities):
    # Generate a random initial path
    current_path = random_path(cities)
    x=current_path
    # Calculate the distance of the current path
    current_distance = tour_length(current_path, cities)
    y= current_distance
    # Keep track of the best path and its distance
    best_path = current_path
    best_distance = current_distance
    # Perform iterations until no better neighbor is found
    while True:
        # Find the best neighbor
        for i in range(len(current_path)):
            for j in range(i+1, len(current_path)):
                # Swap two cities in the path
                swap(current_path, i, j)
                # Calculate the distance of the new path
                new_distance = tour_length(current_path, cities)
                # If the new path is better, remember it
                if new_distance < best_distance:
                    best_path = current_path[:]
                    best_distance = new_distance
                # Swap the cities back to their original positions
                swap(current_path, i, j)
        # If the best neighbor is not better than the current path, stop
        if best_distance == current_distance:
            break
        # Otherwise, move to the best neighbor and continue
        current_path = best_path
        current_distance = best_distance
    # Return the best path and its distance
    return x, y, best_path, best_distance



# Define the acceptance probability function
def acceptance_probability(current_length, new_length, temperature):
    if new_length < current_length:
        return 1.0
    else:
        return math.exp((current_length - new_length) / temperature)
# Define the Simulated Annealing algorithm
def simulated_annealing(cities, temperature, cooling_rate, stopping_temperature, stopping_iter):
    # Initialize the current and best tours
    current_tour = random_path(cities)
    best_tour = current_tour.copy()
    
    # Initialize the current and best tour lengths
    current_length = tour_length(current_tour,cities)
    best_length = current_length
    
    # Initialize the iteration counter
    iteration = 1
    
    # Loop until the stopping criteria are met
    while temperature > stopping_temperature and iteration < stopping_iter:
        # Choose two random cities to swap
        i, j = random.sample(range(len(current_tour)), 2)
       
        # Swap the cities to get a new tour
        new_tour = current_tour.copy()
        new_tour[i], new_tour[j] = new_tour[j], new_tour[i]
        # Calculate the length of the new tour
        new_length = tour_length(new_tour,cities)
        
        # Decide whether to accept the new tour
        if acceptance_probability(current_length, new_length, temperature) > random.random():
            current_tour = new_tour
            current_length = new_length
        
        # Update the best tour if necessary
        if current_length < best_length:
            best_tour = current_tour.copy()
            best_length = current_length
        
        # Update the temperature and iteration counter
        temperature *= cooling_rate
        iteration += 1
    
    return best_tour, best_length




# Define the main function
def main():
    # Define the command-line arguments
    parser = argparse.ArgumentParser('choose one')
  
    parser.add_argument('--algorithm', choices=[ 'hc', 'sa'], required=True,
                        help='Algorithm to use (hc: Hill Climbing, sa: Simulated Annealing)')
    parser.add_argument('--file', type=str, help='The input file containing the city list')
    # Parse the command-line arguments
    args = parser.parse_args()
    
    cities = load_cities(args.file)

    
    # Set the parameters for the Simulated Annealing algorithm
    temperature = 1000.0
    cooling_rate = 0.99
    stopping_temperature = 1e-8
    stopping_iter = 1000
    
    if args.algorithm == 'hc':
        current_path,current_distance,path, distance = hill_climb(cities)
        print('rando path:', ' -> '.join( current_path))
        print('rando path Distance:',  current_distance)
        print('Best path:', ' -> '.join(path))
        print('Distance:', distance)
    elif args.algorithm == 'sa':
        best_tour, best_length = simulated_annealing(cities, temperature, cooling_rate, stopping_temperature, stopping_iter)
        print('Best Tour:', best_tour)
        print('Best Tour Length:', best_length)
        
    start=time()
    # Run the Simulated Annealing algorithm
    best_tour, best_length = simulated_annealing( cities, temperature, cooling_rate, stopping_temperature, stopping_iter)
    
    # Print the results
    print('Best Tour:', best_tour)
    print('Best Tour Length:', best_length)
    end=time()
    print(end-start, 'secs')
if __name__ == '__main__':
    main()
