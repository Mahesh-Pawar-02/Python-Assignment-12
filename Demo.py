import os
import psutil
import smtplib
from email.message import EmailMessage
import sys
import time

def get_process_info():
    """
    Get information about all running processes.
    
    :return: List of dictionaries with process information.
    """
    process_info_list = []
    
    for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_info', 'status']):
        try:
            process_info_list.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    return process_info_list

def create_log_file(directory, log_filename="process_log.txt"):
    """
    Create a log file with information about all running processes in the specified directory.
    
    :param directory: Directory where the log file will be created.
    :param log_filename: Name of the log file.
    :return: Path to the created log file.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    log_filepath = os.path.join(directory, log_filename)
    
    process_info = get_process_info()
    
    with open(log_filepath, 'w') as file:
        for info in process_info:
            file.write("========================================\n")
            file.write(f"Process ID:       {info['pid']}\n")
            file.write(f"Process Name:     {info['name']}\n")
            file.write(f"Username:         {info['username']}\n")
            file.write(f"CPU Usage:        {info['cpu_percent']}%\n")
            file.write(f"Memory Usage:     RSS={info['memory_info'].rss}, VMS={info['memory_info'].vms}\n")
            file.write(f"Status:           {info['status']}\n")
            file.write("========================================\n\n")
    
    return log_filepath

def send_email(recipient_email, subject, body, attachment_path):
    """
    Send an email with an attachment.
    
    :param sender_email: Email address of the sender.
    :param recipient_email: Email address of the recipient.
    :param subject: Subject of the email.
    :param body: Body of the email.
    :param attachment_path: Path to the file to be attached.
    """
    msg = EmailMessage()
    
    msg.set_content(body)

    fromaddr = "try.web.new@gmail.com"
    toaddr = recipient_email

    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = subject
    
    with open(attachment_path, 'rb') as file:
        file_data = file.read()
        file_name = os.path.basename(file.name)
    
    msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)
    
    password = ("qvbp xnrv pbcb pxaf")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(fromaddr,password)
        smtp.send_message(msg)

def main():
    directory = sys.argv[1]
    recipient_email = sys.argv[2]

    log_filepath = create_log_file(directory)
    print(f"Log file created at: {log_filepath}")
    
    subject = "Running Processes Log"
    body = """
    Hello..!
    Greeting from Mahesh Pawar.
    Please find the attached document which contains information of running processes.
    Log File is created at : %s

    This is auto generated mail.

    Thanks and Regards,

    Mahesh Pawar
    RID : PM0100047
    +91 9322150275
    """ %(time.ctime)
    
    send_email(recipient_email, subject, body, log_filepath)
    print(f"Email sent to {recipient_email} with the log file attached.")

if __name__ == "__main__":
    main()
