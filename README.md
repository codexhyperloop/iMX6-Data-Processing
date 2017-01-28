# iMX6-Data-Processing
Python code primarily to be used in the Team Codex Hyperloop Pod.

The program pulls receives data from the MCU (SAM3X8E processor) via serial connections and writes that data to JSON files.

The JSON data is to be read and displayed on a web page. 
The current setup has it being viewed from a Freeboard.io dashboard, but will eventually use https://github.com/codexhyperloop/iMX6-Web-Services

The setup is covered within the "setup" folder and consists of an Installation file and an Install.sh bash script to be used on apt based Linux distributions, UDOObuntu in this case.

## Full Installation.txt
1/17/17 // UDOO Quad Installation

// Updated 1/27/16

// When setting up an UDOO Quad for the first time (Fresh Installation)

// Change port of UDOO Web Control Panel ***IMPORTANT***
// The port needs to be changed before Apache can be installed properly
1. Point web browser to "localhost" (UDOO Web Dashboard should be displayed)
2. Go to "Configuration" -> "Advanced Settings" on the Dashboard
3. Change the port from Port 80 to 81
4. The UDOO may need to be rebooted for changes to take effect
5. To reach this dashboard again, type "localhost:81" in the UDOO browser
   OR: remotely by typing the UDOO IP address followed by ":81" on a remote PC browser


// After the Dashboard port has been changed
Run the "Install.sh" bash script (a "Pushbutton" installation)
This cand be done via LXTerminal on Quad by:
1. using the "cd" command to navigate to the folder containing "Install.sh"
2. typing "sudo ./Install.sh" into the terminal
The script may take time to install everything


// After the "Install.sh" script has been run
1. Type "sudo nano /etc/fstab" in Terminal
	(this opens fstab in the "nano" text editor)
2. Copy contents of "fstabEdit" file into fstab in the terminal
	Should be able to opeb fstabEdit in GUI, "copy" contents, and "paste" into the Terminal
// The line below is the same as in "fstabEdit" for convenience
bindfs#/var/www/html /home/udooer/hyperloop fuse force-user=udooer,force-group=udooer,create-for-user=www-data,create-for-group=www-data,create-with-perms=0770,chgrp-ignore,chown-ignore,chmod-ignore 0 0

3. Press [Ctrl]+[x] to exit "fstab", when asked to save type "y" and then [Enter]

// The above setup should mount /var/www/html to /home/udooer/hyperloop/web on UDOObuntu startup
// Use following command to mount /var/www/html to /home/udooer/hyperloop/web if not mounted on boot
sudo mount /home/udooer/hyperloop/web

// After all of the above is set up and working
1. Place Python code in /home/udooer/hyperloop (Found at https://github.com/codexhyperloop/iMX6-Data-Processing)
//DISCARD - 2. Place Web code in /home/udooer/hyperloop/web (Found at https://github.com/codexhyperloop/iMX6-Web-Services)
2. Place Web code in /home/udooer/hyperloop/web from the same Data-Processing repo

(Note: that files placed in /home/udooer/hyperloop/web SHOULD automatically be placed in /var/www/html via the above bindfs setup)

// Controlling the Pod
1. Navigate to the Pod dashboard by typing "[UDOO IP Address]/freeboard" into web browser of remote PC
2. Start Python Program
	a. Use "RealVNC Viewer" to connect to UDOO IP Address
	b. Start Python program from /home/udooer/hyperloop folder
