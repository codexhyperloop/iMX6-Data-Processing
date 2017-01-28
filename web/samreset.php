<!DOCTYPE html>
<html>
<body>



<?php

$old_path = getcwd();
chdir('/home/pi/Hyperloop/setup');
$output = shell_exec('./Sam3X8Ereset.sh');
chdir($old_path);

?>


