# Truck route optimization with MCTS and NRPA

# Stakeholder Requirements

*censored* is a coffee chain that has stores located all over the world. The company is constantly looking at running better logistics as well as expanding to open more stores at strategic locations. You have been hired to do analysis and provide insights to the management for making business decisions.  
You have been given a sample dataset that contains the location of *censored* stores all over the world. Please use this list to determine the country in Problem 1 and the location of the store in Problem 2.


Problem 1: *censored* is always looking at the possibilities of expanding its business by adding many stores around the world. To do this, they need to analyse local economic and social situations to ensure maximum profits. 
1.	Select any five (5) countries from the list.
2.	Find five (5) articles from online news websites that have published stories related to each country’s local economy and social situation.
3.	Analyze positive, negative, and neutral words of the article to give insights into the local economic and social situation.
4.	Visualize the word count.
5.	Plot any related graphs to show useful information about the analysis.
6.	Give an algorithmic conclusion regarding the sentiment of those articles


Problem 2: Usually, *censored* delivers stocks from a warehouse in the region. But recently, the company decided that they want to have a local central distribution centre in each country. The stocks will be delivered according to a daily schedule by truck to all the stores in the country. To ensure delivery is optimised, delivery routes will be generated for each of the delivery trucks. 
1.	Determine which store to be used for the distribution centre in five (5) of the countries used in Problem 1. The store selected must be in the centre of at least 5 local stores. 
2.	All deliveries will start from and end at the distribution centre. Obtain and show the shortest path for the delivery truck to make an optimal delivery. Keep track of the total distance the truck will be making for the delivery for each of the countries.

Problem 3: The expansion of business in a country is not only determined by the local economic and social situation of the country, but the running cost for delivering logistics needs to be considered as well. Usually, a new store location will be determined by how much is spent on delivery. Based on the ranking of countries and the total journey made for deliveries of each country, determine the final ranking of countries where new stores can be located.
3.	Calculate the probability of a country that has a good local economic and social situation with the lowest optimal delivery. Then, write the summary, ranking from the most recommended countries to the least recommended countries to have an expansion.


# Design Intuitions

## Dataset
The raw CSV was converted to Excel as the Unicode weren't able to be parsed correctly. Moreover, duplicate entries are detected so I have to perform cleaning. 

## Problem 1
The approach to problem 1 is by dumping all the keywords into a Python set whose internal implementation utilizes a hash table. Thus, average operations are O(1) and I doubt other solutions can reach the efficiency & simplicity.  
I've completely exported the positive, and negative along with the stop words into respective sets with an examination of online articles and performed intersection operations on them to get the word ratio for the scatterplot.

## Problem 2
I've employed a modified Monte Carlo Tree Search with Nested Rollout Policy Adaptation. The method guarantees optimal solution as long as sufficient time is given and the hyperparameters are appropriately tuned. I pick depots by evaluating their distances against the centroid. The map is plotted using Google Maps API so you'd need a GCS account and an API key to run the script. By the way, the distance is evaluated as such that it considers the curvature of the Earth. This is especially significant when it comes to cases in countries like CN due to the massive geometrical disparities.

