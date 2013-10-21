["a", "b"] list
(2, "a") tuples
datatype 'a Option = NONE | SOME of 'a
when we dont know type its 'a option otherwise its whatever type it is

function to find last element of a list
fun last [] = NONE
  | last [x] = SOME x
  | last (x::y) = last y;

function to find first element of a list
fun first [] = NONE
  | first (x::y) = SOME x;

function to find nth element of a list
fun nth (n, []) = NONE
  | nth (0, (x::y)) = SOME x
  | nth (n, (x::y)) = nth (n-1, y);
a better way to do it
fun nth (_, []) = NONE
  | nth (0, (x::_)) = SOME x
  | nth (n, (_::y)) = nth (n-1, y);

_ a variable we dont need a name for

Tail recursion:
	The answer to a given call of a function is the same as the answer to the
	recursive that it makes
Not tail recursion:
	fun fact 0 = 1
	  | fact n = n * (fact(n-1));

Tail recursion:
	fun factHelper 0 a = a
	  | factHelper n a = factHelper (n-1) (n*a);
	fun fact n = factHelper n 1

fun revAppend ([], l) = l
  | revAppend (h::t, l) = revAppend (t, h::l);

fun reverse l = revAppend ( l, []);

fun map f [] = []
  | map f (x::y) = (f x) :: (map f y);

datatype IntList = Empty | Cons of (int * IntList);

