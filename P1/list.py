#!/bin/python 
import sys 

# Linked list implementation of dynamic paths 
class Node():
    def __init__(self,key):
        self.key = key 
        self.parent = None 
        self.next = None
        self.nextweight = 0 
    def __str__(self):
        return str(self.key)
    def __repr__(self):
        return str(self.key)

# Link O(n)
def link(u,v,w):
    tail = u 
    head = v 
    while(tail.next != None):
        tail = tail.next 
    while(head.parent != None):
        head = head.parent 
    tail.next = head 
    tail.nextweight = w 
    head.parent = tail 

# Cut O(1)
def cut(u,v):
    u.next = None 
    v.parent = None 
    u.nextweight = 0 

# multiadd O(n)

def multi_add_weight(u,v,d):
    pointer = u 
    while(pointer!=v):
        pointer.nextweight = pointer.nextweight + d
        pointer = pointer.next 

# reverse_path O(n)

def reverse_path(u):
    head = findRoot(u) 
    tail = head.next 
    if tail == None:
        return 
    head.next=None
    temp = tail.next 
    tempweight2 = head.nextweight
    while(tail != None):
        temp = tail.next 
        tail.next=head 
        tempweight1 = tail.nextweight
        tail.nextweight= tempweight2
        tempweight2 = tempweight1
        head.parent = tail 
        head = tail
        tail = temp 
    head.parent = None


# is_reachable O(n)

def is_reachable(u,v):
    head = u 
    tail = v
    while(head != None):
        if head == tail :
            print("1")
            return 
        head = head.next
    print("0")

# report_min O(n)
def report_min(u,v):
    head = u 
    tail = v 
    if u==v :
        print ("Error: report_min . Same node entered")
    minim = u.nextweight
    while(head.next != tail):
        head = head.next 
        minim = min(minim,head.nextweight)
    print(minim)

# Helpers 
def findRoot(node):
    head = node
    while(head.parent != None):
        head = head.parent 
    return head 

# print all the paths 
def print_path(avl):
    check = [1 for i in avl]
    print("################# PATHS #################")
    for i in avl :
        node = findRoot(i)
        if  check[node.key] == 1 :
            check[node.key]=0
            print(node.key+1,end=" ")
            while(node.next != None):
                print("--- " + str(node.nextweight) + " --->",end=" ")
                print(node.next.key+1,end=" ")
                check[node.next.key]=0
                node = node.next
            print()
        
    print("#########################################")

if __name__ == "__main__":    
    nodes = int(input())
    avl=[]
    for i in range(nodes):
        avl.append(Node(i))
    print_path(avl)
    for lines in sys.stdin :
        l = lines.split(' ')
        fn = l[0]
        arg = [int(i) for i in l[1:]]
        if fn=='L':
            link(avl[arg[0]-1],avl[arg[1]-1],arg[2])
        elif fn=='C':
            cut(avl[arg[0]-1],avl[arg[1]-1])
        elif fn=='A':
            multi_add_weight(avl[arg[0]-1],avl[arg[1]-1],arg[2])
        elif fn=='R':
            reverse_path(avl[arg[0]-1])
        elif fn=='M':
            report_min(avl[arg[0]-1],avl[arg[1]-1])
        elif fn=='I':
            is_reachable(avl[arg[0]-1],avl[arg[1]-1])
        else:
            print ("Unrecognised input")
            break
        print_path(avl)

