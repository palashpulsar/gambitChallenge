var select = document.getElementById("selector");
var option = '';
alert("executing");
for (var i=1; i<=100; i++){
	option += '<option value="'+i+'">Register Number '+i+'</option>';
}
select.innerHTML += option;