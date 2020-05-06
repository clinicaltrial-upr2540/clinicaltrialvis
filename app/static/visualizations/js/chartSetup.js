
//Radar Chart Function inspired by Nadieh Bremer, VisualCinnamon.com
 
// set the dimensions and margins of the visualization
var margin = {top: 100, right: 100, bottom: 100, left: 100},
	width = Math.min(700, window.innerWidth - 10) - margin.left - margin.right,
	height = Math.min(width, window.innerHeight - margin.top - margin.bottom - 20);


//set colors scale 
//5 colors from colorbrewer
/*var color = d3.scaleOrdinal()
	.range(['#06D6A0','#118AB2','#E76F51', '#FFD166', '#073B4C']);
*/
//options for radar chart - weight, height, margin, radius as maxValue, number of circles as levels
//rounded corners as roundStrokes, colorscale as color, number format as format, legend, units 
var radarChartOptions = {
  w: width,
  h: height,
  margin: margin,
  maxValue: 10,
  levels: 6,
  roundStrokes: true,
  color: d3.scaleOrdinal(d3.schemeCategory10),
  format: '.0f',
  legend: { title: 'Drug targets by companies', translateX: 100, translateY: 40 },
  unit: 'drugs'
};

//options for dotmatrix
var dotChartOptions = {
    dot_radius : 5,
    no_of_circles_in_a_row: 40,
    dot_padding_left : 5,
    dot_padding_right : 5,
    dot_padding_top : 5,
    dot_padding_bottom : 5
}

//Load the data and Call function to draw the Radar chart
//cdc_data.json
//cd_psa_data.json
//Company_disease_psa_hbd.json
d3.json("/static/visualizations/datafiles/cdc_data.json", function(error, data){
	console.log(data);
	RadarChart("#radarChart", data, radarChartOptions);
	//console.log("Data after loading", data);
});
