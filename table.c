#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "tableandtree.h"

struct ST_node *ST_add_local(char *name)
{
    return ST_add(ST_local, name);
}

void ST_dealloc_local( )
{
    while(ST_local != NULL)
    {
        ST_node *tmp = ST_local;
        ST_local = ST_local->next;
        free(tmp);
    }
    return;
}

struct ST_node *ST_add_global(char *name)
{
    return ST_add(ST_global, name);
}


struct ST_node *ST_add(struct ST_node *cur, char *name)
{

    struct ST_node *newNode = malloc(sizeof(struct ST_node));
    newNode->name = name;
    newNode->type = __undef;
    newNode->value = 0;
    newNode->isDefined = 0;
    newNode->isArray = 0;
    newNode->arrayIndex = 0;
    newNode->isFunction = 0;
    newNode->params = NULL;
    newNode->next = cur;
    return newNode;
}

struct Param *Param_add(struct Param *cur, char *name, enum Type type)
{
    struct Param *newNode = malloc(sizeof(struct Param));
    newNode->name = name;
    newNode->type = type;
    newNode->isArray = 0;
    newNode->next = cur;
    return newNode;
}

int ST_contains(struct ST_node* head, char *name)
{
    struct ST_node *ptr = head;
    while(ptr != NULL)
    {
        if(!strcmp(name, ptr->name))
        {
            //name found in list
            return 1;
        }
        ptr = ptr->next;
    }
    return 0;
}

int is_defined(struct ST_node* head, char *name, int isFunc)
{
    struct ST_node *ptr = head;
    while(ptr != NULL)
    {
        if (isFunc) {
            if(!strcmp(name, ptr->name) && ptr->isDefined)
                return 1;

        } else
            if(!strcmp(name, ptr->name) && !ptr->isFunction && ptr->isDefined) {

            //name found in list
            return 1;
        }
        ptr = ptr->next;
    }
    return 0;
}

void ST_store(char *name, int value)
{
    printf("inside ST_store\n");
    struct ST_node *ptr = ST_local;
    while(ptr != NULL)
    {
        if(!strcmp(name, ptr->name))
        {
            ptr->value = value;
            printf("returning\n");
            return;
        }
        ptr = ptr->next;
    }
    ptr = ST_global;
    while(ptr != NULL)
    {
        if(!strcmp(name, ptr->name))
        {
            ptr->value = value;
            return;
        }
        ptr = ptr->next;
    }
}

struct ST_node *ST_query(struct ST_node *top, char *name)
{
    struct ST_node *ptr = top;
    while(ptr != NULL)
    {
        if(!strcmp(name, ptr->name))
        {
            return ptr;
        }
        ptr = ptr->next;
    }
    return NULL;
}

struct ST_node *ST_query_both(char *name)
{
    struct ST_node *ptr = ST_local;
    while(ptr != NULL)
    {
        if(!strcmp(name, ptr->name))
        {
            return ptr;
        }
        ptr = ptr->next;
    }
    ptr = ST_global;
    while(ptr != NULL)
    {
        if(!strcmp(name, ptr->name))
        {
            return ptr;
        }
        ptr = ptr->next;
    }

    return NULL;
}


int ST_type_query(struct ST_node *top, char *name)
{
    struct ST_node *ptr = top;
    while(ptr != NULL)
    {
        if(!strcmp(name, ptr->name))
        {
            return ptr->type;
        }
        ptr = ptr->next;
    }
    return 0;
}

int ST_value_query(struct ST_node *top, char *name)
{
    struct ST_node *ptr = top;
    while(ptr != NULL)
    {
        if(!strcmp(name, ptr->name))
        {
            return ptr->value;
        }
        ptr = ptr->next;
    }
    return 0;
}



/* Check the params are the same */
int check_params(struct Param *a, struct Param *b) {
    while (a != NULL && b != NULL) {
        if (a->type != b->type || a->isArray != b->isArray)
            return 0;
        a = a->next;
        b = b->next;
    }
    if  (a != NULL || b != NULL)
        return 0;

    return 1;
}

/*
int main() {

    ST_top = ST_add(ST_top, "node1");
    ST_top->value = 42;
    ST_top->type = __char;
    ST_top->isArray = 0;

    ST_top = ST_add(ST_top, "node2");
    ST_top->value = 17;
    ST_top->type = __char;
    ST_top->isArray = 0;

    int result = type_compat(ST_top, ST_top->next);

    printf("%d\n", result);

    return 0;

}
*/
