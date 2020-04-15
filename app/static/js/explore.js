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
    // Filter listeners go here
    // Update Preview button functionality goes here
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
        <span class="custom-toggle-slider rounded-circle" data-label-off="No" data-label-on="Yes"></span>
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




