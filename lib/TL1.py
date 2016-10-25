""" 
Testing TL1 Funtionality
"""
import pexpect
import time
import sys
import nose
import logging
import logging.config
from config import  get_config_arg

logging.config.fileConfig('logging.ini')
LOG = logging.getLogger('TL_ONE')
ses = ''
class TL_ONE:
    def __init__(self, ip, port=6252):
        """ Init Arguments:
            Arguments:
            ip        : IP address.
        """
        self.ip = ip
        self.port = port

    def create_ses(self):
        """
        open the tl1 session
        """
        global ses
	try:
	    ### Logging into TL1 session using given credentials
            LOG.info("Creating tl1 over ssh session <sock = %s:%s>\n" % (self.ip, self.port))
            ses = pexpect.spawn ('ssh admin@%s -p %s' %(self.ip, self.port))
            time.sleep(5)
            user_name = get_config_arg('login_credentials', 'user_name')
            password = get_config_arg('login_credentials', 'password')
            LOG.info("expecting password")
            ses.expect ('password:')
            LOG.info("sending password")
            ses.sendline ('%s' % password)
            LOG.info("expecting > ")
            ses.expect ('>')
            LOG.info("sending disable autonomous message cmd ")
            ses.sendline ('ACT-USER::%s:123::%s;' %(user_name, password))
            time.sleep(5)
            LOG.info("expecting > ")
            ses.expect ('>')
            time.sleep(5)
            Login = ses.before
	    nose.tools.assert_in('Already logged in', Login, 'getting error from switch : %s' % Login)
        except Exception as e:
	    LOG.error("Failed to connect err : %s\n" % e) 


    def delete_all_users(self):
	### Deleting users that are created other than admin
        global ses
	try:
            #LOG.info("expecting > ")
            #ses.expect ('>')
            #time.sleep(5)
            LOG.info("Sending query all users tl1 command\n")
            ses.sendline ('RTRV-USER-SECU:::123:;')
            user_settings = ses.before
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
                    LOG.info("expecting > ")
                    ses.expect ('>')
                    time.sleep(5)
                    LOG.info("Sending query all users tl1 command\n")
                    ses.sendline ('DLT-USER-SECU::%s:123:;' % user)
                    time.sleep(5)
                    LOG.info("expecting > ")
                    ses.expect ('>')
                    time.sleep(5)
                    delete_user = ses.before
    	except Exception as err:
	    LOG.error("Failed to delete all users\n")

   
    def disable_aut_msg(self):
        global ses
	### Disabling autonomous message for avoiding unneccessary tl1 outputs
        LOG.info("Sending disable autonomous message tl1 command\n")
        #LOG.info("expecting > ")
        #ses.expect ('>')
        #time.sleep(5)
        ses.sendline ('OPR-ARC-EQPT::REPMGR:123::IND;')
        time.sleep(5)
        LOG.info("expecting > ")
        ses.expect ('>')
        time.sleep(5)
	Aut = ses.before
        nose.tools.assert_in('123 COMPLD', Aut, 'getting error from switch : %s' %Aut)
    
    def enable_all_ports(self):
	### Reset the oxc and port enable and disable using ph value 1
        global ses
        LOG.info("Sending enable all ports tl1 command\n")
        #LOG.info("expecting > ")
        #ses.expect ('>')
        #time.sleep(5)
        ses.sendline ('INIT-SYS::SYSTEM:123::1;')
        time.sleep(5)
        LOG.info("expecting > ")
        ses.expect ('>')
        time.sleep(5)
        Reset = ses.before	
	nose.tools.assert_in('123 COMPLD', Reset, 'getting error from switch : %s' %Reset)

    def set_dark_mode(self):
     
	### Set dark mode to reset the oxc and port enable and disable
        global ses
        LOG.info("Sending set dark mode tl1 command\n")
	#LOG.info("expecting > ")
        #ses.expect ('>')
        #time.sleep(5)
        ses.sendline ('ED-EQPT::BOOT:123:::MODE=DARK;')
        time.sleep(5)
        LOG.info("expecting > ")
        ses.expect ('>')
        time.sleep(5)
        Mode = ses.before
	nose.tools.assert_in('123 COMPLD', Mode, 'getting error from switch : %s' %Mode)

    def reset(self, **kwargs):
        global ses

	try:
	    LOG.info("Sending %s command to switch : %s\n" % (kwargs['testcase_name'], kwargs['cmd']))
            #LOG.info("expecting > ")
            #ses.expect ('>')
            #time.sleep(5)
            ses.sendline (kwargs['cmd'])
            time.sleep(60)
            LOG.info("expecting > ")
            ses.expect ('>')
            time.sleep(5)
            data = ses.before
        except Exception as err:
            time.sleep(60)
            LOG.info("expecting > ")
            ses.expect ('>')
            time.sleep(5)
            data = ses.before
            LOG.error("Error from the switch : %s\n" % err)

    def execute_tl1_commands(self, **kwargs):
        global ses
        """ Create Socket:
             Arguments:
             cmd    : tl1_cmds
        """

        try:
            LOG.info("Sending %s command to switch : %s\n" % (kwargs['testcase_name'], kwargs['cmd']))
            #LOG.info("expecting > ")
            #ses.expect ('>')
            #time.sleep(5)
            ses.sendline (kwargs['cmd'])
            time.sleep(5)
            LOG.info("expecting > ")
            ses.expect ('>')
            time.sleep(5)
            data = ses.before
        except Exception as err:
            LOG.info("expecting > ")
            ses.expect ('>')
            time.sleep(5)
            data = ses.before
            LOG.error("Error from the switch : %s\n" % err)

        LOG.info("Output response from switch :    %s\n\t" % data)
	
	if 'Not logged in' in str(data):
            LOG.info("Sending disable autonomous message tl1 command\n")
            LOG.info("expecting > ")
            ses.expect ('>')
            time.sleep(5)
            ses.sendline ('OPR-ARC-EQPT::REPMGR:123::IND;')
            time.sleep(5)
            LOG.info("expecting > ")
            ses.expect ('>')
            time.sleep(5)
            data = ses.before
            LOG.info("Sending %s command to switch : %s\n" % (kwargs['testcase_name'], kwargs['cmd']))
            ses.sendline (kwargs['cmd'])
            time.sleep(5)
            LOG.info("expecting > ")
            ses.expect ('>')
            time.sleep(5)
            data = ses.before
            return data
        elif str(data) == '':
	    time.sleep(3)
            LOG.info("Sending disable autonomous message tl1 command\n")
            LOG.info("expecting > ")
            ses.expect ('>')
            time.sleep(5)
            ses.sendline ('OPR-ARC-EQPT::REPMGR:123::IND;')
            time.sleep(5)
            LOG.info("expecting > ")
            ses.expect ('>')
            time.sleep(5)
            data = ses.before
            return
        elif kwargs['case'] == 'valid':
            nose.tools.assert_in('123 COMPLD', data, 'getting error from switch : %s' % data)
            return data
        elif kwargs['case'] == 'invalid':
            return data
        else:
            LOG.info("Please check the running cases are valid.....\n")
            return
            
            
