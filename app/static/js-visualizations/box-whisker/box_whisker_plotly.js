"use strict";



// set the dimensions and margins of the graph
var margin = {top: 10, right: 30, bottom: 30, left: 40},
    width = 460 - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;

// append the svg object to the body of the page
var svg = d3.select("#box-whisker")
  .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");

// Read the data and compute summary statistics for each specie
d3.csv("heatmap_data_CO6.csv", function(data) {

  // Compute quartiles, median, inter quantile range min and max --> these info are then used to draw the box.
  var sumstat = d3.nest() // nest function allows to group the calculation per level of a factor
    .key(function(d) { return d.group;})
    .rollup(function(d) {
      //let q0 = d3.quantile(d.map(function(g) { return g.value;}).sort(d3.ascending),0);
      let sorted = d.map(function(g) { return +g.value;});
      let drugNames = d.map(function(g) { return g.variable;});
      /*let sorted = notSorted.sort(d3.ascending);
      let q1 = d3.quantile(sorted,0.25);*/
      //let median = d3.quantile(d.map(function(g) { return g.value;}).sort(d3.ascending),0.5);
      let median = d3.median(d.map(function(g) { return +g.value;}).sort(d3.ascending));
      let q1 = d3.quantile(d.map(function(g) { return +g.value;}).sort(d3.ascending),0.25);
      let q3 = d3.quantile(d.map(function(g) { return +g.value;}).sort(d3.ascending),0.75);
      let interQuantileRange = q3 - q1;
      let deviation = d3.deviation(d.map(function(g) { return g.value;}).sort(d3.ascending));
      let min = q1 - 1.5 * interQuantileRange;
      let max = q3 + 1.5 * interQuantileRange;
      //let min = d3.min(d.map(function(g) { return +g.value;}).sort(d3.ascending));
      //let max = d3.max(d.map(function(g) { return +g.value;}).sort(d3.ascending));
      return({sorted: sorted, drugNames: drugNames, deviation : deviation, q1: q1, median: median, q3: q3, interQuantileRange: interQuantileRange, min: min, max: max})
    })
    .entries(data);

    console.log(sumstat);

//domain
    var myGroups = d3.map(data, function(d){return d.group;}).keys();
    var myDrugs = d3.map(data, function(d){return d.variable;}).keys();
    console.log(myDrugs);

    var myGroupsTruncated = d3.map(data, function(d){
      var myStr = d.group;
      if(myStr != null){
          myStr = myStr.substring(0, myStr.indexOf(" "))+"...";
      } 
      return myStr;
      }).keys();

    //Plotly

    var allYs = sumstat.map(function(g) { return g.value['sorted'];});


    var allDrugNames = sumstat.map(function(g) { return g.value['drugNames'];});


  //coloring
  function linspace(a,b,n) {
    return Plotly.d3.range(n).map(function(i){return a+i*(b-a)/(n-1);});
  }
  var boxNumber = myGroupsTruncated.length;
  var boxColor = [];
  var allColors = linspace(0, 360, boxNumber);
  for( var i = 0; i < boxNumber;  i++ ){
    var result = 'hsl('+ allColors[i] +',50%'+',50%)';
    boxColor.push(result);
  }

  var colors = ['rgba(93, 164, 214, 0.5)', 'rgba(255, 144, 14, 0.5)', 'rgba(44, 160, 101, 0.5)', 'rgba(255, 65, 54, 0.5)', 'rgba(207, 114, 255, 0.5)', 'rgba(127, 96, 0, 0.5)', 'rgba(255, 140, 184, 0.5)', 'rgba(79, 90, 117, 0.5)', 'rgba(222, 223, 0, 0.5)'];

  var dataForStyled = [];

  for ( var i = 0; i < myGroupsTruncated.length; i ++ ) {
      var result = {
          type: 'box',
          y: allYs[i],
          name: myGroupsTruncated[i],
          boxpoints: 'all',
          jitter: 0.5,
          whiskerwidth: 0.2,
          boxmean: 'sd',
          fillcolor: colors,
          text: allDrugNames[i],
          marker: {
              size: 2,
              color: boxColor[i],
              outliercolor: 'rgba(219, 64, 82, 0.6)',
              line: {
              outliercolor: 'rgba(219, 64, 82, 1.0)',
              outlierwidth: 2
              }
          },
          colorscale: 'Jet',
          line: {
              width: 1
          },
          hovertemplate: '<br><b>Drug</b>: %{text}<br>' +
                        '<i>Psa</i>: %{y}'
      };
      dataForStyled.push(result);
  };

  var layout = {
      title: 'Box-whisker plot accross pharma',
      yaxis: {
          autorange: true,
          showgrid: true,
          zeroline: true,
          dtick: 10,
          gridcolor: 'rgb(255, 255, 255)',
          gridwidth: 1,
          zerolinecolor: 'rgb(255, 255, 255)',
          zerolinewidth: 2
      },
      margin: {
          l: 40,
          r: 30,
          b: 80,
          t: 100
      },
      paper_bgcolor: 'rgb(243, 243, 243)',
      plot_bgcolor: 'rgb(243, 243, 243)',
      hovermode:'closest',
      showlegend: true
  };



    Plotly.newPlot('box-whisker-plotly', dataForStyled, layout);

 


})