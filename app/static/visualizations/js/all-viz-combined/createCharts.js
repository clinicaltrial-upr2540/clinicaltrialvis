"use strict";
function createCharts(data, dataCollection){
//form for companies
    	$(document).ready(function(){



// convert nested data passed into visualizations into an array of nested values
	var dataCompany=d3.nest()
	.key(function(d) {return d.company;})
	.entries(data.data);
	
	//for debugging
	//console.log(dataCompany, typeof(dataCompany));


	//reorganize data to be an object of arrays by companies
	data = dataCompany.map(function(d) { return d.values });
	//console.log("Data values mapped", data, typeof(data));

	//calculate total number of drugs approved by the company and write it in an array
	var array_Total = new Array();
	data.forEach( function( obj ) {
    	var sum=0;
     	Object.entries(obj).forEach(([key, value]) => {
     	sum += value.counts;
        });
     	array_Total.push(sum);
    });

   	//code that helps to identify categories
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
	console.log("object TOTAL ", objTotal);

	*/
	//create an object where the key corresponds to a company position in the data variable and the value is the number of drugs it produces
    var objTotal = JSON.stringify(Object.assign({}, array_Total)); 
	
	//for debugging
	//console.log("object TOTAL ", objTotal);

	//slice an array to create an object by elements positions from - to
	//to create objects for the companies categories
    function toObject(arr, from, to) { 
        var group_obj = {}; 
        for (var i = 0; i < arr.length; ++i) 
        	if (arr[i] >= from && arr[i] <= to){
            	group_obj[i] = arr[i]; 
        	}
        return group_obj; 
    } //end function to Object

    ///////////////////////////////////////////////
    //////////////////*COMPANIES*//////////////////
    ///////////////////////////////////////////////

    //create objects for the companies categories
    const verySmallIndexes = toObject(array_Total, 1,9);
    const smallIndexes = toObject(array_Total, 10,19);
    const mediumSmallIndexes = toObject(array_Total, 20,36);
    const mediumLargeIndexes = toObject(array_Total, 37,99);
    const largeIndexes = toObject(array_Total, 100,896);
    const veryLargeIndexes = toObject(array_Total, 897,1850);

   var companiesCategories = new Array();
    companiesCategories.push({"size": Object.keys(verySmallIndexes).length, "name": "VERY SMALL", "companiesIndexes": verySmallIndexes});
    companiesCategories.push({"size": Object.keys(smallIndexes).length, "name": "SMALL", "companiesIndexes": smallIndexes});
    companiesCategories.push({"size": Object.keys(mediumSmallIndexes).length, "name": "MEDIUM SMALL", "companiesIndexes": mediumSmallIndexes});
    companiesCategories.push({"size": Object.keys(mediumLargeIndexes).length, "name": "MEDIUM LARGE", "companiesIndexes": mediumLargeIndexes});
    companiesCategories.push({"size": Object.keys(largeIndexes).length, "name": "LARGE", "companiesIndexes": largeIndexes});
    companiesCategories.push({"size": Object.keys(veryLargeIndexes).length, "name": "VERY LARGE", "companiesIndexes": veryLargeIndexes});

    //for debugging
    console.log("companiesCategories", companiesCategories.length);
    console.log("VERY SMALL COMPANIES", verySmallIndexes);
    console.log("SMALL COMPANIES", smallIndexes);
    console.log("MEDIUM SMALL COMPANIES", mediumSmallIndexes);
    console.log("MEDIUM LARGE COMPANIES", mediumLargeIndexes);
    console.log("LARGE COMPANIES", largeIndexes);
    console.log("VERY LARGE COMPANIES", veryLargeIndexes);



    		
			

		}); //end document ready
} //end createCharts