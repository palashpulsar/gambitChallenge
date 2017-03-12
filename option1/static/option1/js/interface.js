var variable = [];
var humanData = [];
var modbusData = [];
var backendData;


$(document).on("pagecreate", function(event){
    retrieveCurrentDataFromDatabase();
});

function retrieveCurrentDataFromDatabase(){
    console.log("Looking for fresh data in the database for Option1.");
	$.ajax({
		type: "GET",
        url: dataRetrieve,
        async: false,
        success: function(data){
        	backendData = data;
        	for (var key in data){
        		variable.push(key);
        		humanData.push(data[key].human);
        	}
        }
	});
    displayTabular();
};

setInterval(retrieveCurrentDataFromDatabase, 5*60*1000); // Every 5 minutes

function displayTabular(){
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