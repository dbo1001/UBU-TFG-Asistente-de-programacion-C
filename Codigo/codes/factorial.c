#include <stdio.h>
int main(){
	float resultado;
	resultado = 1;
	for (int i = 1;i<=10;i++){
		resultado*=i;
	}
	printf("%f\n",resultado);
	return 0;
}



