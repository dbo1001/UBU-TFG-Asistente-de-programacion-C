#include <stdio.h>

void suma (int x, int y);

int resta (int a, int b);
 
int main () {
	int a = 10;
	int b = 5;
	suma(a,b);
	int c = resta(a,b);
	printf("la resta de %d y %d es igual a %d\n",a,b,c);
	return 0;
}

void suma (int x, int y){
	int z = x + y;
	printf("la suma de %d y %d es igual a %d\n",x,y,z);
}

int resta (int a, int b){
	return a - b;
}


