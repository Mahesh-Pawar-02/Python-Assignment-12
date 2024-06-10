# Problem Statement : Design automation script which accept process name and display information of that process
# if it is running.

import psutil
import sys

def DisplayProcess(ProcessName):
    
    ProcessList = []
    
    for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_info', 'status']):
        try:
            if proc.info['name'].lower() == ProcessName.lower():
                ProcessList.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    return ProcessList

def main():
    ProcessName = sys.argv[1]
    ProcessInfo = DisplayProcess(ProcessName)
    
    if ProcessInfo:
        for info in ProcessInfo:

            separator = "-"*40
            print(separator)

            print("Process ID: ",      info['pid'])
            print("Process Name: ",    info['name'])
            print("Username:",         info['username'])
            print("CPU Usage:",        info['cpu_percent'],"%")
            print(f"Memory Usage:     RSS={info['memory_info'].rss}, VMS={info['memory_info'].vms}")
            print("Status:",           info['status'])

            print(separator)

    else:
        print(ProcessName,"This process currently not running.")

if __name__ == "__main__":
    main()