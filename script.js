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
    var sessionName = localStorage.getItem("sessionName");
    var sessionId = localStorage.getItem("sessionId");
    document.getElementById("stitle").innerHTML = sessionName;
    document.getElementById("simulation_title").innerHTML = sessionName;

    showHouse();

    if (sessionName) {
        //document.getElementById('addRoom').style.display = '';
        document.getElementById("delete").style.display = "";
    } else {
        //document.getElementById('addRoom').style.display = 'none';
        document.getElementById("delete").style.display = "none";
    }

    document.getElementById("results").style.display = "none";

    showRoom();
}

// perspective
function showHouse() {
    var housename = localStorage.getItem("sessionId");
    const container = document.getElementById("persepective");
    const img = document.createElement("img");
    if (housename == 87) {
        img.src = "assets/perspective/bungalow1.png";
    }
    if (housename == 91) {
        img.src = "assets/perspective/bungalow2.png";
    }
    if (housename == 92) {
        img.src = "assets/perspective/bungalow3.png";
    }
    if (housename == 89) {
        img.src = "assets/perspective/duplex1.png";
    }
    if (housename == 85) {
        img.src = "assets/perspective/duplex2.png";
    }
    if (housename == 86) {
        img.src = "assets/perspective/duplex3.png";
    }
    if (housename == 84) {
        img.src = "assets/perspective/t1.png";
    }
    if (housename == 88) {
        img.src = "assets/perspective/t2.png";
    }
    if (housename == 90) {
        img.src = "assets/perspective/t3.png";
    }
    img.alt = "Example Image";

    // Make the image responsive to the container's size
    img.style.width = "100%";
    img.style.height = "100%";
    img.style.objectFit = "contain"; // Ensures the image fits inside the container without distortion

    // Clear previous content and add the image to the container
    container.innerHTML = "";
    container.appendChild(img);
}

// layout container
function showRoom() {
    var simulationId = localStorage.getItem("sessionId");
    fetch(
        `http://127.0.0.1:5000/api/fetch_room?simulationId=${simulationId}`
    )
        .then((response) => response.json())
        .then((data) => outputRoom(data))
        .catch((error) => console.error("Error fetching room:", error));
}

function outputRoom(response) {
    var a = document.getElementById("roomContainer");
    a.innerHTML = response.message;
}

function canvasShowMessage(response) {
    showRoom();
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
    // document.getElementById("demo").style.color = "";
    event.target.style.border = "";

    const imageId = event.dataTransfer.getData("Text");
    const fromRoom = event.dataTransfer.getData("custom_id");
    const isUpdate = event.dataTransfer.getData("is_update");
    const canvasId = event.dataTransfer.getData("canvas_id");

    var sessionName = localStorage.getItem("sessionName");
    var sessionId = localStorage.getItem("sessionId");

    //dont accept drag drop if same room, and logic for updating or adding

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
    event.target.appendChild(draggedElement);
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
        .then((data) => canvasShowMessage(data))
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
        .then((data) => canvasShowMessage(data))
        .catch((error) =>
        console.error("Error adding appliance to canvas:", error)
        );
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
async function startSimulation(hours, ratePerHour) {
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

    // After processing inputs, compute energy based on total hours
    computeEnergy(hoursTracker, ratePerHour, hours);

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

function stopAndCompute() {
    document.getElementById("results").style.display = "block";

    // Clear the previous content
    const resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = "";

    let totalEnergy = 0; // Variable to store total energy consumption
    let totalCost = 0; // Variable to store total cost

    // Create the table and add headers
    let table = document.createElement("table");
    table.className = "table table-striped"; // Add classes for styling
    table.innerHTML = `
    <thead>
        <tr>
            <th>Room</th>
            <th>Appliance</th>
            <th>Wattage</th>
            <th>Usage</th>
            <th>kWh</th>
            <th>Budget (₱)</th>
        </tr>
    </thead>
    <tbody>
    </tbody>
    `;
    let tableBody = table.querySelector("tbody");

    // Loop through each room and its appliances
    Object.keys(myArray).forEach((roomName) => {
        // Loop through each appliance in the room
        myArray[roomName].forEach((item) => {
        // Create a row for each appliance
        let row = document.createElement("tr");

        // Add the room name and appliance details to the row
        row.innerHTML = `
            <td>${roomName}</td>
            <td>${item.applianceName}</td>
            <td>${item.wattage} W</td>
            <td>${item.hours_used}</td>
            <td>${item.energy}</td>
            <td>₱${item.amount.toFixed(2)}</td>
        `;
        tableBody.appendChild(row);

        // Accumulate total energy and cost
        totalEnergy += item.energy;
        totalCost += item.amount;
        });
    });

    // Create a row for total energy and cost
    let totalRow = document.createElement("tr");
    totalRow.innerHTML = `
    <td colspan="4" class="text-center"><strong>Total</strong></td>
    <td><strong>${totalEnergy.toFixed(2)} kWh</strong></td>
    <td><strong>₱${totalCost.toFixed(2)}</strong></td>
    `;
    tableBody.appendChild(totalRow);

    var targetKwh = document.getElementById("targetKwh").value;
    var targetBill = document.getElementById("targetBill").value;

    // Check if target kWh or target Bill has input and append an extra row
    if (targetKwh || targetBill) {
        let targetRow = document.createElement("tr");
        targetRow.innerHTML = `
        <td colspan="4" class="text-center"><strong>Target</strong></td>
        <td><strong>${targetKwh ? targetKwh + " kWh" : ""}</strong></td>
        <td><strong>₱${targetBill ? targetBill : ""}</strong></td>
        `;
        tableBody.appendChild(targetRow);

        let differenceRow = document.createElement("tr");
        differenceRow.innerHTML = `
        <td colspan="4" class="text-center"><strong>Difference</strong></td>
        <td><strong>${
            targetKwh ? (targetKwh - totalEnergy).toFixed(2) + " kWh" : ""
        }</strong></td>
        <td><strong>₱${
            targetBill ? (targetBill - totalCost).toFixed(2) : ""
        }</strong></td>
        `;
        tableBody.appendChild(differenceRow);
    }

    // Append the table to the results
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
