var variableList = [];
var varType;

$(document).on("pageinit", function(event){
    dropDownMenu('nothing selected');
    $("#radio-choice-0a").click(function(){
        varType = "modbus";
        dropDownMenu(varType);
    });
    $("#radio-choice-0b").click(function(){
        varType = "human";
        dropDownMenu(varType);
    });
});

function dropDownMenu(varType){
    var select = document.getElementById("selector");
    select.innerHTML = "";
    var option;
    if (varType == 'modbus'){
        for (var i=1; i<=100; i++){
            option += '<option value="'+i+'">Register Number '+i+'</option>';
        }
        select.innerHTML += option;
    }
    else{
        if (varType == 'human'){
            $.ajax({
                type: "GET",
                url: urlHumanType,
                async:false,
                success: function(data){
                    variableList = data;
                    for (var i = 0; i<variableList.length; i++){
                        option += '<option value="'+variableList[i]+'">'+variableList[i]+'</option>';
                    }
                }
            });
            select.innerHTML += option;
        }
        else{
            option = '<option>Pick the kind of data (Modbus type or Human readable type) first</option>';
            select.innerHTML += option;
        }
    }
}
