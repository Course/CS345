rm -f li.txt avl.txt
python list.py $1> li.txt
python pyavltree.py $1 > avl.txt
diff avl.txt li.txt
