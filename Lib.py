from netmiko import ConnectHandler
import time, re
from time import gmtime, strftime
from jinja2 import Template
import json
import yaml
import argparse
import os



def configLog(config,Hostname):
    file_path = os.path.dirname(os.path.realpath(__file__))
    print(file_path)
    f = open(file_path + '\\Config\\' + Hostname + '.cfg', 'w+')   # old config will be removed. This config file will be pushed to device.
    f.write(config)
    f.write('\n\n')
    time.sleep(0.5)
    f.close()


def deviceLog(log):
    file_path = os.path.dirname(os.path.realpath(__file__))
    print(file_path)
    LocalTime= strftime("%d%m%Y", gmtime())
    f = open(file_path + '\\Log\\DeviceLog-' + LocalTime + '.txt', 'a')    # append log in the same file
    f.write(log)
    time.sleep(0.5)
    f.close()


def data_file(data):
    # automatic path for data file
    file_path = os.path.dirname(os.path.realpath(__file__))
    for i,j,k in os.walk(file_path):
        if data in k:
            d1 = i + '\\' + data
    # d1 = 'Template/'+d
    d2 = yaml.load(open(d1), Loader=yaml.FullLoader)   # Loader=yaml.Loader --> on Jump Server
    return d2


def TempG(temp, data):
    # automatic path for template file
    file_path = os.path.dirname(os.path.realpath(__file__))
    for i,j,k in os.walk(file_path):
        if temp in k:
            t = i + '\\' + temp
    # t = 'Template/' + temp
    f = open(t,'r')
    tem = f.read()
    #print ('temp')  # to verify template#

    d1 = {}  # define dic
    d1 = data_file(data)   # get json/yaml format data in d1. (class dict is returned)
    # find the no of variables in data file
    #print(d1)
    l = len(d1['data'])
    print('\nTotal devices = ' + str(l) + '\n\n')  # to verify number of inputs in data file (device to be configured)
    #print (d1['data'])

    for i in range(l):
        try:
            template = Template(tem)
            config = template.render(component=d1['data'][i])

            Hostname = d1['data'][i]['HOSTNAME']   # create config file with same name

            print ('\n\n' + Hostname + " Config Prepared as below -\n")
            print (config)
            # return config, Hostname
            configLog(config,Hostname)  # config & Hostname name is passed to create log file#
            time.sleep(0.5)

        except Exception as e:
            log = '\n {} \n'.format(str(e))
            deviceLog(log)
            print(log)


def ConfigP(HOSTNAME,login_details):

    print ('\nDevice to be configured= ' + login_details['ip'] + '\n')
    # push config on device and create log
    # net_connect = ConnectHandler(device_type=deviceType, ip=dip, username=username, password=pw, port=port)
    net_connect = ConnectHandler(**login_details)
    #output1 = net_connect.send_config_set(config)
    
    # get config file from Config folder
    file_path = os.path.dirname(os.path.realpath(__file__))
    print(file_path)
    config_file = file_path + '\\Config\\' + HOSTNAME + '.cfg'

    output1 = net_connect.send_config_from_file(config_file)
    time.sleep(5)
    output2 = net_connect.commit()
    time.sleep(4)
    output3 = net_connect.exit_config_mode()
    output4 = net_connect.disconnect()

    c = ('\n----'+login_details['ip']+'----\n'+'\n'+output1+output2+output3+'\n'+'\n---- END ----\n')
    print (c)
    deviceLog(c)
    time.sleep(1)

def net_con(HOSTNAME,login_details):
    try:
        net_ssh = ConnectHandler(**login_details)
        log = '\n**netmiko ssh connection {}\n'.format(HOSTNAME)
        print(log)
        deviceLog(log)
        return(net_ssh)
    except Exception as e:
        log = '\n**netmiko connection failed {}\n'.format(e)
        print(log)
        deviceLog(log)
