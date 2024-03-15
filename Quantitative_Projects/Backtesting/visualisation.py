import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as colors

import os

def gen_analysis_heatmap(df, title):
    # Set the 'Stock' column as the index
    df.set_index('Stock', inplace=True)

    # Create a custom color map
    cmap = colors.ListedColormap(['red', 'gray', 'green'])
    bounds = [-np.inf, 0, np.inf]
    norm = colors.BoundaryNorm(bounds, cmap.N)

    fig, ax = plt.subplots()
    # Create a heatmap with the custom color map
    sns.heatmap(df, annot=True, cmap=cmap, fmt='g', norm=norm, cbar=False)
    
    # Set the title and labels
    plt.title(title)
    plt.xlabel('Metrics')
    plt.xticks(rotation=45)
    plt.ylabel('Stocks')
    plt.yticks(rotation='horizontal')

    # Display the heatmap
    #plt.show()
    plt.tight_layout()
    
    plt.savefig(os.path.join('.\output', '{}.png'.format(title)))