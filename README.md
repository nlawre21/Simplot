# Simplot
Plotly wrapper that sits on Pandas Dataframes for easier, prettier, and more customizable plotting capabilities.

## Install
This package will be on PyPi *soon*™

## Usage

`from simplot import Simplot`

`graph = Simplot(dataframe, 'This is a Test Plot') # instantiate class, provide data, plot title, optional args for font-family and size`

`graph.draw_axes(y_title='Y1', y2_title='Y2') # draw axes, while not necessary it is good practice, can prevent formatting issues` 

`graph.bar('column1') # plot provided column name on left (default) axis` 

`graph.line('column2', 2) # plot provided column name on secondary y axis `

`graph.plot() # generate plot ` 
