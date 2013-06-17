import httplib
import json
import ravlonbuscnsts
import maths
import time
import logging

class ravTFL:

    _tflurl = "countdown.api.tfl.gov.uk"
    _tfl_busstops = []
    _tfl_busstops_lastfetch = 0
    _sf = ravlonbuscnsts.busstopfields()

    def getbusstops(self, lat, lng, radius=None , returnjson=True):
        try:
            req_para_circle = ''
            req_para_returnlist = 'returnlist=StopPointName,StopID,StopCode1,StopCode2,StopPointType,Towards,Bearing,StopPointIndicator,StopPointState,Latitude,Longitude'
            if lat and lng and radius:
                req_para_circle = 'circle=' + str(lat) + ',' + str(lng) + ',' + str(radius)
            conn = httplib.HTTPConnection(self._tflurl)
            conn.request("GET", "/interfaces/ura/instant_V1?" + req_para_circle + '&' + req_para_returnlist)
            tflResponse = conn.getresponse()
            data = tflResponse.read()
            data = '[' + data.replace('\r\n', ',\r\n') + ']'
            d = json.loads(data)
            d.pop(0)
            if(returnjson):
                return json.dumps(d)
            else:
                return d;
        except:
            raise
        finally:
            conn.close()
    
    def getbuses(self, stopid, returnjson=True):
        if not stopid:
            return []
        try:
            req_para_stopid = 'stopid=' + str(stopid)
            req_para_returnlist = 'returnlist=StopPointName,StopID,StopCode1,StopCode2,StopPointType,Towards,Bearing,StopPointIndicator,StopPointState,Latitude,Longitude,VisitNumber,LineID,LineName,DirectionID,DestinationText,DestinationName,VehicleID,TripID,RegistrationNumber,EstimatedTime,ExpireTime'
            conn = httplib.HTTPConnection(self._tflurl)
            conn.request("GET", "/interfaces/ura/instant_V1?" + req_para_stopid + '&' + req_para_returnlist)
            tflResponse = conn.getresponse()
            data = tflResponse.read()
            data = '[' + data.replace('\r\n', ',\r\n') + ']'
            d = json.loads(data)
            if(returnjson):
                return json.dumps(d)
            else:
                return d
        except:
            raise
        finally:
            conn.close()
            
    def fetchbusstops(self):
        try:
            logging.info('Fetching bus stops list now at - ' + str(time.time()) + '. Last fetch was at -' + str(self._tfl_busstops_lastfetch))
            req_para_returnlist = 'returnlist=StopPointName,StopID,StopCode1,StopCode2,StopPointType,Towards,Bearing,StopPointIndicator,StopPointState,Latitude,Longitude'
            conn = httplib.HTTPConnection(self._tflurl)
            conn.request("GET", "/interfaces/ura/instant_V1?stopalso=1" + '&' + req_para_returnlist)
            tflResponse = conn.getresponse()
            data = tflResponse.read()
            data = '[' + data.replace('\r\n', ',\r\n') + ']'
            d = json.loads(data)
            self._tfl_busstops_lastfetch = d[0][2];
            d.pop(0)
            self._tfl_busstops = d
            conn.close()
        except:
            raise
            

    def getbusstops2(self, lat, lng, radius=500 , returnjson=True):
        if (self._tfl_busstops_lastfetch + 86400000) < (time.time() * 1000):
            self.fetchbusstops()
        result = []
        logging.info(self._tfl_busstops[0][self._sf.Latitude])
        logging.info(self._tfl_busstops[0][self._sf.Longitude])
        for stop in self._tfl_busstops:
            dist = maths.latlngdist(lat, lng, stop[self._sf.Latitude], stop[self._sf.Longitude])
            if  dist <= radius:
                logging.info(dist)
                b = []
                b.append(stop[self._sf.StopID])
                b.append(stop[self._sf.StopPointName])
                b.append(stop[self._sf.StopPointIndicator])
                b.append(dist)
                result.append(b)
        return result
        
                        


#     
# tfl = ravTFL()
# t1 = datetime.datetime.now()
# stops = tfl.getbusstops(51.49599, -0.14192, 100)
# buses = tfl.getbuses(34506)
# print len(stops)
# print len(buses)
# t2 = datetime.datetime.now()
# print stops
# print buses
# print t2 - t1

'''Bus Stop Array'''
'''StopPointName,StopID,StopCode1,StopCode2,StopPointType,Towards,Bearing,StopPointIndicator,StopPointState,Latitude,Longitude'''

'''Prediction Array'''
'''StopPointName,StopID,StopCode1,StopCode2,StopPointType,Towards,Bearing,StopPointIndicator,StopPointState,Latitude,
Longitude,VisitNumber,LineID,LineName,DirectionID,DestinationText,DestinationName,VehicleID,TripID,RegistrationNumber,
EstimatedTime,ExpireTime'''

'''Complete Array'''
'''StopPointName,StopID,StopCode1,StopCode2,StopPointState,StopPointType,StopPointIndicator, Towards,Bearing,Latitude,
Longitude,VisitNumber,TripID,VehicleID,RegistrationNumber,LineID,LineName,DirectionID,DestinationText,DestinationName,
EstimatedTime,MessageUUID,MessageText,MessageType,MessagePriority,StartTime,ExpireTime,BaseVersion'''
