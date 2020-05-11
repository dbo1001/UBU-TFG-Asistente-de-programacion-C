#include <stdio.h>
int main(){
	int sumatorio, factorial;
	sumatorio = 0;
	factorial = 1;
	for (int i = 1;i<=10;i++){
		factorial*=i;
	}
	int i;
	for (i = 1;i<=10;i++){
		sumatorio+=i;
	}
	printf("Factorial: %d\n",factorial);
	printf("Sumatorio: %d\n",sumatorio);
	return 0;
}