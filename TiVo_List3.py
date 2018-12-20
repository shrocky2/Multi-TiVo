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
gpio_ports = {'Bedroom TiVo Pause':"10000##TiVoBedroom",
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

class device_handler(debounce_handler):
    """Triggers on/off based on 'device' selected.
       Publishes the IP address of the Echo making the request.
    """

    TRIGGERS = {"Bedroom TiVo Pause":50041,
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
