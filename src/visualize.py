"""
Build four PDF reports from output/messages.csv:
  1. Map of sighting locations
  2. Bar chart of shape frequencies
  3–4. Two free-form plots you invent
"""
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from pathlib import Path


def make_reports(csv_path: str | Path = "output/messages.csv",
                 outdir: str | Path = "output") -> None:
    df = pd.read_csv(csv_path,
                     names=["ts", "lat", "lon", "shape", "msg", "label"])
    out = Path(outdir)
    out.mkdir(exist_ok=True)

    # Report 1 – location scatter
    with PdfPages(out / "report1.pdf") as pdf:
        plt.figure()
        df.plot.scatter(x="lon", y="lat",
                        c=df.label.map({"human": 0, "alien": 1}),
                        alpha=.6)
        plt.title("Sightings by location")
        pdf.savefig(); plt.close()

    # Report 2 – shape frequency
    with PdfPages(out / "report2.pdf") as pdf:
        plt.figure()
        df["shape"].value_counts().plot.bar()
        plt.title("Shape frequency")
        pdf.savefig(); plt.close()

    # Report 3 – sightings over time
    with PdfPages(out / "report3.pdf") as pdf:
        plt.figure()
        (pd.to_datetime(df.ts)
           .dt.date
           .value_counts()
           .sort_index()
           .plot())
        plt.title("Sightings per day")
        pdf.savefig(); plt.close()

    # Report 4 – human vs alien pie chart
    with PdfPages(out / "report4.pdf") as pdf:
        plt.figure()
        df.label.value_counts().plot.pie(autopct="%1.1f%%")
        plt.title("Human vs Alien messages")
        pdf.savefig(); plt.close()
