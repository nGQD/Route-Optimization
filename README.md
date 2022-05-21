# DO NOT LEAK THE CODES TO OTHER GROUPS

## Dataset
I converted the .csv given by Dr to excel as the unicodes weren't able to be parsed correctly. Moreover, duplicate entries are detected so I have to perform cleaning. 

## Problem 1
The approach to problem 1 is by dumping all the keywords into a Python set whose internal implementation utilizes a hash table. Thus, average operations are O(1) and I doubt other solutions can reach the efficiency & simplicity.  
I've completely exported the positive, negative along with the stop words into respective sets. But I haven't textise online articles and perform intersection operation on them to get the word ratio for the scatterplot.

## Problem 2
I've employed a modified Monte Carlo Tree Search with Nested Rollout Policy Adaptation. The method guarantees optimal solution as long as sufficient time is given and the hyperparameters are appropriately tuned. I pick depot by evaluating their distances against the centroid. The map is plotted using Google Maps API so you'd need a GCS account and an API key to run the script. By the way, the distance is evaluated as such that it takes the curvature of the Earth into consideration. This is especially significant when it comes to cases in countries like CN due to the massive geometrical disparities.

  
Ask me anything :)

