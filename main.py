import math
import time
import random
import pandas as pd
import googlemaps
import geopy as gp
from geopy.distance import geodesic
import matplotlib.pyplot as plt

API_KEY = ""
N = 7
COUNTRY = ["CA", "GB", "PH", "SG", "US"]


def generate_ranking(title: str, values: list) -> None:
    print(f"\n{title}")
    ranking = dict(zip(values, COUNTRY))
    sorted_ranking =  sorted(ranking)
    for place, key in enumerate(sorted_ranking, 1):
        print(f"{place}: {ranking[key]}")


### PROBLEM 1 ###
POSITIVE, NEGATIVE, STOPWORD = [set(open(f"../sentiment/{file}.txt", encoding="utf-8").read().split(",")) for file in ["POSITIVE", "NEGATIVE", "STOPWORD"]]

articles = [set(open(f"../country/{file}.txt", encoding="utf-8").read().split()) for file in COUNTRY]
filtered_articles = [set(article - STOPWORD) for article in articles]

word_count         = [len(article) for article in articles]
stopword           = [len(article & STOPWORD) for article in articles]
filtered_count     = [len(article) for article in filtered_articles]
neutral            = [len(article & POSITIVE | article & NEGATIVE) for article in filtered_articles]
positive, negative = [[len(article & file) for article in filtered_articles] for file in [POSITIVE, NEGATIVE]]


negative_per_positive = [negative[i] / positive[i] for i in range(len(negative))]
negative_per_count    = [negative[i] / filtered_count[i] for i in range(len(negative))]

negativity = [(2 * negative_per_positive[i] * negative_per_count[i]) / (negative_per_positive[i] + negative_per_count[i]) for i in range(len(negative_per_positive))]


def plot(array: list, title: str, ylabel: str, colour: str):
    plt.bar(COUNTRY, array, color=colour)
    plt.title(title)
    plt.xlabel("COUNTRY")
    plt.ylabel(ylabel)
    plt.show()

plot(word_count, "Article Word Count", "Word Count", "black")
plot(stopword, "Article Stopword Count", "Stopword Count", "blue")
plot(filtered_count, "Article Filtered Word Count", "Filtered Word Count", "purple")
plot(neutral, "Article Neutral Word Count", "Neutral Count", "yellow")
plot(positive, "Article Positive Word Count", "Positive Count", "green")
plot(negative, "Article Negative Word Count", "Negative Count", "red")
plot(negative_per_positive, "Article Negative/Positive Ratio", "Negative Per Positive Count", "orange")
plot(negative_per_count, "Article Negative/Filtered Word Count Ratio", "Negative Per Filtered Count", "pink")

plot(negativity, "Negativity", "Negativity", ["red", "yellow", "green", "cyan", "purple"])
generate_ranking("Ranking of Most Recommended country for Expansion Based on Article Reviews", negativity)


### PROBLEM 2 ###
class Route:
    def __init__(self, cost) -> None:
        self.stops = [(0, X, Y)]
        self.cost = cost

    def append(self, location) -> None:
        _, xx, yy = self.stops[-1]
        self.stops.append(location)
        _, x, y = location
        self.cost += geodesic((x, y), (xx, yy)).km
    
    def successors(self) -> list:
        return list(zip(*list(set(global_stops) - set(self.stops))))[0] if set(global_stops) - set(self.stops) else []
    
    def __str__(self) -> str:
        return f"Route: {' -> '.join(map(str, list(zip(*self.stops))[0]))}\nCost:  {self.cost}"


def mcts(level: int, iterations: int) -> Route:
    best_route = Route(float('inf'))
    if not level:
        return rollout()
    else:
        global policy
        global_policy[level] = policy
        for i in range(iterations):
            route = mcts(level-1, i)
            if route.cost < best_route.cost:
                best_route = route
                adapt(best_route, level)
            if time.perf_counter_ns() - INITIAL_TIME >= MAX_SEARCH_TIME:
                return best_route
        policy = global_policy[level]
    return best_route


def adapt(route: Route, level: int) -> None:
    for stop, next_stop in zip(route.stops[0:], route.stops[1:]):
        global_policy[level][stop[0]][next_stop[0]] += ALPHA
        z = sum([math.exp(global_policy[stop[0]][move[0]]) for move in route.successors() if not evaluated[move[0]]])
        for move in route.successors():
            if not evaluated[move[0]]:
                global_policy[level][stop[0]][move[0]] -= ALPHA * math.exp(policy[stop[0]][move[0]]) / z
        evaluated[stop[0]] = 1
        

def rollout() -> Route:
    route = Route(0)
    while True:
        stop = route.stops[-1][0]
        successors = route.successors()
        if not successors:
            route.append((0, X, Y))
            break
        probabilities = [0] * len(successors)
        probability_sum = 0
        for i in range(len(successors)):
            probabilities[i] = math.exp(policy[stop][successors[i]])
            probability_sum += probabilities[i]
        mrand = random.random() * probability_sum
        i = 0
        probability_sum = probabilities[0]
        while probability_sum < mrand:
            i += 1
            probability_sum += probabilities[i]
        route.append((successors[i], global_stops[successors[i]][1], global_stops[successors[i]][2]))
    return route

gm = googlemaps.Client(key=API_KEY)

df = pd.read_excel(r"../raw.xlsx")

costs = []

for country in COUNTRY:

    df_country = df.loc[df["country"] == country]["street_address"]
    stores = df_country.sample(n=N, random_country=42)

    global_stops = [(gl.latitude, gl.longitude) for gl in list(map(gp.geocoders.GoogleV3(api_key=API_KEY).geocode, list(stores))) if gl]
    coordinates = list(zip(*global_stops))
    centroid = sum(coordinates[0]) / len(global_stops), sum(coordinates[1]) / len(global_stops)
    distances = [geodesic(centroid, gl).km for gl in global_stops]
    X, Y = global_stops[distances.index(min(distances))]
    global_stops.remove((X, Y))
    global_stops = [(0, X, Y)] + [(index, *element) for index, element in enumerate(global_stops, 1)]
    coordinates.append((X, Y))

    LEVEL = 3
    ITERATIONS = 1000
    ALPHA = 1e-1
    MAX_SEARCH_TIME = 60e9


    global_policy = [[[0] * N] * N] * LEVEL
    policy = [[0] * N] * N
    evaluated = [1] + [0] * (N - 1)

    INITIAL_TIME = time.perf_counter_ns()


    route = mcts(LEVEL-1, ITERATIONS)
    costs.append(route.cost)
    print(f"\ncountry: {country}\n{route}")

    addresses = []
    for _, x, y in route.stops:
        addresses.append(gm.reverse_geocode((x, y))[0]["formatted_address"])
    markers = ["color:blue|size:mid|label:" + str(0 + i) + "|" + a for i, a in enumerate(addresses)]

    plot = gm.static_map(
                    center=addresses[0],
                    scale=2, 
                    zoom=4.5,
                    size=[1080, 1080], 
                    format="png", 
                    maptype="roadmap",
                    markers=markers,
                    path="color:0xA020F0|weight:2|" + "|".join(addresses))

    with open(f"../output/{country}.png", "wb") as img:
        for chunk in plot:
            img.write(chunk)

    plt.imshow(plt.imread(f"../output/{country}.png"))
    plt.show()
    

generate_ranking("Ranking of Most Recommended country for Expansion Based on Traveling Distances", costs)


### PROBLEM 3 ###
sqrt_area = [math.sqrt(9093507), math.sqrt(241930), math.sqrt(298170), math.sqrt(709.2), math.sqrt(9147593)]

normalized_costs = [cost / weight for cost, weight in zip(costs, sqrt_area)]
final_ranking = [cost * weight for cost, weight in zip(normalized_costs, negativity)]

generate_ranking("Final Ranking of Most Recommended country for Expansion", final_ranking)