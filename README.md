# cs330_transportation_networks
Implements a variety of algorithms to produce quick query times for the transportation network problem. Includes
Brute Force Dijkstra's Algorithm, Arc Flags, Contraction Hierarchy, A*, as well as our own algorithm.

# `requirements.txt`
Use $pip install -r `requirements.txt` to install nessasary packages. 

# `test.py`
This function contains instances of all algorithms. There are very detailed instructions on how to run the file, and
customize which graph is used. This file is delicate, and will run how it is currently set up. Any changes require knowledge on how the algorithms are set up, otherwise user may receive errors. 

# `src/` 
Contains the graph class. 

# `/Algorithms/` 
Contains all the class files for different algorithms. 

# `ArcFlagInstances/`
Contains pickle files of the prerprocessed arc flag graph. Can only run the custom algorithm and arc flag query with these instances. 

# `Data/`
Contains CSV files of the graph maps. 
