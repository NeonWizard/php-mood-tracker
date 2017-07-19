Date.prototype.monthNames = [
	"January", "February", "March",
	"April", "May", "June",
	"July", "August", "September",
	"October", "November", "December"
];

Date.prototype.getMonthName = function() {
	return this.monthNames[this.getMonth()];
};
Date.prototype.getShortMonthName = function () {
	return this.getMonthName().substr(0, 3);
};
Date.prototype.monthDays = function() {
	let d = new Date(this.getFullYear(), this.getMonth() + 1, 0);
	return d.getDate();
}


function createGrid() {
	// clear grid of previous elements
	while (document.getElementById("mood-grid").firstChild) {
		document.getElementById("mood-grid").removeChild(document.getElementById("mood-grid").firstChild);
	}

	let spring = new Date().getMonth() < 6;

	let week = [];
	for (let monthNum = (spring ? 0 : 6); monthNum < (spring ? 6 : 12); monthNum++) {
		let month = new Date(2017, monthNum);
		for (let day = 1; day <= month.monthDays(); day++) {
			// clone my mood box template from the DOM
			let boxContainer = document.getElementById("mood-box-template").content.cloneNode(true).children[0];
			let boxElem = boxContainer.querySelector(".mood-box");

			week.push(boxContainer);

			// if a column is done, we then push it to the DOM's grid
			if (week.length == 7) {
				// create the new week column element
				let weekElem = document.createElement("DIV");
				weekElem.className = "mood-grid-col";

				if (day > 3 && day <= 10) {
					let monthHeader = document.createElement("SPAN");
					monthHeader.innerHTML = month.getShortMonthName();
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
