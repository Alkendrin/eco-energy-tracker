// Disabling Loading Screen
//   document.getElementById("body").style.display = "none"; // Show the main body

//
//   // Wait for 3 seconds before showing the main body
//   setTimeout(() => {
//     document.getElementById("loading-screen").style.display = "none"; // Hide the loading screen
//     document.getElementById("body").style.display = ""; // Show the main body
//   }, 3000); // 3000 milliseconds = 3 seconds

window.addEventListener("DOMContentLoaded", function () {
    showNavbar();
    showAppliance();

    var sessionName = localStorage.getItem("sessionName");

    document.getElementById("stitle").innerHTML = sessionName;
    document.getElementById("simulation_title").innerHTML = sessionName;
    if (sessionName) {
        document.getElementById("delete").style.display = "block";
        showRoom();
    } else {
        document.getElementById("delete").style.display = "none";
    }

    const computeBtn = document.getElementById('compute');
    computeBtn.addEventListener('click', () => {
        stopAndCompute();
        addTableRowHighlighting(); // Add this line
    });
});

// show list of layout
async function showNavbar() {
    fetch("http://127.0.0.1:5000/api/navbar")
        .then((response) => response.json())
        .then((data) => getNavbar(data))
        .catch((error) =>
            console.error("Error fetching navbar list:", error)
        );
}

function getNavbar(response) {
    const a = document.getElementById("navBar");
    a.innerHTML = response.message;
}

// show appliance list
function showAppliance() {
    fetch("http://127.0.0.1:5000/api/appliance_list")
        .then((response) => response.json())
        .then((data) => outputApplianceList(data))
        .catch((error) =>
            console.error("Error fetching appliance list:", error)
        );
}

function outputApplianceList(response) {
    const a = document.getElementById("applianceList");
    a.innerHTML = response.message;
}

// select current layout
function setID(name, simulationId) {
    localStorage.setItem("sessionName", name);
    localStorage.setItem("sessionId", simulationId);

    // Update the dropdown button text
    const dropdownButton = document.querySelector('.house-selector .dropdown-toggle');
    if (dropdownButton) {
        dropdownButton.textContent = name;
    }

    document.getElementById("stitle").innerHTML = name;
    document.getElementById("simulation_title").innerHTML = name;

    // Toggle appliance list visibility
    const applianceList = document.querySelector('.appliance-list-container');
    if (name) {
        applianceList.classList.add('show');
    } else {
        applianceList.classList.remove('show');
    }

    // Show the form content when a layout is selected
    const formContent = document.getElementById('formContent');
    formContent.classList.add('show');

    // Show the summary section when a layout is selected
    const summarySection = document.querySelector('.summary-section');
    if (name) {
        summarySection.classList.add('open');
    } else {
        summarySection.classList.remove('open');
    }

    // Set layout background
    const layoutContainer = document.querySelector('.layout-container');
    if (simulationId == 93) {
        layoutContainer.style.background = 'url("assets/blueprint/Bungalow_1.jpg") no-repeat center center';
    } else if (simulationId == 94) {
        layoutContainer.style.background = 'url("assets/blueprint/Bungalow_2.jpg") no-repeat center center';
    } else if (simulationId == 95) {
        layoutContainer.style.background = 'url("assets/blueprint/Bungalow_3.jpg") no-repeat center center';
    } else if (simulationId == 96) {
        layoutContainer.style.background = 'url("assets/blueprint/Contemporary_1.jpg") no-repeat center center';
    } else if (simulationId == 99) {
        layoutContainer.style.background = 'url("assets/blueprint/Duplex_1.jpg") no-repeat center center';
    }
    layoutContainer.style.backgroundSize = 'contain';

    showHouse();
    showRoom();

    document.getElementById("delete").style.display = name ? "" : "none";
}

// perspective
function showHouse() {
    var housename = localStorage.getItem("sessionId");
    const container = document.getElementById("persepective");
    container.innerHTML = ""; // Clear previous content
    
    const img = document.createElement("img");
    if (housename == 93) {
        img.src = "assets/perspective/bungalow_1.png";
    } else if (housename == 94) {
        img.src = "assets/perspective/bungalow_2.png";
    } else if (housename == 95) {
        img.src = "assets/perspective/bungalow_3.png";
    } else if (housename == 96) {
        img.src = "assets/perspective/contemporary_1.jpg";
    } else if (housename == 99) {
        img.src = "assets/perspective/duplex_1.png";
    }



    img.classList.add('zoomable-image');
    
    // Create and append zoom modal
    const modal = document.createElement('div');
    modal.classList.add('zoom-modal');
    modal.style.display = 'none';
    
    const modalImg = document.createElement('img');
    modalImg.classList.add('modal-content');
    modal.appendChild(modalImg);
    
    // Add click handlers
    img.onclick = function() {
        modal.style.display = 'flex';
        modalImg.src = this.src;
    };

    modal.onclick = function() {
        modal.style.display = 'none';
    };

    container.appendChild(img);
    document.body.appendChild(modal);
}
// layout container
function showRoom() {
    var simulationId = localStorage.getItem("sessionId");
    return fetch(
        `http://127.0.0.1:5000/api/fetch_room?simulationId=${simulationId}`
    )
        .then((response) => response.json())
        .then((data) => {
            outputRoom(data);
            return data; // Return data for chaining
        })
        .catch((error) => {
            console.error("Error fetching room:", error);
            throw error; // Rethrow for error handling
        });
  }
  

function outputRoom(response) {
    var a = document.getElementById("roomContainer");
    a.innerHTML = response.message;
}

function canvasShowMessage(response) {
    // First make the server request and wait for it to complete
    showRoom()
      .then(() => {
        // Now wait a small amount of time to ensure DOM is updated
        return new Promise(resolve => setTimeout(resolve, 50));
      })
      .then(() => {
        // After DOM is fully updated, calculate consumption
        autoUpdateConsumptionAndShowPanel();
      })
      .catch(error => {
        console.error("Failed to update consumption:", error);
      });
  }
  

// Drag and drop functions
// Changed to handle browser but doesn't work on app
// Check commented code in "remove 2" commit
let draggedElement = null;
document.addEventListener("dragstart", function (event) {
    draggedElement = event.target;
    event.dataTransfer.setData("Text", event.target.id);
    event.dataTransfer.setData("custom_id", event.target.dataset.customId);
    event.dataTransfer.setData("is_update", event.target.dataset.isUpdate);
    event.dataTransfer.setData("canvas_id", event.target.dataset.canvasId);
});

// Handle drag enter event (change border of the drop target)
document.addEventListener("dragenter", function (event) {
    if (event.target.className == "droptarget") {
        event.target.style.border = "3px dotted red";
    }
});

// Allow drop event by preventing the default action
document.addEventListener("dragover", function (event) {
    event.preventDefault();
});

// Handle drag leave event (reset border of the drop target)
document.addEventListener("dragleave", function (event) {
    if (event.target.className == "droptarget") {
        event.target.style.border = "";
    }
});

// Handle drop event
document.addEventListener("drop", function (event) {
    event.preventDefault();

    const roomId = event.target.id;

    // Only proceed if the drop target has the class 'droptarget'
    if (event.target.className == "droptarget") {
        event.target.style.border = "";

        const imageId = event.dataTransfer.getData("Text");
        const fromRoom = event.dataTransfer.getData("custom_id");
        const isUpdate = event.dataTransfer.getData("is_update");
        const canvasId = event.dataTransfer.getData("canvas_id");

        var sessionName = localStorage.getItem("sessionName");
        var sessionId = localStorage.getItem("sessionId");

        // Create a clone of the dragged element if it's a new addition
        if (isUpdate !== "1") {
            // Clone the original element
            const clone = draggedElement.cloneNode(true);

            // Update the clone's attributes as needed
            clone.setAttribute('data-is-update', '1');

            // Append the clone instead of the original
            event.target.appendChild(clone);
        } else {
            // If updating position, move the original element
            event.target.appendChild(draggedElement);
        }

        if (roomId != "delete") {
            if (fromRoom !== roomId) {
                if (isUpdate == "1") {
                    updateCanvas(sessionId, roomId, imageId, fromRoom, canvasId);
                } else {
                    addToCanvas(sessionId, roomId, imageId);
                }
            }
        } else {
            removeFromCanvas(canvasId);
        }
    }
});

// canvas update functions
function updateCanvas(sessionId, roomId, imageId, fromRoom, canvasId) {
    fetch("http://127.0.0.1:5000/api/update_appliance_canvas", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            session_id: sessionId,
            room_id: roomId,
            image_id: imageId,
            from_room: fromRoom,
            canvas_id: canvasId,
        }),
    })
        .then((response) => response.json())
        .then((data) => {
            // First update the room display
            return showRoom().then(() => data);
        })
        .then((data) => {
            // Then wait for a complete DOM refresh cycle
            return new Promise(resolve => setTimeout(() => resolve(data), 200));
        })
        .then((data) => {
            // Finally update the consumption calculation
            autoUpdateConsumptionAndShowPanel();
        })
        .catch((error) => {
            console.error("Error updating appliance canvas:", error);
            Swal.fire({
                icon: "error",
                title: "Error",
                text: "Failed to update appliance position",
            });
        });
}

function addToCanvas(sessionId, roomId, imageId) {
    fetch("http://127.0.0.1:5000/api/add_appliance_canvas", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            sessionId: sessionId,
            roomId: roomId,
            imageId: imageId,
        }),
    })
        .then((response) => response.json())
        .then((data) => {
            // First update the room display
            return showRoom().then(() => data);
        })
        .then((data) => {
            // Then wait for a complete DOM refresh cycle
            return new Promise(resolve => setTimeout(() => resolve(data), 200));
        })
        .then((data) => {
            // Finally update the consumption calculation
            autoUpdateConsumptionAndShowPanel();
        })
        .catch((error) => {
            console.error("Error adding appliance to canvas:", error);
        });
}

function removeFromCanvas(canvasId) {
    fetch("http://127.0.0.1:5000/api/delete_appliance_canvas", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            canvas_id: canvasId,
        }),
    })
        .then((response) => response.json())
        .then((data) => canvasShowMessage(data))
        .catch((error) => {
            console.error("Error removing from canvas:", error);
            Swal.fire({
                icon: "error",
                title: "Error",
                text: "Failed to remove appliance",
            });
        });
}


// for appliance toggle
document.addEventListener("show.bs.modal", function (event) {
    // Get the triggering element
    const triggerElement = event.relatedTarget;

    // Retrieve the data-input-hr attribute
    const inputHrValue = triggerElement.getAttribute("data-input-hr");

    // Set the value of the input in the modal
    // const modalInput = document.getElementById('modalInput');
    // modalInput.value = inputHrValue;

    var input = document.getElementById("inputSaver");
    input.value = inputHrValue;
});

document
    .getElementById("appModal")
    .addEventListener("shown.bs.modal", initializeToggleSwitch);

function toggleInputValue() {
    var inputID = document.getElementById("inputSaver").value;
    var input = document.getElementById(inputID);
    var toggleSwitch = document.getElementById("toggleSwitch");

    // Toggle the value between "1" and "0"
    input.value = input.value === "1" ? "0" : "1";

    // Set the toggle switch checked state based on the input value
    toggleSwitch.checked = input.value === "1";
}

function initializeToggleSwitch() {
    var inputID = document.getElementById("inputSaver").value;
    var input = document.getElementById(inputID);
    var toggleSwitch = document.getElementById("toggleSwitch");

    // Set the toggle switch checked state based on the current input value
    toggleSwitch.checked = input.value === "1";
}

let running = false;
let myArray = [];
let intervalId;

// run button calculate
const computeBtn = document.getElementById("compute");
computeBtn.addEventListener("click", function () {
    var sessionId = localStorage.getItem("sessionId");
    if (!sessionId) {
        alert("select house first");
        return;
    }

    // Reset the variables for a new simulation
    myArray = [];
    running = true;

    var ratePerHour = document.getElementById("ratePerHour").value;
    var hours = document.getElementById("hours").value; // Get the user input for hours

    if (ratePerHour < 1) {
        alert("Please enter rate per kWh");
    } else if (hours <= 0) {
        alert("Please enter valid hours");
    } else {
        // document.getElementById("compute").style.display = 'none';
        // document.getElementById("stop").style.display = '';

        startSimulation(hours, ratePerHour); // Start the simulation using the input hours
    }
});

// Simulation function
// Simulation function
async function startSimulation(days, hours, ratePerHour) {
    let hoursTracker = {};

    // Get appliance inputs and accumulate usage over the total hours entered
    let applianceInputs = document.querySelectorAll(".toggleInput");
    applianceInputs.forEach((input) => {
        let inputValue = parseFloat(input.value) || 0;
        let inputId = input.id;

        if (hoursTracker[inputId]) {
            hoursTracker[inputId] += inputValue;
        } else {
            hoursTracker[inputId] = inputValue;
        }
    });

    // Calculate total hours from days and hours
    const totalHours = (days * 24) + hours;

    // After processing inputs, compute energy based on total hours
    computeEnergy(hoursTracker, ratePerHour, totalHours);

    stopAndCompute();
}
// Function to compute energy based on hours
function computeEnergy(hoursTracker, ratePerHour, totalHours) {
    myArray = {}; // Use an object to group by roomName

    Object.keys(hoursTracker).forEach((id) => {
        var parts = id.split("_");
        var canvas_id = parts[0];
        var watts = parseFloat(parts[1]);
        var applianceName = parts[2];
        var roomName = parts[3]; // Get the room name

        if (!isNaN(watts)) {
            var hours_used = hoursTracker[id] * totalHours; // Multiply by total hours to get the usage over the specified period
            var energy = (watts * hours_used) / 1000; // kWh
            var amount = ratePerHour * energy;

            // Check if the roomName group exists, if not, create it
            if (!myArray[roomName]) {
                myArray[roomName] = [];
            }

            // Push the result under the appropriate roomName group
            myArray[roomName].push({
                id: canvas_id,
                hours_used: hours_used,
                energy: energy,
                amount: amount,
                applianceName: applianceName,
                wattage: watts,
            });
        }
    });

    // Optionally, display the results (e.g., on the page or in the console)
    console.log(myArray);
}

// Update the table generation in stopAndCompute function
function stopAndCompute() {
    document.getElementById("results").style.display = "block";
    const resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = "";

    let totalEnergy = 0;
    let totalCost = 0;

    // Create table with enhanced styling
    let table = document.createElement("table");
    table.className = "table";
    table.innerHTML = `
        <thead>
            <tr>
                <th>Room</th>
                <th>Appliance</th>
                <th>Wattage</th>
                <th>Usage (h)</th>
                <th>kWh</th>
                <th>Cost</th>
            </tr>
        </thead>
        <tbody>
        </tbody>
    `;
    let tableBody = table.querySelector("tbody");

    // Add room data
    Object.keys(myArray).forEach((roomName) => {
        myArray[roomName].forEach((item) => {
            let row = document.createElement("tr");
            row.innerHTML = `
                <td><strong>${roomName}</strong></td>
                <td>${item.applianceName}</td>
                <td>${item.wattage} W</td>
                <td>${item.hours_used.toFixed(1)}</td>
                <td class="kwh-value">${item.energy.toFixed(2)}</td>
                <td class="cost-value">₱${item.amount.toFixed(2)}</td>
            `;
            tableBody.appendChild(row);

            totalEnergy += item.energy;
            totalCost += item.amount;
        });
    });

    // Add total row with enhanced styling
    let totalRow = document.createElement("tr");
    totalRow.className = "total-row";
    totalRow.innerHTML = `
        <td colspan="4"><strong>Total Consumption</strong></td>
        <td class="kwh-value"><strong>${totalEnergy.toFixed(2)} kWh</strong></td>
        <td class="cost-value"><strong>₱${totalCost.toFixed(2)}</strong></td>
    `;
    tableBody.appendChild(totalRow);

    // Add target and difference rows if values exist
    var targetKwh = document.getElementById("targetKwh").value;
    var targetBill = document.getElementById("targetBill").value;


    if (targetKwh || targetBill) {
        let targetRow = document.createElement("tr");
        targetRow.className = "target-row";
        targetRow.innerHTML = `
            <td colspan="4"><strong>Target</strong></td>
            <td class="kwh-value"><strong>${targetKwh ? targetKwh + " kWh" : "-"}</strong></td>
            <td class="cost-value"><strong>${targetBill ? "₱" + targetBill : "-"}</strong></td>
        `;
        tableBody.appendChild(targetRow);

        let differenceRow = document.createElement("tr");
        differenceRow.className = "difference-row";
        let kwhDiff = targetKwh ? (targetKwh - totalEnergy).toFixed(2) : "-";
        let billDiff = targetBill ? (targetBill - totalCost).toFixed(2) : "-";

        // Add color classes based on difference values
        const kwhColorClass = kwhDiff !== "-" ? (parseFloat(kwhDiff) >= 0 ? "text-success" : "text-danger") : "";
        const billColorClass = billDiff !== "-" ? (parseFloat(billDiff) >= 0 ? "text-success" : "text-danger") : "";

        differenceRow.innerHTML = `
            <td colspan="4"><strong>Difference</strong></td>
            <td class="kwh-value ${kwhColorClass}"><strong>${kwhDiff} ${kwhDiff !== "-" ? "kWh" : ""}</strong></td>
            <td class="cost-value ${billColorClass}"><strong>${billDiff !== "-" ? "₱" + billDiff : "-"}</strong></td>
        `;
        tableBody.appendChild(differenceRow);
    }

    resultsDiv.appendChild(table);
}

// calculate kwh target
function calculateSuggestionsEnergy() {
    var sessionId = localStorage.getItem("sessionId");
    if (!sessionId) {
        alert("Pelect house first");
        return;
    }

    if (document.getElementById("hours").value < 1) {
        alert("Please input hours that is greater than 0.");
        return;
    }

    const target_kwh = document.getElementById("targetKWH").value;
    var ratePerHour = document.getElementById("ratePerHour").value;

    document.getElementById("suggestions").innerHTML = "";

    if (target_kwh && ratePerHour) {
        fetch("http://127.0.0.1:5000/api/get_suggestions_energy", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                target_kwh: target_kwh,
                rate_per_hour: ratePerHour,
                session_id: sessionId,
            }),
        })
            .then((response) => response.json())
            .then((data) => getSuggestionEnergy(data))
            .catch((error) => {
                console.error("Error calculating suggestions:", error);
                alert("Error calculating suggestions. Please try again.");
            });
    } else {
        alert("Please enter valid kWh and rate per hour.");
    }
}

function getSuggestionEnergy(response) {
    const suggestionsDiv = document.getElementById("suggestions");
}

// calculate bill target
function calculateSuggestions() {
    var sessionId = localStorage.getItem("sessionId");
    if (!sessionId) {
        alert("select house first");
        return;
    }

    const targetAmount = document.getElementById("targetAmount").value;
    const targetHours = document.getElementById("targetHours").value;
    var ratePerHour = document.getElementById("ratePerHour").value;
    document.getElementById("suggestions").innerHTML = "";

    if (targetAmount && targetHours && ratePerHour) {
        fetch("http://127.0.0.1:5000/api/get_suggestions", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                target_amount: parseFloat(targetAmount),
                target_hours: targetHours,
                rate_per_hour: ratePerHour,
                session_id: sessionId,
            }),
        })
            .then((response) => response.json())
            .then((data) => getSuggestion(data))
            .catch((error) => {
                console.error("Error calculating suggestions:", error);
                alert("Error calculating suggestions. Please try again.");
            });

        // Display suggestions
    } else {
        alert("Please enter valid target amount, rate Per Hour, and hours.");
    }
}

function getSuggestion(response) {
    const suggestionsDiv = document.getElementById("suggestions");
    suggestions.innerHTML = response.message;
}

// dragging
document.addEventListener('DOMContentLoaded', function () {
    const container = document.querySelector('.layout-container');
    let isDragging = false;
    let currentX;
    let currentY;
    let initialX;
    let initialY;
    let xOffset = 0;
    let yOffset = 0;

    // Add mousedown event to the container itself
    container.addEventListener('mousedown', dragStart);
    document.addEventListener('mousemove', drag);
    document.addEventListener('mouseup', dragEnd);

    function dragStart(e) {
        // Don't start dragging if we're interacting with an appliance
        if (e.target.closest('.appliance-item') || e.target.closest('.droptarget')) {
            return;
        }

        // Only allow dragging when clicking directly on the container or its background
        if (!container.contains(e.target)) {
            return;
        }

        isDragging = true;
        initialX = e.clientX - xOffset;
        initialY = e.clientY - yOffset;
        e.preventDefault();
    }

    function drag(e) {
        if (isDragging) {
            e.preventDefault();
            currentX = e.clientX - initialX;
            currentY = e.clientY - initialY;
            xOffset = currentX;
            yOffset = currentY;
            setTranslate(currentX, currentY, container);
        }
    }

    function dragEnd() {
        isDragging = false;
    }

    function setTranslate(xPos, yPos, el) {
        el.style.transform = `translate(${xPos}px, ${yPos}px)`;
    }
});

function onHouseSelect(houseId) {
    // ...existing house selection code...
    
    // Show the form content
    const formContent = document.getElementById('formContent');
    formContent.classList.add('show');
  }
  
  // Add this to hide form when house is deselected
  function onHouseDeselect() {
    const formContent = document.getElementById('formContent');
    formContent.classList.remove('show');
  }

  // Add toggle functionality
document.addEventListener('DOMContentLoaded', function() {
    const summarySection = document.querySelector('.summary-section');
    const summaryToggle = document.getElementById('summaryToggle');

    // Toggle summary panel
    function toggleSummary() {
        summarySection.classList.toggle('open');
        summaryToggle.classList.toggle('open');
    }

    summaryToggle.addEventListener('click', toggleSummary);

    // Modify the existing compute button click handler
    const computeBtn = document.getElementById("compute");
    // computeBtn.addEventListener("click", function() {
    //     var sessionId = localStorage.getItem("sessionId");
    //     if (!sessionId) {
    //         alert("select house first");
    //         return;
    //     }

    //     // Reset the variables for a new simulation
    //     myArray = [];
    //     running = true;

    //     var ratePerHour = document.getElementById("ratePerHour").value;
    //     var hours = document.getElementById("hours").value;

    //     if (ratePerHour < 1) {
    //         alert("Please enter rate per kWh");
    //     } else if (hours <= 0) {
    //         alert("Please enter valid hours");
    //     } else {
    //         // Open the summary panel when calculating
    //         if (!summarySection.classList.contains('open')) {
    //             toggleSummary();
    //         }
    //         startSimulation(hours, ratePerHour);
    //     }
    // });
});

function highlightRoom(roomName, shouldHighlight) {
    // Find all rooms and droptargets
    const rooms = document.querySelectorAll('.room');
    
    // Iterate through rooms to find matching one
    rooms.forEach(room => {
        const droptarget = room.querySelector('.droptarget');
        if (droptarget && droptarget.id.includes(roomName)) {
            room.classList.toggle('highlight', shouldHighlight);
            droptarget.classList.toggle('highlight', shouldHighlight);
        }
    });
}

function addTableRowHighlighting() {
    const tableRows = document.querySelectorAll('.result-container tbody tr:not(.total-row):not(.target-row):not(.difference-row)');
    
    tableRows.forEach(row => {
        row.addEventListener('mouseenter', (e) => {
            const roomName = row.querySelector('td:first-child').textContent;
            highlightRoom(roomName.trim(), true);
        });
        
        row.addEventListener('mouseleave', (e) => {
            const roomName = row.querySelector('td:first-child').textContent;
            highlightRoom(roomName.trim(), false);
        });
    });
}

function autoUpdateConsumption() {
    // Get current values
    const days = parseInt(document.getElementById("days").value) || 0;
    const hours = parseInt(document.getElementById("hours").value) || 0;
    const ratePerHour = document.getElementById("ratePerHour").value || 0;
    
    // Only auto-calculate if we have some valid values
    if ((days > 0 || hours > 0) && ratePerHour > 0) {
      // Reset array and run calculation
      myArray = [];
      startSimulation(days, hours, ratePerHour);
      
      // Add highlighting to rows
      addTableRowHighlighting();
      
      // Flash effect on update
      const summaryContent = document.querySelector(".summary-content");
      summaryContent.classList.add("updated");
      setTimeout(() => summaryContent.classList.remove("updated"), 500);
    }
}
  
  // Make sure the summary panel is visible when calculation happens
  function autoUpdateConsumptionAndShowPanel() {
    const days = parseInt(document.getElementById("days").value) || 0;
    const hours = parseInt(document.getElementById("hours").value) || 0;
    const ratePerHour = document.getElementById("ratePerHour").value || 0;
    
    if ((days > 0 || hours > 0) && ratePerHour > 0) {
        // Open the summary panel if not already open
        const summarySection = document.querySelector('.summary-section');
        if (!summarySection.classList.contains('open')) {
            toggleSummary();
        }
        
        // Run the calculation
        myArray = [];
        startSimulation(days, hours, ratePerHour);
        
        // Add highlighting
        addTableRowHighlighting();
    }
}
  
  // Replace canvasShowMessage with this improved version
  function canvasShowMessage(response) {
    showRoom();
    autoUpdateConsumptionAndShowPanel();
  }
  
  // Add event listeners to automatically update calculations when input values change
  document.addEventListener('DOMContentLoaded', function() {
    const daysInput = document.getElementById("days");
    const hoursInput = document.getElementById("hours");
    const rateInput = document.getElementById("ratePerHour");
    
    // Auto-update when days, hours, or rate changes
    daysInput.addEventListener('input', autoUpdateConsumption);
    hoursInput.addEventListener('input', autoUpdateConsumption);
    rateInput.addEventListener('input', autoUpdateConsumption);
    
    // Check if we should calculate on page load
    if (localStorage.getItem("sessionId") && 
        ((daysInput.value > 0 || hoursInput.value > 0) && 
        rateInput.value > 0)) {
      setTimeout(autoUpdateConsumption, 500); // Short delay to ensure DOM is ready
    }
});