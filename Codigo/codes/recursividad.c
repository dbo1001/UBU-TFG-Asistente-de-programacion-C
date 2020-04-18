#include <stdio.h>
int recursividad(int i);
int main(){
	int i = 10;
	int j = recursividad(i);
	i++;
	i-=1;
	int k = 8 + 9;
	int f[9];
	printf("%d\n",j);
	return 0;
}

int recursividad(int i){
	if (i>1){
		return recursividad(i-1) + recursividad(i-2);
	}
	return i;
}



