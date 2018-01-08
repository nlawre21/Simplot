# Simplot
Plotly wrapper that sits on Pandas Dataframes for easier, prettier, and more customizable plotting capabilities.

## Install
This package will be on PyPi *soon*™

## Usage

`from simplot import Simplot`


`graph = Simplot(dataframe, 'This is a Test Plot')`

`graph.draw_axes(y_title='Y1', y2_title='Y2')`

`graph.bar('column1') # plot column on primary (default) axis`

`graph.line('column2', 2) # plot column on secondary y axis`

`graph.plot()` 

![img](https://github.com/nlawre21/Simplot/blob/add_to_readme/readme_example.png)
