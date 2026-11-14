import math, queue
from collections import Counter

####### Problem 1 #######

class TreeNode(object):
    # we assume data is a tuple (frequency, character)
    def __init__(self, left=None, right=None, data=None):
        self.left = left
        self.right = right
        self.data = data
    def __lt__(self, other):
        return(self.data < other.data)
    def children(self):
        return((self.left, self.right))
    
def get_frequencies(fname):
    f=open(fname, 'r')
    C = Counter()
    for l in f.readlines():
        C.update(Counter(l))
    return C

# given a dictionary f mapping characters to frequencies, 
# create a prefix code tree using Huffman's algorithm
def make_huffman_tree(f):
    p = queue.PriorityQueue()
    # construct heap from frequencies, the initial items should be
    # the leaves of the final tree
    for c in f.keys():
        p.put(TreeNode(None,None,(f[c], c)))

    # greedily remove the two nodes x and y with lowest frequency,
    # create a new node z with x and y as children,
    # insert z into the priority queue (using an empty character "")
    while (p.qsize() > 1):
        # TODO
        x = p.get()
        y = p.get()
        z = TreeNode(x, y, (x.data[0] + y.data[0], ""))
        p.put(z)
       
        pass
        
    # return root of the tree
    return p.get()

# Perform a traversal on the prefix code tree to collect all encodings.
# Recursively call get_code, appending 0 or 1 to prefix as appropriate
# depending on if the call is to the left or right child.
# When a leaf is found, update the code dict object to map from
# the value in the leaf to the encoding specified by prefix.
# Return the code object.
def get_code(node, prefix="", code={}):
    # TODO - perform a tree traversal and collect encodings for leaves in code
    if prefix == "":
        code = {}
    if node is None:
        return code
    if node.left is None and node.right is None:
        code[node.data[1]] = prefix
    else:
        if node.left is not None:
            get_code(node.left, prefix + "0", code)
        if node.right is not None:
            get_code(node.right, prefix + "1", code)
    return code
    

# Given an alphabet and frequencies, compute the cost of a fixed length encoding.
# You'll have to consider the total number of unique elements in f to 
# determine the number of bits needed to represent each character.
def fixed_length_cost(f):
    # TODO
    if len(f) ==0:
        return 0
    bits_per_char = max(1, math.ceil(math.log2(len(f))))
    total_chars = sum(f.values())
    return bits_per_char * total_chars


# given a Huffman encoding and character frequencies, compute cost of a Huffman encoding
def huffman_cost(C, f):
    # TODO
    total_cost =0
    for c in f:
        total_cost += len(C[c]) * f[c]
    return total_cost
    pass

def analyze_files():
    for fname in ['alice29.txt', 'asyoulik.txt', 'f1.txt', 'fields.c', 'grammar.lsp']:
        f = get_frequencies(fname)
        fixed = fixed_length_cost(f)
       # print("Fixed-length cost:  %d" % fixed_length_cost(f))

        T = make_huffman_tree(f)
        C = get_code(T)
        huff = huffman_cost(C, f)
       # print("Huffman cost:  %d" % huffman_cost(C, f))

        print(f"{fname} , Fixed: {fixed} , Huffman: {huff}. Raio: {huff/fixed:.4f} ")


####### Problem 4 #######

test_cases = [('book', 'back'), ('kookaburra', 'kookybird'), ('relevant', 'elephant')]
alignments = [('book', 'back'), ('kookaburra', 'kookybird-'), ('relev-ant','-elephant')]

def MED(S, T):
    # TODO - modify to account for insertions, deletions and substitutions
    if (S == ""):
        return(len(T))
    elif (T == ""):
        return(len(S))
    else:
        if (S[0] == T[0]):
            return(MED(S[1:], T[1:]))
        else:
            return(1 + min(MED(S, T[1:]), MED(S[1:], T), MED(S[1:], T[1:])))# include sub


def fast_MED(S, T):
    # TODO -  implement bottom-up memoization
    # returns only the edit distance cost
    m = len(S)
    n = len(T)
    table = [[0] * (n+1) for _ in range(m+1)]

    #base case
    for i in range(m+1):
        table[i][0] =i 
    for j in range(n+1):
        table[0][j] = j

    #fill the table
    for i in range(1, m+1):
        for j in range(1, n+1):
            if S[i-1] == T[j-1]:
                table[i][j] = table[i-1][j-1]
            else:
                table[i][j] = 1+min(
                    table[i-1][j],
                    table[i][j-1],
                    table[i-1][j-1]
                )
    return table[m][n]
    pass

def fast_align_MED(S, T):
    # TODO - implement bottom-up memoization, allowing
    # for traceback of alignment
    # returns the two alignments (see test_align)
    m = len(S)
    n = len(T)
    table = [[0] * (n+1) for _ in range(m+1)]

    #base case
    for i in range(m+1):
        table[i][0] =i 
    for j in range(n+1):
        table[0][j] = j

    #fill the table
    for i in range(1, m+1):
        for j in range(1, n+1):
            if S[i-1] == T[j-1]:
                table[i][j] = table[i-1][j-1]
            else:
                table[i][j] = 1+min(
                    table[i-1][j],
                    table[i][j-1],
                    table[i-1][j-1]
                )
    align_S = []
    align_T = []
    i, j = m, n
    
    while i > 0 or j > 0:
        if i > 0 and j > 0 and S[i - 1] == T[j - 1]:
            align_S.append(S[i - 1])
            align_T.append(T[j - 1])
            i -= 1
            j -= 1
        elif j > 0 and table[i][j] == table[i][j - 1] + 1:
            align_S.append('-')
            align_T.append(T[j - 1])
            j -= 1
        elif i > 0 and table[i][j] == table[i - 1][j] + 1:
            align_S.append(S[i - 1])
            align_T.append('-')
            i -= 1
        else:
            align_S.append(S[i - 1])
            align_T.append(T[j - 1])
            i -= 1
            j -= 1
            
    #reverse the characters since we traced from end to start
    return ''.join(reversed(align_S)), ''.join(reversed(align_T))
    