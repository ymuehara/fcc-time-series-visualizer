import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import numpy as np
# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv", index_col=0, parse_dates=["date"])

# Clean data
# Clean the data by filtering out days
# when the page views were in the top 2.5% of the dataset
# or bottom 2.5% of the dataset.
df = df.loc[
    (df["value"] <= df["value"].quantile(0.975))
    & (df["value"] >= df["value"].quantile(0.025))
    ]


def draw_line_plot():
    dfl = df.copy()
    fig, axes = plt.subplots()
    plt.plot(dfl, color="red")
    plt.ylabel("Page Views")
    plt.xlabel("Date")
    plt.title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    
    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot

    df_bar = df.copy()
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
                       'August', 'September', 'October', 'November', 'December']
    df_bar['year'] = df_bar.index.year
    df_bar['Months'] = df_bar.index.strftime('%B')
    df_bar2 = df_bar.groupby(['year', 'Months']).mean()
    df_bar2.reset_index(level="Months", inplace=True)
    piv = df_bar2.pivot(columns="Months", values='value')
    # ordena os meses
    piv = piv[['January', 'February', 'March', 'April', 'May', 'June', 'July',
                       'August', 'September', 'October', 'November', 'December']]
    #print(piv)

    # Draw bar plot
    piv.plot.bar(label=months)
    plt.ylabel('Average Page Views')
    plt.xlabel('Years')
    plt.legend(loc='upper left', title="Months", prop={'size': 6})
    plt.tight_layout()
    fig = plt.gcf()


    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    # sort by months
    df_box.sort_values(by=['year', 'date'], ascending=[False, True], inplace=True)

    # Draw box plots (using Seaborn)
    fig, axs = plt.subplots(ncols=2)
    ax1 = sns.boxplot(x="year", y="value", data=df_box, ax=axs[0])
    ax1.set_ylabel("Page Views")
    ax1.set_xlabel("Year")
    ax1.set_title("Year-wise Box Plot (Trend)")
    ax2 = sns.boxplot(x="month", y="value", data=df_box, ax=axs[1])
    ax2.set_ylabel("Page Views")
    ax2.set_xlabel("Month")
    ax2.set_title("Month-wise Box Plot (Seasonality)")
    #plt.show()

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
