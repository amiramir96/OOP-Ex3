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
| **Tests**       |   2 categories - 1) Currectness: test each of the public class methods to return currect answer, 2) RunningTime - represented in the file "perform_test.py" | 

## Tests
The "perform_test.py" file is used to test the performaence of the algorithm on graphs with different sizes and for easy comparasion to the results from the prev assigment.  
It can be called from the cmd or be given the number of nodes for the graph.  
`py perform_test.py`, if u would like to see the comparasion test agains the java project, input 0 in place of natural number BUT before, extract the ZIP file of 100Kperformance that direct at the folder tests -> performance <br>  
Unless u input "0" for the compare test, The program will create a random graph with the specified number of nodes in the folder and test the elapsed time of multiple implemented methods on that graph.
<br>
for compare test please ENSURE that u downloaded the whole tests folder and extracted inside the performance folder the 100Kperforamnce.zip file (for the 100K.json graph)
<br>

## graphics - GUI  
The program includes an easy-to-use Graphic User Interface for performing basic tasks on the graph.  
The GUI allows for discovering information about the graph, you can find the center node of the graph (the node with the minimal maximum distance with the other nodes)  
you can find the shortest path between two nodes  
you can find the (almost) best route throgh multiple nodes

### Running The Simulation 
To run the GUI import the project and run `python Ex3.py <graph path>` in the comand line at the primary folder.  
For Example:  `python Ex3.py data/A2.json` will give you the following window: 

![GUI sample image](https://github.com/amiramir96/OOP-Ex3/blob/a7924036eedf118aa5675a03afb6547a124e51a8/wiki%20images/GUI_sample.jpg)

### how to use / tutorial 
To find the center of the grph, press the `center` button. The center node wil turn green, and the min-mx distance will be shown o the button.  
the find the shortest path between 2 node chose the nodes by clicking on them, then press `shortest path`. the shortest path will be marked and the distance will be showen on the button.  
The same goes for `TSP` (shortest path covering multiple nodes), chose your nodes and press the button.

The reset button is used to reset the GUI, you you misclicked or want to check something else just click it and start over.

## Running Time Results
<br>
here is a table for RUNNING TIME of graphs with 100, 1000, 10000, 100K, 1M nodes (and 20 out edges for ea node in avg) <br>

for comparasion results between java and python implementation click here: https://github.com/amiramir96/OOP-Ex3/wiki/Compare-java-VS-python-projects <br>

|**Node_size**|**Edge_size**|**construct graph**|**isConnected**   |**shortestPath**  |  **center**          | **tsp for 20 nodes** |
|-------------|-------------|-------------------|------------------|------------------|----------------------|----------------------|
|    100      |    2000     |   18 ms           | 1 ms             | 4 ms             |  450 ms              |92 ms                 |
|   1,000     |  20,000     |       62 ms       |     19 ms        | 62 ms            |     14 sec           |1 sec                 | 
| 10,000      | 200,000     |      647 ms       |       178 ms     | 806 ms           |     1959 sec         |16 sec                |
| 100,000     | 2,000,000   |        6 sec      |    2 sec         | 7 sec            |timeout(apx 200 hours)|144 sec               |
| 1,000,000   |  20,000,000 |        78 sec     |      26 sec      | 95 sec           |timeout(apx 10 years) |1998 sec              |



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
 
