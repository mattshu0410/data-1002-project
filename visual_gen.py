import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
sns.set_theme()

#import cleaned data from repository
df = pd.read_csv("https://raw.githubusercontent.com/mattshu0410/data-1002-project/master/merged_data.csv")

#Plot 1: Does the GNI per capita of different countries display positive correlation with improved human freedom and happiness scores?
#select indicators as separate dataframes
Freedom = df[['countries','hf_score','GNI_capita']]
Happiness = df[['countries','Happiness.Score', 'GNI_capita']]
#Correlation of Linear Model & Residual Distribution
print(Freedom["hf_score"].corr(Freedom["GNI_capita"]))
print(Happiness["Happiness.Score"].corr(Happiness["GNI_capita"]))
fig, (ax1, ax2) = plt.subplots(1,2)
sns.residplot(data=Freedom, x='GNI_capita', y='hf_score', ax =ax1)
sns.residplot(data=Happiness, x='GNI_capita', y='Happiness.Score', ax =ax2)
plt.show()

#The following code concatenates the x,y of 2 dfs so that their regression models can be plotted together
#https://stackoverflow.com/questions/36026149/plotting-multiple-linear-regressions-on-the-same-seaborn-plot
combined_indicators = pd.concat([Freedom.rename(columns={'GNI_capita':'x','hf_score':'y'})
                .join(pd.Series(['Freedom']*len(Freedom), name='Indicator')),
                Happiness.rename(columns={'GNI_capita':'x','Happiness.Score':'y'})
                .join(pd.Series(['Happiness']*len(Happiness), name='Indicator'))],
               ignore_index=True)
g = sns.FacetGrid(combined_indicators, hue='Indicator', height=5)
g.map(plt.scatter, "x", "y", s=50, alpha=.7, linewidth=.5, edgecolor="white")
g.map(sns.regplot, "x", "y", ci=None, robust=1)
g.add_legend()
plt.title("HFI & Happiness Regressed on GNI/capita")
plt.xlabel("GNI/Capita by Purchasing Power Parity (2017 International $)")
plt.ylabel("Standard Indicator Score (0-10)")
plt.legend(labels=("HFI Regression Line", "Happiness Regression Line"))
plt.savefig("fig1_hap_freedom_regplot", bbox_inches='tight', dpi=500)
plt.show()

#Plot 2: Interactive Plot with Four Variables
print(combined_indicators)
fig = px.scatter(combined_indicators, x='x', y='y', color='Indicator', text = 'countries', trendline='ols',
                 labels={
                     'x':'GNI per Capita by PPP by Purchasing Power Parity (2017 International $)',
                     'y':'Standard Indicator Score (0-10)',
                     'countries':'Country'
                 },
                 title = 'HFI & Happiness Regressed on GNI/capita'
                 )
fig.layout.template = 'plotly_dark'
fig.write_html("M:/Github Version Control Projects/data-1002-project/fig2_hap_freedom_regplot_interactive.html")
fig.show()

#Plot 3: What is the relationship between different regions and their respective happiness and freedom?
#select indicators data with region to identify clustering
indicator_by_region = df[['region', 'hf_score', 'Happiness.Score']]
h = sns.jointplot(data=indicator_by_region, x='hf_score', y='Happiness.Score', hue='region', height=10)
h.set_axis_labels('Human Freedom Score (0-10)', 'Happiness Score (0-10)')
plt.savefig("fig3_hap_freedom_region", dpi=500)
plt.show()

#Plot 4: Barplot of means of happiness and freedom by region
means = indicator_by_region.groupby("region").mean()
means = means.reset_index()
#https://stackoverflow.com/questions/36537945/reshape-wide-to-long-in-pandas
converted_means = pd.melt(means, id_vars='region', value_vars=['hf_score','Happiness.Score'])
print(converted_means)
i = sns.barplot(data=converted_means, x="region", y='value', hue='variable')
h, l = i.get_legend_handles_labels()
i.legend(h, ["Freedom", "Happiness"], title = "Indicator", loc='lower right')
for item in i.get_xticklabels():
    item.set_rotation(90)
    item.horizontalalignment='right'
plt.xlabel("World Region")
plt.ylabel("Mean Score (0-10)")
plt.tight_layout()
plt.savefig("fig4_hap_free_means_by_region", dpi=500)
plt.show()
