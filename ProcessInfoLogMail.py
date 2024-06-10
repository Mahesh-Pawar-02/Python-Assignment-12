# Problem Statement : Design automation script which accept directory name and mail id from user and create log 
# file in that directory which contains information of running processes as its name, PID, 
# Username. After creating log file send that log file to the specified mail.

import os
import psutil
import smtplib
import time
import urllib.error
import urllib.request
import sys
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

def is_connected():
    try:
        urllib.request.urlopen('https://www.google.co.in/',timeout = 1)
        return True
    except urllib.error as err:
        return False
    
def DisplayProcess():
    
    ProcessList = []
    
    for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_info', 'status']):
        try:
             ProcessList.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    return ProcessList
def MailSender(Email, Filename, time):
    try:
        fromaddr = "try.web.new@gmail.com"
        toaddr = Email

        msg = MIMEMultipart()

        msg['From'] = fromaddr
        msg['To'] = toaddr

        body = """
    Hello..!
    Greeting from Mahesh Pawar.
    Please find the attached document which contains Log of Running Process.
    Log File is created at : %s

    This is auto generated mail.

    Thanks and Regards,

    Mahesh Pawar
    RID : PM0100047
    +91 **********
    """ %(time)

        Subject = """
        Process Log generated at : %s
        """%(time)

        msg['Subject'] = Subject
        msg.attach(MIMEText(body,'plain'))
        attachment = open(Filename,"rb")
        p = MIMEBase('application','octet-stream')
        p.set_payload((attachment).read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', "attachment; filename = Process_Log.txt")
        
        msg.attach(p)
        s = smtplib.SMTP('smtp.gmail.com',587)
        s.starttls()
        s.login(fromaddr,"------------")
        text = msg.as_string()
        s.sendmail(fromaddr,toaddr,text)
        s.quit()

        print(f"Email sent to {Email} with the log file attached.")

    except Exception as E:
        print("Unable to send mail",E)

def LogFile(logDir, Email, Filename):
    if not os.path.exists(logDir):
        try:
            os.mkdir(logDir)
        except:
            pass
    
    LogPath = os.path.join(logDir,"Process_Log.txt")
    
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

    connected = is_connected()
    
    if connected:
        StartTime = time.time()
        MailSender(Email, LogPath,time.ctime())
        endTime = time.time()

        print("Took %s seconds to send email"%(endTime-StartTime))
    else:
        print("There is a no internet connection")

def main():
    print('-------------------------------------------------------------------')
    print("Created by Mahesh Pawar")
    print("Application name:" +sys.argv[0])
    print('-------------------------------------------------------------------')

    if (len(sys.argv) != 3):
        print("Error: Invalid number of arguments")
        print("Use -h option to get the help and use -u option to get the usage of application")
        exit()

    if (sys.argv[1] == "-h") or (sys.argv[1] == "-H"):
        print("This Script is used to get Log of Running Process")
        exit()

    if (sys.argv[1] == "-u") or (sys.argv[1] == "-U"): 
        print("usage: ApplicationName AbsolutePath_of_Directory Email_ID ")
        exit()

    directory = sys.argv[1]
    Email = sys.argv[2]

    LogFile(directory, Email , Filename = "Process_Log.txt")
    
if __name__ == "__main__":
    main()
