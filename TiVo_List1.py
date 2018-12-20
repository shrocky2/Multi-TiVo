""" 
   Original Author:  Surendra Kane
   Edited by: shrocky2
  Script to control your TiVo using a Amazon Echo.
"""

import fauxmo
import logging
import time

from debounce_handler import debounce_handler

logging.basicConfig(level=logging.DEBUG)

print " Control+C to exit program"
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
              'Livingroom Cartoon Network':"872##TiVoLivingRoom"}

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
                "Livingroom Cartoon Network":50012}

    def trigger(self,port,state):
      TiVo_IP_Address = "192.168.0.47"
      print 'port:',  port,  "   state:", state
      if state == True:
        print ""
      else:
        print ""

    def act(self, client_address, state, name):
        print "State", state, "on", name, "from client @", client_address, "gpio port:",gpio_ports[str(name)]
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
