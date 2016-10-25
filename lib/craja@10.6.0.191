""" 
Testing TL1 Funtionality
"""
import socket
import time
import sys
import nose
import logging
import logging.config
from config import  get_config_arg

logging.config.fileConfig('logging.ini')
LOG = logging.getLogger('TL_ONE')

class TL_ONE:
    def __init__(self, ip, port=3082):
        """ Init Arguments:
            Arguments:
            ip        : IP address.
        """
        self.ip = ip
        self.port = port
        self.sock = None

    def create_socket(self):
        """
        open the tl1 session
        """
	try:
	    ### Logging into TL1 session using given credentials
            LOG.info("Creating socket <sock = %s:%s>\n" % (self.ip, self.port))
	    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.ip, self.port))
	    LOG.info("logging into switch\n")
            user_name = get_config_arg('login_credentials', 'user_name')
            password = get_config_arg('login_credentials', 'password')
	    self.sock.send('ACT-USER::%s:123::%s;' %(user_name, password))
	    sys.stdout.flush()
	    Login = self.sock.recv(3072)
	    nose.tools.assert_in('123 COMPLD', Login, 'getting error from switch : %s' %Login)
        except socket.error, e:
	    LOG.error("Failed to connect socket\n") 

    def close_socket(self):
        """
        close the tl1 session
        """
        self.sock.close()

    def delete_all_users(self):
	### Deleting users that are created other than admin
	try:
            LOG.info("Sending query all users tl1 command\n")
            self.sock.send('RTRV-USER-SECU:::123:;')
            sys.stdout.flush()
            user_settings = self.sock.recv(3072)
            user_settings.replace('\n', '')

            users_list = user_settings.split('COMPLD', 1)[1]
            users_list = users_list.split(' ')
            users_list = filter(None, users_list)
            users_list.remove('\r\n')
            final_list = []
            LOG.info("Sending delete all users  tl1 command\n")
            for user in users_list:
                u = user.split(',')
                final_list.append(u[0])
            for user in final_list:
                sys.stdout.flush()   
	        if user != 'admin':
                    self.sock.send('DLT-USER-SECU::%s:123:;' % user)
                    sys.stdout.flush()
                    delete_user = self.sock.recv(3072)
    	except Exception as err:
	    LOG.error("Failed to delete all users\n")

   
    def disable_aut_msg(self):
      
	### Disabling autonomous message for avoiding unneccessary tl1 outputs
        LOG.info("Sending disable autonomous message tl1 command\n")
        self.sock.send('OPR-ARC-EQPT::REPMGR:123::IND;')
        sys.stdout.flush()
	Aut = self.sock.recv(3072)
        nose.tools.assert_in('123 COMPLD', Aut, 'getting error from switch : %s' %Aut)
    
    def enable_all_ports(self):

	### Reset the oxc and port enable and disable using ph value 1
        LOG.info("Sending enable all ports tl1 command\n")
	self.sock.send('INIT-SYS::SYSTEM:123::1;')
 	sys.stdout.flush()
        Reset = self.sock.recv(3072)
	nose.tools.assert_in('123 COMPLD', Reset, 'getting error from switch : %s' %Reset)

    def set_dark_mode(self):
     
	### Set dark mode to reset the oxc and port enable and disable
        LOG.info("Sending set dark mode tl1 command\n")
	self.sock.send('ED-EQPT::BOOT:123:::MODE=DARK;')
	sys.stdout.flush()
        Mode = self.sock.recv(3072)
	nose.tools.assert_in('123 COMPLD', Mode, 'getting error from switch : %s' %Mode)

    def reset(self, **kwargs):

	try:
	    LOG.info("Sending %s command to switch : %s\n" % (kwargs['testcase_name'], kwargs['cmd']))
            self.sock.send(kwargs['cmd'])
            sys.stdout.flush()
            time.sleep(60)
            data = self.sock.setblocking(False)
        except Exception as err:
            data = self.sock.recv(3072)
            LOG.error("Error from the switch : %s\n" % err)

    def execute_tl1_commands(self, **kwargs):
        """ Create Socket:
             Arguments:
             cmd    : tl1_cmds
        """

        try:
            LOG.info("Sending %s command to switch : %s\n" % (kwargs['testcase_name'], kwargs['cmd']))
            self.sock.send(kwargs['cmd'])
	    sys.stdout.flush()
	    time.sleep(5)
            data = self.sock.recv(15000)
        except Exception as err:
            data = self.sock.recv(15000)
            LOG.error("Error from the switch : %s\n" % err)

        LOG.info("Output response from switch : \n    %s\n\t" % data)
	
	if 'Not logged in' in str(data):
            self.create_socket()
            LOG.info("Sending disable autonomous message tl1 command\n")
            self.sock.send('OPR-ARC-EQPT::REPMGR:123::IND;')
	    sys.stdout.flush()
            data = self.sock.recv(15000)
            self.sock.send(kwargs['cmd'])
	    time.sleep(3)
	    sys.stdout.flush()
            data = self.sock.recv(15000)
            return data
        elif str(data) == '':
            self.create_socket()
	    time.sleep(3)
            LOG.info("Sending disable autonomous message tl1 command\n")
            self.sock.send('OPR-ARC-EQPT::REPMGR:123::IND;')
	    sys.stdout.flush()
            data = self.sock.recv(15000)
            return
        elif kwargs['case'] == 'valid':
            nose.tools.assert_in('123 COMPLD', data, 'getting error from switch : %s' % data)
            return data
        elif kwargs['case'] == 'invalid':
            return data
        else:
            LOG.info("Please check the running cases are valid.....\n")
            return
            
            
