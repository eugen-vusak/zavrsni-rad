import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patheffects as PathEffects
import numpy as np
from sklearn.manifold import TSNE

np.set_printoptions(threshold=np.nan)


FILE_NAME = "/home/euzenmendenzien/Documents/Gamayun/2.0/\
Data/all_data.csv"

NUMBER_OF_TIMESTEPS = 60
DEGREES_OF_FREEDOM = 6
OUTPUT_SIZE = 1

df = pd.read_csv(FILE_NAME, header=None)

df.set_index(df.columns[0].tolist(), inplace=True)

# print(df.head())

df.iloc[:, 0::6] /= 2**15 * 2
df.iloc[:, 1::6] /= 2**15 * 2
df.iloc[:, 2::6] /= 2**15 * 2
df.iloc[:, 3::6] /= 2**15 * 500
df.iloc[:, 4::6] /= 2**15 * 500
df.iloc[:, 5::6] /= 2**15 * 500

# print(df.head())
# exit()

x = df.values
y = df.index.values

tsne = TSNE(n_components=2, verbose=0, random_state=0)

rez = tsne.fit_transform(x)
# print(len(rez))
with pd.option_context('display.max_rows', None, 'display.max_columns', 3):
    print(rez)

# exit()
gestures = [
    "UP",
    "DOWN",
    "LEFT",
    "RIGHT",
    "PULL",
    "PUSH",
    "CIRCLE CW",
    "CIRCLE CCW",
    "LOCK",
    "UNLOCK",
    "HELLO",
    "WAVE"
]

colors = [
    "#3F51B5",  # red
    "#4CAF50",  # green
    "#F44336",  # blue
    "#0097A7",  # cyan
    "#FFC107",  # magenta
    "#9C27B0",  # yellow
    "#000000",  # black
    "#F06292",  # pink
    "#7986CB",  # light blue
    "#81C784",  # light green
    "#FF6F00",  # ornage
    "#757575"   # gray
]


def color_mapper(input):
    return colors[gestures.index(input)]


def mapper1(input):
    return gestures.index(input)


def scatter(x, y):
    # We create a scatter plot.
    f = plt.figure(figsize=(8, 8))
    ax = plt.subplot(aspect='equal')
    sc = ax.scatter(x[:, 0], x[:, 1],
                    c=list(map(color_mapper, y)))
    plt.xlim(-25, 25)
    plt.ylim(-25, 25)
    ax.axis('off')
    ax.axis('tight')

    # We add the labels for each digit.
    txts = []
    for i in range(len(gestures)):
        # Position of each label.
        xtext, ytext = np.median(
            x[np.array(list(map(mapper1, y))) == i, :], axis=0)
        txt = ax.text(xtext, ytext, gestures[i], fontsize=16)
        txt.set_path_effects([
            PathEffects.Stroke(linewidth=5, foreground="w"),
            PathEffects.Normal()])
        txts.append(txt)

    return f, ax, sc, txts


scatter(rez, y)
plt.show()
