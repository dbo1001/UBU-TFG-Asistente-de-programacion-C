#include <stdio.h>
 
int main () {
	int a[5]={1,2,3,4};
	int b[2][2]={{1},{3,4}};
	a[4]=5;
	b[0][1]=a[1];
	return 0;
}