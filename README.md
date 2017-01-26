# iMX6-Data-Processing
Python code primarily to be used in the Team Codex Hyperloop Pod.

The program pulls receives data from the MCU (SAM3X8E processor) via serial connections and writes that data to JSON files.

The JSON data is to be read and displayed on a web page. 
The current setup has it being viewed from a Freeboard.io dashboard, but will eventually use https://github.com/codexhyperloop/iMX6-Web-Services

The setup is covered within the "setup" folder and consists of an Installation file and an Install.sh bash script to be used on apt based Linux distributions, UDOObuntu in this case.
