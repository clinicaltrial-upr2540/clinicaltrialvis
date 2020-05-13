document.addEventListener('DOMContentLoaded', () => {
    /**
    Build the initial page
    */

    buildSelectionSidebar();

    /**
    End page building
    */

    /**
    Begin event listeners
    */

    // Update Preview button functionality goes here
    document.querySelector('#update-preview-button').onclick = () => {
        // Here, we might gather a list of the checked boxes on the left sidebar
        // Here, gather a list of filters (none by default)
        var jsonToPost = buildDataRequest();

        jsonToPost["join_style"] = document.querySelector('#joinSelect').value;
        jsonToPost["export"] = "false";
        jsonToPost["single_file"] = "true";
        jsonToPost["limit"] = parseInt(document.querySelector('#resultsSelect').value, 10);

        // Request the data
        requestPreviewData(jsonToPost);
    };

    // Export button functionality
    $('#exportModal').on('shown.bs.modal', function (e) {
        // Here, we gather a list of the checked boxes on the left sidebar
        // Here, gather a list of filters (none by default)
        var jsonToPost = buildDataRequest();

        jsonToPost["join_style"] = document.querySelector('#joinSelect').value;
        jsonToPost["export"] = "true";

        if (document.querySelector('#multi-file-checkbox').checked == true) {
            jsonToPost["single_file"] = "false";
        } else {
            jsonToPost["single_file"] = "true";
        }
        
        // Request the data
        requestExport(jsonToPost);
    })

    /**
    End event listeners
    */

});

/***************************
*     Begin functions
***************************/

// Function to build sidebar to select views and fields
function buildSelectionSidebar() {
    var viewRequest = new XMLHttpRequest();

    const thead = document.createElement('thead');

    // Add the sidebar table headers
    document.querySelector('#selection-sidebar').innerHTML = '';
    thead.innerHTML = `<tr class="table-active"><th>Enabled</th><th>View name</th></tr>`;
    document.querySelector('#selection-sidebar').append(thead);

    // Get the list of views and append to sidebar
    viewRequest.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            try {
                var viewList = JSON.parse(this.responseText);
                viewList = viewList["views"];
                buildSidebarViewEntry(viewList);
            } catch(err) {
                console.log(err.message + " in " + this.responseText);
                return;
            }
        }
    };
    viewRequest.open("GET", "/data/views", true);
    viewRequest.send();
}

// Function to add a single view to the sidebar
// Specific columns are nested under the view
function buildSidebarViewEntry(viewList) {
    for (var key in viewList) {
        var columnRequest = new XMLHttpRequest();
        const tr = document.createElement('tr');
        const hidden_tbody = document.createElement('tbody');

        // Build table row for view name and master switch
        tr.setAttribute("class", "table-active");
        tr.innerHTML = `<td>
    <label class="custom-toggle">
        <input type="checkbox" data-toggle="toggle" class="parent-checkbox" id="${viewList[key]}checkbox" name="${viewList[key]}">
        <span class="custom-toggle-slider rounded-circle parent-checkbox" data-label-off="All" data-label-on="All"></span>
    </label>
</td>
<td data-toggle="collapse" href="#${viewList[key]}fields" aria-expanded="false" aria-controls="${viewList[key]}fields" class="accordion-toggle"><a href="#">${viewList[key]} <small class="text-muted">click to expand</small></a></td>`;

        // Build tbody to contain the list of column headers
        hidden_tbody.setAttribute("class", "collapse");
        hidden_tbody.setAttribute("id", `${viewList[key]}fields`);

        document.querySelector('#selection-sidebar').append(tr);
        document.querySelector('#selection-sidebar').append(hidden_tbody);

        // Get the list of fields in the view and append to sidebar
        columnRequest.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                try {
                    var fieldList = JSON.parse(this.responseText);
                    buildSidebarColumnEntry(fieldList);
                } catch(err) {
                    console.log(err.message + " in " + this.responseText);
                    return;
                }
            }
        };
        columnRequest.open("GET", `/data/view/${viewList[key]}`, true);
        columnRequest.send();
    }

    // Add a listener for all parent checkboxes
    document.querySelectorAll(".parent-checkbox").forEach(function(parentSwitch) {
        parentSwitch.onclick = () => {
            var parentName = parentSwitch.getAttribute("name");
            var childSwitches = document.querySelectorAll(`.parent-${parentName}`);

            // Switch all child switches when you click the parent switch
            childSwitches.forEach(function(childSwitch) {
                if (parentSwitch.checked) {
                    childSwitch.checked = true;
                } else {
                    childSwitch.checked = false;
                }
            });
        };
    });
}

// Function to add a single column header to the sidebar
function buildSidebarColumnEntry(fieldList) {
    view = fieldList["view_name"];

    // Table of fields to be added
    const tr = document.createElement('tr');

    for (var key in fieldList["columns"]) {
        const tr = document.createElement('tr');

        // Build the table entry for a single column field
        tr.innerHTML = `<td class=>
    <label class="custom-toggle">
        <input type="checkbox" data-toggle="toggle" class="child-checkbox parent-${view}" data-parent="${view}" id="${view}.${fieldList["columns"][key]["column_name"]}" name="${view}.${fieldList["columns"][key]["column_name"]}">
        <span class="custom-toggle-slider" data-label-off="No" data-label-on="Yes"></span>
    </label>
</td>
<td class="text-muted">${fieldList["columns"][key]["column_name"]}</td>`;
        
        // Append the column to the sidebar
        document.querySelector(`#${view}fields`).append(tr);
    }

    // Add a listener for all child (baby) checkboxes
    document.querySelectorAll(".child-checkbox").forEach(function(babySwitch) {
        babySwitch.onclick = () => {
            var babyParent = babySwitch.getAttribute("data-parent");

            // Switch all child switches when you click the parent switch
            if (babySwitch.checked == false) {
                document.querySelector(`#${babyParent}checkbox`).checked = false;
            }
        };
    });
}

// Function to request preview data to populate the table in the UI
function requestPreviewData(jsonToPost) {
    var dataRequest = new XMLHttpRequest();

    // Get the list of views and append to sidebar
    dataRequest.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            try {
                var data = JSON.parse(this.responseText);
                buildDataPreviewTable(data, jsonToPost);
            } catch(err) {
                // If no data comes back, insert error message
                document.querySelector('#data-preview').innerHTML = `
                <div class="alert alert-danger" role="alert">
                    <p>An error occurred while retrieving data. Please refrsh the page and try again!</p>
                    <p><pre>${err.message}</pre></p>
                </div>`;
                console.log(err.message + " in " + this.responseText);
                return;
            }
        }
    };
    dataRequest.open("POST", "/data/explore", true);
    dataRequest.setRequestHeader("Content-type", "application/json");
    dataRequest.send(JSON.stringify(jsonToPost));
}

// Function to request full data export to download
function requestExport(jsonToPost) {
    var dataRequest = new XMLHttpRequest();

    // Perform the actual request
    dataRequest.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            try {
                // Generate timestamp for filename
                var date = new Date();
                var hours = date.getHours();
                var minutes = date.getMinutes();
                var seconds = date.getSeconds();

                hours = (hours < 10 ? "0" : "") + hours;
                minutes = (minutes < 10 ? "0" : "") + minutes;
                seconds = (seconds < 10 ? "0" : "") + seconds;

                datestring = `${date.getFullYear()}.${date.getMonth()+1}.${date.getDate()}-${hours}.${minutes}.${seconds}`

                // Try to find out the filename from the content disposition `filename` value
                var disposition = this.getResponseHeader('Content-Disposition');
                var matches = /"([^"]*)"/.exec(disposition);
                var filename = (matches != null && matches[1] ? matches[1] : `export-${datestring}.zip`);

                // The actual download
                var blob = new Blob([this.response], { type: 'application/octet-stream' });
                var link = document.createElement('a');
                link.href = window.URL.createObjectURL(blob);
                link.download = filename;

                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);

                // Remove the loading modal
                $('#exportModal').modal('hide');
            } catch(err) {
                // Remove the loading modal
                $('#exportModal').modal('hide');

                // If no data comes back, insert error message
                console.log(err.message + " in " + this.responseText);
                return;
            }
        }
    };
    dataRequest.open("POST", "/data/explore", true);
    dataRequest.setRequestHeader("Content-type", "application/json");
    dataRequest.responseType = 'blob';
    dataRequest.send(JSON.stringify(jsonToPost));
}

// Function to build the preview data table once data has been returned
function buildDataPreviewTable(data, jsonPosted) {
    var html_buffer = '';

    // Extract the data
    column_names = data["data"]["view_column_names"];
    sample_data = data["data"]["data"];

    // Reset the table
    document.querySelector('#data-preview').innerHTML = '';

    // Build and insert the table headers
    const thead = document.createElement('thead');
    thead.setAttribute('class', 'thead-light');
    for (var key in column_names) {
        html_buffer = html_buffer.concat(`<th>${ column_names[key][1] }</th>`)
    }
    thead.innerHTML = html_buffer;
    document.querySelector('#data-preview').append(thead);

    // Build and insert the filter fields
    html_buffer = '';
    const tr = document.createElement('tr');
    tr.setAttribute('class', 'table-active');
    for (var key in column_names) {
        // Determine if data field is a number or text
        var data_type;
        if(isNaN(sample_data[0][key])) {
            data_type = "text";
        } else {
            data_type = "number";
        }

        html_buffer = html_buffer.concat(`<td><input class="form-control form-control-sm data-filter" data-datatype="${data_type}" data-view="${column_names[key][0]}" data-column="${column_names[key][1]}" type="text" placeholder="filter"></td>`);
    }
    tr.innerHTML = html_buffer;
    document.querySelector('#data-preview').append(tr);

    // If there were any filters set on the last refresh, set them again
    for (var view in jsonPosted["data_list"]) {
        if ("filters" in jsonPosted["data_list"][view]) {
            for (var filter in jsonPosted["data_list"][view]["filters"]) {
                // Get the operator
                var filterOperator = "";
                if (jsonPosted["data_list"][view]["filters"][filter]["operator"] != "matches") {
                    filterOperator = jsonPosted["data_list"][view]["filters"][filter]["operator"];
                }

                document.querySelector(`[data-view="${jsonPosted["data_list"][view]["view_name"]}"][data-column="${jsonPosted["data_list"][view]["filters"][filter]["column_name"]}"]`).value = `${filterOperator}${jsonPosted["data_list"][view]["filters"][filter]["target"]}`;
            }
        }
    }

    // Build and insert the data
    for (var key in sample_data) {
        const data_tr = document.createElement('tr');
        html_buffer = '';

        for (var inner_key in sample_data[key]) {
            // If the field is "compound_name", hyperlink to the other page
            if(column_names[inner_key][1] == "compound_name") {
                html_buffer = html_buffer.concat(`<td class="text-truncate" style="max-width: 150px;" title="${sample_data[key][inner_key]}"><a href="/explore/compound?compound_name=${sample_data[key][inner_key]}" target="_blank">${sample_data[key][inner_key]}</a></td>`);
            } else {
                html_buffer = html_buffer.concat(`<td class="text-truncate" style="max-width: 150px;" title="${sample_data[key][inner_key]}">${sample_data[key][inner_key]}</td>`);
            }
        }

        data_tr.innerHTML = html_buffer;
        document.querySelector('#data-preview').append(data_tr);
    }
}

// Function to build the JSON object to request data from the API
// This is a big function, but organized into first checkboxes, then filters
function buildDataRequest() {
    var rawFields = [];
    var fieldDict = {};
    var filterDict = {};
    var resultJSON = {};
    resultJSON["data_list"] = [];

    // Loop through all the column switches, and if they are checked, add them to the list
    document.querySelectorAll(".child-checkbox").forEach(function(babySwitch) {
        if (babySwitch.checked == true) {
            rawFields.push(babySwitch.getAttribute("name"));
        }
    });

    // Loop through the resulting columns
    rawFields.forEach(function(field) {
        var splitBuffer = field.split(".");

        // If this view isn't in the dict yet, add it
        if (!(splitBuffer[0] in fieldDict)) {
            fieldDict[splitBuffer[0]] = [];
        }

        // Add the field being requested to that view
        fieldDict[splitBuffer[0]].push(splitBuffer[1]);
    });

    // Loop through all the filters, and if they are set, add to the list
    document.querySelectorAll(".data-filter").forEach(function(filterField) {
        if (filterField.value.length > 0) {
            var filterDatatype = filterField.getAttribute("data-datatype");
            var filterView = filterField.getAttribute("data-view");
            var filterColumn = filterField.getAttribute("data-column");
            var filterValue = filterField.value;

            // First make sure the field is still relevant (the user may have unchecked it since the last refresh)
            // if (fieldDict[filterView].includes(filterColumn)) {
                var filterType = "matches";
                if (filterDatatype == "number") {
                    filterType = "=";
                } else {
                    filterType = "matches";
                }

                // Derive type of filter comparison from first character
                if (filterValue.charAt(0) == '>') {
                    filterType = '>';
                    filterValue = filterValue.substr(1);
                } else if (filterValue.charAt(0) == '<') {
                    filterType = '<';
                    filterValue = filterValue.substr(1);
                } else if (filterValue.charAt(0) == '=') {
                    filterType = '=';
                    filterValue = filterValue.substr(1);
                }

                // If this view isn't in the dict yet, add it
                if (!(filterView in filterDict)) {
                    filterDict[filterView] = [];
                }

                // Add the filter to that view
                filterDict[filterView].push({column_name:filterColumn, operator:filterType, target:filterValue});
            // }
        }
    });

    // Avengers, assemble (the JSON object to return)
    for (const key of Object.keys(fieldDict)) {
        var viewObj = {};

        viewObj["view_name"] = key;
        viewObj["column_list"] = fieldDict[key];
        if (key in filterDict) {
            viewObj["filters"] = filterDict[key];
        }

        resultJSON["data_list"].push(viewObj);
    }

    return resultJSON;
}



