#include <iostream>
#include <cstdint>
#include <vector>
#include <cmath>
#include <tuple>
using namespace std;

uint64_t CalculateNumberOfPacks(uint64_t H_0, uint64_t W_0, uint64_t D_0) {
  // Calculates the number of packs in a fortress whose tower dimensions are
  // H_0 (height), W_0 (width) and D_0 (depth).
  // Yeah, sure, probably there's a polynomial formula for this, but I don't
  // have time to figure it out right now. The iterative algorithm isn't
  // bad (linear in H, and H is gonna be less than 2^21 because otherwise
  // the number of packs would exceed 2^62).
  uint64_t C_i = 2*(W_0+D_0)-4;
  uint64_t n_packs_i = H_0*W_0*D_0;
  uint64_t last_layer = 2*H_0 - 3;
  for (uint64_t i = 1; i <= last_layer; ++i) {
    C_i = C_i + 8;
    uint64_t H_i = H_0 - (6*(i%2) + 2*i)/4;
    n_packs_i += C_i*H_i;
  }
  return n_packs_i;
}


tuple<uint64_t, uint64_t> BinarySearchH(uint64_t n_packages) {
  // Find max height of tower hx1x1 so the number of packs doesn't exceed
  // n_packages. Returns both h and the number of packs.
  uint64_t l = 3;
  uint64_t r = 1ULL<<21;
  while (l <= r) {
    uint64_t m = (l+r)/2;
    uint64_t pack_m = CalculateNumberOfPacks(m, 1, 1);
    if (pack_m < n_packages) {
      l = m+1;
    } else if (pack_m > n_packages) {
      r = m-1;
    } else {
      return {m, pack_m};
    }
  }
  return {r, CalculateNumberOfPacks(r, 1, 1)};
}

tuple<uint64_t, uint64_t, uint64_t> BinarySearchWD(uint64_t n_packages, uint64_t h) {
  // Find W,D (given H) of tower so the number of packs doesn't exceed
  // n_packages. Returns W, D, and the number of packs.
  uint64_t l = 1;
  uint64_t r = sqrt(n_packages/h);
  uint64_t n_packs = 0;
  uint64_t w = 0;
  uint64_t d = 0;
  while (l <= r) {
    uint64_t m = (l+r)/2;
    uint64_t pack_m = CalculateNumberOfPacks(h, m, m);
    if (pack_m < n_packages) {
      l = m+1;
    } else if (pack_m > n_packages) {
      r = m-1;
    } else {
      w = d = m;
      n_packs = pack_m;
      break;
    }
  }
  if (w == 0) {
    w = d = r;
    n_packs = CalculateNumberOfPacks(h, w, d);
  }
  // Find out for the case in which D = W + 1
  uint64_t pack_w_d_plus_1 = CalculateNumberOfPacks(h, w, d+1);
  if (pack_w_d_plus_1 <= n_packages) {
    d = d+1;
    n_packs = pack_w_d_plus_1;
  }
  return {w, d, n_packs};
}


int main() {
  int C;
  cin >> C;
  for (int i = 1; i <= C; ++i) {
    uint64_t P;
    cin >> P;
    auto[H, n_packs_h_1_1] = BinarySearchH(P);
    if (H >= 3) {
      auto[W, D, n_packs_max] = BinarySearchWD(P, H);
      // some debugging information that I find useful (helps documenting the
      // algorithm too).
      cerr << "Case #" << i << " (" << P << " packs available)\n"
           << "  Max height of fortress = " << H << " (#packs if dimensions are 1x1 = " << n_packs_h_1_1 << ")\n"
           << "  A fortress of height " << (H+1) << " would have " << CalculateNumberOfPacks(H+1, 1, 1) << " packs\n"
           << "  Max tower size " << W << "x" << D << "(#packs = " << n_packs_max << ")" << '\n'
           << "  A slightly larger tower (" << (W+(D>W)) << "x" << (D+(D==W)) << ") would have " << CalculateNumberOfPacks(H, W+(W<D), D+(D==W)) << " packs\n";
      // the information that is actually requested.
      cout << "Case #" << i << ": " << H << ' ' << n_packs_max << endl;
    } else {
      cerr << "Case #" << i << ": IMPOSSIBLE (#packs = " << P << "<43. 43 is the minimum to form a fortress)" << endl;
      cout << "Case #" << i << ": IMPOSSIBLE" << endl;
    }
  }
}



