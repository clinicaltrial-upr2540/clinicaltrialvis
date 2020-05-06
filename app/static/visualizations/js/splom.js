//load the data, using plotly library function

//line for local deployment
//Plotly.d3.csv('/vis/splomdata/csv/splom_data_C14.csv', function(err, rows){
//line for Flask deployment
Plotly.d3.csv('/static/visualizations/datafiles/splom_data_C14.csv', function(err, rows){

//reads the data
    function unpack(rows, key) {
        return rows.map(function(row) { return row[key]; });
    }

//creates color array for each data point
//by looping through the data and defines colors (0, 0.5, 1) for data points for every company
    colors=[];
    for (i=0; i < unpack(rows, 'group').length; i++) {
      if (unpack(rows, 'group')[i] == "MYLAN PHARMACEUTICALS INC") {
        colors.push(0);
      } else if (unpack(rows, 'group')[i] == "SANDOZ INC") {
        colors.push(0.5);
      } else if (unpack(rows, 'group')[i] == "WATSON LABORATORIES INC") {
        colors.push(1);
      }
    }
//color scale that maps colors defined per each data point (0, 0.5, 1) to actual colors
      var pl_colorscale=[               
               [0.0, '#19d3f3'],
               [0.333, '#19d3f3'],
               [0.333, '#e763fa'],
               [0.666, '#e763fa'],
               [0.666, '#636efa'],
               [1, '#636efa']
    ]

//description of the options for axis, data an layout 
//documentation on plotly parameters is here: https://plotly.com/javascript/splom/

//axis
    var axis = () => ({
      showline:false,
      zeroline:false,
      gridcolor:'#ffff',
      ticklen:3
    })

//data
    var data = [{
      type: 'splom',
      dimensions: [
        {label:'MW', values:unpack(rows,'mw')},
        {label:'cLogP', values:unpack(rows,'clogp')},
        {label:'PSA', values:unpack(rows,'psa')},
        {label:'HBA', values:unpack(rows,'hba')},
        {label:'HBD', values:unpack(rows,'hbd')}
      ],
      text: unpack(rows,'group'),
      name: unpack(rows, 'group'),
      marker: {
        color: colors,
        colorscale:pl_colorscale,
        size: 7,
        line: {
          color: 'white',
          width: 0.5
        }
      }
    }]

//layout
    var layout = {
      title:'Molecular descriptors',
      height: 800,
      width: 800,
      autosize: false,
      hovermode:'closest',
      dragmode:'select',
      plot_bgcolor:'rgba(240,240,240, 0.95)',
      xaxis:axis(),
      yaxis:axis(),
      xaxis2:axis(),
      xaxis3:axis(),
      xaxis4:axis(),
      xaxis5:axis(),
      yaxis2:axis(),
      yaxis3:axis(),
      yaxis4:axis(),
      yaxis5:axis()
    }

//calls plotly function to create scatterplot matrix or splom
    Plotly.react('splom-plot', data, layout);


}); //end plotly.d3.csv function