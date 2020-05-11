#include <stdio.h>
int main(){
	int a = 2;
	int b = 3;
	int c;
	int d;
	int e = a ^ b;
	c = a < b;
	d = a > b;
	while (a){
		a--;
	}
	printf("%d %d\n", c, d);
	return 0;
}