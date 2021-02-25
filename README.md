## Veeam Session Report to xlsx

This program will turn a folder of Veeam session report information (html) into a single excel file.

Gathering session information for VM backups can be done via PowerShell; however, agent backups cannot be so this is the main intention of this program. 

However, there is no reason why it cannot be used VM backups as well. It hasn't been tested on NAS yet.

Packages required:

    pip install BeautifulSoup pandas numpy PySimpleGUI

Session reports can be created via:

![button](/sessio_button.png)

A pop up dialogue box will appear when run with:

    python session_report.py

Select the folder with the reports then press 'ok'.

Note that the program will create a small .pkl file while running which is used to hold the data between each execution. It will
be deleted automatically after the final run.

Note the program assumes that each run has the same quantity of hosts per-report, per-session. If there are more/less in one or more then
program may skip that report or the 'Date' column maybe skewed.