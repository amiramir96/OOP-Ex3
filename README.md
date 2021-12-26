# OOP-Ex3
 assigment 3 in Object Oriented Programme, implements directed weighted graph, algorithms and gui with python
 
 ## Program Overview
in this assigment we were required to implement Directed Weighted Garph and some choosen algorithms same as the prev assigment, this time in python
the directed weigthed graph/algorithms objects shall implemented within the best time run as possible since its can hold alot of vertex and edges. <br>
in addition, we shall create a GUI programme that support every algorithm that implemented on the graph (for ex, load graph, isConnected, tsp etc..) <br>

Our implementation works in O(1) for all basic operations on the graph (get/add/remove node/edge).

## structre of the project code
the project splits to packges: src (for graph and algorithm files), graphics, tests (will be explained below, not in this topic)

|**package name:**|                                                     **Description**                                                                                      |
|-----------------|----------------------------------------------------------------------------------------------------------------------------------------------------------|
| **src**         |    interfaces of graph, graph algorithms, graph class, graph algorithm class                                                                             
|  **graphics**   |    represent all the GUI classes, with constructing the Window class, the GUI gets open for the user usage, based on pygames                              |
| **Tests**       |   2 categories - 1) Currectness: test each of the public class methods to return currect answer, 2) RunningTime - represented in the file "performance_test.py" | 

## Tests
The "performance_test.py" file is used to test the performaence of the algorithm on graphs with different sizes and for easy comparasion to the results from the prev assigment.  
It can be called from the cmd or be given the number of nodes for the graph.  
`Python3 PerformanceTest.py`, if u would like to see the comparasion test agains the java project, input 0 in place of natural number.  
Unless u input "0" for the compare test, The program will create a random graph with the specified number of nodes in the folder and test the elapsed time of multiple implemented methods on that graph.
<br>

## graphics - GUI  אורי טיפולך


---------------------<br>
אורי טיפולך
---------------------<br>

### logic system אורי טיפולך


### how to use / tutorial אורי טיפולך


## Download

---------------------<br>
אורי טיפולך
---------------------<br>

## Running The Simulation
---------------------<br>
אורי טיפולך
---------------------<br>

## Running Time Results
<br>

---------------------<br>
אחריות אמיר
---------------------<br>

|**Node_size**|**Edge_size**|**construct graph**|**isConnected**   |**shortestPath**  | **shortestPathDist** |  **center**         | **tsp for 20 nodes** |
|-------------|-------------|-------------------|------------------|------------------|----------------------|---------------------|----------------------|
|    100      |    2000     |                   |                  |                  |                      |                     |                      |
|   1,000     |  20,000     |                   |                  |                  |                      |                     |                      | 
| 10,000      | 200,000     |                   |                  |                  |                      |                     |                      |
| 100,000     | 2,000,000   |                   |                  |                  |                      |                     |                      |
| 1,000,000   |  20,000,000 |                   |                  |                  |                      |                     |                      |



<br>

## Assigment instructions
The instructions for this assignment can be found here (Hebrew):  
https://docs.google.com/document/d/15sTWy_pa6Vg4r7phAC322vZA169V02yezjxxf4b9sJc/edit
<br>

## Review of the Literature
BFS - https://en.wikipedia.org/wiki/Breadth-first_search , https://www.youtube.com/watch?v=oDqjPvD54Ss&t=282s <br>
Dijksta - https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm , https://www.youtube.com/watch?v=pSqmAO-m7Lk&t=776s <br>
tsp algorithms (which helped to get ideas) - https://www.youtube.com/watch?v=M5UggIrAOME , https://en.wikipedia.org/wiki/Travelling_salesman_problem <br>
Directed Weighted Graph implemantation in java: https://github.com/amiramir96/Ex2-OOP <br>
guide for multi process in python: https://www.youtube.com/watch?v=fKl2JW_qrso&t=1015s <br>
 
