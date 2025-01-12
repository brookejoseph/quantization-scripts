#include <iostream>
#include <vector>
#include <cmath>
#include <cstdlib>

using namespace std;

class NeuralNetwork
{
public:
    vector<vector<int>> quantized_weights;
    vector<int> quantized_biases;
    double scale_factor;
    int zero_point;

    NeuralNetwork(int inputSize, int outputSize, int og_start, int og_end, int new_start, int new_end)
    {
        scale_factor = (double)(new_start - new_end) / (og_start - og_end);
        zero_point = new_start - round(scale_factor * og_start);

        for (int i = 0; i < inputSize; ++i)
        {
            vector<int> weightRow(outputSize);
            for (int j = 0; j < outputSize; ++j)
            {
                double randWeight = randomWeight();
                weightRow[j] = quantize(randWeight);
            }
            quantized_weights.push_back(weightRow);
        }
        for (int i = 0; i < outputSize; ++i)
        {
            double randBias = randomWeight();
            quantized_biases.push_back(quantize(randBias));
        }
    }

    vector<int> forward(const vector<int> &inputs)
    {
        vector<int> outputs(quantized_weights[0].size(), 0);
        for (size_t i = 0; i < quantized_weights[0].size(); ++i)
        {
            for (size_t j = 0; j < quantized_weights.size(); ++j)
            {
                outputs[i] += inputs[j] * quantized_weights[j][i];
            }
            outputs[i] += quantized_biases[i];
        }
        return outputs;
    }

private:
    double randomWeight()
    {
        return (rand() / double(RAND_MAX)) * 2 - 1;
    }

    int quantize(double value)
    {
        return round(value * scale_factor + zero_point);
    }
};

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

    NeuralNetwork nn(3, 2, og_start, og_end, new_start, new_end);

    vector<int> inputs = {127, -64, 32};
    vector<int> outputs = nn.forward(inputs);

    for (int o : outputs)
    {
        cout << o << " ";
    }
    cout << endl;

    void plotGraph(const vector<int> &data, const string &label)
    {
        vector<int> x(data.size());
        for (size_t i = 0; i < data.size(); ++i)
        {
            x[i] = i;
        };
        plt::bar(x, data);
        plt::title(label);
        plt::show();
    };

    return 0;
}
