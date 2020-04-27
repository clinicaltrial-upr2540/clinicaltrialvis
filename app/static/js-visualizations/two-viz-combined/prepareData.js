"use strict";


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
		deseasesToRender = new Array(), selectedData = new Array();

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
		//console.log("Data values mapped", data, typeof(data));
		//untouched copy of data to be used in further manipulations
		var dataByCompanies = dataCompany.map(function(d) { return d.values });

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

    	
	//get keys of the selected category of companies
	/*var cKeys = Object.keys(largeIndexes);
	console.log("keys for a category of companies", cKeys, typeof(cKeys));

	getListOfCompanyNames(cKeys, cSelectedCompanies);



	
	console.log("Category list of companies has ", cSelectedCompanies);*/



    ///////////////////////////////////////////////
    //////////////////*DISEASES*//////////////////
    ///////////////////////////////////////////////

	function extractDiseases(arr, dataSource)
		{ Object.entries(dataSource).forEach(([key, value]) => {
			//for debugging
			//console.log(key);
			//console.log(value);
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

	console.log("allDiseasesArray", allDiseasesArray);


	var distinctDiseasesClasses = [...new Set(allDiseasesArray)];
	distinctDiseasesClasses = distinctDiseasesClasses.sort();
	console.log("distinctDiseaseClasses", distinctDiseasesClasses);




		//create object from array
	    function arrayToObject(arr) { 
            var group_obj = {}; 
            for (var i = 0; i < arr.length; ++i){ 
                	group_obj[i] = arr[i]; 
            }
            //Object.values(group_obj).forEach(value => console.log(value.company));
            return group_obj; 
        }


    	var dKeys = ['C10 Nervous System Diseases', 'C14 Cardiovascular Diseases', 'C23 Pathological Conditions, Signs and Symptoms'];

    	//console.log("FILTERED DISEASE data ", Object.values(filtered), typeof(Object.values(filtered)));


    	function createDeseaseData(deseaseKeys){
    		console.log("deseaseKeys", deseaseKeys);
    		console.log("filtered", filtered);
  			//creates a data collection selectedData from diseaseKey: key corresponds to the company, value is company, disease_class (one of the diseaseKeys e.g.desease class), counts
	    	deseaseKeys.forEach((deseaseKey) => {
		    	$.each(Object.values(filtered), function(key, value){	
		    		value.forEach(myFunction); 
						function myFunction(item, index) { 
							if(deseaseKey == item.disease_class){
		    					//console.log(item.disease_class, key, index);
		    					selectedData.push({ key: key, value : value[index], index: index });
		    				}
						}
		    	});
		    });

		    console.log("selectedData", selectedData, typeof(selectedData));
		} //end createDeseaseData finction

		function createRadarChart(){
		    //creates an object of keys from the selectedData
			var recordKeys = [...new Set (selectedData.map(function(d) { return ""+d.key+"" }))];

	  		var recordValues = new Array();
	    	recordKeys.forEach((recordKey) => {
	    		var companiesDiseases = new Array();
		    	$.each(Object.values(selectedData), function(key, value){
		    		console.log(value.key, value.value);
			    	if(recordKey==value.key){
			    		companiesDiseases.push(value.value);	
			    	} //end if
		    	}); //end forEach
		    	recordValues.push(companiesDiseases);
		    });
		    console.log("recordValues", recordValues);


		radarChart("#visualizationSpace", recordValues, radarChartOptions);

		selectedData = new Array();

		} //end createRadarChart function

		createDeseaseData(dKeys);

//to save the data in txt format
		var dataToStr= 'group,variable,mw,clogp,psa,hba,hbd' + '\n';
	    $.each(Object.values(selectedData), function(key, value){

	    			dataToStr += Object.values(value)[1].company + ',' + Object.values(value)[1].drug_pref_name + ',' + Object.values(value)[1].mw + ',' + Object.values(value)[1].clogp + ',' + Object.values(value)[1].psa + ',' + Object.values(value)[1].hba + ',' + Object.values(value)[1].hbd +'\n';
	    			
	    		
	    		//value.forEach(myFunction);
	    		//Object.values(value).map((key,value, index) => console.log(key, value, index));
	    		

	    	});
	    console.log(dataToStr);




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
			/*console.log(passedCompanyKeys);
				var uKeys = passedCompanyKeys.split(',');
				console.log(uKeys);*/
				console.log("in createDotMatrix", uSelectedKeys, typeof(uSelectedKeys));
				//variables for the array of selected companies
				var uSelectedCompanies = new Array(), arrDs = new Array(), 
				arrCs = new Array(), filteredDisArray2 = new Array();

				getListOfCompanyNames(uSelectedKeys, uSelectedCompanies);

				console.log("List for selected companies has ", uSelectedCompanies);

				//filter data for the user selected companies

				filtered = Object.keys(dataByCompanies)
		  			.filter(key => uSelectedKeys.includes(key))
		  			.reduce((obj, key) => {
		    		obj[key] = dataByCompanies[key];
		    		return obj;
		  		}, {});

				console.log("FILTERED data ", filtered, typeof(filtered));

				filteredValues = Object.values(filtered);

				console.log("ITEMS", filteredValues);

				
				extractDiseasesByCounts(arrDs, arrCs, filteredValues);

				var filteredDis2 = Object.values(filtered)
					.filter( (obj, val) => {

  					Object.values(obj).forEach((val) => {

      					filteredDisArray2.push(val);	


  					});
  					return obj;
				}, {});


				console.log("filteredDisArray2 in the confirm scope, createDotMatrix", filteredDisArray2)
				//createDotMatrix(filteredDisArray2);

				objectfromArray2 = arrayToObject(filteredDisArray2);
				console.log("objectfromArray2", objectfromArray2);

				var updatedDiseasesArray = new Array();

				extractDiseases(updatedDiseasesArray, objectfromArray2);

				console.log("allDiseasesArray in createDotMatrix", updatedDiseasesArray);
				

				distinctDiseasesClasses = [...new Set(updatedDiseasesArray)];
				distinctDiseasesClasses = distinctDiseasesClasses.sort();
				console.log("distinctDiseaseClasses in createDotMatrix", distinctDiseasesClasses);


				dotMatrixChart("#visualizationSpace", Object.values(objectfromArray2),dotChartOptions);

				
		} //end create dotMatrix


		dotMatrixChart("#visualizationSpace", Object.values(objectfromArray2),dotChartOptions);


		


	$(document).ready(function(){
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
    			//console.log(companiesCategories[index].name, companiesCategories[index].size);
    			const compCountsFirstEl = $(".companies-counts > div");
    			const compCountsLastEl = $(".companies-counts > button");
    			//var idName = companiesCategories[index].name.substr(0, 3).toLowerCase();
    			//$(".companies-counts").attr("id", idName);
   				$(compCountsFirstEl[index]).text(companiesCategories[index].size);
   				$(compCountsLastEl[index]).text(companiesCategories[index].name);
   				/*var strForId = companiesCategories[index].name.toLowerCase();
   				strForId=strForId.replace(/^\w/, c => c.toUpperCase());
   				strForId=strForId.replace(/\s+/g, '');*/
   				$(compCountsLastEl[index]).attr("id", companiesCategories[index].name).addClass("btn btn-light").attr("type", "button");
    		});

    		//text("VERY SMALL COMPANIES");
    		//$(".stacked > p:nth-of-type(2)").after($(companyNumbers)).addClass("companies-counts");

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
					$("label").addClass("form-check-label");

				});
				//create a button
				var button = "<button></button>";
				$("#companies_form").append(button);
				$("#companies_form > button").attr("id", "companies-confirm");
				$("#companies-confirm").text("Confirm").addClass("btn btn-info").attr("type", "button");
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
					$("label").addClass("form-check-label");

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
				var button = "<button></button>";
				$("#disease_classes_form").append(button);
				$("#disease_classes_form > button").attr("id", "disease-confirm");
				$("#disease-confirm").text("Confirm").addClass("btn btn-info").attr("type", "button");
			}//end createDiseaseChoices

			createDiseaseChoices();
			
			populateDiseaseClasses();


			//event listeners
			//event listener for the button companies_form
			$("#companies_form").click(function(){
				//save user selection of companies in the companiesChoice array
				var companiesChoice = [];
            	$.each($("input[class='form-check-input']:checked"), function(){
                companiesChoice.push($(this).val());
                console.log("companiesIndexes", companiesIndexes);
            });
            // Loop through each cKey to get an array of companies keys
           	companiesKeysToRender = companiesChoice.map(i => cKeys[i]);
			}); //end event listener for checkboxes

			$(document).on("click", "#companies-confirm", function(){

				onClickCompaniesConfirm(companiesIndexes);


			});//end event listener for button

			function onClickCompaniesConfirm(indexesCollection){
				uSelectedKeys=Object.keys(indexesCollection).filter(key => { return ~companiesKeysToRender.indexOf(key) });
				createDotMatrix();
				//Remove whatever chart with the same id/class was present before
	
				$("#disease_classes_form").empty();
				createDiseaseChoices();
			
				populateDiseaseClasses();
			}// end

			var unique = [];

			
			$("#disease_classes_form").click(function(){
				var deseasesChoice = [];
            	$.each($(".disease-class>input[class='form-check-input']:checked"), function(){
            		var label = $(this).next();
                	deseasesChoice.push(label.text());
            	});
            	unique = [...new Set(deseasesChoice)];
            console.log('Selected disease classes', unique);
            // Loop through each cKey

           	//deseasesToRender = deseasesChoice.map(i => dKeys[i]);
            //console.log('deseasesToRender', deseasesToRender);

			}); //end event listener for checkboxes

			/*$("#disease-confirm").click(function(){
				console.log("clicked disease-confirm");

    			createDeseaseData(unique);



			});*///end event listener for button

			$(document).on("click", "#disease-confirm", function(){
				console.log("clicked disease-confirm");

    			createDeseaseData(unique);
    			createRadarChart();
			});//end event listener for button

			/*$(document).on("click", "#Large", function(){
				console.log("MediumLarge is clicked");
				cKeys = Object.keys(largeIndexes);
				console.log("keys for a category of companies", cKeys, typeof(cKeys));

				getListOfCompanyNames(cKeys, cSelectedCompanies);
				populateCompaniesList();

			});*///end event listener for button

			$(document).on("click", ".companies-counts>button", function(){
				$("#companies_form").empty();
				var buttonId = this.id;
				var companyCategoryData = companiesCategories.filter(function(key){
					console.log(key.name);
					/*var strForId = key.name.toLowerCase();
   					strForId=strForId.replace(/^\w/, c => c.toUpperCase());
   					strForId=strForId.replace(/\s+/g, '');*/
					return key.name == buttonId;
				});
				console.log("companyCategoryData", companyCategoryData[0].companiesIndexes);
				companiesIndexes = companyCategoryData[0].companiesIndexes;
				onClickCompanyClasses(buttonId, companyCategoryData[0].companiesIndexes);
			});///end event listener for button

			function onClickCompanyClasses(companyClass, indexesCollection){
				var companyClassEl = $(companyClass);
				companyClassEl.onclick = showCompanyClasses(indexesCollection);
				function showCompanyClasses(iCollection){
					cKeys = Object.keys(iCollection);
					console.log("keys for a category of companies", cKeys, typeof(cKeys));
					getListOfCompanyNames(cKeys, cSelectedCompanies);
					populateCompaniesList();
				}
				cSelectedCompanies=new Array();
			}
			//onClickCompanyClasses("#LARGE", largeIndexes);




	}); //end document ready
	
	return data;

}; //end prepareData


