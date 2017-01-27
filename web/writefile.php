<!DOCTYPE html>
<html>
<body>



<?php

if(isset($_GET['command']) && $_GET['command']== webtest)
{
    // echo $_GET['command'];

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

?>


