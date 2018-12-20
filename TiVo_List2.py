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
gpio_ports = {'Office TiVo Pause':"10000##TiVoOffice",
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
              'Office Cartoon Network':"872##TiVoOffice"}

class device_handler(debounce_handler):
    """Triggers on/off based on 'device' selected.
       Publishes the IP address of the Echo making the request.
    """

    TRIGGERS = {"Office TiVo Pause":50021,
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
                "Office Cartoon Network":50032}

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
