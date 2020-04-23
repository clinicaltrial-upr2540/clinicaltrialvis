//load the data, using plotly library function

//line for local deployment
//Plotly.d3.csv('/vis/splomdata/csv/splom_data_C14.csv', function(err, rows){
//line for Flask deployment
Plotly.d3.csv('/vis/splomdata/csv', function(err, rows){

// create data collection of companies to be used as a color in 3d-bubble-plot 
  var companies = d3.map(rows, function(d){return d.group;}).keys();

//create color scale
  var colors = d3.scaleLinear()
    .domain([0, 9])  
    .range(["blue", "green"]);;
  
//variable for molecular weight
  var xVar = 'mw'

//create data collections that are necessary to represent each of the dimensions in the 3d-bubble-plot
  var sumstat = d3.nest()
      .key(function(d) { return d.group;})
      .rollup(function(d) {
        let x = d.map(function(g) { return +g[xVar];});
        let y = d.map(function(g) { return +g.psa;});
        let z = d.map(function(g) { return g.clogp;});
        let drug = d.map(function(g) { return g.variable;});
        let size = d.map(function(g) { return g.hba;});
       return({x: x, y : y, z: z, drug:drug, size: size})
      })
      .entries(rows);

  
//the description of all parameters for plotly 3d plot is here https://plotly.com/javascript/3d-scatter-plots/
  
//create data in plotly format
  var dataFor3D = [];

//loop through the companies array
  for (i=0; i < companies.length; i++) {
      var traces = {
        x: sumstat[i].value.x, y: sumstat[i].value.y, z:sumstat[i].value.z,
        mode: 'markers',
        name: companies[i],
        text:sumstat[i].value.drug,
        marker: {
          color:colors[i],
          symbol:'circle',
          size: sumstat[i].value.size,
          line: {
            color: '#66c2a5',
            width: 0.5},
            opacity: 0.8},
        hovertemplate: '<br><b>Drug</b>: %{text}' +
                        '<br><i>MW </i>: %{x}' +
                        '<br><i>PSA </i>: %{y}' +
                        '<br><i>CLOGP </i>: %{z}',
        type: 'scatter3d'
      };
      dataFor3D.push(traces);
  } //end for loop
    

//layout
  var layout = {
    scene: {
      xaxis:{title: 'MW'},
      yaxis:{title: 'PSA'},
      zaxis:{title: 'cLogP'},
      },
    margin: {
    l: 0,
    r: 0,
    b: 0,
    t: 0
    },
    hoverlabel: {
        bgcolor: 'lightgrey',
        bordercolor: 'darkgrey',
        font: {
          color: 'black',
          family: 'Open Sans',
          size: 16
        } 
    }
  };

  //calls plotly function to create 3d-bubble plot
  Plotly.newPlot('bubble-plot-3d', dataFor3D, layout, {scrollZoom: true}, {responsive: true});

  }); //end end plotly.d3.csv function