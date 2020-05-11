#include <stdio.h>
int main(){
	int a = -10;
	int b = a++;
	int c = ++a;
	int d = a--;
	int e = --a;
	int f = -a;
	if(a<0){
		a++;
	}
	while(a<0){
		a++;
	}
	for(a=0;a<10;a++){
		b++;
	}
	printf("%d %d %d %d %d %d\n", a, b, c, d ,e, f);
	return 0;
}