<!DOCTYPE html>
<html>
<body>



<?php

if(isset($_GET['command']) && $_GET['command']== webtest)
{

	$file = fopen("command.txt","w") or die("Unable to open file!");
	$txt = "webtest";
	fwrite($file,$txt);
	fclose($file);
}

else if(isset($_GET['command']) && $_GET['command']== stop)
{
    
	$file = fopen("command.txt","w") or die("Unable to open file!");
	$txt = "stop";
	fwrite($file,$txt);
	fclose($file); 
}

else if(isset($_GET['command']) && $_GET['command']== emergencystop)
{
    
	$file = fopen("command.txt","w") or die("Unable to open file!");
	$txt = "emergencystop";
	fwrite($file,$txt);
	fclose($file); 
}

else if(isset($_GET['command']) && $_GET['command']== start)
{
    
	$file = fopen("command.txt","w") or die("Unable to open file!");
	$txt = "start";
	fwrite($file,$txt);
	fclose($file); 
}

else if(isset($_GET['command']) && $_GET['command']== clear)
{
    
	$file = fopen("command.txt","w") or die("Unable to open file!");
	$txt = "";
	fwrite($file,$txt);
	fclose($file); 
}

else if(isset($_GET['command']) && $_GET['command']== pauseall)
{
    
	$file = fopen("command.txt","w") or die("Unable to open file!");
	$txt = "pauseall";
	fwrite($file,$txt);
	fclose($file); 
}

else if(isset($_GET['command']) && $_GET['command']== serialcheck)
{
    
	$file = fopen("command.txt","w") or die("Unable to open file!");
	$txt = "serialcheck";
	fwrite($file,$txt);
	fclose($file); 
}

else if(isset($_GET['command']) && $_GET['command']== systemtest)
{
    
	$file = fopen("command.txt","w") or die("Unable to open file!");
	$txt = "systemtest";
	fwrite($file,$txt);
	fclose($file); 
}

else if(isset($_GET['command']) && $_GET['command']== selftest)
{
    
	$file = fopen("command.txt","w") or die("Unable to open file!");
	$txt = "selftest";
	fwrite($file,$txt);
	fclose($file); 
}

else if(isset($_GET['command']) && $_GET['command']== exitprogram)
{
    
	$file = fopen("command.txt","w") or die("Unable to open file!");
	$txt = "exitprogram";
	fwrite($file,$txt);
	fclose($file); 
}

?>