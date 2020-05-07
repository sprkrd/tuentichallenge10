#include <iostream>
#include <iomanip>
#include <map>
#include <vector>
#include <tuple>
#include <archive.h>
#include <archive_entry.h>
#include <zlib.h>
#include <cstdint>
using namespace std;

// We'll use the fact that the given files are composed entirely by zeros
// (otherwise we would be having a very rough time decompressing the
// +200GB files, even if we do it chunk by chunk) and after the insertions the
// resulting files will be very sparse, so we have to combine the CRCs of spare
// bytes with long strings of 0s.

// I'll use zlib's CRC32 function. zlib also has the very useful crc32_combine
// function, which is not trivial to implement since CRC32 is not additive (only
// pure mathematical CRC is). Since I'm writing the solution in C++,
// I use the libarchive library for easily handling the .tar.gz file (I only
// need to read the entries and their sizes).

// For this one I did a fair bit of research that was not necessarily
// useful for this program. Some interesting reads (for future me):
// https://stackoverflow.com/questions/23122312/crc-calculation-of-a-mostly-static-data-stream/23126768#23126768
// https://stackoverflow.com/questions/38670483/what-is-the-inverse-of-crc32-combines-matrix-trick
// https://stackoverflow.com/questions/2423866/python-decompressing-gzip-chunk-by-chunk (not used here, but I'd may need this in the future)


map<string, size_t> GetFileSizes() {
  const char* archive_filename = "animals.tar.gz";
  struct archive* a;
  struct archive_entry* entry;
  int r;
  a = archive_read_new();
  archive_read_support_filter_all(a);
  archive_read_support_format_all(a);
  r = archive_read_open_filename(a, archive_filename, 10240);
  if (r != ARCHIVE_OK) {
    exit(1);
  }
  map<string, size_t> map_to_sizes;
  while (archive_read_next_header(a, &entry) == ARCHIVE_OK) {
    string entry_name = string(archive_entry_pathname(entry));
    if (entry_name != "animals/./") {
      entry_name = entry_name.substr(10);
      map_to_sizes.insert({entry_name, archive_entry_size(entry)});
    }
  }
  r = archive_read_free(a);
  if (r != ARCHIVE_OK) {
    exit(1);
  }
  return map_to_sizes;
}

auto file_to_size = GetFileSizes();

uint32_t NextCRC(uint32_t current_crc) {
  Bytef c = 0;
  return (uint32_t)crc32(current_crc, &c, 1);
}

uint32_t CalculateZeroStringCRC(uint64_t string_size) {
  if (string_size == 0) return 0;
  uint32_t crc_half = CalculateZeroStringCRC(string_size/2);
  uint32_t result = crc32_combine(crc_half, crc_half, string_size/2);
  if (string_size%2) result = NextCRC(result);
  return result;
}

typedef tuple<uint64_t,unsigned char> LocationAndByte;

void Insert(vector<LocationAndByte>& bytes, const LocationAndByte& addition) {
  // find insertion position
  int i = bytes.size();
  while (i > 0 and get<0>(bytes[i-1]) >= get<0>(addition)) {
    --i;
  }
  auto it = bytes.insert(bytes.begin()+i, addition);
  //increase index of bytes that come after (now they've been shifted to the right)
  while (++it < bytes.end()) {
    get<0>(*it) += 1;
  }
}

uint32_t CalculateCRC32(const string& filename, const vector<LocationAndByte>& additions) {
  vector<LocationAndByte> bytes;
  bytes.reserve(additions.size());
  for (const auto& addition : additions) {
    Insert(bytes, addition);
  }
  uint32_t result = 0;
  uint64_t remaining_zeroes = file_to_size.find(filename)->second;
  for (unsigned i = 0; i < bytes.size(); ++i) {
    auto[pos, byte] = bytes[i];
    uint64_t skipped_zeroes = pos;
    if (i > 0) skipped_zeroes -= get<0>(bytes[i-1])+1;
    remaining_zeroes -= skipped_zeroes;
    result = crc32_combine(result, CalculateZeroStringCRC(skipped_zeroes), skipped_zeroes);
    result = crc32(result, &byte, 1);
  }
  result = crc32_combine(result, CalculateZeroStringCRC(remaining_zeroes), remaining_zeroes);
  return result;
}

int main() {
  string filename;
  unsigned n_additions;
  while (cin >> filename >> n_additions) {
    vector<LocationAndByte> additions;
    vector<uint32_t> crc32s{CalculateCRC32(filename, additions)};
    additions.reserve(n_additions);
    crc32s.reserve(n_additions+1);
    while (additions.size() != n_additions) {
      uint64_t pos;
      int byte;
      cin >> pos >> byte;
      additions.emplace_back(pos, (unsigned char)byte);
      crc32s.push_back(CalculateCRC32(filename, additions));
    }
    for (unsigned i = 0; i <= n_additions; ++i) {
      cout << filename << ' ' << dec << i << ": " << setfill('0') << setw(8) << hex << crc32s[i] << endl;
    }
  }
}

