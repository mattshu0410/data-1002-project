
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
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

combined_indicators["GNI_capita_bins"] = pd.cut(combined_indicators["x"], bins=[0,1025,4035,12475,float('inf')]) #These values from World Bank, Max is Arbitrary
print(combined_indicators)

#EXPERIMENT

sns.lmplot(data=combined_indicators, x='x', y='y', hue='Indicator', palette=["#000620"], markers=['x', '.'], ci=None)
#sns.scatterplot(data=combined_indicators, x="x", y="y",style='Indicator', s=50, alpha=.7, linewidth=.5, edgecolor="white", markers=True)

plt.axvspan(0,1025, alpha=0.5, color='#de425b', zorder=-1)
plt.axvspan(1025,4035, alpha=0.5, color='#fbb862', zorder=-1)
plt.axvspan(4035,12475, alpha=0.5, color ='#afd17c', zorder=-1)
plt.axvspan(12475,100000, alpha=0.5, color='#00876c', zorder=-1)
plt.title("HFI & Happiness Regressed on GNI/capita")
plt.xlabel("GNI/Capita by Purchasing Power Parity (2017 International $)")
plt.ylabel("Standard Indicator Score (0-10)")
plt.legend(labels=("HFI Regression Line", "Happiness Regression Line"))
plt.savefig("Figures/fig1_hap_freedom_regplot.png", bbox_inches='tight', dpi=500)
plt.show()
#EXPERIMENT

#EXPERIMENT
x_col = 'x'
y_col = 'y'
hue_col = 'Indicator'
df = combined_indicators

markers = ['x','.']
colors = ["#000620", "#000620"]
linestyles = ['-','--']

legend_elements = [Line2D([0], [0], color='#000620', lw=4, label='Freedom', linestyles='--'),
                   Line2D([0],[0], color='#000620', lw=4, label='Happiness'),
                   Line2D([0], [0], marker='x', color='#000620', label='Freedom',
                          markerfacecolor='#000620', markersize=10),
                   Line2D([0], [0], marker='.', color='#000620', label='Happiness',
                          markerfacecolor='#000620', markersize=10),
                   Patch(facecolor='#de425b', label='Color Patch')]

plt.figure()
plt.axvspan(0,1025, alpha=0.5, color='#de425b', zorder=-1)
plt.axvspan(1025,4035, alpha=0.5, color='#fbb862', zorder=-1)
plt.axvspan(4035,12475, alpha=0.5, color ='#afd17c', zorder=-1)
plt.axvspan(12475,100000, alpha=0.5, color='#00876c', zorder=-1)

for (hue,gr),m,c,ls in zip(df.groupby(hue_col),markers,colors,linestyles):
    sns.regplot(data=gr, x=x_col, y=y_col, marker=m, color=c, line_kws={'ls':ls}, ci=None, label=f'{hue_col}={hue}')
plt.title("HFI & Happiness Regressed on GNI/capita")
plt.xlabel("GNI/Capita by Purchasing Power Parity (2017 International $)")
plt.ylabel("Standard Indicator Score (0-10)")
plt.legend()
#EXPERIMENT

g = sns.FacetGrid(combined_indicators, height=5, hue='Indicator')
g.map(plt.scatter, "x", "y", s=50, alpha=.7, linewidth=.5, edgecolor="white")
g.map(sns.regplot, "x", "y", ci=None, robust=1)
g.add_legend()
plt.axvspan(0,1025, alpha=0.3, color='#ffa600')
plt.axvspan(1025,4035, alpha=0.3, color='#ff6361')
plt.axvspan(4035,12475, alpha=0.3, color ='#bc5090')
plt.axvspan(12475,100000, alpha=0.3, color='#58508d')
plt.title("HFI & Happiness Regressed on GNI/capita")
plt.xlabel("GNI/Capita by Purchasing Power Parity (2017 International $)")
plt.ylabel("Standard Indicator Score (0-10)")
plt.legend(labels=("HFI Regression Line", "Happiness Regression Line"))
plt.savefig("Figures/fig1_hap_freedom_regplot.png", bbox_inches='tight', dpi=500)
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
fig.write_html("M:/Github Version Control Projects/data-1002-project/Figures/fig2_hap_freedom_regplot_interactive.html")
#import chart_studio
#username = 'matthewshu' # your username
#api_key = 'GZZnWMNJzOUWnhUAB7dw' # your api key - go to profile > settings > regenerate key
#chart_studio.tools.set_credentials_file(username=username, api_key=api_key)
#import chart_studio.plotly as py
#py.plot(fig, filename = 'fig2_hap_freedom_regplot', auto_open=True)
fig.show()

#Plot 3: What is the relationship between different regions and their respective happiness and freedom?
#select indicators data with region to identify clustering
indicator_by_region = df[['region', 'hf_score', 'Happiness.Score']]
h = sns.jointplot(data=indicator_by_region, x='hf_score', y='Happiness.Score', hue='region', height=10)
h.set_axis_labels('Human Freedom Score (0-10)', 'Happiness Score (0-10)')
plt.savefig("Figures/fig3_hap_freedom_region.png", dpi=500)
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
plt.savefig("Figures/fig4_hap_free_means_by_region.png", dpi=500)
plt.show()
