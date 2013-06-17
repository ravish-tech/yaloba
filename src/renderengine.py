import os
import jinja2
import tfl
import logging
import operator

class renderengine:
    ravtfl = tfl.ravTFL()
    def render(self, lat, lng, radius):
        JINJA_ENVIRONMENT = jinja2.Environment(
            loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
            extensions=['jinja2.ext.autoescape'])
        template = JINJA_ENVIRONMENT.get_template('base.html')
        stops = self.ravtfl.getbusstops2(lat, lng, radius, False)
        logging.info(stops)
        preparedstops = []
        for stop in stops:
            s = []
            s.append(stop[0])
            s.append(stop[1])
            s.append(stop[2])
            if len(stop)>2:
                s.append(self.preparebuslist(stop[0]))
                s.append(stop[3])
            preparedstops.append(s)
        return template.render(stops = preparedstops)
    
    def preparebuslist(self, stopid):
        bus_list = []
        busses = self.ravtfl.getbuses(stopid, False)
        for bus in range(1, len(busses)):
            b = []
            b.append(busses[bus][14])  # Bus Number
            b.append(busses[bus][16])  # Destination
            b.append((busses[bus][21] - busses[0][2]) / 60000)
            bus_list.append(b)
        sorted(bus_list, key=operator.itemgetter(2))
        return bus_list
