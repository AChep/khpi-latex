import numpy as np

from pathlib import Path
from keras.models import Sequential
from keras.layers import Dense

rock = [1, 0, 0]
paper = [0, 1, 0]
scissors = [0, 0, 1]


class Forecast:

    def __init__(self, tail_size):
        self.tail = rock * tail_size

        self.model = Sequential()
        self.model.add(Dense(32, input_shape=(tail_size * 3,)))
        self.model.add(Dense(64))
        self.model.add(Dense(3, activation='sigmoid'))
        self.model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    def train(self, x, epochs=1):
        self.model.fit(np.array([self.tail]), np.array([x]), epochs=epochs, verbose=0)

        # Add this move to a tail.
        self.tail = self.tail[3:]
        self.tail.extend(x)

    def predict(self):
        x_prediction = self.model.predict(np.array([self.tail]))[0]
        x_prediction_max = max(x_prediction)
        return [1 if abs(x_prediction_max - e) <= 0.001 else 0 for e in x_prediction]


def get_object(obj):
    if obj == "r":
        return rock
    elif obj == "p":
        return paper
    elif obj == "s":
        return scissors
    return scissors


def get_object_counter(obj):
    if obj[0] == 1:  # rock
        return paper
    elif obj[1] == 1:  # paper
        return scissors
    elif obj[2] == 1:  # scissors
        return rock
    raise RuntimeError()


forecast = Forecast(7)

# Train the model on a
# sample data.
train = Path('data.txt').read_text().splitlines()
for line in train:
    if len(line) != 2:
        continue

    x = get_object(line[0])
    forecast.train(x)

# Play!
user_won_counter = 0
computer_won_counter = 0

while True:
    x = get_object(input("Enter your move: "))
    y = get_object_counter(forecast.predict())
    forecast.train(x, 10)

    t = get_object_counter(x)
    if y == t:
        computer_won_counter += 1
        print("Computer won!")
    elif y == x:
        print("Draw!")
    else:
        user_won_counter += 1
        print("User won!")
    print("User: %s, Computer: %s" % (user_won_counter, computer_won_counter))
