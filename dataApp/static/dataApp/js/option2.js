var varType;

$(document).on("pagecreate", function(event){
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

// The following function creates the content of dropdown menu of Option2 frontend page.
function dropDownMenu(varType){
    var select = document.getElementById("selector");
    select.innerHTML = "";
    var option;
    var variableList = [];
    if (varType == 'modbus'){
        for (var i=1; i<=100; i++){
            option += '<option value="'+i+'">Register Number '+i+'</option>'; // Creating opitons
        }
        select.innerHTML += option;
    }
    else{
        if (varType == 'human'){
            $.ajax({
                type: "GET",
                url: urlVarList,
                async:false,
                success: function(data){
                    variableList = data;
                    for (var i = 0; i<variableList.length; i++){
                        option += '<option value="'+variableList[i]+'">'+variableList[i]+'</option>'; // Creating opitons
                    }
                }
            });
            select.innerHTML += option;
        }
        else{
            option = '<option>Pick the kind of data (Modbus type or Human readable type) first</option>'; // Creating opitons
            select.innerHTML += option;
        }
    }
}

// On Plot button click
function plotButtonClicked(){
    console.log("Looking for fresh data in the database for Option2.");
    var select = document.getElementById("selector");
    varFromDatabaseCalled(select.value)
}

// Setting time interval of 5 minutes to make the frontend real-time.
setInterval(plotButtonClicked, 5*60*1000); // Every 5 minutes

// Making ajax call to retrieve the last 5 data from database.
function varFromDatabaseCalled(value){
    var backendData;
    if (varType == 'modbus'){
        url = urlData + "?varType=modbus&varName=" + value;
    }
    else{
        if (varType == 'human'){
            url = urlData + "?varType=human&varName=" + value;
        }
    }
    $.ajax({
        type: "GET",
        url: url,
        async:false,
        success: function(data){
            backendData = data;
        }
    }); 
    console.log(backendData);
    svgPlot(backendData);
}

function svgPlot(backendData){

    // Remove existing d3 plot
    d3.selectAll("svg").remove();

    // Set the dimension
    var margin = {top: 20, right: 20, bottom: 50, left: 70},
                    width = 1300 - margin.left - margin.right,
                    height = 300 - margin.top - margin.bottom;

    // append the svg obgect to the body of the page
    // appends a 'group' element to 'svg'
    // moves the 'group' element to the top left margin
    var svg = d3.select("#d3js_Plot").append("svg")
                                .attr("width", width + margin.left + margin.right)
                                .attr("height", height + margin.top + margin.bottom)
                                .append("g")
                                .attr("transform",
                                        "translate(" + margin.left + "," + margin.top + ")");
    
    // Parse the date / time
    var parseTime = d3.timeParse('%Y-%m-%dT%H:%M:%S');
    var formatTime = d3.timeFormat("%e %B %H:%M:%S");

    // Get the data
    var dates = backendData.datetimestamp;
    var requiredData = backendData.dataVar;
    var Data = [];
    for (var i=0; i<dates.length; i++){
        Data.push({
            "x": parseTime(dates[i]),
            "y": requiredData[i]
    });
    }

    // Set the ranges
    var x = d3.scaleTime().range([0, width]);
    var y = d3.scaleLinear().range([height, 0]);

    // Scale the range of data
    x.domain(d3.extent(Data, function(d) { return d.x; }));
    y.domain([0, d3.max(Data, function(d) { return d.y; })]);

    // Define the line
    var valueline = d3.line()
                        .x(function(d) {return x(d.x)})
                        .y(function(d) {return y(d.y)});

    // Define the div for the tooltip
    var div = d3.select("#d3js_Plot").append("div")
                                .attr("class", "tooltip")               
                                .style("opacity", 0);

    // Add the valueline path.
    svg.append("path")
        .data([Data])
        .attr("d", valueline)
        .attr("stroke", "blue")
        .attr("stroke-width", 2)
        .attr("fill", "lightsteelblue");

    // Add the scatterplot
    svg.selectAll("dot")    
        .data(Data)         
        .enter().append("circle")                               
                    .attr("r", 5)       
                    .attr("cx", function(d) { return x(d.x); })      
                    .attr("cy", function(d) { return y(d.y); }) 
                    .on("mouseover", function(d) {  
                            console.log(d.x);   
                            div.transition()        
                                .duration(200)      
                                .style("opacity", .9);      
                            div.html(formatTime(d.x) + "<br/>"  + d.y)  
                                .style("left", (d3.event.pageX) + "px")     
                                .style("top", (d3.event.pageY - 28) + "px");    
                    })                  
                    .on("mouseout", function(d) {       
                            div.transition()        
                                .duration(500)      
                                .style("opacity", 0);   
                    }); 

    // Add the x Axis
    svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x));

    // text label for the x axis
    svg.append("text")             
        .attr("transform",
            "translate(" + (width/2) + " ," + 
                           (height + margin.top + 20) + ")")
        .style("text-anchor", "middle")
        .text("Timestamp");

    // Add the y Axis
    svg.append("g")
        .call(d3.axisLeft(y));

    // text label for the y axis
    svg.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 0 - margin.left)
        .attr("x",0 - (height / 2))
        .attr("dy", "1em")
        .style("text-anchor", "middle")
        .text("Value");
}
