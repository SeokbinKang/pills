// JavaScript Document
var group_numberofGroups=0;
var GroupList=[];
function Group_CreateGroup(patientIDs,filter) {
	//TODO create group list
	//TODO Add visual element to each chart	
	if(filter.MPRFilter.enabled) {
	
	 var d_mprovertime = GetData_MPR_over_TIME(null);
	 var o_chartoption = createChartOption(1000,400,"none","none");
	 //createLinechart(d_mprovertime,"GraphView_Time",'appendData',group_numberofGroups,o_chartoption,filter);
	 
	// createScatterchart(d_mprovertime,"GraphView_Period","filter",group_numberofGroups,o_chartoption, filter);
	
	 AddGrouptoUI('Group '+filter.ID,filter.color,filter);	
	}
	// createLinechart(d_mprovertime,"GraphView_Period",'appendData',group_numberofGroups,o_chartoption);
	
}


function ParseData_MPRRange(data_) {
	  var Nrange=20;
	  var data_range = data_.map(function(d) { 
		  var ival = (d[0]*Nrange) | 0;

		  return ival;
	   });
	  var Frequency=[]
	  for (i=0;i<Nrange;i++){
		  Frequency[i]=0;
	  }
	  
	  for (i=0;i<data_range.length;i++){
		  Frequency[data_range[i]]++;		  
	  }
	  var FrequencyObejct = Frequency.map(function(d,i) { 
	  	var item_={range:(i+1)/Nrange,count:d};
		//item_.range = i/Nrange;
	//	item_.count = d;
		return item_;
	  });

	return FrequencyObejct;	   
}

function createChartOption(w,h,xlabel_,ylabel_,type_){
	var option = {type : type_,width:w, height:h, xLabel:xlabel_ , yLabel:ylabel_};
	return option;
}
function createFilterOption(mprenabled, mprMin,mprMax,filterMeasure_){
	group_numberofGroups++;
		var color = d3.scale.category10().domain(d3.range(0,10));
	var filter_option = { ID:group_numberofGroups , filterMeasure : filterMeasure_ , MPRFilter : { enabled : mprenabled, minValue : mprMin , maxValue : mprMax} , color : color(group_numberofGroups) };
	return filter_option;
}
function GetData_MPR_over_TIME(patiensIDs) {
	var MPRt=[];
	var random_start = chance.floating({min: 0.19, max: 0.81});
	for(i=0;i<100;i++){
		var change = chance.floating({min: -0.05, max: 0.05});
		random_start +=change;
		
		MPRt[i]=random_start;
	}
	return MPRt;
}
   

function createbarChart(data_,parentNodeID,flag, cOption) {
	var margin = {top: 40, right: 70, bottom: 80, left: 70},
	 width = cOption.width - margin.left - margin.right,
    height = cOption.height - margin.top - margin.bottom;


	if(cOption.type == 'MPR_DIST') {
		
		data_=data_.stats.mprRange;
		xAttr= 'range';
		yAttr= 'count';
		xLabel = cOption.xLabel;
		yLabel = cOption.yLabel;
			
	} else if(cOption.type == 'CSA_DIST'){
		
		data_=data_.stats.csaRange;
		xAttr= 'range';
		yAttr= 'count';
		xLabel = cOption.xLabel;
		yLabel = cOption.yLabel;
		
	} else if(cOption.type == 'CMG_DIST'){
		
		data_=data_.stats.cmgRange;
		xAttr= 'range';
		yAttr= 'count';
		xLabel = cOption.xLabel;
		yLabel = cOption.yLabel;
		
	} else 	return ;




var x = d3.scale.ordinal()
    .rangeRoundBands([0, width], .1,0.2);

var y = d3.scale.linear()
    .range([height, 0]);

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left")
    .ticks(10, "d");

var svg = d3.select("#"+parentNodeID).append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
	.attr("measure",xLabel);

var brush = d3.svg.brush()
      .x(x)
      .y(y)
      .on("brushstart", brushstart)
      .on("brush", brushmove)
      .on("brushend", brushend);
	  
//var data=[{"letter":"A","frequency" : 0.1},{"letter":"B","frequency" : 0.2},{"letter":"C","frequency" : 0.3}];

var maxFrequency=0;
  	
  x.domain(data_.map(function(d) { 
  if(d[yAttr]>maxFrequency) maxFrequency=d[yAttr];
  return d[xAttr]; }));
//  y.domain([0, d3.max(data_, function(d) { return d.count; })]);
y.domain([0,maxFrequency+10]);
svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .style("fill","rgb(184, 184, 200)")
      .call(xAxis)
  .append("text")     
      .attr("y",60)
	  .attr("x",width/2)
      .style("text-anchor", "middle")	
	  .style("fill","goldenrod") 
      .text(xLabel);

  svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)
	  .style("fill","rgb(184, 184, 200)")
    .append("text")
      //.attr("transform", "rotate(-90)")
      .attr("y",-30)
	  .attr("x",-40)
      .attr("dy", ".71em")
      .style("text-anchor", "start")	
	  .style("fill","goldenrod") 
      .text(yLabel);
	  

  svg.selectAll(".bar")
      .data(data_)
    .enter().append("rect")
      .attr("class", "bardefault")
      .attr("x", function(d) { return x(d[xAttr]); })
      .attr("id", function(d) { return "bar"+d[xAttr]; })
      .attr("width", x.rangeBand())
      .attr("y", function(d) { return y(d[yAttr]); })
      .attr("height", function(d) { return height - y(d[yAttr]); })	;
	  
	svg.call(brush);	   
// Clear the previously-active brush, if any.
 function brushstart(p) {
   // if (brushCell !== this) {
   //   d3.select(brushCell).call(brush.clear());
    //  x.domain(domainByTrait[p.x]);
     // y.domain(domainByTrait[p.y]);
   //   brushCell = this;
 //   }
  }

  // Highlight the selected circles.
  var BarSelected=[];
  var MprData = data_;
  function brushmove(p) {
    var e = brush.extent();
   // console.log(e[0][0] + "  " + e[1][0]);
    svg.selectAll("rect").classed("barselected", function(d,i) {
			var defcolor = false;
			var rect_x=x(d.range);
			//console.log(i);
  		   if( e[0][0] < rect_x && e[1][0] > rect_x  ) {
			  defcolor=true;	 
		//	  console.log("selected"); 
			BarSelected[i]=1;  
		  } else {
			  BarSelected[i]=0;
		  }
          return defcolor;
		  
    });
  }

  // If the brush is empty, select all circles.
  function brushend() {
  //  if (brush.empty()) svg.selectAll(".hidden").classed("hidden", false);
  		//this.clear();
//		brush.clear();
	//Group_CreateGroup(null);
	

	var min_,max_;
	min_=100;
	max_=0;
	var mprwidth = MprData[1].range- MprData[0].range;
	for(i=0;i<BarSelected.length-10;i++){  //why -10? idk.

		if(BarSelected[i]>0) {
			if(MprData[i].range<min_) min_=MprData[i].range;
			if(MprData[i].range>max_) max_=MprData[i].range;
			
		}
		
	}	
		
	var newFilter = createFilterOption(true,(min_-mprwidth).toFixed(2),max_.toFixed(2),this.getAttribute("measure"));
	
	Group_CreateGroup(null,newFilter);
	console.log(this.getAttribute("measure"));
	console.log(this);
	console.log(newFilter);
	for(i=0;i<BarSelected.length-10;i++){
		if(BarSelected[i]>0) {
		//	console.log(svg);
			svg.selectAll('.barselected').style("fill", newFilter.color);
		}
	}
	
	svg.selectAll("rect").classed("barselected",false);
  }

function type(d) {
  d.frequency = +d.frequency;
  return d;
}
}


/*****line chart ******/

function createLinechart(data_o,parentNodeID,flag,chartOption){
	

	var color = d3.scale.category10().domain(d3.range(0,10));
	//color.domain([0, 10]);

	var margin = {top: 40, right: 70, bottom: 80, left: 70},
    width = chartOption.width - margin.left - margin.right,
    height = chartOption.height - margin.top - margin.bottom;

	
	 if(chartOption.type == 'MPR_over_MONTH'){
		data_=data_o.stats.mpr30;
		xAttr= 'i';
		yAttr= 'avg';
		xLabel = chartOption.xLabel;
		yLabel = chartOption.yLabel;
		dataID = data_o.name;
		color_ = data_o.color;
		
	} else 	return ;
	
	
	
	var x_trans = d3.scale.linear()
    .domain([0, data_.length ])
    .range([0, width]);
 
	var y_trans = d3.scale.linear()
	    .domain([0, 1])
	    .range([height, 0]);
		
	var xAxis = d3.svg.axis()
    .scale(x_trans)
    .orient("bottom");

	var yAxis = d3.svg.axis()
    .scale(y_trans)
    .orient("left")
    .ticks(10, "d");
	
	if(flag=='appendData') {
		console.log("#"+parentNodeID+"_svg"+" g"); 
		var svg = d3.select("#"+parentNodeID+"_svg"+" g");
		var line = d3.svg.line()
 		   .x(function(d, i) { return x_trans(i); })
		    .y(function(d, i) { return y_trans(d);;})
			.interpolate("basis");
 		console.log(dataID);
		var path = svg.append("g")
		    .attr("clip-path",dataID)
		  .append("path")
		    .datum(data_)
		    .attr("d", line)
			.style("fill", "none") //chance.integer({min: 0, max: 10})
			.style("stroke",filter.color)
			.style("stroke-width",3);
		
		return path;
		
		
	} else {
	
	var svg = d3.select("#"+parentNodeID).append("svg")
	    .attr("width", width+ margin.left + margin.right )
	    .attr("height", height + margin.top + margin.bottom)
		.attr("id", parentNodeID+"_svg")
	  .append("g")
	    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
 
	svg.append("defs").append("clipPath")
	    .attr("id", "clip")
	  .append("rect")
	    .attr("width", width)
	    .attr("height", height);
		
	svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .style("fill","rgb(184, 184, 200)")
      .call(xAxis)
  .append("text")     
      .attr("y",50)
	  .attr("x",width/2)
      .style("text-anchor", "middle")	
	  .style("fill","goldenrod") 
      .text(xLabel);
	 
	svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)
	  .style("fill","rgb(184, 184, 200)")
    .append("text")
      //.attr("transform", "rotate(-90)")
      .attr("y",-30)
	  .attr("x",-20)
      .attr("dy", ".71em")
      .style("text-anchor", "start")	
	  .style("fill","goldenrod") 
      .text(yLabel); 

	
var line = d3.svg.line()
    .x(function(d, i) { return x_trans(i); })
    .y(function(d, i) { return y_trans(d[yAttr]);;})
	.interpolate("basis");
	;
	
var path = svg.append("g")
	    .attr("clip-path","all")
	  .append("path")
	    .datum(data_)
	    .attr("d", line)
		.style("fill", "none")
		.style("stroke",color_)
		.style("stroke-width",3);
	//	.style("visibility", show);	
	return path;

}

 
}


function createScatterchart(data_o,parentNodeID,flag,chartOption){
	
	
	var color = d3.scale.category10().domain(d3.range(0,10));
	//color.domain([0, 10]);

	var margin = {top: 40, right: 70, bottom: 80, left: 70},
    width = chartOption.width - margin.left - margin.right,
    height = chartOption.height - margin.top - margin.bottom;
	
	var x_trans = d3.scale.linear()
    .domain([0, 780 ])
    .range([0, width]);
 
	var y_trans = d3.scale.linear()
	    .domain([0, 1])
	    .range([height, 0]);
		
	var xAxis = d3.svg.axis()
    .scale(x_trans)
    .orient("bottom");

	var yAxis = d3.svg.axis()
    .scale(y_trans)
    .orient("left")
    .ticks(10, "d");
	
	 if(chartOption.type == 'MPR_over_TotalPeriod'){
		data_=data_o.patientData;
		xAttr= 'totalPeriod';
		yAttr= 'avgMPR';
		xLabel = chartOption.xLabel;
		yLabel = chartOption.yLabel;
		dataID = data_o.name;
		color_ = data_o.color;
		
	} else 	return ;
	
	if(flag=='filter') {
		console.log("#"+parentNodeID+"_svg"+" g"); 
		var svg = d3.select("#"+parentNodeID+"_svg"+" g");
		
		if(Filter.MPRFilter.enabled) {
			var filtermin = Filter.MPRFilter.minValue;
			var filtermax = Filter.MPRFilter.maxValue;
			var minY = y_trans(filtermin);
			var maxY = y_trans(filtermax);
			
/*			var circles = svg.selectAll("circle");
			console.log(circles.length);
			for(var i=0;i<circles.length;i++)
			{
				if(circles[i].cy <=minY && circles.cy >=maxY ) circles[i].fill = Filter.color;
			}*/
			svg.selectAll("circle").style("fill",function(d,i) { 
			
				if(d[0]>=filtermin && d[0]<=filtermax) {
					return Filter.color;
				}//
				//return '#E6E6FA';
				return svg.select("#dot"+i).style("fill");
			});
						
		}
		/*var line = d3.svg.line()
 		   .x(function(d, i) { return x_trans(i); })
		    .y(function(d, i) { return y_trans(d);;})
			.interpolate("basis");
 		console.log(dataID);
		var path = svg.append("g")
		    .attr("clip-path",dataID)
		  .append("path")
		    .datum(data_)
		    .attr("d", line)
			.style("fill", "none") //chance.integer({min: 0, max: 10})
			.style("stroke",color(dataID))
			.style("stroke-width",3);*/
		
	
		
		
	} else {
	
	var svg = d3.select("#"+parentNodeID).append("svg")
	    .attr("width", width+ margin.left + margin.right )
	    .attr("height", height + margin.top + margin.bottom)
		.attr("id", parentNodeID+"_svg")
	  .append("g")
	    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
 
	svg.append("defs").append("clipPath")
	    .attr("id", "clip")
	  .append("rect")
	    .attr("width", width)
	    .attr("height", height);
		
	svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .style("fill","rgb(184, 184, 200)")
      .call(xAxis)
  .append("text")     
      .attr("y",60)
	  .attr("x",width/2-100)
      .style("text-anchor", "center")	
	  .style("fill","goldenrod") 
      .text(xLabel);
	 
	svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)
	  .style("fill","rgb(184, 184, 200)")
    .append("text")
      //.attr("transform", "rotate(-90)")
      .attr("y",-30)
	  .attr("x",0)
      .attr("dy", ".71em")
      .style("text-anchor", "start")	
	  .style("fill","goldenrod") 
      .text(yLabel); 
	  console.log(xAttr);
	  console.log(yAttr);
	console.log(data_);
 svg.selectAll(".dot")
      .data(data_)
    .enter().append("circle")
     // .attr("class", "dot")
      .attr("r", 3.5)
      .attr("cx",function(d, i) { return x_trans(d[xAttr]); })
      .attr("cy",function(d, i) { return y_trans(d[yAttr]); })
	  .attr("id",function(d,i) { return "dot"+i;})
      .style("fill", '#E6E6FA'); 
	

	}	

 
}

