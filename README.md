# logic_puzzle_solve
Solves classic grid logic puzzles like those found at http://www.logic-puzzles.org/

This presented some input challenges, and required me to devise a system to succinctly 
define the parameters and clues in a logic puzzle.  It would be grandiose to call this a 
DSL, but that's the direction I ended up going in.

Here's a small example:

<p align="center"><img width=100% src="https://raw.githubusercontent.com/steve-loomis/logic_puzzle_solve/master/logic%20ex2.png"></p>

and here's how you enter that into the solver:

```shell
3x4
2006,2007,2008,2009
Anita,Chester,Elsie,Fernando
bulldog,dalmatian,maltese,pekingese
STOP
Anita-2=Chester
bulldog-1=maltese
(pekingese)in(2009,Elsie)
(2009,2007)in(Fernando,pekingese)
STOP
```

This first defines the size of the puzzle, 3 categories (years, owners, breeds) by 4 
values per category.

```shell
3x4
```

Then it defines all of the values for those three categories, terminated by STOP.  
Quantitative categories come first.

```shell
2006,2007,2008,2009
Anita,Chester,Elsie,Fernando
bulldog,dalmatian,maltese,pekingese
STOP
```

And finally, it defines the clues, again terminated by STOP

```shell
Anita-2=Chester
bulldog-1=maltese
(pekingese)in(2009,Elsie)
(2009,2007)in(Fernando,pekingese)
STOP
```

For ease of entry and ease of reading output, you can abbreviate values if you want.  
Here's the same puzzle definition with abbreviated values:

```shell
3x4
2006,2007,2008,2009
A,C,E,F
b,d,m,p
STOP
A-2=C
b-1=m
(p)in(2009,E)
(2009,2007)in(F,p)
STOP
```

Here's another puzzle:

<p align="center"><img width=100% src="https://raw.githubusercontent.com/steve-loomis/logic_puzzle_solve/master/logic%20ex1.png"></p>


with its definition:

```shell
3x4
1100,1225,1350,1475
c,d,e,f
975,1250,1600,1850
STOP
e+125=1600
(1475)in(1850,f)
(d)in(1350,1475)
f-125=1250
(1250,1100)in(c,e)
STOP
```

Here's a more difficult puzzle which features all clue types.

<p align="center"><img width=100% src="https://raw.githubusercontent.com/steve-loomis/logic_puzzle_solve/master/logic%20ex3.png"></p>


```shell
4x7
30,35,40,45,50,55,60
H,J,K,L,M,N,S
cc,h,od,p,pr,pc,s
AH,DP,ES,FF,KV,MD,PV
STOP
(45)in(AH,DP)
H<>DP
(L,KV)in(35,h)
PV-5=p
45<>s
(60,N)in(DP,s)
MD>p
s<>FF<>J<>S<>H<>K<>PV
(DP)in(pc,pr)
FF-15=pc
S-10=J
(L,S)in(40,pc)
cc-15=L
STOP
```

To try any of these puzzles on your own, simply type at the command line:

```shell
python logic_puzzle_solve.py
```
and then enter the definitions above at the prompts.  Or find a new puzzle at the link above, and enter your own definition at the prompts.
