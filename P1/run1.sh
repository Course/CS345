rm -f li.txt avl.txt testcases.txt
python generateTests.py
python list.py < testcases.txt > li.txt
python pyavltree.py > avl.txt
diff li.txt avl.txt
