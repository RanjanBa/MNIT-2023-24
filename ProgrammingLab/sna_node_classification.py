import pandas as pd
import os
import numpy as np

import tensorflow as tf
import stellargraph as sg
import stellargraph.datasets as sg_data
from stellargraph.mapper import FullBatchNodeGenerator
from stellargraph.layer import GCN

from tensorflow.keras import layers, optimizers, losses, metrics, Model
from sklearn import preprocessing, model_selection
from IPython.display import display, HTML
import matplotlib.pyplot as plt
from tensorflow.keras.callbacks import EarlyStopping


# Load the CiteSeet dataset
dataset = sg_data.CiteSeer()
G, node_subjects = dataset.load()
type(G), type(node_subjects), node_subjects.shape

train_subjects, test_subjects = model_selection.train_test_split(
    node_subjects, train_size=500, test_size=None, stratify=node_subjects
)
val_subjects, test_subjects = model_selection.train_test_split(
    test_subjects, train_size=500, test_size=None, stratify=test_subjects
)

train_subjects.shape, val_subjects.shape, test_subjects.shape

# Encode target labels
target_encoding = preprocessing.LabelBinarizer()
train_targets = target_encoding.fit_transform(train_subjects)
val_targets = target_encoding.transform(val_subjects)
test_targets = target_encoding.transform(test_subjects)


# Create a FullBatchNodeGenerator
generator = FullBatchNodeGenerator(G, method="gcn")

# Create the GCN model with increased layer sizes and reduced dropout
gcn = GCN(
    layer_sizes=[16, 16, 16],
    activations=["relu", "relu", "relu"],
    generator=generator,
    dropout=0.8,  # Adjusted dropout value
)

x_inp, x_out = gcn.in_out_tensors()

# Use a more complex model architecture with additional Dense layers
x_out = layers.BatchNormalization()(x_out) 

# Output layer with softmax activation
predictions = layers.Dense(units=train_targets.shape[1], activation="softmax")(x_out)

# Create and compile the model
model = Model(inputs=x_inp, outputs=predictions)
model.compile(
    optimizer=optimizers.Adam(learning_rate=0.01),
    loss=losses.categorical_crossentropy,
    metrics=["acc"],
)

# Create validation and test data generators
val_gen = generator.flow(val_subjects.index, val_targets)
test_gen = generator.flow(test_subjects.index, test_targets)

# Create the training data generator
train_gen = generator.flow(train_subjects.index, train_targets)

# Use EarlyStopping with 'val_loss' as the monitored metric
es_callback = EarlyStopping(monitor="val_loss", patience=50, restore_best_weights=True)

# Train the model
history = model.fit(
    train_gen,
    epochs=300,
    validation_data=val_gen,
    # verbose=1,
    shuffle=False,
    callbacks=[es_callback],
)