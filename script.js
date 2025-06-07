// Disabling Loading Screen
//   document.getElementById("body").style.display = "none"; // Show the main body

//
//   // Wait for 3 seconds before showing the main body
//   setTimeout(() => {
//     document.getElementById("loading-screen").style.display = "none"; // Hide the loading screen
//     document.getElementById("body").style.display = ""; // Show the main body
//   }, 3000); // 3000 milliseconds = 3 seconds

let totalHoursSuggested = 0;

window.addEventListener("DOMContentLoaded", function () {
    localStorage.clear();
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

document.getElementById('start-btn').addEventListener('click', function() {
    document.getElementById('splash-screen').classList.add('hidden');
    // After animation completes, remove from DOM
    setTimeout(() => {
        document.getElementById('splash-screen').style.display = 'none';
    }, 500);
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
        layoutContainer.style.background = 'url("assets/blueprint/Bungalow_2.png") no-repeat center center';
    } else if (simulationId == 95) {
        layoutContainer.style.background = 'url("assets/blueprint/Bungalow_3.png") no-repeat center center';
    } else if (simulationId == 96) {
        layoutContainer.style.background = 'url("assets/blueprint/Contemporary_1.jpg") no-repeat center center';
    } else if (simulationId == 97) {
        layoutContainer.style.background = 'url("assets/blueprint/Contemporary_2.png") no-repeat center center';
    } else if (simulationId == 99) {
        layoutContainer.style.background = 'url("assets/blueprint/Duplex_1.png") no-repeat center center';
    } else if (simulationId == 100) {
        layoutContainer.style.background = 'url("assets/blueprint/Duplex_2.jpg") no-repeat center center';
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
    } else if (housename == 97) {
        img.src = "assets/perspective/contemporary_2.png";
    } else if (housename == 99) {
        img.src = "assets/perspective/duplex_1.png";
    } else if (housename == 100) {
        img.src = "assets/perspective/duplex_2.png";
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

        if (roomId === "delete") {
            removeFromCanvas(canvasId);
            // Update consumption after deleting appliance
            setTimeout(() => {
                autoUpdateConsumptionAndShowPanel();
            }, 300); // Small delay to ensure canvas is updated
            return;
        }

        if (isRestrictedCombination(roomId, imageId)) {
            // Flash the container red
            flashContainerRed(event.target);
            // Show error message
            Swal.fire({
                icon: "error",
                title: "Restricted",
                text: "This appliance cannot be placed in this room for safety purposes.",
            });
            return;
        }

        // Rest of your existing drop handling code...
        if (isUpdate !== "1") {
            const clone = draggedElement.cloneNode(true);
            clone.setAttribute('data-is-update', '1');
            event.target.appendChild(clone);
        } else {
            event.target.appendChild(draggedElement);
        }

        if (fromRoom !== roomId) {
            if (isUpdate == "1") {
                updateCanvas(sessionId, roomId, imageId, fromRoom, canvasId);
            } else {
                addToCanvas(sessionId, roomId, imageId);
            }
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
    let roomSubtotals = {};

    // First pass: calculate total energy and room subtotals
    Object.keys(myArray).forEach((roomName) => {
        roomSubtotals[roomName] = { energy: 0, cost: 0 };
        
        myArray[roomName].forEach((item) => {
            totalEnergy += item.energy;
            totalCost += item.amount;
            roomSubtotals[roomName].energy += item.energy;
            roomSubtotals[roomName].cost += item.amount;
        });
    });

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

    // Add room data with subtotals
    Object.keys(myArray).forEach((roomName) => {
        let firstRow = true;
        
        myArray[roomName].forEach((item) => {
            let row = document.createElement("tr");
            row.innerHTML = `
                <td>${firstRow ? `<strong>${roomName}</strong>` : ""}</td>
                <td>${item.applianceName}</td>
                <td>${item.wattage} W</td>
                <td>${item.hours_used.toFixed(1)}</td>
                <td class="kwh-value">${item.energy.toFixed(2)}</td>
                <td class="cost-value">₱${item.amount.toFixed(2)}</td>
            `;
            tableBody.appendChild(row);
            firstRow = false;
        });
        
        // Add subtotal for each room
        const roomEnergy = roomSubtotals[roomName].energy;
        const roomCost = roomSubtotals[roomName].cost;
        const percentage = (roomEnergy / totalEnergy * 100).toFixed(1);
        
        let subtotalRow = document.createElement("tr");
        subtotalRow.className = "subtotal-row";
        subtotalRow.innerHTML = `
            <td colspan="4"><em>Subtotal for ${roomName}</em></td>
            <td class="kwh-value"><em>${roomEnergy.toFixed(2)} kWh (${percentage}%)</em></td>
            <td class="cost-value"><em>₱${roomCost.toFixed(2)}</em></td>
        `;
        tableBody.appendChild(subtotalRow);
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
    
    // Add some CSS for the subtotal row
    const style = document.createElement('style');
    style.textContent = `
        .subtotal-row {
            background-color: #f8f9fa;
            border-bottom: 1px solid #dee2e6;
        }
        .subtotal-row td {
            padding-top: 8px;
            padding-bottom: 8px;
        }
    `;
    document.head.appendChild(style);
}

function calculateSuggestionsEnergy() {
    var sessionId = localStorage.getItem('sessionId');
    if (!sessionId) {
        Swal.fire({
            icon: 'warning',
            title: 'Select House First',
            text: 'Please select a house layout before calculating suggestions.'
        });
        return;
    }

    const targetKwh = document.getElementById('targetKwh').value;
    const hours = document.getElementById('hours').value;
    const ratePerHour = document.getElementById('ratePerHour').value;

    if (targetKwh && hours && ratePerHour) {
        // Show loading indicator
        document.getElementById('results').innerHTML = '<div class="text-center"><div class="spinner-border" role="status"><span class="visually-hidden">Loading...</span></div><p>Calculating suggestions...</p></div>';
        
        // Send data to Python backend
        fetch("http://127.0.0.1:5000/api/get_suggestions_energy", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                target_kwh: parseFloat(targetKwh),
                target_hours: hours,
                rate_per_hour: ratePerHour,
                session_id: sessionId,
            }),
        })
        .then(response => response.json())
        .then(data => {
            processAndDisplaySuggestionsEnergy(data, targetKwh);
        })
        .catch(error => {
            console.error("Error getting energy suggestions:", error);
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'Failed to get energy suggestions. Please try again.'
            });
        });
    } else {
        Swal.fire({
            icon: 'warning',
            title: 'Missing Information',
            text: 'Please enter valid target kWh, rate per hour, and hours.'
        });
    }
}

function processAndDisplaySuggestionsEnergy(response, targetKwh) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = ""; // Clear previous results
    
    if (response && response.message) {
        // Parse the HTML response
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = response.message;
        
        // Extract room data from the response
        const roomSections = tempDiv.querySelectorAll('.room-section');
        const totalBillElement = tempDiv.querySelector('.total-bill p');
        
        // Create the table structure matching the results format
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
        
        // Track totals
        let totalEnergy = 0;
        let totalCost = 0;
        let roomSubtotals = {};
        totalHoursSuggested = 0;
        
        // Process each room's data
        roomSections.forEach(roomSection => {
            const roomName = roomSection.querySelector('p.text-primary').textContent;
            const appliances = roomSection.querySelectorAll('.appliance');
            const roomTotalElement = roomSection.querySelector('.room-total-bill p');
            
            roomSubtotals[roomName] = { energy: 0, cost: 0 };
            
            // Extract room total cost
            if (roomTotalElement) {
                const match = roomTotalElement.textContent.match(/[\d.]+/);
                if (match) roomSubtotals[roomName].cost = parseFloat(match[0]);
            }
            
            let firstRow = true;
            
            
            // Add each appliance as a row
            appliances.forEach(appliance => {
                // Extract data from the appliance element
                const spans = appliance.querySelectorAll('span');
                const applianceName = spans[0].textContent.replace('Appliance: ', '');
                const suggestedHours = parseFloat(spans[1].textContent.match(/[\d.]+/)[0]);
                const applianceBill = parseFloat(spans[2].textContent.match(/[\d.]+/)[0]);
                
                // Calculate wattage and kWh based on bill and hours
                const ratePerHour = parseFloat(document.getElementById('ratePerHour').value);
                const applianceEnergy = applianceBill / ratePerHour;
                const wattage = suggestedHours > 0 ? (applianceEnergy * 1000 / suggestedHours) : 0;
                
                roomSubtotals[roomName].energy += applianceEnergy;
                
                // Create table row
                let row = document.createElement("tr");
                row.innerHTML = `
                    <td>${firstRow ? `<strong>${roomName}</strong>` : ""}</td>
                    <td>${applianceName}</td>
                    <td>${Math.round(wattage)} W</td>
                    <td>${suggestedHours.toFixed(1)}</td>
                    <td class="kwh-value">${applianceEnergy.toFixed(2)}</td>
                    <td class="cost-value">₱${applianceBill.toFixed(2)}</td>
                `;
                tableBody.appendChild(row);
                firstRow = false;
                totalHoursSuggested += parseFloat(suggestedHours);
            });
            
            totalEnergy += roomSubtotals[roomName].energy;
            totalCost += roomSubtotals[roomName].cost;
            
            // Add subtotal for each room
            const roomEnergy = roomSubtotals[roomName].energy;
            const roomCost = roomSubtotals[roomName].cost;
            const percentage = totalEnergy > 0 ? (roomEnergy / totalEnergy * 100).toFixed(1) : '0.0';
            
            let subtotalRow = document.createElement("tr");
            subtotalRow.className = "subtotal-row";
            subtotalRow.innerHTML = `
                <td colspan="4"><em>Subtotal for ${roomName}</em></td>
                <td class="kwh-value"><em>${roomEnergy.toFixed(2)} kWh (${percentage}%)</em></td>
                <td class="cost-value"><em>₱${roomCost.toFixed(2)}</em></td>
            `;
            tableBody.appendChild(subtotalRow);
        });
        
        // Extract total bill from response
        if (totalBillElement) {
            const match = totalBillElement.textContent.match(/[\d.]+/);
            if (match) totalCost = parseFloat(match[0]);
        }
        
        // Add total row with enhanced styling
        let totalRow = document.createElement("tr");
        totalRow.className = "total-row";
        totalRow.innerHTML = `
            <td colspan="3"><strong>Total Suggested Consumption</strong></td>
            <td class="kwh-value"><strong>${totalHoursSuggested.toFixed(1)}</strong></td>
            <td class="kwh-value"><strong>${totalEnergy.toFixed(2)} kWh</strong></td>
            <td class="cost-value"><strong>₱${totalCost.toFixed(2)}</strong></td>
        `;
        tableBody.appendChild(totalRow);
        const billDiff = null;
        const billColorClass = null;
        

        if (targetKwh) {
            const targetBill = document.getElementById('targetBill').value;
            let targetRow = document.createElement("tr");
            targetRow.className = "target-row";
            targetRow.innerHTML = `
                <td colspan="4"><strong>Target</strong></td>
                <td class="kwh-value"><strong>${parseFloat(targetKwh).toFixed(2)} kWh</strong></td>
                <td class="cost-value"><strong>${targetBill ? "₱" + parseFloat(targetBill).toFixed(2) : ""}</strong></td>
            `;
            tableBody.appendChild(targetRow);
            
            // Add difference row
            const kwhDiff = parseFloat(targetKwh) - totalEnergy;
            const kwhColorClass = kwhDiff >= 0 ? "text-success" : "text-danger";
            
            let billDiff, billColorClass;
            if (targetBill) {
                billDiff = parseFloat(targetBill) - totalCost;
                billColorClass = billDiff >= 0 ? "text-success" : "text-danger";
            }
            
            let diffRow = document.createElement("tr");
            diffRow.className = "difference-row";
            diffRow.innerHTML = `
                <td colspan="4"><strong>Difference</strong></td>
                <td class="kwh-value ${kwhColorClass}"><strong>${kwhDiff.toFixed(2)} kWh</strong></td>
                <td class="cost-value ${billColorClass || ""}"><strong>${targetBill ? "₱" + billDiff.toFixed(2) : ""}</strong></td>
            `;
            tableBody.appendChild(diffRow);
        }
        
        
        resultsDiv.appendChild(table);
        
        // Add row highlighting behavior
        setTimeout(addTableRowHighlighting, 100);
    } else {
        resultsDiv.innerHTML = '<div class="alert alert-warning">No energy suggestions available.</div>';
    }
}

// calculate kwh target
// function calculateSuggestionsEnergy() {
//     var sessionId = localStorage.getItem("sessionId");
//     if (!sessionId) {
//         alert("Pelect house first");
//         return;
//     }

//     if (document.getElementById("hours").value < 1) {
//         alert("Please input hours that is greater than 0.");
//         return;
//     }

//     const target_kwh = document.getElementById("targetKWH").value;
//     var ratePerHour = document.getElementById("ratePerHour").value;

//     document.getElementById("suggestions").innerHTML = "";

//     if (target_kwh && ratePerHour) {
//         fetch("http://127.0.0.1:5000/api/get_suggestions_energy", {
//             method: "POST",
//             headers: {
//                 "Content-Type": "application/json",
//             },
//             body: JSON.stringify({
//                 target_kwh: target_kwh,
//                 rate_per_hour: ratePerHour,
//                 session_id: sessionId,
//             }),
//         })
//             .then((response) => response.json())
//             .then((data) => getSuggestionEnergy(data))
//             .catch((error) => {
//                 console.error("Error calculating suggestions:", error);
//                 alert("Error calculating suggestions. Please try again.");
//             });
//     } else {
//         alert("Please enter valid kWh and rate per hour.");
//     }
// }

// function getSuggestionEnergy(response) {
//     const suggestionsDiv = document.getElementById("suggestions");
// }

// calculate bill target
// function calculateSuggestions() {
//     alert("calculate suggestions");
//     var sessionId = localStorage.getItem('sessionId');
//     if (!sessionId) {
//         Swal.fire({
//             icon: 'warning',
//             title: 'Select House First',
//             text: 'Please select a house layout before calculating suggestions.'
//         });
//         return;
//     }

//     const targetAmount = document.getElementById("targetAmount").value;
//     const targetHours = document.getElementById("targetHours").value;
//     var ratePerHour = document.getElementById("ratePerHour").value;
//     document.getElementById("suggestions").innerHTML = "";

//     if (targetAmount && targetHours && ratePerHour) {
//         fetch("http://127.0.0.1:5000/api/get_suggestions", {
//             method: "POST",
//             headers: {
//                 "Content-Type": "application/json",
//             },
//             body: JSON.stringify({
//                 target_amount: parseFloat(targetAmount),
//                 target_hours: targetHours,
//                 rate_per_hour: ratePerHour,
//                 session_id: sessionId,
//             }),
//         })
//             .then((response) => response.json())
//             .then((data) => getSuggestion(data))
//             .catch((error) => {
//                 console.error("Error calculating suggestions:", error);
//                 alert("Error calculating suggestions. Please try again.");
//             });

//         // Display suggestions
//     } else {
//         alert("Please enter valid target amount, rate Per Hour, and hours.");
//     }
// }

function calculateSuggestions() {
    var sessionId = localStorage.getItem('sessionId');
    if (!sessionId) {
        Swal.fire({
            icon: 'warning',
            title: 'Select House First',
            text: 'Please select a house layout before calculating suggestions.'
        });
        return;
    }

    const targetAmount = document.getElementById('targetBill').value;
    const hours = document.getElementById('hours').value;
    const ratePerHour = document.getElementById('ratePerHour').value;

    if (targetAmount && hours && ratePerHour) {
        // Show loading indicator
        document.getElementById('results').innerHTML = '<div class="text-center"><div class="spinner-border" role="status"><span class="visually-hidden">Loading...</span></div><p>Calculating suggestions...</p></div>';
        
        // Send data to Python backend
        fetch("http://127.0.0.1:5000/api/get_suggestions", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                target_amount: parseFloat(targetAmount),
                target_hours: hours,
                rate_per_hour: ratePerHour,
                session_id: sessionId,
            }),
        })
        .then(response => response.json())
        .then(data => {
            processAndDisplaySuggestions(data, targetAmount);
        })
        .catch(error => {
            console.error("Error getting suggestions:", error);
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'Failed to get suggestions. Please try again.'
            });
        });
    } else {
        Swal.fire({
            icon: 'warning',
            title: 'Missing Information',
            text: 'Please enter valid target amount, rate per hour, and hours.'
        });
    }
}

function processAndDisplaySuggestions(response, targetAmount) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = ""; // Clear previous results
    
    if (response && response.message) {
        // Parse the HTML response
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = response.message;
        
        // Extract room data from the response
        const roomSections = tempDiv.querySelectorAll('.room-section');
        // const totalEnergyElement = tempDiv.querySelector('.total-energy p');
        const totalBillElement = tempDiv.querySelector('.total-bill p');
        
        // Create the table structure matching the results format
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
        
        // Track totals
        totalEnergy = 0;
        totalCost = 0;
        let roomSubtotals = {};
        totalHoursSuggested = 0; 
        
        // Process each room's data
        roomSections.forEach(roomSection => {
            const roomName = roomSection.querySelector('p.text-primary').textContent;
            const appliances = roomSection.querySelectorAll('.appliance');
            const roomTotalElement = roomSection.querySelector('.room-total-bill p');
            
            roomSubtotals[roomName] = { energy: 0, cost: 0 };
            
            // Extract room total cost
            if (roomTotalElement) {
                const match = roomTotalElement.textContent.match(/[\d.]+/);
                if (match) roomSubtotals[roomName].cost = parseFloat(match[0]);
            }
            
            let firstRow = true;

    
            
            // Add each appliance as a row
            appliances.forEach(appliance => {
                // Extract data from the appliance element
                const spans = appliance.querySelectorAll('span');
                const applianceName = spans[0].textContent.replace('Appliance: ', '');
                const suggestedHours = parseFloat(spans[1].textContent.match(/[\d.]+/)[0]);
                const applianceBill = parseFloat(spans[2].textContent.match(/[\d.]+/)[0]);
                
                // Calculate wattage and kWh based on bill and hours
                const ratePerHour = parseFloat(document.getElementById('ratePerHour').value);
                const applianceEnergy = applianceBill / ratePerHour;
                const wattage = suggestedHours > 0 ? (applianceEnergy * 1000 / suggestedHours) : 0;
                
                roomSubtotals[roomName].energy += applianceEnergy;
                
                // Create table row
                let row = document.createElement("tr");
                row.innerHTML = `
                    <td>${firstRow ? `<strong>${roomName}</strong>` : ""}</td>
                    <td>${applianceName}</td>
                    <td>${Math.round(wattage)} W</td>
                    <td>${suggestedHours.toFixed(1)}</td>
                    <td class="kwh-value">${applianceEnergy.toFixed(2)}</td>
                    <td class="cost-value">₱${applianceBill.toFixed(2)}</td>
                `;
                tableBody.appendChild(row);
                firstRow = false;

                totalHoursSuggested = suggestedHours.toFixed(1);
            });
            
            totalEnergy += roomSubtotals[roomName].energy;
            totalCost += roomSubtotals[roomName].cost;
            
            // Add subtotal for each room
            const roomEnergy = roomSubtotals[roomName].energy;
            const roomCost = roomSubtotals[roomName].cost;
            const percentage = totalEnergy > 0 ? (roomEnergy / totalEnergy * 100).toFixed(1) : '0.0';
            
            let subtotalRow = document.createElement("tr");
            subtotalRow.className = "subtotal-row";
            subtotalRow.innerHTML = `
                <td colspan="4"><em>Subtotal for ${roomName}</em></td>
                <td class="kwh-value"><em>${roomEnergy.toFixed(2)} kWh (${percentage}%)</em></td>
                <td class="cost-value"><em>₱${roomCost.toFixed(2)}</em></td>
            `;
            tableBody.appendChild(subtotalRow);
        });
        
        // Extract total bill from response
        const totalEnergyElement = tempDiv.querySelector('.total-energy p');
        if (totalEnergyElement) {
            const energyMatch = totalEnergyElement.textContent.match(/[\d.]+/);
            if (energyMatch) totalEnergy = parseFloat(energyMatch[0]);
        }
        
        if (totalBillElement) {
            const costMatch = totalBillElement.textContent.match(/[\d.]+/);
            if (costMatch) totalCost = parseFloat(costMatch[0]);
        }
        
        
        // Add total row with enhanced styling
        let totalRow = document.createElement("tr");
        totalRow.className = "total-row";
        totalRow.innerHTML = `
            <td colspan="3"><strong>Total Suggested Consumption</strong></td>
            <td class="hr-value"><strong>${totalHoursSuggested}</strong></td>
            <td class="kwh-value"><strong>${totalEnergy.toFixed(2)} kWh</strong></td>
            <td class="cost-value"><strong>₱${totalCost.toFixed(2)}</strong></td>
        `;
        tableBody.appendChild(totalRow);
        
        // Add target row
        if (targetAmount) {
            const targetKwh = document.getElementById('targetKwh').value;
            let targetRow = document.createElement("tr");
            targetRow.className = "target-row";
            targetRow.innerHTML = `
                <td colspan="4"><strong>Target</strong></td>
                <td class="kwh-value"><strong>${targetKwh} kWh<strong></td>
                <td class="cost-value"><strong>₱${parseFloat(targetAmount).toFixed(2)}</strong></td>
            `;
            tableBody.appendChild(targetRow);
            
            // Add difference row
            const diff = parseFloat(targetAmount) - totalCost;
            const colorClass = diff >= 0 ? "text-success" : "text-danger";

            if (targetKwh) {
                kwhDiff = parseFloat(targetKwh) - totalEnergy;
                kwhColorClass = kwhDiff >= 0 ? "text-success" : "text-danger";
            }
            
            let diffRow = document.createElement("tr");
            diffRow.className = "difference-row";
            diffRow.innerHTML = `
                <td colspan="4"><strong>Difference</strong></td>
                <td class="kwh-value ${kwhColorClass}"><strong>${targetKwh ? kwhDiff.toFixed(2) + " kWh" : ""}</strong></td>
                <td class="cost-value ${colorClass}"><strong>₱${diff.toFixed(2)}</strong></td>
            `;
            tableBody.appendChild(diffRow);
        }
        
        resultsDiv.appendChild(table);
        
        // Add row highlighting behavior
        setTimeout(addTableRowHighlighting, 100);
    } else {
        resultsDiv.innerHTML = '<div class="alert alert-warning">No suggestions available.</div>';
    }
}

function getSuggestion(response) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = ""; // Clear previous results
    
    if (response && response.message) {
        // Parse the HTML response
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = response.message;
        
        // Extract room data from the response
        const roomSections = tempDiv.querySelectorAll('.room-section');
        const totalBillElement = tempDiv.querySelector('.total-bill p');
        
        // Create the table structure matching the results format
        let table = document.createElement("table");
        table.className = "table";
        table.innerHTML = `
            <thead>
                <tr>
                    <th>Room</th>
                    <th>Appliance</th>
                    <th>Suggested Hours</th>
                    <th>Wattage</th>
                    <th>kWh</th>
                    <th>Cost</th>
                </tr>
            </thead>
            <tbody>
            </tbody>
        `;
        let tableBody = table.querySelector("tbody");
        
        // Track totals
        let totalEnergy = 0;
        let totalCost = 0;
        let roomSubtotals = {};
        
        // Process each room's data
        roomSections.forEach(roomSection => {
            const roomName = roomSection.querySelector('p.text-primary').textContent;
            const appliances = roomSection.querySelectorAll('.appliance');
            const roomTotalElement = roomSection.querySelector('.room-total-bill p');
            
            roomSubtotals[roomName] = { energy: 0, cost: 0 };
            
            // Extract room total cost
            if (roomTotalElement) {
                const match = roomTotalElement.textContent.match(/[\d.]+/);
                if (match) roomSubtotals[roomName].cost = parseFloat(match[0]);
            }
            
            let firstRow = true;
            
            // Add each appliance as a row
            appliances.forEach(appliance => {
                // Extract data from the appliance element
                const spans = appliance.querySelectorAll('span');
                const applianceName = spans[0].textContent.replace('Appliance: ', '');
                const suggestedHours = parseFloat(spans[1].textContent.match(/[\d.]+/)[0]);
                const applianceBill = parseFloat(spans[2].textContent.match(/[\d.]+/)[0]);
                
                // Calculate wattage and kWh based on bill and hours
                const ratePerHour = parseFloat(document.getElementById('ratePerHour').value);
                const applianceEnergy = applianceBill / ratePerHour;
                const wattage = suggestedHours > 0 ? (applianceEnergy * 1000 / suggestedHours) : 0;
                
                roomSubtotals[roomName].energy += applianceEnergy;
                
                // Create table row
                let row = document.createElement("tr");
                row.innerHTML = `
                    <td>${firstRow ? `<strong>${roomName}</strong>` : ""}</td>
                    <td>${applianceName}</td>
                    <td>${suggestedHours.toFixed(1)}</td>
                    <td>${Math.round(wattage)} W</td>
                    <td class="kwh-value">${applianceEnergy.toFixed(2)}</td>
                    <td class="cost-value">₱${applianceBill.toFixed(2)}</td>
                `;
                tableBody.appendChild(row);
                firstRow = false;
            });
            
            totalEnergy += roomSubtotals[roomName].energy;
            totalCost += roomSubtotals[roomName].cost;
        });
        
        // Add subtotals for each room
        Object.keys(roomSubtotals).forEach(roomName => {
            const roomEnergy = roomSubtotals[roomName].energy;
            const roomCost = roomSubtotals[roomName].cost;
            const percentage = totalEnergy > 0 ? (roomEnergy / totalEnergy * 100).toFixed(1) : '0.0';
            
            let subtotalRow = document.createElement("tr");
            subtotalRow.className = "subtotal-row";
            subtotalRow.innerHTML = `
                <td colspan="4"><em>Subtotal for ${roomName}</em></td>
                <td class="kwh-value"><em>${roomEnergy.toFixed(2)} kWh (${percentage}%)</em></td>
                <td class="cost-value"><em>₱${roomCost.toFixed(2)}</em></td>
            `;
            tableBody.appendChild(subtotalRow);
        });
        
        // Extract total bill from response
        if (totalBillElement) {
            const match = totalBillElement.textContent.match(/[\d.]+/);
            if (match) totalCost = parseFloat(match[0]);
        }
        
        // Add total row
        let totalRow = document.createElement("tr");
        totalRow.className = "total-row";
        totalRow.innerHTML = `
            <td colspan="4"><strong>Total Suggested Consumption</strong></td>
            <td class="kwh-value"><strong>${totalEnergy.toFixed(2)} kWh</strong></td>
            <td class="cost-value"><strong>₱${totalCost.toFixed(2)}</strong></td>
        `;
        tableBody.appendChild(totalRow);
        
        // Add target row
        const targetAmount = document.getElementById('targetBill').value;
        if (targetAmount) {
            let targetRow = document.createElement("tr");
            targetRow.className = "target-row";
            targetRow.innerHTML = `
                <td colspan="4"><strong>Target</strong></td>
                <td class="kwh-value"></td>
                <td class="cost-value"><strong>₱${parseFloat(targetAmount).toFixed(2)}</strong></td>
            `;
            tableBody.appendChild(targetRow);
            
            // Add difference row
            const diff = parseFloat(targetAmount) - totalCost;
            const colorClass = diff >= 0 ? "text-success" : "text-danger";
            
            let diffRow = document.createElement("tr");
            diffRow.className = "difference-row";
            diffRow.innerHTML = `
                <td colspan="4"><strong>Difference</strong></td>
                <td class="kwh-value"></td>
                <td class="cost-value ${colorClass}"><strong>₱${diff.toFixed(2)}</strong></td>
            `;
            tableBody.appendChild(diffRow);
        }
        
        resultsDiv.appendChild(table);
        
        // Add row highlighting behavior
        setTimeout(addTableRowHighlighting, 100);
    } else {
        resultsDiv.innerHTML = '<p>No suggestions available.</p>';
    }
}

// function getSuggestion(response) {
//     const suggestionsDiv = document.getElementById("suggestions");
//     suggestions.innerHTML = response.message;
// }

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
    const targetKwhInput = document.getElementById("targetKwh");
    const targetBillInput = document.getElementById("targetBill");
    
    // Auto-update when days, hours, rate, or targets change
    daysInput.addEventListener('input', autoUpdateConsumption);
    hoursInput.addEventListener('input', autoUpdateConsumption);
    rateInput.addEventListener('input', autoUpdateConsumption);
    targetKwhInput.addEventListener('input', autoUpdateConsumption);
    targetBillInput.addEventListener('input', autoUpdateConsumption);
    
    // Check if we should calculate on page load
    if (localStorage.getItem("sessionId") && 
        ((daysInput.value > 0 || hoursInput.value > 0) && 
        rateInput.value > 0)) {
      setTimeout(autoUpdateConsumption, 500); // Short delay to ensure DOM is ready
    }
});

// function calculateSuggestions() {
//     var sessionId = localStorage.getItem('sessionId');
//             if (!sessionId) {
//                 alert('select house first');
//                 return;
//             }


//         const targetAmount = document.getElementById('targetBill').value;
//         const targetHours = document.getElementById('hours').value;
//          var ratePerHour = document.getElementById('ratePerHour').value;
//         // document.getElementById('suggestions').innerHTML = '';

//         if (targetAmount && targetHours && ratePerHour) {
//             // Send data to Python backend
//             alert('calculate suggestions');
//             fetch("http://127.0.0.1:5000/api/get_suggestions", {
//                 method: "POST",
//                 headers: {
//                     "Content-Type": "application/json",
//                 },
//                 body: JSON.stringify({
//                     target_amount: parseFloat(targetAmount),
//                     target_hours: targetHours,
//                     rate_per_hour: ratePerHour,
//                     session_id: sessionId,
//                 }),
//             })
//             .then(response => response.json())
//             .then(getSuggestion)
//             .catch(error => {
//                 console.error("Error getting suggestions:", error);
//                 alert("Failed to get suggestions. Please try again.");
//             });

//         } else {
//             alert("Please enter valid target amount, rate Per Hour, and hours.");
//         }
//     }


    function getSuggestion(response) {
            const suggestionsDiv = document.getElementById('results');
            suggestionsDiv.innerHTML = response.message;
    }

    // Function to check if appliance-room combination is restricted
function isRestrictedCombination(roomId, applianceId) {
    // List of restricted appliance IDs
    //Large Refrigerators - Bedrooms, Bathrooms, Closets, Living Rooms, etc.
    const restrictedApplianceIds1 = ['77', '78', '79'];
    //Ovens and Microwaves - Any non-kitchen, non-dining rooms.
    const restrictedApplianceIds2 = ['93', '94', '95', '96'];
    //Washing Machines - Bedrooms, Living Rooms, Dining Rooms, Closets, etc.
    const restrictedApplianceIds3 = ['107', '108', '109'];
    //TVs Bathrooms, Kitchens, Closets, Laundry, etc.
    const restrictedApplianceIds4 = ['99', '100', '101', '102', '103', '104'];
    //Irons - Kitchens, bathrooms, closets, porches, garage.
    const restrictedApplianceIds5 = ['81', '82'];
    //Vacuum Cleaners - Bathrooms, kitchens, porches.
    const restrictedApplianceIds6 = ['105'];
    // Air Conditioners in non-enclosed or utility areas
    const restrictedApplianceIds7 = ['65', '66'];
    // Chargers (all types) in kitchens, bathrooms, porches
    const restrictedApplianceIds8 = ['67', '68', '69', '70', '71', '72'];
    // Halogen lights and Incandescent bulbs in closets or bathrooms
    const restrictedApplianceIds9 = ['85', '91'];
    // Fans in bathrooms, porches, and walk-in closets
    const restrictedApplianceIds10 = ['73', '74', '75', '76'];
    //Desktops, Laptops & Gaming PCs in bathrooms, kitchens, laundry
    const restrictedApplianceIds11 = ['83', '84', '97', '98'];
    //CRT TVs in non-living spaces
    const restrictedApplianceIds12 = ['99'];
    //Mini Fridge in Bathroom, Porch
    const restrictedApplianceIds13 = ['80'];
    
    // List of restricted room IDs for the first appliance group
    const restrictedRoomIds1 = [
        'B1_bedTop', 'B1_bedBot', 'B1_bath', 'B1_livingRoom',
'B2_bedTopLeft', 'B2_bedTopRight', 'B2_livingRoom', 'B2_bathTop', 'B2_bathBot', 'B2_bedBot',
'B3_bedTop', 'B3_bedBot', 'B3_masterBedroom', 'B3_livingRoom', 'B3_bathroom',
'C1_mainBath', 'C1_walkInCloset', 'C1_bed#2', 'C1_mainBed', 'C1_living', 'C1_bed#3',
'D1_bed1', 'D1_bed2', 'D1_bed3', 'D1_living', 'D1_bathTop', 'D1_bathBot',
'C2_mainBath', 'C2_walkInClosetLeft', 'C2_walkInClosetBotLeft', 'C2_walkInClosetBotRight', 'C2_mainBed',
'C2_greatRoom', 'C2_bath', 'C2_bed#2', 'D2_bedroom', 'D2_living'

    ];
    // List of restricted room IDs for the second appliance group
    const restrictedRoomIds2 = [
          'B1_bedTop', 'B1_bedBot', 'B1_bath', 'B1_livingRoom', 'B1_porch',
  'B2_bedTopLeft', 'B2_bedTopRight', 'B2_livingRoom', 'B2_bathTop', 'B2_bathBot', 'B2_garage', 'B2_porch', 'B2_bedBot',
  'B3_walkInCloset', 'B3_bedTop', 'B3_garage', 'B3_masterBedroom', 'B3_livingRoom', 'B3_bathroom', 'B3_porch', 'B3_bedBot',
  'C1_machine', 'C1_mud', 'C1_bed#2', 'C1_mainBath', 'C1_walkInCloset', 'C1_bathRight', 'C1_mainBed', 'C1_living', 'C1_bed#3', 'C1_coveredPorch',
  'D1_bed3', 'D1_bed2', 'D1_laundry', 'D1_bathTop', 'D1_bed1', 'D1_bathBot', 'D1_living', 'D1_porch',
  'C2_coveredDeck', 'C2_laundry', 'C2_walkInClosetLeft', 'C2_greatRoom', 'C2_mainBath', 'C2_walkInClosetBotLeft', 'C2_bath', 'C2_walkInClosetBotRight', 'C2_mainBed', 'C2_foyer', 'C2_bed#2', 'C2_frontProch',
  'D2_porch', 'D2_bedroom', 'D2_living'
       
    ];
        const restrictedRoomIds3 = [
            'B1_bedTop', 'B1_bedBot', 'B1_dining', 'B1_livingRoom', 'B1_bath',
'B2_bedTopLeft', 'B2_bedTopRight', 'B2_livingRoom', 'B2_dining/kitchen',
'B3_bedTop', 'B3_bedBot', 'B3_dining', 'B3_livingRoom', 'B3_bathroom',
'C1_bed#2', 'C1_mainBed', 'C1_living', 'C1_dining', 'C1_mainBath',
'D1_bed1', 'D1_bed2', 'D1_bed3', 'D1_living', 'D1_dining',
'C2_dining', 'C2_mainBath', 'C2_mainBed', 'C2_bed#2',
'D2_bedroom', 'D2_dining', 'D2_living'

    ];
        const restrictedRoomIds4 = [
            'B1_bath', 'B1_kitchen',
'B2_bathTop', 'B2_bathBot',
'B3_bathroom', 'B3_kitchen',
'C1_mainBath', 'C1_kitchen',
'D1_bathTop', 'D1_bathBot',
'C2_kitchen', 'C2_mainBath', 'C2_bath', 'C2_Pantry',
'D2_kitchen'

    ];
        const restrictedRoomIds5 = [
            'B1_kitchen', 'B1_bath', 'B1_porch',
'B2_bathTop', 'B2_bathBot', 'B2_porch', 'B2_garage',
'B3_bathroom', 'B3_kitchen', 'B3_garage', 'B3_porch',
'C1_kitchen', 'C1_mainBath', 'C1_mud',
'D1_bathTop', 'D1_bathBot', 'D1_porch', 'D1_laundry',
'C2_kitchen', 'C2_mainBath', 'C2_bath', 'C2_Pantry', 'C2_frontProch', 'C2_coveredDeck', 'C2_laundry'

    ];
        const restrictedRoomIds6 = [
            'B1_bath', 'B1_kitchen', 'B1_porch',
'B2_bathTop', 'B2_bathBot', 'B2_porch',
'B3_bathroom', 'B3_kitchen', 'B3_porch',
'C1_kitchen', 'C1_mainBath', 'C1_mud',
'D1_bathTop', 'D1_bathBot', 'D1_porch',
'C2_kitchen', 'C2_mainBath', 'C2_bath', 'C2_frontProch', 'C2_coveredDeck',
'D2_kitchen', 'D2_porch'

    ];
        const restrictedRoomIds7 = [
            'B1_kitchen', 'B1_bath', 'B1_porch',
'B2_bathTop', 'B2_bathBot', 'B2_porch', 'B2_garage',
'B3_kitchen', 'B3_bathroom', 'B3_porch', 'B3_garage',
'C1_kitchen', 'C1_mainBath', 'C1_mud',
'D1_bathTop', 'D1_bathBot', 'D1_porch', 'D1_laundry',
'C2_kitchen', 'C2_mainBath', 'C2_bath', 'C2_Pantry', 'C2_coveredDeck', 'C2_laundry',
'D2_porch', 'D2_kitchen'

    ];
        const restrictedRoomIds8 = [
              'B1_kitchen', 'B1_bath', 'B1_porch',
  'B2_bathTop', 'B2_bathBot', 'B2_porch',
  'B3_kitchen', 'B3_bathroom', 'B3_porch',
  'C1_kitchen', 'C1_mainBath', 'C1_mud',
  'D1_bathTop', 'D1_bathBot', 'D1_porch', 'D1_laundry',
  'C2_kitchen', 'C2_mainBath', 'C2_bath', 'C2_coveredDeck', 'C2_laundry',
  'D2_porch', 'D2_kitchen'
    ];
        const restrictedRoomIds9 = [
              'B1_bath',
  'B2_bathTop', 'B2_bathBot',
  'B3_walkInCloset', 'B3_bathroom',
  'C1_mainBath', 'C1_walkInCloset', 'C1_bathRight',
  'D1_bathTop', 'D1_bathBot',
  'C2_mainBath', 'C2_bath',
  'C2_walkInClosetLeft', 'C2_walkInClosetBotLeft', 'C2_walkInClosetBotRight'
    ];
        const restrictedRoomIds10 = [
              'B1_bath', 'B1_porch',
  'B2_bathTop', 'B2_bathBot', 'B2_porch',
  'B3_walkInCloset', 'B3_bathroom', 'B3_porch',
  'C1_mainBath', 'C1_walkInCloset',
  'D1_bathTop', 'D1_bathBot', 'D1_porch',
  'C2_walkInClosetLeft', 'C2_walkInClosetBotLeft', 'C2_walkInClosetBotRight',
  'C2_mainBath', 'C2_bath', 'C2_coveredDeck',
  'D2_porch'
    ];
        const restrictedRoomIds11 = [
              'B1_kitchen', 'B1_bath', 'B1_porch',
  'B2_bathTop', 'B2_bathBot', 'B2_porch', 'B2_garage',
  'B3_kitchen', 'B3_bathroom', 'B3_porch', 'B3_garage',
  'C1_kitchen', 'C1_mainBath',
  'D1_bathTop', 'D1_bathBot', 'D1_porch', 'D1_laundry',
  'C2_kitchen', 'C2_mainBath', 'C2_bath', 'C2_coveredDeck', 'C2_laundry',
  'D2_kitchen', 'D2_porch'
    ];
        const restrictedRoomIds12 = [
              'B1_kitchen', 'B1_bath', 'B1_porch',
  'B2_bathTop', 'B2_bathBot', 'B2_porch',
  'B3_kitchen', 'B3_bathroom', 'B3_porch', 'B3_walkInCloset',
  'C1_kitchen', 'C1_mainBath', 'C1_walkInCloset',
  'D1_bathTop', 'D1_bathBot', 'D1_porch',
  'C2_kitchen', 'C2_mainBath', 'C2_bath', 'C2_walkInClosetLeft', 'C2_walkInClosetBotLeft', 'C2_walkInClosetBotRight', 'C2_coveredDeck',
  'D2_kitchen', 'D2_porch'
    ];
            const restrictedRoomIds13 = [
                  'B1_bath',
  'B1_porch',
  'B2_bathTop',
  'B2_bathBot',
  'B2_porch',
  'B3_bathroom',
  'B3_porch',
  'C1_mainBath',
  'C1_mud',
  'C1_walkInCloset',
  'C1_bathRight',
  'C1_coveredPorch',
  'D1_bathTop',
  'D1_bathBot',
  'D1_porch',
  'D1_laundry',
  'C2_walkInClosetLeft',
  'C2_coveredDeck',
  'C2_walkInClosetBotLeft',
  'C2_bath',
  'C2_walkInClosetBotRight',
  'C2_laundry',
  'C2_frontProch',
  'D2_porch'
    ];
    
    // Check restrictions for first group
    if (restrictedRoomIds1.includes(roomId) && restrictedApplianceIds1.includes(applianceId)) {
        return true;
    }
    
    // Check restrictions for second group
    if (restrictedRoomIds2.includes(roomId) && restrictedApplianceIds2.includes(applianceId)) {
        return true;
    }
    // Check restrictions for third group
    if (restrictedRoomIds3.includes(roomId) && restrictedApplianceIds3.includes(applianceId)) {
        return true;
    }
    // Check restrictions for fourth group
    if (restrictedRoomIds4.includes(roomId) && restrictedApplianceIds4.includes(applianceId)) {
        return true;
    }
    // Check restrictions for fifth group
    if (restrictedRoomIds5.includes(roomId) && restrictedApplianceIds5.includes(applianceId)) {
        return true;
    }
    // Check restrictions for sixth group
    if (restrictedRoomIds6.includes(roomId) && restrictedApplianceIds6.includes(applianceId)) {
        return true;
    }
    // Check restrictions for seventh group
    if (restrictedRoomIds7.includes(roomId) && restrictedApplianceIds7.includes(applianceId)) {
        return true;
    }
    // Check restrictions for eighth group
    if (restrictedRoomIds8.includes(roomId) && restrictedApplianceIds8.includes(applianceId)) {
        return true;
    }
    // Check restrictions for ninth group
    if (restrictedRoomIds9.includes(roomId) && restrictedApplianceIds9.includes(applianceId)) {
        return true;
    }
    // Check restrictions for tenth group
    if (restrictedRoomIds10.includes(roomId) && restrictedApplianceIds10.includes(applianceId)) {
        return true;
    }
    // Check restrictions for eleventh group
    if (restrictedRoomIds11.includes(roomId) && restrictedApplianceIds11.includes(applianceId)) {
        return true;
    }
    // Check restrictions for twelfth group
    if (restrictedRoomIds12.includes(roomId) && restrictedApplianceIds12.includes(applianceId)) {
        return true;
    }
    // Check restrictions for thirteenth group
    if (restrictedRoomIds13.includes(roomId) && restrictedApplianceIds13.includes(applianceId)) {
        return true;
    }
    
    return false;
}

// Function to flash container red
function flashContainerRed(element) {
    // Find the closest room container
    const roomContainer = element.closest('.room');
    
    // Add a CSS class for the red flash effect
    roomContainer.classList.add('restricted-flash');
    
    // Remove the class after the animation completes
    setTimeout(() => {
        roomContainer.classList.remove('restricted-flash');
    }, 1000);
}