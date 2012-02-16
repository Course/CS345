import random,sys,time

def random_data_generator (max_r):
    for i in range(max_r):
        yield random.randint(0, max_r)

def random_select(l,p):
    t = [] 
    for i,v in enumerate(l):
        t=t+[v]*int(p[i]*100)
    return random.choice(t)
def findEnd(d,key):
    while(key in d):
        key=d[key]
    return key 
# given a dict and a key u which is a node finds randomly a node v such that there is a path from u to v 
def choosePath(d,key):
    l = []
    while key in d:
        key=d[key]
        l.append(key)
    return random.choice(l)

def path(d,key):
    l = []
    while key in d:
        l.append(key)
        key=d[key]
    return l

def revPath(din,dout,key):
    l = []
    key=findEnd(dout,key)
    while key in din:
        l.append(key)
        oldkey=key
        key=din[key]
        din.pop(oldkey)
        dout.pop(key)
    l.append(key)
    for m,n in zip(l,l[1:]):
        dout[m]=n
        din[n]=m

if __name__ == "__main__":
    operations = ['L','C','A','R','M','I']
    probability = [0.7,0,0,0.3,0,0] ## Respective probabilities with which to choose these 
    tnum = 100                              ## Number of nodes 
    maxweight = 1000                            ## Max weight to be used in link 
    maxd = 20                                   ## Argument of multiadd
    testcases = 100                          ## Can be less than this number due to continue skips 
    testfile = 'testcases.txt'                  ## Test case stored here 
    edgein = {}
    edgeout = {}
    f = open(testfile,'w')
    f.write(str(tnum)+"\n")
    for i in range(testcases):    
        #assert(set(edgein.keys())==set(edgeout.values()))
        #assert(set(edgeout.keys())==set(edgein.values()))
        #assert(None not in edgein and None not in edgeout)
        op=random_select(operations,probability)
        d = random.randint(-maxd,maxd)
        if i%1000==0:
            print("Generating test",i," with "+op)
        if op=='L':
            node1 = random.randint(1,tnum-1)
            node2 = random.randint(1,tnum-1)
            if node1 == node2 or findEnd(edgein,node1)==findEnd(edgein,node2): 
                continue
            weight = random.randint(0,maxweight-1)
            t1=findEnd(edgein,node1)
            temp1=findEnd(edgein,node2)
            if t1==temp1 :
                continue
            t2=findEnd(edgeout,node2)
            edgein[t1]=t2
            edgeout[t2]=t1
            f.write("L "+str(node1) + " " +str(node2) + " " + str(weight)+"\n")
        elif op=='C':
            if edgein=={}:
                continue
            node1=random.choice(list(edgein.keys()))
            node2=edgein[node1]
            edgein.pop(node1)
            edgeout.pop(node2)
            f.write("C "+str(node1) + " " +str(node2)+"\n")
        elif op=='A':
            if edgein=={}:
                continue
            node1=random.choice(list(edgein.keys()))
            node2 = choosePath(edgein,node1)
            d = random.randint(-maxd,maxd)
            f.write("M "+str(node1) + " " +str(node2) + " " + str(d)+"\n")
        elif op=='R':
            pass
            if edgein=={}:
                continue
            node1=random.choice(list(edgein.keys()))
            revPath(edgein,edgeout,node1)
            f.write("R "+str(node1)+"\n")
        elif op=='M':
            if edgein=={}:
                continue
            node1=random.choice(list(edgein.keys()))
            node2 = choosePath(edgein,node1)
            f.write("M "+str(node1) + " " +str(node2)+"\n")
        else :
            node1 = random.randint(1,tnum)
            node2 = random.randint(1,tnum)
            f.write("I "+str(node1) + " " +str(node2)+"\n")
