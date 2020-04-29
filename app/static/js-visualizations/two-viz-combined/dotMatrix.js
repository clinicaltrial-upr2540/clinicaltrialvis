
//from https://github.com/arpitnarechania/d3-dotmatrix/blob/master/dist/DotMatrix.js
//rewritten from d3v3 to d3v4 by me

function dotMatrixChart(id,dataset,options){

    var dotRadius = options.dot_radius;
    var noOfCirclesInARow = options.no_of_circles_in_a_row;
    var dotPaddingLeft = options.dot_padding_left;
    var dotPaddingRight = options.dot_padding_right;
    var dotPaddingTop = options.dot_padding_top;
    var dotPaddingBottom = options.dot_padding_bottom;

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

    console.log("dataset in dot matrix", dataset);

    //Remove whatever chart with the same id/class was present before
    d3.select(id).select("svg").remove();


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

    var sumOfEveryCompany = {};
    for(var i=0;i<dataset.length;i++){
        if(sumOfEveryCompany[dataset[i]['company']] == null){
            sumOfEveryCompany[dataset[i]['company']] = 0;
        }
        sumOfEveryCompany[dataset[i]['company']] += dataset[i]['counts'];
    }

    var maxNoOfLinesInCompany = 0;
    for(var company in sumOfEveryCompany){
        if(sumOfEveryCompany[company]/noOfCirclesInARow > maxNoOfLinesInCompany){
            maxNoOfLinesInCompany = Math.ceil(sumOfEveryCompany[company]/noOfCirclesInARow);
        }
    }

    var numberOfLines = maxNoOfLinesInCompany * uniqueCompanies.length;

    var companyScale = d3.scalePoint().domain(uniqueCompanies).range([0, uniqueCompanies.length-1]);
    var diseaseClassScale = d3.scalePoint().domain(uniqueCategories).range([0, uniqueCategories.length]);

    //var color = d3.scaleOrdinal(d3.schemeDark2);
    
    var color = d3.scaleOrdinal(d3.schemeDark2);

    // Set the dimensions of the canvas / graph
    var	margin = {top: dotRadius*10, right: dotRadius*15, bottom: dotRadius*10, left: dotRadius*15};

    height = numberOfLines * (dotRadius*2 + dotPaddingBottom + dotPaddingTop);
    width = (dotRadius*2 + dotPaddingLeft + dotPaddingRight) * noOfCirclesInARow;

    // Set the ranges
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

    //Create SVG element
    var svg = d3.select(id)
                .append("svg")
                .attr("width", width + margin.left + margin.right + width/2)
                .attr("height", height + margin.top + margin.bottom);
                //previous settings
                //.attr("transform", "translate(" + margin.left + "," + margin.top + ")")

    //Create Y axis
    svg.append("g")
        .attr("transform", "translate(" + (margin.left - (dotRadius*2)) + ",0)")
        .attr("class", "y axis")
        .call(yAxis)
        .selectAll("text")
        .attr("y", dotRadius*2.5)
        .attr("x", width-margin.right)
        .attr("dy", ".35em")
        .style("font-size", dotRadius*3 + "px")
        .attr("transform", "rotate(0)")
        .style("text-anchor", "end");

    //Create Y axis
        svg
        .append("line")
        .attr("x1",width)
        .attr("y1",margin.top)
        .attr("x2",width)
        .attr("y2",height)
        .style("stroke","black")
        .style("stroke-width",1)

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
  

    var companies = svg
       .selectAll("g.company")
       .data(dataset)
        .enter()
        .append('g')
        .attr("class", "company");

    var circleArray = companies.selectAll("g.circleArray")
    .data(function(d) {return generate_array(d);});

    circleArray.enter()
    .append('g')
    .attr("class", "circleArray")
    .append("circle")
    .style("fill",function(d){return color(d.disease_class);})
    .attr("r", dotRadius)
    .attr("cx", function(d,i) {return xScale(d.x); })
    .attr("cy", function(d,i) { return yScale(d.y); });

    // add legend
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


    var tooltip = d3.select("body")
    .append('div')
    .attr('class', 'tooltip');

    tooltip.append('div')
    .attr('class', 'company');
    tooltip.append('div')
    .attr('class', 'disease_class');
    tooltip.append('div')
    .attr('class', 'number_of_drugs');

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
}