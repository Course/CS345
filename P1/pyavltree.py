#!/bin/python
from __future__ import print_function
import random, math
import sys
import pdb
def random_data_generator (max_r):
    for i in xrange(max_r):
        yield random.randint(0, max_r)

class Vertex():
    def __init__(self,key):
        self.key = key
        self.inedge = None
        self.outedge = None

    def __repr__(self):
        return str(self.key) + "(" + str(self.inedge)  + "," + str(self.outedge) + ")"

    def get_edge(self):
        if self.outedge is not None:
            return self.outedge
        elif self.inedge is not None:
            return self.inedge
        else:
            return None


class Node():
    def __init__(self, key):
        self.key = key
        self.tail = None
        self.head = None
        self.parent = None
        self.leftChild = None
        self.rightChild = None
        self.minWeight = None
        self.addFactor = 0
        self.revBit = 0
        self.height = 0 

    def reset(self):
        self.tail = None
        self.head = None
        self.parent = None
        self.leftChild = None
        self.rightChild = None
        self.minWeight = None
        self.addFactor = 0
        self.revBit = 0
        self.height = 0 
 
    def __repr__(self):
        return str(self.key) + "(" + str(self.height) + ")"
    
    def is_leaf(self):
        return (self.height == 0)
   
    def max_children_height(self):
        if self.leftChild and self.rightChild:
            return max(self.leftChild.height, self.rightChild.height)
        elif self.leftChild and not self.rightChild:
            return self.leftChild.height
        elif not self.leftChild and  self.rightChild:
            return self.rightChild.height
        else:
            return -1
    def left(self,x):
        if x==0:
            return self.leftChild
        else :
            return self.rightChild

    def right(self,x):
        if x==0:
            return self.rightChild 
        else :
            return self.leftChild

    def is_left_child(self):
        return (self.parent.leftChild == self)

    def is_right_child(self):
        return (self.parent.rightChild == self)

    def is_root(self):
        return (self.parent == None)

    def get_root(self):
        currentNode = self
        while currentNode.parent is not None:
            currentNode = currentNode.parent
        return currentNode

    def balance (self):
        return (self.leftChild.height if self.leftChild else -1) - (self.rightChild.height if self.rightChild else -1)

    def rebalance (self):
        node_to_rebalance = self
        A = node_to_rebalance 
        F = A.parent #allowed to be NULL
        if node_to_rebalance.balance() == -2:
            if node_to_rebalance.rightChild.balance() <= 0:
                """Rebalance, case RRC """
                B = A.rightChild
                C = B.rightChild
                assert (not A is None and not B is None and not C is None)
                A.rightChild = B.leftChild
                if A.rightChild:
                    A.rightChild.parent = A
                B.leftChild = A
                A.parent = B                                                               
                if F is None:                                                              
                   #BUG HERE
                   #self.rootNode = B 
                   #self.rootNode.parent = None                                                   
                   B.parent = None
                else:                                                                        
                   if F.rightChild == A:                                                          
                       F.rightChild = B                                                                  
                   else:                                                                      
                       F.leftChild = B                                                                   
                   B.parent = F 
                recompute_heights (A) 
                recompute_heights (B.parent)                                                                                         
            else:
                """Rebalance, case RLC """
                B = A.rightChild
                C = B.leftChild
                assert (not A is None and not B is None and not C is None)
                B.leftChild = C.rightChild
                if B.leftChild:
                    B.leftChild.parent = B
                A.rightChild = C.leftChild
                if A.rightChild:
                    A.rightChild.parent = A
                C.rightChild = B
                B.parent = C                                                               
                C.leftChild = A
                A.parent = C                                                             
                if F is None:                                                             
                    #self.rootNode = C
                    #self.rootNode.parent = None                                                    
                    C.parent = None
                else:                                                                        
                    if F.rightChild == A:                                                         
                        F.rightChild = C                                                                                     
                    else:                                                                      
                        F.leftChild = C
                    C.parent = F
                recompute_heights (A)
                recompute_heights (B)
        else:
            assert(node_to_rebalance.balance() == +2)
            if node_to_rebalance.leftChild.balance() >= 0:
                B = A.leftChild
                C = B.leftChild
                """Rebalance, case LLC """
                assert (not A is None and not B is None and not C is None)
                A.leftChild = B.rightChild
                if (A.leftChild): 
                    A.leftChild.parent = A
                B.rightChild = A
                A.parent = B
                if F is None:
                    #self.rootNode = B
                    #self.rootNode.parent = None
                    B.parent = None
                else:
                    if F.rightChild == A:
                        F.rightChild = B
                    else:
                        F.leftChild = B
                    B.parent = F
                recompute_heights (A)
                recompute_heights (B.parent) 
            else:
                B = A.leftChild
                C = B.rightChild 
                """Rebalance, case LRC """
                assert (not A is None and not B is None and not C is None)
                A.leftChild = C.rightChild
                if A.leftChild:
                    A.leftChild.parent = A
                B.rightChild = C.leftChild
                if B.rightChild:
                    B.rightChild.parent = B
                C.leftChild = B
                B.parent = C
                C.rightChild = A
                A.parent = C
                if F is None:
                   #self.rootNode = C
                   C.parent = None
                   #self.rootNode.parent = None
                else:
                   if (F.rightChild == A):
                       F.rightChild = C
                   else:
                       F.leftChild = C
                   C.parent = F
                recompute_heights (A)
                recompute_heights (B)
    
    
    def find_biggest(self):
        start_node = self
        xorr = start_node.revBit
        node = start_node
        while node.right(xorr):
            node = node.right(xorr)
            xorr = xor(xorr, node.revBit)
        return (node , xorr)
    
    def find_smallest(self):
        start_node = self
        xorr = start_node.revBit
        node = start_node
        while node.left(xorr):
            node = node.left(xorr)
            xorr = xor(xorr, node.revBit)
        return (node, xorr)
     
    #def inorder_non_recursive (self):
        #node = self
        #retlst = []
        #while node.leftChild:
            #node = node.leftChild
        #while (node):
            #retlst += [node.key]
            #if (node.rightChild):
                #node = node.rightChild
                #while node.leftChild:
                    #node = node.leftChild
            #else:
                #while ((node.parent)  and (node == node.parent.rightChild)):
                    #node = node.parent
                #node = node.parent
        #return retlst
 
    #def preorder(self, node, retlst = None):
        #if retlst is None:
            #retlst = []
        #retlst += [node.key]
        #if node.leftChild:
            #retlst = self.preorder(node.leftChild, retlst) 
        #if node.rightChild:
            #retlst = self.preorder(node.rightChild, retlst)
        #return retlst         
           
    #def inorder(self, node, retlst = None):
        #if retlst is None:
            #retlst = [] 
        #if node.leftChild:
            #retlst = self.inorder(node.leftChild, retlst)
        #retlst += [node.key] 
        #if node.rightChild:
            #retlst = self.inorder(node.rightChild, retlst)
        #return retlst
        
    #def postorder(self, node, retlst = None):
        #if retlst is None:
            #retlst = []
        #if node.leftChild:
            #retlst = self.postorder(node.leftChild, retlst) 
        #if node.rightChild:
            #retlst = self.postorder(node.rightChild, retlst)
        #retlst += [node.key]
        #return retlst  
    
    #def as_list (self, pre_in_post):
        #if not self.rootNode:
            #return []
        #if pre_in_post == 0:
            #return self.preorder (self.rootNode)
        #elif pre_in_post == 1:
            #return self.inorder (self.rootNode)
        #elif pre_in_post == 2:
            #return self.postorder (self.rootNode)
        #elif pre_in_post == 3:
            #return self.inorder_non_recursive()      
    
#BUG HERE
    def find(self, key):
        return self.find_in_subtree (self, key )
    
    def find_in_subtree (self,  node, key):
        if node is None:
            return None  # key not found
        if key < node.key:
            return self.find_in_subtree(node.leftChild, key)
        elif key > node.key:
            return self.find_in_subtree(node.rightChild, key)
        else:  # key is equal to node key
            return node
    
    def remove (self):
            #     There are three cases:
            # 
            #     1) The node is a leaf.  Remove it and return.
            # 
            #     2) The node is a branch (has only 1 child). Make the pointer to this node 
            #        point to the child of this node.
            # 
            #     3) The node has two children. Swap items with the successor
            #        of the node (the smallest item in its right subtree) and
            #        delete the successor from the right subtree of the node.
            if self.is_leaf():
                self.remove_leaf()
            elif (bool(self.leftChild)) ^ (bool(self.rightChild)):  
                self.remove_branch ()
            else:
                #remove this clause
                #self.swap_with_successor_and_remove (node)
                pass
            
    def remove_leaf (self):
        node = self
        parent = node.parent
        if (parent):
            if parent.leftChild == node:
                parent.leftChild = None
            else:
                assert (parent.rightChild == node)
                parent.rightChild = None
            recompute_heights(parent)
        self.reset()
        # rebalance
        node = parent
        while (node):
            if not node.balance() in [-1, 0, 1]:
                node.rebalance()
            node = node.parent
        
        
    def remove_branch (self):
        node = self
        parent = node.parent
        if (parent):
            if parent.leftChild == node:
                parent.leftChild = node.rightChild or node.leftChild
            else:
                assert (parent.rightChild == node)
                parent.rightChild = node.rightChild or node.leftChild
            if node.leftChild:
                node.leftChild.parent = parent
            else:
                assert (node.rightChild)
                node.rightChild.parent = parent 
            recompute_heights(parent)
        #delete node
        self.reset()
        # rebalance
        node = parent
        while (node):
            if not node.balance() in [-1, 0, 1]:
                node.rebalance()
            node = node.parent
        
    # save the tree into a png image
    # filename should be "name.png"
    def toPNG(self, filename):
        from visualize import save_bst
        save_bst(self, filename)

    # use for debug only and only with small trees            
    #def out(self, start_node = None):
        #if start_node == None:
            #start_node = self.rootNode
        #space_symbol = "*"
        #spaces_count = 80
        #out_string = ""
        #initial_spaces_string  = space_symbol * spaces_count + "\n" 
        #if not start_node:
            #return "AVLTree is empty"
        #else:
            #level = [start_node]
            #while (len([i for i in level if (not i is None)])>0):
                #level_string = initial_spaces_string
                #for i in xrange(len(level)):
                    #j = (i+1)* spaces_count / (len(level)+1)
                    #level_string = level_string[:j] + (str(level[i]) if level[i] else space_symbol) + level_string[j+1:]
                #level_next = []
                #for i in level:
                    #level_next += ([i.leftChild, i.rightChild] if i else [None, None])
                #level = level_next
                #out_string += level_string                    
        #return out_string


    def list_ancestors(self):
        currentNode = self
        ancestor_list = []
        while currentNode.parent is not None:
            ancestor_list.append(currentNode.parent)
            currentNode = currentNode.parent
        return ancestor_list

def recompute_heights (start_from_node):
        changed = True
        node = start_from_node
        while node and changed:
            old_height = node.height
            node.height = (node.max_children_height() + 1 if (node.rightChild or node.leftChild) else 0)
            changed = node.height != old_height
            node = node.parent

def inorder(node, xorr = 0, retlst = None):
        if node is None:
            return
        xorr = xor(xorr, node.revBit)
        if xorr == 0:
            if node.leftChild:
                inorder(node.left(xorr), xorr, retlst)
            print (str(node.tail.key) + "---" + str(node.key) + "--->" + str(node.head.key) + "_" , end=" ")
            if node.rightChild:
                inorder(node.right(xorr), xorr, retlst)
        else:
            if node.rightChild:
                inorder(node.rightChild, xorr, retlst)
            print (str(node.head.key) + "---" + str(node.key) + "--->" + str(node.tail.key) + "_" , end=" ")
            if node.leftChild:
                inorder(node.leftChild, xorr, retlst)

def sanity_check (start_node, *args):
        if len(args) == 0:
            node = start_node
        else:
            node = args[0]
        if (node  is None) or (node.is_leaf() and node.parent is None ):
            # trival - no sanity check needed, as either the tree is empty or there is only one node in the tree     
            pass    
        else:
            if node.height != node.max_children_height() + 1:
                raise Exception ("Invalid height for node " + str(node) + ": " + str(node.height) + " instead of " + str(node.max_children_height() + 1) + "!" )
                
            balFactor = node.balance()
            #Test the balance factor
            if not (balFactor >= -1 and balFactor <= 1):
                raise Exception ("Balance factor for node " + str(node) + " is " + str(balFactor) + "!")
            #Make sure we have no circular references
            if not (node.leftChild != node):
                raise Exception ("Circular reference for node " + str(node) + ": node.leftChild is node!")
            if not (node.rightChild != node):
                raise Exception ("Circular reference for node " + str(node) + ": node.rightChild is node!")
            
            if ( node.leftChild ): 
                if not (node.leftChild.parent == node):
                    raise Exception ("Left child of node " + str(node) + " doesn't know who his father is!")
                #if not (node.leftChild.key <=  node.key):
                    #raise Exception ("Key of left child of node " + str(node) + " is greater than key of his parent!")
                sanity_check(node.leftChild)
            
            if ( node.rightChild ): 
                if not (node.rightChild.parent == node):
                    raise Exception ("Right child of node " + str(node) + " doesn't know who his father is!")
                #if not (node.rightChild.key >=  node.key):
                    #raise Exception ("Key of right child of node " + str(node) + " is less than key of his parent!")
                sanity_check(node.rightChild)

# replace a subtree T' in T by another AVLTree of height h+1
# no checks for height is needed?
def replace_sub_tree(old_root, new_root):
    node_to_replace = old_root
    parent = node_to_replace.parent
    if node_to_replace.is_root():
        pass
    elif node_to_replace.is_left_child():
        parent.leftChild = new_root
        new_root.parent = parent
        recompute_heights(parent)
    elif node_to_replace.is_right_child():
        parent.rightChild = new_root
        new_root.parent = parent
        recompute_heights(parent)
    else:
        print ("Cannot reach here")
    old_root.parent = new_root
    recompute_heights(new_root)
    if not new_root.balance() in [-1, 0, 1]:
        new_root.rebalance()
    for node in new_root.list_ancestors():
        if not node.balance () in [-1, 0, 1]:
            node.rebalance()

def merge(root1, root2):
    #pdb.set_trace()
    if root1 is None:
        return root2
    if root2 is None:
        return root1
    taller_tree = root2 if root2.height >= root1.height else root1
    shorter_tree = root2 if taller_tree == root1 else root1
    bigger_tree = root2 
    smaller_tree = root1
    h = shorter_tree.height
    node = taller_tree
    #if node.height == h or node.height == h+1:
    #    pass
    if taller_tree == bigger_tree:
        while (node.height != h and node.height != h+1):
            node = node.leftChild
        xNode = smaller_tree.find_biggest()
        if xNode == smaller_tree:
            smaller_tree = None
        else:
            xNode.remove()
            smaller_root = smaller_tree.get_root() #while rebalancing during removal , root may change
            xNode.leftChild = smaller_root
            smaller_root.parent = xNode
        xNode.rightChild = node
        recompute_heights(xNode)
    else:
        while (node.height != h and node.height != h+1):
            node = node.rightChild
        xNode = bigger_tree.find_smallest()
        if xNode == bigger_tree:
            bigger_tree = None
        else:
            xNode.remove()
            bigger_root = bigger_tree.get_root()
            xNode.rightChild = bigger_root
            bigger_root.parent = xNode
        xNode.leftChild = node
        recompute_heights(xNode)
    xNode.parent = None
    #xNode.height = xNode.max_children_height() + 1
    replace_sub_tree(node, xNode)
    return taller_tree.get_root()
#return root of the merged tree

def special_merge(root1, root2, xNode):
    #pdb.set_trace()
    taller_tree = root2 if root2.height >= root1.height else root1
    shorter_tree = root2 if taller_tree == root1 else root1
    bigger_tree = root2
    smaller_tree = root1
    h = shorter_tree.height
    node = taller_tree
    xorr = 0
    (b1,x1) = smaller_tree.find_biggest()
    (b2,x2) = bigger_tree.find_smallest()
    if x1 == 0:
        xNode.tail = b1.head 
        b1.head.outedge = xNode 
    else:
        xNode.tail = b1.tail
        b1.tail.outedge = xNode
    if x2 == 0:
        xNode.head = b2.tail
        b2.tail.inedge = xNode
    else:
        xNode.head = b2.head
        b2.head.inedge = xNode
    xNode.parent = None
    #if node.height == h or node.height == h+1:
    #    pass
    if taller_tree == bigger_tree:
        while (node.height != h and node.height != h+1):
            xorr = xor(xorr,node.revBit)
            node = node.left(xorr)
        smaller_root = smaller_tree #while rebalancing during removal , root may change
        xNode.leftChild = smaller_root
        smaller_root.parent = xNode
        xNode.rightChild = node
        #recompute_heights(xNode)
    else:
        while (node.height != h and node.height != h+1):
            xorr = xor(xorr,node.revBit)
            node = node.right(xorr)
        bigger_root = bigger_tree
        xNode.rightChild = bigger_root
        bigger_root.parent = xNode
        xNode.leftChild = node
        #recompute_heights(xNode)
    xNode.parent = None
    xNode.revBit = xorr
    node.revBit = (0 if node.revBit == 1 else 0) if xorr == 1 else node.revBit
    #xNode.height = xNode.max_children_height() + 1
    replace_sub_tree(node, xNode)
    #node.parent = xNode

    # dont delete any node

def rbset(node):
    if revBit == 0 :
        return node 
    else: 
        h = node.head 
        t = node.tail 
        node.head = t 
        node.tail = h 
        node.head.inedge = node 
        node.tail.outedge = node 
        node.revBit = 0 
        return node 
def rbinv(node):
    if node.revBit == 1 :
        node.revBit =0 
    else :
        node.revBit =1 

# split :: avl -> node -> (avl,avl)
def split(root,path,node): # splits an avl tree into 2 trees with all elements of 1st < node and all elements of 2nd greater than nodes . O(log n)
    currentNode = root
    #assert(root.find(node.key) == node)
    counter = 0
    xorr  = 0 
    smtree= None
    smmid = None 
    bgtree = None
    bgmid = None 
    for d in path:
        xorr = xor(xorr,currentNode.revBit)
        if xorr == 0:
            if d == 'L':
                if bgtree:
                    bgtree = special_merge(currentNode.rightChild,bgtree,bgmid)
                    bgmid = rbset(currentNode)
                else :
                    bgtree = currentNode.rightChild
                    bgmid = rbset(currentNode)
                currentNode = currentNode.leftChild
            else : 
                if smtree:
                    smtree = special_merge(smtree,currentNode.leftChild,smmid)
                    smmid = rbset(currentNode)
                else :
                    smtree = currentNode.leftChild
                    smmid = rbset(currentNode)
                currentNode = currentNode.rightChild
        else :
            if d == 'L':
                if bgtree:
                    smtree = special_merge(smtree,rbinv(currentNode.rightChild),smmid)
                    smmid = rbset(currentNode)
                else :
                    smtree = rbinv(currentNode.rightChild)
                    smmid = rbset(currentNode)
                currentNode = currentNode.leftChild
            else : 
                if bgtree:
                    bgtree = special_merge(rbinv(currentNode.leftChild),bgtrees,bgmid)
                    bgmid = rbset(currentNode)
                else :
                    bgtree = rbinv(currentNode.leftChild)
                    bgmid = rbset(currentNode)
                currentNode = currentNode.rightChild
    xorr = xor(xorr,currentNode.revBit)
    if xorr == 0:
        bgtree = special_merge(currentNode.rightChild,bgtree,bgmid)
        smtree = special_merge(smtree,currentNode.leftChild,smmid)
    else :
        bgtree = special_merge(rbinv(currentNode.leftChild),bgtrees,bgmid)
        smtree = special_merge(smtree,rbinv(currentNode.rightChild),smmid)

# link 
def link(u,v,w):
    global nodes
    uVertex = nodes[u-1]
    vVertex = nodes[v-1]
    if uVertex == vVertex:
        print ("Cannot link to itself")
    print_path(u)
    print_path(v)
    uEdge = uVertex.get_edge()
    vEdge = vVertex.get_edge()
    if uEdge is None:
        if vEdge is None:
            edge = Node(w)
            edge.tail = uVertex
            edge.head = vVertex
            uVertex.outedge = edge
            vVertex.inedge = edge
        else:
            edge = Node(w)
            vRoot = vEdge.get_root()
            edge.tail = uVertex
            uVertex.outedge = edge
            smallest_edge,x2 = vRoot.find_smallest()
            if x2 == 0:
                edge.head = smallest_edge.tail
                smallest_edge.tail.inedge = edge
                smallest_edge.leftChild = edge
            else:
                edge.revBit = x2
                edge.head = smallest_edge.head
                smallest_edge.head.outedge = edge
                smallest_edge.rightChild = edge
            #assert(smallest_edge.leftChild == None)
            edge.parent = smallest_edge
            recompute_heights(smallest_edge)
            if not smallest_edge.balance() in [-1,0,1]:
                smallest_edge.rebalance()
            for node in smallest_edge.list_ancestors():
                if not node.balance() in [-1,0,1]:
                    node.rebalance()
    else:
        if vEdge is None:
            edge = Node(w)
            uRoot = uEdge.get_root()
            biggest_edge,x1 = uRoot.find_biggest()
            if x1 == 0:
                edge.tail = biggest_edge.head 
                biggest_edge.head.outedge =  edge
                biggest_edge.rightChild = edge
            else:
                edge.revBit = x1
                edge.tail = biggest_edge.tail
                biggest_edge.tail.inedge = edge
                biggest_edge.leftChild = edge
            edge.head = vVertex
            vVertex.inedge = edge
            #assert( biggest_edge.rightChild == None)
            edge.parent = biggest_edge
            recompute_heights(biggest_edge)
            if not biggest_edge.balance() in [-1,0,1]:
                biggest_edge.rebalance()
            for node in biggest_edge.list_ancestors():
                if not node.balance() in [-1,0,1]:
                  node.rebalance()
        else:
            # both uEdge and vEdge are not None
            if uEdge.get_root() == vEdge.get_root():
                print ("Already linked")
            else:
                edge = Node(w)
                uEdge.get_root().toPNG("u.jpeg")
                vEdge.get_root().toPNG("v.jpeg")
                special_merge(uEdge.get_root(),vEdge.get_root(), edge)
                sanity_check(uEdge.get_root())
                uEdge.get_root().toPNG("r.jpeg")
    print_path(u)
    #uNode.get_root().toPNG("u.png")
    #vNode.get_root().toPNG("v.png")
    #print_link(vNode.get_root())
    #vRoot = vNode.get_root()
    #if uRoot == vRoot:
        #pass
    #else:
        #special_merge(uRoot, vRoot)
        #print_link(uNode.get_root())
        ##uNode.get_root().toPNG("r.png")
        #sanity_check(uNode.get_root())

def print_path(u):
    global nodes
    vertex = nodes[u-1]
    edge = vertex.get_edge()
    if edge is None:
        print(str(vertex.key)+"\n")
    else:
        root = edge.get_root()
        inorder(root)
        print("\n")
        #for edge in edge_list:
            #print (str(edge.tail.key) + "---" + str(edge.key) + "--->",end=" ")
        #last_edge = edge_list.pop()
        #print(str(last_edge.head.key)+"\n")

# cut 
def cut(u,v):
    global nodes
    uVertex = nodes[u-1]
    vVertex = nodes[v-1]
    #print_path(uVertex)
    #print_path(vVertex)
    uEdge = uVertex.outedge
    vEdge = vVertex.inedge
    assert(uEdge is not None)
    assert(vEdge is not None)
    if uEdge != vEdge:
        return "No edge between u and v"
    else:
        assert(uEdge.get_root() == vEdge.get_root())
        #sanity_check(vVertex.outedge.get_root())
        #sanity_check(uVertex.inedge.get_root())
        #sanity_check(vVertex.outedge.get_root())
        (rt,path)=give_path(uEdge)
        split(rt,path, uEdge)
        uEdge.tail = None
        uEdge.head = None
        uVertex.outedge = None
        vVertex.inedge = None
        del uEdge
        uVertex.inedge.get_root().toPNG("ufinal.png")
        vVertex.outedge.get_root().toPNG("vfinal.png")
    #print_path(uVertex)
    #print_path(vVertex)




# multiadd 
def multi_add_weight(u,v,d):
    pass

# reverse path 
def reverse_path(u):
    global nodes
    node = nodes[u-1]
    edge = node.get_edge()
    if edge is None:
        return
    while edge.parent is not None:
        edge = edge.parent
    edge.revBit = 1 if edge.revBit == 0 else 0
    print_path(u)


# report_min
def report_min(u,v):
    pass

# is_reachable 
def is_reachable(u,v):
    pass 

# root and path to root 
def give_path(u):
    node = u 
    path = []
    while node.parent is not None :
        temp = node 
        node = node.parent 
        if temp == node.leftChild:
            path.append('L')
        else :
            path.append('R')
    return (node, reversed(path))

    return (node,path)
def xor(a,b):
    assert((a==0 or a==1) and (b==0 or b==1))
    if a==1 and b==1:
        return 0 
    elif a==1 and b==0:
        return 1 
    elif a==0 and b==1:
        return 1 
    else :
        return 0 

nodes = []

if True:
#if __name__ == "__main__":
    f = open("testcases.txt",'r')
    noofnodes = int(f.readline())
    for i in range(noofnodes):
        nodes.append(Vertex(i+1))
    for t,lines  in enumerate(f):
        pdb.set_trace()
        l = lines.split(' ')
        print ("Line no : " + str(t) + "\n")
        fn = l[0]
        arg = [int(i) for i in l[1:]]
        if fn=='L':
            link(arg[0],arg[1],arg[2])
        elif fn=='C':
            cut(arg[0],arg[1])
        elif fn=='A':
            multi_add_weight(arg[0],arg[1],arg[2])
        elif fn=='R':
            reverse_path(arg[0])
        elif fn=='M':
            report_min(arg[0],arg[1])
        elif fn=='I':
            is_reachable(arg[0],arg[1])
        else:
            print ("Unrecognised input")
            break

