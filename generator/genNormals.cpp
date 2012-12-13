#include <boost/numeric/ublas/vector.hpp>
#include <boost/numeric/ublas/io.hpp>
#include <iostream>
#include <vector>
#include <sstream>
#include <string>

using std::cin;
using std::cout;
using std::cerr;
using std::endl;
using std::string;

using namespace boost::numeric;

typedef ublas::vector<double> vec;

int main() {
  string s;
  while (std::getline(cin, s)) {
    std::istringstream iss(s);
    std::vector<vec> points;
    std::vector<double> inp;
    double d;
    while (iss >> d) {
      inp.push_back(d);
      if (inp.size() == 3) {
        vec v(3);
        for (int i = 0; i < 3; ++i) {
          v(i) = inp[i];
        }
        points.push_back(v);
        inp.clear();
      }
    }
    // gen vectors to neighbours
    std::vector<vec> vecs;
    vec sum(3);
    sum(0) = sum(1) = sum(2) = 0.0;
    for (size_t i = 1; i < points.size(); ++i) {
      vecs.push_back(points[i] - points[0]);
      sum += points[i] - points[0];
      //sum += (points[i] - points[0]) / ublas::norm_2(points[i] - points[0]);
    }
    double l = ublas::norm_2(sum);
    if (l < 1e-4) {
      cout << "0.0 0.0 0.0" << endl;
    } else {
      sum /= -l;
      cout << sum(0) << " " << sum(1) << " "<< sum(2) << endl;
    }
  }
  return 0;
}
