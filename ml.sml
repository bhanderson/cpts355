fun in_list (x, []) = false
  | in_list (x, (y::ys)) = if x = y then true else in_list (x, ys);

fun intersection ([],[]) = []
  | intersection (x,[]) = []
  | intersection ([],x) = []
  | intersection ((x::xs),(z)) = if in_list (x,xs) then intersection (xs,z)
                                else if in_list (x,z) then x::intersection
                                (xs,z) else intersection (xs,z);

fun union ([], []) = []
  | union (l, []) = l
  | union ([], l) = l
  | union (a::b, c) = if in_list (a, c) then union (b,c)
                      else union(b,a::c);

fun filter f L = let
  fun filter2 [] A = (rev A)
    | filter2 (x::xs) A = if f x then filter2 xs ((x)::A) else filter2 xs A
in
  filter2 L []
end;

fun insert x [] = [[x]]
  | insert x (y::ys) = let
    fun consy l = y :: l
in (x::y::ys) :: (map consy (insert x ys))
end;

fun perms [] = [[]]
  | perms (x::y) = List.concat (map (insert x) (perms y));

datatype either = ImAString of string | ImAnInt of int;

datatype eitherTree = LEAF of either | NODE of (eitherTree * eitherTree);

fun eitherSearch (LEAF(ImAnInt x)) y = (x=y)
  | eitherSearch(LEAF(ImAString x)) y = false
  | eitherSearch (NODE (t1,t2)) y = (eitherSearch t1 y)
  orelse (eitherSearch t2 y);

fun eitherTest () =
let
  val L1 = LEAF(ImAnInt 1)
  val L2 = LEAF(ImAnInt 2)
  val L3 = LEAF(ImAnInt 13)
  val L4 = LEAF(ImAnInt 14)
  val L5 = LEAF(ImAnInt 15)
  val L6 = LEAF(ImAString "a")
  val L7 = LEAF(ImAString "b")
  val L8 = LEAF(ImAString "c")
  val L9 = LEAF(ImAString "d")
  val L10 = LEAF(ImAString "e")
  val N1 = NODE (L1,L2)
  val N2 = NODE (N1, L3)
  val N3 = NODE (N2, L4)
  val N4 = NODE (N3, L5)
  val N5 = NODE (N4, L6)
  val N6 = NODE (N5, L7)
  val N7 = NODE (N6, L8)
  val N8 = NODE (N7, L9)
  val N9 = NODE (N8, L10)

                       in
                         not  (eitherSearch N9 15)
                       end;


datatype 'a Tree = Empty | LEAF of 'a | NODE of ('a Tree) list;

val L1a = LEAF "a"
val L1b = LEAF "b"
val L1c = LEAF "c"
val L2a = NODE [L1a, L1b, L1c]
val L2b = NODE [L1b, L1c, L1a]
val L3 = NODE [L2a, L2b, L1a, L1b]
val L4 = NODE [L1c, L1b, L3]
val L5 = NODE [L4]
val iL1a = LEAF 1
val iL1b = LEAF 2
val iL1c = LEAF 3
val iL2a = NODE [iL1a, iL1b, iL1c]
val iL2b = NODE [iL1b, iL1c, iL1a]
val iL3 = NODE [iL2a, iL2b, iL1a, iL1b]
val iL4 = NODE [iL1c, iL1b, iL3]
val iL5 = NODE [iL4]

fun treeToString f Node =
let
  fun treeToString2 (Empty) = [""]
    | treeToString2 (NODE([])) = [")"]
    | treeToString2 (LEAF(v)) = [f v]
    | treeToString2 (NODE(x)) = ["("] @ List.concat (map treeToString2 x) @ [")"]
in
  String.concat(treeToString2 Node)
end;

