#include "XE.h"
#include <iostream>

using namespace std;

int main(int argc, const char* argv[])
{
	if (argc != 2) return 1;
	XE *xe = new XE(argv[1]);
	if (!*xe) return 2;
	return 0;
}
