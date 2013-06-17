#import datetime
import webapp2
import tfl
import renderengine


class MainService(webapp2.RequestHandler):

    ravtfl = tfl.ravTFL()
    renderer = renderengine.renderengine()
    def get(self):
        #tstart = datetime.datetime.now()
        '''Set header values'''
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.headers['Access-Control-Allow-Origin'] = "*"
        '''Prepare response'''
        try:
            reqargs = self.request.arguments();
            if "stopid" in reqargs:
                try:
                    self.response.write(self.ravtfl.getbuses(self.request.get('stopid')))
                except:
                    self.response.write('Please check your stopid!')
            if "lat" in reqargs and "lng" in reqargs and "radius" in reqargs:
                try:
                    self.response.write(self.ravtfl.getbusstops(self.request.get('lat'), self.request.get('lng'), self.request.get('radius')))
                except:
                    self.response.write('Please check your lat, lng and radius values!')
            if "render" in reqargs:
                self.response.headers['Content-Type'] = 'html'
                self.response.write(renderengine.renderengine().render(51.517337, -0.08066, 100))
        except:
            self.response.write('error occurred!')
            raise
        finally:
            '''if self.response.headers['Content-Type'] == 'text/plain':
                ttaken = datetime.datetime.now() - tstart;
                self.response.write("['")
                self.response.write(ttaken)
                self.response.write("']")'''


application = webapp2.WSGIApplication([
    ('/', MainService),
], debug=False)
