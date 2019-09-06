%{
    #include <assert.h>
    #include "lex.yy.c"
    #include "tableandtree.h"

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
%type <value> type
%type <stnode> var_decl comvar comvars parm_types
%type <ptnode> expr opt_expr comexpr comexprs  stmt stmts
%type <ptnode> comid comids  optelse
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

var_decl: ID                    { if (scope == 0) {
                                    if (ST_query(ST_global, $1) != NULL) {
                                        semanticError("Redeclaration of global variable");
                                    }
                                    ST_global = ST_add(ST_global, $1);
                            printf("[var_decl]\tAdded var to ST! name: %s\n",ST_global->name); 
                                    $$ = ST_global;
                                  } else {
                                    if (ST_query(ST_local, $1) != NULL) {
                                        semanticError("Redeclaration of local variable");
                                    }
                                    ST_local = ST_add(ST_local, $1);
                               printf("[var_decl]\tAdded var to ST! name: %s\n",ST_local->name); 
                                    $$ = ST_local;
                                  }}
        ;

type    : INT                   { $$ = __int;  }
        ;


parm_types:VOID                     {}
	;


func 	: type ID '(' parm_types ')'
                    { if (ST_contains(ST_global, $2) && ST_query(ST_global, $2)->isDefined) {
                                        semanticError("Redeclaration of function");
                                  }
                                  ST_global = ST_add(ST_global, $2);
                                  ST_global->type = $1;
                                  ST_global->isFunction = 1;
                                  ST_global->isDefined = 1;
                                  cur_func = ST_global;
                               printf("[func]: Added func to global ST! ");
                               printf("name: %s\n", ST_global->name);
                                 scope = 1;

                                 root = PT_make(__enter, NULL, NULL, NULL, NULL);
                                }

                    '{' typeddecs stmts '}' {root->next = $9;

                                assert( root->next != NULL );

                                /* generate code for the function */

                                  code_gen(root);

                                /* pop the ST */
                                  ST_dealloc_local();
                                  scope = 0;

                                }

        | VOID ID '(' parm_types ')'
                                 { if (ST_contains(ST_global, $2)
                                       && ST_query(ST_global, $2)->isDefined)
                                { semanticError("Redeclaration of function"); }

                                  ST_global = ST_add(ST_global, $2);
                                  ST_global->type = __void;
                                  ST_global->isFunction = 1;
                                  ST_global->isDefined = 1;
                                  cur_func = ST_global;
                                  scope = 1;
                                }
                            '{' typeddecs stmts '}' {}
        ;

typeddecs: typeddecs typeddec
        |
        ;

typeddec: type var_decl ';' { $2->type = $1;
                                      struct ST_node *ptr = ST_local;
                                      while(ptr->type == __undef) {
                                        ptr->type = $1;
                                        ptr = ptr->next;
                                      }
                                    }
        ;

stmts   : stmts stmt            { if ($1 != NULL) { $1->next = $2; $$ = $1; }
                                  else { $$ = $2; } }
        |                       { $$ = NULL; }
        ;

stmt    : FOR '(' opt_assg ';' opt_expr ';' opt_assg ')' stmt
                                { PT_make(__for, $3, $5, $7, $9); }
        | assg ';'              { $$ = $1; printf("inside assg ';'\n"); }
        | '{' stmts '}'         { $$ = $2; }
        | ';'                   { $$ = NULL; }
        ;

opt_assg: assg                  { $$ = $1; }
        | /* empty */           { $$ = NULL; }
        ;

opt_expr: expr                  { if ($1->type != __bool)
                        {semanticError("You need a bool expression");}
                                  $$ = $1; }
        | /* empty */           { $$ = NULL; }
        ;

assg    : ID '=' expr           {  printf("lhs->type: %d ", ST_query_both($1)->type);
                                   printf("rhs->type: %d\n", $3->type);
                                    //if (!type_compat($3, ST_query_both($1)))
                                  //{ semanticError("Don't assign that type!"); }
                        $$ = PT_make(__assign, PT_make_fromST(ST_query_both($1)), $3, NULL, NULL); 
                        printf("still okay\n");
                                  ST_store($1, $3->value);
                                }

        ;

expr    : '-' expr  %prec '!'   { if (!($2->type == __int || $2->type == __int))
                          {semanticError("Can only take negative of int or char");}
                                  $$ = PT_make(__minus, $2, NULL, NULL, NULL);
                                  $$->type = __int;
                                  $$->value = (-1) * $2->value;
                                }
        | expr '+' expr         { if (!type_compat($1, $3)) {semanticError("Type incompatibility");}
                                  $$ = PT_make(__plus, $1, $3, NULL, NULL);
                                  $$->type = __int;
                                  $$->value = $1->value + $3->value;
                                  }
        | expr '-' expr         { if (!type_compat($1, $3)) {semanticError("Type incompatibility");}
                                  $$ = PT_make(__sub, $1, $3, NULL, NULL);
                                  $$->type = __int;
                                  $$->value = $1->value -  $3->value;
                                  }
        | expr '*' expr         { if (!type_compat($1, $3)) {semanticError("Type incompatibility");}
                                  $$ = PT_make(__mult, $1, $3, NULL, NULL);
                                  $$->type = __int;
                                  $$->value = $1->value *  $3->value;
                                  }
        | expr '/' expr         { if (!type_compat($1, $3)) {semanticError("Type incompatibility");}
                                  $$ = PT_make(__div, $1, $3, NULL, NULL);
                                  $$->type = __int;
                                  $$->value = $1->value /  $3->value;
                                  }
        | expr EQUAL expr       { if (!type_compat($1, $3)) {semanticError("Type incompatibility");}
                                  $$ = PT_make(__equal, $1, $3, NULL, NULL);
                                  $$->type = __bool;
                                  $$->value = $1->value ==  $3->value;
                                  }
        | expr NOTEQUAL expr    { if (!type_compat($1, $3)) {semanticError("Type incompatibility");}
                                  $$ = PT_make(__notequal, $1, $3, NULL, NULL);
                                  $$->type = __bool;
                                  $$->value = $1->value != $3->value;
                                }
        | expr LESSEQUAL expr   { if (!type_compat($1, $3)) {semanticError("Type incompatibility");}
                                  $$ = PT_make(__lessequal, $1, $3, NULL, NULL);
                                  $$->type = __bool;
                                  $$->value = $1->value <= $3->value;
                                }
        | expr LESSTHAN expr    { if (!type_compat($1, $3)) {semanticError("Type incompatibility");}
                                  $$ = PT_make(__lessthan, $1, $3, NULL, NULL);
                                  $$->type = __bool;
                                  $$->value = $1->value <  $3->value;
                                }
        | expr GREATEREQUAL expr{ if (!type_compat($1, $3)) {semanticError("Type incompatibility");}
                                  $$ = PT_make(__greaterequal, $1, $3, NULL, NULL);
                                  $$->type = __bool;
                                  $$->value = $1->value >= $3->value;
                                }
        | expr GREATERTHAN expr { if (!type_compat($1, $3)) {semanticError("Type incompatibility");}
                                  $$ = PT_make(__greaterthan, $1, $3, NULL, NULL);
                                  $$->type = __bool;
                                  $$->value = $1->value >  $3->value;
                                }
    /* bool stuff */
        | '!' expr              { if ($2->type != __bool) {semanticError("#");}
                                  $$ = PT_make(__not, $2, NULL, NULL, NULL);
                                  $$->type = __bool;
                                  $$->value =   ! $2->value;
                                  }
        | expr AND expr         { if ($1->type != __bool) {semanticError("#");}
                                  if ($3->type != __bool) {semanticError("#");}
                                  $$ = PT_make(__and, $1, $3, NULL, NULL);
                                  $$->type = __bool;
                                  $$->value = $1->value && $3->value;
                                  }
        | expr OR expr          { if ($1->type != __bool) {semanticError("#");}
                                  if ($3->type != __bool) {semanticError("#");}
                                  $$ = PT_make(__or, $1, $3, NULL, NULL);
                                  $$->type = __bool;
                                  $$->value = $1->value || $3->value;
                                  }
    /* known vars */
        | ID                    { $$ = PT_make_fromST(ST_query_both($1)); }
        | '(' expr ')'          { $$ =    $2;    }
        | INTCON                { $$ = PT_make(__intconst, NULL, NULL, NULL, NULL) ;
                                  $$->value = $1;
                                  $$->type = __int; }
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




