#include <stdio.h>
#include <mpfr.h>
#include <sstream>
#include <iostream>
#include <cstdarg>

using namespace std;

template<size_t N, size_t Precise = 1024>
class Vec {
 public:
  Vec() {
    for (size_t i = 0; i < N; ++i) {
      mpfr_init2(coords[i], Precise);
      mpfr_set_zero(coords[i], 0);
    }
  }

  Vec(const Vec& other) {
    for (size_t i = 0; i < N; ++i) {
      mpfr_init2(coords[i], Precise);
      mpfr_set(coords[i], other.coords[i], MPFR_RNDN);
    }
  }

  Vec& operator= (const Vec& other) {
    if (&other != this) {
      for (size_t i = 0; i < N; ++i) {
        mpfr_set(coords[i], other.coords[i], MPFR_RNDN);
      }
    }
    return *this;
  }

  void init(...) {
    va_list arguments;
    va_start(arguments, N);
    for (size_t i = 0; i < N; ++i) {
      long l = va_arg(arguments, long);
      mpfr_set_si(coords[i], l, MPFR_RNDN);
    }
    va_end(arguments);
  }

  ~Vec() {
    for (size_t i = 0; i < N; ++i) {
      mpfr_clear(coords[i]);
    }
  }

  float float_at(size_t i) const {
    return mpfr_get_flt(coords[i], MPFR_RNDN);
  }

  void normalize() {
    mpfr_t l, sq;
    mpfr_init(l);
    mpfr_init(sq);
    mpfr_set_zero(l, 0);
    for (size_t i = 0; i < N; ++i) {
      mpfr_mul(sq, coords[i], coords[i], MPFR_RNDN);
      mpfr_add(l, l, sq, MPFR_RNDN);
    }
    mpfr_sqrt(l, l, MPFR_RNDN);
    for (size_t i = 0; i < N; ++i) {
      mpfr_div(coords[i], coords[i], l, MPFR_RNDN);
    }
    mpfr_clear(l);
    mpfr_clear(sq);
  }
 public:
  mpfr_t coords[N];
};

template<size_t N, size_t Precision = 1024>
class Mat {
 public:
  void repl_column(size_t i, const Vec<N, Precision>& v) {
    for (size_t row = 0; row < N; ++row) {
      mpfr_set(rows[row].coords[i], v.coords[row], MPFR_RNDN);
    }
  }
 public:
  Vec<N, Precision> rows[N];
};

ostream& operator << (ostream& os, mpfr_t m) {
  os << mpfr_get_flt(m, MPFR_RNDN);
  return os;
}

template<size_t N>
ostream& operator << (ostream& os, const Vec<N>& v) {
  os << "[" << v.float_at(0) << ", " << v.float_at(1) << ", " << v.float_at(2) << ", " << v.float_at(3) << "]";
  return os;
}

template<size_t N>
ostream& operator << (ostream& os, const Mat<N>& m) {
  for (size_t i = 0; i < N; ++i) {
    cout << m.rows[i] << endl;
  }
  return os;
}

typedef Vec<4> vec4;
typedef Mat<4> mat4;

vec4 operator* (const mat4& m, const vec4& v) {
  vec4 res;
  mpfr_t x;
  mpfr_init2(x, 1024);
  for (size_t i = 0; i < 4; ++i) {
    for (size_t j = 0; j < 4; ++j) {
      mpfr_mul(x, m.rows[i].coords[j], v.coords[j], MPFR_RNDN);
      mpfr_add(res.coords[i], res.coords[i], x, MPFR_RNDN);
    }
  }
  mpfr_clear(x);
  return res;
}

long stol(char* s) {
  long l;
  istringstream iss(s);
  iss >> l;
  return l;
}

void addmul4(mpfr_t res, mpfr_t x1, mpfr_t x2, mpfr_t x3, mpfr_t x4) {
  mpfr_t tmp;
  mpfr_init2(tmp, 1024);
  mpfr_set(tmp, x1, MPFR_RNDN);
  mpfr_mul(tmp, tmp, x2, MPFR_RNDN);
  mpfr_mul(tmp, tmp, x3, MPFR_RNDN);
  mpfr_mul(tmp, tmp, x4, MPFR_RNDN);
  mpfr_add(res, res, tmp, MPFR_RNDN);
  mpfr_clear(tmp);
}

void submul4(mpfr_t res, mpfr_t x1, mpfr_t x2, mpfr_t x3, mpfr_t x4) {
  mpfr_t tmp;
  mpfr_init2(tmp, 1024);
  mpfr_set(tmp, x1, MPFR_RNDN);
  mpfr_mul(tmp, tmp, x2, MPFR_RNDN);
  mpfr_mul(tmp, tmp, x3, MPFR_RNDN);
  mpfr_mul(tmp, tmp, x4, MPFR_RNDN);
  mpfr_sub(res, res, tmp, MPFR_RNDN);
  mpfr_clear(tmp);
}

void det(mpfr_t result, mat4& m) {
  mpfr_set_zero(result, MPFR_RNDN);
  addmul4(result, m.rows[0].coords[0],m.rows[1].coords[1],m.rows[2].coords[2],m.rows[3].coords[3]);
  addmul4(result, m.rows[0].coords[0],m.rows[1].coords[2],m.rows[2].coords[3],m.rows[3].coords[1]);
  addmul4(result, m.rows[0].coords[0],m.rows[2].coords[1],m.rows[3].coords[2],m.rows[1].coords[3]);
  submul4(result, m.rows[0].coords[0],m.rows[1].coords[3],m.rows[2].coords[2],m.rows[3].coords[1]);
  submul4(result, m.rows[0].coords[0],m.rows[1].coords[1],m.rows[3].coords[2],m.rows[2].coords[3]);
  submul4(result, m.rows[0].coords[0],m.rows[1].coords[2],m.rows[2].coords[1],m.rows[3].coords[3]);

  submul4(result, m.rows[1].coords[0],m.rows[0].coords[1],m.rows[2].coords[2],m.rows[3].coords[3]);
  submul4(result, m.rows[1].coords[0],m.rows[0].coords[2],m.rows[2].coords[3],m.rows[3].coords[1]);
  submul4(result, m.rows[1].coords[0],m.rows[2].coords[1],m.rows[3].coords[2],m.rows[0].coords[3]);
  addmul4(result, m.rows[1].coords[0],m.rows[0].coords[3],m.rows[2].coords[2],m.rows[3].coords[1]);
  addmul4(result, m.rows[1].coords[0],m.rows[0].coords[1],m.rows[3].coords[2],m.rows[2].coords[3]);
  addmul4(result, m.rows[1].coords[0],m.rows[0].coords[2],m.rows[2].coords[1],m.rows[3].coords[3]);

  addmul4(result, m.rows[2].coords[0],m.rows[0].coords[1],m.rows[1].coords[2],m.rows[3].coords[3]);
  addmul4(result, m.rows[2].coords[0],m.rows[0].coords[2],m.rows[1].coords[3],m.rows[3].coords[1]);
  addmul4(result, m.rows[2].coords[0],m.rows[1].coords[1],m.rows[3].coords[2],m.rows[0].coords[3]);
  submul4(result, m.rows[2].coords[0],m.rows[0].coords[3],m.rows[1].coords[2],m.rows[3].coords[1]);
  submul4(result, m.rows[2].coords[0],m.rows[1].coords[1],m.rows[0].coords[2],m.rows[3].coords[3]);
  submul4(result, m.rows[2].coords[0],m.rows[1].coords[3],m.rows[0].coords[1],m.rows[3].coords[2]);

  submul4(result, m.rows[3].coords[0],m.rows[0].coords[1],m.rows[1].coords[2],m.rows[2].coords[3]);
  submul4(result, m.rows[3].coords[0],m.rows[0].coords[3],m.rows[1].coords[1],m.rows[2].coords[2]);
  submul4(result, m.rows[3].coords[0],m.rows[2].coords[1],m.rows[0].coords[2],m.rows[1].coords[3]);
  addmul4(result, m.rows[3].coords[0],m.rows[0].coords[3],m.rows[1].coords[2],m.rows[2].coords[1]);
  addmul4(result, m.rows[3].coords[0],m.rows[1].coords[1],m.rows[0].coords[2],m.rows[2].coords[3]);
  addmul4(result, m.rows[3].coords[0],m.rows[0].coords[2],m.rows[1].coords[1],m.rows[2].coords[3]);
}

vec4 solve(mat4& m, const vec4& b) {
  vec4 res;
  mpfr_t d;
  mpfr_init2(d, 1024);
  det(d, m);
  //cout << "det=" << d << endl;
  for (size_t i = 0; i < 4; ++i) {
    mat4 mt = m;
    mt.repl_column(i, b);
    //cout << i << endl << mt << b << endl;
    det(res.coords[i], mt);
    //cout << "subdet " << i << " = "<< res.coords[i] << endl;
    mpfr_div(res.coords[i], res.coords[i], d, MPFR_RNDN);
    //cout << "subdet " << i << " = "<< res.coords[i] << endl;
  }
  mpfr_clear(d);
  return res;
}

mat4 complete_basis(const vec4& v) {
  mat4 res;
  vec4 dopvec, b, v0, v1, v2;
  dopvec.init(1, 1, 1, 1);
  b.init(0, 0, 0, 1);
  v0 = v;
  mpfr_set(v1.coords[2], v.coords[3], MPFR_RNDN);
  mpfr_set(v1.coords[3], v.coords[2], MPFR_RNDN);
  mpfr_mul_d(v1.coords[3], v1.coords[3], -1.0, MPFR_RNDN);
  mpfr_set(v2.coords[0], v.coords[1], MPFR_RNDN);
  mpfr_set(v2.coords[1], v.coords[0], MPFR_RNDN);
  mpfr_mul_d(v2.coords[0], v2.coords[0], -1.0, MPFR_RNDN);
  v0.normalize();
  v1.normalize();
  v2.normalize();
  mat4 mtx;
  mtx.rows[0] = v0;
  mtx.rows[1] = v1;
  mtx.rows[2] = v2;
  mtx.rows[3] = dopvec;
  vec4 v3 = solve(mtx, b);
  //cout << "mtx:\n"<< mtx << "v3: " << endl << v3 << endl;
  v3.normalize();
  res.rows[0] = v0;
  res.rows[1] = v1;
  res.rows[2] = v2;
  res.rows[3] = v3;
  return res;
}

int main (int argc, char** argv)
{
  if (argc != 5) {
    cerr << "Wrong number of args: got " << argc << ", should be 5" << endl;
    return 1;
  }
  vec4 maindir;
  maindir.init(stol(argv[1]), stol(argv[2]), stol(argv[3]), stol(argv[4]));
  mat4 basis = complete_basis(maindir);
  //cout << basis << endl;
  while (cin) {
    long x, y, z, w;
    cin >> x >> y >> z >> w;
    if (!cin) {
      break;
    }
    vec4 v;
    v.init(x, y, z, w);
    vec4 projected = basis * v;
    cout << mpfr_get_d(projected.coords[1], MPFR_RNDN) << "\t";
    cout << mpfr_get_d(projected.coords[2], MPFR_RNDN) << "\t";
    cout << mpfr_get_d(projected.coords[3], MPFR_RNDN) << endl;
  }
  //printf ("MPFR library: %-12s\nMPFR header:  %s (based on %d.%d.%d)\n",
  //mpfr_get_version(), MPFR_VERSION_STRING, MPFR_VERSION_MAJOR,
  //MPFR_VERSION_MINOR, MPFR_VERSION_PATCHLEVEL);
  mpfr_free_cache();
  return 0;
}
