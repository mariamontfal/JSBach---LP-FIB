grammar jsbach;
root : func* EOF ;

func: FUNCNAME expr* OPEN 
        bloc CLOSE                     #ExprFunc
        ;

bloc: inst*;

inst: 
    VAR ASS expr                        #ExprAssig
    | CUT VAR OC expr CC                #ExprPop
    | booleanExpr                       #ExprBool
    | whileExpr                         #ExprWhile
    | WRT expr+                         #ExprWrite
    | RD expr                           #ExprRead
    | FUNCNAME expr*                    #ExprFuncInvoke
    | VAR PUSH expr                     #ExprPush
    | PLAY expr                         #ExprPlay
    ;
    

//EXPRESSIO ARITMETICA
expr :
    LEN VAR                             #ExprLenList
    | VAR OC expr CC                    #ExprIndex
    | '(' expr* ')'                     #ExprParentesis
    | '{' expr* '}'                     #ExprList
    | expr (DIV|MUL|MOD) expr           #ExprDivMulMod
    | expr (SUB|ADD) expr               #ExprSubAdd
    | NUM                               #ExprNum
    | BOOL                              #ExprBoolVar
    | VAR                               #ExprVar
    | STR                               #ExprString 
    | NOTA                              #ExprNota
    ;

condition:
    '(' condition* ')'                  #ExprCondParentesis
    | expr (LT | GT | GE | LE) expr     #ExprLessGreater
    | expr (EQ | DIFF) expr             #ExprEqDiff
    | expr                              #ExprConditBool
    ;

//EXPRESSIO BOOLEANA
booleanExpr : 
    IFC condition OPEN inst* CLOSE      #ExprIf
    | IFC condition OPEN inst* CLOSE 
    ELSE OPEN inst* CLOSE               #ExprIfElse
    ;
  
//EXPRESSIO WHILE LOOP
whileExpr:
    (WHILE (condition) OPEN inst* CLOSE )   #ExprLoop
    
    ;

//INDICADOR REPRODUCCIO
PLAY :         '<:>' ;
NOTA : ([A-G][0-8]|[A-G]);

//INDICADOR ESCRIPTURA
WRT :          '<!>' ;

//INDICADOR LECTURA
RD :           '<?>' ;

//CONDICIONAL
IFC:            'if' ;
ELSE:         'else' ;

//OPERADORS LOGICS
EQ :             '=' ;
DIFF :          '/=' ;
LT :            '<'  ;
GT :            '>'  ;
LE :            '<=' ;
GE :            '>=' ;

//ITERACIO
WHILE :      'while' ;

//ASSIGNACIO
ASS :           '<-' ;

//LLISTES
PUSH :          '<<' ;
CUT :           '8<' ;
OC :            '['  ;
CC :            ']'  ;
LEN :           '#'  ;

//ARITMETICA
ADD : '+' ;
SUB : '-' ;
MUL : '*' ;
DIV : '/' ;
MOD : '%' ;

//TIPUS
BOOL : ('true'|'false');
FUNCNAME : [A-ZÀ-Ý]([a-zA-ZÀ-Ýà-ÿ0-9]|'_')*;
VAR : [a-z][a-zA-Z]*; 
STR : '"'~[\t\r\n]+'"'+ ;
FLO : [0-9]+'.'[0-9]*;
NUM : [0-9]+;

//REGIONS
OPEN : '|:';
CLOSE : ':|';

//SKIPS
COMMENT: '//' -> skip;
COMMENTS : '~~~' ~[\t\r\n]* '~~~'-> skip ;     // skip comments
WS : [ \t\r\n]+ -> skip ;                // skip spaces, tabs, newlines
