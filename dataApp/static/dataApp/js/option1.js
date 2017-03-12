$(document).on("pagecreate", function(event){
    retrieveCurrentDataFromDatabase();
});

// Making AJAX call to retrieve the latest entry to database.
function retrieveCurrentDataFromDatabase(){
    console.log("Looking for fresh data in the database for Option1.");
    var backendData;
	$.ajax({
		type: "GET",
        url: dataRetrieve,
        async: false,
        success: function(data){
        	backendData = data;
        }
	});
    displayTabular(backendData);
};

// AJAX call is made every 5 minutes
setInterval(retrieveCurrentDataFromDatabase, 5*60*1000); // Every 5 minutes

// Displaying the lastest entry to database in a tabular form in front end.
function displayTabular(backendData){
    var tbody = document.getElementById('tbody');
    for (var key in backendData){
        var regVar=[];
        var human = backendData[key]["human"];
        regVar.push(backendData[key]["A"]);
        if (backendData[key]["B"] != null) {
            regVar.push(backendData[key]["B"]);
        }
        if (backendData[key]["C"] != null) {
            regVar.push(backendData[key]["C"]);
        }
        var tr = "<tr>";
        tr += "<td>" + key + "</td>" + "<td>" + regVar + "</td>" + "<td>" + human + "</td></tr>";
        tbody.innerHTML += tr;
    }
}