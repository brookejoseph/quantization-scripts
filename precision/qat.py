import tensorflow as tf
from tensorflow.keras import layers, models
import tensorflow_model_optimization as tfmot
import numpy as np
import matplotlib.pyplot as plt

# Step 1: Generate Synthetic Data
def generate_data(samples=1000):
    X = np.random.rand(samples, 2) * 2 - 1  # Random values in [-1, 1]
    y = (X[:, 0] * X[:, 1] > 0).astype(int)  # XOR-like classification
    return X, y

X_train, y_train = generate_data(1000)
X_test, y_test = generate_data(200)

# Step 2: Define a Floating Point Model
def create_model():
    model = models.Sequential([
        layers.Input(shape=(2,)),
        layers.Dense(16, activation='relu'),
        layers.Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

float_model = create_model()

# Step 3: Train the Model
float_model.fit(X_train, y_train, epochs=10, batch_size=32, verbose=0)
float_model.evaluate(X_test, y_test, verbose=1)

# Step 4: Apply Quantization Aware Training (QAT)
quant_aware_model = tfmot.quantization.keras.quantize_model(float_model)

quant_aware_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Step 5: Train the QAT Model
quant_aware_model.fit(X_train, y_train, epochs=10, batch_size=32, verbose=0)
qat_accuracy = quant_aware_model.evaluate(X_test, y_test, verbose=1)[1]

# Step 6: Convert to a Fully Quantized Model
converter = tf.lite.TFLiteConverter.from_keras_model(quant_aware_model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
quantized_tflite_model = converter.convert()

# Save the quantized model
with open('quantized_model.tflite', 'wb') as f:
    f.write(quantized_tflite_model)

# Step 7: Evaluate the Quantized Model
interpreter = tf.lite.Interpreter(model_content=quantized_tflite_model)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

def evaluate_tflite_model(interpreter, X, y):
    correct = 0
    for i in range(len(X)):
        input_data = np.expand_dims(X[i], axis=0).astype(np.float32)
        interpreter.set_tensor(input_details[0]['index'], input_data)
        interpreter.invoke()
        prediction = interpreter.get_tensor(output_details[0]['index'])
        correct += (prediction > 0.5) == y[i]
    return correct / len(X)

quantized_accuracy = evaluate_tflite_model(interpreter, X_test, y_test)

# Step 8: Visualize Accuracy Comparison
methods = ['Floating Point Model', 'Quantization Aware Model', 'Quantized Model']
accuracies = [float_model.evaluate(X_test, y_test, verbose=0)[1], qat_accuracy, quantized_accuracy]

plt.figure(figsize=(8, 5))
plt.bar(methods, accuracies, color=['blue', 'green', 'orange'])
plt.ylim(0, 1)
plt.title('Model Accuracy Comparison')
plt.ylabel('Accuracy')
plt.xlabel('Model Type')
plt.show()
