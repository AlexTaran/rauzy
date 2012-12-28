#include <iostream>

using namespace std;

int main() {
  char ch;
  unsigned long long x = 0, y = 0, z = 0, w = 0;
  while(cin.get(ch)) {
    switch(ch) {
      case '1': ++x; break;
      case '2': ++y; break;
      case '3': ++z; break;
      case '4': ++w; break;
      default:
        cerr << "Invalid symbol on input" << endl;
        return 1;
    }
    cout << x << "\t" << y << "\t" << z << '\t' << w << endl;
  }
  return 0;
}
