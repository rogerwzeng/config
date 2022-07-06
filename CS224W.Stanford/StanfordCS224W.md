## Stanford CS224W Machine Learning w/ Graph
#### Lecture Notes

### Concepts and Definitions
**What is a graph?**

**Heterogeneous Graph**
$$G = (V, E, R, T)$$

**Homogeneous Graph**
$$G = (V, E)$$
#### Degree Connection

**Undirected Graph**

Avg Degrees: 
$$\bar K = \frac {1}{n} \sum_i K_i = \frac {\sum_{i,j}A_{ij}}{n} = \frac{2m}{n}$$
where:
+ m = |E| (# of edges)
+ n = |V| (# of nodes)
There is a **2** because, in a undirected graph, each edge is counted twice to account for both nodes on the two ends of a edge.

