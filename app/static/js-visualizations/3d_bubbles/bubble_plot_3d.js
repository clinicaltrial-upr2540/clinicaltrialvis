// Plotly.d3.csv('splom_data_C14.csv', function(err, rows){
Plotly.d3.csv('/vis/splomdata/csv', function(err, rows){

var companies = d3.map(rows, function(d){return d.group;}).keys();

console.log(companies[0]);

var colors = d3.scaleLinear()
  .domain([0, 9])  
  .range(["blue", "green"]);;
  var xVar = 'mw'


var sumstat = d3.nest() // nest function allows to group the calculation per level of a factor
    .key(function(d) { return d.group;})
    .rollup(function(d) {
      //let q0 = d3.quantile(d.map(function(g) { return g.value;}).sort(d3.ascending),0);
      let x = d.map(function(g) { return +g[xVar];});
      let y = d.map(function(g) { return +g.psa;});
      let z = d.map(function(g) { return g.clogp;});
      let drug = d.map(function(g) { return g.variable;});
      let size = d.map(function(g) { return g.hba;});
     return({x: x, y : y, z: z, drug:drug, size: size})
    })
    .entries(rows);

    // console.log(sumstat[1].value);


var dataFor3D = [];



  for (i=0; i < companies.length; i++) {

   // console.log(companies[1]===sumstat[1].key);

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
        type: 'scatter3d'
      };
      dataFor3D.push(traces);

  }

  console.log(dataFor3D);
  
  


/*
var trace1 = {
  x:unpack(rows, 'psa'), y: unpack(rows, 'mw'), z: unpack(rows, 'variable'),
  mode: 'markers',
  marker: {
    color:'#4E79A7',
    size: 12,
    line: {
      color: '#4E79A7',
      width: 0.5},
      opacity: 0.8},
  type: 'scatter3d'
};

var trace2 = {
  x:unpack(rows, 'psa'), y: unpack(rows, 'mw'), z: unpack(rows, 'variable'),
  mode: 'markers',
  marker: {
    color: '#F28E2B',
    size: 12,
    symbol: 'circle',
    line: {
    color: '#F28E2B',
      width: 1},
      opacity: 0.8},
  type: 'scatter3d'};

var dataFor3D = [trace1, trace2];
console.log(dataFor3D);
*/


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
  }};
Plotly.newPlot('bubble-plot-3d', dataFor3D, layout, {scrollZoom: true}, {responsive: true});
});