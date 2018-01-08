# Simplot
Plotly wrapper that sits on Pandas Dataframes for easier, prettier, and more customizable plotting capabilities.

## Install
This package will be on PyPi *soon*™

## Usage

`from simplot import Simplot`

`graph = Simplot(dataframe, 'This is a Test Plot') # optional args for font-family and size`
`graph.draw_axes(y_title='Y1', y2_title='Y2') # while not necessary it is good practice, can prevent formatting issues`

`graph.bar('column1') # plot column on left (default) axis`

`graph.line('column2', 2) # plot column on secondary y axis`

`graph.plot() # generate plot` 
