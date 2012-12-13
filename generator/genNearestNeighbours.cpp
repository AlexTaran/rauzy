#include <boost/numeric/ublas/vector.hpp>
#include <boost/numeric/ublas/io.hpp>
#include <iostream>
#include <vector>
#include <sstream>

using namespace boost::numeric;

using std::cin;
using std::cout;
using std::cerr;
using std::endl;

typedef ublas::vector<double> vec;
std::vector<vec> read_points() {
  std::vector<vec> points;
  std::vector<double> inp;
  double f;
  while (cin >> f) {
    inp.push_back(f);
    if (inp.size() == 3) {
      vec v(3);
      for (int i = 0; i < 3; ++i) {
        v(i) = inp[i];
      }
      points.push_back(v);
      inp.clear();
    }
  }
  return points;
}

int stoi(char* s) {
  int n;
  std::istringstream iss(s);
  iss >> n;
  return n;
}

inline double sqr(double d) {
  return d * d;
}

class DistComparator {
 public:
  DistComparator(const vec& p) : center(p)
  { }

  bool operator() (const vec& v1, const vec& v2) const {
    double dist1 = sqr(v1(0) - center(0)) +
                   sqr(v1(1) - center(1)) +
                   sqr(v1(2) - center(2));
    double dist2 = sqr(v2(0) - center(0)) +
                   sqr(v2(1) - center(1)) +
                   sqr(v2(2) - center(2));
    return dist1 < dist2;
  }
 private:
  vec center;
};

std::vector<vec> genNeighbours(const std::vector<vec>& points, int point_index, int k) {
  vec center = points[point_index];
  std::vector<vec> sorted(points);
  //std::sort(sorted.begin(), sorted.end(), DistComparator(center));
  std::nth_element(sorted.begin(), sorted.begin() + k, sorted.end(), DistComparator(center));
  std::nth_element(sorted.begin(), sorted.begin(), sorted.begin() + k + 1, DistComparator(center));
  return std::vector<vec>(sorted.begin() + 1, sorted.begin() + 1 + k);
}

int main(int argc, char** argv) {
  if (argc != 2) {
    cerr << "Wrong number of arguments" << endl;
    return 1;
  }
  // k nearest neighbours
  int k = stoi(argv[1]);
  std::vector<vec> points = read_points();
  cerr << points.size() << endl;
  for (size_t i = 0; i < points.size(); ++i) {
    std::vector<vec> neighbours = genNeighbours(points, i, k);
    cout << points[i](0) << " " << points[i](1) << " " << points[i](2);
    for (size_t j = 0; j < neighbours.size(); ++j) {
      cout << " "<< neighbours[j](0) << " " << neighbours[j](1) << " " << neighbours[j](2);
    }
    cout << endl;
    if (i % 200 == 0) {
      cerr << "Processed " << i << " points" << endl;
    }
  }
  return 0;
}
