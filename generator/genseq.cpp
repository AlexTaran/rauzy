#include <iostream>
#include <string>
#include <sstream>

using namespace std;

string genseq(int iters) {
  string s1 = "12";
  string s2 = "13";
  string s3 = "14";
  string s4 = "1";
  for (int i = 0; i < iters; ++i) {
    string s = s1 + s2 + s3 + s4;
    s1 = s2;
    s2 = s3;
    s3 = s4;
    s4 = s;
  }
  return s4;
}



int main(int argc, char** argv) {
  if (argc != 2) {
    cerr << "Wrong number of args" << endl;
    return 1;
  }
  istringstream iss(argv[1]);
  int n;
  iss >> n;
  cout << genseq(n);
  return 0;
}
