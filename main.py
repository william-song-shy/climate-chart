from math import ceil,floor

from matplotlib import pyplot as plt
from matplotlib.ticker import FuncFormatter, LinearLocator, FixedLocator

data_test = {"prep":[54,46,50,44,58,56,53,51,56,57,58,54],"temp":[3.7,4.6,8.1,11.2,14.7,17.8,19.8,19.4,16.7,12,7.5,4.6]}
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def month_formatter(x, pos):
    if x % 3 == 1:
        return months[int(x)]


def gen_plot(data,name=""):

    fig, ax1 = plt.subplots()
    ax1.xaxis.set_major_formatter(FuncFormatter(month_formatter))
    ax1.xaxis.set_ticks([x for x in range(12) if x % 3 == 1])
    fig.set_size_inches(5.5, 7)
    ax2 = ax1.twinx()
    ax1.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: str(int(x)) + " mm"))
    ax2.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: str(int(x)) + " °C"))
    ax1.bar(months, data["prep"], color="deepskyblue")
    ax2.plot(months, data["temp"], color="darkred",clip_on=False)
    ax1.set_ylim(0, ceil(max(data["prep"]) * 1.5 / 50) * 50)
    ax1.yaxis.set_major_locator(LinearLocator(numticks=6))
    diff = max(data["temp"]) - min(data["temp"])
    mi = min(data["temp"])
    ma = max(data["temp"])
    mi = floor(mi / 5) * 5
    ma = ceil(ma / 5) * 5
    if ma-mi <= 30:
        ax2.set_ylim(ma-25, ma)
        ax2.yaxis.set_major_locator(FixedLocator([ma-25,ma-20,ma-15,ma-10,ma-5,ma]))
    else:
        ax2.set_ylim(-10, 40)
        ax2.yaxis.set_major_locator(FixedLocator([-10,0,10,20,30,40]))
    ax1.grid(axis="y", color="black", linestyle="--")
    ax2.grid(axis="y", color="black", linestyle="--")
    ax1.set_title(f"Climate Chart - {name}")
    ax1.set_axisbelow(True)
    # plt.show()
    return fig

if __name__=="__main__":
    fig = gen_plot(data_test,'Paris')
    fig.savefig("test.png",dpi=300)