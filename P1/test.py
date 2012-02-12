from pyavltree import *
import pdb

seq0 = [x for x in range(0,10)]
seq1 = [x for x in range(15,20)]
seq2 = [x for x in range(30,50)]
seq3 = [x for x in range(60,1000)]

seq4 = [1]
seq5 = [2]

n = 25
#b = AVLTree(seq0)
#c = AVLTree(seq1)
#d = AVLTree(seq2)
#e = AVLTree(seq3)

#x = AVLTree(seq4)
#y = AVLTree(seq5)
for i in range(n):
    nodes.append(Vertex(i+1))

for i in range(20):
    a = random.randint(1,n)
    b = random.randint(1,n)
    c = random.randint(1,n)
    print "link("+str(a)+", "+str(b)+", "+str(i)+")\n"
    link(a, b, i)
#f = d.special_merge(b)
#f.toPNG("f.png")

