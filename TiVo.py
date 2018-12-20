""" 
   Author: Originally Surendra Kane
   Edited by: shrocky2
  Script to control your TiVo using a Amazon Echo.
  This script originally was used to control the gpio ports on the raspberry pi, so you will see remnants of that code. 
"""

import fauxmo
import logging
import time
#Telnet Added Information
import getpass
import sys
import telnetlib
#End Telnet Added Information

from debounce_handler import debounce_handler

logging.basicConfig(level=logging.DEBUG)

print " Control+C to exit program"
#Edit this section to personalize your TV Channels. The channel number is listed after each station.
#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
gpio_ports = {'Livingroom TiVo Pause':"10000##TiVoLivingRoom",
              'Livingroom A.B.C.':"6.1##TiVoLivingRoom",
              'Livingroom N.B.C.':"10.1##TiVoLivingRoom",
              'Livingroom C.B.S.':"3.1##TiVoLivingRoom",
              'Livingroom Fox':"47.1##TiVoLivingRoom",
              'Livingroom Comedy Central':"754##TiVoLivingRoom",
              'Livingroom T.B.S.':"767##TiVoLivingRoom",
              'Livingroom HGTV':"762##TiVoLivingRoom",
              'Livingroom ESPN':"800##TiVoLivingRoom",
              'Livingroom The CW':"787##TiVoLivingRoom",
              'Livingroom A and E':"795##TiVoLivingRoom",
              'Livingroom Cartoon Network':"872##TiVoLivingRoom",


              'Office TiVo Pause':"10000##TiVoOffice",
              'Office A.B.C.':"6.1##TiVoOffice",
              'Office N.B.C.':"10.1##TiVoOffice",
              'Office C.B.S.':"3.1##TiVoOffice",
              'Office Fox':"47.1##TiVoOffice",
              'Office Comedy Central':"754##TiVoOffice",
              'Office T.B.S.':"767##TiVoOffice",
              'Office HGTV':"762##TiVoOffice",
              'Office ESPN':"800##TiVoOffice",
              'Office The CW':"787##TiVoOffice",
              'Office A and E':"795##TiVoOffice",
              'Office Cartoon Network':"872##TiVoOffice",

              'Bedroom TiVo Pause':"10000##TiVoBedroom",
              'Bedroom A.B.C.':"6.1##TiVoBedroom",
              'Bedroom N.B.C.':"10.1##TiVoBedroom",
              'Bedroom C.B.S.':"3.1##TiVoBedroom",
              'Bedroom Fox':"47.1##TiVoBedroom",
              'Bedroom Comedy Central':"754##TiVoBedroom",
              'Bedroom T.B.S.':"767##TiVoBedroom",
              'Bedroom HGTV':"762##TiVoBedroom",
              'Bedroom ESPN':"800##TiVoBedroom",
              'Bedroom The CW':"787##TiVoBedroom",
              'Bedroom A and E':"795##TiVoBedroom",
              'Bedroom Cartoon Network':"872##TiVoBedroom"}
#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------


class device_handler(debounce_handler):
    """Triggers on/off based on 'device' selected.
       Publishes the IP address of the Echo making the request.
    """
    TRIGGERS = {"Livingroom TiVo Pause":50001,
                "Livingroom A.B.C.":50002,
                "Livingroom N.B.C.":50003,
                "Livingroom C.B.S.":50004,
                "Livingroom Fox":50005,
                "Livingroom Comedy Central":50006,
                "Livingroom T.B.S.":50007,
                "Livingroom HGTV":50008,
                "Livingroom ESPN":50009,
                "Livingroom The CW":50010,
                "Livingroom A and E":50011,
                "Livingroom Cartoon Network":50012,

                "Office TiVo Pause":50021,
                "Office A.B.C.":50022,
                "Office N.B.C.":50023,
                "Office C.B.S.":50024,
                "Office Fox":50025,
                "Office Comedy Central":50026,
                "Office T.B.S.":50027,
                "Office HGTV":50028,
                "Office ESPN":50029,
                "Office The CW":50030,
                "Office A and E":50031,
                "Office Cartoon Network":50032,

                "Bedroom TiVo Pause":50041,
                "Bedroom A.B.C.":50042,
                "Bedroom N.B.C.":50043,
                "Bedroom C.B.S.":50044,
                "Bedroom Fox":50045,
                "Bedroom Comedy Central":50046,
                "Bedroom T.B.S.":50047,
                "Bedroom HGTV":50048,
                "Bedroom ESPN":50049,
                "Bedroom The CW":50050,
                "Bedroom A and E":50051,
                "Bedroom Cartoon Network":50052}

    def trigger(self,port,state):
      PortSplit = port.split("##")
      channel = PortSplit[0]
      TiVoName = PortSplit[1]
      If TiVoName = "TiVoLivingRoom":
        TiVo_IP_Address = "192.168.0.1"  #IP address of the LivingRoom TiVo
      If TiVoName = "TiVoOffice":
        TiVo_IP_Address = "192.168.0.2"  #IP address of the Office TiVo
      If TiVoName = "TiVoBedroom":
        TiVo_IP_Address = "192.168.0.3"  #IP address of the Bedroom TiVo

      print 'port:',  port,  "   state:", state
      if state == True: #If the ON command is given, it will run this code
        if channel < 10000: #Numbers Less Than 10000 are channels, numbers above 10000 are Services like Netflix
                try:
                        tn = telnetlib.Telnet(TiVo_IP_Address, "31339")
                        tn.write('SETCH '+ str(channel).replace("."," ") + '\r')
                        tn.close()
                        print "Channel Changed to", channel
                except:
                        print "Telnet Error, Check TiVo IP Address"
                print " "
        else:
                if channel == 10000: #TiVo Paused
                        try:
                         tn = telnetlib.Telnet(TiVo_IP_Address, "31339")
                         tn.write("IRCODE PAUSE\r")
                         tn.close()
                         print "TiVo Paused"
                        except:
                         print "Telnet Error, Check TiVo IP Address"

                          
                if channel == 10001: #Netflix
                        try:
                         tn = telnetlib.Telnet(TiVo_IP_Address, "31339")
                         tn.write("IRCODE TIVO\r")
                         time.sleep(.4)
                         tn.write("IRCODE DOWN\r")
                         time.sleep(.4)
                         tn.write("IRCODE DOWN\r")
                         time.sleep(.4)
                         tn.write("IRCODE RIGHT\r")
                         time.sleep(1)
                         tn.write("IRCODE SELECT\r")
                         tn.close()
                         print "TiVo App Netflix is Starting"
                        except:
                         print "Telnet Error, Check TiVo IP Address"

                if channel == 10002: #Hulu
                        print "Hulu Code Needed"
                if channel == 10003: #YouTube
                        try:
                         tn = telnetlib.Telnet(TiVo_IP_Address, "31339")
                         tn.write("IRCODE TIVO\r")
                         time.sleep(.4)
                         tn.write("IRCODE DOWN\r")
                         time.sleep(.4)
                         tn.write("IRCODE DOWN\r")
                         time.sleep(1)
                         tn.write("IRCODE RIGHT\r")
                         time.sleep(1)
                         tn.write("IRCODE DOWN\r")
                         time.sleep(.4)
                         tn.write("IRCODE DOWN\r")
                         time.sleep(.4)
                         tn.write("IRCODE DOWN\r")
                         time.sleep(.4)
                         tn.write("IRCODE SELECT\r")
                         tn.close()
                         print "TiVo App YouTube is Starting"
                        except:
                         print "Telnet Error, Check TiVo IP Address"
                print " "
               
      else: #If the OFF command is given, it will run this code
        if channel == 10001 or channel == 10002 or channel == 10003: #Netflix, Hulu, or YoutTube OFF command is given
                try:
                        tn = telnetlib.Telnet(TiVo_IP_Address, "31339")
                        tn.write("IRCODE LIVETV\r")
                        tn.close()
                        print "TiVo LiveTv Button Pressed"
                except:
                        print "Telnet Error, Check TiVo IP Address"
        print " "


    def act(self, client_address, state, name):
        print "State", state, "on", name, "from client @", client_address, "port:",gpio_ports[str(name)]
        self.trigger(gpio_ports[str(name)],state)
        return True

if __name__ == "__main__":
    # Startup the fauxmo server
    fauxmo.DEBUG = True
    p = fauxmo.poller()
    u = fauxmo.upnp_broadcast_responder()
    u.init_socket()
    p.add(u)

    # Register the device callback as a fauxmo handler
    d = device_handler()
    for trig, port in d.TRIGGERS.items():
        fauxmo.fauxmo(trig, u, p, None, port, d)

    # Loop and poll for incoming Echo requests
    logging.debug("Entering fauxmo polling loop")
    print " "
    while True:
        try:
            # Allow time for a ctrl-c to stop the process
            p.poll(100)
            time.sleep(0.1)
        except Exception, e:
            logging.critical("Critical exception: " + str(e))
            break
