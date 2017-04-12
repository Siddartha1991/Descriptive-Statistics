import requests
import datetime
import simplejson as json
import tornado.web
from packageStatisticalMethods.classStatisticalMethods import StatisticalMethods

class Backend(object):

    def __init__ (self, loggerObject, configObject):
        self.loggerObject = loggerObject
        self.configObject = configObject
        #self.loggerObject.logger.logActivity("INFO", "Initializing backend object complete ", __name__)

       
    def formRequest(self, requestJSON, typeOfAnalysis,token_auth,token_cont):
        try:

            headerStr1 = "authorization" 
            headerStr1Value = token_auth
            headerStr2 = "Content-Type"
            headerStr2Value = token_cont
            timeoutParam = self.configObject.timeoutParameter
            requestid = '{:%Y%m%d%H%M%S%f}'.format(datetime.datetime.now())
            hostIP = self.configObject.backendHost
            
            self.loggerObject.logger.logActivity("INFO", "timeout value " + timeoutParam, __name__)       
            if(typeOfAnalysis == 'ComparisonAnalysis'):
                print("entered..")
                requestJSON = json.loads(requestJSON)
                projectid = requestJSON['Projectid']
                options = requestJSON['compare']  
                data_list = []
                getRequestURL = "http://" + hostIP + "/projects/" + projectid + "/responses"
                data_option = []
                for i in range(len(options)):
                    tmp1 = {}
                    # we should always have from date and to date (even when no dates are specified)
                    if(requestJSON['from_date']):
                        tmp1['from_date'] = requestJSON['from_date']
                        from_date = requestJSON['from_date']
                    else:
                        from_date = ''
                           
                    if(requestJSON['to_date']):
                        tmp1['to_date'] = requestJSON['to_date']
                        to_date = requestJSON['to_date']
                    else:
                        to_date = ''
                        
                    tmp1["filters"] = []
                    tmp1["filters"].append(options[i])
                    print('going into filter')
                    if('filter' in requestJSON):
                        print("in filter..")
                        for j in requestJSON['filter']:
                            tmp1["filters"].append(j)   
                    requestJSONdumps1 = json.dumps(tmp1)
                    total_resp = []
                    print('entered.................')
                    
                    getRequestURL = "http://" + hostIP + "/projects/" + projectid + "/responses" + "?pageNumber=0&itemsPerPage=200"
                    resp = requests.post(getRequestURL, data=requestJSONdumps1, headers={headerStr1:headerStr1Value,headerStr2:headerStr2Value ,'requestid':str(requestid)}, timeout=float(timeoutParam))
                    #print(resp)
                    total_resp = resp.json()
                    print(getRequestURL)
                    print('check')
                    #print(total_resp)
                    print('json')
                    print(len(resp.json()))
                    getRequestURL = "http://" + hostIP + "/projects/" + projectid + "/responses" + "?pageNumber=1&itemsPerPage=200"
                    resp = requests.post(getRequestURL, data=requestJSONdumps1, headers={headerStr1:headerStr1Value,headerStr2:headerStr2Value ,'requestid':str(requestid)}, timeout=float(timeoutParam))
                    page_num = 1
                    while len(resp.json()) != 0:
                        print('ntred while loop')
                        for j in resp.json():
                            total_resp.append(j)   
                        page_num = page_num + 1
                        print(page_num)
                        getRequestURL = "http://" + hostIP + "/projects/" + projectid + "/responses" + "?pageNumber=" + str(page_num) +"&itemsPerPage=200"
                        resp = requests.post(getRequestURL, data=requestJSONdumps1, headers={headerStr1:headerStr1Value,headerStr2:headerStr2Value ,'requestid':str(requestid)}, timeout=float(timeoutParam))
                    print('im out', len(total_resp))
                    print(data_option)
                    ###################
                    
                    print(i)
                    if(resp.status_code == 200):
                        if(len(total_resp) !=0):
                            print(options)
                            data_option.append(options[i])
                            print(data_option)
                            data_list.append(total_resp)
                
                            print(resp.status_code)       
                    else:
                        res = "ERROR", "backend response error " + str(resp.status_code)
                        self.loggerObject.logger.logActivity("ERROR", "backend response error " + str(resp.status_code), __name__)
                        return res
                    print(len(data_list))   
                if (len(data_list) > 1) :
                    print("in here...")
                    print('wewewew')
                    getRequestURL1 = "http://" + hostIP + "/projects/" + projectid 
                    r = requests.get(getRequestURL1,headers={headerStr1:headerStr1Value,headerStr2:headerStr2Value ,'requestid':str(requestid)})
                    print(r.json())
                    self.loggerObject.logger.logActivity("INFO", "backend HTTP Response Code : " + str(resp.status_code), __name__)
                    self.loggerObject.logger.logActivity("INFO", "backend Response : " + resp.text, __name__)
                    self.loggerObject.logger.logActivity("INFO", "forming backend request for " + typeOfAnalysis, __name__)
                    SM = StatisticalMethods()
                    res = SM.CompareAnalysis(typeOfAnalysis, data_list, from_date, to_date ,data_option,r.json(),self.loggerObject)
                    return res 
                else:
                    res = "Please enter a valid option for both questions" 
                    return res
                    
            
            elif(typeOfAnalysis == 'TrendAnalysis'):
                print("entered trend analysis..")
                requestJSON = json.loads(requestJSON)
                
            
                projectid = requestJSON['Projectid']
                trend_type = requestJSON['trend']
                from_date = requestJSON['from_date']
                to_date = requestJSON['to_date']
                
            
                tmp1 = {}
                # we should always have from date and to date (even when no dates are specified)
                if(requestJSON['from_date']):
                    tmp1['from_date'] = requestJSON['from_date']
                    from_date = requestJSON['from_date']
                else:
                    from_date = ''
                       
                if(requestJSON['to_date']):
                    tmp1['to_date'] = requestJSON['to_date']
                    to_date = requestJSON['to_date']
                else:
                    to_date = ''
                
                print('going into filter')
                if('filter' in requestJSON):
                    print("in filter..")
                    for i in requestJSON['filter']:
                        tmp1["filters"] = requestJSON['filter']
                    
                requestJSONdumps1 = json.dumps(tmp1)
                

                mm = int(from_date[5:7])
                dd = int(from_date[8:10])
                
                fdate = from_date[0:10]
                tdate = to_date[0:10]
                boln = False
                if trend_type == 'hourly':
                    if(fdate == tdate):
                        boln = True
                elif trend_type == 'yearly':
                    boln = True
                elif trend_type == 'monthly':
                    t_year = int(to_date[0:4])
                    f_year = int(from_date[0:4])
                    t_mon = int(to_date[5:7])
                    f_mon = int(from_date[5:7])
                    if (t_year - f_year) == 0:
                        boln = True
                    elif (t_year - f_year) == 1:
                        if(t_mon <= f_mon):
                            boln = True
                        else:
                            boln = False
                    else:
                        boln = False
                        
                elif trend_type == 'daily':
                    t_year = int(to_date[0:4])
                    f_year = int(from_date[0:4])
                    t_mon = int(to_date[5:7])
                    f_mon = int(from_date[5:7])
                    t_day = int(to_date[8:10])
                    f_day = int(from_date[8:10])
                    if (t_year - f_year == 0):
                        if (t_mon - f_mon == 0):
                            boln = True
                        elif (t_mon - f_mon == 1):
                            if(t_day <= f_day):
                                boln = True
                            else:
                                boln = False
                        elif (t_mon - f_mon > 1):
                            boln = False
                    elif (t_year - f_year == 1):
                        if(f_mon == 12 and t_mon == 1):
                            if(t_day <= f_day):
                                boln = True
                            else:
                                boln = False
                        else:
                            boln = False
                    else:
                        boln = False
                        
                        
                        
                    
                    
                        
                    
                    
                print('boolean')
                print(boln)
                if boln:
                    total_resp = []
                    print('entered.................')
                    
                    getRequestURL = "http://" + hostIP + "/projects/" + projectid + "/responses" + "?pageNumber=0&itemsPerPage=200"
                    resp = requests.post(getRequestURL, data=requestJSONdumps1, headers={headerStr1:headerStr1Value,headerStr2:headerStr2Value ,'requestid':str(requestid)}, timeout=float(timeoutParam))
                    #print(resp)
                    total_resp = resp.json()
                    
                    print('check')
                    print(total_resp)
                    print('json')
                    print(len(resp.json()))
                    getRequestURL = "http://" + hostIP + "/projects/" + projectid + "/responses" + "?pageNumber=1&itemsPerPage=200"
                    resp = requests.post(getRequestURL, data=requestJSONdumps1, headers={headerStr1:headerStr1Value,headerStr2:headerStr2Value ,'requestid':str(requestid)}, timeout=float(timeoutParam))
                    page_num = 1
                    while len(resp.json()) != 0:
                        print('ntred while loop')
                        for i in resp.json():
                            total_resp.append(i)   
                        page_num = page_num + 1
                        print(page_num)
                        getRequestURL = "http://" + hostIP + "/projects/" + projectid + "/responses" + "?pageNumber=" + str(page_num) +"&itemsPerPage=200"
                        resp = requests.post(getRequestURL, data=requestJSONdumps1, headers={headerStr1:headerStr1Value,headerStr2:headerStr2Value ,'requestid':str(requestid)}, timeout=float(timeoutParam))
    
                    #payload = {'pageNumber': '0', 'itemsPerPage': '10'}
                    
                    print('helloooooooooooooooooooooooo')
                    getRequestURL1 = "http://" + hostIP + "/projects/" + projectid 
                    r = requests.get(getRequestURL1,headers={headerStr1:headerStr1Value,headerStr2:headerStr2Value ,'requestid':str(requestid)})
                    print(r.json())
                    
                    print(resp.status_code)
                    print(r.status_code)
                    if (resp.status_code == 200 and r.status_code == 200):
                    
                        self.loggerObject.logger.logActivity("INFO", "backend HTTP Response Code : " + str(resp.status_code), __name__)
                        self.loggerObject.logger.logActivity("INFO", "backend Response : " + resp.text, __name__)
                        self.loggerObject.logger.logActivity("INFO", "forming backend request for " + typeOfAnalysis, __name__)
                        
                        SM = StatisticalMethods()
                        res = SM.TrendAnalysis(typeOfAnalysis, total_resp, from_date, to_date, trend_type, r.json(), self.loggerObject)
                        
                        return res   
                    else:
                    
                        self.loggerObject.logger.logActivity("ERROR", "backend response error " + str(resp.status_code), __name__)
                
                else:
                    temp = {}
                    temp['message'] = 'ERROR MESSAGEPlease enter valid from_date and to_date for trend analysis'
                    return temp
                
                
            elif(typeOfAnalysis == 'GroupAnalysis'):
                
                print("entered..")
                requestJSON = json.loads(requestJSON)
                
            
                projectid = requestJSON['Projectid']
                options = requestJSON['group']
                print(options)
                #from_date = requestJSON['from_date']
                #to_date = requestJSON['to_date']
                
            
                tmp1 = {}
                # we should always have from date and to date (even when no dates are specified)
                if(requestJSON['from_date']):
                    tmp1['from_date'] = requestJSON['from_date']
                    from_date = requestJSON['from_date']
                else:
                    from_date = ''
                       
                if(requestJSON['to_date']):
                    tmp1['to_date'] = requestJSON['to_date']
                    to_date = requestJSON['to_date']
                else:
                    to_date = ''
                
                print('going into filter')
                if('filter' in requestJSON):
                    print("in filter..")
                    for i in requestJSON['filter']:
                        tmp1["filters"] = requestJSON['filter']
                    
                requestJSONdumps1 = json.dumps(tmp1)
                
                
                total_resp = []
                print('entered.................')
                
                getRequestURL = "http://" + hostIP + "/projects/" + projectid + "/responses" + "?pageNumber=0&itemsPerPage=200"
                resp = requests.post(getRequestURL, data=requestJSONdumps1, headers={headerStr1:headerStr1Value,headerStr2:headerStr2Value ,'requestid':str(requestid)}, timeout=float(timeoutParam))
                #print(resp)
                total_resp = resp.json()
                print('check')
                print('json')
                print(len(resp.json()))
                getRequestURL = "http://" + hostIP + "/projects/" + projectid + "/responses" + "?pageNumber=1&itemsPerPage=200"
                resp = requests.post(getRequestURL, data=requestJSONdumps1, headers={headerStr1:headerStr1Value,headerStr2:headerStr2Value ,'requestid':str(requestid)}, timeout=float(timeoutParam))
                page_num = 1
                while len(resp.json()) != 0:
                    print('ntred while loop')
                    for i in resp.json():
                        total_resp.append(i)   
                    page_num = page_num + 1
                    print(page_num)
                    getRequestURL = "http://" + hostIP + "/projects/" + projectid + "/responses" + "?pageNumber=" + str(page_num) +"&itemsPerPage=200"
                    resp = requests.post(getRequestURL, data=requestJSONdumps1, headers={headerStr1:headerStr1Value,headerStr2:headerStr2Value ,'requestid':str(requestid)}, timeout=float(timeoutParam))

                #payload = {'pageNumber': '0', 'itemsPerPage': '10'}
                
                print('helloooooooooooooooooooooooo')
                getRequestURL1 = "http://" + hostIP + "/projects/" + projectid 
                r = requests.get(getRequestURL1,headers={headerStr1:headerStr1Value,headerStr2:headerStr2Value ,'requestid':str(requestid)})
                print(r.json())
                
                
                
                
                if (resp.status_code == 200 and r.status_code == 200):
                    print('in resp..')
                    self.loggerObject.logger.logActivity("INFO", "backend HTTP Response Code : " + str(resp.status_code), __name__)
                    self.loggerObject.logger.logActivity("INFO", "backend Response : " + resp.text, __name__)
                    self.loggerObject.logger.logActivity("INFO", "forming backend request for " + typeOfAnalysis, __name__)
                    
                    SM = StatisticalMethods()
                    res = SM.groupAnalysis(typeOfAnalysis, total_resp, from_date, to_date, options, r.json(), self.loggerObject)
                    
                    return res   
                else:
                    
                    self.loggerObject.logger.logActivity("ERROR", "backend response error " + str(resp.status_code), __name__)
                    
                    
                    
            elif(typeOfAnalysis == 'OverviewAnalysis'):
                requestJSON = json.loads(requestJSON)
                print(requestJSON)
                projectid = requestJSON['Projectid']
                from_date = requestJSON['from_date']
                to_date = requestJSON['to_date']
                requestJSONdumps = json.dumps(requestJSON)
                total_resp = []
                print('entered.................')
                
                getRequestURL = "http://" + hostIP + "/projects/" + projectid + "/responses" + "?pageNumber=0&itemsPerPage=200"
                resp = requests.post(getRequestURL, data=requestJSONdumps, headers={headerStr1:headerStr1Value,headerStr2:headerStr2Value ,'requestid':str(requestid)}, timeout=float(timeoutParam))
                total_resp = resp.json()
                #print(resp.text)
                print('check')
                #print(total_resp)
                print('json')
                temp = (resp.text)
                print(getRequestURL)
                getRequestURL = "http://" + hostIP + "/projects/" + projectid + "/responses" + "?pageNumber=1&itemsPerPage=200"
                resp = requests.post(getRequestURL, data=requestJSONdumps, headers={headerStr1:headerStr1Value,headerStr2:headerStr2Value ,'requestid':str(requestid)}, timeout=float(timeoutParam))
                
                page_num = 1
                while len(resp.json()) != 0:
                    print('ntred while loop')
                    for i in resp.json():
                        total_resp.append(i)   
                    page_num = page_num + 1
                    print(page_num)
                    getRequestURL = "http://" + hostIP + "/projects/" + projectid + "/responses" + "?pageNumber=" + str(page_num) +"&itemsPerPage=200"
                    resp = requests.post(getRequestURL, data=requestJSONdumps, headers={headerStr1:headerStr1Value,headerStr2:headerStr2Value ,'requestid':str(requestid)}, timeout=float(timeoutParam))

                
                if (resp.status_code == 200):
                    #print('success 200')
                    self.loggerObject.logger.logActivity("INFO", "backend HTTP Response Code : " + str(resp.status_code), __name__)
                    self.loggerObject.logger.logActivity("INFO", "backend Response : " + resp.text, __name__)
                    self.loggerObject.logger.logActivity("INFO", "forming backend request for " + typeOfAnalysis, __name__)
                    
                    SM = StatisticalMethods()
                    #total_resp = str(total_resp)
                    #print((total_resp))
                    print(type(resp.text))
                    res = SM.OverviewAnalysis(typeOfAnalysis, total_resp, from_date, to_date , self.loggerObject)
                    return res  
                else:
                    
                    self.loggerObject.logger.logActivity("ERROR", "backend response error " + str(resp.status_code), __name__)

           
            
            
            else:
                requestJSON = json.loads(requestJSON)
                print(requestJSON)
                projectid = requestJSON['Projectid']
                from_date = requestJSON['from_date']
                to_date = requestJSON['to_date']
                requestJSONdumps = json.dumps(requestJSON)
                total_resp = []
                print('entered.................')
                
                getRequestURL = "http://" + hostIP + "/projects/" + projectid + "/responses" + "?pageNumber=0&itemsPerPage=200"
                resp = requests.post(getRequestURL, data=requestJSONdumps, headers={headerStr1:headerStr1Value,headerStr2:headerStr2Value ,'requestid':str(requestid)}, timeout=float(timeoutParam))
                total_resp = resp.json()
                #print(resp.text)
                print('check')
                #print(total_resp)
                print('json')
                temp = (resp.text)
                print(len(resp.json()))
                getRequestURL = "http://" + hostIP + "/projects/" + projectid + "/responses" + "?pageNumber=1&itemsPerPage=200"
                resp = requests.post(getRequestURL, data=requestJSONdumps, headers={headerStr1:headerStr1Value,headerStr2:headerStr2Value ,'requestid':str(requestid)}, timeout=float(timeoutParam))
                
                page_num = 1
                while len(resp.json()) != 0:
                    print('ntred while loop')
                    for i in resp.json():
                        total_resp.append(i)   
                    page_num = page_num + 1
                    print(page_num)
                    getRequestURL = "http://" + hostIP + "/projects/" + projectid + "/responses" + "?pageNumber=" + str(page_num) +"&itemsPerPage=200"
                    resp = requests.post(getRequestURL, data=requestJSONdumps, headers={headerStr1:headerStr1Value,headerStr2:headerStr2Value ,'requestid':str(requestid)}, timeout=float(timeoutParam))

                #payload = {'pageNumber': '0', 'itemsPerPage': '10'}
                
                print('helloooooooooooooooooooooooo')
                getRequestURL1 = "http://" + hostIP + "/projects/" + projectid 
                r = requests.get(getRequestURL1,headers={headerStr1:headerStr1Value,headerStr2:headerStr2Value ,'requestid':str(requestid)})
                print(r.json())
                if (resp.status_code == 200 and r.status_code == 200):
                    #print('success 200')
                    self.loggerObject.logger.logActivity("INFO", "backend HTTP Response Code : " + str(resp.status_code), __name__)
                    self.loggerObject.logger.logActivity("INFO", "backend Response : " + resp.text, __name__)
                    self.loggerObject.logger.logActivity("INFO", "forming backend request for " + typeOfAnalysis, __name__)
                    
                    SM = StatisticalMethods()
                    #total_resp = str(total_resp)
                    print(type(total_resp))
                    print(type(resp.text))
                    res = SM.processData(typeOfAnalysis, total_resp, from_date, to_date , r.json(), self.loggerObject)
                    return res  
                else:
                    
                    self.loggerObject.logger.logActivity("ERROR", "backend response error " + str(resp.status_code), __name__)


        except Exception as err:
            res = "ERROR", "backend response exception " + str(err) , __name__
            return res
        
        
        
            
                            
    
    
