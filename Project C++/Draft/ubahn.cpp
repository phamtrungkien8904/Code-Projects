#include <bits/stdc++.h>
using namespace std;

int NO_PARENT = -1;

map<int, string> station = {
    {0, "Hauptbahnhof"},
    {1, "Sendlinger Tor"},
    {2, "Marienplatz"},
    {3, "Odeonsplatz"},
    {4, "Münchner Freiheit"},
    {5, "Universität"},
    {6, "Moosach"},
    {7, "Olympia-Einkaufszentrum"},
    {8, "Scheidplatz"}
};

void collectPath(int currentVertex, vector<int> parents, vector<string>& path)
{
    if (currentVertex == NO_PARENT) {
        return;
    }
    collectPath(parents[currentVertex], parents, path);
    path.push_back(station[currentVertex]);
}

void printSolution(int startVertex, int vertexIndex, vector<int> distances, vector<int> parents)
{
    int nVertices = distances.size();

    if (vertexIndex != startVertex) {
        cout << "\nRoute: " << station[startVertex] << " -> " << station[vertexIndex] << endl;
        cout << "Reisedauer(min.): " << distances[vertexIndex] << endl;

        vector<string> path;
        collectPath(vertexIndex, parents, path);

        cout << "Routenverlauf: ";
        for (size_t i = 0; i < path.size(); ++i) {
            cout << path[i];
            if (i != path.size() - 1) {
                cout << " -> ";
            }
        }
        cout << endl;
    }
}

// Function that implements Dijkstra's
// single source shortest path
// algorithm for a graph represented
// using adjacency matrix
// representation

void dijkstra(vector<vector<int> > adjacencyMatrix,
			int startVertex, int vertexIndex)
{
	int nVertices = adjacencyMatrix[0].size();

	// shortestDistances[i] will hold the
	// shortest distance from src to i
	vector<int> shortestDistances(nVertices);

	// added[i] will true if vertex i is
	// included / in shortest path tree
	// or shortest distance from src to
	// i is finalized
	vector<bool> added(nVertices);

	// Initialize all distances as
	// INFINITE and added[] as false
	for (int vertexIndex = 0; vertexIndex < nVertices;
		vertexIndex++) {
		shortestDistances[vertexIndex] = INT_MAX;
		added[vertexIndex] = false;
	}

	// Distance of source vertex from
	// itself is always 0
	shortestDistances[startVertex] = 0;

	// Parent array to store shortest
	// path tree
	vector<int> parents(nVertices);

	// The starting vertex does not
	// have a parent
	parents[startVertex] = NO_PARENT;

	// Find shortest path for all
	// vertices
	for (int i = 1; i < nVertices; i++) {

		// Pick the minimum distance vertex
		// from the set of vertices not yet
		// processed. nearestVertex is
		// always equal to startNode in
		// first iteration.
		int nearestVertex = -1;
		int shortestDistance = INT_MAX;
		for (int vertexIndex = 0; vertexIndex < nVertices;
			vertexIndex++) {
			if (!added[vertexIndex]
				&& shortestDistances[vertexIndex]
					< shortestDistance) {
				nearestVertex = vertexIndex;
				shortestDistance
					= shortestDistances[vertexIndex];
			}
		}

		// Mark the picked vertex as
		// processed
		added[nearestVertex] = true;

		// Update dist value of the
		// adjacent vertices of the
		// picked vertex.
		for (int vertexIndex = 0; vertexIndex < nVertices;
			vertexIndex++) {
			int edgeDistance
				= adjacencyMatrix[nearestVertex]
								[vertexIndex];

			if (edgeDistance > 0
				&& ((shortestDistance + edgeDistance)
					< shortestDistances[vertexIndex])) {
				parents[vertexIndex] = nearestVertex;
				shortestDistances[vertexIndex]
					= shortestDistance + edgeDistance;
			}
		}
	}

	printSolution(startVertex, vertexIndex , shortestDistances, parents);
}

// Driver Code
int main()
{
	vector<vector<int> > adjacencyMatrix
		= { { 0, 2, 0, 4, 0, 0, 0, 14, 10 },
			{ 2, 0, 2, 4, 10, 6, 26, 22, 14 },
			{ 0, 2, 0, 2, 8, 4, 24, 20, 12  },
			{ 4, 4, 2, 0, 6, 2, 22, 18, 10 },
			{ 0, 10, 8, 6, 0, 4, 16, 12, 4 },
			{ 0, 6, 4, 2, 4, 0, 20, 16, 8  },
			{ 0, 26, 24, 22, 16, 20, 0, 4, 12 },
			{ 14, 16, 20, 18, 12, 16, 2, 0, 12 },
			{ 10, 12, 12, 10, 4, 8, 12, 8, 0 } };
    cout << "U-Bahn München" << endl;
    cout << "Stationen: " << endl;
    for (auto it = station.begin(); it != station.end(); ++it) {
        cout << it->first << ": " << it->second << endl;
    }
    cout << endl;
    cout << "Verbindungen (Bitte Nummer eingeben): " << endl;
    int s;
    cout << "Startstation: ";
    cin >> s;
	int e;
	cout << "Zielstation: ";
	cin >> e;
	dijkstra(adjacencyMatrix, s, e);
    cout << endl;
	return 0;
}