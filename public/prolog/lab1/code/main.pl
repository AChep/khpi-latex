and(A,B) :- A,B.
or(A,B) :- A;B.
nand(A,B) :- not(and(A,B)).
xor(A,B) :- or(A,B), nand(A,B).
