from __future__ import annotations
from csv import reader
import random
from typing import List
import subprocess
import requests

class Location():
    def __init__(self, name: str, latitutude: str, longitude: str) -> None:
        self.name = name
        self.latitude = float(latitutude)
        self.longitude = float(longitude)
    
    def __repr__(self) -> str:
        return f"Name: {self.name}, Latitude: {self.latitude}, Longitude: {self.longitude}\n"

def parse_locations(filename: str) -> List[Location]:
    locations = []
    with open(filename, 'r') as f:
        csv_reader = reader(f)
        for row in csv_reader:
            loc = Location(row[0], row[1], row[2])
            locations.append(loc)
    return locations

def generate_initial_population(population_size: int, num_locations: int) -> List[List[int]]:
    population = []
    random.seed(42)
    for _ in range(population_size):
        population_member = list(range(1, num_locations))
        random.shuffle(population_member)
        population_member.insert(0, 0)
        population.append(population_member)
    return population

def convert_to_radians(location: Location) -> Location:
    location_radians = Location(location.name, location.latitude, location.longitude)
    location_radians.latitude = location.latitude * 0.0174533
    location_radians.longitude = location.longitude * 0.0174533
    return location_radians

class FitnessPair():
    def __init__(self, id: int, fitness: float) -> None:
        self.id = id
        self.fitness = fitness
    
    def __repr__(self) -> str:
        return f"Id: {self.id}, Fitness: {self.fitness}\n"

    def __lt__(self, obj: FitnessPair) -> bool:
        return ((self.fitness) < (obj.fitness))
  
    def __gt__(self, obj: FitnessPair) -> bool:
        return ((self.fitness) > (obj.fitness))
  
    def __le__(self, obj: FitnessPair) -> bool:
        return ((self.fitness) <= (obj.fitness))
  
    def __ge__(self, obj: FitnessPair) -> bool:
        return ((self.fitness) >= (obj.fitness))
  
    def __eq__(self, obj: FitnessPair) -> bool:
        return (self.fitness == obj.fitness)

class ParentPair():
    def __init__(self, first: int, second: int) -> None:
        self.first = first
        self.second = second
    
    def __repr__(self) -> str:
        return f"Parents: {self.first}, {self.second}\n"

def calculate_haverstine_distance_hidden(loc_1: Location, loc_2: Location) -> float:
    # p = subprocess.Popen(['./haversine', str(loc_1.latitude), str(loc_1.longitude), str(loc_2.latitude), str(loc_2.longitude)], stdout=subprocess.PIPE)
    # output, _ = p.communicate()
    # dist = float(output.decode('utf-8'))
    params = {"lat_1": loc_1.latitude, "lon_1": loc_1.longitude, "lat_2": loc_2.latitude, "lon_2": loc_2.longitude }
    r = requests.get(url = 'https://c2vow4thgaizqmyszu3zmgwi640oljvc.lambda-url.us-east-2.on.aws/', params = params)
    # print('r: ', r.json())
    # return dist
    return r.json()['distance']

def validate_solution(solution: List[int], score: float, locations: List[Location]) -> None:
    is_valid = True
    if len(solution) != len(set(solution)):
        print('Cannot visit a location more than once')
        is_valid = False
    if len(solution) == len(set(solution)) and len(solution) != len(locations):
        print('Must visit every location')
        is_valid = False
    if solution[0] != 0:
        print('Must start traversal at LAX (idx 0 of locations)')
        is_valid = False
    solution_locations = [locations[i] for i in solution]
    fitness = sum([calculate_haverstine_distance_hidden(x, y) for x, y in zip(solution_locations[1:], solution_locations)])
    fitness += calculate_haverstine_distance_hidden(solution_locations[-1], solution_locations[0])
    if round(score, 4) != round(fitness, 4):
        print('Fitness score computed incorrectly')
        is_valid = False
    return is_valid

