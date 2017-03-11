var variable = [];
var humanData = [];
var modbusData = [];
var backendData;

$(document).on("pageinit", function(event){
    alert("Page is being shown here.");
    retrieveCurrentDataFromDatabase();
});

function retrieveCurrentDataFromDatabase(){
	console.log("1. retrieveDataFromDatabase activated");
	console.log(dataRetrieve);
	$.ajax({
		type: "GET",
        url: dataRetrieve,
        success: function(data){
        	backendData = data;
        	for (var key in data){
        		variable.push(key);
        		humanData.push(data[key].human);
        	}
        	console.log(backendData);
        	console.log(variable);
        }
	});
}