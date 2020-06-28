#include <stdio.h>
//funcionan los comentarios??
void suma (int x, int y);
//veremos
int resta (int a, int b);
 
int main () {//y en mitad de la linea???
	int a = 10;
	int b = 5
	suma(a,b);
	int c;
	c = resta(a,b) * resta(a,b);
	printf("El cuadrado de la resta de %d y %d es igual a %d\n",a,b,c);
	return 0;
}

void suma (int x, int y){
	int z = x + y;
	printf("La suma de %d y %d es igual a %d\n",x,y,z);
}

int resta (int a, int b){
	return a - b;
}









