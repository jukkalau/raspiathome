<!DOCTYPE html>                 <!-- This is an HTML5 file -->
<html>                          <!-- The root element -->
<head>                          <!-- Title, scripts & styles go here -->
<title>Digital Clock</title>
<meta http-equiv="refresh" content="60" > 
<meta http-equiv="content-type" content="text/html; charset=utf-8" /> 
<meta name="Language" content="fi">
<script>                        // A script of js code
// Define a function to display the current time
function displayTime() {
    var elt = document.getElementById("clock");  // Find element with id="clock"
    var now = new Date();                        // Get current time
    elt.innerHTML = now.toLocaleTimeString();    // Make elt display it
    setTimeout(displayTime, 1000);               // Run again in 1 second
}
window.onload = displayTime;  // Start displaying the time when document loads.
</script>
<style>                         /* A CSS stylesheet for the clock */
#clock {                        /* Style apply to element with id="clock" */
  font: bold 90pt sans;         /* Use a big bold font */
  background: #ddf;             /* On a light bluish-gray background */
  padding: 5px;                /* Surround it with some space */
  border: solid black 2px;      /* And a solid black border */
  border-radius: 10px;          /* Round the corners (where supported) */
}
#temp {                        /* Style apply to element with id="temp" */
  font: bold 42pt sans;         /* Use a big bold font */
  background: #ddf;             /* On a light bluish-gray background */
  padding: 5px;                /* Surround it with some space */
  border: solid black 2px;      /* And a solid black border */
  border-radius: 10px;          /* Round the corners (where supported) */
}

</style>
</head>
<body>                    <!-- The body is the displayed parts of the doc. -->
<!--
<br>
<span id="clock"></span>  <!-- The time gets inserted here -->
<br>

<br>
<span id="temp">
<?php
$myFile = "temp/last_tempBB.txt";
$fh = fopen($myFile, 'r');
echo date ("d.m H:i ", filemtime($myFile));
$theData = fread($fh, 45);
fclose($fh);
echo $theData;
?>
</span>
<br>
<br>
<span id="temp">
<?php
$myFile = "temp/last_tempCC.txt";
$fh = fopen($myFile, 'r');
echo date ("d.m H:i ", filemtime($myFile));
$theData = fread($fh, 45);
fclose($fh);
echo $theData;
?>
</span>
<br>
<br>
<span id="temp">
<?php
$myFile = "temp/last_tempDD.txt";
$fh = fopen($myFile, 'r');
echo date ("d.m H:i ", filemtime($myFile));
$theData = fread($fh, 45);
fclose($fh);
echo $theData;
?>
</span>

<br>
<br>
<h2>Edellinen vuorokausi ulkona</h2>
<br>
<img src="temp/m.png">

<h2>Edellinen vuorokausi LTO</h2>
<br>
<img src="temp/m_CC.png">

<h2>Edellinen vuorokausi alakerta</h2>
<br>
<img src="temp/m_DD.png">


<h2>Edellinen viikko</h2>
<br>
<img src="temp/7_days.png">
<br>
<img src="monitor/ping-stats.jpg">
</body>
</html>
