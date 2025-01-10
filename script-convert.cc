#include <iostream>
#include <cstdlib>
#include <cmath>

using namespace std;

// asymmetric

int main(int argc, char *argv[])
{
    if (argc != 5)
    {
        cout << "Usage: " << argv[0] << " <og_start> <og_end> <new_start> <new_end>" << endl;
        return 1;
    }

    int og_start = atoi(argv[1]);
    int og_end = atoi(argv[2]);
    int new_start = atoi(argv[3]);
    int new_end = atoi(argv[4]);

    if (new_end == new_start)
    {
        cout << "Error: Division by zero." << endl;
        return 1;
    }

    int scaled_value = (og_start - og_end) / (new_start - new_end);

    cout << "Scaled Value: " << scaled_value << endl;
    int zero_point = (scaled_value * new_start) - og_start;

    int x;
    while (cin >> x)
    {
        round(scaled_value * x + zero_point);
    }

    return 0;
}
