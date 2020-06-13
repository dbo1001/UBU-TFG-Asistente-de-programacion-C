#include <stdio.h>
int recursividad(int i);
int main(){
	int i = 10;
	int j = recursividad(i);
	printf("%d\n",j);
	return 0;
}

int recursividad(int i){
	int c = i;
	if (i>1){
		c = recursividad(i-1) + recursividad(i-2);
	}
	return c;
}








