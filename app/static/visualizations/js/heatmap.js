"use strict";

// set the dimensions and margins of the graph
var margin = {top: 80, right: 30, bottom: 30, left: 300},
  width = 1000 - margin.left - margin.right,
  height = 1000 - margin.top - margin.bottom;

// append the svg object to the heatmap element of the page
var svg = d3.select("#heatmap")
.append("svg")
  .attr("width", width + margin.left + margin.right)
  .attr("height", height + margin.top + margin.bottom)
.append("g")
  .attr("transform",
        "translate(" + margin.left + "," + margin.top + ")");

// add title to graph
svg.append("text")
        .attr("x", 0)
        .attr("y", -50)
        .attr("text-anchor", "left")
        .style("font-size", "22px")
        .text("A heatmap for one disease category");

// add subtitle to graph
svg.append("text")
        .attr("x", 0)
        .attr("y", -20)
        .attr("text-anchor", "left")
        .style("font-size", "14px")
        .style("fill", "grey")
        .style("max-width", 400)
        .text("Company (row), drug(column), psa(color)");

//read the data
//line for local deployment
//d3.csv('/vis/heatmap/csv/heatmap_data_CO6.csv', function(err, data){
//line for Flask deployment
d3.csv("/vis/heatmapdata/csv", function(data) {

  //labels for rows ('group' or company) and columns('variable' or drug)
  var myGroups = d3.map(data, function(d){return d.group;}).keys();

  var myVars = d3.map(data, function(d){return d.variable;}).keys();

  var myGroupsTruncated = d3.map(data, function(d){
      var myStr = d.group;
      if(myStr != null){
          myStr = myStr.substring(0, myStr.indexOf(" "))+"...";
      } 
      return myStr;
      }).keys();

  myVars = myVars.sort().reverse();


  // build x scale and axis:
  var x = d3.scaleBand()
    .range([ 0, width ])
    .domain(myGroupsTruncated)
    .padding(0.1);
  svg.append("g")
    .style("font-size", "1em")
    .attr("class","xScale")
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(x).tickSize(0))
    .select(".domain").remove()

  // build y scale and axis:
  var y = d3.scaleBand()
    .range([ height, 0 ])
    .domain(myVars)
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

  // build color scale
  var myColor = d3.scaleSequential()
    .interpolator(d3.interpolatePiYG)
    .domain([1,100])

  // create a tooltip
  var tooltip = d3.select("#heatmap")
    .append("div")
    .style("opacity", 0)
    .attr("class", "tooltip")
    .style("background-color", "white")
    .style("border", "solid")
    .style("border-width", "2px")
    .style("border-radius", "5px")
    .style("padding", "5px")

  // tooltip on hover over or mouse enter/over
  var mouseover = function(d) {
    tooltip
      .style("opacity", 1)
    d3.select(this)
      .style("stroke", "black")
      .style("opacity", 1)
  }
  //toopltip on mouse move
  var mousemove = function(d) {
    tooltip
      .html(d.variable + "<br>PSA: " + d.value)
      .style("left", (d3.mouse(this)[0]+300) + "px")
      .style("top", (d3.mouse(this)[1]) + "px")
  }
  //tooltip on mouse leave
  var mouseleave = function(d) {
    tooltip
      .style("opacity", 0)
    d3.select(this)
      .style("stroke", "none")
      .style("opacity", 0.8)
  }

  // add the squares
  svg.selectAll()
    .data(data, function(d) {return d.group+':'+d.variable;})
    .enter()
    .append("rect")
      .attr("x", function(d) { var myStr = d.group;
      if(myStr != null){
          myStr = myStr.substring(0, myStr.indexOf(" "))+"...";
      } 
      return x(myStr);
       })
      .attr("y", function(d) { return y(d.variable) })
      .attr("rx", 4)
      .attr("ry", 4)
      .attr("width", x.bandwidth() )
      .attr("height", y.bandwidth() )
      .style("fill", function(d) { return myColor(d.value)} )
      .style("stroke-width", 4)
      .style("stroke", "none")
      .style("opacity", 0.8)
    .on("mouseover", mouseover)
    .on("mousemove", mousemove)
    .on("mouseleave", mouseleave)

}) //end d3.csv

