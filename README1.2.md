### Macinton C 1.2 and it's dialect Macinton C Macro have been released!

**New:**

1. Macroses:

1.1. Adding macros: `! : name : value :`

1.2. Remove macros: `~name`


2. New Pointers:

2.1. `->name` - set function `name`

2.2. `<-` - close function


3. Compiler arguments:

3.1. --help - shows info about current version

3.2. rm - removes out.c after compilation


**Fixed:**

1. Parsing strings

2. Including same C library from init


### BONUS

Macinton C dialect "Macinton C Macro" has been realesd. It was made to learn new programmers qmacros programming. It's good small language based on Macinton C. All arguments are in Macroses. Syntax from Macinton C can be used in Macinton C Macro code

**Macroses:**
1. mode - variable type
2. name - variable name
3. include - variable value
4. condition - condition for IF, IFEL, FOR, WHILE
5. macros - macros name
6. macros_include - macros value
7. argument - argument for functions

**Functions(THEIR ARGUMENTS ARE DEFINED IN MACROSES):**
1. echo - printing text
2. OUT - exit
3. set - set variable
4. IF - if statement
5. ELSE - else statement
6. IFEL - else if statement
7. FI - closing logic trees(also can be used as `}`)
8. FOR - for cycle
9. WHILE - while cycle
10. change - defining macros
11. remove - removing macros

**Example(printing number from 0 to 10):**

`~argument`

`~condition`

`! : condition : int i = 0; i < 10; ++i :`

`! : argument : "%d\n", i :`

`#FOR;`

`#echo;`

`~argument`

`#FI;`

`! : argument : "%d", 10 :`

`#echo;`
