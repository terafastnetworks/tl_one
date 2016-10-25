from config import get_config_arg


def get_single_ingress_port():
        """get the existing ingress list from config.txt file
        """
        ex_ingress_ports = []

        try:
            ingressPrtRange = (
                get_config_arg(
                    "cross_connects",
                    "ingress_ports_range")).split(
                    '-')

            for i in range(int(ingressPrtRange[0]), int(ingressPrtRange[1]) + 1):
                ex_ingress_ports.append(i)


            for i in range(0, 1):
                return ex_ingress_ports [i]
        except Exception as err:
            print "INFO : \nPlease give valid port format under [cross-connects] in confif.txt \
- seperated by hypen 'Eg : 1-48'"
            #print "Error : " , err
            exit()


def get_single_egress_port():
        """get the existing egress port list from config.txt file
        """
        ex_egress_ports = []
       
        try: 
            egressPrtRange = (
                get_config_arg(
                    "cross_connects",
                    "egress_ports_range")).split(
                            '-')

            for j in range(int(egressPrtRange[0]), int(egressPrtRange[1]) + 1):
                ex_egress_ports.append(j)


            for i in range(0, 1):
                return ex_egress_ports[i]
        except Exception as err:
            print "INFO : \nPlease give valid port format under [cross-connects] in confif.txt \
- seperated by hypen 'Eg : 1-48'"
            #print "Error : " , err
            exit()
        



def get_multiple_ingress_ports():
        """get the existing ingress list from config.txt file
        """
        ingress_port = []
        ex_ingress_ports = []

        try:
            ingressPrtRange = (
                get_config_arg(
                    "cross_connects",
                    "ingress_ports_range")).split(
                    '-')

            for i in range(int(ingressPrtRange[0]), int(ingressPrtRange[1]) + 1):
                ex_ingress_ports.append(i)

            for prt1, prt2, prt3 in zip(range(0, 1), range(6, 7), range(14, 15)):
                return ex_ingress_ports[prt1], ex_ingress_ports[prt2], ex_ingress_ports[prt3] 
        except Exception as err:
            print "INFO : \nPlease give valid port format under [cross-connects] in confif.txt \
- seperated by hypen 'Eg : 1-48'"
            #print "Error : " , err
            exit()

def get_multiple_egress_ports():
        """get the existing egress port list from config.txt file
        """
        egress_port = []
        ex_egress_ports = []

        try:
            egressPrtRange = (
                get_config_arg(
                    "cross_connects",
                    "egress_ports_range")).split(
                            '-')

            for j in range(int(egressPrtRange[0]), int(egressPrtRange[1]) + 1):
                ex_egress_ports.append(j)
            for prt1, prt2, prt3 in zip(range(0, 1), range(6, 7), range(14, 15)):
                return ex_egress_ports[prt1], ex_egress_ports[prt2], ex_egress_ports[prt3] 
        except Exception as err:
            print "INFO : \nPlease give valid port format under [cross-connects] in confif.txt \
- seperated by hypen 'Eg : 1-48'"
            #print "Error : " , err
            exit()

def get_grouped_ingress_ports():
        """get the existing ingress list from config.txt file
        """
        ingress_port = []
        ex_ingress_ports = []

        try:
            ingressPrtRange = (
                get_config_arg(
                    "cross_connects",
                    "ingress_ports_range")).split(
                    '-')

            for i in range(int(ingressPrtRange[0]), int(ingressPrtRange[1]) + 1):
                ex_ingress_ports.append(i)

            for prt1, prt2 in zip(range(0, 1), range(6, 7)):
                return ex_ingress_ports[prt1], ex_ingress_ports[prt2]
        except Exception as err:
            print "INFO : \nPlease give valid port format under [cross-connects] in confif.txt \
- seperated by hypen 'Eg : 1-48'"
            #print "Error : " , err
            exit()

def get_grouped_egress_ports():
        """get the existing egress port list from config.txt file
        """
        egress_port = []
        ex_egress_ports = []

        try:
            egressPrtRange = (
                get_config_arg(
                    "cross_connects",
                    "egress_ports_range")).split(
                            '-')

            for j in range(int(egressPrtRange[0]), int(egressPrtRange[1]) + 1):
                ex_egress_ports.append(j)
            for prt1, prt2 in zip(range(0, 1), range(6, 7)):
                return ex_egress_ports[prt1], ex_egress_ports[prt2]
        except Exception as err:
            print "INFO : \nPlease give valid port format under [cross-connects] in confif.txt \
- seperated by hypen 'Eg : 49-96'"
            #print "Error : " , err
            exit()


def get_mixed_ports():
        """get the existing egress port list from config.txt file
        """
        ports = []
        ex_ports = []

        try:
            PrtRange = (
                get_config_arg(
                    "cross_connects",
                    "ingress_ports_range")).split(
                            '-')

            for j in range(int(PrtRange[0]), 2*(int(PrtRange[1])) + 1):
                ex_ports.append(j)

            for prt1, prt2, prt3 in zip(range(int(PrtRange[0]), int(PrtRange[0])+1), range(int(PrtRange[1])+ 1, int(PrtRange[1]) + 2), range(int(PrtRange[1]) + 5, int(PrtRange[1]) + 6)):
                return ex_ports[prt1], ex_ports[prt2], ex_ports[prt3] 
        except Exception as err:
            print "INFO : \nPlease give valid port format under [cross-connects] in confif.txt \
- seperated by hypen 'Eg : 1-48'"
            #print "Error : " , err
            exit()
