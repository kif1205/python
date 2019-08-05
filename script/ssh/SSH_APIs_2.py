import paramiko
import time
		
def SSH_Init(Test_IP,Test_Port,Test_UserName,Test_Password):

    global client
    global BMC_SSH_IP 
    global BMC_SSH_UserName
    global BMC_SSH_PassWord
    global BMC_SSH_Port

    BMC_SSH_IP = Test_IP
    BMC_SSH_Port = Test_Port
    BMC_SSH_UserName = Test_UserName
    BMC_SSH_PassWord = Test_Password
	
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  
    client.connect(BMC_SSH_IP, port=BMC_SSH_Port, username=BMC_SSH_UserName, password=BMC_SSH_PassWord)

def SSH_State():
    return client.get_transport().is_active()

def SSH_SendCommand(command,delay_second=0):

    if SSH_State() == False: 
        client.connect(BMC_SSH_IP, port=BMC_SSH_Port, username=BMC_SSH_UserName, password=BMC_SSH_PassWord)
		
    (stdin, stdout, stderr) = client.exec_command(command) 
    Command_return = stdout.readlines()	
	
    return Command_return

	
def SSH_Close():
    client.close()

def delays(seconds,delay_reason=""):
    print(delay_reason)
    while seconds >= 0:
        time.sleep(1)        
        second_str = "%d seconds...\r" %seconds
        print(second_str, end='')
        seconds -= 1
    #print("")
	
def SSH_FWVersion_BuildID():
    Temp_Result = SSH_SendCommand("cat /etc/os-release")
    for item in Temp_Result:
        if "BUILD_ID" in item:
            Command_return = item.split("=")  
            break      
    return Command_return[1]

def SSH_IPAddr_Eth0_IP():
    Temp_Result = SSH_SendCommand("/sbin/ip addr")
    for item in Temp_Result:
        if "global" in item:
            temp_string=item.split("/")
            Command_return=temp_string[0].split(" ")
            break      
    return Command_return[5]