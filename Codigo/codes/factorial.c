#include <stdio.h>
int main(){
	int sumatorio;
	int factorial;
	sumatorio = 0;
	factorial = 1;
	int i = 1;
	while (i<=10){
		factorial*=i;
		i++;
	}
	for (i = 1;i<=10;i++){
		sumatorio+=i;
	}
	printf("Factorial: %d\n",factorial);
	printf("Sumatorio: %d\n",sumatorio);
	return 0;
}







