#include <cstring>
#include <cstdio>
#include <iostream>

using namespace std;

int main(void) {
  double d;
  while(cin >> d) {
    float f = (float)d;
    fwrite(&f, sizeof(float), 1, stdout);
  }
  return 0;
}
