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

    // Checkbox listeners go here
    document.getElementsByClassName('parent-checkbox').onclick = () => {
        console.log("YAY");
    };

    // Update Preview button functionality goes here
    document.querySelector('#update-preview-button').onclick = () => {
        // Here, we might gather a list of the checked boxes on the left sidebar
        // Here, gather a list of filters (none by default)

        // Request the data
        requestPreviewData();
    };

    // Export button functionality goes here

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
    thead.innerHTML = `<tr><th>View name</th><th>Enabled</th></tr>`;
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
        const tr2 = document.createElement('tr');

        // Build table row for view name and master switch
        tr.innerHTML = `<td data-toggle="collapse" data-target="#${viewList[key]}fields" class="accordion-toggle">${viewList[key]} <small class="text-muted">click to expand</small></td>
<td>
    <label class="custom-toggle">
        <input type="checkbox" checked data-toggle="toggle" id="${viewList[key]}checkbox" name="${viewList[key]}">
        <span class="custom-toggle-slider rounded-circle parent-checkbox" data-label-off="All" data-label-on="All"></span>
    </label>
</td>
`;

        // Build table row to contain the list of column headers
        tr2.innerHTML = `<td class="hiddenRow" colspan="2">
    <table class="table table-sm accordion-body collapse ml-3" id="${viewList[key]}fields">
    </table>
</td>`;

        document.querySelector('#selection-sidebar').append(tr);
        document.querySelector('#selection-sidebar').append(tr2);

        // Add a listener for all child checkboxes
        document.querySelector(`#${viewList[key]}checkbox`).onclick = () => {
            console.log("YAY");
        };

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
}

// Function to add a single column header to the sidebar
function buildSidebarColumnEntry(fieldList) {
    view = fieldList["view_name"];

    // Table of fields to be added
    const tr = document.createElement('tr');

    for (var key in fieldList["columns"]) {
        const tr = document.createElement('tr');

        // Build the table entry for a single column field
        tr.innerHTML = `<td class="text-muted">${fieldList["columns"][key]["column_name"]}</td>
<td>
    <label class="custom-toggle">
        <input type="checkbox" checked data-toggle="toggle" id="${view}.${fieldList["columns"][key]["column_name"]}" name="${view}.${fieldList["columns"][key]["column_name"]}">
        <span class="custom-toggle-slider rounded-circle" data-label-off="No" data-label-on="Yes"></span>
    </label>
</td>`;
        
        // Append the column to the sidebar
        document.querySelector(`#${view}fields`).append(tr);
    }
}

function requestPreviewData() {
    var dataRequest = new XMLHttpRequest();

    // Get the list of views and append to sidebar
    dataRequest.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            try {
                var data = JSON.parse(this.responseText);
                buildDataPreviewTable(data);
            } catch(err) {
                // TODO: If no data comes back, insert error message
                document.querySelector('#data-preview').innerHTML = `<div class="alert alert-danger" role="alert">An error occurred while retrieving data. Please try again!</div>`;
                console.log(err.message + " in " + this.responseText);
                return;
            }
        }
    };
    dataRequest.open("GET", "/data/explore", true);
    dataRequest.send();
}

function buildDataPreviewTable(data) {
    var html_buffer = '';

    // Extract the data
    column_names = data["data"][0]["column_names"];
    sample_data = data["data"][0]["data"];

    // Reset the table
    document.querySelector('#data-preview').innerHTML = '';

    // Build and insert the table headers
    const thead = document.createElement('thead');
    thead.setAttribute('class', 'thead-light');
    for (var key in column_names) {
        html_buffer = html_buffer.concat(`<th>${ column_names[key] }</th>`)
    }
    thead.innerHTML = html_buffer;
    document.querySelector('#data-preview').append(thead);

    // Build and insert the filter fields
    html_buffer = '';
    const tr = document.createElement('tr');
    tr.setAttribute('class', 'table-active');
    for (var key in sample_data[0]) {
        if (typeof sample_data[0][key] == 'number') {
            html_buffer = html_buffer.concat(`<td class="form-inline">
    <div class="row input-group">
        <div class="col-3">
            <select class="form-control form-control-sm">
                <option>></option>
                <option><</option>
                <option>=</option>
            </select>
        </div>
        <div class="col-9">
            <input class="form-control form-control-sm" type="text" placeholder="filter" style="max-width: 100%;">
        </div>
    </div>
</td>`);
        } else {
            html_buffer = html_buffer.concat('<td><input class="form-control form-control-sm" type="text" placeholder="filter"></td>');
        }
    }
    tr.innerHTML = html_buffer;
    document.querySelector('#data-preview').append(tr);

    // Build and insert the data
    for (var key in sample_data) {
        const data_tr = document.createElement('tr');
        html_buffer = '';

        for (var inner_key in sample_data[key]) {
            html_buffer = html_buffer.concat(`<td>${sample_data[key][inner_key]}</td>`)
        }

        data_tr.innerHTML = html_buffer;
        document.querySelector('#data-preview').append(data_tr);
    }
}
