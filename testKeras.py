from keras.models import Sequential

from keras.layers import Dense


couche_milieu = Dense(units=9, activation='sigmoid')
morpion = Sequential()
morpion.add(Dense(units=9, activation='relu', input_dim=2))
morpion.add(couche_milieu)
morpion.add(couche_milieu)
morpion.add(couche_milieu)
morpion.add(couche_milieu)
morpion.add(couche_milieu)
morpion.add(couche_milieu)
morpion.add(couche_milieu)
morpion.add(couche_milieu)
morpion.add(Dense(units=1, activation='linear'))

morpion.compile(optimizer='sgd', loss='mse', metrics=['accuracy'])

morpion.fit(10, 10, verbose=2, epochs=10, batch_size=20)
