#include <iostream>
#include <vector>
#include <cmath>
#include <cstdlib>

using namespace std;

class NeuralNetwork
{
public:
    vector<vector<double>> weights;
    vector<double> biases;

    NeuralNetwork(int inputSize, int outputSize)
    {
        for (int i = 0; i < inputSize; ++i)
        {
            vector<double> weightRow(outputSize);
            for (int j = 0; j < outputSize; ++j)
            {
                weightRow[j] = randWeight();
            }
            weights.push_back(weightRow);
        }
        for (int i = 0; i < outputSize; ++i)
        {
            biases.push_back(randWeight());
        }
    }

    vector<double> forward(const vector<double> &inputs)
    {
        vector<double> outputs(weights[0].size(), 0);
        for (size_t i = 0; i < weights[0].size(); ++i)
        {
            for (size_t j = 0; j < weights.size(); ++j)
            {
                outputs[i] += inputs[j] * weights[j][i];
            }
            outputs[i] += biases[i];
            outputs[i] = sigmoid(outputs[i]);
        }
        return outputs;
    }

private:
    double randWeight()
    {
        return (rand() / double(RAND_MAX)) * 2 - 1;
    }

    double sigmoid(double x)
    {
        return 1 / (1 + exp(-x));
    }
};

int main()
{
    NeuralNetwork nn(3, 2);
    vector<double> inputs = {0.5, -0.2, 0.1};
    vector<double> outputs = nn.forward(inputs);
    for (double o : outputs)
    {
        cout << o << " ";
    }
    cout << endl;
    return 0;
}
