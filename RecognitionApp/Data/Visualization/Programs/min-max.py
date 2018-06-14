import pandas as pd
from numpy import array
import matplotlib.pyplot as plt

FILE_NAME = "/home/euzenmendenzien/Documents/\
Gamayun/2.0/Data/all_data.csv"

NUMBER_OF_TIMESTEPS = 60
DEGREES_OF_FREEDOM = 6
OUTPUT_SIZE = 4

x_axis = array([x for x in range(NUMBER_OF_TIMESTEPS)])

df = pd.read_csv(FILE_NAME, header=None)

df.set_index(df.columns[0].tolist(), inplace=True)

df.iloc[:, 0::6] /= 2**15 * 2
df.iloc[:, 1::6] /= 2**15 * 2
df.iloc[:, 2::6] /= 2**15 * 2
df.iloc[:, 3::6] /= 2**15 * 1000
df.iloc[:, 4::6] /= 2**15 * 1000
df.iloc[:, 5::6] /= 2**15 * 1000

layer0 = ['t' + str(x).zfill(2) for x in range(NUMBER_OF_TIMESTEPS)
          for y in range(DEGREES_OF_FREEDOM)]

layer1 = ['ac_x', 'ac_y', 'ac_z', 'gy_x', 'gy_y', 'gy_z'] * NUMBER_OF_TIMESTEPS

df.columns = pd.MultiIndex.from_arrays([layer0, layer1])

# use this for finding exceptions in data

'''
gesture_name = "gesture_1"
axis_name = "gy_z"

df["i"] = [x for x in range(558)]
df.set_index("i", append =True, inplace=True)

print(df)

with pd.option_context('display.max_rows', None, 'display.max_columns', 3):
    print(df.sort_index().loc[gesture_name].xs(axis_name, axis = 1, level = 1))
    print(df.sort_index().loc[gesture_name] \
    .xs(axis_name, axis = 1, level = 1).idxmax())
'''

grouped_data = df.groupby(level=0)


def add_index(df, string, inplace=False):
    if string in df.index.names:
        return

    df[string] = string
    df.set_index(string, append=True, inplace=inplace)
    df.index.names = [None] * len(df.index.names)


mean_df = grouped_data.mean().stack()
add_index(mean_df, "mean", inplace=True)

max_df = grouped_data.max().stack()
add_index(max_df, "max", inplace=True)

min_df = grouped_data.min().stack()
add_index(min_df, "min", inplace=True)

rez = pd.concat([mean_df, max_df, min_df]).sort_index()

axes = ["ac_x", "ac_y", "ac_z", "gy_x", "gy_y", "gy_z"]
colors = ["#3F51B5", "#4CAF50", "#F44336", "#00BCD4", "#9C27B0", "#FFC107"]

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

for gesture in gestures:
    plt.suptitle(gesture)
    for axis, color, i in zip(axes, colors, range(len(axes))):
        ax = plt.subplot(2, 3, i + 1)
        ax.set_title(axis)
        if i < 3:
            plt.ylabel("G-s")
        else:
            plt.ylabel("°/s")
        plt.xlabel("time steps")
        plt.fill_between(x_axis,
                         rez.loc[gesture, axis, "max"],
                         rez.loc[gesture, axis, "min"],
                         color=color,
                         alpha=0.4,
                         linewidth=0, label=axis + " range")

        plt.plot(
            x_axis,
            rez.loc[gesture, axis, "mean"],
            color=color,
            label=axis + " mean")

        plt.legend()

    # plt.subplots_adjust(top=0.935,
    #           bottom=0.075,
    #           left=0.06,
    #           right=0.975,
    #           hspace=0.2,
    #           wspace=0.2)

    plt.subplots_adjust(top=0.91,
                        bottom=0.075,
                        left=0.06,
                        right=0.975,
                        hspace=0.290,
                        wspace=0.4)
    # plt.ylabel("raw value")
    # plt.xlabel("time steps")
    # plt.legend()
    plt.show()
