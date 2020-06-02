## noctionTraceroute
###### perform batch traceroutes in Noction platform via selenium
###### 1. Install Libraries
```
pip install selenium
pip install pandas
```
###### 2. You need [download the chromedriver](https://chromedriver.chromium.org/downloads) in this current folder 
###### 3. Put the destination IPs in DstIPList.txt
###### 4. Proceed noctionTraceroute.py
###### 5. Enter Noction Login account and password
###### 6. Every tab excute traceroute will take about 27 seconds, eg. 100 traceroutes may take 2700 seconds, or 45 minutes. If there is any occured error, please follow step 7 and 8.
###### 7. If the tabs are stop at the stauts without clicking "Trace" button, then just click it. After completing the traceroute in those tabs. The procees will continue.
###### 8. It has been kept around 5 minutes for the step 7 in every tab. If you don't perform the issue tabs, the program will stop in 5 minutes and TraceRouteCombined.xlsx won't appear. You need to excrat what you need in every tabs.
###### 9. All the csv files will be combined in TraceRouteCombined.xlsx
###### _Note:_ you can also convert the .py to .exe file by the following steps:###### - `pip install pyinstaller`
###### - Open PowerShell and excute `pyinstaller --onefile -w 'getTopTenSourceIP_V1_2.py'`



















