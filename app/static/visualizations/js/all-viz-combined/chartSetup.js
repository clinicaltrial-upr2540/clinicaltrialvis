//Radar Chart Function inspired by Nadieh Bremer, VisualCinnamon.com
 
// set the dimensions and margins of the visualization

var margin = {top: 100, right: 100, bottom: 100, left: 100},
	width = Math.min(900, window.innerWidth - 10) - margin.left - margin.right,
	height = Math.min(600, window.innerHeight - margin.top - margin.bottom - 20);
					
//set colors scale 
//5 colors from colorbrewer as an alternative to current d3 ordinal scale of 10 colors
/*var color = d3.scaleOrdinal()
	.range(['#06D6A0','#118AB2','#E76F51', '#FFD166', '#073B4C']);
*/
//options for radar chart - weight, height, margin, radius as maxValue, number of circles as levels
//rounded corners as roundStrokes, colorscale as color, number format as format, legend, units 
var radarChartOptions = {
	w: width,
	h: height,
	svg_height: 600,
	margin: margin,
	maxValue: 6,
	levels: 6,
	roundStrokes: true,
	color: d3.scaleOrdinal(d3.schemeCategory10),
	format: '.0f',
	legend: { title: '', translateX: 150, translateY: 100 },
	unit: 'drugs'
};

var dotChartOptions = {
	svg_height: 600,
	h:height,
    dot_radius : 4,
    no_of_circles_in_a_row: 25,
    dot_padding_left : 5,
    dot_padding_right : 5,
    dot_padding_top : 5,
    dot_padding_bottom : 5
}

// Load the data and call function to draw the dotmatrix
d3.json("/static/visualizations/datafiles/all_cdc_data.json", function(error, data){
	prepareData(data);
});
			