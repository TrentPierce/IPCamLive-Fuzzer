# IPCamLive-Fuzzer
## This python program tries a brute force method of fuzzing the DES hash and appending that to the default URL in an attempt to find unsecured IP cameras.

I created this program to find unsecured public facing IP cameras from https://www.ipcamlive.com/ in order to add them to a map for a weather project. This project was intended to provide local views of weather events from video sources that were not commonly known. A small delay was added between searches to prevent hitting the rate limits. 

**Installation:**

- Download the zip file of this code and extract it to a folder.
- Open CMD or PowerShell and navigate to the folder that you have extracted this program into.
- In CMD or Powershell type ''' python camscan.py '''
