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

Note that the program will create a small .pkl file while running which is used to hold the data between each execution. It will be deleted automatically after the final run.

Note if a report fails it is probably a problem with the '1 of 1 hosts processed' field. The tools uses the second number (of x) number to multiple the date field and add it back to the dataframe. If that is incorrect the new column is the wrong length so the operation fails.

![report](/report.png)

You'll need to look through the failing reports and check if the quantity of VMs on that day matches the second number. You'll then need to manually edit the HTML of the second number which is relatively easy. The HTML class tag that is used for that field is "jobDescription".

