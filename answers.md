# CMPS 2200 Assignment 5
## Answers

**Name:**_________________________

Place all written answers from `assignment-05.md` here for easier grading.


**1: Fixed-Length vs. Variable-Length Codes**

- **1d. (5 pts)** What trend do you see?
alice29.txt , Fixed: 1039367 , Huffman: 676374. Raio: 0.6508 
asyoulik.txt , Fixed: 876253 , Huffman: 606448. Raio: 0.6921 
f1.txt , Fixed: 1340 , Huffman: 826. Raio: 0.6164 
fields.c , Fixed: 78050 , Huffman: 56206. Raio: 0.7201 
grammar.lsp , Fixed: 26047 , Huffman: 17356. Raio: 0.6663 

We can see that for all of them, Huffman reduces file size. These ratios are between 62% to 72% , so Huffman coding shaves off about 28% to 38% of the file size. 

- **1e. (4 pts)** What is the expected
  cost of a Huffman encoding for the document? Is it consistent across
  documents?

  If every character has the same frequency, Huffman coding fails to compress the file size. 
  This is because Huffman's algorithm will merge pairs of nodes evenly, creating a balanced tree. Every character ends up about the same depth/level so it recieves a binary code of log_2 of the alphabet size. So the total expected cost for a document of length n ith alpgabet size k is n*log_2(k) which is the same as a fixed_length ecoding. 
  Total bit cost is not consistent across different documents because it depends on the lengths of the document and size of the alphabet. 


**2: Making Change**

- **2a. (5 pts)** Given a $N$ dollars, state a greedy algorithm for producing
as few coins as possible that sum to $N$.

If the coins are denominated 2^0 , 2^1, 2^2, all the way to 2^k, then 2^k is the largest pissible value a single coin can take. To produce the sum to N, we should start with 2^k and go down. That is, start with 2^k, is N is greater than 2^k then pick that coin and subtract 2^k from N. If 2^k is greater than N, then try comparing with 2^k-1 and so on. 

Essentially, the algorithm would go like this:
Loop from largest to smallest denomination, iterate from i=k down to i =0. While the current coin value 2^i is less than or equal to the remaining amount, add the coin to the collection and subtract 2^i from the remaining amount. Finish once the remaining amount reaches 0. 


- **2b. (5 pts)** Prove that this algorithm is optimal by proving the greedy
  choice and optimal substructure properties.

Greedy choice:
Suppose an optimal solution N does not use the largest valid coin 2^i<=N, instead it uses smaller ones. Since every coin denomination is a power of 2, they all divide 2^i evenly. Additionally if you added 2^0 all the way to 2^(i-1) = 2^(i)-1 so its always less than 2^i. So to reach N>= 2^i , th eoptimal solution musr contain a subset of at least 2 smaller coins that add up to 2^i. If we swap these 2 smaller coins with the one with value 2^i, we would sill reach N, and we would have fewer coins so it contradicts the assumption that the original solution was optimal. 

Optimal substructure: 
Suppose we have an optimal solution, that uses m coins to add to N, and one of the coins is c=2^i. if we remove c, then we have m-1 coins that add up to N-c. So the m-1 coins must be the fewest coins needed to make N-c. If there was a way to add up to N-c using fewer than m-1 coins, we could use this result and add c back to make N which would make N with fewer than m coins which contradicts the assumtion that the original solution was optimal.



- **2c. (4 pts)** What is the work and span of your algorithm?
Since this is a while loop subtracting 2^i each time, then all coins smaller than 2^k appear at most once each so O(k) steps
If N ia a lot bigger than the biggest coin for example N = 1000 and 2^3 is the biggest coin then I would subtract 8 one time at a time, so N/2^k separate subtractions so O(N/2^k +k) . This could be simplified if we did divisions and look at mod. 
Span would also be O(N/2^k +k) becaus esubtracting each time is sequential. 

- **3a. 
Let MED(S,T) be the minimum number of unit cost edits like insertions deletions and substitiutions needed to transform S to T. 
Base case:
 if S is empty we must insert all character of T . MED("", T) = |T|
if T is empty, we must delete all characters of s so Med(S, "") = |S|
 Recusrsive: 
 Maching first char. No edit is needed so optimal edit distance is the rest. MED(S[1:], T[1:])
 Not matching first. WE can either insert or delete or substitute.
 Insertion: Insert T[0] before S[0] orint 1+ MED(S, T[1:])
 Deletion: Delete S[0] costing 1+ MED(S[1:]T)
Substitution: Replace S[0] with T[0] costing 1 + MED(S[1:], T[1:])
so when the first element doesnt match: MED(S, T) = 1 + min(MED(S, T[1:]), MED(S[1:], T), MED(S[1:], T[1:])).
