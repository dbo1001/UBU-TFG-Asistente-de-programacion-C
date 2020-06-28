#include <stdio.h>
#include <string.h>
 
struct Books {
   char  titulo[50];
   char  autor[50];
   int   ISBN;
}; 
 
int main( ) {

   struct Books Book;

   strcpy( Book.titulo, "El viento en los sauces");
   strcpy( Book.autor, "Kenneth Grahame"); 
   Book.ISBN = 1530059984;

   return 0;
}






