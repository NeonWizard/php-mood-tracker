Date.prototype.isLeapYear = function() {
	var year = this.getFullYear();
	if((year & 3) != 0) return false;
	return ((year % 100) != 0 || (year % 400) == 0);
}

// Get Day of Year
Date.prototype.getDOY = function() {
	var dayCount = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334];
	var mn = this.getMonth();
	var dn = this.getDate();
	var dayOfYear = dayCount[mn] + dn;
	if(mn > 1 && this.isLeapYear()) dayOfYear++;
	return dayOfYear;
}

Date.daysBetween = function(date1, date2) {
	let one_day = 1000*60*60*24;
	let date1_ms = date1.getTime();
	let date2_ms = date2.getTime();
	let difference_ms = date2_ms - date1_ms;

	return Math.round(difference_ms / one_day);
}

Date.prototype.monthNames = [
	"January", "February", "March",
	"April", "May", "June",
	"July", "August", "September",
	"October", "November", "December"
];

Date.prototype.getMonthName = function() {
	return this.monthNames[this.getMonth()];
}
Date.prototype.getShortMonthName = function () {
	return this.getMonthName().substr(0, 3);
}
Date.prototype.monthDays = function() {
	let d = new Date(this.getFullYear(), this.getMonth() + 1, 0);
	return d.getDate();
}
