#include <iostream>
#include <map>
#include <tuple>
using namespace std;

map<tuple<char,char>,char> win_table{
  {{'P','P'},'-'}, {{'P','S'},'S'}, {{'P','R'},'P'},
  {{'S','P'},'S'}, {{'S','S'},'-'}, {{'S','R'},'R'},
  {{'R','P'},'P'}, {{'R','S'},'R'}, {{'R','R'},'-'}
};

int main() {
  int N;
  cin >> N;
  for (int i = 1; i <= N; ++i) {
    char l, r;
    cin >> l >> r;
    cout << "Case #" << i << ": " << win_table[{l,r}] << endl;
  }
}



