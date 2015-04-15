

<?php

$RandomMPRData="[";
$RandomPeriodData="[";
for($i=0;$i<1000;$i++){
	if($i!=0) 
	{
		$RandomMPRData .=" , ";		
		$RandomPeriodData .= " , ";
	}
	$randomval =  rand() / getrandmax(); //[0,1]
	$RandomMPRData .= ' [ ' . $randomval . ' , ' . rand(60,720) . ' ] ';
	$RandomPeriodData .= rand(60,720);
}
$RandomMPRData .=" ]";
$RandomPeriodData .=" ]";

$RandomMPRoverTimeData = "[";
for($i=0;$i<100;$i++){
	if($i!=0) 
	{
		$RandomMPRoverTimeData .=" , ";		
	}
	$randomval =  rand() / getrandmax(); //[0,1]
	$RandomMPRoverTimeData .= $randomval;
}
$RandomMPRoverTimeData .=" ]";

$RandomData = '{ "MPRALL" : ' . $RandomMPRData . ' , "MPRvTime" : ' . $RandomMPRoverTimeData . ' , "Period" : ' . $RandomPeriodData . ' }';


echo "<script>\n";
echo "function GetRandomMPRData() {  return ";
//echo $RandomMPRData . "; }" ;
echo $RandomData . "; }" ;
echo "\n</script>";			

?>
<!doctype html>
<html>
<script src="/lib/jquery-2.1.1.js"></script>
<script src="/lib/viz/lib/d3.v3.js" charset="utf-8"></script>
<script src="/lib/chance.js" charset="utf-8"></script>
<script src="./pills.js"></script>
<head>
<meta charset="utf-8">
<title>Pills v0.2 - Visualization of Drug Prescription Patterns </title>
<link href="pills.css" rel="stylesheet" type="text/css">
<!--The following script tag downloads a font from the Adobe Edge Web Fonts server for use within the web page. We recommend that you do not modify it.-->
<script>var __adobewebfontsappname__="dreamweaver"</script>
<script src="http://use.edgefonts.net/days-one:n4:default;holtwood-one-sc:n4:default.js" type="text/javascript"></script>

</head>

<body>
   <div class="leftcontrolCSS" id="leftcontrol">
      <div class="headingCSS"> General Properties</div>
      <div class="managingCSS">
        <form method="post">
        <fieldset>
                <legend><b>Measures</b></legend>
                <br>
                        <input type="checkbox" name="a" value="aa" />MPR(Medication Possession Rate) <br />
                        <input type="checkbox" name="b" value="bb" />CSA(Continuous single-interval medication availability)<br />
                        <input type="checkbox" name="c" value="cc" />CMG (continuous multiple-interval medication gaps)<br />
                       
        </fieldset>
	</form>
      <form method="post">
        <fieldset>
                <legend><b>Drugs</b></legend>
                <br>
                        <input type="checkbox" name="a" value="aa" />ABC <br />
                        <input type="checkbox" name="b" value="bb" />DEF<br />
                        <input type="checkbox" name="c" value="cc" />OPP (continuous multiple-interval medication gaps)<br />
                       
        </fieldset>
	</form>
        <p>&nbsp;</p>
        <p>&nbsp;</p>
      </div>
      <div class="headingCSS"> Data Setting</div>
      <div class="managingCSS"> 
       <form method="post">
        <fieldset>
                <legend><b>Data Source</b></legend>
                <br>
                        <input type="checkbox" name="a" value="aa" />Dataset name 1 (loaded)<br />
                        <input type="checkbox" name="b" value="bb" />Dataset name 2 (loaded)<br />
                        <input type="checkbox" name="c" value="cc" />Import a new dataset<br />
                       
        </fieldset>
	</form>

     <form method="post">
        <fieldset>
                <legend><b>Preprocessing</b></legend>
                <br>
                        <input type="checkbox" name="a" value="aa" />Using raw data<br />
                        <input type="checkbox" name="b" value="bb" />Preprocessing preset A<br />
                        <input type="checkbox" name="c" value="cc" />Preprocessign preset B <br />
                        <input type="checkbox" name="c" value="cc" />Create a new preprocessing prest<br />
                       
        </fieldset>
	</form>
       </div>
      <div class="headingCSS"> Gap and Overlap</div>
      <div class="managingCSS"> 
       <form method="post">
        <fieldset>
                <legend><b>Smooth Gaps</b></legend>
                <br>
                        <input type="checkbox" name="a" value="aa" />Enabled<br />
                        Options
               
                       
        </fieldset>
	</form>
     <form method="post">
        <fieldset>
                <legend><b>Smooth Overlaps </b></legend>
                <br>
                        <input type="checkbox" name="a" value="aa" />Enabled<br />
						Options
                       
        </fieldset>
	</form>
      </div>      

   </div>
<div class="middleviewCSS" id="middleview">
<div class="middleheadingCSS" id="middleHeading">
MPR
</div>
   <div class="GraphViewCSS" id="GraphView"  ></div>
   <div class="GraphViewCSS" id="GraphView_Time"  ></div>
   <div class="GraphViewCSS" id="GraphView_Period"  ></div>
   </div>
<div class="rightcontrolCSS" id="rightcontrol">
  <div class="headingCSS" > Data Group</div>
  
      <div class="managingCSS" id="groups">
     
      
      </div>
      </div>

</div>
  
 

</div>
	
  <script>
  var g_ranData = GetRandomMPRData();

  var d_rangenfrequency = ParseData_MPRRange(g_ranData.MPRALL);
  var d_mprovertime = GetData_MPR_over_TIME(null);
  var o_chartoption = createChartOption(1000,400,"Time","MPR");
 
 createbarChart(1000,400,d_rangenfrequency,"GraphView");
 createLinechart(d_mprovertime,"GraphView_Time",'new','all',o_chartoption);
 o_chartoption.xLabel="Period";
 //createLinechart(d_mprovertime,"GraphView_Period",'new','all',o_chartoption);

 createScatterchart(g_ranData.MPRALL,"GraphView_Period", 'new','all',o_chartoption);
;
 function AddGrouptoUI(groupname,color,filter) {
	 var grouproot = document.getElementById('groups');
	 var div_ = document.createElement("div");
	 var div_child = document.createElement("div");
	 var div_child2 = document.createElement("div");
	 div_.className = 'GroupItemCSS';
	 div_child.className = 'GroupNameCSS';
	 div_child.innerHTML = groupname;
	 div_child.style.background=color;
	 div_.appendChild(div_child);
	 	 div_.appendChild(div_child2);
	 div_child2.innerHTML = filter.MPRFilter.minValue + " <= MPR Range <= " +filter.MPRFilter.maxValue;
	 grouproot.appendChild(div_);
 }
  </script>
</body>
</html>