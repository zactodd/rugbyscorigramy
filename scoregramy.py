import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.lines import Line2D

EXPECTIONS = lambda i, j: i > j or j in [1, 2, 4] or i in [1, 2, 4] or (j == 3 and 0 <= i < 3)

# Display matrix

cmap = ListedColormap(('k', 'w', 'g', 'r'))
bounds = [0, 1, 2, 3, 4]
norm = BoundaryNorm(bounds, cmap.N)

score_matrix = np.zeros((45, 150))
for i in range(45):
    for j in range(150):
        score_matrix[i, j] = 0 if EXPECTIONS(i, j) else 1

try_matrix = np.ones((8, 25))

for i, row in enumerate(base_result_mat):
    date, tour, rnd, team1, team2, s1, s2, tr1, tr2, _, _, location = row

    rnd = "" if rnd == "" else " " + rnd
    title_str = f"{team1} v {team2} on {date} at {location} during {tour}{rnd}\nScore: {s1}-{s2}, Trys: {tr1}-{tr2}"
    day, date = date.split(",")

    fig, axs = plt.subplots(ncols=2, nrows=1, figsize=(10, 3))
    title_colour = "k"
    font_weight = "normal"
    if tour.lower() == "wc":
        title_colour = "b"
        if rnd.lower() == "final":
            font_weight = "bold"

    fig.suptitle(title_str, fontsize=12, color=title_colour, fontweight=font_weight)

    sp1, sp2 = (int(i) for i in sorted([s1, s2], key=int))
    score_matrix[sp1, sp2] = 3

    axs[0].matshow(score_matrix, cmap=cmap, norm=norm)
    axs[0].set_title("Score", fontsize=10)

    trp1, trp2 = (int(t) for s, t in sorted([(s1, tr1), (s2, tr2)], key=lambda x: int(x[0])))
    try_matrix[trp1, trp2] = 3

    axs[1].matshow(try_matrix, cmap=cmap, norm=norm)
    axs[1].set_title("Trys", fontsize=10)

    for a in axs:
        a.title.set_position([.5, 1.15])
        a.tick_params(labelsize=8)
        a.set_xlabel("Winning Team", fontsize=8)
        a.set_ylabel("Losing Team", fontsize=8)

    custom_lines = [Line2D([0], [0], color="red", lw=4),
                    Line2D([0], [0], color="green", lw=4),
                    Line2D([0], [0], color="black", lw=4)]

    plt.legend(custom_lines, ["Match Results", "Previous Match Result", "Cannot be Scored Results"],
               bbox_to_anchor=(.5, -0.25), fontsize=8, ncol=3)

    print(f"images/image_{i:50d}_{date}_{team1}v{team2}.png")
    plt.savefig(f"images/image_{i:50d}_{date}_{team1}v{team2}.png", bbox_inches='tight')
    plt.clf()
    plt.close("all")

    score_matrix[sp1, sp2] = 2
    try_matrix[trp1, trp2] = 2

    print(f"{i:50d}/{date}")
