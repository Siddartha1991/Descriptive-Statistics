import collections
import pandas as pd
from statistics import mode
import numpy as np
import simplejson as json


class StatisticalMethods(object):
    def __init__ (self):
        pass
        

    def processData(self, typeOfAnalysis, dataSet, Object):
        try:
            Object.logger.logActivity("INFO", "dataSet : " + str(dataSet), __name__)
            if (typeOfAnalysis == 'RequestAnalysis'):
                Object.logger.logActivity("INFO", "forming backend request for " + typeOfAnalysis, __name__)

                # reading sample json :
                #samp = pd.read_json('C:/Users/Siddartha Rao/Downloads/output.json')
                samp=pd.read_json(dataSet)
                #print(dataSet)
                one = pd.DataFrame(samp['answers'])
                # ques_dict_disp maintains display value of option that user selected (for eg, if user selects red option for q1, it stores red )
                ques_dict_disp = {}

                res = {}
                # assigning project ID - need to update this as per real time response file
                res['projectID'] = samp['projectId'][0]
                # do not have consistency in todatetime and fromdatetime
                res['fromdatetime'] = ''
                res['todatetime'] = ''

                # do not have 'type of analysis' input from json
                res['TypeofAnalysis'] = 'QuestionAnalysis'

                res['AnalysisList'] = []

                # code which fetches question and its type . we need this for performing type wise analysis.


                questype = {}
                for i in range(one.shape[0]):
                    ques_per_person = one['answers'][i]
                    for ques in ques_per_person:
                        questype[ques['questionId']] = ques['question'][0]['type']

                for i in range(one.shape[0]):
                    ques_per_person = one['answers'][i]
                    for ques in ques_per_person:
                        if questype[ques['questionId']] != 'matrix':
                            if ques['questionId'] not in ques_dict_disp:
                                ques_dict_disp[ques['questionId']] = {}
                                if ques['selectedOptionDisplayValue'] not in ques_dict_disp[ques['questionId']]:
                                    ques_dict_disp[ques['questionId']][ques['selectedOptionDisplayValue']] = [
                                        ques['assignedOptionValue']]
                                else:
                                    ques_dict_disp[ques['questionId']][ques['selectedOptionDisplayValue']].append(
                                        ques['assignedOptionValue'])
                            else:
                                if ques['selectedOptionDisplayValue'] not in ques_dict_disp[ques['questionId']]:
                                    ques_dict_disp[ques['questionId']][ques['selectedOptionDisplayValue']] = [
                                        ques['assignedOptionValue']]
                                else:
                                    ques_dict_disp[ques['questionId']][ques['selectedOptionDisplayValue']].append(
                                        ques['assignedOptionValue'])
                        else:
                            if ques['questionId'] not in ques_dict_disp:
                                ques_dict_disp[ques['questionId']] = {}
                                if ques['selectedOptionDisplayValue'].split(',')[0] not in ques_dict_disp[ques['questionId']]:
                                    ques_dict_disp[ques['questionId']][ques['selectedOptionDisplayValue'].split(',')[0]] = {}
                                    if ques['selectedOptionDisplayValue'].split(',')[1] not in \
                                            ques_dict_disp[ques['questionId']][ques['selectedOptionDisplayValue'].split(',')[0]]:
                                        ques_dict_disp[ques['questionId']][ques['selectedOptionDisplayValue'].split(',')[0]][
                                            ques['selectedOptionDisplayValue'].split(',')[1]] = [
                                            ques['assignedOptionValue']]
                                    else:
                                        ques_dict_disp[ques['questionId']][ques['selectedOptionDisplayValue'].split(',')[0]][
                                            ques['selectedOptionDisplayValue'].split(',')[1]].append(
                                            ques['assignedOptionValue'])
                                else:
                                    if ques['selectedOptionDisplayValue'].split(',')[1] not in \
                                            ques_dict_disp[ques['questionId']][ques['selectedOptionDisplayValue'].split(',')[0]]:
                                        ques_dict_disp[ques['questionId']][ques['selectedOptionDisplayValue'].split(',')[0]][
                                            ques['selectedOptionDisplayValue'].split(',')[1]] = [
                                            ques['assignedOptionValue']]
                                    else:
                                        ques_dict_disp[ques['questionId']][ques['selectedOptionDisplayValue'].split(',')[0]][
                                            ques['selectedOptionDisplayValue'].split(',')[1]].append(
                                            ques['assignedOptionValue'])
                            else:

                                if ques['selectedOptionDisplayValue'].split(',')[0] not in ques_dict_disp[ques['questionId']]:
                                    ques_dict_disp[ques['questionId']][ques['selectedOptionDisplayValue'].split(',')[0]] = {}
                                    if ques['selectedOptionDisplayValue'].split(',')[1] not in \
                                            ques_dict_disp[ques['questionId']][ques['selectedOptionDisplayValue'].split(',')[0]]:
                                        ques_dict_disp[ques['questionId']][ques['selectedOptionDisplayValue'].split(',')[0]][
                                            ques['selectedOptionDisplayValue'].split(',')[1]] = [
                                            ques['assignedOptionValue']]
                                    else:
                                        ques_dict_disp[ques['questionId']][ques['selectedOptionDisplayValue'].split(',')[0]][
                                            ques['selectedOptionDisplayValue'].split(',')[1]].append(
                                            ques['assignedOptionValue'])
                                else:
                                    if ques['selectedOptionDisplayValue'].split(',')[1] not in \
                                            ques_dict_disp[ques['questionId']][ques['selectedOptionDisplayValue'].split(',')[0]]:
                                        ques_dict_disp[ques['questionId']][ques['selectedOptionDisplayValue'].split(',')[0]][
                                            ques['selectedOptionDisplayValue'].split(',')[1]] = [
                                            ques['assignedOptionValue']]
                                    else:
                                        ques_dict_disp[ques['questionId']][ques['selectedOptionDisplayValue'].split(',')[0]][
                                            ques['selectedOptionDisplayValue'].split(',')[1]].append(
                                            ques['assignedOptionValue'])

                                #print(ques_dict_disp)

                # code to calculate total entries for each question type except grid type

                leng = {}
                for qid in ques_dict_disp:
                    li = []
                    cum_fre = 0
                    for aid in ques_dict_disp[qid]:
                        for item in (ques_dict_disp[qid][aid]):
                            li.append(item)
                    leng[qid] = len(li)

                # code to calculate total entries for grid
                gleng = {}

                for qid in ques_dict_disp:
                    cum_fre = 0
                    if questype[qid] == 'matrix':
                        gleng[qid] = {}
                        agree = []
                        disagree = []
                        neutral = []
                        for aid in ques_dict_disp[qid]:
                            for gid in (ques_dict_disp[qid][aid]):
                                if gid.lower() == ' agree':
                                    for item in (ques_dict_disp[qid][aid][gid]):
                                        agree.append(item)
                                if gid.lower() == ' disagree':
                                    for item in (ques_dict_disp[qid][aid][gid]):
                                        disagree.append(item)
                                if gid.lower() == ' neutral':
                                    for item in (ques_dict_disp[qid][aid][gid]):
                                        neutral.append(item)
                        gleng[qid]['agree'] = len(agree)
                        gleng[qid]['disagree'] = len(disagree)
                        gleng[qid]['neutral'] = len(neutral)

                # defining statistics method:
                """
                def Stats_Cal(question_results, ques_dict_disp):
                    li = []

                    for aid in ques_dict_disp[qid]:
                        for item in (ques_dict_disp[qid][aid]):
                            li.append(item)
                    question_results['statistics'] = {}
                    # calculating statistics : mean,median,mode,variance,standard deviation
                    question_results['statistics']['mean'] = round(np.mean(li),2)
                    question_results['statistics']['median'] = round(np.median(li),2)
                    question_results['statistics']['mode'] = pd.DataFrame(li).mode()[0].tolist()  ## mode can take multiple values - so there is no one single value?
                    question_results['statistics']['variance'] = round(np.var(li),2)
                    question_results['statistics']['standard deviation'] = round(np.std(li),2)
                    """
                def Stats_Cal(question_results, ques_dict_disp):
                    li = []

                    for aid in ques_dict_disp[qid]:
                        for item in (ques_dict_disp[qid][aid]):
                            li.append(item)
                    question_results['statistics'] = {}
                    # calculating statistics : mean,median,mode,variance,standard deviation
                    question_results['statistics']['mean'] = float("{0:.2f}".format(np.mean(li)))
                    question_results['statistics']['median'] = float("{0:.2f}".format(np.median(li)))
                    question_results['statistics']['mode'] = pd.DataFrame(li).mode()[0].tolist()  ## mode can take multiple values - so there is no one single value?
                    question_results['statistics']['variance'] = float("{0:.2f}".format(np.var(li)))
                    question_results['statistics']['standard deviation'] = float("{0:.2f}".format(np.std(li)))

                # defining Cumulative frequency stats method:
                def Freq_Cal(question_results, ques_dict_disp):
                    cum_fre = 0
                    for aid in ques_dict_disp[qid]:
                        freq_stats = {}
                        freq_stats['name'] = aid
                        freq_stats['freq'] = len(ques_dict_disp[qid][aid])
                        freq_stats['percent'] = round(len(ques_dict_disp[qid][aid]) / (leng[qid] * 1.0) * 100,2)
                        cum_fre = (len(ques_dict_disp[qid][aid])) + cum_fre
                        freq_stats['cum_freq'] = cum_fre
                        freq_stats['cum_percent'] = round((cum_fre / (leng[qid] * 1.0) * 100),2)
                        question_results['options'].append(freq_stats)

                # defining Rank order stats method:
                def Rank_Stats(question_results, ques_dict_disp):
                    for aid in ques_dict_disp[qid]:
                        rank_stats = {}
                        rank_stats['name'] = aid
                        rank_stats['ranks'] = {}
                        li = ques_dict_disp[qid][aid]
                        rank_count_dist = {x: li.count(x) for x in li}
                        rank_stats['ranks'] = rank_count_dist
                        question_results['options'].append(rank_stats)

                # performing summary statistics on all question types except grid type :

                q_order = 0
                for qid in ques_dict_disp:
                    q_order = q_order + 1
                    question_results = {}
                    question_results['qid'] = qid
                    question_results['qType'] = questype[qid]
                    question_results['qOrder'] = q_order
                    question_results['noOfAnswers'] = 'null'
                    question_results['options'] = []

                    ######################################################
                    # multiple choice type questions
                    ######################################################
                    if (questype[qid] == 'multiple'):
                        Stats_Cal(question_results, ques_dict_disp)
                        Freq_Cal(question_results, ques_dict_disp)
                        res['AnalysisList'].append(question_results)

                    ######################################################
                    # rank type questions
                    ######################################################
                    if (questype[qid] == 'rank'):
                        Rank_Stats(question_results, ques_dict_disp)
                        question_results['statistics'] = 'null'
                        res['AnalysisList'].append(question_results)

                    ######################################################
                    # numeric and SlidingScale type questions
                    ######################################################

                    if (questype[qid] == 'numeric' or questype[qid] == 'SlidingScale'):
                        Stats_Cal(question_results, ques_dict_disp)
                        question_results['options'] = 'null'
                        res['AnalysisList'].append(question_results)

                    ######################################################
                    # Grid type questions
                    ######################################################
                    if (questype[qid] == 'matrix'):
                        question_results['statistics'] = 'null'
                        # Stats_Cal(question_results,ques_dict_disp)
                        question_results['options'] = []
                        question_results['statements'] = []
                        for rowid in ques_dict_disp[qid]:
                            li = []
                            temp_grid_stats = {}
                            for gid in ques_dict_disp[qid][rowid]:
                                for item in (ques_dict_disp[qid][rowid][gid]):
                                    li.append(item)
                            temp_grid_stats['statement'] = rowid
                            temp_grid_stats['order'] = 1
                            temp_grid_stats['mean'] = round(np.mean(li),2)
                            temp_grid_stats['median'] = round(np.median(li),2)
                            temp_grid_stats['mode'] = pd.DataFrame(li).mode()[0].tolist() ## mode can take multiple values - so there is no one single value?
                            temp_grid_stats['variance'] = round(np.var(li),2)
                            temp_grid_stats['standard deviation'] = round(np.std(li),2)
                            question_results['statements'].append(temp_grid_stats)

                        total = gleng[qid]['agree'] + gleng[qid]['disagree'] + gleng[qid]['neutral']
                        cum_fre = 0
                        for i in gleng[qid]:
                            freq_stats = {}
                            freq_stats['name'] = i
                            freq_stats['freq'] = gleng[qid][i]
                            freq_stats['percent'] = round((gleng[qid][i] / (total * 1.0)*100),2)
                            cum_fre = cum_fre + gleng[qid][i]
                            freq_stats['cum_freq'] = cum_fre
                            freq_stats['cum_percent'] = round((cum_fre / (total * 1.0)*100),2)
                            question_results['options'].append(freq_stats)

                        res['AnalysisList'].append(question_results)


                #print (res)
                return res

            elif (typeOfAnalysis == 'ECLCustomReport'):
                
                def Stats_Cal(question_results, ques_dict_disp):
                    li = []

                    for aid in ques_dict_disp[qid]:
                        for item in (ques_dict_disp[qid][aid]):
                            li.append(item)
                    question_results['statistics'] = {}
                    # calculating statistics : mean,median,mode,variance,standard deviation
                    question_results['statistics']['mean'] = float("{0:.2f}".format(np.mean(li)))
                    question_results['statistics']['median'] = float("{0:.2f}".format(np.median(li)))
                    question_results['statistics']['mode'] = pd.DataFrame(li).mode()[0].tolist()  ## mode can take multiple values - so there is no one single value?
                    question_results['statistics']['variance'] = float("{0:.2f}".format(np.var(li)))
                    question_results['statistics']['standard deviation'] = float("{0:.2f}".format(np.std(li)))

                #samp = pd.read_json('F:/projectSurveyAnalysis/customer report docs/cr_backend_new2.json')
                samp=pd.read_json(dataSet)
                one = pd.DataFrame(samp['answers'])
                res = {}
                # assigning project ID - need to update this as per real time response file
                res['projectID'] = samp['projectId'][0]
                # do not have consistency in todatetime and fromdatetime
                res['fromdatetime'] = ''
                res['todatetime'] = ''
                # do not have 'type of analysis' input from json
                res['TypeofAnalysis'] = 'Custom Report'
                res['AnalysisList'] = []
                
                
                #creating question type dictionary
                
                questype = {}
                for i in range(one.shape[0]):
                    ques_per_person = one['answers'][i]
                    for ques in ques_per_person:
                        questype[ques['questionId']] = ques['question'][0]['type']
                
                
                ques_dict_disp_cr = {}
                questions = [9,30,33,34]
                ques_dict_disp_cr_final = {}
                for i in range(one.shape[0]):
                    ques_per_person = one['answers'][i]
                    for ques in ques_per_person:
                        if ques['questionId'] not in ques_dict_disp_cr:
                            ques_dict_disp_cr[ques['questionId']] = {}
                            if ques['selectedOptionDisplayValue'] not in ques_dict_disp_cr[ques['questionId']]:
                                ques_dict_disp_cr[ques['questionId']][ques['selectedOptionDisplayValue']] = [ques['assignedOptionValue']]
                            else:
                                ques_dict_disp_cr[ques['questionId']][ques['selectedOptionDisplayValue']].append(ques['assignedOptionValue'])
                        else:
                            if ques['selectedOptionDisplayValue'] not in ques_dict_disp_cr[ques['questionId']]:
                                ques_dict_disp_cr[ques['questionId']][ques['selectedOptionDisplayValue']] = [ques['assignedOptionValue']]
                            else:
                                ques_dict_disp_cr[ques['questionId']][ques['selectedOptionDisplayValue']].append(ques['assignedOptionValue'])
                            
                
                for i in range(one.shape[0]):
                    ques_per_person = one['answers'][i]
                    for ques in ques_per_person:            
                        for i in ques_dict_disp_cr:
                            if ques['question'][0]['position'] in questions:
                                ques_dict_disp_cr_final[i] = {}
                                for j in ques_dict_disp_cr[i]:
                                    ques_dict_disp_cr_final[i][j] = len(ques_dict_disp_cr[i][j])
                
                
                #creating question position dict:
                question_position ={}
                for i in range(one.shape[0]):
                    ques_per_person = one['answers'][i]
                    for ques in ques_per_person:
                        question_position[ques['questionId']] = ques['question'][0]['position']
                        
                #creating num of responses for each question:
                num_of_responses={}
                for i in ques_dict_disp_cr_final:
                    sum = 0
                    for j in ques_dict_disp_cr_final[i]:
                        sum = sum + ques_dict_disp_cr_final[i][j]
                    num_of_responses[i]=sum
                        
                        
                        
                            
                #print(ques_dict_disp_cr_final)
                
                # building top 5 :
                
                ques_dict_disp_cr_final_sorted = {}
                for i in ques_dict_disp_cr_final:
                    ques_dict_disp_cr_final_sorted[i] = {}
                    l = []
                    keys = []
                    count = 0
                    for j in ques_dict_disp_cr_final[i]:
                        keys.append(j)
                        l.append(ques_dict_disp_cr_final[i][j])
                    l.sort(reverse = True)
                    length = len(l)-1
                    for p in range(length):
                        if(count<5):
                            if(l[p] == l[p+1]):
                                for r in keys:
                                    if(ques_dict_disp_cr_final[i][r] == l[p]):
                                        ques_dict_disp_cr_final_sorted[i][r] = l[p]
                            else:
                                for r in keys:
                                    if(ques_dict_disp_cr_final[i][r] == l[p]):
                                        ques_dict_disp_cr_final_sorted[i][r] = l[p]
                                count = count + 1
                ##################### defining top 5 stats 
                
                for qid in ques_dict_disp_cr_final:
                    top_five_stats = {}
                    top_five_stats['qstring'] = "Top five reasons employees join ELC"
                    top_five_stats['qorder'] = question_position[qid]
                    top_five_stats['qType'] = questype[qid]
                    top_five_stats['noOfResponses'] = num_of_responses[qid]
                    top_five_stats['options'] = []
                    top_five_stats['statistics'] ={}
                    
                    total = 0
                    #cal num of top 5 responses for each question
                    for i in ques_dict_disp_cr_final_sorted[qid]:
                        total = total + ques_dict_disp_cr_final_sorted[qid][i]
                    order = 1
                    cum = 0
                    
                    for i in ques_dict_disp_cr_final_sorted[qid]:
                        option_dict = {}
                        option_dict["name"] = i
                        option_dict["order"] = order
                        order = order+1
                        option_dict["frequency"] = ques_dict_disp_cr_final_sorted[qid][i]
                        option_dict["percent"] = float("{0:.2f}".format(((ques_dict_disp_cr_final_sorted[qid][i])/(total*1.0))*100))
                        cum = cum + ques_dict_disp_cr_final_sorted[qid][i]
                        option_dict["cumulativeFrequency"] = cum
                        option_dict["cumulativePercent"] = float("{0:.2f}".format((cum/(total*1.0))*100))
                        top_five_stats['options'].append(option_dict)
                        
                    
                    Stats_Cal(top_five_stats,ques_dict_disp_cr)
                    res['AnalysisList'].append(top_five_stats)
                ########################################
                    
                ###########BUILDING GROUPING 10-25 questions report
                
                
                # building grouped report for q no 9 - 25 :
                ques_dict_disp_group_final = {}
                questions_group = [9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]
                for i in range(one.shape[0]):
                    ques_per_person = one['answers'][i]
                    for ques in ques_per_person:            
                        for i in ques_dict_disp_cr:
                            if ques['question'][0]['position'] in questions_group:
                                ques_dict_disp_group_final[i] = {}
                                for j in ques_dict_disp_cr[i]:
                                    ques_dict_disp_group_final[i][j] = len(ques_dict_disp_cr[i][j])
                                    
                                    
                
                group_question_dict = {}
                group_question_dict['Agree']={}
                group_question_dict['Disagree']={}
                group_question_dict['Neutral']={}
                group_question_dict['Strongly Disagree']={}
                group_question_dict['Strongly Agree']={}
                for qid in ques_dict_disp_group_final:
                    for group in ques_dict_disp_group_final[qid]:
                        if(group == "Agree"):#agree
                            group_question_dict['Agree'][qid] = ques_dict_disp_group_final[qid]['Agree']
                        elif group == "Disagree":#disagree
                            group_question_dict['Disagree'][qid] = ques_dict_disp_group_final[qid]['Disagree']
                        elif group == "Neutral":#neutral
                            group_question_dict['Neutral'][qid] = ques_dict_disp_group_final[qid]['Neutral']
                        elif group == "Strongly Agree":#disagree
                            group_question_dict['Strongly Agree'][qid] = ques_dict_disp_group_final[qid]['Strongly Agree']
                        elif group == "Strongly Disagree":#disagree
                            group_question_dict['Strongly Disagree'][qid] = ques_dict_disp_group_final[qid]['Strongly Disagree']
                            
                            
                groups_sorted = {}
                for i in group_question_dict:
                    groups_sorted[i] = {}
                    l = []
                    keys = []
                    count = 0
                    for j in group_question_dict[i]:
                        keys.append(j)
                        l.append(group_question_dict[i][j])
                    l.sort(reverse = True)
                    length = len(l)-1
                    for p in range(length):
                        if(count<5):
                            if(l[p] == l[p+1]):
                                for r in keys:
                                    if(group_question_dict[i][r] == l[p]):
                                        groups_sorted[i][r] = l[p]
                            else:
                                for r in keys:
                                    if(group_question_dict[i][r] == l[p]):
                                        groups_sorted[i][r] = l[p]
                                count = count + 1
                
                    
                
                    
                ####################
                
                group_analysis_dict = {}
                group_analysis_dict['qString'] = "GroupingQuestion"
                group_analysis_dict['qOrder'] = 8
                group_analysis_dict['qType'] = "MultipleChoice"
                group_analysis_dict['noOfResponses'] = "null"
                group_analysis_dict['options'] = []
                
                for group in group_question_dict:
                    group_stats = {}
                    group_stats['name'] = group
                    group_stats['top'] = []
                    total = 0
                    for i in groups_sorted[group]:
                        total = total + groups_sorted[group][i]
                        
                    cum=0
                    for i in groups_sorted[group]:
                        tmp = {}
                        tmp["name"] = i
                        tmp["frequency"] = groups_sorted[group][i]
                        cum = cum + groups_sorted[group][i]
                        tmp["cumulativeFrequency"] = cum
                        tmp["percent"] = float("{0:.2f}".format((groups_sorted[group][i]/(total*1.0))*100))
                        tmp["cumulativePercent"] = float("{0:.2f}".format((cum/(total*1.0))*100))
                        group_stats['top'].append(tmp)
                        
                    group_analysis_dict['options'].append(group_stats)
                    
                res['AnalysisList'].append(group_analysis_dict)
        
                print("Namaskaram - ur in custom report analysis")
                return res
    


       
                    
            elif (typeOfAnalysis == 'GroupAnalysis'):
                Object.logger.logActivity("INFO", "forming backend request for " + typeOfAnalysis, __name__)
            
            elif (typeOfAnalysis == 'ComparisonAnalysis'):
                Object.logger.logActivity("INFO", "forming backend request for " + typeOfAnalysis, __name__)
                
            elif (typeOfAnalysis == 'TrendAnalysis'):
                Object.logger.logActivity("INFO", "forming backend request for " + typeOfAnalysis, __name__)
            
            else:
                Object.logger.logActivity("INFO", "forming backend request for " + typeOfAnalysis, __name__)
        
            
        except Exception as err:
            Object.logger.logActivity("INFO", "error in processing data : " + str(err), __name__)
            
        
# end of class StatisticalMethods 
        