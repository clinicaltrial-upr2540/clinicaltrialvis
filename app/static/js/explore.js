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
                buildSidebarViewEntry(JSON.parse(this.responseText));
            } catch(err) {
                console.log(err.message + " in " + this.responseText);
                return;
            }
        }
    };
    viewRequest.open("GET", "/data/tables", true);
    viewRequest.send();
}

// Function to add a single view to the sidebar
function buildSidebarViewEntry(viewList) {
    for (var key in viewList) {
        const tr = document.createElement('tr');

        tr.innerHTML = `<td data-toggle="collapse" data-target="#${viewList[key]}fields" class="accordion-toggle">${viewList[key]} <small class="text-muted">click to expand</small></td>
<td>
    <label class="custom-toggle">
        <input type="checkbox" checked data-toggle="toggle" id="${viewList[key]}checkbox" name="${viewList[key]}">
        <span class="custom-toggle-slider rounded-circle" data-label-off="No" data-label-on="Yes"></span>
    </label>
</td>`;

        document.querySelector('#selection-sidebar').append(tr);
    }
}
