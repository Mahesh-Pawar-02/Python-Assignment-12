# Design automation script which accept directory name from user and create log file in that directory which 
# contains information of running processes as its name, PID, Username. 

# Usage : ProcInfoLog.py Demo

import os
import psutil
import time
import sys
    
def DisplayProcess():
    
    ProcessList = []
    
    for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_info', 'status']):
        try:
             ProcessList.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    return ProcessList

def LogFile(logDir, Filename = "Process_Log.txt"):
    if not os.path.exists(logDir):
        try:
            os.mkdir(logDir)
        except:
            pass
    
    LogPath = os.path.join(logDir,Filename)
    
    ProcessInfo = DisplayProcess()

    with open(LogPath, 'w') as file:
        file.write("========================================\n")

        file.write("Welcome..! to Log File "+"\n")
        file.write("Log File created at : "+time.ctime()+"\n")
        file.write("========================================\n")
        file.write("Running Processes Log file contents are : " + "\n")
        file.write("========================================\n")
        for info in ProcessInfo:

            file.write(f"Process ID:       {info['pid']}\n")
            file.write(f"Process Name:     {info['name']}\n")
            file.write(f"Username:         {info['username']}\n")
            file.write(f"CPU Usage:        {info['cpu_percent']}%\n")
            file.write(f"Memory Usage:     RSS={info['memory_info'].rss}, VMS={info['memory_info'].vms}\n")
            file.write(f"Status:           {info['status']}\n")
            file.write("========================================\n\n")

        print("Log File is successfully generated at location : ",(LogPath))

def main():
    print('-------------------------------------------------------------------')
    print("Created by Mahesh Pawar")
    print("Application name:" +sys.argv[0])
    print('-------------------------------------------------------------------')

    if (len(sys.argv) != 2):
        print("Error: Invalid number of arguments")
        print("Use -h option to get the help and use -u option to get the usage of application")
        exit()

    if (sys.argv[1] == "-h") or (sys.argv[1] == "-H"):
        print("This Script is used to get Log of Running Process")
        exit()

    if (sys.argv[1] == "-u") or (sys.argv[1] == "-U"): 
        print("usage: ApplicationName AbsolutePath_of_Directory ")
        exit()

    directory = sys.argv[1]

    LogFile(directory, Filename = "Process_Log.txt")
    
if __name__ == "__main__":
    main()
