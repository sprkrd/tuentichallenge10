#include <iostream>
#include <set>
#include <vector>
#include <string>
#include <sstream>
using namespace std;


/*
 *
 * O = {o_0, o_1, ..., o_{M-1}}: set of AVAILABLE operators (o_i < o_{i+1})
 *
 * C(x,i): "number of ways of summing x with operands {o_i, o_{i+1}, ..., O_{M-1}}
 *
 * if x = 0: C(x,*) = 1
 * if x > 0 and o_i > x: C(x,i) = 0
 * if o_i <= x and i < M-1: C(x,i) = C(x-o_i,i) + C(x, i+1)
 * if o_i <= x and i = M-1: C(x,M-1) = C(x-o_i,M-1)
 *
 */


int number_of_sums(int X, const vector<int>& O) {
  // Dynamic programming. Complexity: O(X*|O|)
  int M = O.size();
  vector<vector<int>> C(X+1, vector<int>(M));

  for (int i = 0; i < M; ++i) {
    C[0][i] = 1; // base case 1: C(0,*) = 1
  }

  for (int x = 1; x <= X; ++x) {
    for (int i = M-1; i >= 0; --i) {
      if (O[i] > x) C[x][i] = 0; // base case 2: C(x,i) = 0 if x > 0 and o_i > x
      else {
        C[x][i] = C[x-O[i]][i];
        if (i < M-1) C[x][i] += C[x][i+1];
      }
    }
  }

  return C[X][0] - 1; // we have to account only for the "proper" sums, so
                      // we subtract 1 (i.e. avoid the 1-operand trivial "sum")
}

int main() {
  int T;
  cin >> T; cin.ignore();
  for (int i = 1; i <= T; ++i) {
    string line;
    getline(cin, line);
    istringstream in(line);
    int X, N;
    in >> X;
    set<int> O;
    for (int o = 1; o <= X; ++o) O.insert(o);
    while (in >> N)
      O.erase(N);
    
    int S = number_of_sums(X, vector<int>(O.begin(), O.end()));
    cout << "Case #" << i << ": " << S << endl;
  }
}

