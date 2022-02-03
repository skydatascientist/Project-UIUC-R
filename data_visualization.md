<p style="text-align: center;"> <span style="color:firebrick"> <font size="5"> <b> USC Marshall School of Business </b> </font> </p> </span> 

<p style="text-align: center;"> <b> <font font size="5"> DSO 545-Data Visualization  </p> </b></font>

<p style="text-align: center;"> <b> Fall 2020 </b> </p>



## <span style="color:blue"> Xiangyu Huang </span>


```python
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
```


```python
data1 = pd.read_csv('World.csv')
data1.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Year</th>
      <th>Energy Sector</th>
      <th>Carrier Type</th>
      <th>Final Energy Demand</th>
      <th>RE Share</th>
      <th>CumSumEnergy</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2015</td>
      <td>Transportation</td>
      <td>Electricity</td>
      <td>1503</td>
      <td>0.015467</td>
      <td>1503</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2020</td>
      <td>Transportation</td>
      <td>Electricity</td>
      <td>1855</td>
      <td>0.018480</td>
      <td>1855</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2025</td>
      <td>Transportation</td>
      <td>Electricity</td>
      <td>4930</td>
      <td>0.062231</td>
      <td>4930</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2030</td>
      <td>Transportation</td>
      <td>Electricity</td>
      <td>11034</td>
      <td>0.184887</td>
      <td>11034</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2035</td>
      <td>Transportation</td>
      <td>Electricity</td>
      <td>17582</td>
      <td>0.365423</td>
      <td>17582</td>
    </tr>
  </tbody>
</table>
</div>




```python
data1['label'] = None
def func1(x):
    return f'{round(100*x)}% electrification'
data1.loc[data1['Carrier Type'] == 'Electricity',['label']] = data1.loc[data1['Carrier Type'] == 'Electricity']['RE Share'].apply(lambda x: func1(x))
data1.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Year</th>
      <th>Energy Sector</th>
      <th>Carrier Type</th>
      <th>Final Energy Demand</th>
      <th>RE Share</th>
      <th>CumSumEnergy</th>
      <th>label</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2015</td>
      <td>Transportation</td>
      <td>Electricity</td>
      <td>1503</td>
      <td>0.015467</td>
      <td>1503</td>
      <td>2% electrification</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2020</td>
      <td>Transportation</td>
      <td>Electricity</td>
      <td>1855</td>
      <td>0.018480</td>
      <td>1855</td>
      <td>2% electrification</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2025</td>
      <td>Transportation</td>
      <td>Electricity</td>
      <td>4930</td>
      <td>0.062231</td>
      <td>4930</td>
      <td>6% electrification</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2030</td>
      <td>Transportation</td>
      <td>Electricity</td>
      <td>11034</td>
      <td>0.184887</td>
      <td>11034</td>
      <td>18% electrification</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2035</td>
      <td>Transportation</td>
      <td>Electricity</td>
      <td>17582</td>
      <td>0.365423</td>
      <td>17582</td>
      <td>37% electrification</td>
    </tr>
  </tbody>
</table>
</div>




```python
[(i,j) for i in data1['Energy Sector'].unique() for j in data1['Carrier Type'].unique()]
```




    [('Transportation', 'Electricity'),
     ('Transportation', 'Other Carrier'),
     ('Industry', 'Electricity'),
     ('Industry', 'Other Carrier'),
     ('Buildings/Others', 'Electricity'),
     ('Buildings/Others', 'Other Carrier')]




```python
[0]+data1[data1['Year'] == 2015][['CumSumEnergy','Carrier Type']]['CumSumEnergy'].tolist()[:5]
```




    [0, 1503, 97185, 127776, 210746, 251386]




```python
import plotly.graph_objects as go

x = data1['Year'].unique()
kind = [(i,j) for i in data1['Energy Sector'].unique() for j in data1['Carrier Type'].unique()]
fig = go.Figure()
clrs = ['rgb(160,200,255)','rgb(0,152,255)','lightgrey','#575d6d','rgb(247,104,161)','rgb(150,0,90)']
for count, trace in enumerate(kind):
    if count == 0:
        fill = 'tozeroy'
    else:
        fill = 'tonexty'
    if trace[1] == 'Electricity':
        md = 'markers'
    else:
        md = 'none'
    y = data1[(data1['Carrier Type'] == trace[1])&(data1['Energy Sector'] == trace[0])]['CumSumEnergy']
    fig.add_trace(go.Scatter(x=x, y=y, fill=fill, fillcolor = clrs[count],
                    mode=md, name = str(trace[0])+'-'+str(trace[1]),
                    text = data1[(data1['Carrier Type'] == trace[1])&(data1['Energy Sector'] == trace[0])]['label'],
                    marker = dict(size=3, color = 'white')))
ant = data1[(data1['Carrier Type'] == 'Other Carrier')&(data1['Year'] == 2015)][['CumSumEnergy','Energy Sector']].set_index('Energy Sector')
for anno in ant.index:
    fig.add_annotation(x=2015, align = 'left', y=ant.loc[anno,'CumSumEnergy'],
                text=f'<b>{anno}</b>',
                width = 200,
                showarrow=False,
                xshift=105,
                yshift = -20,
                font = dict(size = 15, color = 'white'),                
                )

for y,anno2 in zip([0]+data1[data1['Year'] == 2050][['CumSumEnergy','Carrier Type']]['CumSumEnergy'].tolist()[:5],
                  ['Electric power', 'On-board fuels', 'Electric power', 'On-site energy', 'Electric power', 'On-site energy']):        
    fig.add_annotation(x=2050, align = 'right', y=y,
                text=anno2,
                width = 200,
                showarrow=False,
                xshift=-105,
                yshift = 9,
                font = dict(size = 15, color = 'black'),                
                )
fig.update_layout(yaxis = dict(title = '<b>Final Energy Demand (PJ)<b>', showgrid = False, tickfont=dict(size=14),
                        ticktext=[str(i)+',000' for i in [50,100,150,200,250,300,350]], 
                        tickvals=[1000*i for i in [50,100,150,200,250,300,350]]),
                  xaxis =dict(showgrid = False),
                  plot_bgcolor = 'white',
                  showlegend=False)
for vl in [2020,2030,2040]:
    fig.add_shape(type="line", x0=vl, y0=0, x1=vl, y1=data1['CumSumEnergy'].max(),
        line=dict(color="white",width=1, dash = 'dash')
)
fig.update_layout(
    autosize=False,
    width=900,
    height=800)
fig.show()
```


<div>                            <div id="633cdfd8-ddc2-4030-b40f-10e52070f4c3" class="plotly-graph-div" style="height:800px; width:900px;"></div>            <script type="text/javascript">                require(["plotly"], function(Plotly) {                    window.PLOTLYENV=window.PLOTLYENV || {};                                    if (document.getElementById("633cdfd8-ddc2-4030-b40f-10e52070f4c3")) {                    Plotly.newPlot(                        "633cdfd8-ddc2-4030-b40f-10e52070f4c3",                        [{"fill":"tozeroy","fillcolor":"rgb(160,200,255)","marker":{"color":"white","size":3},"mode":"markers","name":"Transportation-Electricity","text":["2% electrification","2% electrification","6% electrification","18% electrification","37% electrification","45% electrification","48% electrification","50% electrification"],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[1503,1855,4930,11034,17582,19380,19142,18839],"type":"scatter"},{"fill":"tonexty","fillcolor":"rgb(0,152,255)","marker":{"color":"white","size":3},"mode":"none","name":"Transportation-Other Carrier","text":[null,null,null,null,null,null,null,null],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[97185,100395,79222,59680,48113,43435,40116,37710],"type":"scatter"},{"fill":"tonexty","fillcolor":"lightgrey","marker":{"color":"white","size":3},"mode":"markers","name":"Industry-Electricity","text":["27% electrification","28% electrification","33% electrification","40% electrification","47% electrification","51% electrification","54% electrification","58% electrification"],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[127776,134251,117232,102785,95282,93701,93601,94587],"type":"scatter"},{"fill":"tonexty","fillcolor":"#575d6d","marker":{"color":"white","size":3},"mode":"none","name":"Industry-Other Carrier","text":[null,null,null,null,null,null,null,null],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[210746,219912,192730,166868,148957,142684,138379,136282],"type":"scatter"},{"fill":"tonexty","fillcolor":"rgb(247,104,161)","marker":{"color":"white","size":3},"mode":"markers","name":"Buildings/Others-Electricity","text":["31% electrification","33% electrification","38% electrification","45% electrification","50% electrification","55% electrification","60% electrification","64% electrification"],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[251386,265095,241832,219388,205957,205446,207112,210720],"type":"scatter"},{"fill":"tonexty","fillcolor":"rgb(150,0,90)","marker":{"color":"white","size":3},"mode":"none","name":"Buildings/Others-Other Carrier","text":[null,null,null,null,null,null,null,null],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[341889,355100,320466,284145,262699,256844,253713,253150],"type":"scatter"}],                        {"template":{"data":{"bar":[{"error_x":{"color":"#2a3f5f"},"error_y":{"color":"#2a3f5f"},"marker":{"line":{"color":"#E5ECF6","width":0.5},"pattern":{"fillmode":"overlay","size":10,"solidity":0.2}},"type":"bar"}],"barpolar":[{"marker":{"line":{"color":"#E5ECF6","width":0.5},"pattern":{"fillmode":"overlay","size":10,"solidity":0.2}},"type":"barpolar"}],"carpet":[{"aaxis":{"endlinecolor":"#2a3f5f","gridcolor":"white","linecolor":"white","minorgridcolor":"white","startlinecolor":"#2a3f5f"},"baxis":{"endlinecolor":"#2a3f5f","gridcolor":"white","linecolor":"white","minorgridcolor":"white","startlinecolor":"#2a3f5f"},"type":"carpet"}],"choropleth":[{"colorbar":{"outlinewidth":0,"ticks":""},"type":"choropleth"}],"contour":[{"colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]],"type":"contour"}],"contourcarpet":[{"colorbar":{"outlinewidth":0,"ticks":""},"type":"contourcarpet"}],"heatmap":[{"colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]],"type":"heatmap"}],"heatmapgl":[{"colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]],"type":"heatmapgl"}],"histogram":[{"marker":{"pattern":{"fillmode":"overlay","size":10,"solidity":0.2}},"type":"histogram"}],"histogram2d":[{"colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]],"type":"histogram2d"}],"histogram2dcontour":[{"colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]],"type":"histogram2dcontour"}],"mesh3d":[{"colorbar":{"outlinewidth":0,"ticks":""},"type":"mesh3d"}],"parcoords":[{"line":{"colorbar":{"outlinewidth":0,"ticks":""}},"type":"parcoords"}],"pie":[{"automargin":true,"type":"pie"}],"scatter":[{"marker":{"colorbar":{"outlinewidth":0,"ticks":""}},"type":"scatter"}],"scatter3d":[{"line":{"colorbar":{"outlinewidth":0,"ticks":""}},"marker":{"colorbar":{"outlinewidth":0,"ticks":""}},"type":"scatter3d"}],"scattercarpet":[{"marker":{"colorbar":{"outlinewidth":0,"ticks":""}},"type":"scattercarpet"}],"scattergeo":[{"marker":{"colorbar":{"outlinewidth":0,"ticks":""}},"type":"scattergeo"}],"scattergl":[{"marker":{"colorbar":{"outlinewidth":0,"ticks":""}},"type":"scattergl"}],"scattermapbox":[{"marker":{"colorbar":{"outlinewidth":0,"ticks":""}},"type":"scattermapbox"}],"scatterpolar":[{"marker":{"colorbar":{"outlinewidth":0,"ticks":""}},"type":"scatterpolar"}],"scatterpolargl":[{"marker":{"colorbar":{"outlinewidth":0,"ticks":""}},"type":"scatterpolargl"}],"scatterternary":[{"marker":{"colorbar":{"outlinewidth":0,"ticks":""}},"type":"scatterternary"}],"surface":[{"colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]],"type":"surface"}],"table":[{"cells":{"fill":{"color":"#EBF0F8"},"line":{"color":"white"}},"header":{"fill":{"color":"#C8D4E3"},"line":{"color":"white"}},"type":"table"}]},"layout":{"annotationdefaults":{"arrowcolor":"#2a3f5f","arrowhead":0,"arrowwidth":1},"autotypenumbers":"strict","coloraxis":{"colorbar":{"outlinewidth":0,"ticks":""}},"colorscale":{"diverging":[[0,"#8e0152"],[0.1,"#c51b7d"],[0.2,"#de77ae"],[0.3,"#f1b6da"],[0.4,"#fde0ef"],[0.5,"#f7f7f7"],[0.6,"#e6f5d0"],[0.7,"#b8e186"],[0.8,"#7fbc41"],[0.9,"#4d9221"],[1,"#276419"]],"sequential":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]],"sequentialminus":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]},"colorway":["#636efa","#EF553B","#00cc96","#ab63fa","#FFA15A","#19d3f3","#FF6692","#B6E880","#FF97FF","#FECB52"],"font":{"color":"#2a3f5f"},"geo":{"bgcolor":"white","lakecolor":"white","landcolor":"#E5ECF6","showlakes":true,"showland":true,"subunitcolor":"white"},"hoverlabel":{"align":"left"},"hovermode":"closest","mapbox":{"style":"light"},"paper_bgcolor":"white","plot_bgcolor":"#E5ECF6","polar":{"angularaxis":{"gridcolor":"white","linecolor":"white","ticks":""},"bgcolor":"#E5ECF6","radialaxis":{"gridcolor":"white","linecolor":"white","ticks":""}},"scene":{"xaxis":{"backgroundcolor":"#E5ECF6","gridcolor":"white","gridwidth":2,"linecolor":"white","showbackground":true,"ticks":"","zerolinecolor":"white"},"yaxis":{"backgroundcolor":"#E5ECF6","gridcolor":"white","gridwidth":2,"linecolor":"white","showbackground":true,"ticks":"","zerolinecolor":"white"},"zaxis":{"backgroundcolor":"#E5ECF6","gridcolor":"white","gridwidth":2,"linecolor":"white","showbackground":true,"ticks":"","zerolinecolor":"white"}},"shapedefaults":{"line":{"color":"#2a3f5f"}},"ternary":{"aaxis":{"gridcolor":"white","linecolor":"white","ticks":""},"baxis":{"gridcolor":"white","linecolor":"white","ticks":""},"bgcolor":"#E5ECF6","caxis":{"gridcolor":"white","linecolor":"white","ticks":""}},"title":{"x":0.05},"xaxis":{"automargin":true,"gridcolor":"white","linecolor":"white","ticks":"","title":{"standoff":15},"zerolinecolor":"white","zerolinewidth":2},"yaxis":{"automargin":true,"gridcolor":"white","linecolor":"white","ticks":"","title":{"standoff":15},"zerolinecolor":"white","zerolinewidth":2}}},"annotations":[{"align":"left","font":{"color":"white","size":15},"showarrow":false,"text":"<b>Transportation</b>","width":200,"x":2015,"xshift":105,"y":97185,"yshift":-20},{"align":"left","font":{"color":"white","size":15},"showarrow":false,"text":"<b>Industry</b>","width":200,"x":2015,"xshift":105,"y":210746,"yshift":-20},{"align":"left","font":{"color":"white","size":15},"showarrow":false,"text":"<b>Buildings/Others</b>","width":200,"x":2015,"xshift":105,"y":341889,"yshift":-20},{"align":"right","font":{"color":"black","size":15},"showarrow":false,"text":"Electric power","width":200,"x":2050,"xshift":-105,"y":0,"yshift":9},{"align":"right","font":{"color":"black","size":15},"showarrow":false,"text":"On-board fuels","width":200,"x":2050,"xshift":-105,"y":18839,"yshift":9},{"align":"right","font":{"color":"black","size":15},"showarrow":false,"text":"Electric power","width":200,"x":2050,"xshift":-105,"y":37710,"yshift":9},{"align":"right","font":{"color":"black","size":15},"showarrow":false,"text":"On-site energy","width":200,"x":2050,"xshift":-105,"y":94587,"yshift":9},{"align":"right","font":{"color":"black","size":15},"showarrow":false,"text":"Electric power","width":200,"x":2050,"xshift":-105,"y":136282,"yshift":9},{"align":"right","font":{"color":"black","size":15},"showarrow":false,"text":"On-site energy","width":200,"x":2050,"xshift":-105,"y":210720,"yshift":9}],"yaxis":{"tickfont":{"size":14},"title":{"text":"<b>Final Energy Demand (PJ)<b>"},"showgrid":false,"ticktext":["50,000","100,000","150,000","200,000","250,000","300,000","350,000"],"tickvals":[50000,100000,150000,200000,250000,300000,350000]},"xaxis":{"showgrid":false},"plot_bgcolor":"white","showlegend":false,"shapes":[{"line":{"color":"white","dash":"dash","width":1},"type":"line","x0":2020,"x1":2020,"y0":0,"y1":355100},{"line":{"color":"white","dash":"dash","width":1},"type":"line","x0":2030,"x1":2030,"y0":0,"y1":355100},{"line":{"color":"white","dash":"dash","width":1},"type":"line","x0":2040,"x1":2040,"y0":0,"y1":355100}],"autosize":false,"width":900,"height":800},                        {"responsive": true}                    ).then(function(){

var gd = document.getElementById('633cdfd8-ddc2-4030-b40f-10e52070f4c3');
var x = new MutationObserver(function (mutations, observer) {{
        var display = window.getComputedStyle(gd).display;
        if (!display || display === 'none') {{
            console.log([gd, 'removed!']);
            Plotly.purge(gd);
            observer.disconnect();
        }}
}});

// Listen for the removal of the full notebook cells
var notebookContainer = gd.closest('#notebook-container');
if (notebookContainer) {{
    x.observe(notebookContainer, {childList: true});
}}

// Listen for the clearing of the current output cell
var outputEl = gd.closest('.output');
if (outputEl) {{
    x.observe(outputEl, {childList: true});
}}

                        })                };                });            </script>        </div>


**Code for Figure 2:**


```python
cleandf = pd.read_csv('World.csv')
cleandf.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Year</th>
      <th>Energy Sector</th>
      <th>Carrier Type</th>
      <th>Final Energy Demand</th>
      <th>RE Share</th>
      <th>CumSumEnergy</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2015</td>
      <td>Transportation</td>
      <td>Electricity</td>
      <td>1503</td>
      <td>0.015467</td>
      <td>1503</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2020</td>
      <td>Transportation</td>
      <td>Electricity</td>
      <td>1855</td>
      <td>0.018480</td>
      <td>1855</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2025</td>
      <td>Transportation</td>
      <td>Electricity</td>
      <td>4930</td>
      <td>0.062231</td>
      <td>4930</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2030</td>
      <td>Transportation</td>
      <td>Electricity</td>
      <td>11034</td>
      <td>0.184887</td>
      <td>11034</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2035</td>
      <td>Transportation</td>
      <td>Electricity</td>
      <td>17582</td>
      <td>0.365423</td>
      <td>17582</td>
    </tr>
  </tbody>
</table>
</div>




```python
df1 = pd.read_csv('data_for_pic2.csv', index_col = 0)
df2 = pd.read_csv('data_for_pic2_partb.csv', index_col = 0)
```


```python

x = df1['year'].unique()
kind = [(i,j) for i in df1['Sector'].unique() for j in df1['Category'].unique()]
fig = go.Figure()
clrs = []
black_clrs = []
for i in range(len(kind)):
    clrs.append(f'rgb({np.random.randint(0,200)},{np.random.randint(100,200)},{np.random.randint(100,200)})')
for i in range(20):
    black_clrs.append(f'rgb({10*i},{10*i},{10*i})')
FF_count = 0
for count, trace in enumerate(kind):
    if count == 0:
        fill = 'tozeroy'
    else:
        fill = 'tonexty'

    y = df1[(df1['Category'] == trace[1])&(df1['Sector'] == trace[0])]['CumSumEnergy']
    if trace[0] == 'FFs':
        color_to_fill = black_clrs[FF_count]
        FF_count += 1
    else:
        color_to_fill = clrs[count]
    
    fig.add_trace(go.Scatter(x=x, y=y, fill=fill, fillcolor = color_to_fill,
                    mode='none', 
                    name = str(trace[0])+'-'+str(trace[1]),
                    text = df2[(df2['Carrier Type'] == trace[0])]['percentage'].apply(lambda x: f'{round(x*100, 2)}%').values,
                    marker = dict(size=3, color = 'white')))
    
ant1 = df1[(df1['Sector'] == 'FFs')&(df1['year'] == 2015)][['CumSumEnergy','Category']].set_index('Category')
for anno in ant1.index:
    fig.add_annotation(x=2015, align = 'left', y=ant1.loc[anno,'CumSumEnergy'],
                text=f'<b>{anno}</b>',
                width = 200,
                showarrow=False,
                xshift=105,
                yshift = -20,
                font = dict(size = 15, color = 'white'),                
                )
ant2 = df1[(df1['Sector'] != 'FFs')&(df1['year'] == 2050)][['CumSumEnergy','Category']].set_index('Category')
print_dict = {'Synfuels':'RE Fuel', 'RE District heat':'RE District', 'H Process':'Hydrogen', 'Geothermal':'Geothermal', 
 'Biomass':'Biomass',
 'Solar Heat': 'Solar Heat',
 'Hydro Power': 'Hydro',
 'Wind':'Wind',
 'Geothermal Power': 'Geothermal',
 'Solar thermal power plants': 'Solar CSP',
'PV': 'Solar PV'}

for i in range(len(ant2.index)):
    anno = ant2.index.values[i]
    prev_anno = ant2.index.values[i-1]
    if anno in print_dict.keys():
        if i != 1:
            height_val = np.mean([ant2.loc[anno,'CumSumEnergy'], ant2.loc[prev_anno,'CumSumEnergy']])
        else:
            height_val = ant2.loc[anno,'CumSumEnergy']
        fig.add_annotation(x=2050, align = 'right', y= height_val,
                    text=f'<b>{print_dict[anno]}</b>',
                    width = 200,
                    showarrow=False,
                    xshift= -105,
                    yshift = 0,
                    font = dict(size = 15, color = 'white'),                
                    )

fig.update_layout(yaxis = dict(title = '<b>Final Energy Demand (PJ)<b>', showgrid = False, tickfont=dict(size=14),
                        ticktext=[str(i)+',000' for i in [50,100,150,200,250,300,350]], 
                        tickvals=[1000*i for i in [50,100,150,200,250,300,350]]),
                  xaxis =dict(showgrid = False),
                  plot_bgcolor = 'white',
                  showlegend=False)
for vl in [2020,2030,2040]:
    fig.add_shape(type="line", x0=vl, y0=0, x1=vl, y1=df1['CumSumEnergy'].max(),
        line=dict(color="white",width=1, dash = 'dash')
)
    
cat_h_dict = df1.groupby(['year','Sector']).CumSumEnergy.max()
Direct_hs = []
Electric_hs = []
for year in [2020,2030,2040]:
    Direct_h = cat_h_dict.loc[year, 'FFs']
    Direct_hs.append(Direct_h)
    Electric_h = cat_h_dict.loc[year, 'POWER']
    Electric_hs.append(Electric_h)
    pct_D = int(df2[(df2['Carrier Type'] == 'OTHER HEAT')&(df2['year']==year)].percentage.values[0]*100)
    fig.add_annotation(x=year, align = 'center', y= Direct_h,
                    text=f'<b>Direct E: {pct_D}%</b>',
                    width = 200,
                    showarrow=False,
                    xshift= 20,
                    yshift = -20,
                    font = dict(size = 12, color = 'white'),                
                    )
    pct_E = int(df2[(df2['Carrier Type'] == 'POWER')&(df2['year']==year)].percentage.values[0]*100)
    fig.add_annotation(x=year, align = 'center', y= Electric_h,
                    
                    text=f'<b>Electricity E: {pct_D}%</b>',
                    width = 200,
                    showarrow=False,
                    xshift= 20,
                    yshift = -20,
                    font = dict(size = 12, color = 'white')     
                    )
fig.add_trace(
    go.Scatter(
        x = [2020,2030,2040],
        y = Direct_hs,
        mode = 'markers',
        marker = dict(size=8, color = 'white'))  
)
fig.add_trace(
    go.Scatter(
        x = [2020,2030,2040],
        y = Electric_hs,
        mode = 'markers',
        marker = dict(size=8, color = 'white'))
)

fig.update_layout(
    title = 'Global Expansion of Renewables to Achieve the 1.5C Goal',
    autosize=False,
    width=800,
    height=800)
fig.show()
```


<div>                            <div id="5f964799-81f6-44e8-aa1b-50869581e4a6" class="plotly-graph-div" style="height:800px; width:800px;"></div>            <script type="text/javascript">                require(["plotly"], function(Plotly) {                    window.PLOTLYENV=window.PLOTLYENV || {};                                    if (document.getElementById("5f964799-81f6-44e8-aa1b-50869581e4a6")) {                    Plotly.newPlot(                        "5f964799-81f6-44e8-aa1b-50869581e4a6",                        [{"fill":"tozeroy","fillcolor":"rgb(63,140,111)","marker":{"color":"white","size":3},"mode":"none","name":"POWER-Nuclear","text":["22.81%","29.16%","50.64%","72.81%","86.14%","94.09%","98.0%","100.0%"],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[7628.561970877593,8851.746127484423,6888.446690041118,4390.1277669980445,2233.9026493036363,439.89453253091847,27.21993767287694,0.0],"type":"scatter"},{"fill":"tonexty","fillcolor":"rgb(47,195,161)","marker":{"color":"white","size":3},"mode":"none","name":"POWER-Hydrogen Power","text":["22.81%","29.16%","50.64%","72.81%","86.14%","94.09%","98.0%","100.0%"],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[7628.561970877593,8853.079678226082,6991.452639616799,5171.338466741594,4252.223324034787,4619.061967907302,6036.4900938531455,7189.227035741623],"type":"scatter"},{"fill":"tonexty","fillcolor":"rgb(27,136,143)","marker":{"color":"white","size":3},"mode":"none","name":"POWER-Hydro Power","text":["22.81%","29.16%","50.64%","72.81%","86.14%","94.09%","98.0%","100.0%"],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[19285.380479895703,21881.597652504846,20688.805922541484,18570.346191749377,17009.296755854506,16288.147619881627,17265.51497031703,18656.525913276284],"type":"scatter"},{"fill":"tonexty","fillcolor":"rgb(171,121,149)","marker":{"color":"white","size":3},"mode":"none","name":"POWER-Wind","text":["22.81%","29.16%","50.64%","72.81%","86.14%","94.09%","98.0%","100.0%"],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[21797.7157854036,26562.90629921781,34334.68670581134,44826.98642179952,53776.52682171976,59054.77634104194,63748.613678036505,68234.97459455578],"type":"scatter"},{"fill":"tonexty","fillcolor":"rgb(199,177,110)","marker":{"color":"white","size":3},"mode":"none","name":"POWER-PV","text":["22.81%","29.16%","50.64%","72.81%","86.14%","94.09%","98.0%","100.0%"],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[22536.90950911168,29504.082767921063,46331.07043975182,66641.20959375372,84428.73316043206,96922.43660626867,106058.46133645708,113549.35234627356],"type":"scatter"},{"fill":"tonexty","fillcolor":"rgb(68,125,111)","marker":{"color":"white","size":3},"mode":"none","name":"POWER-Biomass Power","text":["22.81%","29.16%","50.64%","72.81%","86.14%","94.09%","98.0%","100.0%"],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[23947.454339958447,31998.822817882115,51460.61435295567,73614.2255570337,91638.02032757658,104018.9177987218,113277.23455509846,121093.2001885308],"type":"scatter"},{"fill":"tonexty","fillcolor":"rgb(27,197,189)","marker":{"color":"white","size":3},"mode":"none","name":"POWER-Geothermal Power","text":["22.81%","29.16%","50.64%","72.81%","86.14%","94.09%","98.0%","100.0%"],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[24188.63589112978,32341.636282403026,52418.96586073863,76244.68107518973,95855.62680803372,109501.29093418524,119792.5210652278,128733.9508962314],"type":"scatter"},{"fill":"tonexty","fillcolor":"rgb(64,138,191)","marker":{"color":"white","size":3},"mode":"none","name":"POWER-Solar thermal power plants","text":["22.81%","29.16%","50.64%","72.81%","86.14%","94.09%","98.0%","100.0%"],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[24216.816209103807,32437.56101188836,53371.19186678648,81557.76552605433,106001.61655131965,123316.20534459958,136287.98628616886,147446.1815883853],"type":"scatter"},{"fill":"tonexty","fillcolor":"rgb(65,157,179)","marker":{"color":"white","size":3},"mode":"none","name":"POWER-Ocean energy","text":["22.81%","29.16%","50.64%","72.81%","86.14%","94.09%","98.0%","100.0%"],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[24219.84409433293,32443.955993854048,53495.62183486857,82044.7656771052,107114.00878118792,125021.41367194014,138553.80592151522,150154.44999999998],"type":"scatter"},{"fill":"tonexty","fillcolor":"rgb(13,122,160)","marker":{"color":"white","size":3},"mode":"none","name":"POWER-Coal & Lignite","text":["22.81%","29.16%","50.64%","72.81%","86.14%","94.09%","98.0%","100.0%"],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[],"type":"scatter"},{"fill":"tonexty","fillcolor":"rgb(53,101,111)","marker":{"color":"white","size":3},"mode":"none","name":"POWER-Gas","text":["22.81%","29.16%","50.64%","72.81%","86.14%","94.09%","98.0%","100.0%"],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[],"type":"scatter"},{"fill":"tonexty","fillcolor":"rgb(38,150,110)","marker":{"color":"white","size":3},"mode":"none","name":"POWER-Oil & Diesel","text":["22.81%","29.16%","50.64%","72.81%","86.14%","94.09%","98.0%","100.0%"],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[],"type":"scatter"},{"fill":"tonexty","fillcolor":"rgb(189,184,127)","marker":{"color":"white","size":3},"mode":"none","name":"POWER-Solar Heat","text":["22.81%","29.16%","50.64%","72.81%","86.14%","94.09%","98.0%","100.0%"],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[],"type":"scatter"},{"fill":"tonexty","fillcolor":"rgb(32,122,172)","marker":{"color":"white","size":3},"mode":"none","name":"POWER-Biomass","text":["22.81%","29.16%","50.64%","72.81%","86.14%","94.09%","98.0%","100.0%"],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[],"type":"scatter"},{"fill":"tonexty","fillcolor":"rgb(172,165,180)","marker":{"color":"white","size":3},"mode":"none","name":"POWER-Geothermal","text":["22.81%","29.16%","50.64%","72.81%","86.14%","94.09%","98.0%","100.0%"],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[],"type":"scatter"},{"fill":"tonexty","fillcolor":"rgb(172,161,102)","marker":{"color":"white","size":3},"mode":"none","name":"POWER-H Process","text":["22.81%","29.16%","50.64%","72.81%","86.14%","94.09%","98.0%","100.0%"],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[],"type":"scatter"},{"fill":"tonexty","fillcolor":"rgb(150,151,126)","marker":{"color":"white","size":3},"mode":"none","name":"POWER-RE district heat","text":["22.81%","29.16%","50.64%","72.81%","86.14%","94.09%","98.0%","100.0%"],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[],"type":"scatter"},{"fill":"tonexty","fillcolor":"rgb(191,136,167)","marker":{"color":"white","size":3},"mode":"none","name":"POWER-Biofuels","text":["22.81%","29.16%","50.64%","72.81%","86.14%","94.09%","98.0%","100.0%"],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[],"type":"scatter"},{"fill":"tonexty","fillcolor":"rgb(169,174,182)","marker":{"color":"white","size":3},"mode":"none","name":"POWER-Synfuels","text":["22.81%","29.16%","50.64%","72.81%","86.14%","94.09%","98.0%","100.0%"],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[],"type":"scatter"},{"fill":"tonexty","fillcolor":"rgb(10,100,107)","marker":{"color":"white","size":3},"mode":"none","name":"POWER-H Fuel","text":["22.81%","29.16%","50.64%","72.81%","86.14%","94.09%","98.0%","100.0%"],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[],"type":"scatter"},{"fill":"tonexty","fillcolor":"rgb(0,0,0)","marker":{"color":"white","size":3},"mode":"none","name":"FFs-Nuclear","text":[],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[],"type":"scatter"},{"fill":"tonexty","fillcolor":"rgb(10,10,10)","marker":{"color":"white","size":3},"mode":"none","name":"FFs-Hydrogen Power","text":[],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[],"type":"scatter"},{"fill":"tonexty","fillcolor":"rgb(20,20,20)","marker":{"color":"white","size":3},"mode":"none","name":"FFs-Hydro Power","text":[],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[],"type":"scatter"},{"fill":"tonexty","fillcolor":"rgb(30,30,30)","marker":{"color":"white","size":3},"mode":"none","name":"FFs-Wind","text":[],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[],"type":"scatter"},{"fill":"tonexty","fillcolor":"rgb(40,40,40)","marker":{"color":"white","size":3},"mode":"none","name":"FFs-PV","text":[],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[],"type":"scatter"},{"fill":"tonexty","fillcolor":"rgb(50,50,50)","marker":{"color":"white","size":3},"mode":"none","name":"FFs-Biomass Power","text":[],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[],"type":"scatter"},{"fill":"tonexty","fillcolor":"rgb(60,60,60)","marker":{"color":"white","size":3},"mode":"none","name":"FFs-Geothermal Power","text":[],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[],"type":"scatter"},{"fill":"tonexty","fillcolor":"rgb(70,70,70)","marker":{"color":"white","size":3},"mode":"none","name":"FFs-Solar thermal power plants","text":[],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[],"type":"scatter"},{"fill":"tonexty","fillcolor":"rgb(80,80,80)","marker":{"color":"white","size":3},"mode":"none","name":"FFs-Ocean energy","text":[],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[],"type":"scatter"},{"fill":"tonexty","fillcolor":"rgb(90,90,90)","marker":{"color":"white","size":3},"mode":"none","name":"FFs-Coal & Lignite","text":[],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[92429.6540227016,94931.05104874002,91662.03041051692,97519.01091349372,110381.6379397722,125965.1003386068,138890.83925484854,150154.45666666664],"type":"scatter"},{"fill":"tonexty","fillcolor":"rgb(100,100,100)","marker":{"color":"white","size":3},"mode":"none","name":"FFs-Gas","text":[],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[170325.05993802173,179028.1954203903,169641.51215492387,158976.0578916959,153651.3510869689,149891.24922047672,147270.59954056388,150154.4633333333],"type":"scatter"},{"fill":"tonexty","fillcolor":"rgb(110,110,110)","marker":{"color":"white","size":3},"mode":"none","name":"FFs-Oil & Diesel","text":[],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[296052.82,304475.12969202857,252931.59,202173.19896913637,170078.47310268565,154945.41419661892,147908.2828738972,150154.46999999994],"type":"scatter"},{"fill":"tonexty","fillcolor":"rgb(120,120,120)","marker":{"color":"white","size":3},"mode":"none","name":"FFs-Solar Heat","text":[],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[],"type":"scatter"},{"fill":"tonexty","fillcolor":"rgb(130,130,130)","marker":{"color":"white","size":3},"mode":"none","name":"FFs-Biomass","text":[],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[],"type":"scatter"},{"fill":"tonexty","fillcolor":"rgb(140,140,140)","marker":{"color":"white","size":3},"mode":"none","name":"FFs-Geothermal","text":[],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[],"type":"scatter"},{"fill":"tonexty","fillcolor":"rgb(150,150,150)","marker":{"color":"white","size":3},"mode":"none","name":"FFs-H Process","text":[],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[],"type":"scatter"},{"fill":"tonexty","fillcolor":"rgb(160,160,160)","marker":{"color":"white","size":3},"mode":"none","name":"FFs-RE district heat","text":[],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[],"type":"scatter"},{"fill":"tonexty","fillcolor":"rgb(170,170,170)","marker":{"color":"white","size":3},"mode":"none","name":"FFs-Biofuels","text":[],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[],"type":"scatter"},{"fill":"tonexty","fillcolor":"rgb(180,180,180)","marker":{"color":"white","size":3},"mode":"none","name":"FFs-Synfuels","text":[],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[],"type":"scatter"},{"fill":"tonexty","fillcolor":"rgb(190,190,190)","marker":{"color":"white","size":3},"mode":"none","name":"FFs-H Fuel","text":[],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[],"type":"scatter"},{"fill":"tonexty","fillcolor":"rgb(89,157,187)","marker":{"color":"white","size":3},"mode":"none","name":"OTHER HEAT-Nuclear","text":["17.03%","18.46%","29.57%","46.18%","65.71%","81.89%","94.17%","100.0%"],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[],"type":"scatter"},{"fill":"tonexty","fillcolor":"rgb(83,195,152)","marker":{"color":"white","size":3},"mode":"none","name":"OTHER HEAT-Hydrogen Power","text":["17.03%","18.46%","29.57%","46.18%","65.71%","81.89%","94.17%","100.0%"],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[],"type":"scatter"},{"fill":"tonexty","fillcolor":"rgb(190,113,145)","marker":{"color":"white","size":3},"mode":"none","name":"OTHER HEAT-Hydro Power","text":["17.03%","18.46%","29.57%","46.18%","65.71%","81.89%","94.17%","100.0%"],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[],"type":"scatter"},{"fill":"tonexty","fillcolor":"rgb(42,182,194)","marker":{"color":"white","size":3},"mode":"none","name":"OTHER HEAT-Wind","text":["17.03%","18.46%","29.57%","46.18%","65.71%","81.89%","94.17%","100.0%"],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[],"type":"scatter"},{"fill":"tonexty","fillcolor":"rgb(137,139,127)","marker":{"color":"white","size":3},"mode":"none","name":"OTHER HEAT-PV","text":["17.03%","18.46%","29.57%","46.18%","65.71%","81.89%","94.17%","100.0%"],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[],"type":"scatter"},{"fill":"tonexty","fillcolor":"rgb(94,149,197)","marker":{"color":"white","size":3},"mode":"none","name":"OTHER HEAT-Biomass Power","text":["17.03%","18.46%","29.57%","46.18%","65.71%","81.89%","94.17%","100.0%"],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[],"type":"scatter"},{"fill":"tonexty","fillcolor":"rgb(79,185,159)","marker":{"color":"white","size":3},"mode":"none","name":"OTHER HEAT-Geothermal Power","text":["17.03%","18.46%","29.57%","46.18%","65.71%","81.89%","94.17%","100.0%"],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[],"type":"scatter"},{"fill":"tonexty","fillcolor":"rgb(9,158,189)","marker":{"color":"white","size":3},"mode":"none","name":"OTHER HEAT-Solar thermal power plants","text":["17.03%","18.46%","29.57%","46.18%","65.71%","81.89%","94.17%","100.0%"],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[],"type":"scatter"},{"fill":"tonexty","fillcolor":"rgb(49,126,178)","marker":{"color":"white","size":3},"mode":"none","name":"OTHER HEAT-Ocean energy","text":["17.03%","18.46%","29.57%","46.18%","65.71%","81.89%","94.17%","100.0%"],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[],"type":"scatter"},{"fill":"tonexty","fillcolor":"rgb(80,168,193)","marker":{"color":"white","size":3},"mode":"none","name":"OTHER HEAT-Coal & Lignite","text":["17.03%","18.46%","29.57%","46.18%","65.71%","81.89%","94.17%","100.0%"],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[],"type":"scatter"},{"fill":"tonexty","fillcolor":"rgb(125,109,115)","marker":{"color":"white","size":3},"mode":"none","name":"OTHER HEAT-Gas","text":["17.03%","18.46%","29.57%","46.18%","65.71%","81.89%","94.17%","100.0%"],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[],"type":"scatter"},{"fill":"tonexty","fillcolor":"rgb(61,131,141)","marker":{"color":"white","size":3},"mode":"none","name":"OTHER HEAT-Oil & Diesel","text":["17.03%","18.46%","29.57%","46.18%","65.71%","81.89%","94.17%","100.0%"],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[],"type":"scatter"},{"fill":"tonexty","fillcolor":"rgb(78,143,135)","marker":{"color":"white","size":3},"mode":"none","name":"OTHER HEAT-Solar Heat","text":["17.03%","18.46%","29.57%","46.18%","65.71%","81.89%","94.17%","100.0%"],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[297297.74,306739.9596920286,259937.07,215344.73896913635,187327.79310268565,174832.35419661892,169775.2728738972,173237.93999999994],"type":"scatter"},{"fill":"tonexty","fillcolor":"rgb(103,105,149)","marker":{"color":"white","size":3},"mode":"none","name":"OTHER HEAT-Biomass","text":["17.03%","18.46%","29.57%","46.18%","65.71%","81.89%","94.17%","100.0%"],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[337799.89,348677.81969202857,303315.94,256550.2889691364,224283.3031026857,207048.2141966189,195955.1428738972,193548.19999999995],"type":"scatter"},{"fill":"tonexty","fillcolor":"rgb(24,166,162)","marker":{"color":"white","size":3},"mode":"none","name":"OTHER HEAT-Geothermal","text":["17.03%","18.46%","29.57%","46.18%","65.71%","81.89%","94.17%","100.0%"],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[338162.61,349470.4696920286,306046.29,262235.9189691364,232693.68310268567,217635.51419661893,208966.7628738972,208929.02999999997],"type":"scatter"},{"fill":"tonexty","fillcolor":"rgb(193,193,147)","marker":{"color":"white","size":3},"mode":"none","name":"OTHER HEAT-H Process","text":["17.03%","18.46%","29.57%","46.18%","65.71%","81.89%","94.17%","100.0%"],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[338162.61,349470.4696920286,306166.8,263771.07896913635,236425.7031026857,225793.0741966189,220986.7628738972,221187.25999999995],"type":"scatter"},{"fill":"tonexty","fillcolor":"rgb(119,176,124)","marker":{"color":"white","size":3},"mode":"none","name":"OTHER HEAT-RE district heat","text":["17.03%","18.46%","29.57%","46.18%","65.71%","81.89%","94.17%","100.0%"],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[338725.72,350958.7696920286,310305.84,270657.14896913635,245672.43310268567,236752.04419661887,233119.9628738972,234279.25999999995],"type":"scatter"},{"fill":"tonexty","fillcolor":"rgb(189,138,104)","marker":{"color":"white","size":3},"mode":"none","name":"OTHER HEAT-Biofuels","text":["17.03%","18.46%","29.57%","46.18%","65.71%","81.89%","94.17%","100.0%"],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[341888.99,355082.6996920286,319635.25999999995,280711.89896913635,255453.96310268567,245984.1941966189,241320.9928738972,239972.36999999997],"type":"scatter"},{"fill":"tonexty","fillcolor":"rgb(18,151,177)","marker":{"color":"white","size":3},"mode":"none","name":"OTHER HEAT-Synfuels","text":["17.03%","18.46%","29.57%","46.18%","65.71%","81.89%","94.17%","100.0%"],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[341888.99,355084.5096920286,319640.25999999995,281115.8389691364,257569.29310268565,250535.0341966189,246949.7428738972,246300.84999999995],"type":"scatter"},{"fill":"tonexty","fillcolor":"rgb(54,114,122)","marker":{"color":"white","size":3},"mode":"none","name":"OTHER HEAT-H Fuel","text":["17.03%","18.46%","29.57%","46.18%","65.71%","81.89%","94.17%","100.0%"],"x":[2015,2020,2025,2030,2035,2040,2045,2050],"y":[341888.99,355100.7796920286,320467.12999999995,284144.89896913635,262699.48310268566,256843.0241966189,253713.6128738972,253149.92999999996],"type":"scatter"},{"marker":{"color":"white","size":8},"mode":"markers","x":[2020,2030,2040],"y":[304475.12969202857,202173.19896913637,154945.41419661892],"type":"scatter"},{"marker":{"color":"white","size":8},"mode":"markers","x":[2020,2030,2040],"y":[32443.955993854048,82044.7656771052,125021.41367194014],"type":"scatter"}],                        {"template":{"data":{"bar":[{"error_x":{"color":"#2a3f5f"},"error_y":{"color":"#2a3f5f"},"marker":{"line":{"color":"#E5ECF6","width":0.5},"pattern":{"fillmode":"overlay","size":10,"solidity":0.2}},"type":"bar"}],"barpolar":[{"marker":{"line":{"color":"#E5ECF6","width":0.5},"pattern":{"fillmode":"overlay","size":10,"solidity":0.2}},"type":"barpolar"}],"carpet":[{"aaxis":{"endlinecolor":"#2a3f5f","gridcolor":"white","linecolor":"white","minorgridcolor":"white","startlinecolor":"#2a3f5f"},"baxis":{"endlinecolor":"#2a3f5f","gridcolor":"white","linecolor":"white","minorgridcolor":"white","startlinecolor":"#2a3f5f"},"type":"carpet"}],"choropleth":[{"colorbar":{"outlinewidth":0,"ticks":""},"type":"choropleth"}],"contour":[{"colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]],"type":"contour"}],"contourcarpet":[{"colorbar":{"outlinewidth":0,"ticks":""},"type":"contourcarpet"}],"heatmap":[{"colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]],"type":"heatmap"}],"heatmapgl":[{"colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]],"type":"heatmapgl"}],"histogram":[{"marker":{"pattern":{"fillmode":"overlay","size":10,"solidity":0.2}},"type":"histogram"}],"histogram2d":[{"colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]],"type":"histogram2d"}],"histogram2dcontour":[{"colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]],"type":"histogram2dcontour"}],"mesh3d":[{"colorbar":{"outlinewidth":0,"ticks":""},"type":"mesh3d"}],"parcoords":[{"line":{"colorbar":{"outlinewidth":0,"ticks":""}},"type":"parcoords"}],"pie":[{"automargin":true,"type":"pie"}],"scatter":[{"marker":{"colorbar":{"outlinewidth":0,"ticks":""}},"type":"scatter"}],"scatter3d":[{"line":{"colorbar":{"outlinewidth":0,"ticks":""}},"marker":{"colorbar":{"outlinewidth":0,"ticks":""}},"type":"scatter3d"}],"scattercarpet":[{"marker":{"colorbar":{"outlinewidth":0,"ticks":""}},"type":"scattercarpet"}],"scattergeo":[{"marker":{"colorbar":{"outlinewidth":0,"ticks":""}},"type":"scattergeo"}],"scattergl":[{"marker":{"colorbar":{"outlinewidth":0,"ticks":""}},"type":"scattergl"}],"scattermapbox":[{"marker":{"colorbar":{"outlinewidth":0,"ticks":""}},"type":"scattermapbox"}],"scatterpolar":[{"marker":{"colorbar":{"outlinewidth":0,"ticks":""}},"type":"scatterpolar"}],"scatterpolargl":[{"marker":{"colorbar":{"outlinewidth":0,"ticks":""}},"type":"scatterpolargl"}],"scatterternary":[{"marker":{"colorbar":{"outlinewidth":0,"ticks":""}},"type":"scatterternary"}],"surface":[{"colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]],"type":"surface"}],"table":[{"cells":{"fill":{"color":"#EBF0F8"},"line":{"color":"white"}},"header":{"fill":{"color":"#C8D4E3"},"line":{"color":"white"}},"type":"table"}]},"layout":{"annotationdefaults":{"arrowcolor":"#2a3f5f","arrowhead":0,"arrowwidth":1},"autotypenumbers":"strict","coloraxis":{"colorbar":{"outlinewidth":0,"ticks":""}},"colorscale":{"diverging":[[0,"#8e0152"],[0.1,"#c51b7d"],[0.2,"#de77ae"],[0.3,"#f1b6da"],[0.4,"#fde0ef"],[0.5,"#f7f7f7"],[0.6,"#e6f5d0"],[0.7,"#b8e186"],[0.8,"#7fbc41"],[0.9,"#4d9221"],[1,"#276419"]],"sequential":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]],"sequentialminus":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]},"colorway":["#636efa","#EF553B","#00cc96","#ab63fa","#FFA15A","#19d3f3","#FF6692","#B6E880","#FF97FF","#FECB52"],"font":{"color":"#2a3f5f"},"geo":{"bgcolor":"white","lakecolor":"white","landcolor":"#E5ECF6","showlakes":true,"showland":true,"subunitcolor":"white"},"hoverlabel":{"align":"left"},"hovermode":"closest","mapbox":{"style":"light"},"paper_bgcolor":"white","plot_bgcolor":"#E5ECF6","polar":{"angularaxis":{"gridcolor":"white","linecolor":"white","ticks":""},"bgcolor":"#E5ECF6","radialaxis":{"gridcolor":"white","linecolor":"white","ticks":""}},"scene":{"xaxis":{"backgroundcolor":"#E5ECF6","gridcolor":"white","gridwidth":2,"linecolor":"white","showbackground":true,"ticks":"","zerolinecolor":"white"},"yaxis":{"backgroundcolor":"#E5ECF6","gridcolor":"white","gridwidth":2,"linecolor":"white","showbackground":true,"ticks":"","zerolinecolor":"white"},"zaxis":{"backgroundcolor":"#E5ECF6","gridcolor":"white","gridwidth":2,"linecolor":"white","showbackground":true,"ticks":"","zerolinecolor":"white"}},"shapedefaults":{"line":{"color":"#2a3f5f"}},"ternary":{"aaxis":{"gridcolor":"white","linecolor":"white","ticks":""},"baxis":{"gridcolor":"white","linecolor":"white","ticks":""},"bgcolor":"#E5ECF6","caxis":{"gridcolor":"white","linecolor":"white","ticks":""}},"title":{"x":0.05},"xaxis":{"automargin":true,"gridcolor":"white","linecolor":"white","ticks":"","title":{"standoff":15},"zerolinecolor":"white","zerolinewidth":2},"yaxis":{"automargin":true,"gridcolor":"white","linecolor":"white","ticks":"","title":{"standoff":15},"zerolinecolor":"white","zerolinewidth":2}}},"annotations":[{"align":"left","font":{"color":"white","size":15},"showarrow":false,"text":"<b>Coal & Lignite</b>","width":200,"x":2015,"xshift":105,"y":92429.6540227016,"yshift":-20},{"align":"left","font":{"color":"white","size":15},"showarrow":false,"text":"<b>Gas</b>","width":200,"x":2015,"xshift":105,"y":170325.05993802173,"yshift":-20},{"align":"left","font":{"color":"white","size":15},"showarrow":false,"text":"<b>Oil & Diesel</b>","width":200,"x":2015,"xshift":105,"y":296052.82,"yshift":-20},{"align":"right","font":{"color":"white","size":15},"showarrow":false,"text":"<b>Hydro</b>","width":200,"x":2050,"xshift":-105,"y":12922.876474508954,"yshift":0},{"align":"right","font":{"color":"white","size":15},"showarrow":false,"text":"<b>Wind</b>","width":200,"x":2050,"xshift":-105,"y":43445.750253916034,"yshift":0},{"align":"right","font":{"color":"white","size":15},"showarrow":false,"text":"<b>Solar PV</b>","width":200,"x":2050,"xshift":-105,"y":90892.16347041467,"yshift":0},{"align":"right","font":{"color":"white","size":15},"showarrow":false,"text":"<b>Geothermal</b>","width":200,"x":2050,"xshift":-105,"y":124913.57554238109,"yshift":0},{"align":"right","font":{"color":"white","size":15},"showarrow":false,"text":"<b>Solar CSP</b>","width":200,"x":2050,"xshift":-105,"y":138090.06624230836,"yshift":0},{"align":"right","font":{"color":"white","size":15},"showarrow":false,"text":"<b>Solar Heat</b>","width":200,"x":2050,"xshift":-105,"y":161696.19499999995,"yshift":0},{"align":"right","font":{"color":"white","size":15},"showarrow":false,"text":"<b>Biomass</b>","width":200,"x":2050,"xshift":-105,"y":183393.06999999995,"yshift":0},{"align":"right","font":{"color":"white","size":15},"showarrow":false,"text":"<b>Geothermal</b>","width":200,"x":2050,"xshift":-105,"y":201238.61499999996,"yshift":0},{"align":"right","font":{"color":"white","size":15},"showarrow":false,"text":"<b>Hydrogen</b>","width":200,"x":2050,"xshift":-105,"y":215058.14499999996,"yshift":0},{"align":"right","font":{"color":"white","size":15},"showarrow":false,"text":"<b>RE Fuel</b>","width":200,"x":2050,"xshift":-105,"y":243136.60999999996,"yshift":0},{"align":"center","font":{"color":"white","size":12},"showarrow":false,"text":"<b>Direct E: 18%</b>","width":200,"x":2020,"xshift":20,"y":304475.12969202857,"yshift":-20},{"align":"center","font":{"color":"white","size":12},"showarrow":false,"text":"<b>Electricity E: 18%</b>","width":200,"x":2020,"xshift":20,"y":32443.955993854048,"yshift":-20},{"align":"center","font":{"color":"white","size":12},"showarrow":false,"text":"<b>Direct E: 46%</b>","width":200,"x":2030,"xshift":20,"y":202173.19896913637,"yshift":-20},{"align":"center","font":{"color":"white","size":12},"showarrow":false,"text":"<b>Electricity E: 46%</b>","width":200,"x":2030,"xshift":20,"y":82044.7656771052,"yshift":-20},{"align":"center","font":{"color":"white","size":12},"showarrow":false,"text":"<b>Direct E: 81%</b>","width":200,"x":2040,"xshift":20,"y":154945.41419661892,"yshift":-20},{"align":"center","font":{"color":"white","size":12},"showarrow":false,"text":"<b>Electricity E: 81%</b>","width":200,"x":2040,"xshift":20,"y":125021.41367194014,"yshift":-20}],"yaxis":{"tickfont":{"size":14},"title":{"text":"<b>Final Energy Demand (PJ)<b>"},"showgrid":false,"ticktext":["50,000","100,000","150,000","200,000","250,000","300,000","350,000"],"tickvals":[50000,100000,150000,200000,250000,300000,350000]},"xaxis":{"showgrid":false},"plot_bgcolor":"white","showlegend":false,"shapes":[{"line":{"color":"white","dash":"dash","width":1},"type":"line","x0":2020,"x1":2020,"y0":0,"y1":355100.7796920286},{"line":{"color":"white","dash":"dash","width":1},"type":"line","x0":2030,"x1":2030,"y0":0,"y1":355100.7796920286},{"line":{"color":"white","dash":"dash","width":1},"type":"line","x0":2040,"x1":2040,"y0":0,"y1":355100.7796920286}],"title":{"text":"Global Expansion of Renewables to Achieve the 1.5C Goal"},"autosize":false,"width":800,"height":800},                        {"responsive": true}                    ).then(function(){

var gd = document.getElementById('5f964799-81f6-44e8-aa1b-50869581e4a6');
var x = new MutationObserver(function (mutations, observer) {{
        var display = window.getComputedStyle(gd).display;
        if (!display || display === 'none') {{
            console.log([gd, 'removed!']);
            Plotly.purge(gd);
            observer.disconnect();
        }}
}});

// Listen for the removal of the full notebook cells
var notebookContainer = gd.closest('#notebook-container');
if (notebookContainer) {{
    x.observe(notebookContainer, {childList: true});
}}

// Listen for the clearing of the current output cell
var outputEl = gd.closest('.output');
if (outputEl) {{
    x.observe(outputEl, {childList: true});
}}

                        })                };                });            </script>        </div>

