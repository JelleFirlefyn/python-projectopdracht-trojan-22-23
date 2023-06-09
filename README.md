# Python Projectopdracht Trojan 22-23

## Documentation

This Python script makes use of a GitHub repository that you will need to create yourself. This repository has to contain a JSON file. This JSON file will be used to configure which modules you want the script to execute. When changing to different modules the script will remotely change it functionality.

### Data storage
You also need to set up your own FTP server. This FTP server is used for receiving all data retrieved from the infected PC. The reason for using a FTP server is because the infected PC does not have any requirements or is not OS bound to send data to this server. (There are multiple services that offer free FTP servers)

To make use of this script you will need to clone this repository and add a .env file.  
This .env file has to contain these variables:
```
    ftp-host=<ftp-server-ip>
    ftp-port=<ftp-server-port>
    ftp-user=<ftp-server-user>
    ftp-password=<ftp-server-user-password>
    repo=<remote-github-repository>
    config-file=<config-file-inside-repo>
```

The script will periodically run every hour. To stop the script add `stop` to the JSON config file.

On execution of the script, the system information of the host will be send to the FTP server.

#### Alternative way of data storage
You can also use a GitHub repository to store the infected host's data. To use this functionality you will have to uncomment the code at the bottom of the **send_file.py** file, and comment the function at the top of the file. You will also need to add a variable called `data_repo_url` to your .env file. The value of this variable should be the .git link to an empty GitHub repository.

## Modules

The script currently contains these functionalities:  

| Name          | Functionality |
| ------------- |:-------------:|
| mod_keylogger      | Registers keystrokes for a set duration and logs these keystrokes in a .txt file to the FTP server. *(Duration can be changed in **main.py**)*     |
| mod_chromepasswords      | Retrieves all saved Chrome passwords and sends these in JSON file to FTP server. *(Only works in case these are not locked)*     |
| mod_rdp     | Enables RDP on the infected host.    |
| mod_screenshot      | Makes screenshot and sends this screenshot to FTP server.     |
| mod_systeminfo      | Retrieves all system information. *(Can also retrieve open ports by uncommenting the correct code in **sysinfo.py**)*     |
| mod_wifipasswords      | Retrieves all Wi-Fi passwords saved on the host and sends this JSON file to FTP server.      |
| mod_downloadexecute      | Executes code stored on another repository. This function needs 2 parameters to work: `repository_url` - the API url to the repository & `file_path` the location and name of the file inside the repository      |
| stop      | Stop the execution of this script      |

##### Example of config file: 
```
{
    "mod_downloadexecute": {
        "parameters": {
            "repository_url": "https://api.github.com/repos/JelleFirlefyn/remote-control",
            "file_path": "/test.py"
        }
    },
    "mod_screenshot": {}
}
```

## Remote control

To use these modules in your script by controlling them with the remote repository you will have to create a new **GitHub** repository.  
This repository will have to contain a JSON file. The name of the JSON file you can choose yourself, but remember to add the correct filename to your .env file.

##### Example: 
[The repository I used](https://github.com/JelleFirlefyn/remote-control).