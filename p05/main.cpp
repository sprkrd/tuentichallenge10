#include <iostream>
#include <cstdint>
using namespace std;


int main() {
  int C;
  cin >> C;
  for (int i = 1; i <= C; ++i) {
    uint64_t N;
    cin >> N;
    uint64_t n_twenties = N/20;
    uint64_t rem = N%20;
    cout << "Case #" << i << ": ";
    // check if the remainder can be distributed among the twenties without
    // exceeding 29 in any of them
    if (n_twenties and rem/n_twenties + (rem%n_twenties? 1 : 0) < 10) {
      cout << n_twenties << endl;
    }
    else {
      cout << "IMPOSSIBLE" << endl;
    }
  }
}



