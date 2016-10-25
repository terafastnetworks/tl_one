import re
import datetime
import time
import nose
from TL1 import TL_ONE
from config import  get_config_arg
from get_switch_ports import get_single_ingress_port
from get_switch_ports import get_single_egress_port
from get_switch_ports import get_multiple_ingress_ports
from get_switch_ports import get_multiple_egress_ports
from get_switch_ports import get_mixed_ports

oxcDict = {

    'single_ingress_port'           : get_single_ingress_port(),
    'single_egress_port'            : get_single_egress_port(),
    'invalid_ingress_port'          : '1000',
    'invalid_egress_port'           : '2000',


}


BOX_IP = get_config_arg('switch_ip', 'ip')


class testTL1TestSuite:
    """ Executing TL1 commands and validating the result """

    @classmethod
    def setUpClass(cls):
        cls.tl1 = TL_ONE(BOX_IP)
        #cls.clean = cls.tl1.switch_reset()
        cls.tl1.create_ses()
        cls.tl1.disable_aut_msg()
        cls.tl1.set_dark_mode()
        cls.tl1.enable_all_ports()
	#cls.tl1.delete_all_users()	

    #@classmethod
    #def tearDownClass(cls):
    #    cls.tl1.close_socket()
   
    def create_box(self, testcase_name):
        """create box for test case name.
        Arguments:
        testcase_name   :       valid testcase name
        """

        print "\n"
        l = len(testcase_name) + 7
        start_end_session = '       +' + (l * '-') + '+       '
        middle = '| ' + '   ' + str(testcase_name) + '  ' + ' |'

        print '%s\n       %s\n%s\n\n' % (start_end_session, middle, start_end_session)

    def test_get_switch_serial_number(self):
        """
        testing query serial number functionality,
        and validating the result
        """
           
        self.create_box('test_get_switch_serial_number')
        result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-INV::OCS:123:;', testcase_name='test_get_serial_number')
        serial_number = get_config_arg('system_administration', 'serial_number')
        nose.tools.assert_in(serial_number, result, "getting error when querying switch serial number" )

    def test_set_and_query_switch_time(self):
        """
        testing set switch time and query switch time functionality,
        and validating the result
        """

	self.create_box('test_set_and_query_switch_time')
	current_time = datetime.datetime.now()
   	ex = current_time.strftime("%y-%m-%d,%H-%M-%S")
       	result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ED-DAT:::123::%s;' %ex, testcase_name = 'set_switch_time')
	print (time.strftime("%y-%m-%d,%H-%M-%S"))
	ex = current_time.strftime("%y-%m-%d %H:%M:%S")
      	nose.tools.assert_in(ex, result, "getting error when setting time")

	result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-TOD:::123:;',testcase_name = 'query_switch_time')
	current_time = datetime.datetime.now()
	ex = current_time.strftime("%Y,%m,%d,%H,%M")
	nose.tools.assert_in(ex, result, "getting error when querying time")

    def test_set_and_query_session_timeout_for_admin(self):
	"""
        testing set session timeout and query session timeout for admin functionality,
        and validating the result
        """

	self.create_box('test_session_timeout_set_and_query_for_admin')

	self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ED-EQPT::TIMEOUT:123:::ADMIN=0;', testcase_name = 'set_session_timeout_for_admin')
        result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-EQPT::TIMEOUT:123:::PARAMETER=ADMIN;', testcase_name = 'query_session_timeout_for_admin') 
	nose.tools.assert_in('0', result, "getting error when querying session timeout for admin")

    def test_set_and_query_session_timeout_for_user(self):
      	"""
        testing set session timeout and query session timeout for user functionality,
        and validating the result
        """

        self.create_box('test_session_timeout_set_and_query_for_user')

        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ED-EQPT::TIMEOUT:123:::USER=0;', testcase_name = 'set_session_timeout_for_user')
        result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-EQPT::TIMEOUT:123:::PARAMETER=USER;',testcase_name = 'query_session_timeout_for_user')
        nose.tools.assert_in('0', result, "getting error when querying session timeout for user")

    def test_query_switch_size(self):
	"""
        testing query switch size functionality,
        and validating the result
        """

	self.create_box('test_query_switch_size')

	result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-EQPT::SYSTEM:123:::PARAMETER=SIZE;', testcase_name = 'query_switch_size')
	ex = get_config_arg('system_administration','switch_size')
	nose.tools.assert_in(ex, result,"getting error when querying switch size")

    def test_query_header(self):
	"""
        testing query header functionality,
        and validating the result
        """
	
	self.create_box('test_query_header')

	self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-HDR:::123:;', testcase_name = 'query_header')

    def test_query_network_element_type(self):
	"""
        testing query network element type functionality,
        and validating the result
        """

	self.create_box('test_query_network_element_type')
	
	result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-NETYPE:::123:;', testcase_name = 'query_network_element_type')
	nose.tools.assert_in('OCS', result, "getting error when querying network element type")

    def test_set_system_identifier(self):
	"""
        testing set system identifier functionality,
        and validating the result
        """

	self.create_box('test_set_system_identifier')

	self.tl1.execute_tl1_commands(case = 'valid', cmd = 'SET-SID:::123::PolatisOXC;', testcase_name = 'set_system_identifier')

    def test_set_system_identifier_with_spaces(self):
        """
        testing set system identifier with spaces functionality,
        and validating the result
        """

        self.create_box('test_set_system_identifier_with_spaces')

        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'SET-SID:::123::Polatis OXC;', testcase_name = 'set_system_identifier')


    def test_set_system_identifier_as_numbers(self):
	"""
        testing set system identifier as numbers functionality,
        and validating the result
        """
	self.create_box('test_set_system_identifier_as_numbers')

        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'SET-SID:::123::565959856232;', testcase_name = 'set_system_identifier_as_numbers')

    def test_query_ip_address_for_eth0(self):
	"""
        testing query ip address for eth0 functionality,
        and validating the result
        """

	self.create_box('test_query_ip_address_for_eth0')

	result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-IP::eth0:123:;', testcase_name = 'query_ip_address_for_eth0')
	IP = get_config_arg('interface_eth0','eth0_ip')
	Gateway = get_config_arg('interface_eth0','gateway')
	Mask = get_config_arg('interface_eth0','mask')
	Broadcast = get_config_arg('interface_eth0','broadcast')
	
	nose.tools.assert_in(IP, result, "getting error when querying IP")
        nose.tools.assert_in(Gateway, result, "getting error when querying gateway")
        nose.tools.assert_in(Mask, result, "getting error when querying mask")
        nose.tools.assert_in(Broadcast, result, "getting error when querying broadcast")

    def test_query_ip_address_for_eth1(self):
        """
        testing query ip address for eth1 functionality,
        and validating the result
        """
	self.create_box('test_query_ip_address_for_eth1')	

	result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-IP::eth1:123:;', testcase_name = 'query_ip_address_for_eth1')
	IP = get_config_arg('interface_eth1','eth1_ip')
        Gateway = get_config_arg('interface_eth1','gateway')
        Mask = get_config_arg('interface_eth1','mask')
        Broadcast = get_config_arg('interface_eth1','broadcast')
	
	nose.tools.assert_in(IP, result, "getting error when querying IP")
        nose.tools.assert_in(Gateway, result, "getting error when querying gateway")
        nose.tools.assert_in(Mask, result, "getting error when querying mask")
        nose.tools.assert_in(Broadcast, result, "getting error when querying broadcast")
	
    def test_query_ip_address_with_keywords_for_eth0(self):
	"""
        testing query ip address for eth0 functionality,
        and validating the result
        """
	self.create_box('test_query_ip_address_with_keywords_for_eth0')

	result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-IPPORT::eth0:123:;', testcase_name = 'query_ip_address_with_keywords_for_eth0')
	Name = get_config_arg('interface_eth0', 'name')
	IP = get_config_arg('interface_eth0','eth0_ip')
        Gateway = get_config_arg('interface_eth0','gateway')
        Mask = get_config_arg('interface_eth0','mask')
        Broadcast = get_config_arg('interface_eth0','broadcast')
	
	nose.tools.assert_in(Name, result, "getting error when querying name")
        nose.tools.assert_in(IP, result, "getting error when querying IP")
        nose.tools.assert_in(Gateway, result, "getting error when querying gateway")
        nose.tools.assert_in(Mask, result, "getting error when querying mask")
        nose.tools.assert_in(Broadcast, result, "getting error when querying broadcast")
	
    def test_query_ip_address_with_keywords_for_eth1(self):
        """
        testing query ip address for eth1 functionality,
        and validating the result
        """
        self.create_box('test_query_ip_address_with_keywords_for_eth1')

        result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-IPPORT::eth1:123:;', testcase_name = 'query_ip_address_with_keywords_for_eth1')
        Name = get_config_arg('interface_eth1', 'name')
        IP = get_config_arg('interface_eth1','eth1_ip')
        Gateway = get_config_arg('interface_eth1','gateway')
        Mask = get_config_arg('interface_eth1','mask')
        Broadcast = get_config_arg('interface_eth1','broadcast')

        nose.tools.assert_in(Name, result, "getting error when querying name")
        nose.tools.assert_in(IP, result, "getting error when querying IP")
        nose.tools.assert_in(Gateway, result, "getting error when querying gateway")
        nose.tools.assert_in(Mask, result, "getting error when querying mask")
        nose.tools.assert_in(Broadcast, result, "getting error when querying broadcast")
    
    def test_query_mac_address_for_eth0(self):
	"""
        testing query mac address for eth0 functionality,
        and validating the result
        """

	self.create_box('test_query_mac_address_for_eth0')

        result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-MAC::eth0:123:;', testcase_name = 'query_mac_address_for_eth0')
	ex = get_config_arg('interface_eth0','mac')
        nose.tools.assert_in(ex, result,"getting error when querying mac address")
	
    def test_query_mac_address_for_eth1(self):
        """
        testing query mac address for eth1 functionality,
        and validating the result
        """
	self.create_box('test_query_mac_address_for_eth1')	

        result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-MAC::eth1:123:;', testcase_name = 'query_mac_address_for_eth1')
	ex1 = get_config_arg('interface_eth1','mac')
        nose.tools.assert_in(ex1, result,"getting error when querying mac address")

    def test_reset_the_system_with_ph_value_0(self):
	"""
        testing set reset the system with ph value 0 functionality,
        and validating the result
        """

	self.create_box('test_reset_the_system_with_ph_value_0')

	self.tl1.execute_tl1_commands(case = 'valid', cmd = 'INIT-SYS::SYSTEM:123::0;', testcase_name = 'reset_system_with_ph_value_0') 

    def test_reset_the_system_with_ph_value_1(self):
        """
        testing set reset the system with ph value 1 functionality,
        and validating the result
        """
	self.create_box('test_set_reset_the_system_with_ph_value_1')
	
	self.tl1.execute_tl1_commands(case = 'valid', cmd = 'INIT-SYS::SYSTEM:123::1;', testcase_name = 'reset_system_with_ph_value_1')

    def test_reset_the_system_with_ph_value_10(self):
        """
        testing set reset the system with ph value 10 functionality,
        and validating the result
        """
        self.create_box('test_reset_the_system_with_ph_value_10')


   	result = self.tl1.reset(case = 'valid', cmd = 'INIT-SYS::SYSTEM:123::10;', testcase_name = 'reset_system_with_ph_value_10')
	
	print "result: ", result
        #nose.tools.assert_in('', result, "getting error when reset the system")
	print "fininside..........."
	#time.sleep(70)
	print "foutside.........."
	self.tl1.create_socket()
	self.tl1.disable_aut_msg()
		
    def test_set_and_query_switch_startup_mode_using_dark_mode(self):
	"""
        testing set and query switch startup mode using dark mode functionality,
        and validating the result
        """

	self.create_box('test_set_and_query_switch_startup_mode_using_dark_mode')

	self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ED-EQPT::BOOT:123:::MODE=DARK;', testcase_name = 'set_switch_startup_mode_using_dark_mode')

	result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-EQPT::BOOT:123:::PARAMETER=MODE;', testcase_name = 'query_switch_startup_mode_using_dark_mode')
        nose.tools.assert_in('DARK', result, "getting error when querying boot mode")

    def test_set_and_query_switch_startup_mode_using_restore_mode(self):
	"""
        testing set and query switch startup mode using restore mode functionality,
        and validating the result
        """

        self.create_box('test_set_and_query_switch_startup_mode_using_restore_mode')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ED-EQPT::BOOT:123:::MODE=RESTORE;', testcase_name = 'set_switch_startup_mode_using_restore_mode')
        result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-EQPT::BOOT:123:::PARAMETER=MODE;', testcase_name = 'query_switch_startup_mode_using_restore_mode')
        nose.tools.assert_in('RESTORE', result, "getting error when querying boot mode")

    def test_set_and_query_oxc_for_single_port(self):
	"""
        testing set and query oxc single port functionality,
        and validating the result
        """

	self.create_box('test_set_and_query_oxc_single_port')

	SetOxc = (oxcDict['single_ingress_port'], oxcDict['single_egress_port'])
	self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ENT-PATCH::%s,%s:123:;' % SetOxc, testcase_name = 'set_oxc_individual_port')

	QueryOxc = (oxcDict['single_ingress_port'])      
        result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-PATCH::%s:123:;'% QueryOxc,testcase_name = 'query_oxc_individual_port')
	nose.tools.assert_in(str(QueryOxc), result, "getting error while querying ingress and egress ports")
	
	DelPort = (oxcDict['single_ingress_port'])
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'DLT-PATCH::ALL:123:;' , testcase_name = 'delete_oxc')

    def test_set_and_query_oxc_for_multiple_ports_using_single_ampersand(self):
        """
        testing set and query oxc for multiple ports using single ampersand functionality,
        and validating the result
        """

        self.create_box('test_set_and_query_oxc_for_multiple_ports_using_single_ampersand')
        prt1, prt2, prt3 = get_multiple_ingress_ports() 
        prt4, prt5, prt6 = get_multiple_egress_ports() 
        
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ENT-PATCH::%d&%d&%d,%d&%d&%d:123:;' % (prt1, prt2, prt3, prt4, prt5, prt6) , testcase_name = 'set_oxc_multiple_ports')
        result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-PATCH::%d&%d&%d:123:;'% (prt1, prt2, prt3),testcase_name = 'query_oxc_multiple_ports')
	nose.tools.assert_in(str(prt1), result, "getting error while querying ingress and egress ports")   
	self.tl1.execute_tl1_commands(case = 'valid', cmd = 'DLT-PATCH::ALL:123:;' , testcase_name = 'delete_oxc')

    def test_set_and_query_oxc_for_multiple_ports_using_double_ampersand(self):
        """
        testing set and query oxc for multiple ports using double ampersand functionality,
        and validating the result
        """

        self.create_box('test_set_and_query_oxc_for_multiple_ports_using_double_ampersand')
        prt1, prt2, prt3 = get_multiple_ingress_ports() 
        prt4, prt5, prt6 = get_multiple_egress_ports() 

        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ENT-PATCH::%d&&%d,%d&&%d:123:;' % (prt1, prt2, prt4, prt5) , testcase_name = 'set_oxc_grouped_ports')
        result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-PATCH::%d&&%d:123:;'% (prt1, prt2),testcase_name = 'query_oxc_grouped_ports')
        nose.tools.assert_in(str(prt1), result, "getting error while querying ingress and egress ports")
	self.tl1.execute_tl1_commands(case = 'valid', cmd = 'DLT-PATCH::%d&&%d:123:;' % (prt1, prt2), testcase_name = 'delete_oxc_grouped_ports')
	
    def test_delete_oxc_for_single_port(self):
	"""
        testing set, delete and query oxc single port functionality,
        and validating the result
        """

	self.create_box('test_delete_oxc_for_single_port')

	SetOxc = (oxcDict['single_ingress_port'], oxcDict['single_egress_port'])
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ENT-PATCH::%s,%s:123:;' % SetOxc, testcase_name = 'set_oxc_individual_port')

	DelPort = (oxcDict['single_ingress_port'])
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'DLT-PATCH::%s:123:;' % DelPort, testcase_name = 'delete_oxc_individual_port')
	
	QueryOxc = (oxcDict['single_ingress_port'])
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-PATCH::%s:123:;'% QueryOxc,testcase_name = 'query_oxc_individual_port')

    def test_delete_and_query_oxc_for_multiple_ports_using_single_ampersand(self):
        """
        testing delete and query oxc for multiple ports using single ampersand functionality,
        and validating the result
        """

        self.create_box('test_delete_and_query_oxc_for_multiple_ports_using_single_ampersand')
        prt1, prt2, prt3 = get_multiple_ingress_ports()
        prt4, prt5, prt6 = get_multiple_egress_ports()

        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ENT-PATCH::%d&%d&%d,%d&%d&%d:123:;' % (prt1, prt2, prt3, prt4, prt5, prt6) , testcase_name = 'set_oxc_multiple_ports')
	self.tl1.execute_tl1_commands(case = 'valid', cmd = 'DLT-PATCH::%d&%d&%d:123:;' % (prt1, prt2, prt3), testcase_name = 'delete_oxc_multiple_ports')
        result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-PATCH::%d&%d&%d:123:;'% (prt1, prt2, prt3),testcase_name = 'query_oxc_multiple_ports')
        nose.tools.assert_in(str(prt1), result, "getting error while querying ingress and egress ports")

    def test_delete_and_query_oxc_for_multiple_ports_using_double_ampersand(self):
        """
        testing delete and query oxc for multiple ports using double ampersand functionality,
        and validating the result
        """

        self.create_box('test_delete_and_query_oxc_for_multiple_ports_using_double_ampersand')
        prt1, prt2, prt3 = get_multiple_ingress_ports()
        prt4, prt5, prt6 = get_multiple_egress_ports()

	self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ENT-PATCH::%d&&%d,%d&&%d:123:;' % (prt1, prt2, prt4, prt5) , testcase_name = 'set_oxc_grouped_ports')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'DLT-PATCH::%d&&%d:123:;' % (prt1, prt2), testcase_name = 'delete_oxc_grouped_ports')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-PATCH::%d&&%d:123:;'% (prt1, prt2),testcase_name = 'query_oxc_multiple_ports')

    def test_delete_and_query_oxc_using_all_aid(self):
        """
        testing delete and query oxc using all aid port functionality,
        and validating the result
        """

        self.create_box('test_delete_and_query_oxc_using_all_aid')
        prt1, prt2, prt3 = get_multiple_ingress_ports()
        prt4, prt5, prt6 = get_multiple_egress_ports()

        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ENT-PATCH::%d&&%d,%d&&%d:123:;' % (prt1, prt2, prt4, prt5) , testcase_name = 'set_oxc_grouped_ports')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'DLT-PATCH::ALL:123:;' , testcase_name = 'delete_oxc_grouped_ports')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-PATCH::%d&&%d:123:;'% (prt1, prt2),testcase_name = 'query_oxc_multiple_ports')
		
    def test_delete_and_query_oxc_using_without_aid(self):
        """
        testing delete and query oxc using without aid port functionality,
        and validating the result
        """

        self.create_box('test_delete_and_query_oxc_using_without_aid')
        prt1, prt2, prt3 = get_multiple_ingress_ports()
        prt4, prt5, prt6 = get_multiple_egress_ports()

        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ENT-PATCH::%d&&%d,%d&&%d:123:;' % (prt1, prt2, prt4, prt5) , testcase_name = 'set_oxc_grouped_ports')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'DLT-PATCH:::123:;' , testcase_name = 'delete_oxc_grouped_ports')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-PATCH::%d&&%d:123:;'% (prt1, prt2),testcase_name = 'query_oxc_multiple_ports')

    def test_query_oxc_using_all_aid(self):
        """
        testing set and query oxc using ALL functionality,
        and validating the result
        """

        self.create_box('test_query_oxc_using_all_aid')

        SetOxc = (oxcDict['single_ingress_port'], oxcDict['single_egress_port'])
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ENT-PATCH::%s,%s:123:;' % SetOxc, testcase_name = 'set_oxc_individual_port')
        result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-PATCH::ALL:123:;',testcase_name = 'query_oxc_using_ALL')
        QueryOxc = (oxcDict['single_ingress_port'])
        nose.tools.assert_in(str(QueryOxc), result, "getting error when querying crossconnects")

	DelPort = (oxcDict['single_ingress_port'])
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'DLT-PATCH:::123:;', testcase_name = 'delete_oxc')

    def test_query_oxc_without_aid(self):
        """
        testing set and query oxc without AID functionality,
        and validating the result
        """

        self.create_box('test_query_oxc_without_aid')

        SetOxc = (oxcDict['single_ingress_port'], oxcDict['single_egress_port'])
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ENT-PATCH::%s,%s:123:;' % SetOxc, testcase_name = 'set_oxc_individual_port')
        result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-PATCH:::123:;',testcase_name = 'query_oxc_without_aid')
        QueryOxc = (oxcDict['single_ingress_port'])
        nose.tools.assert_in(str(QueryOxc), result, "getting error when querying crossconnects")
	
	DelPort = (oxcDict['single_ingress_port'])
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'DLT-PATCH:::123:;', testcase_name = 'delete_oxc')

    def test_set_and_query_single_port_label(self):
	"""
        testing set and query single port label functionality,
        and validating the result
        """

	self.create_box('test_set_and_query_single_port_label')

	PortLabel = (oxcDict['single_ingress_port'])
	self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ED-PORT-LABEL::%s:123:::LABEL=src;' % PortLabel, testcase_name = 'set_single_port_label')
	result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-PORT-LABEL::%s:123:;' % PortLabel, testcase_name = 'query_single_port_label')
	nose.tools.assert_in(str(PortLabel), result, "getting error when querying multiple port label")
	self.tl1.execute_tl1_commands(case = 'valid', cmd = 'DLT-PORT-LABEL::%s:123:;' % PortLabel, testcase_name = 'delete_port_label')

    def test_set_and_query_multiple_port_label(self):
        """
        testing set and query multiple port label functionality,
        and validating the result
        """

        self.create_box('test_set_and_query_multiple_port_label')
	
	prt1, prt2, prt3 = get_multiple_ingress_ports()
        prt4, prt5, prt6 = get_multiple_egress_ports()

        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ED-PORT-LABEL::%s&%s:123:::LABEL=src1&src2;' %(prt1,prt2), testcase_name = 'set_multiple_port_label')
        result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-PORT-LABEL::%s&%s:123:;' % (prt1, prt2), testcase_name = 'query_multiple_port_label')
        nose.tools.assert_in(str(prt1), result, "getting error when querying multiple port label")
	nose.tools.assert_in(str(prt2), result, "getting error when querying multiple port label")
	self.tl1.execute_tl1_commands(case = 'valid', cmd = 'DLT-PORT-LABEL::%s&%s:123:;' %(prt1, prt2), testcase_name = 'delete_port_label')

    def test_delete_single_port_label(self):
	"""
        testing set and query single port label functionality,
        and validating the result
        """

	self.create_box('test_delete_single_port_label')

	PortLabel = (oxcDict['single_ingress_port'])
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ED-PORT-LABEL::%s:123:::LABEL=src;' % PortLabel, testcase_name = 'set_single_port_label')
	self.tl1.execute_tl1_commands(case = 'valid', cmd = 'DLT-PORT-LABEL::%s:123:;' % PortLabel, testcase_name = 'delete_single_port_label')
	result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-PORT-LABEL::%s:123:;' % PortLabel, testcase_name = 'query_single_port_label')
        nose.tools.assert_in(str(PortLabel), result, "getting error when querying port label")
    
    def test_delete_multiple_port_label(self):
        """
        testing set and query multiple port label functionality,
        and validating the result
        """

        self.create_box('test_delete_multiple_port_label')

	prt1, prt2, prt3 = get_multiple_ingress_ports()
        prt4, prt5, prt6 = get_multiple_egress_ports()

        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ED-PORT-LABEL::%s&%s:123:::LABEL=src1&src2;' %(prt1, prt2), testcase_name = 'set_multiple_port_label')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'DLT-PORT-LABEL::%s&%s:123:;' %(prt1, prt2), testcase_name = 'delete_multiple_port_label')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-PORT-LABEL::%s&%s:123:;' % (prt1, prt2), testcase_name = 'query_multiple_port_label')

    def test_query_port_label_without_port_aid(self):
	"""
        testing query port label without port aid functionality,
        and validating the result
        """

	self.create_box('test_query_port_label_without_port_aid')

	prt1, prt2, prt3 = get_multiple_ingress_ports()
        prt4, prt5, prt6 = get_multiple_egress_ports()

        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ED-PORT-LABEL::%d&%d:123:::LABEL=src1&src2;' %(prt1, prt2), testcase_name = 'set_multiple_port_label')
	result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-PORT-LABEL:::123:;', testcase_name = 'query_multiple_port_label')
        nose.tools.assert_in(str(prt1), result, "getting error when querying multiple port label")
	self.tl1.execute_tl1_commands(case = 'valid', cmd = 'DLT-PORT-LABEL::%s&%s:123:;' %(prt1, prt2), testcase_name = 'delete_port_label')

    def test_disable_single_port_aid(self):
	"""
        testing disable single port aid functionality,
        and validating the result
        """

	self.create_box('test_disable_single_port_aid')

	
	PortLabel = (oxcDict['single_ingress_port'])
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'OPR-PORT-SHUTTER::%s:123:;' % PortLabel, testcase_name = 'disable_single_port_aid')
	result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-PORT-SHUTTER::%s:123:;' %PortLabel, testcase_name = 'query_single_port_label')
	nose.tools.assert_in('CLOSED', result, "getting error when disable the port functionality")
	self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RLS-PORT-SHUTTER::%s:123:;' %PortLabel, testcase_name = 'enable_port_aid')
	
    def test_disable_multiple_ports_using_single_ampersand(self):
	"""
        testing disable multiple ports using single ampersand functionality,
        and validating the result
        """

	self.create_box('test_disable_multiple_ports_using_single_ampersand')

	prt1, prt2, prt3 = get_multiple_ingress_ports()
        prt4, prt5, prt6 = get_multiple_egress_ports()

        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'OPR-PORT-SHUTTER::%s&%s:123:;' %(prt1, prt2), testcase_name = 'disable_multiple_port_aid')
        result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-PORT-SHUTTER::%s&%s:123:;' %(prt1, prt2), testcase_name = 'query_multiple_port_label')
        nose.tools.assert_in('CLOSED', result, "getting error when querying multiple port label")
	self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RLS-PORT-SHUTTER::%s&%s:123:;' %(prt1, prt2), testcase_name = 'enable_port_aid')

    def test_disable_multiple_ports_using_double_ampersand(self):
        """
        testing disable multiple ports using double ampersand functionality,
        and validating the result
        """

        self.create_box('test_disable_multiple_ports_using_double_ampersand')

        prt1, prt2, prt3 = get_multiple_ingress_ports()
        prt4, prt5, prt6 = get_multiple_egress_ports()

        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'OPR-PORT-SHUTTER::%s&&%s:123:;' %(prt1, prt2), testcase_name = 'disable_multiple_port_aid')
        result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-PORT-SHUTTER::%s&&%s:123:;' %(prt1, prt2), testcase_name = 'query_multiple_port_label')
        nose.tools.assert_in('CLOSED', result, "getting error when querying multiple port label")
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RLS-PORT-SHUTTER::%s&&%s:123:;' %(prt1, prt2), testcase_name = 'enable_port_aid')

    def test_enable_single_port_aid(self):
        """
        testing enable single port aid functionality,
        and validating the result
        """

        self.create_box('test_enable_single_port_aid')


        PortLabel = (oxcDict['single_ingress_port'])
	self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RLS-PORT-SHUTTER::%s:123:;' %PortLabel, testcase_name = 'enable_port_aid')
        result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-PORT-SHUTTER::%s:123:;' % PortLabel, testcase_name = 'query_disable_single_port_aid')
        nose.tools.assert_in('OPEN', result, "getting error when disable the port functionality")

    def test_enable_multiple_ports_using_single_ampersand(self):
        """
        testing enable multiple ports using single ampersand functionality,
        and validating the result
        """

        self.create_box('test_enable_multiple_ports_using_single_ampersand')

        prt1, prt2, prt3 = get_multiple_ingress_ports()
        prt4, prt5, prt6 = get_multiple_egress_ports()
	
	self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RLS-PORT-SHUTTER::%s&%s:123:;' %(prt1, prt2), testcase_name = 'enable_port_aid')
        result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-PORT-SHUTTER::%s&%s:123:;' %(prt1, prt2), testcase_name = 'query_multiple_port_label')
        nose.tools.assert_in('OPEN', result, "getting error when querying multiple port label")

    def test_enable_multiple_ports_using_double_ampersand(self):
        """
        testing enable multiple ports using double ampersand functionality,
        and validating the result
        """

        self.create_box('test_enable_multiple_ports_using_double_ampersand')

        prt1, prt2, prt3 = get_multiple_ingress_ports()
        prt4, prt5, prt6 = get_multiple_egress_ports()

	self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RLS-PORT-SHUTTER::%s&&%s:123:;' %(prt1, prt2), testcase_name = 'enable_port_aid')
        result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-PORT-SHUTTER::%s&&%s:123:;' %(prt1, prt2), testcase_name = 'query_multiple_port_label')
        nose.tools.assert_in('OPEN', result, "getting error when querying multiple port label")

    def test_query_without_port_aid(self):
        """
        testing query without port aid functionality,
        and validating the result
        """

        self.create_box('test_query_without_port_aid')

        prt1, prt2, prt3 = get_multiple_ingress_ports()
        prt4, prt5, prt6 = get_multiple_egress_ports()

        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RLS-PORT-SHUTTER::%s&&%s:123:;' %(prt1, prt2), testcase_name = 'enable_port_aid')
        result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-PORT-SHUTTER:::123:;', testcase_name = 'query_multiple_port_label')
        nose.tools.assert_in('OPEN', result, "getting error when querying multiple port label")

    def test_login_with_username_as_numbers(self):
        """
        testing login username as numbers functionality,
        and validating the result
        """

        self.create_box('test_login_with_username_as_numbers')

	self.tl1.delete_all_users()
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ENT-USER-SECU::9942:123::root,,admin;', testcase_name = 'create_user_with_username_as_numbers')

	Logout = get_config_arg('login_credentials', 'user_name')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'CANC-USER::%s:123:;' % Logout, testcase_name = 'logout_the_current_user')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ACT-USER::9942:123::root;', testcase_name = 'login_with_created_user')
	Password = get_config_arg('login_credentials', 'password')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ACT-USER::%s:123::%s;' %(Logout, Password), testcase_name = 'login_with_default_user')

    def test_login_with_password_as_numbers(self):
	"""
        testing login password as numbers functionality,
        and validating the result
        """
	
	self.create_box('test_login_with_password_as_numbers')

	self.tl1.delete_all_users()
	self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ENT-USER-SECU::polatis:123::99427,,admin;', testcase_name = 'create_user_with_password_as_numbers')

	Logout = get_config_arg('login_credentials', 'user_name')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'CANC-USER::%s:123:;' % Logout, testcase_name = 'logout_the_current_user')
	self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ACT-USER::polatis:123::99427;', testcase_name = 'login_with_created_user')
        Password = get_config_arg('login_credentials', 'password')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ACT-USER::%s:123::%s;' %(Logout, Password), testcase_name = 'login_with_default_user')

    def test_logout_session(self):
        """
        testing logout session functionality,
        and validating the result
        """

        self.create_box('test_logout_session')
	
	#self.tl1.delete_all_users()
	Username = get_config_arg('login_credentials', 'user_name')
	Password = get_config_arg('login_credentials', 'password')
	self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ACT-USER::%s:123::%s;' %(Username, Password), testcase_name = 'login_with_default_user')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'CANC-USER::%s:123:;' % Username, testcase_name = 'logout_the_current_user')
	self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ACT-USER::%s:123::%s;' %(Username, Password), testcase_name = 'login_with_default_user')
	
    def test_create_user_with_password_as_numbers(self):
        """
        testing create user with password as numbers functionality,
        and validating the result
        """

        self.create_box('test_create_user_with_password_as_numbers')
	
	self.tl1.delete_all_users()
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ENT-USER-SECU::polatis1:123::99427,,;', testcase_name = 'create_user_without_user_access_privilege')
        result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-USER-SECU::polatis1:123:;', testcase_name = 'query_created_user')
        nose.tools.assert_in('polatis1', result, "getting error when query created user")
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'DLT-USER-SECU::polatis1:123:;', testcase_name = 'delete_created_user')

    def test_create_user_without_user_access_privilege(self):
        """
        testing create user without user access privilege functionality,
        and validating the result
        """

        self.create_box('test_create_user_without_user_access_privilege')

 	self.tl1.delete_all_users()
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ENT-USER-SECU::polatis1:123::root,,;', testcase_name = 'create_user_without_user_access_privilege')
        result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-USER-SECU::polatis1:123:;', testcase_name = 'query_created_user')
        nose.tools.assert_in('polatis1', result, "getting error when query created user")
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'DLT-USER-SECU::polatis1:123:;', testcase_name = 'delete_created_user')

    def test_create_user_without_password(self):
        """
        testing create user without password functionality,
        and validating the result
        """

        self.create_box('test_create_user_without_password')

	self.tl1.delete_all_users()
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ENT-USER-SECU::polatis1:123::,,admin;', testcase_name = 'create_user_without_password')
        result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-USER-SECU::polatis1:123:;', testcase_name = 'query_created_user')
        nose.tools.assert_in('polatis1', result, "getting error when query created user")
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'DLT-USER-SECU::polatis1:123:;', testcase_name = 'delete_created_user')

    def test_create_user_without_password_and_user_access_privilege(self):
        """
        testing create user without password and user access privilege functionality,
        and validating the result
        """

        self.create_box('test_create_user_without_password_and_user_access_privilege')

	self.tl1.delete_all_users()
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ENT-USER-SECU::polatis1:123::,,;', testcase_name = 'create_user_without_password_and_uap')
        result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-USER-SECU::polatis1:123:;', testcase_name = 'query_created_user')
        nose.tools.assert_in('polatis1', result, "getting error when query created user")
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'DLT-USER-SECU::polatis1:123:;', testcase_name = 'delete_created_user')
   
    def test_change_password_for_created_admin_priv_user(self):
        """
        testing change password for admin priv user using edit user settings functionality,
        and validating the result
        """

        self.create_box('test_change_password_for_created_admin_priv_user')

	self.tl1.delete_all_users()
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ENT-USER-SECU::polatis1:123::root,,admin;', testcase_name = 'create_user_without_password_and_uap')
	self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ED-USER-SECU::polatis1:123::,abcd,,;', testcase_name = 'change_password_for_admin')
	
	Username = get_config_arg('login_credentials', 'user_name')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'CANC-USER::%s:123:;' % Username, testcase_name = 'logout_the_current_user')
	self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ACT-USER::polatis1:123::abcd;', testcase_name = 'login_with_edited_user')
        result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-USER-SECU::polatis1:123:;', testcase_name = 'query_created_user')
        nose.tools.assert_in('polatis1', result, "getting error when query created user")
	self.tl1.execute_tl1_commands(case = 'valid', cmd = 'CANC-USER::polatis1:123:;', testcase_name = 'logout_the_current_user')

	Password = get_config_arg('login_credentials', 'password')
	self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ACT-USER::%s:123::%s;' %(Username, Password), testcase_name = 'login_with_default_user')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'DLT-USER-SECU::polatis1:123:;', testcase_name = 'delete_created_user')

    def test_change_password_for_created_user_priv_user(self):
        """
        testing change password for user priv user using edit user settings functionality,
        and validating the result
        """

        self.create_box('test_change_password_for_created_user_priv_user')

	self.tl1.delete_all_users()
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ENT-USER-SECU::polatis1:123::root,,user;', testcase_name = 'create_user_without_password_and_uap')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ED-USER-SECU::polatis1:123::,abcd,,;', testcase_name = 'change_password_for_the_user')

        Username = get_config_arg('login_credentials', 'user_name')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'CANC-USER::%s:123:;' % Username, testcase_name = 'logout_the_current_user')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ACT-USER::polatis1:123::abcd;', testcase_name = 'login_with_edited_user')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'CANC-USER::polatis1:123:;', testcase_name = 'logout_the_current_user')

        Password = get_config_arg('login_credentials', 'password')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ACT-USER::%s:123::%s;' %(Username, Password), testcase_name = 'login_with_default_user')
	result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-USER-SECU::polatis1:123:;', testcase_name = 'query_created_user')
        nose.tools.assert_in('polatis1', result, "getting error when query created user")
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'DLT-USER-SECU::polatis1:123:;', testcase_name = 'delete_created_user')

    def test_change_password_for_created_view_priv_user(self):
        """
        testing change password for view priv user using edit user settings functionality,
        and validating the result
        """

        self.create_box('test_change_password_for_created_view_priv_user')

	self.tl1.delete_all_users()
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ENT-USER-SECU::polatis1:123::root,,view;', testcase_name = 'create_user_without_password_and_uap')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ED-USER-SECU::polatis1:123::,abcd,,;', testcase_name = 'change_password_for_the_user')

        Username = get_config_arg('login_credentials', 'user_name')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'CANC-USER::%s:123:;' % Username, testcase_name = 'logout_the_current_user')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ACT-USER::polatis1:123::abcd;', testcase_name = 'login_with_edited_user')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'CANC-USER::polatis1:123:;', testcase_name = 'logout_the_current_user')

        Password = get_config_arg('login_credentials', 'password')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ACT-USER::%s:123::%s;' %(Username, Password), testcase_name = 'login_with_default_user')
        result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-USER-SECU::polatis1:123:;', testcase_name = 'query_created_user')
        nose.tools.assert_in('polatis1', result, "getting error when query created user")
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'DLT-USER-SECU::polatis1:123:;', testcase_name = 'delete_created_user')

    def test_change_username_for_created_admin_priv_user(self):
        """
        testing change username for admin priv user using edit user settings functionality,
        and validating the result
        """

        self.create_box('test_change_username_for_created_admin_priv_user')

	self.tl1.delete_all_users()
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ENT-USER-SECU::polatis1:123::root,,admin;', testcase_name = 'create_user_without_password_and_uap')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ED-USER-SECU::polatis1:123::polatis2,,,;', testcase_name = 'change_username_for_the_user')

        Username = get_config_arg('login_credentials', 'user_name')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'CANC-USER::%s:123:;' % Username, testcase_name = 'logout_the_current_user')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ACT-USER::polatis2:123:;', testcase_name = 'login_with_edited_user')
	result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-USER-SECU::polatis2:123:;', testcase_name = 'query_created_user')
        nose.tools.assert_in('polatis2', result, "getting error when query created user")	
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'CANC-USER::polatis2:123:;', testcase_name = 'logout_the_current_user')

        Password = get_config_arg('login_credentials', 'password')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ACT-USER::%s:123::%s;' %(Username, Password), testcase_name = 'login_with_default_user')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'DLT-USER-SECU::polatis2:123:;', testcase_name = 'delete_created_user')

    def test_change_username_for_created_user_priv_user(self):
        """
        testing change username for user priv user using edit user settings functionality,
        and validating the result
        """

        self.create_box('test_change_username_for_created_user_priv_user')

	self.tl1.delete_all_users()
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ENT-USER-SECU::polatis1:123::root,,user;', testcase_name = 'create_user_without_password_and_uap')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ED-USER-SECU::polatis1:123::polatis2,,,;', testcase_name = 'change_username_for_the_user')

        Username = get_config_arg('login_credentials', 'user_name')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'CANC-USER::%s:123:;' % Username, testcase_name = 'logout_the_current_user')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ACT-USER::polatis2:123:;', testcase_name = 'login_with_edited_user')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'CANC-USER::polatis2:123:;', testcase_name = 'logout_the_current_user')

        Password = get_config_arg('login_credentials', 'password')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ACT-USER::%s:123::%s;' %(Username, Password), testcase_name = 'login_with_default_user')
        result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-USER-SECU::polatis2:123:;', testcase_name = 'query_created_user')
        nose.tools.assert_in('polatis2', result, "getting error when query created user")
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'DLT-USER-SECU::polatis2:123:;', testcase_name = 'delete_created_user')

    def test_change_username_for_created_view_priv_user(self):
        """
        testing change username for view priv user using edit user settings functionality,
        and validating the result
        """

        self.create_box('test_change_username_for_created_view_priv_user')

	self.tl1.delete_all_users()
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ENT-USER-SECU::polatis1:123::root,,view;', testcase_name = 'create_user')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ED-USER-SECU::polatis1:123::polatis2,,,;', testcase_name = 'change_username_for_the_user')

        Username = get_config_arg('login_credentials', 'user_name')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'CANC-USER::%s:123:;' % Username, testcase_name = 'logout_the_current_user')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ACT-USER::polatis2:123:;', testcase_name = 'login_with_edited_user')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'CANC-USER::polatis2:123:;', testcase_name = 'logout_the_current_user')

        Password = get_config_arg('login_credentials', 'password')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ACT-USER::%s:123::%s;' %(Username, Password), testcase_name = 'login_with_default_user')
        result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-USER-SECU::polatis2:123:;', testcase_name = 'query_created_user')
        nose.tools.assert_in('polatis2', result, "getting error when query created user")
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'DLT-USER-SECU::polatis2:123:;', testcase_name = 'delete_created_user')
 
    def test_change_access_level_for_created_admin_priv_user(self):
        """
        testing change access level for admin priv user using edit user settings functionality,
        and validating the result
        """

        self.create_box('test_change_access_level_for_created_admin_priv_user')

	self.tl1.delete_all_users()
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ENT-USER-SECU::polatis1:123::root,,admin;', testcase_name = 'create_user')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ED-USER-SECU::polatis1:123::,,,user;', testcase_name = 'change_access_level_for_the_user')

        Username = get_config_arg('login_credentials', 'user_name')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'CANC-USER::%s:123:;' % Username, testcase_name = 'logout_the_current_user')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ACT-USER::polatis1:123:;', testcase_name = 'login_with_edited_user')

	SetOxc = (oxcDict['single_ingress_port'], oxcDict['single_egress_port'])
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ENT-PATCH::%s,%s:123:;' % SetOxc, testcase_name = 'set_oxc_individual_port')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'CANC-USER::polatis1:123:;', testcase_name = 'logout_the_current_user')

        Password = get_config_arg('login_credentials', 'password')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ACT-USER::%s:123::%s;' %(Username, Password), testcase_name = 'login_with_default_user')
        result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-USER-SECU::polatis1:123:;', testcase_name = 'query_created_user')
        nose.tools.assert_in('polatis1', result, "getting error when query created user")
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'DLT-USER-SECU::polatis1:123:;', testcase_name = 'delete_created_user')

    def test_change_access_level_for_created_user_priv_user(self):
        """
        testing change access level for user priv user using edit user settings functionality,
        and validating the result
        """

        self.create_box('test_change_access_level_for_created_user_priv_user')
	self.tl1.delete_all_users()

        result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ENT-USER-SECU::polatis1:123::root,,user;', testcase_name = 'create_user')
        result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ED-USER-SECU::polatis1:123::,,,admin;', testcase_name = 'change_access_level_for_the_user')

        Username = get_config_arg('login_credentials', 'user_name')
        result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'CANC-USER::%s:123:;' % Username, testcase_name = 'logout_the_current_user')
        result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ACT-USER::polatis1:123:;', testcase_name = 'login_with_edited_user')

        SetOxc = (oxcDict['single_ingress_port'], oxcDict['single_egress_port'])
        result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ENT-PATCH::%s,%s:123:;' % SetOxc, testcase_name = 'set_oxc_individual_port')
        result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'CANC-USER::polatis1:123:;', testcase_name = 'logout_the_current_user')

        Password = get_config_arg('login_credentials', 'password')
        result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ACT-USER::%s:123::%s;' %(Username, Password), testcase_name = 'login_with_default_user')

        result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-USER-SECU::polatis1:123:;', testcase_name = 'query_created_user')
        nose.tools.assert_in('polatis1', result, "getting error when query created user")

        result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'DLT-USER-SECU::polatis1:123:;', testcase_name = 'delete_created_user')

    def test_change_access_level_for_created_view_priv_user(self):
        """
        testing change access level for view priv user using edit user settings functionality,
        and validating the result
        """

        self.create_box('test_change_access_level_for_created_view_priv_user')
	self.tl1.delete_all_users()
	
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ENT-USER-SECU::polatis1:123::root,,view;', testcase_name = 'create_user')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ED-USER-SECU::polatis1:123::,,,admin;', testcase_name = 'change_access_level_for_the_user')

        Username = get_config_arg('login_credentials', 'user_name')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'CANC-USER::%s:123:;' % Username, testcase_name = 'logout_the_current_user')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ACT-USER::polatis1:123:;', testcase_name = 'login_with_edited_user')

        SetOxc = (oxcDict['single_ingress_port'], oxcDict['single_egress_port'])
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ENT-PATCH::%s,%s:123:;' % SetOxc, testcase_name = 'set_oxc_individual_port')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'CANC-USER::polatis1:123:;', testcase_name = 'logout_the_current_user')

        Password = get_config_arg('login_credentials', 'password')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ACT-USER::%s:123::%s;' %(Username, Password), testcase_name = 'login_with_default_user')
        result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-USER-SECU::polatis1:123:;', testcase_name = 'query_created_user')
        nose.tools.assert_in('polatis1', result, "getting error when query created user")
        result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'DLT-USER-SECU::polatis1:123:;', testcase_name = 'delete_created_user')

    def test_change_username_and_password_for_created_admin_priv_user(self):
        """
        testing change username and password for admin priv user using edit user settings functionality,
        and validating the result
        """
        self.create_box('test_change_username_and_password_for_created_admin_priv_user')
	self.tl1.delete_all_users()

        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ENT-USER-SECU::polatis1:123::root,,admin;', testcase_name = 'create_user')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ED-USER-SECU::polatis1:123::polatis2,abcd,,;', testcase_name = 'change_username_and_password_for_the_user')

        Username = get_config_arg('login_credentials', 'user_name')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'CANC-USER::%s:123:;' % Username, testcase_name = 'logout_the_current_user')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ACT-USER::polatis2:123::abcd;', testcase_name = 'login_with_edited_user')

        SetOxc = (oxcDict['single_ingress_port'], oxcDict['single_egress_port'])
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ENT-PATCH::%s,%s:123:;' % SetOxc, testcase_name = 'set_oxc_individual_port')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'CANC-USER::polatis1:123:;', testcase_name = 'logout_the_current_user')

        Password = get_config_arg('login_credentials', 'password')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ACT-USER::%s:123::%s;' %(Username, Password), testcase_name = 'login_with_default_user')
        result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-USER-SECU::polatis2:123:;', testcase_name = 'query_created_user')
        nose.tools.assert_in('polatis2', result, "getting error when query created user")
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'DLT-USER-SECU::polatis2:123:;', testcase_name = 'delete_created_user')

    def test_change_username_and_access_priv_for_admin_priv_user(self):
        """
        testing change username and access privilege for admin priv user using edit user settings functionality,
        and validating the result
        """
        self.create_box('test_change_username_and_access_priv_for_admin_priv_user')
	self.tl1.delete_all_users()

        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ENT-USER-SECU::polatis1:123::root,,admin;', testcase_name = 'create_user')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ED-USER-SECU::polatis1:123::polatis2,,,user;', testcase_name = 'change_username_and_password_for_the_user')

        Username = get_config_arg('login_credentials', 'user_name')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'CANC-USER::%s:123:;' % Username, testcase_name = 'logout_the_current_user')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ACT-USER::polatis2:123:;', testcase_name = 'login_with_edited_user')

        SetOxc = (oxcDict['single_ingress_port'], oxcDict['single_egress_port'])
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ENT-PATCH::%s,%s:123:;' % SetOxc, testcase_name = 'set_oxc_individual_port')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'CANC-USER::polatis1:123:;', testcase_name = 'logout_the_current_user')

        Password = get_config_arg('login_credentials', 'password')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ACT-USER::%s:123::%s;' %(Username, Password), testcase_name = 'login_with_default_user')
        result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-USER-SECU::polatis2:123:;', testcase_name = 'query_created_user')
        nose.tools.assert_in('polatis2', result, "getting error when query created user")
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'DLT-USER-SECU::polatis2:123:;', testcase_name = 'delete_created_user')

    def test_change_username_and_password_for_user_priv_user(self):
        """
        testing change username and password for user priv user using edit user settings functionality,
        and validating the result
        """
        self.create_box('test_change_username_and_password_for_user_priv_user')
	self.tl1.delete_all_users()

        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ENT-USER-SECU::polatis1:123::root,,user;', testcase_name = 'create_user')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ED-USER-SECU::polatis1:123::polatis2,abcd,,;', testcase_name = 'change_username_and_password_for_the_user')

        Username = get_config_arg('login_credentials', 'user_name')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'CANC-USER::%s:123:;' % Username, testcase_name = 'logout_the_current_user')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ACT-USER::polatis2:123::abcd;', testcase_name = 'login_with_edited_user')

        SetOxc = (oxcDict['single_ingress_port'], oxcDict['single_egress_port'])
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ENT-PATCH::%s,%s:123:;' % SetOxc, testcase_name = 'set_oxc_individual_port')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'CANC-USER::polatis1:123:;', testcase_name = 'logout_the_current_user')

        Password = get_config_arg('login_credentials', 'password')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ACT-USER::%s:123::%s;' %(Username, Password), testcase_name = 'login_with_default_user')
        result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-USER-SECU::polatis2:123:;', testcase_name = 'query_created_user')
        nose.tools.assert_in('polatis2', result, "getting error when query created user")
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'DLT-USER-SECU::polatis2:123:;', testcase_name = 'delete_created_user')

    def test_change_username_and_access_priv_for_user_priv_user(self):
        """
        testing change username and access privilege for user priv user using edit user settings functionality,
        and validating the result
        """
        self.create_box('test_change_username_and_access_priv_for_user_priv_user')
	self.tl1.delete_all_users()

        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ENT-USER-SECU::polatis1:123::root,,user;', testcase_name = 'create_user')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ED-USER-SECU::polatis1:123::polatis2,,,admin;', testcase_name = 'change_username_and_password_for_the_user')

        Username = get_config_arg('login_credentials', 'user_name')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'CANC-USER::%s:123:;' % Username, testcase_name = 'logout_the_current_user')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ACT-USER::polatis2:123:;', testcase_name = 'login_with_edited_user')

        SetOxc = (oxcDict['single_ingress_port'], oxcDict['single_egress_port'])
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ENT-PATCH::%s,%s:123:;' % SetOxc, testcase_name = 'set_oxc_individual_port')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'CANC-USER::polatis1:123:;', testcase_name = 'logout_the_current_user')

        Password = get_config_arg('login_credentials', 'password')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ACT-USER::%s:123::%s;' %(Username, Password), testcase_name = 'login_with_default_user')
        result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-USER-SECU::polatis2:123:;', testcase_name = 'query_created_user')
        nose.tools.assert_in('polatis2', result, "getting error when query created user")
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'DLT-USER-SECU::polatis2:123:;', testcase_name = 'delete_created_user')

    def test_change_username_and_password_for_created_view_priv_user(self):
        """
        testing change username and password for view priv user using edit user settings functionality,
        and validating the result
        """
        self.create_box('test_change_username_and_password_for_created_view_priv_user')
	self.tl1.delete_all_users()

        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ENT-USER-SECU::polatis1:123::root,,view;', testcase_name = 'create_user')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ED-USER-SECU::polatis1:123::polatis2,abcd,,;', testcase_name = 'change_username_and_password_for_the_user')

        Username = get_config_arg('login_credentials', 'user_name')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'CANC-USER::%s:123:;' % Username, testcase_name = 'logout_the_current_user')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ACT-USER::polatis2:123::abcd;', testcase_name = 'login_with_edited_user')

        SetOxc = (oxcDict['single_ingress_port'], oxcDict['single_egress_port'])
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ENT-PATCH::%s,%s:123:;' % SetOxc, testcase_name = 'set_oxc_individual_port')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'CANC-USER::polatis1:123:;', testcase_name = 'logout_the_current_user')

        Password = get_config_arg('login_credentials', 'password')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ACT-USER::%s:123::%s;' %(Username, Password), testcase_name = 'login_with_default_user')
        result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-USER-SECU::polatis2:123:;', testcase_name = 'query_created_user')
        nose.tools.assert_in('polatis2', result, "getting error when query created user")
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'DLT-USER-SECU::polatis2:123:;', testcase_name = 'delete_created_user')

    def test_change_username_and_access_priv_for_created_view_priv_user(self):
        """
        testing change username and access privilege for view priv user using edit user settings functionality,
        and validating the result
        """
        self.create_box('test_change_username_and_access_priv_for_created_view_priv_user')
	self.tl1.delete_all_users()

        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ENT-USER-SECU::polatis1:123::root,,view;', testcase_name = 'create_user')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ED-USER-SECU::polatis1:123::polatis2,,,admin;', testcase_name = 'change_username_and_password_for_the_user')

        Username = get_config_arg('login_credentials', 'user_name')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'CANC-USER::%s:123:;' % Username, testcase_name = 'logout_the_current_user')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ACT-USER::polatis2:123:;', testcase_name = 'login_with_edited_user')

        SetOxc = (oxcDict['single_ingress_port'], oxcDict['single_egress_port'])
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ENT-PATCH::%s,%s:123:;' % SetOxc, testcase_name = 'set_oxc_individual_port')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'CANC-USER::polatis1:123:;', testcase_name = 'logout_the_current_user')

        Password = get_config_arg('login_credentials', 'password')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ACT-USER::%s:123::%s;' %(Username, Password), testcase_name = 'login_with_default_user')
        result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-USER-SECU::polatis2:123:;', testcase_name = 'query_created_user')
        nose.tools.assert_in('polatis2', result, "getting error when query created user")
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'DLT-USER-SECU::polatis2:123:;', testcase_name = 'delete_created_user')

    def test_query_user_own_settings_for_admin_priv_user(self):
        """
        testing query user own settings for admin priv user functionality,
        and validating the result
        """
        self.create_box('test_query_user_own_settings_for_admin_priv_user')
	self.tl1.delete_all_users()
	
	Username = get_config_arg('login_credentials', 'user_name')
        result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-USER:::123:;', testcase_name = 'query_own_user')
        nose.tools.assert_in(Username , result, "getting error when query created user")

    def test_query_user_own_settings_for_created_admin_priv_user(self):
        """
        testing query user own settings for admin priv user using edit user settings functionality,
        and validating the result
        """
        self.create_box('test_query_user_own_settings_for_created_admin_priv_user')

	self.tl1.delete_all_users()
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ENT-USER-SECU::polatis1:123::root,,admin;', testcase_name = 'create_user')

        Username = get_config_arg('login_credentials', 'user_name')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'CANC-USER::%s:123:;' % Username, testcase_name = 'logout_the_current_user')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ACT-USER::polatis1:123::root;', testcase_name = 'login_with_edited_user')
	result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-USER:::123:;', testcase_name = 'query_own_user')
        nose.tools.assert_in('polatis1', result, "getting error when query created user")
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'CANC-USER::polatis1:123:;', testcase_name = 'logout_the_current_user')

        Password = get_config_arg('login_credentials', 'password')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ACT-USER::%s:123::%s;' %(Username, Password), testcase_name = 'login_with_default_user')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'DLT-USER-SECU::polatis1:123:;', testcase_name = 'delete_created_user')

    def test_query_user_own_settings_for_created_user_priv_user(self):
        """
        testing query user own settings for user priv user using edit user settings functionality,
        and validating the result
        """
        self.create_box('test_query_user_own_settings_for_created_user_priv_user')
	self.tl1.delete_all_users()
	
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ENT-USER-SECU::polatis1:123::root,,user;', testcase_name = 'create_user')

        Username = get_config_arg('login_credentials', 'user_name')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'CANC-USER::%s:123:;' % Username, testcase_name = 'logout_the_current_user')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ACT-USER::polatis1:123::root;', testcase_name = 'login_with_edited_user')
        result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-USER:::123:;', testcase_name = 'query_own_user')
        nose.tools.assert_in('polatis1', result, "getting error when query created user")
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'CANC-USER::polatis1:123:;', testcase_name = 'logout_the_current_user')

        Password = get_config_arg('login_credentials', 'password')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ACT-USER::%s:123::%s;' %(Username, Password), testcase_name = 'login_with_default_user')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'DLT-USER-SECU::polatis1:123:;', testcase_name = 'delete_created_user')

    def test_query_user_own_settings_for_created_view_priv_user(self):
        """
        testing query user own settings for view priv user using edit user settings functionality,
        and validating the result
        """
        self.create_box('test_query_user_own_settings_for_created_view_priv_user')
	self.tl1.delete_all_users()
	
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ENT-USER-SECU::polatis1:123::root,,view;', testcase_name = 'create_user')
        
        Username = get_config_arg('login_credentials', 'user_name')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'CANC-USER::%s:123:;' % Username, testcase_name = 'logout_the_current_user')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ACT-USER::polatis1:123::root;', testcase_name = 'login_with_edited_user')
        result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-USER:::123:;', testcase_name = 'query_own_user')
        nose.tools.assert_in('polatis1', result, "getting error when query created user")
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'CANC-USER::polatis1:123:;', testcase_name = 'logout_the_current_user')

        Password = get_config_arg('login_credentials', 'password')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ACT-USER::%s:123::%s;' %(Username, Password), testcase_name = 'login_with_default_user')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'DLT-USER-SECU::polatis1:123:;', testcase_name = 'delete_created_user')

    def test_query_another_user_settings_for_created_admin_priv_user(self):
        """
        testing query another user settings for admin priv user using edit user settings functionality,
        and validating the result
        """
        self.create_box('test_query_another_user_settings_for_created_admin_priv_user')
	self.tl1.delete_all_users()

        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ENT-USER-SECU::polatis1:123::root,,admin;', testcase_name = 'create_user')

        Username = get_config_arg('login_credentials', 'user_name')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'CANC-USER::%s:123:;' % Username, testcase_name = 'logout_the_current_user')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ACT-USER::polatis1:123::root;', testcase_name = 'login_with_edited_user')
        result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-USER-SECU::%s:123:;'% Username, testcase_name = 'query_own_user')
        nose.tools.assert_in(Username, result, "getting error when query created user")
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'CANC-USER::polatis1:123:;', testcase_name = 'logout_the_current_user')

        Password = get_config_arg('login_credentials', 'password')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ACT-USER::%s:123::%s;' %(Username, Password), testcase_name = 'login_with_default_user')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'DLT-USER-SECU::polatis1:123:;', testcase_name = 'delete_created_user')

    def test_query_all_user_settings_for_admin_priv_user(self):
        """
        testing query all user settings for admin priv user functionality,
        and validating the result
        """
        self.create_box('test_query_user_own_settings_for_admin_priv_user')
	self.tl1.delete_all_users()

        Username = get_config_arg('login_credentials', 'user_name')
        result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-USER-SECU:::123:;', testcase_name = 'query_own_user')
        nose.tools.assert_in(Username , result, "getting error when query created user")

    def test_query_all_user_settings_for_created_admin_priv_user(self):
        """
        testing query all user settings for created admin priv user functionality,
        and validating the result
        """
        self.create_box('test_query_all_user_settings_for_created_admin_priv_user')
	self.tl1.delete_all_users()

        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ENT-USER-SECU::polatis1:123::root,,admin;', testcase_name = 'create_user')

        Username = get_config_arg('login_credentials', 'user_name')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'CANC-USER::%s:123:;' % Username, testcase_name = 'logout_the_current_user')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ACT-USER::polatis1:123::root;', testcase_name = 'login_with_edited_user')
        result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-USER-SECU:::123:;', testcase_name = 'query_own_user')
        nose.tools.assert_in('polatis1', result, "getting error when query created user")
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'CANC-USER::polatis1:123:;', testcase_name = 'logout_the_current_user')

        Password = get_config_arg('login_credentials', 'password')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ACT-USER::%s:123::%s;' %(Username, Password), testcase_name = 'login_with_default_user')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'DLT-USER-SECU::polatis1:123:;', testcase_name = 'delete_created_user')

    def test_change_user_password_as_empty_string(self):
        """
        testing change user password as empty string functionality,
        and validating the result
        """

        self.create_box('test_change_user_password_as_empty_string')
	self.tl1.delete_all_users()

        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ENT-USER-SECU::polatis1:123::root,,admin;', testcase_name = 'create_user')
        result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ED-USER-SECU::polatis1:123::,,,;', testcase_name = 'change_user_password_as_empty_string')

        Username = get_config_arg('login_credentials', 'user_name')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'CANC-USER::%s:123:;' % Username, testcase_name = 'logout_the_current_user')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ACT-USER::polatis1:123:;', testcase_name = 'login_with_edited_user')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'CANC-USER::polatis1:123:;', testcase_name = 'logout_the_current_user')

        Password = get_config_arg('login_credentials', 'password')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ACT-USER::%s:123::%s;' %(Username, Password), testcase_name = 'login_with_default_user')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'DLT-USER-SECU::polatis1:123:;', testcase_name = 'delete_created_user')

    def test_change_admin_priv_user_pwd_using_change_users_pwd_cmd(self):
        """
        testing change admin priv user pwd using change users pwd cmd functionality,
        and validating the result
        """

        self.create_box('test_change_admin_priv_user_pwd_using_change_users_pwd_cmd')
	self.tl1.delete_all_users()

        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ENT-USER-SECU::polatis1:123::root,,admin;', testcase_name = 'create_user')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ED-SECU-PID::polatis1:123::root,pass;', testcase_name = 'change_user_password_as_empty_string')

        Username = get_config_arg('login_credentials', 'user_name')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'CANC-USER::%s:123:;' % Username, testcase_name = 'logout_the_current_user')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ACT-USER::polatis1:123::pass;', testcase_name = 'login_with_edited_user')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'CANC-USER::polatis1:123:;', testcase_name = 'logout_the_current_user')

        Password = get_config_arg('login_credentials', 'password')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ACT-USER::%s:123::%s;' %(Username, Password), testcase_name = 'login_with_default_user')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'DLT-USER-SECU::polatis1:123:;', testcase_name = 'delete_created_user')

    def test_change_user_priv_user_pwd_using_change_users_pwd_cmd(self):
        """
        testing change user priv user pwd using change users pwd cmd functionality,
        and validating the result
        """

        self.create_box('test_change_user_priv_user_pwd_using_change_users_pwd_cmd')
	self.tl1.delete_all_users()

        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ENT-USER-SECU::polatis1:123::root,,user;', testcase_name = 'create_user')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ED-SECU-PID::polatis1:123::root,pass;', testcase_name = 'change_user_password_as_empty_string')

        Username = get_config_arg('login_credentials', 'user_name')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'CANC-USER::%s:123:;' % Username, testcase_name = 'logout_the_current_user')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ACT-USER::polatis1:123::pass;', testcase_name = 'login_with_edited_user')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'CANC-USER::polatis1:123:;', testcase_name = 'logout_the_current_user')

        Password = get_config_arg('login_credentials', 'password')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ACT-USER::%s:123::%s;' %(Username, Password), testcase_name = 'login_with_default_user')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'DLT-USER-SECU::polatis1:123:;', testcase_name = 'delete_created_user')

    def test_change_view_priv_user_pwd_using_change_users_pwd_cmd(self):
        """
        testing change view priv user pwd using change users pwd cmd functionality,
        and validating the result
        """
	
        self.create_box('test_change_view_priv_user_pwd_using_change_users_pwd_cmd')
	self.tl1.delete_all_users()

        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ENT-USER-SECU::polatis1:123::root,,view;', testcase_name = 'create_user')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ED-SECU-PID::polatis1:123::root,pass;', testcase_name = 'change_user_password_as_empty_string')

        Username = get_config_arg('login_credentials', 'user_name')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'CANC-USER::%s:123:;' % Username, testcase_name = 'logout_the_current_user')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ACT-USER::polatis1:123::pass;', testcase_name = 'login_with_edited_user')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'CANC-USER::polatis1:123:;', testcase_name = 'logout_the_current_user')

        Password = get_config_arg('login_credentials', 'password')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ACT-USER::%s:123::%s;' %(Username, Password), testcase_name = 'login_with_default_user')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'DLT-USER-SECU::polatis1:123:;', testcase_name = 'delete_created_user')

    def test_delete_admin_priv_user(self):
	"""
	testing delete admin priv user functionality,
	and validating the result
        """
	
	self.create_box('test_delete_admin_priv_user')
	self.tl1.delete_all_users()
	
	self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ENT-USER-SECU::polatis1:123::root,,admin;', testcase_name = 'create_user')
	result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-USER-SECU::polatis1:123:;' , testcase_name = 'query_user')
        nose.tools.assert_in('ADMIN', result, "getting error when querying")
	self.tl1.execute_tl1_commands(case = 'valid', cmd = 'DLT-USER-SECU::polatis1:123:;', testcase_name = 'delete_created_user')

    def test_delete_user_priv_user(self):
        """
        testing delete user priv user functionality,
        and validating the result
        """

        self.create_box('test_delete_user_priv_user')
	self.tl1.delete_all_users()

        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ENT-USER-SECU::polatis1:123::root,,user;', testcase_name = 'create_user')
        result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-USER-SECU::polatis1:123:;' , testcase_name = 'query_user')
        nose.tools.assert_in('USER', result, "getting error when querying")
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'DLT-USER-SECU::polatis1:123:;', testcase_name = 'delete_created_user')

    def test_delete_view_priv_user(self):
        """
        testing delete view priv user functionality,
        and validating the result
        """

        self.create_box('test_delete_view_priv_user')
	self.tl1.delete_all_users()

        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ENT-USER-SECU::polatis1:123::root,,view;', testcase_name = 'create_user')
        result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-USER-SECU::polatis1:123:;' , testcase_name = 'query_user')
        nose.tools.assert_in('VIEW', result, "getting error when querying")
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'DLT-USER-SECU::polatis1:123:;', testcase_name = 'delete_created_user')

    def test_del_and_create_user_with_same_name_using_diff_uap(self):
        """
        testing test delete and create user with same name but different user access priv functionality,
        and validating the result
        """
        self.create_box('test_del_and_create_user_with_same_name_using_diff_uap')
	self.tl1.delete_all_users()

        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ENT-USER-SECU::polatis1:123::root,,admin;', testcase_name = 'create_user')
        result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-USER-SECU::polatis1:123:;' , testcase_name = 'query_user')
        nose.tools.assert_in('ADMIN', result, "getting error when querying")
	self.tl1.execute_tl1_commands(case = 'valid', cmd = 'DLT-USER-SECU::polatis1:123:;', testcase_name = 'delete_created_user')
	self.tl1.execute_tl1_commands(case = 'valid', cmd = 'ENT-USER-SECU::polatis1:123::root,,user;', testcase_name = 'create_user')
        result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-USER-SECU::polatis1:123:;', testcase_name = 'query_user')
        nose.tools.assert_in('USER', result, "getting error when query created user")
      	self.tl1.execute_tl1_commands(case = 'valid', cmd = 'DLT-USER-SECU::polatis1:123:;', testcase_name = 'delete_created_user')

    def test_disable_autonomous_msg(self):
	"""
        testing test disable autonomous messages functionality,
        and validating the result
        """
	self.create_box('test_disable_autonomous_msg')
	
	PortLabel = (oxcDict['single_ingress_port'])
        result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'OPR-PORT-SHUTTER::%s:123:;' % PortLabel, testcase_name = 'disable_port_aid')
	nose.tools.assert_not_in('Port 1 disabled',result,"getting error when disable")
		
    def test_enable_autonomous_msg(self):
	"""
        testing test enable autonomous messages functionality,
        and validating the result
        """
	self.create_box('test_enable_autonomous_msg')

	self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RLS-ARC-EQPT::REPMGR:123:;', testcase_name = 'enable_aut_msg')
	self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-PORT-SHUTTER::1:123:;', testcase_name = 'enable_aut_msg')
	PortLabel = (oxcDict['single_ingress_port'])
        result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'OPR-PORT-SHUTTER::%s:123:;' %PortLabel, testcase_name = 'disable_port_aid')
        nose.tools.assert_in('Port 1 disabled',result,"getting error when disable port")
	self.tl1.execute_tl1_commands(case = 'valid', cmd = 'OPR-ARC-EQPT::REPMGR:123::IND;', testcase_name = 'disable_aut_msg')

    def test_query_autonomous_msg_using_all(self):
	"""
        testing test query autonomous messages using all functionality,
        and validating the result
        """
	self.create_box('test_query_autonomous_msg_using_all')

	result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-ARC-EQPT::ALL:123:;', testcase_name = 'query_autonomous_msg_using_all')
	nose.tools.assert_in('REPMGR:IND,,',result, "getting error when querying autonomous msg")

    def test_query_autonomous_msg_using_repmgr(self):
        """
        testing test query autonomous messages using repmgr functionality,
        and validating the result
        """
        self.create_box('test_query_autonomous_msg_using_repmgr')
	
        result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-ARC-EQPT::REPMGR:123:;', testcase_name = 'query_autonomous_msg_using_all')
        nose.tools.assert_in('REPMGR:IND,,',result, "getting error when querying autonomous msg")

    def test_query_stored_alarms(self):
        """
        testing test query stored alarms functionality,
        and validating the result
        """
        self.create_box('test_query_stored_alarms')

	result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-ALM-EQPT::ALL:123::;', testcase_name = 'query_stored_alarms')
        nose.tools.assert_in('123 COMPLD', result, "getting error when querying stored alarms")

    def test_query_stored_environmental_alarms(self):
	"""
	testing test query stored environmental alarms functionality,
        and validating the result
        """
	self.create_box('test_query_stored_environmental_alarms')

	result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-ALM-ENV::ALL:123:;', testcase_name = 'query_stored_environmental_alarms')
        nose.tools.assert_in('123 COMPLD', result, "getting error when querying environmental stored alarms")

    def test_query_all_stored_alarms(self):
        """
        testing test query all stored alarms functionality,
        and validating the result
        """
        self.create_box('test_query_all_stored_alarms')

        result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-ALM-ALL::ALL:123:;', testcase_name = 'query_all_stored_alarms')
        nose.tools.assert_in('123 COMPLD', result, "getting error when all querying stored alarms")

    def test_clear_env_alarms_using_ph_value_1(self):
	"""
        testing test clear env alarms using ph value 1 functionality,
        and validating the result
        """
        self.create_box('test_clear_env_alarms_using_ph_value_1')

	self.tl1.execute_tl1_commands(case = 'valid', cmd = 'INIT-SYS::ALARM:123::1;', testcase_name = 'clear_environmental_alarms_using_ph_value_1')
	self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-ALM-ENV::ALL:123:;', testcase_name = 'query_stored_environmental_alarms')

    def test_clear_env_alarms_using_ph_value_2(self):
        """
        testing test clear env alarms using ph value 2 functionality,
        and validating the result
        """
        self.create_box('test_clear_env_alarms_using_ph_value_2')

        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'INIT-SYS::ALARM:123::2;', testcase_name = 'clear_environmental_alarms_using_ph_value_2')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-ALM-EQPT::ALL:123:;', testcase_name = 'query_stored_environmental_alarms')

    def test_clear_env_alarms_using_ph_value_3(self):
        """
        testing test clear env alarms using ph value 3 functionality,
        and validating the result
        """
        self.create_box('test_clear_env_alarms_using_ph_value_3')

        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'INIT-SYS::ALARM:123::3;', testcase_name = 'clear_environmental_alarms_using_ph_value_3')
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-ALM-ALL::ALL:123:;', testcase_name = 'query_stored_environmental_alarms')

    def test_tl1_command_with_tid(self):
	"""
        testing test tl1 command with tid functionality,
        and validating the result
        """
	self.create_box('test_tl1_command_with_tid')

	result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'SET-SID:::123::PolatisOXC;', testcase_name = 'set_TID')
	nose.tools.assert_in('123 COMPLD', result, "getting error when setting SID")
	self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-NETYPE:PolatisOXC::123:;', testcase_name = 'query_network_element_type')
	
    def test_tl1_command_without_tid(self):
        """
        testing test tl1 command without tid functionality,
        and validating the result
        """
        self.create_box('test_tl1_command_without_tid')

        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-NETYPE:::123:;', testcase_name = 'query_network_element_type')

    def test_tl1_command_tid_with_maximum_limit(self):
	"""
        testing test tl1 command tid with maximum limit functionality,
        and validating the result
        """
	self.create_box('test_tl1_command_tid_with_maximum_limit')

	result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'SET-SID:::123::ABCDEFGHIJKLMNOPQRST;', testcase_name = 'set_TID')
        nose.tools.assert_in('123 COMPLD', result, "getting error when setting SID")
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-NETYPE:ABCDEFGHIJKLMNOPQRST::123:;', testcase_name = 'query_network_element_type')
	self.tl1.execute_tl1_commands(case = 'valid', cmd = 'SET-SID:::123::PolatisOXC;', testcase_name = 'set_TID')	

    def test_tl1_command_ctag_using_spaces_with_quotes(self):
        """
        testing test tl1 command ctag using spaces with quotes functionality,
        and validating the result
        """
        self.create_box('test_tl1_command_ctag_using_spaces_with_quotes')

        result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-NETYPE:::"Polatis OXC":;', testcase_name = 'query_network_element_type')
	nose.tools.assert_in('Polatis OXC', result, "getting error when querying")

    def test_tl1_command_tid_using_spaces_with_quotes(self):
	"""
        testing test tl1 command tid using spaces with quotes functionality,
        and validating the result
        """
	self.create_box('test_tl1_command_tid_using_spaces_with_quotes')

 	result = self.tl1.execute_tl1_commands(case = 'valid', cmd = 'SET-SID:::123::"Polatis OXC";', testcase_name = 'set_TID')
        nose.tools.assert_in('Polatis OXC', result, "getting error when setting SID")
        self.tl1.execute_tl1_commands(case = 'valid', cmd = 'RTRV-NETYPE:"Polatis OXC"::123:;', testcase_name = 'query_network_element_type')
	self.tl1.execute_tl1_commands(case = 'valid', cmd = 'SET-SID:::123::PolatisOXC;', testcase_name = 'set_TID')

	"""
	INVALID TESTCASES
	"""

    def test_set_invalid_format_of_switch_time(self):
        """
        testing test set invalid format of switch time functionality,
        and validating the result
        """
        self.create_box('test_set_invalid_format_of_switch_time')

        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ED-DAT::123::31-2016-12;', testcase_name = 'set_invalid_format')
        nose.tools.assert_in('IICT', result, "getting error when setting invalid time")
 	nose.tools.assert_in('Parse error at offset 13 in command', result, "getting error when setting invalid time")	
	
    def test_set_switch_time_using_invalid_year(self):
        """
        testing test set invalid year of switch time functionality,
        and validating the result
        """
        self.create_box('test_set_switch_time_using_invalid_year')

        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ED-DAT:::123::2038-08-16;', testcase_name = 'set_invalid_year')
        nose.tools.assert_in('SSTP', result, "getting error when setting invalid time")


    def test_set_switch_time_using_invalid_month(self):
        """
        testing test set invalid month of switch time functionality,
        and validating the result
        """
        self.create_box('test_set_switch_time_using_invalid_month')

        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ED-DAT:::123::16-13-16;', testcase_name = 'set_invalid_month')
        nose.tools.assert_in('IDNV', result, "getting error when setting invalid time")
	nose.tools.assert_in('Bad parameter value', result, "getting error when setting invalid time")

    def test_set_switch_time_using_invalid_date(self):
        """
        testing test set invalid date of switch time functionality,
        and validating the result
        """
        self.create_box('test_set_switch_time_using_invalid_date')

        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ED-DAT:::123::16-08-33;', testcase_name = 'set_invalid_date')
        nose.tools.assert_in('IDNV', result, "getting error when setting invalid time")
        nose.tools.assert_in('Bad parameter value', result, "getting error when setting invalid time")

    def test_set_invalid_session_timeout_for_admin(self):
        """
        testing test set invalid session timeout for admin functionality,
        and validating the result
        """
        self.create_box('test_set_invalid_session_timeout_for_admin')

        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ED-EQPT::TIMEOUT:123:::ADMIN=@#$#$$;', testcase_name = 'set_invalid_timeout')
        nose.tools.assert_in('IPNV', result, "getting error when setting invalid session timeout")
	nose.tools.assert_in('Parameter not valid', result, "getting error when setting invalid session time")

    def test_set_invalid_max_session_timeout_for_admin(self):
        """
        testing test set invalid max session timeout for admin functionality,
        and validating the result
        """
        self.create_box('test_set_invalid_max_session_timeout_for_admin')

        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ED-EQPT::TIMEOUT:123:::ADMIN=61;', testcase_name = 'set_invalid_maximum')
        nose.tools.assert_in('IPNV', result, "getting error when setting invalid session timeout")
        nose.tools.assert_in('Parameter not valid', result, "getting error when setting invalid session time")

    def test_set_invalid_negative_value_session_timeout_for_admin(self):
        """
        testing test set invalid negative value session timeout for admin functionality,
        and validating the result
        """
        self.create_box('test_set_invalid_negative_value_session_timeout_for_admin')

        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ED-EQPT::TIMEOUT:123:::ADMIN=-2;', testcase_name = 'set_invalid_negative_value')
        nose.tools.assert_in('IPNV', result, "getting error when setting invalid session timeout")
        nose.tools.assert_in('Parameter not valid', result, "getting error when setting invalid session time")

    def test_set_invalid_session_timeout_for_user(self):
        """
        testing test set invalid session timeout for user functionality,
        and validating the result
        """
        self.create_box('test_set_invalid_session_timeout_for_user')

        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ED-EQPT::TIMEOUT:123:::USER=@#$#$$;', testcase_name = 'set_invalid_timeout')
        nose.tools.assert_in('IPNV', result, "getting error when setting invalid session timeout")
        nose.tools.assert_in('Parameter not valid', result, "getting error when setting invalid session time")

    def test_set_invalid_max_session_timeout_for_user(self):
        """
        testing test set invalid max session timeout for user functionality,
        and validating the result
        """
        self.create_box('test_set_invalid_max_session_timeout_for_user')

        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ED-EQPT::TIMEOUT:123:::USER=61;', testcase_name = 'set_invalid_maximum')
        nose.tools.assert_in('IPNV', result, "getting error when setting invalid session timeout")
        nose.tools.assert_in('Parameter not valid', result, "getting error when setting invalid session time")

    def test_set_invalid_negative_value_session_timeout_for_user(self):
        """
        testing test set invalid negative value session timeout for user functionality,
        and validating the result
        """
        self.create_box('test_set_invalid_negative_value_session_timeout_for_user')

        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ED-EQPT::TIMEOUT:123:::USER=-2;', testcase_name = 'set_invalid_negavive_value')
        nose.tools.assert_in('IPNV', result, "getting error when setting invalid session timeout")
        nose.tools.assert_in('Parameter not valid', result, "getting error when setting invalid session time")

    def test_set_invalid_user_access_level_for_session_timeout(self):
        """
        testing test set invalid user access level for session timeout functionality,
        and validating the result
        """
        self.create_box('test_set_invalid_user_access_level_for_session_timeout')

        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ED-EQPT::TIMEOUT:123:::adm=0;', testcase_name = 'set_invalid_access_level')
        nose.tools.assert_in('IPNV', result, "getting error when setting invalid timeout")
        nose.tools.assert_in('Unexpected parameter adm in block 2', result, "getting error when setting invalid timeout")

    def test_set_invalid_maximum_value_system_identifier(self):
        """
        testing test set invalid maximum value system identifier functionality,
        and validating the result
        """
        self.create_box('test_set_invalid_maximum_value_system_identifier')

        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'SET-SID:::1::Jasmine_Lotus_Rose_Lily; ', testcase_name = 'set_invalid_sys_identifer')
        nose.tools.assert_in('IDNV', result, "getting error when setting invalid system identifier")

    def test_set_invalid_system_identifier(self):
        """
        testing test set invalid system identifier functionality,
        and validating the result
        """
        self.create_box('test_set_invalid_system_identifier')

        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'SET-SID:::1::**raja;', testcase_name = 'set_invalid_sys_identifer')
        nose.tools.assert_in('IDNV', result, "getting error when setting invalid system identifier")


#    def test_set_invalid_ph_value_for_reset_system(self):
        """
        testing test set invalid ph value for reset system functionality,
        and validating the result
        """
#        self.create_box('test_set_invalid_ph_value_for_reset_system')

#        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'INIT-SYS::SYSTEM:123::2;', testcase_name = 'query_invalid_ph_value')
#        nose.tools.assert_in('IDNV', result, "getting error when query_ invalid ph value")

    def test_query_invalid_startup_mode_as_numbers(self):
        """
        testing test query invalid parameter as number for switch start up mode functionality,
        and validating the result
        """
        self.create_box('test_query_invalid_startup_mode_as_numbers')

        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'RTRV-EQPT::BOOT:123:::PARAMETER=12345;', testcase_name = 'query_invalid_parameter')
        nose.tools.assert_in('IPNV', result, "getting error when query invalid parameter")

    def test_query_invalid_startup_mode_as_characters(self):
        """
        testing test query invalid parameter as characters for switch start up mode functionality,
        and validating the result
        """
        self.create_box('test_query_invalid_startup_mode_as_characters')

        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'RTRV-EQPT::BOOT:123:::PARAMETER=$#@$%;', testcase_name = 'query_invalid_parameter')
        nose.tools.assert_in('IPNV', result, "getting error when query invalid parameter")

    def test_query_invalid_startup_mode_as_text(self):
        """
        testing test query invalid parameter as text for switch start up mode functionality,
        and validating the result
        """
        self.create_box('test_query_invalid_startup_mode_as_text')

        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'RTRV-EQPT::BOOT:123:::PARAMETER=SUN;', testcase_name = 'query_invalid_parameter')
        nose.tools.assert_in('IPNV', result, "getting error when query invalid parameter")

    def test_set_invalid_startup_mode_as_numbers(self):
        """
        testing test set invalid parameter as numbers for switch start up mode functionality,
        and validating the result
        """
        self.create_box('test_set_invalid_startup_mode_as_numbers')

        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ED-EQPT::BOOT:123:::MODE=12345; ', testcase_name = 'set_invalid_parameter')
        nose.tools.assert_in('IPNV', result, "getting error when setting invalid parameter")

    def test_set_invalid_startup_mode_as_characters(self):
        """
        testing test set invalid parameter as characters for switch start up mode functionality,
        and validating the result
        """
        self.create_box('test_set_invalid_startup_mode_as_characters')

        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ED-EQPT::BOOT:123:::MODE=@$;', testcase_name = 'set_invalid_parameter')
        nose.tools.assert_in('IDNV', result, "getting error when setting invalid parameter")
	nose.tools.assert_in('Invalid value @$', result, "getting error when setting invalid parameter")

    def test_set_invalid_startup_mode_as_text(self):
        """
        testing test set invalid parameter as text for switch start up mode functionality,
        and validating the result
        """
        self.create_box('test_set_invalid_startup_mode_as_text')

        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ED-EQPT::BOOT:123:::MODE=sun;', testcase_name = 'set_invalid_parameter')
        nose.tools.assert_in('IDNV', result, "getting error when setting invalid parameter")
	nose.tools.assert_in('Invalid value sun', result, "getting error when setting invalid parameter")

    def test_set_oxc_with_invalid_ingress_port(self):
        """
        testing set invalid ingress port functionality,
        and validating the result
        """

        self.create_box('test_set_oxc_with_invalid_egress_port')

        SetOxc = (oxcDict['invalid_ingress_port'], oxcDict['single_egress_port'])
        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ENT-PATCH::%s,%s:123:;' % SetOxc, testcase_name = 'set_invalid_ingress_port')
 	nose.tools.assert_in('IDNV', result, "getting error when setting invalid ingress port")
 	nose.tools.assert_in('Invalid OXC port: 100', result, "getting error when setting invalid ingress port")

    def test_set_oxc_with_invalid_egress_port(self):
        """
        testing set invalid egress port functionality,
        and validating the result
        """

        self.create_box('test_set_oxc_with_invalid_egress_port')

        SetOxc = (oxcDict['single_ingress_port'], oxcDict['invalid_egress_port'])
        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ENT-PATCH::%s,%s:123:;' % SetOxc, testcase_name = 'set_invalid_egress_port')
        nose.tools.assert_in('IDNV', result, "getting error when setting invalid egress port")
        nose.tools.assert_in('Invalid OXC port: 200', result, "getting error when setting invalid egress port")

    def test_set_oxc_with_invalid_ingress_and_egress_using_empty(self):
        """
        testing set invalid empty ingress and egress port functionality,
        and validating the result
        """

        self.create_box(' test_set_oxc_with_invalid_ingress_and_egress_using_empty')

        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ENT-PATCH::,:123:;' , testcase_name = 'set_invalid_empty_port')
        nose.tools.assert_in('IIAC', result, "getting error when setting invalid empty port")
        nose.tools.assert_in('Empty parameters', result, "getting error when setting invalid empty port")

    def test_set_oxc_with_invalid_ingress_and_egress_using_text (self):
        """
        testing set invalid text ingress and egress port functionality,
        and validating the result
        """

        self.create_box('test_set_oxc_with_invalid_ingress_and_egress_using_text ')

        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ENT-PATCH::a,b:123:;' , testcase_name = 'set_invalid_text')
        nose.tools.assert_in('IDNV', result, "getting error when setting invalid text port")
        nose.tools.assert_in('Invalid OXC port', result, "getting error when setting invalid text port")

    def test_set_oxc_with_invalid_ingress_and_egress_using_neg_num(self):
        """
        testing set invalid negative numbers ingress and egress port functionality,
        and validating the result
        """

        self.create_box('test_set_oxc_with_invalid_ingress_and_egress_using_neg_num')

        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ENT-PATCH::-10,-49:123:;' , testcase_name = 'set_invalid_negative_numbers')
        nose.tools.assert_in('IDNV', result, "getting error when setting invalid negative number port")
        nose.tools.assert_in('Invalid OXC port', result, "getting error when setting invalid negative number port")

    def test_set_oxc_with_invalid_ingress_and_egress_using_char(self):
        """
        testing set invalid characters ingress and egress port functionality,
        and validating the result
        """

        self.create_box('test_set_oxc_with_invalid_ingress_and_egress_using_char')

        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ENT-PATCH::@,#:123:;' , testcase_name = 'set_invalid_characters')
        nose.tools.assert_in('IDNV', result, "getting error when setting invalid characters port")
        nose.tools.assert_in('Invalid OXC port', result, "getting error when setting invalid characters port")

    def test_delete_oxc_with_invalid_port(self):
        """
        testing delete invalid oxc port functionality,
        and validating the result
        """

        self.create_box('test_delete_oxc_with_invalid_port')
	
	DelOxc = (oxcDict['invalid_ingress_port'])
	result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'DLT-PATCH::%s:123:;' % DelOxc , testcase_name = 'delete_invalid_oxc_port')	
	nose.tools.assert_in('IDNV', result, "getting error when delete invalid ingress port")
        nose.tools.assert_in('Invalid OXC port: 100', result, "getting error when delete invalid ingress port")

    def test_delete_invalid_text_ingress_and_egress_port(self):
        """
        testing delete invalid text ingress and egress port functionality,
        and validating the result
        """

        self.create_box('test_delete_invalid_text_ingress_and_egress_port')

        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'DLT-PATCH::a&b:123:;' , testcase_name = 'delete_invalid_text')
        nose.tools.assert_in('IDNV', result, "getting error when setting invalid text port")
        nose.tools.assert_in('Invalid OXC port: a', result, "getting error when setting invalid text port")

    def test_delete_invalid_negative_numbers_ingress_and_egress_port(self):
        """
        testing delete invalid negative numbers ingress and egress port functionality,
        and validating the result
        """

        self.create_box('test_delete_invalid_negative_numbers_ingress_and_egress_port')

        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'DLT-PATCH::-10:123:;' , testcase_name = 'delete_invalid_negative_numbers')
        nose.tools.assert_in('IDNV', result, "getting error when setting invalid negative number port")
        nose.tools.assert_in('Invalid OXC port: -10', result, "getting error when setting invalid negative number port")

    def test_delete_invalid_characters_ingress_and_egress_port(self):
        """
        testing delete invalid characters ingress and egress port functionality,
        and validating the result
        """

        self.create_box('test_delete_invalid_characters_ingress_and_egress_port')

        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'DLT-PATCH::@:123:;' , testcase_name = 'delete_invalid_characters')
        nose.tools.assert_in('IDNV', result, "getting error when setting invalid characters port")
        nose.tools.assert_in('Invalid OXC port: @', result, "getting error when setting invalid characters port")

    def test_set_invalid_characters_in_port_label(self):
        """
        testing test set invalid characters in port label functionality,
        and validating the result
        """

        self.create_box('test_set_invalid_characters_in_port_label')

        PortLabel = (oxcDict['single_ingress_port'])
        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ED-PORT-LABEL::%s:123:::LABEL=@#$;' % PortLabel, testcase_name = 'set_invalid_port_label')
	nose.tools.assert_in('IPNV', result, "getting error when setting invalid characters port")


    def test_set_invalid_maximum_port_label(self):
        """
        testing test set invalid maximum port label functionality,
        and validating the result
        """

        self.create_box('test_set_invalid_maximum_port_label')

        PortLabel = (oxcDict['single_ingress_port'])
        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ED-PORT-LABEL::%s:123:::LABEL=ABCDEFGHIJKLMNOPQRSTUVWXYZ;' % PortLabel, testcase_name = 'set_invalid_port_label')
        nose.tools.assert_in('IPNV', result, "getting error when setting invalid maximum port")

    def test_delete_invalid_port_label(self):
        """
        testing test delete invalid port label functionality,
        and validating the result
        """

        self.create_box('test_delete_invalid_port_label')

        PortLabel = (oxcDict['invalid_ingress_port'])
        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'DLT-PORT-LABEL::%s:123:;'%PortLabel, testcase_name = 'delete_invalid_port_label')
        nose.tools.assert_in('IDNV', result, "getting error when querying invalid port")
        nose.tools.assert_in('Invalid OXC port', result, "getting error when deleting invalid port")
	
    def test_query_invalid_port_label(self):
        """
        testing test query invalid port label functionality,
        and validating the result
        """

        self.create_box('test_query_invalid_port_label')

	QueryLabel = (oxcDict['invalid_ingress_port'])
        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd ='RTRV-PORT-LABEL::%s:123:;'%QueryLabel,testcase_name = 'query_invalid_port_label')
        nose.tools.assert_in('IDNV', result, "getting error when querying invalid port")

  
    def test_enable_invalid_port_aid(self):
        """
        testing enable invalid port aid functionality,
        and validating the result
        """

        self.create_box('test_enable_invalid_port_aid')


        PortLabel = (oxcDict['invalid_ingress_port'])
        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'RLS-PORT-SHUTTER::%s:123:;' %PortLabel, testcase_name = 'enable_invalid_port_aid')
 	nose.tools.assert_in('IDNV', result, "getting error when enable invalid port")
        nose.tools.assert_in('Invalid OXC port: 100', result, "getting error when enable invalid port")

    def test_disable_invalid_port_aid(self):
        """
        testing disable invalid port aid functionality,
        and validating the result
        """

        self.create_box('test_disable_invalid_port_aid')


        PortLabel = (oxcDict['invalid_ingress_port'])
        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'OPR-PORT-SHUTTER::%s:123:;' % PortLabel, testcase_name = 'disable_invalid_port_aid')	
	nose.tools.assert_in('IDNV', result, "getting error when disable invalid port")
        nose.tools.assert_in('Invalid OXC port: 100', result, "getting error when disable invalid port")

    def test_query_invalid_port_aid(self):
        """
        testing query invalid port aid functionality,
        and validating the result
        """

        self.create_box('test_query_invalid_port_aid')

	QueryLabel = (oxcDict['invalid_ingress_port'])
        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'RTRV-PORT-SHUTTER::%s:123:;' %QueryLabel, testcase_name = 'query_invalid_port_label')
	nose.tools.assert_in('IDNV', result, "getting error when querying invalid port")
	
    def test_enable_multiple_invalid_port_aid(self):
        """
        testing enable multiple invalid port aid functionality,
        and validating the result
        """

        self.create_box('test_enable_multiple_invalid_port_aid')


        PortLabel = oxcDict['invalid_ingress_port']
        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'RLS-PORT-SHUTTER::%s&%s:123:;' %(PortLabel, PortLabel), testcase_name = 'enable_multiple_invalid_port_aid')
        nose.tools.assert_in('IDNV', result, "getting error when enable invalid port")

    def test_disable_multiple_invalid_port_aid(self):
        """
        testing disable invalid multiple port aid functionality,
        and validating the result
        """

        self.create_box('test_disable_multiple_invalid_port_aid')


        PortLabel = (oxcDict['invalid_ingress_port'])
        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'OPR-PORT-SHUTTER::%s&%s:123:;' %(PortLabel,  PortLabel), testcase_name = 'disable_multiple_invalid_port_aid')
        nose.tools.assert_in('IDNV', result, "getting error when disable invalid port")

    def test_login_with_invalid_username(self):
	"""
        testing test login with invalid username functionality,
        and validating the result
        """

	self.create_box('test_login_with_invalid_username')
	self.tl1.delete_all_users()

	Username = get_config_arg('login_credentials', 'user_name')
	self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'CANC-USER::%s:123:;' % Username, testcase_name = 'logout_the_current_user')
	
	Password = get_config_arg('login_credentials', 'password')
        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ACT-USER::invalid:123::%s;' %Password, testcase_name = 'login_with_invalid_username')
	nose.tools.assert_in('PICC', result, "getting error when login with invalid username")
	nose.tools.assert_not_in('User invalid authentication failure', result, "getting error when login with invalid username")	
	self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ACT-USER::%s:123::%s;' %(Username, Password), testcase_name = 'login_with_default_user')

    def test_login_with_invalid_password(self):
        """
        testing test login with invalid password functionality,
        and validating the result
        """

        self.create_box('test_login_with_invalid_password')
	self.tl1.delete_all_users()

        Username = get_config_arg('login_credentials', 'user_name')
        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'CANC-USER::%s:123:;' % Username, testcase_name = 'logout_the_current_user')

        Password = get_config_arg('login_credentials', 'password')
        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ACT-USER::%s:123::invalid;' %Username, testcase_name = 'login_with_invalid_password')
        nose.tools.assert_in('PICC', result, "getting error when login with invalid password")
        nose.tools.assert_not_in('User admin authentication failure', result, "getting error when login with invalid password")
        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ACT-USER::%s:123::%s;' %(Username, Password), testcase_name = 'login_with_default_user')

    def test_login_with_invalid_extra_block(self):
        """
        testing test login with invalid extra block functionality,
        and validating the result
        """

        self.create_box('test_login_with_invalid_extra_block')
	self.tl1.delete_all_users()

        Username = get_config_arg('login_credentials', 'user_name')
        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'CANC-USER::%s:123:;' % Username, testcase_name = 'logout_the_current_user')

        Password = get_config_arg('login_credentials', 'password')
        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ACT-USER::%s::123::%s;' %(Username, Password), testcase_name = 'login_with_invalid_password')
        nose.tools.assert_in('IICT', result, "getting error when login with invalid password")
        nose.tools.assert_in('Parse error at offset 17 in command', result, "getting error when login with invalid password")
        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ACT-USER::%s:123::%s;' %(Username, Password), testcase_name = 'login_with_default_user')

    def test_login_with_invalid_empty_username(self):
        """
        testing test login with invalid empty username functionality,
        and validating the result
        """

        self.create_box('test_login_with_invalid_empty_username')
	self.tl1.delete_all_users()

        Username = get_config_arg('login_credentials', 'user_name')
        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'CANC-USER::%s:123:;' % Username, testcase_name = 'logout_the_current_user')

        Password = get_config_arg('login_credentials', 'password')
        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ACT-USER:::123::%s;' %Password, testcase_name = 'login_with_invalid_empty_username')
        nose.tools.assert_in('IIAC', result, "getting error when login with invalid empty username")
        nose.tools.assert_in('Too few parameters (0/1)', result, "getting error when login with invalid empty username")
        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ACT-USER::%s:123::%s;' %(Username, Password), testcase_name = 'login_with_default_user')

    def test_login_with_invalid_empty_pwd(self):
        """
        testing test login with invalid empty password functionality,
        and validating the result
        """

        self.create_box('test_login_with_invalid_empty_pwd')
	self.tl1.delete_all_users()

        Username = get_config_arg('login_credentials', 'user_name')
        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'CANC-USER::%s:123:;' % Username, testcase_name = 'logout_the_current_user')

        Password = get_config_arg('login_credentials', 'password')
        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ACT-USER::%s:123::;' %Username, testcase_name = 'login_with_invalid_empty_password')
        nose.tools.assert_in('IPMS', result, "getting error when login with invalid empty password")
        nose.tools.assert_in('Too few parameters (0/1) in block 1', result, "getting error when login with invalid empty password")
        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ACT-USER::%s:123::%s;' %(Username, Password), testcase_name = 'login_with_default_user')

    def test_login_with_invalid_empty_username_and_pwd(self):
        """
        testing test login with invalid empty username and password functionality,
        and validating the result
        """

        self.create_box('test_login_with_invalid_empty_username_and_pwd')
	self.tl1.delete_all_users()

        Username = get_config_arg('login_credentials', 'user_name')
        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'CANC-USER::%s:123:;' % Username, testcase_name = 'logout_the_current_user')

        Password = get_config_arg('login_credentials', 'password')
        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ACT-USER:::123::;' , testcase_name = 'login_with_invalid_empty_password')
        nose.tools.assert_in('IIAC', result, "getting error when login with invalid empty username and password")
        nose.tools.assert_in('Too few parameters (0/1)', result, "getting error when login with invalid empty username and password")
        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ACT-USER::%s:123::%s;' %(Username, Password), testcase_name = 'login_with_default_user')

    def test_login_with_invalid_username_as_char(self):
        """
        testing test login with invalid username as characters functionality,
        and validating the result
        """

        self.create_box('test_login_with_invalid_username_as_char')
	self.tl1.delete_all_users()

        Username = get_config_arg('login_credentials', 'user_name')
        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'CANC-USER::%s:123:;' % Username, testcase_name = 'logout_the_current_user')

        Password = get_config_arg('login_credentials', 'password')
        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ACT-USER::@$:123::%s;' %Password, testcase_name = 'login_with_invalid_username')
        nose.tools.assert_in('PICC', result, "getting error when login with invalid username as characters")
        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ACT-USER::%s:123::%s;' %(Username, Password), testcase_name = 'login_with_default_user')

    def test_login_with_invalid_pwd_as_char(self):
        """
        testing test login with invalid password as characters functionality,
        and validating the result
        """

        self.create_box('test_login_with_invalid_pwd_as_char')
	self.tl1.delete_all_users()

        Username = get_config_arg('login_credentials', 'user_name')
        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'CANC-USER::%s:123:;' % Username, testcase_name = 'logout_the_current_user')

        Password = get_config_arg('login_credentials', 'password')
        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ACT-USER::%s:123::@$;' %Username, testcase_name = 'login_with_invalid_password')
        nose.tools.assert_in('PICC', result, "getting error when login with invalid password as characters")
        nose.tools.assert_not_in('User ad authentication failure', result, "getting error when login with invalid password as characters")
        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ACT-USER::%s:123::%s;' %(Username, Password), testcase_name = 'login_with_default_user')

    def test_login_with_invalid_username_as_capital_letters(self):
	"""
        testing test login with invalid username as capital letters functionality,
        and validating the result
        """

	self.create_box('test_login_with_invalid_username_as_capital_letters')
	self.tl1.delete_all_users()	

	Username = get_config_arg('login_credentials', 'user_name')
        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'CANC-USER::%s:123:;' % Username, testcase_name = 'logout_the_current_user')

        Password = get_config_arg('login_credentials', 'password')
        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ACT-USER::Admin:123::%s;' %Password, testcase_name = 'login_with_invalid_username')
	nose.tools.assert_in('PICC', result, "getting error when login with invalid username as capital letters")
        nose.tools.assert_not_in('User Admin authentication failure',result,"getting error when login with invalid username as capital letters")
        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ACT-USER::%s:123::%s;' %(Username, Password), testcase_name = 'login_with_default_user')

    def test_login_with_invalid_pwd_as_capital_letters(self):
        """
        testing test login with invalid password as capital letters functionality,
        and validating the result
        """

        self.create_box('test_login_with_invalid_pwd_as_capital_letters')
	self.tl1.delete_all_users()

        Username = get_config_arg('login_credentials', 'user_name')
        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'CANC-USER::%s:123:;' % Username, testcase_name = 'logout_the_current_user')

        Password = get_config_arg('login_credentials', 'password')
        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ACT-USER::%s:123::Root;' %Username, testcase_name = 'login_with_invalid_password')
        nose.tools.assert_in('PICC', result, "getting error when login with invalid password as capital letters")
        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ACT-USER::%s:123::%s;' %(Username, Password), testcase_name = 'login_with_default_user')

    def test_logout_with_invalid_username(self):
        """
        testing test logout with invalid username functionality,
        and validating the result
        """

        self.create_box('test_logout_with_invalid_username')
	self.tl1.delete_all_users()

        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'CANC-USER::invalid:123:;', testcase_name = 'logout_with_invalid_username')
	nose.tools.assert_in('PICC', result, "getting error when logout with invalid username")
        nose.tools.assert_in(' Permission denied ',result,"getting error when logout with invalid username")

    def test_logout_with_invalid_username_above_max_limit(self):
        """
        testing test logout with invalid username above maximum limit functionality,
        and validating the result
        """

        self.create_box('test_logout_with_invalid_username_above_max_limit')
	self.tl1.delete_all_users()

        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'CANC-USER::invalidusernameinvalidusername:123:;', testcase_name = 'logout_with_invalid_username')
        nose.tools.assert_in('PICC', result, "getting error when logout with invalid username above max limit")
        nose.tools.assert_in(' Permission denied ',result,"getting error when logout with invalid username above max limit")

    def test_logout_with_invalid_username_using_char(self):
        """
        testing test logout with invalid username using characters functionality,
        and validating the result
        """

        self.create_box('test_logout_with_invalid_username_using_char')
	self.tl1.delete_all_users()

        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'CANC-USER::@$:123:;', testcase_name = 'logout_with_invalid_username')
        nose.tools.assert_in('PICC', result, "getting error when logout with invalid username using characters")
        nose.tools.assert_in(' Permission denied ',result,"getting error when logout with invalid username using characters")

    def test_logout_with_invalid_username_as_capital_letters(self):
        """
        testing test logout with invalid username as capital letters functionality,
        and validating the result
        """

        self.create_box('test_logout_with_invalid_username_as_capital_letters')
	self.tl1.delete_all_users()

        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'CANC-USER::ADMIN:123:;', testcase_name = 'logout_with_invalid_username')
        nose.tools.assert_in('PICC', result, "getting error when logout with invalid username as capital letters")
        nose.tools.assert_in(' Permission denied ',result,"getting error when logout with invalid username as capital letters")


    def test_logout_with_invalid_admin_user(self):
        """
        testing test logout with invalid admin user for created user priv user functionality,
        and validating the result
        """
        self.create_box('test_logout_with_invalid_admin_user')
	self.tl1.delete_all_users()

        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ENT-USER-SECU::polatis1:123::root,,user;', testcase_name = 'create_user')

        Username = get_config_arg('login_credentials', 'user_name')
        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'CANC-USER::%s:123:;' % Username, testcase_name = 'logout_the_current_user')
        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ACT-USER::polatis1:123::root;', testcase_name = 'login_with_edited_user')
	result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'CANC-USER::%s:123:;' %Username, testcase_name = 'logout_the_current_user')
	nose.tools.assert_in('PICC', result, "getting error when logout with invalid admin user")
        nose.tools.assert_in('Permission denied',result,"getting error when logout with invalid admin user")
        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ACT-USER::%s:123::%s;' %(Username, Password), testcase_name = 'login_with_default_user')
	self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'DLT-USER-SECU::polatis1:123:;', testcase_name = 'delete_created_user')
	
    def test_create_user_with_invalid_pwd_as_char(self):
        """
        testing test create user with invalid password as characters functionality,
        and validating the result
        """
        self.create_box('test_create_user_with_invalid_pwd_as_char')
	self.tl1.delete_all_users()

        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ENT-USER-SECU::polatis1:123::@$,,admin;', testcase_name = 'create_user')
	nose.tools.assert_in('PICC', result, "getting error when creating with invalid user")
        nose.tools.assert_in('Permission denied',result,"getting error when creating with invalid user")
	self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'DLT-USER-SECU::polatis1:123:;', testcase_name = 'delete_created_user')
		
    def test_create_user_with_invalid_username_as_char(self):
        """
        testing test create user with invalid username as characters functionality,
        and validating the result
        """
        self.create_box('test_create_user_with_invalid_username_as_char')
        self.tl1.delete_all_users()

        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ENT-USER-SECU::polatis1@#$:123::root,,admin;', testcase_name = 'create_user')
        nose.tools.assert_in('PICC', result, "getting error when creating with invalid user")
        nose.tools.assert_in('Permission denied',result,"getting error when creating with invalid user")

    def test_create_and_delete_with_invalid_user(self):
        """
        testing test create and_delete user with invalid created user functionality,
        and validating the result
        """
        self.create_box('test_create_and_delete_with_invalid_user')
        self.tl1.delete_all_users()

	self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ENT-USER-SECU::polatis1:123::root,,admin;', testcase_name = 'create_user')
        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ENT-USER-SECU::polatis1:123::root,,admin;', testcase_name = 'create_user')
        nose.tools.assert_in('IDNV', result, "getting error when creatig with invalid admin user")
        nose.tools.assert_in('User exists',result,"getting error when creating with invalid admin user")
        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'DLT-USER-SECU::polatis1:123:;', testcase_name = 'delete_created_user')
	result1 = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'DLT-USER-SECU::polatis1:123:;', testcase_name = 'delete_created_user')
	nose.tools.assert_in('IDNV', result1, "getting error when deleting")
        nose.tools.assert_in('User does not exist',result1,"getting error when deleting")

    def test_create_user_with_invalid_user_access_priv(self):
        """
        testing test create user with invalid username as characters functionality,
        and validating the result
        """
        self.create_box('test_create_user_with_invalid_user_access_priv')
        self.tl1.delete_all_users()

        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ENT-USER-SECU::polatis1:123::root,,polatis;', testcase_name = 'create_user')
        nose.tools.assert_in('IPNV', result, "getting error when creating with invalid user")
        nose.tools.assert_in('Invalid user access privilege',result,"getting error when creating with invalid user")

    def test_delete_invalid_user_as_numbers(self):
        """
        testing test delete invalid user as numbers functionality,
        and validating the result
        """
        self.create_box('test_delete_invalid_user_as_numbers')
        self.tl1.delete_all_users()

	result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'DLT-USER-SECU::5147:123:;', testcase_name = 'delete_created_user')
      	nose.tools.assert_in('IDNV', result, "getting error when deleting")
        nose.tools.assert_in('User does not exist',result,"getting error when deleting")

    def test_invalid_login_as_user_and_create_new_user(self):
        """
        testing test invalid login as user and create new user functionality,
        and validating the result
        """

        self.create_box('test_invalid_login_as_user_and_create_new_user')

        self.tl1.delete_all_users()
        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ENT-USER-SECU::polatis1:123::root,,user;', testcase_name = 'create_user')

        Username = get_config_arg('login_credentials', 'user_name')
        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'CANC-USER::%s:123:;' % Username, testcase_name = 'logout_the_current_user')
        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ACT-USER::polatis1:123::root;', testcase_name = 'login_with_edited_user')
	result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ENT-USER-SECU::polatis2:123::root,,admin;', testcase_name = 'create_user')
	nose.tools.assert_in('PICC', result, "getting error when creating invalid user")
        nose.tools.assert_in('Permission denied',result,"getting error when creating invalid user")
        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'CANC-USER::polatis1:123:;', testcase_name = 'logout_the_current_user')

        Password = get_config_arg('login_credentials', 'password')
        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ACT-USER::%s:123::%s;' %(Username, Password), testcase_name = 'login_with_default_user')
        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'DLT-USER-SECU::polatis1:123:;', testcase_name = 'delete_created_user')

    def test_invalid_login_as_view_and_create_new_user(self):
        """
        testing test invalid login as view and create new user functionality,
        and validating the result
        """

        self.create_box('test_invalid_login_as_view_and_create_new_user')

        self.tl1.delete_all_users()
        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ENT-USER-SECU::polatis1:123::root,,view;', testcase_name = 'create_user')

        Username = get_config_arg('login_credentials', 'user_name')
        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'CANC-USER::%s:123:;' % Username, testcase_name = 'logout_the_current_user')
        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ACT-USER::polatis1:123::root;', testcase_name = 'login_with_edited_user')
        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ENT-USER-SECU::polatis2:123::root,,admin;', testcase_name = 'create_user')
        nose.tools.assert_in('PICC', result, "getting error when creating invalid user")
        nose.tools.assert_in('Permission denied',result,"getting error when creating invalid user")
        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'CANC-USER::polatis1:123:;', testcase_name = 'logout_the_current_user')

        Password = get_config_arg('login_credentials', 'password')
        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ACT-USER::%s:123::%s;' %(Username, Password), testcase_name = 'login_with_default_user')
        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'DLT-USER-SECU::polatis1:123:;', testcase_name = 'delete_created_user')

    def test_edit_username_with_invalid_char(self):
        """
        testing test edit username with invalid characterts functionality,
        and validating the result
        """

        self.create_box('test_edit_username_with_invalid_char')

        self.tl1.delete_all_users()
        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ENT-USER-SECU::polatis1:123::root,,admin;', testcase_name = 'create_user')

	result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'RTRV-USER-SECU:::123:;', testcase_name = 'query_all_user')
	nose.tools.assert_in('polatis1', result, "getting error when querying user")
	result1 = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ED-USER-SECU::polatis1:123::@polatis2,,,admin;', testcase_name = 'edit_user')
        nose.tools.assert_in('PICC', result1, "getting error when creating invalid user")
        nose.tools.assert_in('Permission denied',result1,"getting error when creating invalid user")
	self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'DLT-USER-SECU::polatis1:123:;', testcase_name = 'delete_created_user')

    def test_edit_password_with_invalid_char(self):
        """
        testing test edit password with invalid characterts functionality,
        and validating the result
        """

        self.create_box('test_edit_password_with_invalid_char')

        self.tl1.delete_all_users()
        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ENT-USER-SECU::polatis1:123::root,,admin;', testcase_name = 'create_user')

        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'RTRV-USER-SECU:::123:;', testcase_name = 'query_all_user')
        nose.tools.assert_in('polatis1', result, "getting error when querying user")
        result1 = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ED-USER-SECU::polatis1:123::,@root,,admin;', testcase_name = 'edit_user')
        nose.tools.assert_in('PICC', result1, "getting error when creating invalid user")
        nose.tools.assert_in('Permission denied',result1,"getting error when creating invalid user")
        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'DLT-USER-SECU::polatis1:123:;', testcase_name = 'delete_created_user')

    def test_edit_user_access_priv_with_invalid_text(self):
        """
        testing test edit user access priv with invalid text functionality,
        and validating the result
        """

        self.create_box('test_edit_user_access_priv_with_invalid_text')

        self.tl1.delete_all_users()
        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ENT-USER-SECU::polatis1:123::root,,admin;', testcase_name = 'create_user')

        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'RTRV-USER-SECU:::123:;', testcase_name = 'query_all_user')
        nose.tools.assert_in('polatis1', result, "getting error when querying user")
        result1 = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ED-USER-SECU::polatis1:123::,,,abcd;', testcase_name = 'edit_user')
        nose.tools.assert_in('IPNV', result1, "getting error when creating invalid user")
        nose.tools.assert_in('Invalid user access privilege',result1,"getting error when creating invalid user")
        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'DLT-USER-SECU::polatis1:123:;', testcase_name = 'delete_created_user')

    def test_query_another_user_with_invalid_username(self):
	"""
	testing test query another user with invalid username functionality,
	and validating the result
	"""

	self.create_box('test_query_another_user_with_invalid_username')

	self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'RTRV-USER-SECU:::123:;', testcase_name = 'query_all_user')
	result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'RTRV-USER-SECU::abcd:123:;', testcase_name = 'query_invalid_user')
        nose.tools.assert_in('IDNV', result, "getting error when creating invalid user")
        nose.tools.assert_in('User does not exist',result,"getting error when creating invalid user")
	
    def test_query_another_user_with_invalid_users_login(self):
        """
        testing test query another user with invalid users login functionality,
        and validating the result
        """

        self.create_box('test_query_another_user_with_invalid_users_login')

        self.tl1.delete_all_users()
        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ENT-USER-SECU::polatis1:123::root,,user;', testcase_name = 'create_user')

        Username = get_config_arg('login_credentials', 'user_name')
        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'CANC-USER::%s:123:;' % Username, testcase_name = 'logout_the_current_user')
        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ACT-USER::polatis1:123::root;', testcase_name = 'login_with_edited_user')
        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'RTRV-USER-SECU::%s:123:;' % Username, testcase_name = 'query_user')
        nose.tools.assert_in('SRCN', result, "getting error when creating invalid user")
        nose.tools.assert_in('User not in the admin group',result,"getting error when creating invalid user")
	result1 = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'RTRV-USER-SECU:::123:;', testcase_name = 'query_all_user')
        nose.tools.assert_in('SRCN', result1, "getting error when creating invalid user")
        nose.tools.assert_in('User not in the admin group',result1,"getting error when creating invalid user")
        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'CANC-USER::polatis1:123:;', testcase_name = 'logout_the_current_user')

        Password = get_config_arg('login_credentials', 'password')
        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ACT-USER::%s:123::%s;' %(Username, Password), testcase_name = 'login_with_default_user')
        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'DLT-USER-SECU::polatis1:123:;', testcase_name = 'delete_created_user')

    def test_query_another_user_with_invalid_view_login(self):
        """
        testing test query another user with invalid view login functionality,
        and validating the result
        """

        self.create_box('test_query_another_user_with_invalid_view_login')

        self.tl1.delete_all_users()
        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ENT-USER-SECU::polatis1:123::root,,view;', testcase_name = 'create_user')

        Username = get_config_arg('login_credentials', 'user_name')
        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'CANC-USER::%s:123:;' % Username, testcase_name = 'logout_the_current_user')
        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ACT-USER::polatis1:123::root;', testcase_name = 'login_with_edited_user')
        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'RTRV-USER-SECU::%s:123:;' % Username, testcase_name = 'query_user')
        nose.tools.assert_in('SRCN', result, "getting error when creating invalid user")
        nose.tools.assert_in('User not in the admin group',result,"getting error when creating invalid user")
        result1 = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'RTRV-USER-SECU:::123:;', testcase_name = 'query_all_user')
        nose.tools.assert_in('SRCN', result1, "getting error when creating invalid user")
        nose.tools.assert_in('User not in the admin group',result1,"getting error when creating invalid user")
        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'CANC-USER::polatis1:123:;', testcase_name = 'logout_the_current_user')

        Password = get_config_arg('login_credentials', 'password')
        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ACT-USER::%s:123::%s;' %(Username, Password), testcase_name = 'login_with_default_user')
        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'DLT-USER-SECU::polatis1:123:;', testcase_name = 'delete_created_user')

    def test_change_user_pwd_with_invalid_char(self):
        """
        testing test test change user pwd with invalid characters functionality,
        and validating the result
        """

        self.create_box('test_change_user_pwd_with_invalid_char')

        self.tl1.delete_all_users()
        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ENT-USER-SECU::polatis1:123::root,,view;', testcase_name = 'create_user')

	result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ED-SECU-PID::polatis1:123::root,@@##;', testcase_name = 'change_pwd')
	nose.tools.assert_in('PICC', result, "getting error when creating invalid user")
        nose.tools.assert_in('Permission denied',result,"getting error when creating invalid user")
	self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'DLT-USER-SECU::polatis1:123:;', testcase_name = 'delete_created_user')

    def test_delete_invalid_user(self):
        """
        testing test delete invalid user functionality,
        and validating the result
        """

        self.create_box('test_delete_invalid_user')

        self.tl1.delete_all_users()
        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'DLT-USER-SECU::delete:123:;', testcase_name = 'create_user')

        nose.tools.assert_in('IDNV', result, "getting error when creating invalid user")
        nose.tools.assert_in('User does not exist',result,"getting error when creating invalid user")


    def test_delete_user_with_invalid_user_priv(self):
        """
        testing test delete user with invalid user priv functionality,
        and validating the result
        """

        self.create_box('test_delete_user_with_invalid_user_priv')

        self.tl1.delete_all_users()
        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ENT-USER-SECU::polatis1:123::root,,user;', testcase_name = 'create_user')

        Username = get_config_arg('login_credentials', 'user_name')
	
        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'CANC-USER::%s:123:;' % Username, testcase_name = 'logout_the_current_user')
        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ACT-USER::polatis1:123::root;', testcase_name = 'login_with_edited_user')
        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'DLT-USER-SECU::%s:123;' % Username, testcase_name = 'query_user')
        nose.tools.assert_in('PICC', result, "getting error when deleting invalid user")
        nose.tools.assert_in('User not in the admin group',result,"getting error when creating invalid user")
        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'CANC-USER::polatis1:123:;', testcase_name = 'logout_the_current_user')

        Password = get_config_arg('login_credentials', 'password')
        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ACT-USER::%s:123::%s;' %(Username, Password), testcase_name = 'login_with_default_user')
        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'DLT-USER-SECU::polatis1:123:;', testcase_name = 'delete_created_user')

    def test_delete_user_with_invalid_view_priv(self):
        """
        testing test delete user with invalid view priv functionality,
        and validating the result
        """

        self.create_box('test_delete_user_with_invalid_view_priv')

        self.tl1.delete_all_users()
        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ENT-USER-SECU::polatis1:123::root,,view;', testcase_name = 'create_user')

        Username = get_config_arg('login_credentials', 'user_name')

        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'CANC-USER::%s:123:;' % Username, testcase_name = 'logout_the_current_user')
        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ACT-USER::polatis1:123::root;', testcase_name = 'login_with_edited_user')
        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'DLT-USER-SECU::%s:123;' % Username, testcase_name = 'query_user')
        nose.tools.assert_in('PICC', result, "getting error when deleting invalid user")
        nose.tools.assert_in('User not in the admin group',result,"getting error when creating invalid user")
        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'CANC-USER::polatis1:123:;', testcase_name = 'logout_the_current_user')

        Password = get_config_arg('login_credentials', 'password')
        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'ACT-USER::%s:123::%s;' %(Username, Password), testcase_name = 'login_with_default_user')
        self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'DLT-USER-SECU::polatis1:123:;', testcase_name = 'delete_created_user')

    def test_disable_autonomous_msg_using_invalid_aid(self):
        """
        testing test disable autonomous msg using invalid aid functionality,
        and validating the result
        """
	
	self.create_box('test_disable_autonomous_msg_using_invalid_aid')
	
	result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'OPR-ARC-EQPT::Invalid:123::IND;', testcase_name = 'disable_aut_msg')
	nose.tools.assert_in('IIAC', result, "getting error when disabling aut msg invalid aid")

    def test_enable_autonomous_msg_using_invalid_aid(self):
        """
        testing test enable autonomous msg using invalid aid functionality,
        and validating the result
        """

        self.create_box('test_enable_autonomous_msg_using_invalid_aid')

        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'RLS-ARC-EQPT::Invalid:123:;', testcase_name = 'disable_aut_msg')
        nose.tools.assert_in('IIAC', result, "getting error when enabling aut msg invalid aid")

    def test_query_autonomous_msg_using_invalid_aid(self):
        """
        testing test query autonomous msg using invalid aid functionality,
        and validating the result
        """

        self.create_box('test_query_autonomous_msg_using_invalid_aid')

        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'RTRV-ARC-EQPT::Invalid:123:;', testcase_name = 'query_aut_msg')
        nose.tools.assert_in('IIAC', result, "getting error when querying aut msg invalid aid")

    def test_query_stored_equip_alarms_using_invalid_aid(self):
        """
        testing test query stored equip alarms using invalid aid functionality,
        and validating the result
        """

        self.create_box('test_query_stored_equip_alarms_using_invalid_aid')

        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'RTRV-ALM-EQPT::Invalid:123::cr,,sa;', testcase_name = 'query_stord_equip_alarms')
        nose.tools.assert_in('IIAC', result, "getting error when querying stored equip alarms using invalid aid")

    def test_query_stored_env_alarms_using_invalid_aid(self):
        """
        testing test query stored env alarms using invalid aid functionality,
        and validating the result
        """

        self.create_box('test_query_stored_env_alarms_using_invalid_aid')

        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'RTRV-ALM-ENV::Invalid:123:;', testcase_name = 'query_stord_env_alarms')
        nose.tools.assert_in('IIAC', result, "getting error when querying stored env alarms using invalid aid")

    def test_query_all_stored_alarms_using_invalid_aid(self):
        """
        testing test query all stored alarms using invalid aid functionality,
        and validating the result
        """

        self.create_box('test_query_all_stored_alarms_using_invalid_aid')

        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'RTRV-ALM-ALL::Invalid:123:;', testcase_name = 'query_stord_env_alarms')
        nose.tools.assert_in('IIAC', result, "getting error when querying all stored alarms using invalid aid")

    def test_clear_stored_msgs_using_invalid_ph_value(self):
        """
        testing test clear stored messages using invalid ph value functionality,
        and validating the result
        """

        self.create_box('test_clear_stored_msgs_using_invalid_ph_value')

        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'INIT-SYS::ALARM:123::8;', testcase_name = 'query_stord_env_alarms')
        nose.tools.assert_in('IPNV', result, "getting error when clearing stored msgs using invalid ph value")

    def test_invalid_tl1_command_without_ctag(self):
	"""
        testing test invalid tl1 command without ctag functionality,
        and validating the result
        """
	
	self.create_box('test_invalid_tl1_command_without_ctag')

	result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'INIT-SYS::ALARM:::1;', testcase_name = 'tl1_cmd_without_ctag')
	nose.tools.assert_in('IICT', result, "getting error when clearing stored msgs without ctag")
	nose.tools.assert_in('Parse error at offset 17 in command', result, "getting error when clearing stored msgs without ctag")

    def test_tl1_command_with_invalid_tid_as_char(self):
	"""
        testing test tl1 command with invalid tid as characters functionality,
        and validating the result
        """

	self.create_box('test_tl1_command_with_invalid_tid_as_char')
	
	result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'INIT-SYS:@#@#:ALARM:123::1;', testcase_name = 'tl1_cmd_with_invalid_tid')
	nose.tools.assert_in('IITA', result, "getting error when clearing stored msgs using invalid tid")
        nose.tools.assert_in('Parse error at offset 10 in command', result, "getting error when clearing stored msgs using invalid tid")

    def test_tl1_command_with_invalid_tid_as_numbers(self):
        """
        testing test tl1 command with invalid tid as numbers functionality,
        and validating the result
        """

        self.create_box('test_tl1_command_with_invalid_tid_as_numbers')

        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'INIT-SYS:9942:ALARM:123::1;', testcase_name = 'tl1_cmd_with_invalid_tid')
        nose.tools.assert_in('IITA', result, "getting error when clearing stored msgs using invalid tid")
        nose.tools.assert_in('Parse error at offset 10 in command', result, "getting error when clearing stored msgs using invalid tid")

    def test_tl1_cmd_with_invalid_tid_above_max_limit(self):
        """
        testing test tl1 command with invalid tid above maximum limit functionality,
        and validating the result
        """

        self.create_box('test_tl1_cmd_with_invalid_tid_above_max_limit')

	self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'SET-SID:::123::Jasmine_Lotus_Rose_Lily;', testcase_name = 'set_tid')
        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'RTRV-ARC-EQPT:Jasmine_Lotus_Rose_Lily:ALL:123;', testcase_name = 'tl1_cmd_with_above_max_limit')
        nose.tools.assert_in('IITA', result, "getting error when querying all stored alarms using invalid tid")
        nose.tools.assert_in('Mismatched TID', result, "getting error when querying all stored alarms using invalid tid")
	
    def test_tl1_cmd_with_invalid_aid_as_numbers(self):
        """
        testing test tl1 command with invalid aid as numbers functionality,
        and validating the result
        """

        self.create_box('test_tl1_cmd_with_invalid_aid_as_numbers')

        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'RTRV-EQPT::9999:123:::PARAMETER=SIZE;', testcase_name = 'tl1_cmd_with_invalid_aid')
        nose.tools.assert_in('IIAC', result, "getting error when querying session timeout period using invalid aid")


    def test_tl1_cmd_with_invalid_aid_as_text(self):
        """
        testing test tl1 command with invalid aid as text functionality,
        and validating the result
        """

        self.create_box('test_tl1_cmd_with_invalid_aid_as_text')

        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'RTRV-EQPT::ABCD:123:::PARAMETER=SIZE;', testcase_name = 'tl1_cmd_with_invalid_aid')
        nose.tools.assert_in('IIAC', result, "getting error when querying session timeout period using invalid aid")

    def test_tl1_cmd_with_invalid_aid_as_char(self):
        """
        testing test tl1 command with invalid aid as characters functionality,
        and validating the result
        """

        self.create_box('test_tl1_cmd_with_invalid_aid_as_char')

        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'RTRV-EQPT::@#@#:123:::PARAMETER=SIZE;', testcase_name = 'tl1_cmd_with_invalid_aid')
        nose.tools.assert_in('IIAC', result, "getting error when querying session timeout period using invalid aid")

    def test_invalid_tl1_cmd(self):
        """
        testing test invalid tl1_command functionality,
        and validating the result
        """

        self.create_box('test_invalid_tl1_cmd')

        result = self.tl1.execute_tl1_commands(case = 'invalid', cmd = 'RTRV-EQPT::timeout:::PARAMETER=USER;', testcase_name = 'invalid_tl1_cmd')
        nose.tools.assert_in('IICT', result, "getting error when querying session timeout period using invalid tl1 cmd")
	nose.tools.assert_in('Parse error at offset 20 in command', result, "getting error when querying session timeout period using invalid tl1 cmd")
