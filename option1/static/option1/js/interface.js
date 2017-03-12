var variable = [];
var humanData = [];
var modbusData = [];
var backendData;

$(document).on("pageinit", function(event){
    retrieveCurrentDataFromDatabase();
});

function retrieveCurrentDataFromDatabase(){
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
}

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