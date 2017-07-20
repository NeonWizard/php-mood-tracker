function createGrid() {
	// clear grid of previous elements
	while (document.getElementById("mood-grid").firstChild) {
		document.getElementById("mood-grid").removeChild(document.getElementById("mood-grid").firstChild);
	}

	let today = new Date();
	let doy = today.getDOY();
	let startDate = new Date();
	startDate.setDate(today.getDate() - 182);
	startDate.setDate(startDate.getDate() - (6-startDate.getDay())); // set startDate to a monday
	
	let daysToDisplay = Date.daysBetween(startDate, today)

	// get daily information from server from past daysToDisplay
	// -- pass --

	// populate grid with boxes
	let week = [];
	for (let day = daysToDisplay; day >= 0; day--) {
		// clone my mood box template from the DOM
		let boxContainer = document.getElementById("mood-box-template").content.cloneNode(true).children[0];
		let boxElem = boxContainer.querySelector(".mood-box");
		// boxElem.innerText = doy - day;
		boxElem.doy = doy - day;

		week.push(boxContainer);

		// if a column is done, we then push it to the DOM's grid
		if (week.length == 7) {
			// create the new week column element
			let weekElem = document.createElement("DIV");
			weekElem.className = "mood-grid-col";

			if (day > 3 && day <= 10) {
				let monthHeader = document.createElement("SPAN");
				// monthHeader.innerHTML = month.getShortMonthName();
				monthHeader.className = "month-header";
				weekElem.appendChild(monthHeader);
			}

			// populate the week element and empty the array
			for (let boxElem of week) {
				weekElem.appendChild(boxElem);
			}
			week = [];

			// push it to DOM
			document.getElementById("mood-grid").appendChild(weekElem);
		}
	}
	if (week) {
		// create the new week column element
		let weekElem = document.createElement("DIV");
		weekElem.className = "mood-grid-col";

		// populate the week element and empty the array
		for (let boxElem of week) {
			weekElem.appendChild(boxElem);
		}
		week = [];

		// push it to DOM
		document.getElementById("mood-grid").appendChild(weekElem);
	}
}

createGrid();
