#include <stdio.h>

int suma(int,int);

int main(){
	int a = 10;
	int b = 7;
	int c = 16;
	int d = 23;
	int e = 90;
	int f = 3;
	int g = 8;
	int h = 12;
	int i;
	i = suma(suma(suma(a,b),suma(c,d)),suma(suma(e,f),suma(g,h)));
	printf("%d",i);
	return 0;
}

int suma(int x, int y){
	return x + y;
}
