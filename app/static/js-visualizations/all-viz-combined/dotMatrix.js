"use strict";
//inspired by d3v3 from https://github.com/arpitnarechania/d3-dotmatrix/blob/master/dist/DotMatrix.js
//rewritten from d3v3 to d3v4 and adjusted to the company-> disease_class -> drugs dataset by Jelena Dowey

function dotMatrixChart(id,dataset,options){

     //remove any previously created chart from DOM that had the same id
    const item = document.querySelector(id)
        while (item.firstChild) {
        item.removeChild(item.firstChild)
    }

    //settings for dotMatrix chart
    var dotRadius = options.dot_radius;
    var noOfCirclesInARow = options.no_of_circles_in_a_row;
    var dotPaddingLeft = options.dot_padding_left;
    var dotPaddingRight = options.dot_padding_right;
    var dotPaddingTop = options.dot_padding_top;
    var dotPaddingBottom = options.dot_padding_bottom;

    //error handling for the lack of settings
    if(isNaN(dotRadius)){
        throw new Error("dot_radius must be a Number");
    }
    if(isNaN(noOfCirclesInARow)){
        throw new Error("no_of_circles_in_a_row must be a Number");
    }
    if(isNaN(dotPaddingLeft)){
        throw new Error("dot_padding_left must be a Number");
    }
    if(isNaN(dotPaddingRight)){
        throw new Error("dot_padding_right must be a Number");
    }
    if(isNaN(dotPaddingTop)){
        throw new Error("dot_padding_top must be a Number");
    }
    if(isNaN(dotPaddingBottom)){
        throw new Error("dot_padding_bottom must be a Number");
    }


    // create data collections for the drug class (categories) and companies 
    var flags = [], uniqueCategories = [], uniqueCompanies=[], l = dataset.length, i;
    for( i=0; i<l; i++) {
        if( flags[dataset[i].disease_class]) continue;
        flags[dataset[i].disease_class] = true;
        uniqueCategories.push(dataset[i].disease_class);
    }
    uniqueCategories.sort();
    flags = [];
    for( i=0; i<l; i++) {
        if( flags[dataset[i].company]) continue;
        flags[dataset[i].company] = true;
        uniqueCompanies.push(dataset[i].company);
    }

    //create a data collection for a number of drugs approved by each company
    var sumOfEveryCompany = {};
    for(var i=0;i<dataset.length;i++){
        if(sumOfEveryCompany[dataset[i]['company']] == null){
            sumOfEveryCompany[dataset[i]['company']] = 0;
        }
        sumOfEveryCompany[dataset[i]['company']] += dataset[i]['counts'];
    }

    //create a variable that defines a max number of lines per company in visualization
    var maxNoOfLinesInCompany = 0;
    for(var company in sumOfEveryCompany){
        if(sumOfEveryCompany[company]/noOfCirclesInARow > maxNoOfLinesInCompany){
            maxNoOfLinesInCompany = Math.ceil(sumOfEveryCompany[company]/noOfCirclesInARow)+1;
        }
    }

    //create a variable that defines a total number of lines in visualization
    var numberOfLines = maxNoOfLinesInCompany * uniqueCompanies.length;

    //create a company and disease class scale
    var companyScale = d3.scalePoint().domain(uniqueCompanies).range([0, uniqueCompanies.length-1]);
    var diseaseClassScale = d3.scalePoint().domain(uniqueCategories).range([0, uniqueCategories.length]);

    //create a color scale
    //d3 scales can be viewed here https://github.com/d3/d3-scale-chromatic
    //schemeDark2 has 8 colors
    var color = d3.scaleOrdinal(d3.schemeDark2);

    // set dimensions and margins of the visualization
    var	margin = {top: dotRadius*10, right: dotRadius*15, bottom: dotRadius*10, left: dotRadius*30},
    height = numberOfLines * (dotRadius*2 + dotPaddingBottom + dotPaddingTop),
    width = (dotRadius*2 + dotPaddingLeft + dotPaddingRight) * noOfCirclesInARow;

    // set x-axis and y-axis - scale, range, axis, ticks, domain
    var	xScale = d3.scaleLinear().range([margin.left, width]);
    var	yScale = d3.scaleLinear().range([height, margin.bottom]);

    var xAxis = d3.axisBottom(xScale);

    var yAxis = d3.axisLeft(yScale)
                .tickFormat(function (d) {
                    var myStr = uniqueCompanies[d];
                    if(myStr != null){
                        myStr = myStr.substring(0, myStr.indexOf(" "))+"...";
                    } 
                    return myStr;
                })
                .ticks(uniqueCompanies.length)
                .tickSize(-width+margin.left-(dotRadius*2), 0, 0)


    xScale.domain([0,noOfCirclesInARow]);
    yScale.domain([0,d3.max(dataset,function(d){return companyScale(d.company)+1;})]);
    yScale.domain([0,d3.max(dataset,function(d){return companyScale(d.company)+1;})]);

    //create and append the svg element to the dotMatrixChart element of the page
    var svg = d3.select(id)
                .append("svg")
                .attr("width", width + margin.left + margin.right + width/2)
                .attr("height", height + margin.top + margin.bottom);
                //.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    //populate y axis
    svg.append("g")
        .attr("transform", "translate(" + (margin.left - (dotRadius*2)) + ",0)")
        .attr("class", "y axis")
        .call(yAxis)
        .selectAll("text")
        .attr("y", -dotRadius*1.9*maxNoOfLinesInCompany)
        .attr("dy", ".35em")
        .style("font-size", dotRadius*3 + "px")
        .attr("transform", "rotate(0)")
        .style("fill", "hsl(268, 62%, 39%)")
        .style("font-weight", "bold")
        .style("text-anchor", "end");
        
        /*
        alternative settings
        -dotRadius*1.9*maxNoOfLinesInCompany
        initial setings

        attr("y", dotRadius*2.5)
        .attr("x", width-margin.right)
        .attr("dy", ".35em")
        .style("font-size", dotRadius*3 + "px")
        .attr("transform", "rotate(0)")
        .style("text-anchor", "end");

        */

    //populate x axis
        svg
        .append("line")
        .attr("x1",width)
        .attr("y1",margin.top)
        .attr("x2",width)
        .attr("y2",height)
        .style("stroke","black")
        .style("stroke-width",1)

    //create an array of dots and their positions in the lines
    var globalLineNoForCompany = {};
    var globalLineSizeForCompany = {};
    var globalDotXPosition = {};
    function generate_array(d){

        if(globalLineSizeForCompany[d.company] == null){
            globalLineSizeForCompany[d.company] = 0;
        }
        if(globalLineNoForCompany[d.company] == null){
            globalLineNoForCompany[d.company] = 0.5/(maxNoOfLinesInCompany);
        }
        if(globalDotXPosition[d.company] == null){
            globalDotXPosition[d.company] = 0;
        }

        var arr = new Array(d.counts);
        for(var i=0;i<d.counts;i++){

            if(globalLineSizeForCompany[d.company]!=0 && globalLineSizeForCompany[d.company] % noOfCirclesInARow == 0){
                globalLineNoForCompany[d.company] += 1/(maxNoOfLinesInCompany);
                globalDotXPosition[d.company]=1;
            }else{
                globalDotXPosition[d.company]+=1;
            }

            arr[i] = {y:companyScale(d.company)+globalLineNoForCompany[d.company],x: globalDotXPosition[d.company]-1, company:d.company,disease_class:d.disease_class, counts:d.counts};
            globalLineSizeForCompany[d.company] += 1;
        }
        return arr;
    }
  
    //create company element and append it to the DOM
    var companies = svg
       .selectAll("g.company")
       .data(dataset)
        .enter()
        .append('g')
        .attr("class", "company");

    //create circle elements (array fo circles) and append them to the DOM
    var circleArray = companies.selectAll("g.circleArray")
    .data(function(d) {return generate_array(d);});

    //color circle elements
    circleArray.enter()
    .append('g')
    .attr("class", "circleArray")
    .append("circle")
    .style("fill",function(d){return color(d.disease_class);})
    .attr("r", dotRadius)
    .attr("cx", function(d,i) {return xScale(d.x); })
    .attr("cy", function(d,i) { return yScale(d.y); });

    // add  and style legend, color by colorscheme according to the disease class
    var legend = svg
    .selectAll(".legend")
    .data(uniqueCategories)
    .enter()
    .append("g")
    .attr("class", "legend")
    .attr("transform", "translate(" + 0  + "," + (margin.top+dotRadius) + ")");

    legend
      .append("circle")
      .attr("cx", width + dotRadius*4)
      .attr("cy", function(d,i){return i*dotRadius*4;})
      .attr("r", dotRadius)
      .style("fill", function(d) {
        return color(d);
      })

    legend
      .append("text")
      .attr("x", width + dotRadius*4 + dotRadius*3)
      .attr("text-anchor",'start')
      .attr("y", function(d,i){return i*dotRadius*4 + dotRadius;})
      .style("font-size", dotRadius*3 + "px")
      .text(function(d){return d});

    //create tooltip
    var tooltip = d3.select("body")
    .append('div')
    .attr('class', 'tooltip');

    //populate tooltip with a name of the company, disease class and a number of drugs within the disease class
    tooltip.append('div')
    .attr('class', 'company');
    tooltip.append('div')
    .attr('class', 'disease_class');
    tooltip.append('div')
    .attr('class', 'number_of_drugs');

    //add mouse over, mouse move and mouse out behavior that shows a tooltip on hovering over the circles
    svg.selectAll(".circleArray > circle")
    .on('mouseover', function(d,i) {

        tooltip.select('.company').html("<b>Company: " + d.company+ "</b>");
        tooltip.select('.disease_class').html("<b>Disease class: " + d.disease_class+ "</b>");
        tooltip.select('.number_of_drugs').html("<b>Number of drugs: " + d.counts + "</b>");

        tooltip.style('display', 'block');
        tooltip.style('opacity',2);

    })
    .on('mousemove', function(d) {
        tooltip.style('top', (d3.event.layerY - 30) + 'px')
        .style('left', (d3.event.layerX + 20) + 'px');
    })
    .on('mouseout', function() {
        tooltip.style('display', 'none');
        tooltip.style('opacity',0);
    });
} //end dotMatrixChart function