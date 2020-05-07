#include <iostream>
#include <array>
#include <string>
using namespace std;

array<char,128> dvorak_to_qwerty_map() {
  const char* qwerty = "-=qwertyuiop[]asdfghjkl;'zxcvbnm,./_+QWERTYUIOP{}ASDFGHJKL:\"ZXCVBNM<>?";
  const char* dvorak = "[]',.pyfgcrl/=aoeuidhtns-;qjkxbmwvz{}\"<>PYFGCRL?+AOEUIDHTNS_:QJKXBMWVZ";
  array<char,128> map;
  map.fill('\0');
  const char* ptr = dvorak;
  while (*ptr != '\0') {
    map[*ptr] = qwerty[ptr-dvorak];
    ++ptr;
  }
  return map;
}

void decypher(string& text, const array<char,128>& map) {
  for (char& c : text) {
    if (map[c] != '\0')
      c = map[c];
  }
}

int main() {
  auto char_map = dvorak_to_qwerty_map();
  int N;
  cin >> N; cin.ignore();
  for (int i = 1; i <= N; ++i) {
    string line;
    getline(cin, line);
    decypher(line, char_map);
    cout << "Case #" << i << ": " << line << endl;
  }
}

