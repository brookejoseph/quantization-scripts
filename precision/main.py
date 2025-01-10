import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

def generate_data(samples=1000):
    X = np.random.rand(samples, 2) * 2 - 1  # Random values in [-1, 1]
    y = (X[:, 0] * X[:, 1] > 0).astype(int) 
    return X, y

def create_model():
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(16, activation='relu', input_shape=(2,)),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

X_train, y_train = generate_data(1000)
X_test, y_test = generate_data(200)

model = create_model()
model.fit(X_train, y_train, epochs=10, batch_size=32, verbose=0)
original_accuracy = model.evaluate(X_test, y_test, verbose=0)[1]

def quantize_weights(weights, scale_factor, zero_point=0):
    quantized = [
        (np.round(w / scale_factor) + zero_point).astype(np.int8)
        for w in weights
    ]
    return quantized

def dequantize_weights(quantized_weights, scale_factor, zero_point=0):
    dequantized = [(w - zero_point) * scale_factor for w in quantized_weights]
    return dequantized

original_weights = model.get_weights()

symmetric_scale = max(abs(w).max() for w in original_weights if w.ndim > 0) / 127
symmetric_quantized = quantize_weights(original_weights, symmetric_scale)
symmetric_dequantized = dequantize_weights(symmetric_quantized, symmetric_scale)

asymmetric_scale = (original_weights[0].max() - original_weights[0].min()) / 255
asymmetric_zero_point = -np.round(original_weights[0].min() / asymmetric_scale)
asymmetric_quantized = quantize_weights(original_weights, asymmetric_scale, asymmetric_zero_point)
asymmetric_dequantized = dequantize_weights(asymmetric_quantized, asymmetric_scale, asymmetric_zero_point)

symmetric_model = create_model()
symmetric_model.set_weights(symmetric_dequantized)
symmetric_accuracy = symmetric_model.evaluate(X_test, y_test, verbose=0)[1]

asymmetric_model = create_model()
asymmetric_model.set_weights(asymmetric_dequantized)
asymmetric_accuracy = asymmetric_model.evaluate(X_test, y_test, verbose=0)[1]

methods = ['Original', 'Symmetric Quantization', 'Asymmetric Quantization']
accuracies = [original_accuracy, symmetric_accuracy, asymmetric_accuracy]

plt.figure(figsize=(8, 5))
plt.bar(methods, accuracies, color=['blue', 'green', 'orange'])
plt.ylim(0, 1)
plt.title('Model Accuracy Comparison')
plt.ylabel('Accuracy')
plt.xlabel('Quantization Method')
plt.show()