// JavaScript Document
  var group_numberofGroups=0;
  var GroupList=[];
  
  
function renewData() {
	console.log('attemping renew data\n');

    console.log(	$( ".GraphViewCSS" ));
    $( ".GraphViewCSS" ).remove();		
		
	initialize()
	//.remove(this);
	
	
}
function Interact_createMPRRangeGroup(mprmin,mprmax){
	var range = {min:mprmin , max:mprmax};
	new_group = createPatientGroup("MPRGroup ("+ range.min + " < MPR <="+range.max+")",g_colorPal(group_numberofGroups));			
	new_group = constructInitData(new_group,"MPRrange",range);
		


//		AddGrouptoUI(groupname,color,filter)
	AddGrouptoUI(new_group.name,new_group.color,null,new_group.size);

	//update group to each visualization

		updateAllChart(new_group);		 
	return new_group;
}
function Quick_createGroupByAge() {
	var ageRange = [ {min:0 , max:20}, {min:21,max:40}];
	
	for(var i=0;i<ageRange.length;i++)
	{
		
		var range = ageRange[i];	
	//form patient group for each drug
		new_group = createPatientGroup("AgeGroup ("+ range.min + " <= age <="+range.max+")",g_colorPal(group_numberofGroups));			
		new_group = constructInitData(new_group,"age",range);
		


//		AddGrouptoUI(groupname,color,filter)
		AddGrouptoUI(new_group.name,new_group.color,null,new_group.size);

	//update group to each visualization

		updateAllChart(new_group);		 
	}
	
}
function Quick_createGroupByGender() {
	var genderL = ["male","female"];
	var idx=0;
	for(var gen in genderL){		

		
	//form patient group for each drug
		new_group = createPatientGroup("GenderGroup (gender="+gen+")",g_colorPal(group_numberofGroups));			
		new_group = constructInitData(new_group,"gender",idx);
		

//		AddGrouptoUI(groupname,color,filter)
		AddGrouptoUI(new_group.name,new_group.color,null,new_group.size);

	//update group to each visualization

		updateAllChart(new_group);		 
		idx++;
		
	}
}
function Quick_createGroupByDrug() {
	//create comprehensive groups with different drugs. ( dual/triple Therapy is not considered)

	var drugNameList =[];
	//get the list of drug
	var new_group;
	
	for(var drug in g_rawdata.drugs){
		var drugname = String(drug);

		
	//form patient group for each drug
		new_group = createPatientGroup("DrugGroup (drugID="+drugname+")",g_colorPal(group_numberofGroups));			
		new_group = constructInitData(new_group,"drug_id",drugname);
		

//		AddGrouptoUI(groupname,color,filter)
		AddGrouptoUI(new_group.name,new_group.color,null,new_group.size);


	//update group to each visualization

		updateAllChart(new_group);		 
		
	}

}
function updateAllChart(new_group){
	
	var o_chartoption = createChartOption(w_view,400,"MPR","# of Patients",'MPR_DIST');
		 createbarChart(new_group,"Chart_Bar_MPR_DISTRIBUTION", 'appendGroup',o_chartoption); 
		 
		 o_chartoption = createChartOption(w_view,400,"Time (Months from the start of medication) ","MPR",'MPR_over_MONTH');		
		 createLinechart(new_group,"Chart_Line_MPR_overMONTH",'appendGroup',o_chartoption);
		 
		  var o_chartoption = createChartOption(w_view,400,"Total Medication Period(Days)","MPR","MPR_over_TotalPeriod");
		 createScatterchart(new_group,"Chart_Scatter_MPR_overMONTH", 'appendGroup',o_chartoption);
}
 function AddGrouptoUI(groupname,color,filter,size) {
	 var grouproot = document.getElementById('groups');
	 var div_ = document.createElement("div");
	 var div_child = document.createElement("div");
	 var div_child2 = document.createElement("div");
	 div_.className = 'GroupItemCSS';
	 div_child.className = 'GroupNameCSS';
	 if(size!=null) {
		 div_child.style.width = (parseInt(size)+"%");
	 }
//	 div_child.innerHTML = "-";
	div_child.style.height = "30px";
	 div_.innerHTML = groupname;
	 div_child.style.background=color;
	 div_.appendChild(div_child);
	 	 div_.appendChild(div_child2);
	// div_child2.innerHTML = filter.MPRFilter.minValue + " <= "+filter.filterMeasure + " <= " +filter.MPRFilter.maxValue;
	 grouproot.appendChild(div_);
 }
function Group_CreateGroup(patientIDs,filter) {
	//TODO create group list
	//TODO Add visual element to each chart	
	if(filter.MPRFilter.enabled) {
	
	 var d_mprovertime = GetData_MPR_over_TIME(null);
	 var o_chartoption = createChartOption("100%","auto","none","none");
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
   

function createbarChart(data_o,parentNodeID,flag, cOption) {
	var margin = {top: 40, right: 70, bottom: 80, left: 70},
	 width = cOption.width - margin.left - margin.right,
    height = cOption.height - margin.top - margin.bottom;


	if(cOption.type == 'MPR_DIST') {
		
		data_=data_o.stats.mprRange;
		xAttr= 'range';
		yAttr= 'count';
		xLabel = cOption.xLabel;
		yLabel = cOption.yLabel;
			
	} else if(cOption.type == 'CSA_DIST'){
		
		data_=data_o.stats.csaRange;
		xAttr= 'range';
		yAttr= 'count';
		xLabel = cOption.xLabel;
		yLabel = cOption.yLabel;
		
	} else if(cOption.type == 'CMG_DIST'){
		
		data_=data_o.stats.cmgRange;
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
	
	var grouping_type = "stack-up";
	
	if(flag=='appendGroup') {

		if(grouping_type == "split" ) {
			var svgg =document.getElementById(parentNodeID+"_svg");		
			svgg = svgg.getElementsByTagName('g');
			svgg=svgg[0];
	
			maxFrequency = parseInt(svgg.getAttribute('maxFrequency'));
			
			
			
	
			x.domain(data_.map(function(d) {  return d[xAttr]; }));
			
			y.domain([0,maxFrequency+10]);
				  
		  	svg = d3.select("#"+parentNodeID+"_svg"+" g");
			
	
			svg = svg.append("g")
				//    .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
					//.attr("groupID",data_.id);
					.attr("id",parentNodeID+"_svg"+"_group"+data_o.id)
					.attr("groupID","group"+data_o.id);
					
	 	    svg.selectAll(".bar")
	 	       .data(data_)
		    .enter().append("rect")
	    	  .attr("class", "bardefault")
			  .style("fill",data_o.color)
		      .attr("x", function(d) { return (x(d[xAttr])).toFixed(0);+(parseInt(data_o.id)-2)*x.rangeBand()/2; })
		      .attr("id", function(d) { return "bar"+d[xAttr]; })
		      .attr("width", x.rangeBand()/2)
		      .attr("y", function(d) { return (y(d[yAttr])).toFixed(0);; })
    		  .attr("height", function(d) {	  return height - (y(d[yAttr])).toFixed(0);; })	; 
	
	
		} else if (grouping_type == "stack-up") {
		
			var svgg =document.getElementById(parentNodeID+"_svg");		
			svgg = svgg.getElementsByTagName('g');
			svgg=svgg[0];
			maxFrequency = parseInt(svgg.getAttribute('maxFrequency'));
	
						//retrieve the last bars' heights
			var LastGroupID = "group"+(data_o.id-1);
			var lastgroup_DOM =svgg.querySelector('#'+(parentNodeID+"_svg_"+LastGroupID));
			console.log(svgg);
			console.log('[groupID="'+LastGroupID+'"]');
			console.log(lastgroup_DOM);
			var lastArrayRect = lastgroup_DOM.getElementsByTagName('rect');
			console.log(lastArrayRect);
			console.log(lastArrayRect.length);
			

			x.domain(data_.map(function(d) {  return d[xAttr]; }));
			
			y.domain([0,maxFrequency+10]);

			var lastY = [];
			if(data_o.id>2) {
				for(i=0;i<lastArrayRect.length;i++)
				{
					lastY[i] = y(0) - lastArrayRect[i].getAttribute('y');
				}				
			} else {
				for(i=0;i<lastArrayRect.length;i++)
				{
					lastY[i] = 0;
				}
			}

						console.log(lastY);				  
		  	svg = d3.select("#"+parentNodeID+"_svg"+" g");

				svg = svg.append("g")
				//    .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
					//.attr("groupID",data_.id);
					.attr("id",parentNodeID+"_svg"+"_group"+data_o.id)
					.attr("groupID","group"+data_o.id);
		
	 	    svg.selectAll(".bar")
	 	       .data(data_)
		    .enter().append("rect")
	    	  .attr("class", "bardefault")
			  .style("fill",data_o.color)
		      .attr("x", function(d) { return (x(d[xAttr])).toFixed(0);+(parseInt(data_o.id)-2)*x.rangeBand()/2; })
		      .attr("id", function(d) { return "bar"+d[xAttr]; })
		      .attr("width", x.rangeBand())
		      .attr("y", function(d,i) { 	   
				  return (y(d[yAttr])).toFixed(0) - lastY[i];; 
				  })
    		  .attr("height", function(d) {	  return height - (y(d[yAttr])).toFixed(0);; })	; 
			
	}
		
	} else {
		
		maxFrequency=0;
	  x.domain(data_.map(function(d) { 
  if(d[yAttr]>maxFrequency) maxFrequency=d[yAttr];
  return d[xAttr]; }));
  y.domain([0,maxFrequency+10]);
var svg = d3.select("#"+parentNodeID).append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
	.attr("id", parentNodeID+"_svg")
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
	.attr("measure",xLabel)
	.attr("maxFrequency",maxFrequency)
	.attr("barWidth",x.rangeBand());

var brush = d3.svg.brush()
      .x(x)
      .y(y)
      .on("brushstart", brushstart)
      .on("brush", brushmove)
      .on("brushend", brushend);
	  
//var data=[{"letter":"A","frequency" : 0.1},{"letter":"B","frequency" : 0.2},{"letter":"C","frequency" : 0.3}];

var maxFrequency=0;
  	

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
	  
var groupRoot = svg.append("g")		
				.attr("id",parentNodeID+"_svg"+"_group"+data_o.id)
				.attr("groupID","group"+data_o.id);
				
  groupRoot.selectAll(".bar")
      .data(data_)
    .enter().append("rect")
      .attr("class", "bardefault")
      .attr("x", function(d) { return (x(d[xAttr])).toFixed(0); })
      .attr("id", function(d) { return "bar"+d[xAttr]; })
      .attr("width", x.rangeBand())
      .attr("y", function(d) { return (y(d[yAttr])).toFixed(0); })
      .attr("height", function(d) { return height - (y(d[yAttr])).toFixed(0);; })	;
	  
	svg.call(brush);	   
// Clear the previously-active brush, if any.
 function brushstart(p) {
   // if (brushCell !== this) {
   //   d3.select(brushCell).call(brush.clear());
    //  x.domain(domainByTrait[p.x]);
     // y.domain(domainByTrait[p.y]);
   //   brushCell = this;
 //   }
 		BarSelected=[];
  }

  // Highlight the selected circles.
  var BarSelected=[];
  var MprData = data_;
  function brushmove(p) {
    var e = brush.extent();
   // console.log(e[0][0] + "  " + e[1][0]);
   groupRoot.selectAll("rect").classed("barselected", function(d,i) {
   // svg.selectAll("rect").classed("barselected", function(d,i) {
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
	min_=1000;
	max_=-1;
	var mprwidth = MprData[1].range- MprData[0].range;
	for(i=0;i<BarSelected.length;i++){  //why -10? idk.
		if(BarSelected[i]>0) {
			if(MprData[i].range<min_) min_=MprData[i].range;
			if(MprData[i].range>max_) max_=MprData[i].range;
			
		}
		
	}
	if(min_ == 1000) return ;	
		
//	var newFilter = createFilterOption(true,(min_-mprwidth).toFixed(2),max_.toFixed(2),this.getAttribute("measure"));
	//if(min_==0) min_=-0.1;
	var group_ = Interact_createMPRRangeGroup(min_,max_);

	/*for(i=0;i<BarSelected.length-10;i++){
		if(BarSelected[i]>0) {
		//	console.log(svg);
			svg.selectAll('.barselected').style("fill", group_.color);
		}
	}*/
	
	svg.selectAll("rect").classed("barselected",false);
  }

function type(d) {
  d.frequency = +d.frequency;
  return d;
}
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
	
	if(flag=='appendGroup') {
		
		var svg = d3.select("#"+parentNodeID+"_svg"+" g");
		var line = d3.svg.line()
 		   .x(function(d, i) { return x_trans(i); })
		    .y(function(d, i) { return y_trans(d[yAttr]);;})
			.interpolate("basis");

		var path = svg.append("g")
		    .attr("clip-path",data_o.id)
			.attr("group","group"+data_o.id)
		  .append("path")
		    .datum(data_)
		    .attr("d", line)
			.style("fill", "none") //chance.integer({min: 0, max: 10})
			.style("stroke",data_o.color)
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
    .domain([0, 870 ])
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
	if(flag=="appendGroup"){
		
		var svg = d3.select("#"+parentNodeID+"_svg"+" g");
		svg = svg.append("g")		
				.attr("groupID","group"+data_o.id);
		svg.selectAll(".dot")
   		   .data(data_)
		   .enter().append("circle")
		      .attr("r", 3.5)
		      .attr("cx",function(d, i) { return x_trans(d[xAttr]); })
		      .attr("cy",function(d, i) { return y_trans(d[yAttr]); })
//			  .attr("id",function(d,i) { return "dot"+i;})
		      .style("fill", data_o.color); 
		
	} else 	if(flag=='filter') {
		
		var svg = d3.select("#"+parentNodeID+"_svg"+" g");
		
		if(Filter.MPRFilter.enabled) {
			var filtermin = Filter.MPRFilter.minValue;
			var filtermax = Filter.MPRFilter.maxValue;
			var minY = y_trans(filtermin);
			var maxY = y_trans(filtermax);			

			svg.selectAll("circle").style("fill",function(d,i) { 
			
				if(d[0]>=filtermin && d[0]<=filtermax) {
					return Filter.color;
				}//
			
				return svg.select("#dot"+i).style("fill");
			});
						
		}
		
		
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

