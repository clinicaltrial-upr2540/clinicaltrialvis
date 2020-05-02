"use strict";

//main function that reads the json data, creates all f the buttons and events handlers for the buttons, calling other js files

function prepareData(data){

	//declaration of variables

	//arrays for 
	//companiesCategories - categories of companies
	//cSelectedCompanies - companies from one selected category
	//uSelectedCompanies - user selected companies
	//allDiseaseArray - distinct disease classes for the names of Axis
	//arrDs - disease classes by counts
	//arrCs - disease classes by descriptors
	//companiesKeysToRender - user selected companies keys



	var companiesCategories = new Array(), cSelectedCompanies = new Array(),
	allDiseasesArray= new Array(), companiesKeysToRender = new Array(), 
	deseasesToRender = new Array(), selectedData = new Array(), companiesList = new Array();

	//objects

	//uSelectedKeys - an object to store companies names per user selected keys
	var uSelectedKeys = new Object();
	var cKeys = new Object;


	var filtered = new Object();
	var filteredValues = new Object();

	var objectfromArray2 = new Object();




	// convert nested data passed into visualizations into an array of nested values
	var dataCompany=d3.nest()
	.key(function(d) {return d.company;})
	.entries(data.data);


	//reorganize data to be an object of arrays by companies
	data = dataCompany.map(function(d) { return d.values });
	//untouched copy of data to be used in further manipulations
	var dataByCompanies = dataCompany.map(function(d) { return d.values });

	//calculate total number of drugs approved by the company and write it in an array
	var array_Total = new Array();
	dataByCompanies.forEach( function( obj ) {
    	var sum=0;
     	Object.entries(obj).forEach(([key, value]) => {
     	sum += value.counts;
        });
     	array_Total.push(sum);
    });
    

   	//code that helps to identify categories
   	var arrayTotalToSort = [...array_Total];
   	
    //set threshold and calculate quantiles to categorize the companies
    //sort an array
    var array_sorted = arrayTotalToSort.sort(d3.ascending);
  
    //define thresholds and create an array withinin the thresholds
    var lowest_threshold = 9;
    var highest_threshold = 16;
    var array_cleaned = array_sorted.filter(function(item) {
    return (item > lowest_threshold && item < highest_threshold)
	});
	//print out
	for (var i=0; i<array_cleaned.length; i++)

    // define categories for companies 
    var a_threshhold = d3.quantile(array_sorted, 0); 
    var b_threshhold = d3.quantile(array_sorted, 0.2);  
    var c_threshhold = d3.quantile(array_sorted, 0.4);  
    var d_threshhold = d3.quantile(array_sorted, 0.6); 
    var e_threshhold = d3.quantile(array_sorted, 0.8);  
   	var f_threshhold = d3.quantile(array_sorted, 1);
   	var variance = d3.variance(array_sorted);
   	var deviation = d3.deviation(array_sorted);
   	var mean = d3.mean(array_sorted);
   	var median = d3.median(array_sorted);
   	var min = d3.min(array_sorted);
   	var max = d3.max(array_sorted);



	
	//create an object where the key corresponds to a company position in the data variable and the value is the number of drugs it produces
    var objTotal = JSON.stringify(Object.assign({}, array_Total)); 


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
//const verySmallIndexes = toObject(array_Total, a_threshhold,b_threshhold-1);
const verySmallIndexes = toObject(array_Total, a_threshhold,b_threshhold-1);
const smallIndexes = toObject(array_Total, b_threshhold,c_threshhold-1);
const mediumSmallIndexes = toObject(array_Total, c_threshhold,d_threshhold-1);
const mediumLargeIndexes = toObject(array_Total, d_threshhold,e_threshhold-1);
const largeIndexes = toObject(array_Total, e_threshhold,500);
const veryLargeIndexes = toObject(array_Total, 501,max+1);


companiesCategories.push({"size": Object.keys(verySmallIndexes).length, "name": "VERY SMALL", "companiesIndexes": verySmallIndexes});
companiesCategories.push({"size": Object.keys(smallIndexes).length, "name": "SMALL", "companiesIndexes": smallIndexes});
companiesCategories.push({"size": Object.keys(mediumSmallIndexes).length, "name": "MEDIUM SMALL", "companiesIndexes": mediumSmallIndexes});
companiesCategories.push({"size": Object.keys(mediumLargeIndexes).length, "name": "MEDIUM LARGE", "companiesIndexes": mediumLargeIndexes});
companiesCategories.push({"size": Object.keys(largeIndexes).length, "name": "LARGE", "companiesIndexes": largeIndexes});
companiesCategories.push({"size": Object.keys(veryLargeIndexes).length, "name": "VERY LARGE", "companiesIndexes": veryLargeIndexes});


//retrieve company name from the mapped entries (data)
function getCompanyName(companyKey, arr){

	//filter data for the company names
	//var compNames=Object.keys(filtered).map(i=> filtered[i]);
	Object.values(companyKey).map(i=> 
		{Object.entries(dataByCompanies).forEach(([key, value]) => {
			if (i == key&& !arr.includes(value[0].company)){
 				arr.push(value[0].company);
 			}			

    	})}
	); //end Object.values(companyKey).map()

} //end getCompanyName()

function getListOfCompanyNames(companyKeys, companyArr){
	for (const companyKey of companyKeys) {
			getCompanyName(Object.values(companyKeys), companyArr);
	};

} //end function getListOfCompanyNames

	



///////////////////////////////////////////////
//////////////////*DISEASES*//////////////////
///////////////////////////////////////////////

function extractDiseases(arr, dataSource)
	{ Object.entries(dataSource).forEach(([key, value]) => {
		if (dataSource==data){
		var extractedDiseases = value.map(el => el.disease_class);
		for(var i = 0; i < extractedDiseases.length; i++){
				arr.push(extractedDiseases[i]);
			}//end for
		} else {extractedDiseases=value.disease_class;
			arr.push(extractedDiseases);
		} //end else
		}) //end forEach
	}; //end extractDiseases function 

extractDiseases(allDiseasesArray, data);



var distinctDiseasesClasses = [...new Set(allDiseasesArray)];
distinctDiseasesClasses = distinctDiseasesClasses.sort();





	//create object from array
    function arrayToObject(arr) { 
        var group_obj = {}; 
        for (var i = 0; i < arr.length; ++i){ 
            	group_obj[i] = arr[i]; 
        }
        return group_obj; 
    }


	var dKeys = ['C10 Nervous System Diseases', 'C14 Cardiovascular Diseases', 'C23 Pathological Conditions, Signs and Symptoms'];


	function createDeseaseData(deseaseKeys){
			//creates a data collection selectedData from diseaseKey: key corresponds to the company, value is company, disease_class (one of the diseaseKeys e.g.desease class), counts
    	deseaseKeys.forEach((deseaseKey) => {
	    	$.each(Object.values(filtered), function(key, value){	
	    		value.forEach(myFunction); 
					function myFunction(item, index) { 
						if(deseaseKey == item.disease_class){
	    					selectedData.push({ key: key, value : value[index], index: index });
	    				}
					}
	    	});
	    });

	} //end createDeseaseData finction

	function createRadarChart(){
	    //creates an object of keys from the selectedData
		var recordKeys = [...new Set (selectedData.map(function(d) { return ""+d.key+"" }))];

  		var recordValues = new Array();
    	recordKeys.forEach((recordKey) => {
    		var companiesDiseases = new Array();
	    	$.each(Object.values(selectedData), function(key, value){
		    	if(recordKey==value.key){
		    		companiesDiseases.push(value.value);	
		    	} //end if
	    	}); //end forEach
	    	recordValues.push(companiesDiseases);
	    });


	radarChart("#visualizationSpace", recordValues, radarChartOptions);

	selectedData = new Array();

	} //end createRadarChart function

	createDeseaseData(dKeys);

//to save the data in txt format
	var dataToStr= 'group,variable,mw,clogp,psa,hba,hbd' + '\n';
    $.each(Object.values(selectedData), function(key, value){

    			dataToStr += Object.values(value)[1].company + ',' + Object.values(value)[1].drug_pref_name + ',' + Object.values(value)[1].mw + ',' + Object.values(value)[1].clogp + ',' + Object.values(value)[1].psa + ',' + Object.values(value)[1].hba + ',' + Object.values(value)[1].hbd +'\n';
    	});

	function extractDiseasesByCounts(arr1, arr2, itemValues){	Object.entries(itemValues).forEach(([key, value]) => {
		var extractedDiseases = value.map(el => el.disease_class);
		var extractedCounts = value.map(el => el.counts);
		var extractedDrug = value.map(el => el.drug_pref_name);
		var extractedMw = value.map(el => el.mw);
		var extractedClogp = value.map(el => el.clogp);
		var extractedPsa = value.map(el => el.psa);
		var extractedHba = value.map(el => el.hba)
		var extractedHbd = value.map(el => el.hbd);


		for(var i = 0; i < extractedDiseases.length; i++){
				arr1.push({"disease" : extractedDiseases[i],"c": extractedCounts[i] });
		}

		for(var i = 0; i < extractedDiseases.length; i++){
				arr2.push({"group" : extractedDiseases[i],"variable": extractedDrug[i], "mw": extractedMw[i], "clogp": extractedClogp[i], "psa": extractedPsa[i], "hba": extractedHba[i], "hbd": extractedHbd[i] });
		}



	});

	} //end exctractDiseasesByCounts

	
	function createDotMatrix(){
			//variables for the array of selected companies
			var uSelectedCompanies = new Array(), arrDs = new Array(), 
			arrCs = new Array(), filteredDisArray2 = new Array();

			getListOfCompanyNames(uSelectedKeys, uSelectedCompanies);
			companiesList = [...uSelectedCompanies];


			//filter data for the user selected companies

			filtered = Object.keys(dataByCompanies)
	  			.filter(key => uSelectedKeys.includes(key))
	  			.reduce((obj, key) => {
	    		obj[key] = dataByCompanies[key];
	    		return obj;
	  		}, {});


			filteredValues = Object.values(filtered);


			extractDiseasesByCounts(arrDs, arrCs, filteredValues);

			var filteredDis2 = Object.values(filtered)
				.filter( (obj, val) => {

					Object.values(obj).forEach((val) => {

  					filteredDisArray2.push(val);	


					});
					return obj;
			}, {});


			objectfromArray2 = arrayToObject(filteredDisArray2);
	

			var updatedDiseasesArray = new Array();

			extractDiseases(updatedDiseasesArray, objectfromArray2);

			

			distinctDiseasesClasses = [...new Set(updatedDiseasesArray)];
			distinctDiseasesClasses = distinctDiseasesClasses.sort();



			dotMatrixChart("#visualizationSpace", Object.values(objectfromArray2),dotChartOptions);

			
	} //end create dotMatrix



	$(document).ready(function(){

		//show the svg

		// set the dimensions and margins of the graph
		var margin = {top: 80, right: 30, bottom: 30, left: 300},
		  width = 900 - margin.left - margin.right,
		  height = 600 - margin.top - margin.bottom;

		// append the svg object to the body of the page
		var svg = d3.select("#visualizationSpace")
		.append("svg")
		  .attr("width", width + margin.left + margin.right)
		  .attr("height", height + margin.top + margin.bottom)
		.append("g")
		  .attr("transform",
		        "translate(" + margin.left + "," + margin.top + ")");

		//show companies counts to the user
		var companiesIndexes= new Object();

			for (var i = 0; i < companiesCategories.length; ++i) {
				var companyNumbers = "<div></div>";
				var companyNumbersButton = "<button></button>";
				$(".stacked-companies > div:last-of-type").after($(companyNumbers));
	    		$(".stacked-companies > div:last-of-type").addClass("companies-counts");
	    		$(".stacked-companies > div:last-of-type").addClass("row");
	    		$(".companies-counts:last-of-type").append($(companyNumbers));
	    		$(".companies-counts:last-of-type").append($(companyNumbersButton));

			}


			$.each(companiesCategories,function(index,value){

				//const compCountsFirstEl = $(".companies-counts > div");
				const compCountsLastEl = $(".companies-counts > button");

					//$(compCountsFirstEl[index]).text(companiesCategories[index].size);
					$(compCountsLastEl[index]).text(`${companiesCategories[index].name} (${companiesCategories[index].size})`);


					$(compCountsLastEl[index]).attr("id", companiesCategories[index].name).addClass("btn btn-sm btn-block btn-secondary mb-1").attr("type", "button");
			});


			//show the list of companies
			function populateCompaniesList(){
				$.each(cSelectedCompanies,function(index,value){
					//create a div
					var div_check_box = "<div></div>";
					//create one row per company
					$("#companies_form").append($(div_check_box));

					$("#companies_form>div").addClass("form-check");

					//create a checkbox
					var checkbox="<input type='checkbox' id="+value+" value="+index+" name="+value+"><label for="+value+">"+value+"</label>";
					//append the div
					$(".form-check").eq(index).append($(checkbox));
					$("input").addClass("form-check-input");
					$("label").addClass("form-check-label small");

				});
				//create a button
				createButton("#companies_form", "companies-confirm", "CONFIRM", "#companies_form > button");
			} //end populateCompaniesList function




			//Disease classes

			//show disease counts to the user
			for (var i = 0; i < distinctDiseasesClasses.length; ++i) {
				var diseaseNumbers = "<div></div>";
				$(".stacked-diseases > div:last-of-type").after($(diseaseNumbers));
	    		$(".stacked-diseases > div:last-of-type").addClass("disease-counts");
	    		$(".stacked-diseases > div:last-of-type").addClass("row");
	    		$(".disease-counts:last-of-type").append($(diseaseNumbers));
	    		$(".disease-counts:last-of-type").append($(diseaseNumbers));

			};


			function populateDiseaseClasses(){
			//show the list of companies
				$.each(distinctDiseasesClasses,function(index,value){

					//create a checkbox
					var checkbox="<input type='checkbox' id="+value+" value="+value+" name="+value+"><label for="+value+">"+value+"</label>";
					//append the div
					$(".disease-class").eq(index).append($(checkbox));
					$("input").addClass("form-check-input");
					$("label").addClass("form-check-label small");

					});
				
			} //end populateDiseaseClasses

			function createDiseaseChoices(){

			$.each(distinctDiseasesClasses,function(index,value){

					//create a div
					var div_check_box = "<div></div>";
					//create one row per company
					$("#disease_classes_form").append($(div_check_box));
					$("#disease_classes_form>div").addClass("form-check");
					$("#disease_classes_form>div").addClass("disease-class");
			});
				//create a button
				createButton("#disease_classes_form", "disease-confirm", "CONFIRM", "#disease_classes_form > button");

			}//end createDiseaseChoices

			createDiseaseChoices();
			
			populateDiseaseClasses();


			//event listeners and logic related to them
			//adds event listener
			$("#companies_form").click(function(){
				//save user selection of companies in the companiesChoice array
				var companiesChoice = [];
	        	$.each($("input[class='form-check-input']:checked"), function(){
	            companiesChoice.push($(this).val());
	        });
	        // Loop through each cKey to get an array of companies keys
	       	companiesKeysToRender = companiesChoice.map(i => cKeys[i]);
			}); //end event listener for checkboxes

			//adds event listener
			$(document).on("click", "#companies-confirm", function(){

				onClickCompaniesConfirm(companiesIndexes);

				//delete the buttons "BY DISEASES" and " BY COMPANIES" as well as all descriptor buttons
				removeButtons("#by_diseases");
				removeButtons("#by_companies");
				removeButtons(".descriptor_buttons_d>button");
				removeButtons(".descriptor_buttons_c>button");


			});//end event listener for button

			//creates a collection of user selected companies, call a dot matrix chart, 
			//empties a disease classes form, 
			//creates and shows a new list of disease classes that correspond to the disease classes targeted by the companies that the user has selected
			function onClickCompaniesConfirm(indexesCollection){
				uSelectedKeys=Object.keys(indexesCollection).filter(key => { return ~companiesKeysToRender.indexOf(key) });
				createDotMatrix();
				
				//Remove whatever chart with the same id/class was present before
				$("#disease_classes_form").empty();
				createDiseaseChoices();
			
				populateDiseaseClasses();
			}// end onClickCompaniesConfirm function

			var unique = [];

			//adds event listener
			$("#disease_classes_form").click(function(){
				var deseasesChoice = [];
	        	$.each($(".disease-class>input[class='form-check-input']:checked"), function(){
	        		var label = $(this).next();
	            	deseasesChoice.push(label.text());
	        	});
	        	unique = [...new Set(deseasesChoice)];


			}); //end event listener for checkboxes

			//adds event listener
			$(document).on("click", "#disease-confirm", function(){
				//check that the companies have been selected before calling the next visualizations with the buttons
				if(companiesList.length>0){
					createDeseaseData(unique);
	    			createRadarChart();

	    			//create the buttons if they don't already exist, remove all of the descriptor buttons
	    			if($('#by_diseases').length > 0){
	    			} else{
	    				createButton(".choice_buttons", "by_diseases", "BY DISEASE CLASSES", ".choice_buttons > button:first-of-type");
					}
	    			if($('#by_companies').length > 0){
	    			} else{
	    				createButton(".choice_buttons", "by_companies", "BY COMPANIES", ".choice_buttons > button:last-of-type");
					}
					if($('.descriptor_buttons_d>button').length > 0){
	    				$('.descriptor_buttons_d>button').remove();
	    			} else{
	    			}

				}	

			});//end event listener for button

			//creates a button element and appends to the DOM
			function createButton(parentId, buttonId, textValue, position){
				var button = "<button></button>";	
				var buttonIdStr='#'+buttonId;
				$(parentId).append(button);
				$(position).attr("id", buttonId);
				$(buttonIdStr).text(textValue).addClass("btn btn-info mt-2").attr("type", "button");

			} //end createButton function

			//removes a button if it exists
			function removeButtons(buttonIdentifier){
				
				if($(buttonIdentifier).length > 0){
					$(buttonIdentifier).remove();
				} else{
				}

			} //end removeButtons function


			//creates a list of companies, adds event listener to each of the company (every company has a checkbox to listen to)
			function onClickCompanyClasses(companyClass, indexesCollection){
				var companyClassEl = $(companyClass);
				companyClassEl.onclick = showCompanyClasses(indexesCollection);
				function showCompanyClasses(iCollection){
					cKeys = Object.keys(iCollection);
					getListOfCompanyNames(cKeys, cSelectedCompanies);
					populateCompaniesList();
				}
				cSelectedCompanies=new Array();
			} //end onClickCompanyClasses function

			$(document).on("click", ".companies-counts>button", function(){
				$("#companies_form").empty();
				var buttonId = this.id;
				var companyCategoryData = companiesCategories.filter(function(key){
					return key.name == buttonId;
				});
				companiesIndexes = companyCategoryData[0].companiesIndexes;
				onClickCompanyClasses(buttonId, companyCategoryData[0].companiesIndexes);
			});///end event listener for button


			//adds event listener
			$(document).on("click", "#by_diseases", function(){
				
				if ($('.descriptor_buttons_d>button').length>0){
				} else{
					createDescriptorButtonsD();
				}
				if ($('.descriptor_buttons_c>button').length>0){
					removeButtons(".descriptor_buttons_c>button");
				} else{
				}


			});///end event listener for button

			$(document).on("click", "#by_companies", function(){
				
				if ($('.descriptor_buttons_d>button').length>0){
					removeButtons(".descriptor_buttons_d>button");
				} else{
				}
				if ($('.descriptor_buttons_c>button').length>0){
				} else{
					createDescriptorButtonsC();
				}

			});///end event listener for button

			//creates buttons for the choice "By diseases"
			function createDescriptorButtonsD(){
				createButton(".descriptor_buttons_d", 'mw', "MW", ".descriptor_buttons_d>button:nth-of-type(1)");
				createButton(".descriptor_buttons_d", 'clogp', "CLOGP", ".descriptor_buttons_d>button:nth-of-type(2)");
				createButton(".descriptor_buttons_d", 'arom', "AROM", ".descriptor_buttons_d>button:nth-of-type(3)");
				createButton(".descriptor_buttons_d", 'hba', "HBA", ".descriptor_buttons_d>button:nth-of-type(4)");
				createButton(".descriptor_buttons_d", 'hbd', "HBD", ".descriptor_buttons_d>button:nth-of-type(5)");
				createButton(".descriptor_buttons_d", 'rtb', "RTB", ".descriptor_buttons_d>button:nth-of-type(6)");
				createButton(".descriptor_buttons_d", 'psa', "PSA", ".descriptor_buttons_d>button:nth-of-type(7)");
				createButton(".descriptor_buttons_d", 'apka', "APKA", ".descriptor_buttons_d>button:nth-of-type(8)");
				createButton(".descriptor_buttons_d", 'bpka', "BPKA", ".descriptor_buttons_d>button:nth-of-type(9)");
			} //end createDescriptorButtonsD function

			//creates buttons for the choice "By companies"
			function createDescriptorButtonsC(){
				createButton(".descriptor_buttons_c", 'mw', "MW", ".descriptor_buttons_c>button:nth-of-type(1)");
				createButton(".descriptor_buttons_c", 'clogp', "CLOGP", ".descriptor_buttons_c>button:nth-of-type(2)");
				createButton(".descriptor_buttons_c", 'arom', "AROM", ".descriptor_buttons_c>button:nth-of-type(3)");
				createButton(".descriptor_buttons_c", 'hba', "HBA", ".descriptor_buttons_c>button:nth-of-type(4)");
				createButton(".descriptor_buttons_c", 'hbd', "HBD", ".descriptor_buttons_c>button:nth-of-type(5)");
				createButton(".descriptor_buttons_c", 'rtb', "RTB", ".descriptor_buttons_c>button:nth-of-type(6)");
				createButton(".descriptor_buttons_c", 'psa', "PSA", ".descriptor_buttons_c>button:nth-of-type(7)");
				createButton(".descriptor_buttons_c", 'apka', "APKA", ".descriptor_buttons_c>button:nth-of-type(8)");
				createButton(".descriptor_buttons_c", 'bpka', "BPKA", ".descriptor_buttons_c>button:nth-of-type(9)");
			} //end createDescriptorButtonsC function


			//adds event listener and calls respective visualization
			function addEventListener(elementToListenTo, descriptorId, chartName){

				$(document).on("click", elementToListenTo, function(){
					chartName("#visualizationSpace", unique, companiesList, descriptorId);
				});///end event listener for button
			}


			//buttons for triggering heatmap chart

			addEventListener(".descriptor_buttons_d>#mw", "mw", heatmapChart);
			addEventListener(".descriptor_buttons_d>#clogp", "clogp", heatmapChart);
			addEventListener(".descriptor_buttons_d>#arom", "arom", heatmapChart);
			addEventListener(".descriptor_buttons_d>#hba", "hba", heatmapChart);
			addEventListener(".descriptor_buttons_d>#hbd", "hbd", heatmapChart);
			addEventListener(".descriptor_buttons_d>#rtb", "rtb", heatmapChart);
			addEventListener(".descriptor_buttons_d>#psa", "psa", heatmapChart);
			addEventListener(".descriptor_buttons_d>#apka", "apka", heatmapChart);
			addEventListener(".descriptor_buttons_d>#bpka", "bpka", heatmapChart);


			//buttons for triggering box-whisker chart

			addEventListener(".descriptor_buttons_c>#mw", "mw", boxWhiskerChart);
			addEventListener(".descriptor_buttons_c>#clogp", "clogp", boxWhiskerChart);
			addEventListener(".descriptor_buttons_c>#arom", "arom", boxWhiskerChart);
			addEventListener(".descriptor_buttons_c>#hba", "hba", boxWhiskerChart);
			addEventListener(".descriptor_buttons_c>#hbd", "hbd", boxWhiskerChart);
			addEventListener(".descriptor_buttons_c>#rtb", "rtb", boxWhiskerChart);
			addEventListener(".descriptor_buttons_c>#psa", "psa", boxWhiskerChart);
			addEventListener(".descriptor_buttons_c>#apka", "apka", boxWhiskerChart);
			addEventListener(".descriptor_buttons_c>#bpka", "bpka", boxWhiskerChart);



	}); //end document ready

return data;

}; //end prepareData


