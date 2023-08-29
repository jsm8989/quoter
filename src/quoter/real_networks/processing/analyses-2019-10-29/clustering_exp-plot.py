import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

### ADDING EDGES VS TRIANGLES
df1 = pd.read_csv("real_networks-links_only.csv")
df2 = pd.read_csv("real_networks-links_only-EDGE.csv")
df3 = pd.read_csv("real_networks-links_only-TRIANGLE.csv")

for i in range(len(df1["network"].values)):
    t1 = df1["transitivity"].values[i]
    t2 = df2["transitivity"].values[i]
    t3 = df3["transitivity"].values[i]
    h1 = df1["average_hx"].values[i]
    h2 = df2["average_hx"].values[i]
    h3 = df3["average_hx"].values[i]
    plt.plot(t1, h1, "ko")
    plt.plot(t2, h2, "co")
    plt.plot(t3, h3, "ro")

    plt.plot([t2, t1, t3], [h2, h1, h3], "k-")


label1 = mlines.Line2D(
    [],
    [],
    color="black",
    marker="o",
    linestyle="None",
    markersize=6,
    label="Real network",
)
label2 = mlines.Line2D(
    [],
    [],
    color="cyan",
    marker="o",
    linestyle="None",
    markersize=6,
    label="Edge added randomly",
)
label3 = mlines.Line2D(
    [],
    [],
    color="red",
    marker="o",
    linestyle="None",
    markersize=6,
    label="Triangle completion",
)
plt.legend(handles=[label1, label2, label3])
plt.xlabel("Transitivity")
plt.ylabel(r"Average cross-entropy, $\langle h_\times \rangle$")
plt.show()