#include <boost/numeric/ublas/vector.hpp>
#include <boost/numeric/ublas/io.hpp>
#include <iostream>
#include <vector>
#include <sstream>
#include <ctime>
#include "megatree.h"

using namespace boost::numeric;

using std::cin;
using std::cout;
using std::cerr;
using std::endl;
using std::pair;

typedef ublas::vector<double> vec;

int stoi(char* s) {
  int n;
  std::istringstream iss(s);
  iss >> n;
  return n;
}

inline double sqr(double d) {
  return d * d;
}

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

class DistComparator {
 public:
  DistComparator(const vec& p) : center(p)
  { }

  bool operator() (const pair<vec, size_t>& v1, const pair<vec, size_t>& v2) const {
    double dist1 = sqr(v1.first(0) - center(0)) +
                   sqr(v1.first(1) - center(1)) +
                   sqr(v1.first(2) - center(2));
    double dist2 = sqr(v2.first(0) - center(0)) +
                   sqr(v2.first(1) - center(1)) +
                   sqr(v2.first(2) - center(2));
    return dist1 < dist2;
  }
 private:
  vec center;
};

std::vector<pair<vec, size_t> > genIndexedNeighbours(const std::vector<pair<vec, size_t> > points,
                                                     const vec& center, int k) {
  std::vector<pair<vec, size_t> > sorted(points);
  //std::sort(sorted.begin(), sorted.end(), DistComparator(center));
  std::nth_element(sorted.begin(), sorted.begin() + k, sorted.end(), DistComparator(center));
  std::nth_element(sorted.begin(), sorted.begin(), sorted.begin() + k + 1, DistComparator(center));
  return std::vector<pair<vec, size_t> >(sorted.begin() + 1, sorted.begin() + 1 + k);
}

int main(int argc, char** argv) {
  if (argc != 2) {
    cerr << "Wrong number of arguments" << endl;
    return 1;
  }
  // k nearest neighbours
  int k = stoi(argv[1]);
  std::vector<vec> points = read_points();
  Kubizm<double> main_kubizm;
  main_kubizm.low(0)  = main_kubizm.low(1)  = main_kubizm.low(2)  = -10.0;
  main_kubizm.high(0) = main_kubizm.high(1) = main_kubizm.high(2) =  10.0;
  MegaTree<double, size_t> octree(main_kubizm);
  for (size_t i = 0; i < points.size(); ++i) {
    octree.add_point(points[i], i);
  }
  /*cerr << points.size() << endl;
  std::vector<std::string> node_infos = octree.get_nodes_info();
  for (size_t i = 0; i < node_infos.size(); ++i) {
    cerr << node_infos[i] << endl;
  }
  return 0;*/
  // And now search nearest neighbours!
  double current_search_radius = 0.5;
  time_t begin_processing = clock();
  for (size_t i = 0; i < points.size(); ++i) {
    std::vector<std::pair<ublas::vector<double>, size_t> > found_neibs;
    double current_step = 0.5;
    while(true) {
      found_neibs = octree.get_nearest_neighbours(points[i], current_search_radius);
      if (found_neibs.size() < k + 1) {
        current_search_radius += current_step;
        current_step *= 0.5;
      } else if (found_neibs.size() > k * 10) {
        current_search_radius -= current_step;
        current_step *= 0.5;
      } else {
        break;
      }
    }
    std::vector<pair<vec, size_t> > neighbours;
    neighbours = genIndexedNeighbours(found_neibs, points[i], k);

    cout << points[i](0) << " " << points[i](1) << " " << points[i](2);
    for (size_t j = 0; j < neighbours.size(); ++j) {
      cout << " "<< neighbours[j].first(0) << " " << neighbours[j].first(1) << " " <<
          neighbours[j].first(2);
    }
    cout << endl;
    // Pretty print time estimations!
    if (i !=0 && i % 200 == 0) {
      cerr << "Processed " << i << " points" << endl;
      time_t delta_processing = clock() - begin_processing;
      double seconds_passed = delta_processing * 1.0 / CLOCKS_PER_SEC;
      double seconds_left = seconds_passed / i * (points.size() - i);
      cerr << "Left " << seconds_left << " seconds / ";
      cerr << seconds_left / 60.0 << " minutes / ";
      cerr << seconds_left / 3600.0 << " hours"<< endl;
    }
  }
  return 0;
}
