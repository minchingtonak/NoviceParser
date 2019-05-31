%{
    #include <assert.h>
    #include "lex.yy.c"
    #include "tableandtree.h"

    #define TYPE_CONVERTER(type) (type == 0 ? "char" : (type == 1 ? "int" : "undef??"))

    int yylex(void);
    void yyerror(char *);
    int yydebug = 1;

    int exit_value = 0;

    void semanticError(char *s);

    int scope = 0;
    int code_gen_on = 0;

%}

/* These are possible "types" for the tokens and non-terminals (yylval) */
%union {
    int value;
    char *name;
    char charcon; /* maybe delete */
    char *stringcon;
    struct ST_node *stnode;
    struct PT_node *ptnode;
    struct Param *param;
}

/* Here we specify types for individual non-terminals */ /** unused ones should be deleted **/
%type <value> type /* types are represented as ints from an enum in tableandtree.h */
%type <stnode> var_decl parm_types
%type <ptnode> expr opt_expr  stmt stmts
%type <ptnode> opt_assg assg

/* Here we specify types for individual tokens */
%token <name> ID
%token <value> INTCON

%token VOID INT FOR
%token EQUAL NOTEQUAL LESSEQUAL LESSTHAN GREATEREQUAL GREATERTHAN AND OR

%left  OR
%left  AND
%left  EQUAL NOTEQUAL
%left  LESSEQUAL  LESSTHAN GREATEREQUAL GREATERTHAN
%left  '+' '-'
%left  '*' '/'
%right '!'

%start progs

%%
progs   : progs prog
        |
        ;

prog    : func           {    }
        ;

var_decl: ID                    { printf("Variable declared\n");
                                  $$ = ST_add_global($1);
                                  printf("created st node %s %i\n", $$->name, ST_contains($$, "a")); }
        ;

type    : INT                   { printf("int type\n");
                                  $$ = __int; }
        ;


parm_types:VOID                     { printf("void param\n"); }
	;


func 	: type ID '(' parm_types ')'
                    { printf("Function %s declared\n", $2); }

                    '{' typeddecs stmts '}' {  }

        | VOID ID '(' parm_types ')'
                                 { }
                            '{' typeddecs stmts '}' {}
        ;

typeddecs: typeddecs typeddec
        |
        ;

typeddec: type var_decl ';' { printf("%s %s declared\n", TYPE_CONVERTER($1), $2->name); }
        ;

stmts   : stmts stmt            { }
        |                       { }
        ;

stmt    : FOR '(' opt_assg ';' opt_expr ';' opt_assg ')' stmt
                                { printf("for loop declared\n"); }
        | assg ';'              { }
        | '{' stmts '}'         { }
        | ';'                   { }
        ;

opt_assg: assg                  { printf("optional assignment\n"); }
        | /* empty */           { }
        ;

opt_expr: expr                  { }
        | /* empty */           { }
        ;

assg    : ID '=' expr           { printf("variable %s assigned the value of %i", $1, $3->value); }

        ;

expr    : '-' expr  %prec '!'   { }
        | expr '+' expr         { }
        | expr '-' expr         { }
        | expr '*' expr         { }
        | expr '/' expr         { }
        | expr EQUAL expr       { }
        | expr NOTEQUAL expr    { }
        | expr LESSEQUAL expr   { }
        | expr LESSTHAN expr    { }
        | expr GREATEREQUAL expr{ }
        | expr GREATERTHAN expr { }
    /* bool stuff */
        | '!' expr              { }
        | expr AND expr         { }
        | expr OR expr          { }
    /* known vars */
        | ID                    { }
        | '(' expr ')'          { }
        | INTCON                { }
        ;

%%

void yyerror(char *s) {

    exit_value = 1;

    fprintf(stderr, "Line %d: %s", yylineno, s);
    fprintf(stderr, ": unexpected ");
    switch (yychar) {
        case 0:
            fprintf(stderr, "EOF");
            break;
        default:
            fprintf(stderr, "%s", yytext);
            break;
    }

    fprintf(stderr, "\n");

    return;
}

void semanticError(char *s) {

    exit_value = 1;

    fprintf(stderr, "Line %d: %s", yylineno, s);
    fprintf(stderr, "\n");

    return;
}

int main(void) {

    out_fp = fopen("out.s", "w");
    if (out_fp == NULL) {
        fprintf(stderr, "Could not write out.s\n");
        exit(1);
    }
    code_gen_on = 1;

    yyparse();

    fclose(out_fp);
    return exit_value;

}




