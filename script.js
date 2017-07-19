function createGrid() {
	// clear grid of previous elements
	while (document.getElementById("mood-grid").firstChild) {
		document.getElementById("mood-grid").removeChild(document.getElementById("mood-grid").firstChild);
	}

 	let week = [];
	for (let day = 0; day < 145; day++) {
		// clone my mood box template from the DOM
		let boxElem = document.getElementById("mood-box-template").content.cloneNode(true).querySelector(".mood-box");
		if (Math.random() < 0.3) {
			boxElem.style.backgroundColor = "orange";
		}

		week.push(boxElem);

		// if a column is done, we then push it to the DOM's grid
		if (week.length == 6) {
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
}

createGrid();
