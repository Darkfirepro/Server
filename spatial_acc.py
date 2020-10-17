import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches

origin_old = -5
length = 10

trial1_y_ofall = [0.38, 0.49, 0.36, 0.13, 0.09, 0.04]
trial1_x_ofall = [1.46, 1.39, 1.45, 0.36, 0.29, 0.27]
trial2_y_ofall = [0.64, 0.69, 0.76, 0.38, 0.42, 0.27]
trial2_x_ofall = [1.52, 1.54, 1.56, 0.46, 0.38, 0.34]
trial3_y_ofall = [2.37, 2.46, 2.69, 0.69, 0.86, 1.08]
trial3_x_ofall = [1.69, 1.61, 1.75, 0.93, 1.04, 0.91]
trial4_y_ofall = [3.57, 2.88, 3.15, 1.07, 1.83, 1.86]
trial4_x_ofall = [2.67, 2.61, 2.65, 1.21, 1.16, 1.12]

trial1_y_asa = [0.33, 0.42, 0.39, 0.09, 0.08, 0.06]
trial1_x_asa = [1.43, 1.41, 1.43, 0.44, 0.34, 0.41]
trial2_y_asa = [0.64, 0.69, 0.72, 0.37, 0.39, 0.48]
trial2_x_asa = [1.58, 1.61, 1.55, 0.39, 0.42, 0.31]
trial3_y_asa = [2.39, 2.81, 2.65, 0.56, 0.73, 1.21]
trial3_x_asa = [1.61, 1.63, 1.63, 0.94, 1.13, 0.93]
trial4_y_asa = [3.65, 3.29, 2.79, 2.11, 1.72, 1.69]
trial4_x_asa = [2.68, 2.74, 2.63, 1.24, 1.22, 1.15]

average_front_y_ofall = [0.41, 0.697, 2.507, 3.2]
average_front_x_ofall = [1.43, 1.54, 1.683, 2.643]
average_back_y_ofall = [0.0867, 0.3567, 0.8767, 1.5867]
average_back_x_ofall = [0.3067, 0.3933, 0.96, 1.1633]

average_front_y_asa = [0.38, 0.6833, 2.6167, 3.243]
average_front_x_asa = [1.423, 1.58, 1.6233, 2.6833]
average_back_y_asa = [0.0767, 0.4133, 0.833, 1.84]
average_back_x_asa = [0.3967, 0.3733, 1, 1.2033]

def draw_position(trial_x, trial_y, dist, type_1):
    plt.axes()
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.grid(True, which='both')
    ax.axhline(y=0, color='k')
    ax.axvline(x=0, color='k')

    ax.set_xlim(-8, 9)
    ax.set_ylim(-8, 9)
    # Set major ticks for x axis
    major_xticks = np.arange(-8, 9, 1)

    # Set major ticks for y axis
    major_yticks = np.arange(-8, 9, 1)

    # I want minor ticks for x axis
    minor_xticks = np.arange(-8, 9, 0.25)

    # I want minor ticks for y axis
    minor_yticks = np.arange(-8, 9, 0.25)

    ax.tick_params(axis='both', which='major', labelsize=6)
    ax.tick_params(axis='both', which='minor', labelsize=0)

    ax.set_xticks(major_xticks)
    ax.set_xticks(minor_yticks, minor=True)

    ax.set_yticks(major_xticks)
    ax.set_yticks(minor_yticks, minor=True)

    ax.tick_params(which='both', direction='out')

    # Specify different settings for major and minor grids
    ax.grid(which='minor', alpha=0.3)
    ax.grid(which='major', alpha=0.7)

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels)

    plt.title("The physical positions of the cube on " + str(dist) + "m - " + type_1)
    for i in range(6):
        if i < 3:
            rectangle = plt.Rectangle((origin_old + trial_x[i], origin_old + trial_y[i]), length, length, fill=False, edgecolor=(1, 0, 0))
            plt.gca().add_patch(rectangle)
            plt.axis('scaled')
        else:
            rectangle = plt.Rectangle((origin_old + trial_x[i], origin_old + trial_y[i]), length, length, fill=False, edgecolor="blue")
            plt.gca().add_patch(rectangle)
            plt.axis('scaled')
    rectangle = plt.Rectangle((origin_old, origin_old), length, length, fill=False, edgecolor=(0, 0, 0), linewidth=2, linestyle="-.")
    plt.gca().add_patch(rectangle)

    plt.axis('scaled')

    red_patch = mpatches.Patch(color='blue', label='Position on View: back')
    blue_patch = mpatches.Patch(color='red', label='Position on View: front')
    black_patch = mpatches.Patch(color='black', label='Theoretical Position')
    plt.legend(handles=[red_patch, blue_patch, black_patch], loc="upper left", borderaxespad=0., bbox_to_anchor=(1.05, 1))

    plt.show()

def draw_bar(trial1_ofall, trial1_asa, view1, axis1):
    labels = ["1m", "2m", "3m", "4m"]
    x = np.arange(len(labels))
    width = 0.35
    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, trial1_ofall, width, label="OFALL"+"_"+view1+"_"+axis1)
    rects2 = ax.bar(x + width / 2, trial1_asa, width, label="ASA"+"_"+view1+"_"+axis1)

    ax.set_ylabel('offsets (cm)')
    ax.set_title('The offsets on the ' + view1 + " view " + " of " + axis1 + "-axis " + "between ASA and OFALL in different distances")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    autolabel(rects1, ax)
    autolabel(rects2, ax)

    fig.tight_layout()

    plt.show()

def autolabel(rects, ax):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


draw_position(trial4_x_ofall, trial4_y_ofall, 4, "OFALL")
#draw_bar(average_back_y_ofall, average_back_y_asa, "back", "y")
