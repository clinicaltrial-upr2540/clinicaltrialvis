
//Radar Chart Function inspired by Nadieh Bremer, VisualCinnamon.com

	
function radarChart(id, data, options) {

	//remove any previously created chart from DOM that had the same id
	const item = document.querySelector(id)
		while (item.firstChild) {
  		item.removeChild(item.firstChild)
	}


	//configurations
	var cfg = {
	 w: 300,				//Width of the circle
	 h: 300,				//Height of the circle
	 margin: {top: 5, right: 5, bottom: 5, left: 5}, //The margins around the circle
	 levels: 5,				//How many levels or inner circles should there be drawn
	 maxValue: 0, 				//What is the value that the biggest circle will represent
	 labelFactor: 1.25, 			//How much farther than the radius of the outer circle should the labels be placed
	 wrapWidth: 60, 			//The number of pixels after which a label needs to be given a new line
	 opacityArea: 0.35, 			//The opacity of the area of the blob
	 dotRadius: 3, 				//The size of the colored circles of each blog
	 opacityCircles: 0.1, 			//The opacity of the circles of each blob
	 strokeWidth: 2, 			//The width of the stroke around each blob
	 roundStrokes: false,			//If true the area and stroke will follow a round path (cardinal-closed)
	 color: d3.scaleOrdinal(d3.schemeCategory10),	//Color function
	 format: '.2%',
	 unit:'drugs',						//units
	 legend:false 					//legend		
	};
	
	//put all of the configuration options into a variable called cfg
	if('undefined' !== typeof options){
	  for(var i in options){
		if('undefined' !== typeof options[i]){ cfg[i] = options[i]; }
	  }
	}//end if

///////
	// data part

	//select distinct disease classes from the data for the names of Axis
	var diseaseArray= new Array();
	function extractDiseases(arr)
		{ Object.entries(data).forEach(([key, value]) => {
			//for debugging
			//console.log(key);
			//console.log(value);
			var extractedDiseases = value.map(el => el.disease_class);
				for(var i = 0; i < extractedDiseases.length; i++){
					arr.push(extractedDiseases[i]);
				}//end for
			}) //end forEach
		};
	extractDiseases(diseaseArray);


	let distinctDiseaseClasses = [...new Set(diseaseArray)];
	distinctDiseaseClasses = distinctDiseaseClasses.sort();


	//if the configuration value of maxValue is smaller than the calculated value, based on the max number of drugs to be visualized,
	// replace by the max in the data
	var maxValue = Math.max(cfg.maxValue, d3.max(data, function(i){
		var maxPerCompany = d3.max(i.map(
			function(o){ return o.counts; }
		));
		return maxPerCompany;
	}));

///////////
	//visualization part

	//axis 
	var allAxis = (distinctDiseaseClasses.map(function(el){return el})),	//Names of each axis
		total = allAxis.length,					//The number of different axes
		radius = Math.min(cfg.w/2, cfg.h/2), 			//Radius of the outermost circle
		Format = d3.format('.0f'),			 	//Percentage formatting
		angleSlice = Math.PI * 2 / total;			//The width in radians of each "slice"
	
	//radius scale
	var rScale = d3.scaleLinear()
		.range([0, radius])
		.domain([0, maxValue]);
		

	//append svg element with width, height and class
	var svg = d3.select(id).append("svg")
			.attr("width",  cfg.w + cfg.margin.left + cfg.margin.right)
			.attr("height", cfg.h + cfg.margin.top + cfg.margin.bottom)
			.attr("class", "radar"+id);
	
	//append a g elementt		
	var g = svg.append("g")
			.attr("transform", "translate(" + (cfg.w/2 + cfg.margin.left) + "," + (cfg.h/2 + cfg.margin.top/1.8) + ")");
	
	//filter for the outside glow
	var filter = g.append('defs').append('filter').attr('id','glow'),
		feGaussianBlur = filter.append('feGaussianBlur').attr('stdDeviation','2.5').attr('result','coloredBlur'),
		feMerge = filter.append('feMerge'),
		feMergeNode_1 = feMerge.append('feMergeNode').attr('in','coloredBlur'),
		feMergeNode_2 = feMerge.append('feMergeNode').attr('in','SourceGraphic');

	//draw the grid	
	//wrapper for the grid & axes
	var axisGrid = g.append("g").attr("class", "axisWrapper");
	
	//draw the background circles
	axisGrid.selectAll(".levels")
	   .data(d3.range(1,(cfg.levels+1)).reverse())
	   .enter()
		.append("circle")
		.attr("class", "gridCircle")
		.attr("r", function(d, i){return radius/cfg.levels*d;})
		.style("fill", "#CDCDCD")
		.style("stroke", "#CDCDCD")
		.style("fill-opacity", cfg.opacityCircles)
		.style("filter" , "url(#glow)");

	//text indicating at what % each level is
	axisGrid.selectAll(".axisLabel")
	   .data(d3.range(1,(cfg.levels+1)).reverse())
	   .enter().append("text")
	   .attr("class", "axisLabel")
	   .attr("x", 4)
	   .attr("y", function(d){return -d*radius/cfg.levels;})
	   .attr("dy", "0.4em")
	   .style("font-size", "12px")
	   .attr("fill", "#737373")
	   .text(function(d,i) { return Format(maxValue * d/cfg.levels); });

	//draw the axis	
	//create straight radius lines
	var axis = axisGrid.selectAll(".axis")
		.data(allAxis)
		.enter()
		.append("g")
		.attr("class", "axis");
	
	//append the lines
	axis.append("line")
		.attr("x1", 0)
		.attr("y1", 0)
		.attr("x2", function(d, i){ return rScale(maxValue*1.1) * Math.cos(angleSlice*i); })
		.attr("y2", function(d, i){ return rScale(maxValue*1.1) * Math.sin(angleSlice*i); })
		.attr("class", "line")
		.style("stroke", "white")
		.style("stroke-width", "2px");

	//append the labels to each of the axis
	axis.append("text")
		.attr("class", "legend")
		.style("font-size", "12px")
		.attr("text-anchor", "middle")
		.attr("dy", "0.35em")
		.attr("x", function(d, i){ return rScale(maxValue * cfg.labelFactor) * Math.cos(angleSlice*i - Math.PI/2); })
		.attr("y", function(d, i){ return rScale(maxValue * cfg.labelFactor) * Math.sin(angleSlice*i - Math.PI/2); })
		.text(function(d){return d})
		.call(wrap, cfg.wrapWidth);

	//draw the actual radar chart
	
	//create the the radial line
	var radarLine = d3.radialLine()
		.curve(d3.curveLinearClosed)
		.radius(function(d) { return rScale(d.counts); })
		.angle(function(d,i) {	return i*angleSlice; });
		
	if(cfg.roundStrokes) {
		radarLine.curve(d3.curveCardinalClosed);
	}
				
	//create a wrapper for the chart data	
	var blobWrapper = g.selectAll(".radarWrapper")
		.data(data)
		.enter().append("g")
		.attr("class", "radarWrapper");
			
	//append the backgrounds of the areas for each of the companies		
	blobWrapper
		.append("path")
		.attr("class", "radarArea")
		.attr("d", function(d,i) { return radarLine(d); })
		.style("fill", function(d,i) { return cfg.color(i); })
		.style("fill-opacity", cfg.opacityArea)
		.on('mouseover', function (d,i){
			//change opacity of non-selected area
			d3.selectAll(".radarArea")
				.transition().duration(200)
				.style("fill-opacity", 0.1); 
			//show the selected area
			d3.select(this)
				.transition().duration(200)
				.style("fill-opacity", 0.7);	
		})
		.on('mouseout', function(){
			//show all of the areas
			d3.selectAll(".radarArea")
				.transition().duration(200)
				.style("fill-opacity", cfg.opacityArea);
		});
		
	//create the outlines	
	blobWrapper.append("path")
		.attr("class", "radarStroke")
		.attr("d", function(d,i) { return radarLine(d); })
		.style("stroke-width", cfg.strokeWidth + "px")
		.style("stroke", function(d,i) { return cfg.color(i); })
		.style("fill", "none")
		.style("filter" , "url(#glow)");		
	
	//append the circles or edges of the area objects
	blobWrapper.selectAll(".radarCircle")
		.data(function(d,i) { return d; })
		.enter().append("circle")
		.attr("class", "radarCircle")
		.attr("r", cfg.dotRadius)
		.attr("cx", function(d,i){ return rScale(d.counts) * Math.cos(angleSlice*i - Math.PI/2); })
		.attr("cy", function(d,i){ return rScale(d.counts) * Math.sin(angleSlice*i - Math.PI/2); })
		.style("fill", function(d,i,j) { return cfg.color(j); })
		.style("fill-opacity", 0.8);

	//wrapper for the invisible circles to be used for tooltip
	var blobCircleWrapper = g.selectAll(".radarCircleWrapper")
		.data(data)
		.enter().append("g")
		.attr("class", "radarCircleWrapper");
		
	//append a set of invisible circles on top for the mouseover pop-up
	blobCircleWrapper.selectAll(".radarInvisibleCircle")
		.data(function(d,i) { return d; })
		.enter().append("circle")
		.attr("class", "radarInvisibleCircle")
		.attr("r", cfg.dotRadius*1.5)
		.attr("cx", function(d,i){ return rScale(d.counts) * Math.cos(angleSlice*i - Math.PI/2); })
		.attr("cy", function(d,i){ return rScale(d.counts) * Math.sin(angleSlice*i - Math.PI/2); })
		.style("fill", "none")
		.style("pointer-events", "all")
		.on("mouseover", function(d,i) {
			newX =  parseFloat(d3.select(this).attr('cx')) - 10;
			newY =  parseFloat(d3.select(this).attr('cy')) - 10;
					
			tooltip
				.attr('x', newX)
				.attr('y', newY)
				.text(d.company + ": " + Format(d.counts))
				.transition().duration(200)
				.style('opacity', 1);
		})
		.on("mouseout", function(){
			tooltip.transition().duration(200)
				.style("opacity", 0);
		});
		
	//set up a tooltip for hover over functionality
	var tooltip = g.append("text")
		.attr("class", "tooltip")
		.style("opacity", 0);
	
	// create rectangles markers

	//Taken from http://bl.ocks.org/mbostock/7555321
	//Wraps SVG text	
	function wrap(text, width) {
	  text.each(function() {
		var text = d3.select(this),
			words = text.text().split(/\s+/).reverse(),
			word,
			line = [],
			lineNumber = 0,
			lineHeight = 1.4, // ems
			y = text.attr("y"),
			x = text.attr("x"),
			dy = parseFloat(text.attr("dy")),
			tspan = text.text(null).append("tspan").attr("x", x).attr("y", y).attr("dy", dy + "em");
			
		while (word = words.pop()) {
		  line.push(word);
		  tspan.text(line.join(" "));
		  if (tspan.node().getComputedTextLength() > width) {
			line.pop();
			tspan.text(line.join(" "));
			line = [word];
			tspan = text.append("tspan").attr("x", x).attr("y", y).attr("dy", ++lineNumber * lineHeight + dy + "em").text(word);
		  }
		}
	  });
	}//wrap	

	
}//end radarChart