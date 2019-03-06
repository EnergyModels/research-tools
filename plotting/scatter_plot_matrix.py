import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#=====================================================
# User Inputs
#=====================================================
figure_name = "SPLOM" # png extension automatically added later
data_file = "results_monte_carlo_xls.csv"

#-----------------------------------------------------
# Import data - expected as a pandas DataFrame
#----------------------------------------------------
df = pd.read_csv(data_file)

#-----------------------------------------------------
# Aesthetics (style + context)
# https://seaborn.pydata.org/tutorial/aesthetics.html
#-----------------------------------------------------
resolution = 1000 # Resolution (DPI - dots per inch)
style = 'white'     # options: "white", "whitegrid", "dark", "darkgrid", "ticks"
context = 'talk'  # options "paper", "notebook", "talk", "poster" (smallest -> largest)

# Series palette options
colorblind_palette = sns.color_palette('colorblind')        # https://seaborn.pydata.org/tutorial/color_palettes.html
xkcd_palette = sns.xkcd_palette(["royal blue", "tangerine", "greyish", "faded green", "raspberry"]) # https://xkcd.com/color/rgb/
custom_palette = [(0.380,0.380,0.380),(0.957,0.451,0.125),(.047, 0.149, 0.361),(0.847,0.000,0.067)] # Custom palette

#-----------------------------------------------------
# Plotting Inputs
#-----------------------------------------------------
# x variables, all lists are expected to the same length
x_vars = ["a","b","c"]                     # Need to be columns in DataFrame
x_labels = ["A (-)","B (1E3)","C (-)"]     # Note: keep short
x_converts = [1,1E-3,1,1]                  # Multiplier to convert to display units
x_ticks = [[],[],[]]                       # Ok to leave empty
x_lims = [[],[],[]]                        # Ok to leave empty

# y variables, all lists are expected to the same length
y_vars = ["x","y"]
y_labels = ["X (%)", "Y (%)"]
y_converts = [1,1E-2]
y_ticks = [[],[],[],[]]
y_lims = [[],[],[],[]]

# series variables, all lists are expected to the same length
series_var = 'sheetname'
series_vals = ['case1','case2','case3','case4']
series_labels = ['Case 1','Case 2','Case 3',' Case 4']
series_colors = custom_palette # Use a palette listed above
series_markers = ['x', '+', 'o', '*']
series_marker_sizes = [40,40,40,40]

#=====================================================
# Set figure parameters based on experience for each context
#=====================================================
if context=='paper':
    fig_size = [8,6]        # (width followed by height, in inches) Note: OK to leave as an empty list
    leg_coord = [1.6, -0.3] # Legend coordinates (x,y)
    hspace = 0.15           # vertical space between figures
    wspace = 0.15           # horizontal space between figures
elif context=='notebook':
    fig_size = [8,6]
    leg_coord = [1.75, -0.3]
    hspace = 0.2
    wspace = 0.2
elif context == 'talk':
    fig_size = [12,8]
    leg_coord = [1.75, -0.4]
    hspace = 0.3
    wspace = 0.35
elif context == 'poster':
    fig_size = [12,8]
    leg_coord = [1.8, -0.5]
    hspace = 0.3
    wspace = 0.35

#=====================================================
# Begin plotting
#=====================================================

# Set style and context using seaborn
sns.set_style(style)
sns.set_context(context)

# Create Plots
nrows = len(y_vars)
ncols = len(x_vars)
f, ax = plt.subplots(nrows, ncols)

# Iterate Rows (Y variables)
for i,y_var,y_label,y_convert, y_tick,y_lim in zip(range(nrows),y_vars,y_labels,y_converts,y_ticks,y_lims):

    # Iterate Columns (X variables)
    for j, x_var, x_label, x_convert, x_tick,x_lim in zip(range(ncols), x_vars, x_labels, x_converts,x_ticks,x_lims):

        # Iterate Series
        for series_val,label,color,marker,size in zip(series_vals,series_labels,series_colors,series_markers,series_marker_sizes):

            # Select entries of interest
            df2 = df[(df.loc[:,series_var] == series_val)]

            # Plot
            x = df2.loc[:, x_var] * x_convert
            y = df2.loc[:, y_var] * y_convert
            ax[i,j].scatter(x.values, y.values, c=color, s=size, marker=marker, label=label,edgecolors='none')

        # X-axis Labels (Only bottom)
        if i == nrows-1:
            ax[i,j].set_xlabel(x_label)
        else:
            ax[i,j].get_xaxis().set_visible(False)

        # Y-axis labels (Only left side)
        if j == 0:
            ax[i,j].set_ylabel(y_label)
            ax[i,j].yaxis.set_label_coords(-0.25, 0.5)
        else:
            ax[i,j].get_yaxis().set_visible(False)

        # Set X and Y Limits
        if len(x_lim)== 2:
            ax[i,j].set_xlim(left=x_lim[0], right=x_lim[1])
        if len(y_lim) ==2 :
            ax[i,j].set_ylim(bottom=y_lim[0],top=y_lim[1])

        # Set X ticks
        if len(x_tick) > 2:
            ax[i,j].xaxis.set_ticks(x_tick)
        else:
            n_ticks = 4
            ax[i, j].locator_params(axis='x', nbins=n_ticks)

        # Set Y ticks (either specified values, or limits number of ticks used)
        if len(y_tick) > 2:
            ax[i,j].yaxis.set_ticks(y_tick)
        else:
            n_ticks = 4
            ax[i, j].locator_params(axis='y', nbins=n_ticks)


# Legend (only for middle bottom)
leg = ax[nrows-1,0].legend(bbox_to_anchor=(leg_coord[0], leg_coord[1]), loc='center', ncol=len(series_labels), frameon = False, scatterpoints = 1)

# Adjust layout
if len(fig_size)>0:
    f.set_size_inches(fig_size)
plt.tight_layout()                         # https://matplotlib.org/users/tight_layout_guide.html
f.subplots_adjust(wspace = wspace,hspace=hspace) # https://matplotlib.org/api/_as_gen/matplotlib.pyplot.subplots_adjust.html

# Save Figure
savename = figure_name + "_" + context + '.png'
plt.savefig(savename, dpi=resolution, bbox_inches="tight") #  bbox_inches="tight" is used to include the legend
plt.close()
