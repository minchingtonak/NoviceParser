#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "tableandtree.h"


/* For leaf node from ID */
PT_node *PT_make_fromST(struct ST_node *id)
{

    PT_node *newNode = malloc(sizeof(PT_node));
    newNode->ST_entry = id;
    newNode->tag = __someconst;
    newNode->type = id->type;
    int i;
    for (i = 0; i < 4; i++)
        newNode->children[i] = NULL;
    return newNode;

}

PT_node *PT_make(enum Tag t, PT_node *c0, PT_node *c1, PT_node *c2, PT_node *c3)
{

    PT_node *newNode = malloc(sizeof(PT_node));
    newNode->tag = t;
    newNode->ST_entry = NULL;
    newNode->children[0] = c0;
    if (c0 != NULL)
        c0->parent = newNode;
    newNode->children[1] = c1;
    if (c1 != NULL)
        c1->parent = newNode;
    newNode->children[2] = c2;
    if (c2 != NULL)
        c2->parent = newNode;
    newNode->children[3] = c3;
    if (c3 != NULL)
        c3->parent = newNode;
    return newNode;

}


void free_PT_node(PT_node *cur_node)
{
    int i;
    for (i = 0; i < 4; i++)
    {
        if (cur_node->children[i] != NULL) {
            free_PT_node(cur_node->children[i]);
            free(cur_node->children[i]);
        }
    }
    return;
}

void PT_dealloc( )
{
    free_PT_node(root);
}

/* Compatible only if:
 * int is compatible with int,
 * char is compatible with char;
 * int is compatible with char,
 * char is compatible with int;
 * an array of int is compatible with an array of int,
 * an array of char is compatible with an array of char;
 */
int type_compat(struct PT_node *a, struct PT_node *b) {

    enum Type type1 = a->type;
    enum Type type2 = b->type;


    if ( (type1 == __int  && type2 == __int)  ||
         (type1 == __int  && type2 == __char) ||
         (type1 == __char && type2 == __int)  ||
         (type1 == __char && type2 == __char) )
        return 1;

    return 0;

}


void code_gen(struct PT_node *root)
{
    struct PT_node *ptr = root;

    if (ptr == NULL) {
        fprintf(out_fp, "NULL\n");
        return;
    }



    switch (ptr->tag) {

        case __enter:
            fprintf(out_fp, ".text\n\n");
            fprintf(out_fp, "%s:\n\n", cur_func->name);
            fprintf(out_fp, "#Enter\n");
            fprintf(out_fp, "sw $fp, -4($sp)\n");
            fprintf(out_fp, "sw $ra, -8($sp)\n");
            fprintf(out_fp, "la $fp, 0($sp)\n");
            int offset = 32;
            fprintf(out_fp, "la $sp, -%d($sp)\n", offset);
            fprintf(out_fp, "\n");

            break;

        case __return:
            fprintf(out_fp, "#Return\n");

            if (ptr->children[0] != NULL) {
                fprintf(out_fp, "lw $v0, 4($fp)\n");
            }

            fprintf(out_fp, "la $sp, 0($fp)\n");
            fprintf(out_fp, "lw $ra, -8($sp)\n");
            fprintf(out_fp, "lw $fp, -4($sp)\n");
            fprintf(out_fp, "jr $ra\n");
            fprintf(out_fp, "\n");
            break;

        case __for:
            ;
            break;
        case __while:
            ;
            break;
        case __if:
            fprintf(out_fp, "if!!\n");
            break;
        case __assign:
            fprintf(out_fp, "assign!!\n");
            ;
            break;
    }

    int i;
    for (i = 0; i < 4; i++) {
        code_gen(ptr->children[i]);
    }


    code_gen(ptr->next);


}


void code_gen_stmt(struct PT_node *S)
{
    switch (S->tag) {
        case __for:
            ;
            break;
        case __while:
            ;
            break;
        case __if:
            ;
            break;
        case __assign:
            ;
            break;
    }

}

void code_gen_expr(struct PT_node *E)
{
    switch (E->tag) {
        case __plus:
            ;
            break;
        case __minus:
            ;
            break;
        case __mult:
            ;
            break;
        case __div:
            ;
            break;
        case __equal:
            ;
            break;
        case __lessthan:
            ;
            break;
        case __lessequal:
            ;
            break;
        case __greaterthan:
            ;
            break;
        case __greaterequal:
            ;
            break;
    }

}

