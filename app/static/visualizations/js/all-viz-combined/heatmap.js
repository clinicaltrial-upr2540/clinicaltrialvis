"use strict";
function heatmapChart(id, diseaseClasses, companies, descriptor) {


  //remove any previously created chart from DOM that had the same id
  const item = document.querySelector(id)
  while (item.firstChild) {
    item.removeChild(item.firstChild)
  }


  // set the dimensions and margins of the graph
  var margin = {top: 80, right: 30, bottom: 30, left: 300},
    width = 900 - margin.left - margin.right,
    height = 600 - margin.top - margin.bottom;

  // append the svg object to the body of the page
  var svg = d3.select(id)
  .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");

//Load the data and draw heatmap

d3.csv("/static/visualizations/datafiles/all_cdc_descriptors.csv", function(error, data){

  //create a collection of values that correspond to the companies passed to the function
  var dataByCompany=d3.nest()
  .key(function(d) {return d.company;})
  .entries(Object.values(data));

   //create arrays for further data manipulations
   //an array that represents data in visualizations
    var arr1 = new Array();
   //intermediate array used in data manipulations
    var arr2 = new Array();
   //to store data by disease class
    var arr3 = new Array();

  //extracts the set of data  
  function extractDiseaseSets(dataSource)
    { Object.entries(dataSource).forEach(([key, value]) => {
      for(var i = 0; i < companies.length; i++){
        if (value.key==companies[i]){
          arr2 = value.values;
        }// end if
        if(Array.isArray(arr2) && arr2.length){
          arr3=[...arr3, ...arr2];
          arr2=new Array();
          i++;
        }
      }//end for
      }) //end forEach
    }; //end extractDiseases function 

  //extract the set of data ordered by passed disease classes
  extractDiseaseSets(dataByCompany);

  //create a collection of values that correspond to the disease classes passed to the function
   var recordValues = new Array();
    diseaseClasses.forEach((diseaseClass) => {
      var diseasesDescriptors = new Array();
      $.each(arr3, function(key, value){
        if(diseaseClass==value.disease_class){
          var descriptorName= descriptor;
          diseasesDescriptors.push({disease_class: value.disease_class, compound: value.compound, descriptor: value[descriptor]});  
        } //end if
      }); //end forEach
      recordValues.push(diseasesDescriptors);
    });
        
 

  //selects the rows from csv file that correspond to a passed key
  function selectRows(rows, column) {
        return rows.map(function(row) { return row[column]; });
    }

  // create a duplicate of the array with the values to be used in the visualization
  //add columnNames to this array
  var recordValuesWithColNames = [...recordValues];
  var columnNames=["disease_class", "compound", "descriptor"];
  recordValuesWithColNames.push(columnNames);

 
  //removes duplicates from an array and returns an object of values with no duplicates
  function removeDuplicates(arr) {
    let uniqueObj = {};
    arr.forEach(function(i) {
      if(!uniqueObj[i]) {
        uniqueObj[i] = true;
      }
    });
    return Object.keys(uniqueObj);
  }

  // creates a collection a values determined by a given dimension from recordValuesWithColNames
  function createCollection (dimension){
    var arr = new Array();
    for (var index = 0; index < diseaseClasses.length; index++) { 
      arr=[...arr, ...selectRows(recordValuesWithColNames[index], dimension)]; 
    }//end for loop
    return arr;
  } //end createCollection()


  //create a collection of all compounds and all descriptors to be used in the heatmap
  var allCompounds = [...createCollection ('compound')];
  var descriptorValues= [...createCollection ("descriptor")];
  allCompounds.sort().reverse();
  descriptorValues.sort();

  descriptorValues=descriptorValues.map(function(el){ if (el!=""){return +el} else return el;});

  //remove duplicates for Y axis
  var compoundsNoDupl = removeDuplicates(allCompounds);


  //creates an array of the values that are truncated, given orginal list, an array to push value into and a string to add when truncating 
  function truncateNames(arr, originalList, strAdded){
      originalList.forEach(function(item, i){

      var myStr = item;
      if(myStr != null){
          myStr = myStr.substring(0, myStr.indexOf(" "))+strAdded;
      } 
      arr.push(myStr);
      }  );

    }

  //create two arrays, one with the trancated disease classes to be used in the X axis of the plot
  //and the other one to be used in the header
  var diseaseClassesTruncated = new Array();
  var diseaseClassesForHeader = new Array();

  truncateNames(diseaseClassesTruncated, diseaseClasses, "...");
  truncateNames(diseaseClassesForHeader, diseaseClasses, "");


  //create a data collection to be used by the heatmap function
  for (var index = 0; index < recordValues.length; index++) { 
    arr1 =[...arr1, ...recordValues[index]];
  } //end for loop

  data =[...arr1];



  // Build X scale and axis:
  var x = d3.scaleBand()
    .range([ 0, width ])
    .domain(diseaseClassesTruncated)
    .padding(0.1);
  svg.append("g")
    .style("font-size", "1em")
    .attr("class","xScale")
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(x).tickSize(0))
    .select(".domain").remove()

  // Build Y scale and axis:
  var y = d3.scaleBand()
    .range([ height, 0 ])
    .domain(compoundsNoDupl)
    .padding(0.05)
    .align(1);
  svg.append("g")
    .style("font-size", "1em")
    .attr("class","yScale")
    .call(d3.axisLeft(y).tickSize(0))
    .select(".domain").remove();

  svg.selectAll(".xScale > g > text")
  .style("text-anchor", "right")
  .attr("x",3) 
  .attr("y", 9);

  svg.selectAll(".yScale > g > text")
  .style("text-anchor", "right")
  .attr("x",0) 
  .attr("y", 0);

// Build a color scale based on d3 sequential scale with a domain from 1 to a maximum value of the descriptor
  var myColor = d3.scaleSequential()
    .interpolator(d3.interpolatePiYG)
    .domain([1,d3.max(descriptorValues)])

  // create a tooltip
var tooltipDescriptor = "<br>"+ descriptor.toUpperCase() + ": "
  var tooltip = d3.select(id)
    .append("div")
    .attr('style', 'position:absolute; opacity:0')
    .attr("class", "tooltip")
    .style("background-color", "white")
    .style("border", "solid")
    .style("border-width", "2px")
    .style("border-radius", "5px")
    .style("padding", "5px")

  // Three function that change the tooltip when user hover / move / leave a cell
  var mouseover = function(d) {
    tooltip
      .style("opacity", 1)
    d3.select(this)
      .style("stroke", "black")
      .style("opacity", 1)
  }
  var mousemove = function(d) {
    tooltip
      .html(d.compound + tooltipDescriptor + d["descriptor"])
      .style('top', (d3.event.layerY - 30) + 'px')
      .style('left', (d3.event.layerX + 20) + 'px')
  }
  var mouseleave = function(d) {
    tooltip
      .style("opacity", 0)
    d3.select(this)
      .style("stroke", function(d) { if (d["descriptor"]==""){return "darkgrey"} else {return "none"}})
      .style("opacity", 0.8)
  }


  // add the squares
  //for the values that are an empty string shows a white square with a darkgrey border 
  svg.selectAll()
    .data(data, function(d) {return d.disease_class+':'+d.compound;})
    .enter()
    .append("rect")
      .attr("x", function(d) { var myStr = d.disease_class;
      if(myStr != null){
          myStr = myStr.substring(0, myStr.indexOf(" "))+"...";
      } 
      return x(myStr);
       })
      .attr("y", function(d) { return y(d.compound) })
      .attr("rx", 4)
      .attr("ry", 4)
      .attr("width", x.bandwidth() )
      .attr("height", y.bandwidth() )
      .style("fill", function(d) { if (d["descriptor"]==""){return "none"} else {return myColor(d["descriptor"])} } )
      .style("stroke", function(d) { if (d["descriptor"]==""){return "darkgrey"} else {return "none"}})
      .style("stroke-width", 4)
      .style("opacity", 0.8)
    .on("mouseover", mouseover)
    .on("mousemove", mousemove)
    .on("mouseleave", mouseleave)


  // Add title to graph
  svg.append("text")
          .attr("x", 0)
          .attr("y", -50)
          .attr("text-anchor", "left")
          .style("font-size", "22px")
          .text("Heatmap for " + diseaseClassesForHeader.join(",") + " disease classes");

  // Add subtitle to graph
  svg.append("text")
          .attr("x", 0)
          .attr("y", -20)
          .attr("text-anchor", "left")
          .style("font-size", "14px")
          .style("fill", "grey")
          .style("max-width", 400)
          .text(descriptor.toUpperCase());

     }); //end d3.csv

} //end heatmapChart function