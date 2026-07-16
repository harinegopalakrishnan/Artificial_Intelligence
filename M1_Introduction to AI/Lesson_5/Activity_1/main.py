# 1. Import necessary Libraries
import tensorflow as tf
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt

# 2. Load the MNIST Dataset
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

# 3. Normalize the data
x_train, x_test = x_train / 255.0, x_test / 255.0

# 4. Build the model
model = models.Sequential([
    layers.Flatten(input_shape=(28, 28)), #(28 * 28 = 784)
    layers.Dense(128, activation='relu'), #fully connected layer with 128 neurons
    layers.Dense(10, activation='softmax') #fully connected layer with 10 neurons representing a possible digit (0-9)
])

# 5. Compile the model

model.compile(
    optimizer='adam', #Adaptive Moment Estimation
    loss='sparse_categorical_crossentropy', #loss function measures how well the model is performing.
    metrics=['accuracy'] # model will track accuracy
)

# 6.Train the model
'''
x_train: The training images.
y_train: The corresponding labels (digits) for the training images.
epochs: The number of times the model will train on specific dataset
'''
model.fit(x_train, y_train, epochs=5)

# 7. Evaluate the model

test_loss, test_acc = model.evaluate(x_test, y_test)

print(f"Test accuracy: {test_acc}")

# 8. Make Predictions

predictions = model.predict(x_test)

# 9. Display the First Image and Prediction

plt.imshow(x_test[0], cmap=plt.cm.binary)

plt.title(f"Predicted: {predictions[0].argmax()}")

plt.show()