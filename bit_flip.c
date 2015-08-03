#include <stdio.h>
#include <string.h>


int main(int argc, char *argv[])
{
	unsigned long long val = 0xffffffc000e219e0;
	int i;

	for (i=2; i < 32;i++)
		printf("%llx\n", (val ^ 1<<i));

	return 0;
}

