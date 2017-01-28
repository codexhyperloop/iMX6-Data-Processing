<!DOCTYPE html>
<html>
<body>



<?php

if(isset($_GET['threading']) && $_GET['threading']== yes)
{
	$file = fopen("threading.txt","w") or die("Unable to open file!");
	$txt = "true";
	fwrite($file,$txt);
	fclose($file);
}

if(isset($_GET['threading']) && $_GET['threading']== no)
{
    
	$file = fopen("threading.txt","w") or die("Unable to open file!");
	$txt = "false";
	fwrite($file,$txt);
	fclose($file); 
}

?>


