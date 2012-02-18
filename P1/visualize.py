def bst_to_dot(tree, stream,
               get_key=lambda node: (str(node.key)+ "," + str(node.revBit) + "," + str(node.minWeight)+"," + str(node.addFactor) +",#"+str(node.head)+","+str(node.tail)),
               get_left=lambda node: node.leftChild,
               get_right=lambda node: node.rightChild,
               nodestyle='fontname="Arial"'):
    """Prints a GraphViz .dot file of tree to stream.
       get_left(node) and get_right(node) should return the appropriate
       child of node, or None if there is no such child.
       get_key(node) should return a str()-able object to use as both the
       node name and its displayed value (FIXME: this is not a great idea).
    """
    def escape(text):
        return '"%s"' % text  # TODO: escaping

    nullcount = [0]
    def null_to_dot(key):
        print >>stream, "    null%d [shape=point];" % nullcount[0]
        print >>stream, "    %s -> null%d;" % (escape(key), nullcount[0])
        nullcount[0] += 1

    def node_to_dot(node):
        if get_left(node) is not None:
            print >>stream, "    %s -> %s;" % (
                escape(get_key(node)), escape(get_key(get_left(node))))
            node_to_dot(get_left(node))
        else:
            null_to_dot(get_key(node))
        if get_right(node) is not None:
            print >>stream, "    %s -> %s;" % (
                escape(get_key(node)), escape(get_key(get_right(node))))
            node_to_dot(get_right(node))
        else:
            null_to_dot(get_key(node))

    print >>stream, "digraph BST {"
    print >>stream, "    node [%s];" % nodestyle
    if tree is None:
        print >>stream
    elif get_right(tree) is None and get_left(tree) is None:
        print >>stream, "    %s;" % escape(get_key(tree))
    else:
        node_to_dot(tree)
    print >>stream, "}"

def bst_to_dot_string(tree, *args, **kwargs):
    import StringIO
    stream = StringIO.StringIO()
    bst_to_dot(tree, stream, *args, **kwargs)
    return stream.getvalue()

def save_bst(tree, filename, *args, **kwargs):
    'Saves a PNG of tree to filename by executing "dot -Tpng -o<filename>".'
    import subprocess
    p = subprocess.Popen(["dot", "-Tpng", "-o"+filename],
                         stdin=subprocess.PIPE)
    p.stdin.write(bst_to_dot_string(tree, *args, **kwargs))
    p.stdin.close()
    if p.wait() != 0:
        raise RuntimeError('Unexpected return code: %d' % p.returncode)

def test():
    import sys
    class Node(object):
        def __init__(self, key, left=None, right=None):
            self.key, self.left, self.right = key, left, right
    tree = Node(15, Node(6), Node(18, Node(17)))
    try:
        filename = sys.argv[1]
    except IndexError:
        sys.exit('usage: %s FILENAME\n' % sys.argv[0] +
                 'Test this code - save a test PNG to FILENAME')
    save_bst(tree, filename)

if __name__=='__main__':
    test()
