#include <iostream>
#include <cstdio>

using namespace std;

int main() {
  char ch;
  while(cin.get(ch)) {
    float r, g, b;
    switch(ch) {
      case '1': r = 1.0f; g = 0.0f; b = 0.0f; break;
      case '2': r = 0.0f; g = 1.0f; b = 0.0f; break;
      case '3': r = 0.0f; g = 0.0f; b = 1.0f; break;
      case '4': r = 1.0f; g = 1.0f; b = 0.0f; break;
      default:
        cerr << "Invalid symbol on input" << endl;
        return 1;
    }
    fwrite(&r, sizeof(float), 1, stdout);
    fwrite(&g, sizeof(float), 1, stdout);
    fwrite(&b, sizeof(float), 1, stdout);
  }
  return 0;
}
