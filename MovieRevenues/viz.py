import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# I'll run data prep script first
exec(open("moviesprep.py").read())

# Now, let's start examining visually
"""
Here I will prepare the scatter and bar plot side by side
to show how well female lead and male lead movies are doing
and what are frequencies of male vs female lead movies
"""

# I get two seperate datasets for female and for male
females = movies_updated[movies_updated['gender'] == 1.0]
males = movies_updated[movies_updated['gender'] == 0.0]

# I drop unrecognizable values
females = females[females['budget_log'] > 0]
females = females[females['revenue_log'] > 0]

males = males[males['budget_log'] > 0]
males = males[males['revenue_log'] > 0]

# I construct the counter for the bar plot
labels = ['Movies']
women = len(females.revenue)
men = len(males.revenue)
width = 0.35
x = np.arange(len(labels))


# Let's start plotting
fig, ax = plt.subplots(1, 2, figsize=(18,9))
fig.patch.set_facecolor('slategrey') # I setup the backgroung color
fig.suptitle('Top 5000 Grossing Movies with Female and Male Leads', color='w', fontsize=22)
    
# background color for each individual graphs
ax[0].set_facecolor('slategrey')
ax[1].set_facecolor('slategrey')

"""
Scatter plot with male vs female lead movies
with a movie budget on x-axis and movie revenue on y-axis
"""
ax[0].scatter(females.budget, females.revenue, c='w', s=100, alpha=.50)
ax[0].scatter(males.budget, males.revenue, c='cyan', s=80, alpha=.3)
ax[0].set_xlim(left=0)
ax[0].set_ylim(bottom=0)
legend = ax[0].legend(labels=('Female', 'Male'), loc='upper right',
             fontsize=14, frameon=None, framealpha=.2)
plt.setp(legend.get_texts(), color='w')
ax[0].spines['top'].set_visible(False)
ax[0].spines['right'].set_visible(False)
ax[0].tick_params(color='grey', labelcolor='w')
for spine in ax[0].spines.values():
        spine.set_edgecolor('whitesmoke')
ax[0].set_xlabel('Movie Budget', c='w', fontsize=14)
ax[0].set_ylabel('Movie Revenue', c='w', fontsize=14)

rects1 = ax[1].bar(x - width/2, women, width, label='Females', color='w', alpha=.5)
rects2 = ax[1].bar(x + width/2, men, width, label='Males', color='cyan', alpha=.3)

legend1 = ax[1].legend(labels=('Female', 'Male'), loc='upper left',
             fontsize=14, frameon=None, framealpha=.2)
plt.setp(legend1.get_texts(), color='w')
ax[1].spines['top'].set_visible(False)
ax[1].spines['right'].set_visible(False)
ax[1].tick_params(color='grey', labelcolor='w')
for spine in ax[1].spines.values():
        spine.set_edgecolor('whitesmoke')
ax[1].set_xticks(x, '')
ax[1].set_ylabel('Number of Movies', c='w', fontsize=14)

# Custom function to label the bars
def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax[1].annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', color='white', fontsize=16)
        
autolabel(rects1)
autolabel(rects2)
plt.show()


# I plot the boxplot for main variables to see the
# distribution and what can be potential outliers
fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(2, 3, figsize=(12, 8))
figsize=(20, 6)

ax1.boxplot(movies_updated['budget_log'].values)
ax1.set_title('Log of Budget')
ax2.boxplot(movies_updated['budget'].values)
ax2.set_title('Budget')
ax3.boxplot(movies_updated['popularity'].values)
ax3.set_title('Popularity')
ax4.boxplot(movies_updated['runtime'].values)
ax4.set_title('Runtime in minutes')
ax5.boxplot(movies_updated['vote_average'].values)
ax5.set_title('Average Vote')
ax6.boxplot(movies_updated['vote_count'].values)
ax6.set_title('Total Votes')
plt.show()








