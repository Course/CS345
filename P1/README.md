# Algorithm is described here .

Given n vertices we do the following 
An array of n nodes which are single node avl tree . 
Description of node :

* Left , Right and Parent pointer .
* Weight corresponding to each left and right pointer .
* Minimum weight in the subtree rooted at that node . We have to take care of this during merge and split  operations. 
* An add factor to the weights maintained at the node . So weight of each node in the subtree = net weight + add factor . This is to take care of the multi add operation . 
* Reverse bit maintained at the node . If it is 0 then actual.left= node.left and same for right . If 1 then opposite . Net effect is the XOR of all the reverse bits . Take care of it during split and merge . 

Operations are performed as follows :

* link(u,v,w) : 

    * lookup nodes corresponding to u and v . O(1) for the array lookup. 
    * go to the roots . O(log n) 
    * perform merge(u,v). O(log n)

* cut(u,v) :

    * lookup nodes u and v . O(1)
    * perform split(u) . Note smaller tree contains all nodes <= u . O(log n).
    * Note We have to start travelling up from u upto the root. As there is no explicit total order we can not search u in the tree once we are at root. So We have to perform split in reverse order . Also dont forget to take care of add factor and reverse bits and minimum weight field.  

* multi_add_weight(u,v,d)
    
    * lookup nodes u and v . O(1)
    * Add weight to all the edges from u to the common ancestor , similarly add weight to all the edges from v to common ancestor .O(log n 
    * While moving up from u and v change the add factor field for the necessary children of the nodes on the path . 

* Reverse(u) 

    * Go to the root and change the reverse bit . 

* report_min(u,v) : 
    
    * It is similar to the traversal done in multiadd weight . Just find the minimum of all the edges on the path from u to common ancestor . From v to common ancestor and the necessary minimum taken from the children of the nodes on the path . 

* Is_reachable(u,v) :
    
    * Find the common ancestor of u and v . If no common ancestor then false. Let u' be the node just below ancestor on path to u . and similarly for v
    * Calculate the XOR of reverse bits from root to the ancestor . 
    * If ancestor.left = u' and ancestor.right=v' then true else false . 

Notes :
* Take care of cases when node.left or node.right is null for a node on the path up u in report_min or multi_add operation . 

Merge(u,v) : nodes(u)<nodes(v) 
    
    * Take care of XOR reverse bit while travelling . 
    * In actual algorithm you have to keep on travelling node.left or always node.right. but here it can be both mixed due to reverse bits .
    * Take care of the minimum weight field while merging. 

Split(u) :

    * Take care of XOR reverse bit as in merge . 
    * minimum weight field. 
    * Also calculate net add_weight from root to the node of interest whenever you remove a link add this value to the add_weight field of the removed subtree . 
    
