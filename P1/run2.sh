rm -f li.txt avl.txt
python list.py < testcases.txt > li.txt
python pyavltree.py > avl.txt
diff avl.txt li.txt
