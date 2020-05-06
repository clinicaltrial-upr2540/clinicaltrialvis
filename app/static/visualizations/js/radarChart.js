
//Radar Chart Function inspired by Nadieh Bremer, VisualCinnamon.com


//create a radar chart	
function RadarChart(id, data, options) {

	//configurations
	var cfg = {
	 w: 600,				//Width of the circle
	 h: 600,				//Height of the circle
	 margin: {top: 20, right: 20, bottom: 20, left: 20}, //The margins around the circle
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
	  }//for i
	}//if

///////
	// data part


	// convert the nested data passed in
	// into an array of nested values arrays
	var dataCompany=d3.nest()
	.key(function(d) {return d.company;})
	.entries(data.data);

	//create a collection of values per company
	var data = dataCompany.map(function(d) { return d.values });

	//calculate total number of  drugs approved by the company
	//an array for total number of drugs approved by the company
	var array_Total = new Array();

	//write into the array_Total
	data.forEach( function( obj ) {

    	var sum=0;
     	Object.entries(obj).forEach(([key, value]) => {
     	sum += value.counts;
        });

     	array_Total.push(sum);

    });



   	//code that helps to identify categories
   	//we will still need this code in further stages of development
   	/*
    //set threshold and calculate quantiles to categorize the companies
    //sort an array
    array_sorted = array_Total.sort(d3.ascending);
    //define thresholds and create an array withinin the thresholds
    var lowest_threshold = 19;
    var highest_threshold = 100;
    array_cleaned = array_sorted.filter(function(item) {
    return (item > lowest_threshold && item < highest_threshold)
	});
	//print out
	for (var i=0; i<array_cleaned.length; i++)
    console.log(i + ". " + array_cleaned[i]);

    // define categories for companies 
    a_threshhold = d3.quantile(array_Total, 0);  
    b_threshhold = d3.quantile(array_cleaned, 0.25);  
    c_threshhold = d3.quantile(array_cleaned, 0.5); 
    d_threshhold = d3.quantile(array_cleaned, 0.75);  
   	e_threshhold = d3.quantile(array_cleaned, 1);
   	console.log(a_threshhold);
   	console.log(b_threshhold);
   	console.log(c_threshhold);
   	console.log(d_threshhold);
   	console.log(e_threshhold);
   	variance = d3.variance(array_Total);
   	console.log(variance);
   	deviation = d3.deviation(array_Total);
   	console.log(deviation);
   	mean = d3.mean(array_Total);
   	console.log(mean);
   	median = d3.median(array_Total);
   	console.log(median);

    var objTotal = JSON.stringify(Object.assign({}, array_Total)); 
	console.log(objTotal)

	*/
	//object for total number of  drugs approved by the company
	var objTotal = JSON.stringify(Object.assign({}, array_Total)); 


	//slice an array to create collections of companies data objects
    function toObject(arr, from, to) { 
        var group_obj = {}; 
        for (var i = 0; i < arr.length; ++i) 
        	if (arr[i] >= from && arr[i] <= to){
            	group_obj[i] = arr[i]; 
        	}
        return group_obj; 
    } 

    //creates collection of companies data objects by companies size
    //parameters are established in earlier code with the help of statistics
    var verySmallIndexes = toObject(array_Total, 1,9);
    var smallIndexes = toObject(array_Total, 10,19);
    var mediumSmallIndexes = toObject(array_Total, 20,36);
    var mediumLargeIndexes = toObject(array_Total, 37,99);
    var largeIndexes = toObject(array_Total, 100,896);
    var veryLargeIndexes = toObject(array_Total, 897,1850);


    //an array to store selected companies
	var selectedCompanies = new Array();

    //retrieves company name from the mapped entries (data)
    function getCompanyName(company_key){

		Object.entries(data).forEach(([key, value]) => {
 			if (company_key == key){
 				selectedCompanies.push(value[0].company);

 			}	
    	});


	} //end getCompanyName function

    	
	//imitates user selection that is under development
	//get keys of the company group selected by user
	//to be shown in the form in the later stages of development
	index_keys = Object.keys(largeIndexes);


	//imitates user selection that is under development
	//get keys of the companies selected by user
	let keysToRender = ['9', '48', '65', '83'];
	//get list of the companies selected by the user
	index_keys=Object.keys(largeIndexes).filter(key => { return ~keysToRender.indexOf(key) });


	//create an array of the company names
	for (const index_key of index_keys) {
			getCompanyName(index_key);
	}

    //form for companies created for demostration purposes and to be replaced with Flask variables
	$(document).ready(function(){

		const quotient = Math.ceil(selectedCompanies.length/3);

		$.each(selectedCompanies,function(index,value){
			//create a div
			var div_check_box = "<div></div>";
			//create three columns
			$(".checkBoxContainer").append($(div_check_box));
			$(".checkBoxContainer>div").addClass("col-4");
			$(".checkBoxContainer>div").addClass("form-check");

			//create a checkbox
			var checkbox="<input type='checkbox' id="+value+" value="+value+" name="+value+"><label for="+value+">"+value+"</label>";
			//append the div
			$(".form-check").eq(index).append($(checkbox));
			$("input").addClass("form-check-input");
			$("label").addClass("form-check-label");
		})
		

	});

	//filter data corresponding to the selected companies

	filtered = Object.keys(data)
			.filter(key => index_keys.includes(key))
			.reduce((obj, key) => {
		obj[key] = data[key];
		return obj;
		}, {});

	//create a collection of values from the above filter
	var myItems = Object.values(filtered);

	//extracts disease classes and a number of drugs in each of them
	//extracts disease class, drug and their top descriptors 
	function extractDiseasesByCounts(arr){	Object.entries(myItems).forEach(([key, value]) => {
			var extractedDiseases = value.map(el => el.disease_class);
			var extractedCounts = value.map(el => el.counts);
			var extractedDrug = value.map(el => el.drug_pref_name);
			var extractedMw = value.map(el => el.mw);
			var extractedClogp = value.map(el => el.clogp);
			var extractedPsa = value.map(el => el.psa);
			var extractedHba = value.map(el => el.hba)
			var extractedHbd = value.map(el => el.hbd);

			for(var i = 0; i < extractedDiseases.length; i++){
					arr.push({"disease" : extractedDiseases[i],"c": extractedCounts[i] });
			}

			for(var i = 0; i < extractedDiseases.length; i++){
					arrCs.push({"group" : extractedDiseases[i],"variable": extractedDrug[i], "mw": extractedMw[i], "clogp": extractedClogp[i], "psa": extractedPsa[i], "hba": extractedHba[i], "hbd": extractedHbd[i] });
			}
	
    	});

	} //end extractDiseasesByCounts function



	//array for the collection of disease classes and a number of drugs in each of them
	var arrDs = new Array();

	//array for the collection of disease class, drug and their top descriptors 
	var arrCs = new Array();


	//call the function extractDiseasesByCounts to create one collection of disease classes, number of drugs and 
	//another one - of disease class, drug, top descriptors
	extractDiseasesByCounts(arrDs);


	//for showing disease:number of approved drugs relationship
	var grouped = arrDs.reduce((map => (r, a) => {
    	map.set(a.disease, map.get(a.disease) || r[r.push({ disease: a.disease, counts: 0 }) - 1]);
    	map.get(a.disease).counts += a.c;
    	return r;
	})(new Map), []);

	//slice of the grouped data
	var grouped_selection = grouped.slice(0,8);
    	
	//imitates user selection that is under development
	//get the list of disease classes selected by the user
	let dKeys = ['C10 Nervous System Diseases', 'C14 Cardiovascular Diseases', 'C23 Pathological Conditions, Signs and Symptoms'];

	var selectedData = new Array();
	dKeys.forEach((dKey) => {
    	$.each(Object.values(filtered), function(key, value){
    		
    		value.forEach(myFunction); 
				function myFunction(item, index) 
				{ 
					if(dKey == item.disease_class){
    					selectedData.push({ key: key, value : value[index], index: index });
    				}

				}

    	});
    });

	//to save the data in txt format
	var dataToStr= 'group,variable,mw,clogp,psa,hba,hbd' + '\n';
    $.each(Object.values(selectedData), function(key, value){

    			dataToStr += Object.values(value)[1].company + ',' + Object.values(value)[1].drug_pref_name + ',' + Object.values(value)[1].mw + ',' + Object.values(value)[1].clogp + ',' + Object.values(value)[1].psa + ',' + Object.values(value)[1].hba + ',' + Object.values(value)[1].hbd +'\n';


    	});
    //need this line for further development
    //console.log(dataToStr);

    //data collections for testing
    //this section of code to be deleted after testing
	var recordKeys = [...new Set (selectedData.map(function(d) { return ""+d.key+"" }))];

	var recordIndexes = [...new Set (selectedData.map(function(d) { return ""+d.index+"" }))];

    
		filteredS = Object.keys(myItems)
			.filter(key => recordKeys.includes(key))
			.reduce((obj, key) => {
		obj[key] = myItems[key];
		return obj;
		}, {});

	var myItemsS = Object.values(filteredS);


	filteredI = Object.keys(Object.keys(Object.values(myItemsS)))
		.filter(key => recordIndexes.includes(key))
		.reduce((obj, key) => {
		obj[key] = Object.keys(Object.values(myItemsS))[key];
		return obj;
	}, {});


	var myItemsI = Object.values(filteredI);


	var filteredDisArray = new Array();


	var filteredDis = myItemsS
		.filter( (obj, val, i) => {

				Object.values(obj).forEach((val, i) => {

				if(recordIndexes.includes(""+i+"")) {

  					filteredDisArray.push(val);	

				}

				});
				return obj;
		}, {});

    function arrayToObject(arr) { 
        var group_obj = {}; 
        for (var i = 0; i < arr.length; ++i){ 
            	group_obj[i] = arr[i]; 
        }
        return group_obj; 
    } 

	const objectfromArray = arrayToObject(filteredDisArray);


	const groupedMap = filteredDisArray.reduce(
		(entryMap, e) => entryMap.set(e.company, [...entryMap.get(e.company)||[], e]),
		 new Map(), []);

	let groupedObjFromMap = [...groupedMap.entries()].reduce((obj, [key, value]) => (obj[key] = value, obj), {});

	//end data collection for testing


///////////
	//visualization part

	//filter data for the visualization
	var data=Object.keys(filtered).map(i=> filtered[i]);
	data = Object.values(groupedObjFromMap);

	//data for the dot matrix chart
	var filteredDisArray2 = new Array();

	var filteredDis2 = Object.values(filtered)
		.filter( (obj, val) => {

				Object.values(obj).forEach((val) => {

  					filteredDisArray2.push(val);	

				});
				return obj;
		}, {});

	const objectfromArray2 = arrayToObject(filteredDisArray2);


	const groupedMap2 = filteredDisArray2.reduce(
		(entryMap, e) => entryMap.set(e.company, [...entryMap.get(e.company)||[], e]),
		 new Map(), []);


	let groupedObjFromMap2 = [...groupedMap2.entries()].reduce((obj, [key, value]) => (obj[key] = value, obj), {});


	dotMatrixChart(Object.values(objectfromArray2),dotChartOptions);

	//radar chart part

	//if the configuration value of maxValue is smaller than the calculated value, based on the max number of drugs to be visualized,
	// replace by the max in the data
	var maxValue = Math.max(cfg.maxValue, d3.max(data, function(i){
		return d3.max(i.map(
			function(o){ return o.counts; }
		))
	}));

	//axis 
	var allAxis = (grouped_selection.map(function(i, j){return i.disease})),	//Names of each axis
		total = allAxis.length,					//The number of different axes
		radius = Math.min(cfg.w/2, cfg.h/2), 			//Radius of the outermost circle
		Format = d3.format('.0f'),			 	//Percentage formatting
		angleSlice = Math.PI * 2 / total;			//The width in radians of each "slice"
	
	//radius scale
	var rScale = d3.scaleLinear()
		.range([0, radius])
		.domain([0, maxValue]);
		

	//remove any visualization that was in gthe svg object before
	d3.select(id).select("svg").remove();
	
	//append svg element with width, height and class
	var svg = d3.select(id).append("svg")
			.attr("width",  cfg.w*1.5 + cfg.margin.left + cfg.margin.right)
			.attr("height", cfg.h + cfg.margin.top + cfg.margin.bottom)
			.attr("class", "radar"+id);
	
	//append a g element		
	var g = svg.append("g")
			.attr("transform", "translate(" + (cfg.w/2 + cfg.margin.left) + "," + (cfg.h/2 + cfg.margin.top) + ")");
		
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
	   .style("font-size", "10px")
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
		.style("font-size", "11px")
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
				.text(Format(d.counts))
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
	
	if (cfg.legend !== false && typeof cfg.legend === "object") {
	let legendZone = svg.append('g');
	let names = data.map(el => el[0].company);
	if (cfg.legend.title) {
		let title = legendZone.append("text")
			.attr("class", "title")
			.attr('transform', `translate(${cfg.legend.translateX},${cfg.legend.translateY})`)
			.attr("x", cfg.w - 70)
			.attr("y", 10)
			.attr("font-size", "12px")
			.attr("fill", "#404040")
			.text(cfg.legend.title);
	}
	let legend = legendZone.append("g")
		.attr("class", "legend")
		.attr("height", 100)
		.attr("width", 200)
		.attr('transform', `translate(${cfg.legend.translateX},${cfg.legend.translateY + 20})`);
	
	// create rectangles markers
	legend.selectAll('rect')
	  .data(names)
	  .enter()
	  .append("rect")
	  .attr("x", cfg.w - 65)
	  .attr("y", (d,i) => i * 20)
	  .attr("width", 10)
	  .attr("height", 10)
	  .style("fill", (d,i) => cfg.color(i));
	
	// create labels
	legend.selectAll('text')
	  .data(names)
	  .enter()
	  .append("text")
	  .attr("x", cfg.w - 52)
	  .attr("y", (d,i) => i * 20 + 9)
	  .attr("font-size", "11px")
	  .attr("fill", "#737373")
	  .text(d => d);
	}

	/////////////////////////////////////////////////////////
	/////////////////// Helper Function /////////////////////
	/////////////////////////////////////////////////////////

	//copied from http://bl.ocks.org/mbostock/7555321
	//wraps SVG text	
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
	}// end wrap function	

	
}//end RadarChart function