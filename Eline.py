from netmiko import ConnectHandler
import time
import Lib as Lib
import os
import yaml

def ELINE(temp, data):
    print(temp,data)

    # generate template
    l = Lib.TempG(temp,data)

    # get data from file
    d1 = Lib.data_file(data)

    # find total devices
    l = len(d1['data'])

    # get required parameters
    HOSTNAME=[];LOGIN=[];INTERFACE=[];VLAN=[];N=[]
    for i in range(l):
        HOSTNAME.append(d1['data'][i]['HOSTNAME'])
        LOGIN.append(d1['data'][i]['LOGIN'])
        INTERFACE.append(d1['data'][i]['interface'])
        VLAN.append(d1['data'][i]['vlan'])
        N.append(d1['data'][i]['n'])    # total number of service to be created
    print(HOSTNAME, LOGIN, INTERFACE, VLAN, N)
    print('\n\n')


    # Push config on the device // hash this code if config push is not required on the device //
    for i in range(l):
        Lib.ConfigP(HOSTNAME[i], LOGIN[i])

    
    # This is to execute show command // hash this code if show command not required //
    # netmiko ssh connection//ssh to all devices
    net_ssh=[]
    for i in range(l):
        net_ssh.append(Lib.net_con(HOSTNAME[i], LOGIN[i]))
    
    print(net_ssh)

    # verification/show command
    for i in range(l):
        try:
            for j in range(d1['data'][i]['n']):                
                output1= net_ssh[i].find_prompt()
                command= 'show l2vpn xconnect interface {}.{}'.format(INTERFACE[i],str((int(VLAN[i]+j))))
                output2= net_ssh[i].send_command_expect(command)
                log = '{}{}\n{}\n\n'.format(output1,command,output2)
                Lib.deviceLog(log)
                print(log)           
            print(net_ssh[i].disconnect())
            
        except Exception as e:
                log = '\n {} \n'.format(str(e))
                Lib.deviceLog(log)
                print(log)



# ELINE('eline.jinja','ar1-ar6-110.yml')
ELINE('eline_del.jinja','ar1-ar6-110.yml')