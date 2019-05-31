/* Symbol Table */

struct ST_node
{
    char *name;
    int value;
    int type;
    int isDefined;
    int isArray;
    int arrayIndex;
    int isFunction;
    struct Param *params;
    struct ST_node *next;
};

typedef struct ST_node ST_node;

/* Parse Table */

struct PT_node
{
    struct ST_node *ST_entry;
    int tag;
    int type;
    int value;
    struct PT_node *parent;
    struct PT_node *children[4];
    struct PT_node *next;
};

typedef struct PT_node PT_node;

/* Param struct */
struct Param
{
    char *name;
    int type;
    int isArray;
    struct Param *next;
};

typedef struct Param Param;

enum Type {
    __char,
    __int,
    __bool,
    __void,
    /* possibly a kludge */
    __undef
};

enum Tag {
    /* binary operators */
    __plus,
    __sub,
    __mult,
    __div,
    __minus,
    /* logical */
    __not,
    __equal,
    __notequal,
    __lessthan,
    __lessequal,
    __greaterthan,
    __greaterequal,
    __and,
    __or,
    /* structure */
    __for,
    __while,
    __if,
    /* assignment */
    __assign,
    __intconst,
    __charconst,
    __strconst,
    __someconst,
    /* function */
    __call,
    __return,
    __enter
};

// So it begins
struct ST_node *ST_local;
struct ST_node *ST_global;

struct PT_node *root;

// Keep track of stuff
struct ST_node *cur_func;

// Output file
FILE *out_fp;


// ST linked list methods
struct ST_node *ST_add_local(char *name);
void            ST_dealloc_local( );
struct ST_node *ST_add_global(char *name);
struct ST_node *ST_add(struct ST_node *top, char *name);
int             ST_contains(struct ST_node *top, char *name);
void            ST_store(char *name, int value);
struct ST_node *ST_query(struct ST_node *top, char *name);
struct ST_node *ST_query_both(char *name);
int             ST_type_query(struct ST_node *top, char *name);
int             ST_value_query(struct ST_node *top, char *name);

// PT tree structure methods
PT_node *PT_make_fromST(struct ST_node *id);
PT_node *PT_make(enum Tag t, PT_node *c0, PT_node *c1, PT_node *c2, PT_node *c3);
void PT_dealloc();

// Param linked list methods
struct Param *  Param_add(struct Param *cur, char *name, enum Type type);

// Type compatibility methods
int             type_compat(struct PT_node *a, struct PT_node *b);
int             is_defined(struct ST_node* head, char *name, int isFunc);

// Code generation
void            code_gen(struct PT_node *root);

