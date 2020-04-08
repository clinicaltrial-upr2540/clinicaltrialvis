Plotly.d3.csv('/vis/splomdata/csv', function(err, rows){


    function unpack(rows, key) {
        return rows.map(function(row) { return row[key]; });
    }

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

      var pl_colorscale=[               
               [0.0, '#19d3f3'],
               [0.333, '#19d3f3'],
               [0.333, '#e763fa'],
               [0.666, '#e763fa'],
               [0.666, '#636efa'],
               [1, '#636efa']
    ]


scl = [[0, 'rgb(150,0,90)'],[0.125, 'rgb(0, 0, 200)'],[0.25,'rgb(0, 25, 255)'],[0.375,'rgb(0, 152, 255)'],[0.5,'rgb(44, 255, 150)'],[0.625,'rgb(151, 255, 0)'],[0.75,'rgb(255, 234, 0)'],[0.875,'rgb(255, 111, 0)'],[1,'rgb(255, 0, 0)']];



    var axis = () => ({
      showline:false,
      zeroline:false,
      gridcolor:'#ffff',
      ticklen:4
    })

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
        size: 7,
        line: {
          color: 'white',
          width: 0.5
        }
      }
    }]

    var layout = {
      title:'Molecular descriptors',
      height: 800,
      width: 800,
      autosize: true,
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

    Plotly.react('splom-plot', data, layout);
    

});