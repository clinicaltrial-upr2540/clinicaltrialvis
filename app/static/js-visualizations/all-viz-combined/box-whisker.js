"use strict";
function boxWhiskerChart(id, diseaseClasses, companies, descriptor) {

  //remove any previously created chart from DOM that had the same id

  const item = document.querySelector(id)
  while (item.firstChild) {
    item.removeChild(item.firstChild)
  }

  // read the data
  //line for Flask deployment

  //line for local deployment
  d3.csv("/static/js-visualizations/all-viz-combined/cdc_descriptors.csv", function(data) {

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
          diseasesDescriptors.push({company: value.company, compound: value.compound, descriptor: value[descriptor]});  
        } //end if
      }); //end forEach
      recordValues.push(diseasesDescriptors);
    });
          

    // create data collections and compute statistics that are necessary to draw the box
    var sumstat = d3.nest()
      .key(function(d) { return d.company;})
      .rollup(function(d) {
        let sorted = d.map(function(g) { return +g[descriptor];});
        let compoundNames = d.map(function(g) { return g.compound;});
        let diseaseClass = d.map(function(g) { return g.disease_class;});
        let median = d3.median(d.map(function(g) { return +g[descriptor];}).sort(d3.ascending));
        let q1 = d3.quantile(d.map(function(g) { return +g[descriptor];}).sort(d3.ascending),0.25);
        let q3 = d3.quantile(d.map(function(g) { return +g[descriptor];}).sort(d3.ascending),0.75);
        let interQuantileRange = q3 - q1;
        let deviation = d3.deviation(d.map(function(g) { return g[descriptor];}).sort(d3.ascending));
        let min = q1 - 1.5 * interQuantileRange;
        let max = q3 + 1.5 * interQuantileRange;
        return({sorted: sorted, compoundNames: compoundNames, diseaseClass: diseaseClass, deviation : deviation, q1: q1, median: median, q3: q3, interQuantileRange: interQuantileRange, min: min, max: max})
      })
      .entries(arr3);

   // create additional data collections for drug groups and drugs as well as for axis

    /*var myGroups = d3.map(data, function(d){return d.company;}).keys();
    var myDrugs = d3.map(data, function(d){return d.compound;}).keys();*/

    //creates an array of the values that are truncated, given orginal list, an array to push value into and a string to add when truncating 
    function truncateNames(arr, originalList, strAdded){
      originalList.forEach(function(item, i){

      var myStr = item;
      if(myStr != null){
          myStr = myStr.substring(0, myStr.indexOf(" "))+strAdded;
      } 
      arr.push(myStr);
      }  );
    } //end truncateNames function

    //create two arrays, one with the trancated disease classes to be used in the header
    //and the other one with companies to be used in the X axis
    var companiesTruncated = new Array();
    var diseaseClassesTruncated = new Array();

    truncateNames(companiesTruncated, companies, "...");
    truncateNames(diseaseClassesTruncated, diseaseClasses, "");


    //data collections for Y axis and for the plot
    var allYs = sumstat.map(function(g) { return g.value['sorted'];});
    var allCompoundsNames = sumstat.map(function(g) { return g.value['compoundNames'];});
    var allDiseaseClasses = sumstat.map(function(g) { return g.value['diseaseClass'];});
    var tooltipText = [];

    //create a tooltip text
    allCompoundsNames.forEach((array1, index) => {
      const array2 = allDiseaseClasses[index];
      var thirdArray = array1.map((e, i) => 'Compound: ' + e + ', Disease Class: '+ array2[i].substring(0, array2[i].indexOf(" ")));
      tooltipText.push(thirdArray);

    });

    //Plotly
    //all code below prepares the data that plotly requires for visualizing multiple box-whisker plots
    //the description of all parameters is here https://plotly.com/javascript/box-plots/

    //rainbow coloring inspired by plotly https://plotly.com/javascript/box-plots/
    function linspace(a,b,n) {
      return Plotly.d3.range(n).map(function(i){return a+i*(b-a)/(n-1);});
    }
    var boxNumber = companiesTruncated.length+1;
    var boxColor = [];
    var allColors = linspace(0, 360, boxNumber);

    for( var i = 0; i < boxNumber;  i++ ){
      var result = 'hsl('+ allColors[i] +',50%'+',50%)';
      boxColor.push(result);
    }

    var colors = ['rgba(93, 164, 214, 0.5)', 'rgba(255, 144, 14, 0.5)', 'rgba(44, 160, 101, 0.5)', 'rgba(255, 65, 54, 0.5)', 'rgba(207, 114, 255, 0.5)', 'rgba(127, 96, 0, 0.5)', 'rgba(255, 140, 184, 0.5)', 'rgba(79, 90, 117, 0.5)', 'rgba(222, 223, 0, 0.5)', 'rgba(93, 164, 214, 0.5)'];

    //create data in plotly format
    var dataForStyled = [];
    for ( var i = 0; i < companiesTruncated.length; i ++ ) {
        var result = {
            type: 'box',
            y: allYs[i],
            name: companiesTruncated[i],
            boxpoints: 'all',
            jitter: 0.5,
            whiskerwidth: 0.2,
            boxmean: 'sd',
            fillcolor: colors,
            text: tooltipText[i],
            marker: {
                size: 2,
                color: boxColor[i],
                outliercolor: 'rgba(219, 64, 82, 0.6)',
                line: {
                outliercolor: 'rgba(219, 64, 82, 1.0)',
                outlierwidth: 2
                }
            },
            line: {
                width: 1
            },
            hovertemplate: '<br> %{text}<br>' +
                          '<b>'+descriptor.toUpperCase()+'</b>: %{y}'
        };
        dataForStyled.push(result);
    };

    // if there is a need to do by selected disease classes
    //title: 'Box-whisker for '+diseaseClassesTruncated.join(',') + ' disease classes',
    //layout
    var layout = {
        autosize:false,
        width:900,
        height:600,
        title: 'Box-whisker for all disease classes targeted by the selected companies',
        annotations: [{
          text: descriptor.toUpperCase(),
            font: {
            size: 14,
            color: 'rgb(128, 128, 128)',
          },
          showarrow: false,
          align: 'center',
          x: 0.5,
          y: 1.1,
          xref: 'paper',
          yref: 'paper',
        }],
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
        showlegend: true,
        hoverlabel: {
          bgcolor: 'lightgrey',
          bordercolor: 'darkgrey',
          font: {
            color: 'black',
            family: 'Open Sans',
            size: 16
          } 
        }
    };

    //calls plotly function to create box-whisker plot
    id=id.substring(1);
    Plotly.newPlot(id, dataForStyled, layout);

  }) //end d3.csv function

} //end heatmapChart function