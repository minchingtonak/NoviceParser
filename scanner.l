    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>
    #include "y.tab.h"
    void yyerror(char *);

EXTERN      extern
VOID        void
RETURN      return
CHAR        char
INT         int
IF          if
ELSE        else
WHILE       while
FOR         for

ID	        [[:alpha:]][[:alpha:][:digit:]_]*

INTCON	    [[:digit:]]+

CHARCON	    '[[:print:]]{-}['\\]'|'\\n'|'\\0'

STRINGCON	\"[[:print:]]{-}[\n\"]*\"

EQUAL        ==
NOTEQUAL     !=
LESSEQUAL    <=
LESSTHAN     \<
GREATEREQUAL \>=
GREATERTHAN  \>
AND          &&
OR           \|\|

%start commentmid commentend

%option nounput
%option noinput
%option yylineno

%%

<INITIAL>"/*"      { BEGIN(commentmid); }
<commentmid>"*"    { BEGIN(commentend); }
<commentmid>[^*]+  { ; }
<commentmid><<EOF>>  { yyerror("EOF inside comment!"); }
<commentend>"*"    { ; }
<commentend><<EOF>>  { yyerror("EOF inside comment!"); }
<commentend>"/"    { BEGIN(INITIAL); }
<commentend>[^*/]+ { BEGIN(commentmid); }

{VOID}          { return VOID; }
{INT}           { return INT; }
{FOR}           { return FOR; }

"="             { return '='; }
";"             { return ';'; }
","             { return ','; }
"("             { return '('; }
")"             { return ')'; }
"{"             { return '{'; }
"}"             { return '}'; }
"["             { return '['; }
"]"             { return ']'; }

"!"             { return '!'; }
"+"             { return '+'; }
"-"             { return '-'; }
"*"             { return '*'; }
"/"             { return '/'; }

\"              { return '"'; }

{EQUAL}         { return EQUAL; }
{NOTEQUAL}      { return NOTEQUAL; }
{LESSEQUAL}     { return LESSEQUAL; }
{LESSTHAN}      { return LESSTHAN; }
{GREATEREQUAL}  { return GREATEREQUAL; }
{GREATERTHAN}   { return GREATERTHAN; }
{AND}           { return AND; }
{OR}            { return OR; }

{ID}            { yylval.name = strdup(yytext); return ID; }
{INTCON}        { yylval.value = atoi(yytext); return INTCON; }

[ \t\n]*        ;
