#include <cassert>
#include <iostream>
#include <map>
#include <tuple>
#include <algorithm>
#include <vector>
using namespace std;

typedef vector<vector<int>> Graph;

void InsertEdge(Graph& graph, int u, int v) {
  int max_uv = max(u, v);
  if (graph.size() <= max_uv) {
    graph.resize(max_uv+1);
  }
  graph[u].push_back(v);
}

vector<int> CalculateInDegree(const Graph& graph) {
  vector<int> in_degree(graph.size());
  for (int u = 0; u < graph.size(); ++u) {
    for (int v : graph[u]) {
      in_degree[v] += 1;
    }
  }
  return in_degree;
}

int main() {
  int C;
  cin >> C;
  for (int i = 1; i <= C; ++i) {
    int N;
    cin >> N;
    // graph will contain an edge (u,v) if player u is better than player v
    Graph graph;
    for (int game = 0; game < N; ++game) {
      int A, B, R;
      cin >> A >> B >> R;
      if (R)
        InsertEdge(graph, A-1, B-1);
      else
        InsertEdge(graph, B-1, A-1);
    }
    // it's not necessary to compute full topological sorting
    auto in_degree = CalculateInDegree(graph);
    // find the (hopefully) only player with 0 input degree
    auto it = find(in_degree.begin(), in_degree.end(), 0);
    // the following shouldn't happen as per the precondition, still let's make
    // sure to catch errors in code
    assert(it != in_degree.end() and "couldn't find best player");
    int best_player = it + 1 - in_degree.begin();
    // a simple sanity check (again, the following shouldn't happen as per
    // the precondition)
    assert(find(it+1, in_degree.end(), 0) == in_degree.end() and "solution is not unique");
    cout << "Case #" << i << ": " << best_player << endl;
  }
}



