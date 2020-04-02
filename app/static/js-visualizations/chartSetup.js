
//Radar Chart Function inspired by Nadieh Bremer, VisualCinnamon.com
////////////////////////////////////////////////////////////// 
			//////////////////////// Set-Up ////////////////////////////// 
			////////////////////////////////////////////////////////////// 

			var margin = {top: 100, right: 100, bottom: 100, left: 100},
				width = Math.min(700, window.innerWidth - 10) - margin.left - margin.right,
				height = Math.min(width, window.innerHeight - margin.top - margin.bottom - 20);
					
			////////////////////////////////////////////////////////////// 
			//////////////////// Draw the Chart ////////////////////////// 
			////////////////////////////////////////////////////////////// 

			//8 colors from colorbrewer
			var color = d3.scaleOrdinal()
				.range(['#06D6A0','#118AB2','#E76F51', '#FFD166', '#073B4C']);
//['#2A9D8F','#E9C46A','#E76F51', '#264653', '#F4A261']
//['#003f5c','#58508d','#bc5090','#ff6361','#ffa600']
//['#7b3294','#c2a5cf','#f7f7f7','#a6dba0','#008837']
				//['#66c2a5','#fc8d62','#8da0cb','#e78ac3','#a6d854']
//['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00']
//['#8dd3c7','#ffffb3','#bebada','#fb8072','#80b1d3','#fdb462','#b3de69','#fccde5','#d9d9d9','#bc80bd']
				//.range(['#1b9e77','#d95f02','#7570b3','#e7298a','#66a61e','#e6ab02','#a6761d','#666666']);
				//10 colors
				//.range(["#a6cee3", "#1f78b4", "#b2df8a", "#33a02c", "#fb9a99", "#e31a1c", "#fdbf6f", "#ff7f00", "#cab2d6", "#6a3d9a" ]);
				//	.range(["#AFC52F", "#ff6600", "#2a2fd4"]);

				
				
			/*var radarChartOptions = {
			  w: width,
			  h: height,
			  margin: margin,
			  maxValue: 0.5,
			  levels: 5,
			  roundStrokes: true,
			  color: color,
			  format: '.0f',
			  legend: { title: 'Drug targets by companies', translateX: 100, translateY: 40 },
			  unit: ' drugs'
			};
			*/
			var radarChartOptions = {
			  w: width,
			  h: height,
			  margin: margin,
			  maxValue: 60,
			  levels: 6,
			  roundStrokes: true,
			  color: d3.scaleOrdinal(d3.schemeCategory10),
				format: '.0f',
				legend: { title: 'Drug targets by companies', translateX: 100, translateY: 40 },
				unit: 'drugs'
			};

			var dotChartOptions = {
			    dot_radius : 5,
			    no_of_circles_in_a_row: 40,
	            dot_padding_left : 5,
	            dot_padding_right : 5,
	            dot_padding_top : 5,
	            dot_padding_bottom : 5
			}

			//Load the data and Call function to draw the Radar chart
			//cdc_data.json
			//cd_psa_data.json
			//Company_disease_psa_hbd.json
			d3.json("/vis/cdcdata", function(error, data){
				console.log(data);
				RadarChart(".radarChart", data, radarChartOptions);
				//console.log("Data after loading", data);
			});
			