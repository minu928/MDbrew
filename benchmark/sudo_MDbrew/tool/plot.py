import matplotlib.pyplot as plt


def set_format():
    plt.rc("text")  # , usetex=True)
    plt.rcParams["font.family"] = "Serif"
    plt.rcParams["mathtext.fontset"] = "custom"
    plt.rcParams["mathtext.it"] = "Serif"
    plt.rcParams["mathtext.rm"] = "Serif"
    plt.rcParams["mathtext.tt"] = "Serif"
    plt.rcParams["mathtext.bf"] = "Serif"
    plt.rcParams["mathtext.cal"] = "Serif"
    plt.rcParams["mathtext.sf"] = "Serif"

    plt.rcParams["lines.linewidth"] = 2.0
    plt.rcParams["errorbar.capsize"] = 4
    plt.rcParams["figure.dpi"] = 330

    plt.rcParams["xtick.major.size"] = 5
    plt.rcParams["ytick.major.size"] = 5

    plt.rcParams["xtick.direction"] = "in"
    plt.rcParams["ytick.direction"] = "in"

    plt.rcParams["xtick.minor.visible"] = True
    plt.rcParams["ytick.minor.visible"] = True

    plt.rcParams["xtick.top"] = True
    plt.rcParams["ytick.right"] = True

    plt.rcParams["figure.subplot.left"] = 0.2
    plt.rcParams["figure.subplot.right"] = 0.925
    plt.rcParams["figure.subplot.bottom"] = 0.2
    plt.rcParams["figure.subplot.top"] = 0.85
    plt.rcParams["figure.subplot.wspace"] = 0.4
    plt.rcParams["figure.subplot.hspace"] = 0.4

    plt.rcParams["grid.alpha"] = 0.25

    plt.rcParams["legend.fontsize"] = "x-small"

    plt.rcParams["lines.markersize"] = 3
    plt.rcParams["lines.markeredgewidth"] = 1.5

    plt.rcParams["xtick.major.width"] = 1.5
    plt.rcParams["ytick.major.width"] = 1.5
