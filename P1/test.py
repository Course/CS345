from pyavltree import *
import pdb

seq0 = [x for x in range(0,10)]
seq1 = [x for x in range(15,20)]
seq2 = [x for x in range(30,50)]
seq3 = [x for x in range(60,1000)]

seq4 = [1]
seq5 = [2]

b = AVLTree(seq0)
c = AVLTree(seq1)
d = AVLTree(seq2)
e = AVLTree(seq3)

x = AVLTree(seq4)
y = AVLTree(seq5)

#f = d.special_merge(b)
#f.toPNG("f.png")

