%{
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

typedef union {
    char *str;
} YYSTYPE;

#define YYSTYPE_IS_DECLARED 1
#include "CAS+2AB_auh_y.tab.h"

void yyerror(char *);
%}

%%
"Protocol"               { yylval.str = strdup(yytext); return PROTOCOL; }
"Knowledge"              { yylval.str = strdup(yytext); return KNOWLEDGE; }
"Actions"                 { yylval.str = strdup(yytext); return ACTIONS; }
"Goals"                   { yylval.str = strdup(yytext); return GOALS; }
"/*Authenticity*/"                   { yylval.str = strdup(yytext); return AUTHENTICITY; }
"end"                     { return END; }
[()<>'a-zA-Z0-9/-][(){}''/*a-z*A-Z,.^<>/0-9_-]*   { yylval.str = strdup(yytext); return ID; }
[\n]                    ;
[ \t]                   ;
.                      ;
%%

