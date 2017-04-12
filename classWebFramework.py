import tornado.ioloop
import tornado.web
import json


from packageBackend.classBackend import Backend

class RootHandler(tornado.web.RequestHandler):
    def initialize(self, loggerObject, backendObject):
                self.loggerObject = loggerObject
                self.backendObject = backendObject       
                
    @tornado.gen.coroutine
    def post(self):
        try:
            self.write("Analysis REST API v1.0")
            self.loggerObject.logger.logActivity("INFO", "GET RootHandler request initiated ", __name__)
            
        except Exception as err:
            self.loggerObject.logger.logActivity("ERROR", "GET RootHandler request error " + str(err), __name__)
            return False
    
class QuestionAnalysis(tornado.web.RequestHandler):
    def initialize(self, loggerObject, backendObject):
                self.loggerObject = loggerObject
                self.backendObject = backendObject
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type,Authorization")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS') 
        
    @tornado.gen.coroutine
    def post(self):
        try:
            #self.write("Question Analysis REST api v1.0")
            self.loggerObject.logger.logActivity("INFO", "GET QuestionAnalysis request initiated ", __name__)
            
            requestJSON = self.request.body
            requestAuth = self.request.headers['Authorization']
            requestCont = self.request.headers['Content-Type']
            response1 = self.backendObject.formRequest(requestJSON, "RequestAnalysis", requestAuth,requestCont) 
            result = {'status':'success','result':response1}
            #print(result)
            #print((response1))
            self.write(result)
            #res = response1.toJSON()
            
            
            
        except Exception as err:
            self.loggerObject.logger.logActivity("ERROR", "GET QuestionAnalysis request error " + str(err), __name__)
            response2 = ("ERROR" + str(err), __name__)
            result = {'status':'failure','result':response2}
            self.write(result)
            return False
    @tornado.gen.coroutine 
    def options(self):
        # no body
        self.set_status(204)
        self.finish()
        
        
class ELCCustomReport(tornado.web.RequestHandler):
    def initialize(self, loggerObject, backendObject):
                self.loggerObject = loggerObject
                self.backendObject = backendObject
    
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type,Authorization")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS') 
        
    @tornado.gen.coroutine
    def post(self):
        try:
            #self.write("Question Analysis REST api v1.0")
            self.loggerObject.logger.logActivity("INFO", "GET QuestionAnalysis request initiated ", __name__)
            print("Im in custom report , hello ")
            
            requestJSON = self.request.body
            requestAuth = self.request.headers['Authorization']
            requestCont = self.request.headers['Content-Type']
            response1 = self.backendObject.formRequest(requestJSON, "ECLCustomReport", requestAuth,requestCont) 
            result = {'status':'success','result':response1}
            #print((response1))
            self.write(result)
            #res = response1.toJSON()
            
            
            
        except Exception as err:
            self.loggerObject.logger.logActivity("ERROR", "GET QuestionAnalysis request error " + str(err), __name__)
            response2 = ("ERROR" + str(err), __name__)
            result = {'status':'failure','result':response2}
            self.write(result)
            return False
     
    @tornado.gen.coroutine 
    def options(self):
        # no body
        self.set_status(204)
        self.finish() 
        
    
class GroupAnalysis(tornado.web.RequestHandler):
    def initialize(self, loggerObject, backendObject):
                self.loggerObject = loggerObject
                self.backendObject = backendObject
                
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type,Authorization")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS') 
    
    @tornado.gen.coroutine
    def post(self):
        try:
            self.write("Group Analysis REST api v1.0")
            print("Im in group analysis , hello ")
            
            requestJSON = self.request.body
            requestAuth = self.request.headers['Authorization']
            requestCont = self.request.headers['Content-Type']
            response1 = self.backendObject.formRequest(requestJSON, "GroupAnalysis", requestAuth,requestCont) 
            result = {'status':'success','result':response1}
            #print((response1))
            self.write(result)
            
        except Exception as err:
            self.loggerObject.logger.logActivity("ERROR", "GET GroupAnalysis request error " + str(err), __name__)
            
            return False
            
    @tornado.gen.coroutine  
    def options(self):
         # no body
        self.set_status(204)
        self.finish() 

class ComparisonAnalysis(tornado.web.RequestHandler):
    def initialize(self, loggerObject, backendObject):
                self.loggerObject = loggerObject
                self.backendObject = backendObject
                
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type,Authorization")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS') 
    
    @tornado.gen.coroutine
    def post(self):
        try:
            self.write("Comparison Analysis REST api v1.0")
            
            self.loggerObject.logger.logActivity("INFO", "GET Comparison analysis request initiated ", __name__)
            print("Im in comparison analysis , hello ")
            
            requestJSON = self.request.body
            requestAuth = self.request.headers['Authorization']
            requestCont = self.request.headers['Content-Type']
            response1 = self.backendObject.formRequest(requestJSON, "ComparisonAnalysis", requestAuth,requestCont) 
            result = {'status':'success','result':response1}
            #print((response1))
            self.write(result)
            
            
            self.loggerObject.logger.logActivity("INFO", "GET ComparisonAnalysis request initiated ", __name__)
    
        except Exception as err:
            self.loggerObject.logger.logActivity("ERROR", "GET ComparisonAnalysis request error " + str(err), __name__)
    @tornado.gen.coroutine
    def options(self):
        # no body
        self.set_status(204)
        self.finish()         

class TrendAnalysis(tornado.web.RequestHandler):
    def initialize(self, loggerObject, backendObject):
                self.loggerObject = loggerObject
                self.backendObject = backendObject
                
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type,Authorization")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS') 

    
    @tornado.gen.coroutine
    def post(self):
        try:
            self.write("Trend Analysis REST api v1.0")
            requestJSON = self.request.body
            self.loggerObject.logger.logActivity("INFO", "GET TrendAnalysis request initiated ", __name__)
            
            print("Im in trend analysis , hello ")
            
            requestJSON = self.request.body
            requestAuth = self.request.headers['Authorization']
            requestCont = self.request.headers['Content-Type']
            response1 = self.backendObject.formRequest(requestJSON, "TrendAnalysis", requestAuth,requestCont) 
            result = {'status':'success','result':response1}
            #print((response1))
            self.write(result)
    
        except Exception as err:
            self.loggerObject.logger.logActivity("ERROR", "GET TrendAnalysis request error " + str(err), __name__)
   
    @tornado.gen.coroutine 
    def options(self):
        # no body
        self.set_status(204)
        self.finish()    
        
        
class ProjectOverviewStats(tornado.web.RequestHandler):
    def initialize(self, loggerObject, backendObject):
                self.loggerObject = loggerObject
                self.backendObject = backendObject
                
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type,Authorization")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS') 

    
    @tornado.gen.coroutine
    def post(self):
        try:
            self.write("Overview Analysis REST api v1.0")
            self.loggerObject.logger.logActivity("INFO", "GET Overview request initiated ", __name__)
            print("Im in overview analysis , hello ")
            
            requestJSON = self.request.body
            requestAuth = self.request.headers['Authorization']
            requestCont = self.request.headers['Content-Type']
            response1 = self.backendObject.formRequest(requestJSON, "OverviewAnalysis", requestAuth,requestCont) 
            result = {'status':'success','result':response1}
            #print((response1))
            self.write(result)
    
        except Exception as err:
            self.loggerObject.logger.logActivity("ERROR", "GET TrendAnalysis request error " + str(err), __name__)
   
    @tornado.gen.coroutine 
    def options(self):
        # no body
        self.set_status(204)
        self.finish()            

class WebFramework(object):
    def __init__ (self, Object, appConfig):
        try:
            Object.logger.logActivity("INFO", "Initializing backend object ", __name__)
            
            backendObject = Backend(Object, appConfig)
                      
            Object.logger.logActivity("INFO", "Initializing web framework ", __name__)
            
            application = tornado.web.Application([("/", RootHandler, {"loggerObject" : Object,"backendObject" : backendObject }),
                                                    ("/QuestionAnalysis", QuestionAnalysis, {"loggerObject" : Object, "backendObject" : backendObject }), 
                                                   ("/GroupAnalysis", GroupAnalysis, {"loggerObject" : Object,"backendObject" : backendObject }), 
                                                   ("/ComparisonAnalysis", ComparisonAnalysis, {"loggerObject" : Object,"backendObject" : backendObject }), 
                                                   ("/TrendAnalysis", TrendAnalysis, {"loggerObject" : Object,"backendObject" : backendObject }),
                                                   ("/ELCCustomReport", ELCCustomReport, {"loggerObject" : Object,"backendObject" : backendObject }),
                                                   ("/ProjectOverviewStats", ProjectOverviewStats, {"loggerObject" : Object,"backendObject" : backendObject })
                                                   ])
            #application = tornado.web.Application([("/", RootHandler, {"loggerObject" : Object })])
            print("hi")
            application.listen(80)
            tornado.ioloop.IOLoop.instance().start()
            Object.logger.logActivity("INFO", "Web framework started and listening for requests ", __name__)
        
            
        except Exception as err:
            print("hii")
            Object.logger.logActivity("ERROR", "error starting the web framework instance" + str(err), __name__)
            #return False
    
        
