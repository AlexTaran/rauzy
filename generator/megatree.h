#ifndef __MEGATREE_H__
#define __MEGATREE_H__

#include <algorithm>
#include <vector>
#include <sstream>
#include <string>
#include <utility>

#include <boost/numeric/ublas/vector.hpp>

using namespace boost::numeric;
using std::swap;
using std::pair;
using std::make_pair;

// typedef ublas::vector uvec;
#define uvec ublas::vector

template<class T>
T squared_norm_2(const ublas::vector<T>& v) {
  T result = 0;
  for (size_t i = 0; i < v.size(); ++i) {
    result += v[i] * v[i];
  }
  return result;
}

template<class T>
struct Kubizm {
  ublas::vector<T> low, high;

  Kubizm() : low(3), high(3) {}

  void fix() {
    if (low(1) > high(1)) {swap(low(1), high(1));}
    if (low(2) > high(2)) {swap(low(2), high(2));}
    if (low(3) > high(3)) {swap(low(3), high(3));}
  }

  bool has_point(const ublas::vector<T>& point) const {
    for (size_t i = 0; i < 3; ++i) {
      if (low(i) > point(i) || high(i) < point(i)) {
        return false;
      }
    }
    return true;
  }

  // bydlo-style check. behaves wrong, but for our purposes is enough, lol!
  bool touches_sphere(const ublas::vector<T>& center, const T& radius) const {
    for (size_t i = 0; i < 3; ++i) {
      if (low(i) - radius > center(i) || high(i) + radius < center(i)) {
        return false;
      }
    }
    return true;
  }
};

template<class T, class V>
struct MegaNode {
 public:
  MegaNode(const Kubizm<T>& k) : kubizm(k) {
    for (size_t i = 0; i < 8; ++i) {
      sub_nodes[i % 2][i / 2 % 2][i / 4 % 2] = 0;
    }
    splitted = false;
  }

  void add_point(const ublas::vector<T>& point, const V& data) {
    if (!splitted) {
      points.push_back(make_pair(point, data));
      try_split();
    } else {
      for (size_t i = 0; i < 8; ++i) {
        MegaNode<T, V>* sub_node = sub_nodes[i % 2][i / 2 % 2][i / 4 % 2];
        if (sub_node != 0) {
          if (!sub_node->kubizm.has_point(point)) {
            continue;
          } else { // here add a point!
            sub_node->add_point(point, data);
            break;
          }
        }
      }
    }
  }

  void get_nearest_neighbours(std::vector<pair<uvec<T>, V> >& out, const uvec<T>& center, const T& radius) const {
    if (!kubizm.touches_sphere(center, radius)) {
      return;
    }
    for (size_t i = 0; i < points.size(); ++i) {
      uvec<T> df = center - points[i].first;
      if (squared_norm_2(df) < radius * radius) {
        out.push_back(points[i]);
      }
    }
    for (size_t i = 0; i < 8; ++i) {
      MegaNode<T, V>* sub_node = sub_nodes[i % 2][i / 2 % 2][i / 4 % 2];
      if (sub_node != 0) {
        sub_node->get_nearest_neighbours(out, center, radius);
      }
    }
  }

  std::string get_node_info(int h) {
    std::ostringstream oss;
    oss << "Points: " << points.size() << " splitted: " << (int)splitted;
    oss << " height: " << h;
    return oss.str();
  }

  void fill_node_infos(std::vector<std::string>& infos, int h) {
    infos.push_back(get_node_info(h));
    for (size_t i = 0; i < 8; ++i) {
      if (sub_nodes[i % 2][i / 2 % 2][i / 4 % 2] != 0) {
        sub_nodes[i % 2][i / 2 % 2][i / 4 % 2]->fill_node_infos(infos, h + 1);
      }
    }
  }

 private:
  void try_split() {
    if (points.size() > 100) {
      splitted = true;
      // TODO: split here!
      for (size_t i = 0; i < 8; ++i) {
        MegaNode<T, V>*& sub_node = sub_nodes[i % 2][i / 2 % 2][i / 4 % 2];
        Kubizm<T> new_kubizm;
        for (size_t dim = 0; dim < 3; ++dim) {
          size_t flag = i / (1 << dim) % 2; // = that dimension index
          T half_dist = (kubizm.high(dim) - kubizm.low(dim)) / 2;
          new_kubizm.low(dim) = kubizm.low(dim) + half_dist * flag;
          new_kubizm.high(dim) = kubizm.high(dim) - half_dist * (1 - flag);
        }
        sub_nodes[i % 2][i / 2 % 2][i / 4 % 2] = new MegaNode<T, V>(new_kubizm);
      }
      std::vector<pair<uvec<T>,V> > orphan_points;
      for (size_t i = 0; i < points.size(); ++i) {
        size_t j = 0;
        for (; j < 8; ++j) {
          if (sub_nodes[j % 2][j / 2 % 2][j / 4 % 2]->kubizm.has_point(points[i].first)) {
            sub_nodes[j % 2][j / 2 % 2][j / 4 % 2]->add_point(points[i].first, points[i].second);
            break;
          }
        }
        if (j >= 8) {
          orphan_points.push_back(points[i]);
        }
      }
      points = orphan_points;
    }
  }

  const Kubizm<T> kubizm;
  std::vector<pair<uvec<T>,V> > points;
  MegaNode<T, V>* sub_nodes[2][2][2];
  bool splitted;
};

template<class T, class V>
class MegaTree {
 public:
  MegaTree(const Kubizm<T>& main_kubizm) : root(main_kubizm)
  { }

  void add_point(const ublas::vector<T>& point, const V& data) {
    root.add_point(point, data);
  }

  void add_points(const std::vector<ublas::vector<T> >& points, const std::vector<V>& datas) {
    for (size_t i = 0; i < points.size(); ++i) {
      add_point(points[i], datas[i]);
    }
  }

  std::vector<pair<uvec<T>,V> > get_nearest_neighbours(const ublas::vector<T>& center,
                                                     const T& radius) {
    std::vector<pair<uvec<T>,V> > out;
    root.get_nearest_neighbours(out, center, radius);
    return out;
  }

  std::vector<std::string> get_nodes_info() {
    std::vector<std::string> infos;
    root.fill_node_infos(infos, 0);
    return infos;
  }
 private:
  MegaNode<T, V> root;
};

#endif
