%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef union {
    char *str;
} YYSTYPE;

void yyerror(char *);
int yylex(void);
void yyerror(char *);
int yylex(void);
#define YYSTYPE char *
int i = 1;
%}

%token PROTOCOL
%token DECLARATIONS
%token KNOWLEDGE
%token ACTIONS
%token GOALS
%token END
%token ID

%%
program : protocol declarations knowledge actions goals end
        ;

protocol : PROTOCOL ID          { printf("protocol %s;\n", $2); }
         ;

declarations :DECLARATIONS{ printf("declarations\n"); }   declarations_list
             ;

declarations_list : /* empty */
               | declarations_list declarations_entry
               ;

declarations_entry : ID  ID { printf("    %s %s;\n", $1, $2); }
		

knowledge : KNOWLEDGE { printf("knowledge\n"); }  knowledge_list 
          ;

knowledge_list : /* empty */
               | knowledge_list knowledge_entry
               ;

knowledge_entry : ID  ID { printf("    %s: %s%s;\n", $1, $2);}
		
                ;

actions : ACTIONS { printf("messages\n"); }  actions_list
        ;

actions_list : /* empty */
             | actions_list action_entry
             ;

action_entry :  ID  ID  ID  ID ID{ printf("%d.    %s %s %s : %s\n", i,$2, $3, $4,$5); i++;}
             ;

goals : GOALS { printf("goal\n"); } goals_list
      ;

goals_list : /* empty */
           | goals_list goal_entry
           ;

goal_entry :  ID  ID  ID  ID ID { printf("    secrecy_%s %s [%s];\n", $4, $2, $5);}
           ;

end : END {; }
           ;
%%
int main() {
    yyparse();
    return 0;
}

int yywrap(){
    return 1;
}

void yyerror(char *str){
    fprintf(stderr,"error:%s\n",str);
}
