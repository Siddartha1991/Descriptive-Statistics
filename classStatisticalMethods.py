import collections
import pandas as pd
from statistics import mode
import numpy as np
import simplejson as json
from numpy.ma.core import getdata


class StatisticalMethods(object):
    def __init__ (self):
        pass
        
    
    def processData(self, typeOfAnalysis, dataSet, from_date, to_date ,json_data, Object):
        try:
            Object.logger.logActivity("INFO", "dataSet : " + str(dataSet), __name__)
            if (typeOfAnalysis == 'RequestAnalysis'):
                Object.logger.logActivity("INFO", "forming backend request for " + typeOfAnalysis, __name__)
                print('in request anaysis')
                
                resp = json_data
                    
                resp1 = resp['pages'][0]
                resp2 = resp1['questions']
                
                j=1
                
                question_with_options = {}
                for ques in resp2:
                    if ques['type'] == 'multiple':
                        question_with_options[ques['_id']] = []
                        ans = (ques['answerConfig'].keys())
                        for each_option in ques['answerConfig']['options']:
                            question_with_options[ques['_id']].append(each_option['title'])

                # for grid questions                
                question_with_options_grid = {}
                for ques in resp2:
                    if ques['type'] == 'grid':
                        tmp = []
                        for each_option in ques['answerConfig']['options']:
                            tmp.append((each_option['title']).strip())
                        question_with_options_grid[ques['_id']] = {}
                        for each_row in ques['answerConfig']['rows']:
                            question_with_options_grid[ques['_id']][(each_row['title']).strip()] = tmp

                samp=pd.DataFrame(dataSet)
                one = pd.DataFrame(samp['answers'])
                # ques_dict_disp maintains display value of option that user selected (for eg, if user selects red option for q1, it stores red )
                ques_dict_disp = {}
                res = {}
                # assigning project ID - need to update this as per real time response file
                res['projectID'] = samp['projectId'][0]
                # do not have consistency in todatetime and fromdatetime
                res['fromdatetime'] = from_date
                res['todatetime'] = to_date
                # do not have 'type of analysis' input from json
                res['TypeofAnalysis'] = 'QuestionAnalysis'
                res['AnalysisList'] = []
                # code which fetches question and its type . we need this for performing type wise analysis.
                questype = {}
                for i in range(one.shape[0]):
                    ques_per_person = one['answers'][i]
                    for ques in ques_per_person:
                        questype[ques['questionId']] = ques['question'][0]['type']
                # ques_name is a dict which stores names of each question : 
                ques_name = {}
                for i in range(one.shape[0]):
                    ques_per_person = one['answers'][i]
                    for ques in ques_per_person:
                        ques_name[ques['questionId']] = ques['question'][0]['title']
                

                for i in range(one.shape[0]):
                    ques_per_person = one['answers'][i]
                    for ques in ques_per_person:
                        if questype[ques['questionId']] != 'grid' and questype[ques['questionId']] != 'simple':
                            print(questype[ques['questionId']])
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
                        elif questype[ques['questionId']] == 'simple':
                            print(questype[ques['questionId']],'in simple')
                            if ques['questionId'] not in ques_dict_disp:
                                ques_dict_disp[ques['questionId']] = {}
                                if ques['assignedOptionValue'] not in ques_dict_disp[ques['questionId']]:
                                    ques_dict_disp[ques['questionId']][ques['assignedOptionValue']] = [
                                        ques['selectedOptionActualValue']]
                                else:
                                    ques_dict_disp[ques['questionId']][ques['assignedOptionValue']].append(
                                        ques['selectedOptionActualValue'])
                            else:
                                if ques['assignedOptionValue'] not in ques_dict_disp[ques['questionId']]:
                                    ques_dict_disp[ques['questionId']][ques['assignedOptionValue']] = [
                                        ques['selectedOptionActualValue']]
                                else:
                                    ques_dict_disp[ques['questionId']][ques['assignedOptionValue']].append(
                                        ques['selectedOptionActualValue'])
                        else:
                            print(ques['questionId'])
                            if ques['questionId'] not in ques_dict_disp:
                                ques_dict_disp[ques['questionId']] = {}
                                if (ques['selectedOptionDisplayValue'].rsplit(',',1)[0]).strip() not in ques_dict_disp[ques['questionId']]:
                                    ques_dict_disp[ques['questionId']][(ques['selectedOptionDisplayValue'].rsplit(',',1)[0]).strip()] = {}
                                    if (ques['selectedOptionDisplayValue'].rsplit(',',1)[1]).strip() not in \
                                            ques_dict_disp[ques['questionId']][(ques['selectedOptionDisplayValue'].rsplit(',',1)[0]).strip()]:
                                        ques_dict_disp[ques['questionId']][(ques['selectedOptionDisplayValue'].rsplit(',',1)[0]).strip()][
                                            (ques['selectedOptionDisplayValue'].rsplit(',',1)[1]).strip()] = [
                                            ques['assignedOptionValue']]
                                    else:
                                        ques_dict_disp[ques['questionId']][(ques['selectedOptionDisplayValue'].rsplit(',',1)[0]).strip()][
                                            (ques['selectedOptionDisplayValue'].rsplit(',',1)[1]).strip()].append(
                                            ques['assignedOptionValue'])
                                else:
                                    if (ques['selectedOptionDisplayValue'].rsplit(',',1)[1]).strip() not in \
                                            ques_dict_disp[ques['questionId']][(ques['selectedOptionDisplayValue'].rsplit(',',1)[0]).strip()]:
                                        ques_dict_disp[ques['questionId']][(ques['selectedOptionDisplayValue'].rsplit(',',1)[0]).strip()][
                                            (ques['selectedOptionDisplayValue'].rsplit(',',1)[1]).strip()] = [
                                            ques['assignedOptionValue']]
                                    else:
                                        ques_dict_disp[ques['questionId']][(ques['selectedOptionDisplayValue'].rsplit(',',1)[0]).strip()][
                                            (ques['selectedOptionDisplayValue'].rsplit(',',1)[1]).strip()].append(
                                            ques['assignedOptionValue'])
                            else:

                                if (ques['selectedOptionDisplayValue'].rsplit(',',1)[0]).strip() not in ques_dict_disp[ques['questionId']]:
                                    ques_dict_disp[ques['questionId']][(ques['selectedOptionDisplayValue'].rsplit(',',1)[0]).strip()] = {}
                                    if (ques['selectedOptionDisplayValue'].rsplit(',',1)[1]).strip() not in \
                                            ques_dict_disp[ques['questionId']][(ques['selectedOptionDisplayValue'].rsplit(',',1)[0]).strip()]:
                                        ques_dict_disp[ques['questionId']][(ques['selectedOptionDisplayValue'].rsplit(',',1)[0]).strip()][
                                            (ques['selectedOptionDisplayValue'].rsplit(',',1)[1]).strip()] = [
                                            ques['assignedOptionValue']]
                                    else:
                                        ques_dict_disp[ques['questionId']][(ques['selectedOptionDisplayValue'].rsplit(',',1)[0]).strip()][
                                            (ques['selectedOptionDisplayValue'].rsplit(',',1)[1]).strip()].append(
                                            ques['assignedOptionValue'])
                                else:
                                    if (ques['selectedOptionDisplayValue'].rsplit(',',1)[1]).strip() not in \
                                            ques_dict_disp[ques['questionId']][(ques['selectedOptionDisplayValue'].rsplit(',',1)[0]).strip()]:
                                        ques_dict_disp[ques['questionId']][(ques['selectedOptionDisplayValue'].rsplit(',',1)[0]).strip()][
                                            (ques['selectedOptionDisplayValue'].rsplit(',',1)[1]).strip()] = [
                                            ques['assignedOptionValue']]
                                    else:
                                        ques_dict_disp[ques['questionId']][(ques['selectedOptionDisplayValue'].rsplit(',',1)[0]).strip()][
                                            (ques['selectedOptionDisplayValue'].rsplit(',',1)[1]).strip()].append(
                                            ques['assignedOptionValue'])
                
                print('here')

                #print(ques_dict_disp)
                ques_num_resp = {}
                for qid in ques_dict_disp:
                    length = []
                    for opt in ques_dict_disp[qid]:
                        for p in ques_dict_disp[qid][opt]:
                            length.append(p)
                    ques_num_resp[qid] = len(length)
                print(ques_num_resp)


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
                # code to calculate total entries for grid
                gleng = {}
                grid_positions = {}

                for qid in ques_dict_disp:
                    if questype[qid]=='grid':
                        grid_positions[qid] = []
                        for aid in ques_dict_disp[qid]:
                            for position in ques_dict_disp[qid][aid]:
                                grid_positions[qid].append(position)
                print('grid pos')

                for qid in ques_dict_disp:
                    cum_fre = 0
                    if questype[qid] == 'grid':
                        gleng[qid] = {}
                        tmp = set(grid_positions[qid])
                        temp2 = {}
                        for i in tmp:
                            temp2[i] = []
                        for aid in ques_dict_disp[qid]:
                            for gid in (ques_dict_disp[qid][aid]):
                                for pos in tmp:
                                    if pos == gid:
                                        for item in (ques_dict_disp[qid][aid][gid]):
                                            temp2[pos].append(item)
                        for p in tmp:
                            gleng[qid][p] = len(temp2[p])
                print("gleng")
                #print(ques_dict_disp)
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
                ques_opt = {}
                for qid in ques_dict_disp:
                    ques_opt[qid] = {}
                    for aid in ques_dict_disp[qid]:
                        ques_opt[qid][aid] = len(ques_dict_disp[qid][aid])
                print('hereeeeeeeeeeeeeee')       
                print(ques_opt)
                
                
                        
                def Freq_Cal(question_results, ques_dict_disp):
                    cum_fre = 0
                    print(qid)
                    print(question_with_options[qid])
                    select_options = []
                    for aid in ques_dict_disp[qid]:
                        select_options.append(aid)
                    li = question_with_options[qid]
                    print('sorting')
                    dict1 = ques_opt[qid]
                    srt = sorted(dict1, key=dict1.get)
                    rest_options = set(li) - set(select_options)
                    for aid in reversed(srt):
                        freq_stats = {}
                        freq_stats['name'] = aid
                        freq_stats['freq'] = len(ques_dict_disp[qid][aid])
                        freq_stats['percent'] = round(len(ques_dict_disp[qid][aid]) / (leng[qid] * 1.0) * 100,2)
                        cum_fre = (len(ques_dict_disp[qid][aid])) + cum_fre
                        freq_stats['cum_freq'] = cum_fre
                        freq_stats['cum_percent'] = round((cum_fre / (leng[qid] * 1.0) * 100),2)
                        question_results['options'].append(freq_stats)
                    for bid in rest_options:
                        freq_stats = {}
                        freq_stats['name'] = bid
                        freq_stats['freq'] = 0
                        freq_stats['percent'] = 0
                        freq_stats['cum_freq'] = cum_fre
                        freq_stats['cum_percent'] = 100.0
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
                # constructing question_position dictionary which is used for giving q_order :
                #creating question position dict:
                question_position ={}
                for i in range(one.shape[0]):
                    ques_per_person = one['answers'][i]
                    for ques in ques_per_person:
                        question_position[ques['questionId']] = ques['question'][0]['position']
                #q_order = 0

                #creating dict to find no of responses for each sub question in grid type:
                ques_len = {}

                for ques in ques_dict_disp:
                    if questype[ques] == 'grid':
                        ques_len[ques] = {}
                        for option in ques_dict_disp[ques]:
                            total = 0
                            for p in ques_dict_disp[ques][option]:
                                total = total + len(ques_dict_disp[ques][option][p])
                            ques_len[ques][option] = total
                print('ques_ken')
                print(ques_len)

                #now finding freq stats for each sub question in grid type for every option they have:
                grid_temp = {}
                for ques in ques_dict_disp:
                    if questype[ques] == 'grid':
                        print('in grid temp..')
                        grid_temp[ques] = {}
                        for option in ques_dict_disp[ques]:
                            grid_temp[ques][option] = []
                            cum = 0
                            ordr = 1
                            select_options=[]
                            print(option)
                            
                            for i in ques_dict_disp[ques][option]:
                                i = i.strip()
                                select_options.append(i)
                                
                            ques_opt1 = {}
                            for rid in ques_dict_disp[ques]:
                                ques_opt1[rid] = {}
                                for aid in ques_dict_disp[ques][rid]:
                                    ques_opt1[rid][aid] = len(ques_dict_disp[ques][rid][aid])
                            print(ques_opt1)
                            print(ques)
                            dict1 = ques_opt1[option]
                            srt = sorted(dict1, key=dict1.get)    
                            print(ques)
                            print(option)

                            #print(question_with_options_grid['58b1b8e563d53c679fd12186'][option])
                            li  = question_with_options_grid[ques][option]
                            print(li)

                            rest_options = set(li) - set(select_options)
                            print(li)
                            print(select_options)
                            print(rest_options)
                            for i in reversed(srt):
                                tmp = {}
                                tmp['name'] = i
                                le = len(ques_dict_disp[ques][option][i])
                                tmp['frequency'] = le
                                tmp['percent'] = float("{0:.2f}".format((le/(ques_len[ques][option]*1.0))*100))
                                cum = cum + le
                                tmp['cum_freq'] = cum
                                tmp['cum_percent'] = float("{0:.2f}".format((cum/(ques_len[ques][option]*1.0))*100))
                                tmp['order'] = ordr
                                ordr = ordr + 1
                                grid_temp[ques][option].append(tmp)
                            #assigning stats for non selected options in particular row
                            for i in rest_options:
                                tmp = {}
                                tmp['name'] = i
                                tmp['frequency'] = 0
                                tmp['percent'] = 0
                                tmp['cum_freq'] = cum
                                tmp['cum_percent'] = 100.0
                                tmp['order'] = ordr
                                ordr = ordr + 1
                                grid_temp[ques][option].append(tmp)

                print('grid_temmp')
                print(grid_temp)
                for qid in ques_dict_disp:
                    #q_order = q_order + 1
                    question_results = {}
                    question_results['qid'] = qid 
                    question_results['qstring'] =ques_name[qid]
                    question_results['qType'] = questype[qid]
                    question_results['qOrder'] = question_position[qid]
                    question_results['noOfAnswers'] = ques_num_resp[qid] # need to change here 
                    question_results['options'] = []

                    ######################################################
                    # multiple choice type questions
                    ######################################################
                    if (questype[qid] == 'multiple'):
                        print(' in multiple...')
                        Stats_Cal(question_results, ques_dict_disp)
                        print(' iuuse here...')
                        Freq_Cal(question_results, ques_dict_disp)
                        print('isse here')
                        question_results['OtherEntries'] = []
                        for i in range(one.shape[0]):
                            ques_per_person = one['answers'][i]
                            for ques in ques_per_person:
                                if ques['selectedOptionDisplayValue'] == 'Other' and ques['questionId'] == qid:
                                    question_results['OtherEntries'].append(ques['selectedOptionActualValue'])

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
                        print('in numeric..')

                        question_results['numeric_items'] = []
                        for aid in ques_dict_disp[qid]:
                            for num in ques_dict_disp[qid][aid]:
                                question_results['numeric_items'].append(num)


                        Stats_Cal(question_results, ques_dict_disp)
                        question_results['options'] = 'null'
                        res['AnalysisList'].append(question_results)

                    ######################################################
                    # Simple type questions
                    ######################################################

                    if (questype[qid] == 'simple'):
                        print('in simple..')
                        question_results['text_items'] = []
                        for aid in ques_dict_disp[qid]:
                            for text in ques_dict_disp[qid][aid]:
                                question_results['text_items'].append(text)
                        res['AnalysisList'].append(question_results)

                    ######################################################
                    # Grid type questions
                    ######################################################
                    if (questype[qid] == 'grid'):
                        print('in grid..')
                        # Stats_Cal(question_results,ques_dict_disp)
                        question_results['options'] = []
                        question_results['statements'] = []
                        consolidated_list=[]
                        for rowid in ques_dict_disp[qid]:
                            li = []
                            temp_grid_stats = {}
                            for gid in ques_dict_disp[qid][rowid]:
                                for item in (ques_dict_disp[qid][rowid][gid]):
                                    li.append(item)
                            temp_grid_stats['statement'] = rowid
                            temp_grid_stats['order'] = 1
                            temp_grid_stats['mean'] = float("{0:.2f}".format(np.mean(li)))
                            temp_grid_stats['median'] = float("{0:.2f}".format(np.median(li)))
                            temp_grid_stats['mode'] = pd.DataFrame(li).mode()[0].tolist()  ## mode can take multiple values - so there is no one single value?
                            temp_grid_stats['variance'] = float("{0:.2f}".format(np.var(li)))
                            temp_grid_stats['standard deviation'] = float("{0:.2f}".format(np.std(li)))
                            temp_grid_stats['noofResponses'] = len(li)
                            temp_grid_stats['options'] = grid_temp[qid][rowid]

                            for i in li :
                                consolidated_list.append(i)
                            question_results['statements'].append(temp_grid_stats)


                        total = 0


                        question_results['statistics'] = {}
                        question_results['statistics']['mean'] = float("{0:.2f}".format(np.mean(consolidated_list)))
                        question_results['statistics']['median'] = float("{0:.2f}".format(np.median(consolidated_list)))
                        question_results['statistics']['mode'] = pd.DataFrame(consolidated_list).mode()[0].tolist()  ## mode can take multiple values - so there is no one single value?
                        question_results['statistics']['variance'] = float("{0:.2f}".format(np.var(consolidated_list)))
                        question_results['statistics']['standard deviation'] = float("{0:.2f}".format(np.std(consolidated_list)))

                        for p in gleng[qid]:
                            total = total + gleng[qid][p]

                        question_results['noOfAnswers'] = total
                        cum_fre = 0
                        select_options = []
                        for j in gleng[qid]:
                            select_options.append(j)
                        li = []
                        cou = 0
                        for j in question_with_options_grid[qid]:
                            if(cou == 0):
                                li = question_with_options_grid[qid][j]
                                cou = cou + 1
                        rest_options = set(li) - set(select_options)
                        print('vanakam')
                        dict1 = gleng[qid]
                        srt = sorted(dict1, key=dict1.get)
                        print(srt)
                        for i in reversed(srt):
                            freq_stats = {}
                            freq_stats['name'] = i
                            freq_stats['freq'] = gleng[qid][i]
                            freq_stats['percent'] = round((gleng[qid][i] / (total * 1.0)*100),2)
                            cum_fre = cum_fre + gleng[qid][i]
                            freq_stats['cum_freq'] = cum_fre
                            freq_stats['cum_percent'] = round((cum_fre / (total * 1.0)*100),2)
                            question_results['options'].append(freq_stats)

                        for i in rest_options:
                            freq_stats = {}
                            freq_stats['name'] = i
                            freq_stats['freq'] = 0
                            freq_stats['percent'] = 0
                            freq_stats['cum_freq'] = cum_fre
                            freq_stats['cum_percent'] = 100.0
                            question_results['options'].append(freq_stats)

                        res['AnalysisList'].append(question_results)

                (res)
                
                
               
                return res

            elif (typeOfAnalysis == 'ECLCustomReport'):
                
                print('in customer report')
                resp = json_data
                    
                resp1 = resp['pages'][0]
                print(resp.keys())
                resp2 = resp1['questions']
                j=1
                question_with_options = {}
                for ques in resp2:
                    if ques['type'] == 'multiple':
                        question_with_options[ques['_id']] = []
                        #print(ques['type'])
                        ans = (ques['answerConfig'].keys())
                        for each_option in ques['answerConfig']['options']:
                            #print(ques['answerConfig'][opt][0])
                            question_with_options[ques['_id']].append(each_option['title'])
                
                # for grid questions                
                question_with_options_grid = {}
                for ques in resp2:
                    if ques['type'] == 'grid':
                        tmp = []
                        for each_option in ques['answerConfig']['options']:
                            tmp.append(each_option['title'])
                        question_with_options_grid[ques['_id']] = {}
                        for each_row in ques['answerConfig']['rows']:
                            question_with_options_grid[ques['_id']][each_row['title']] = tmp
                                
                
                print(question_with_options)
                
                
                
                
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
                
                def Freq_Cal(question_results, ques_dict_disp):
                    question_results['table_statistics']['option'] = {}
                    
                    select_options = []
                    print(ques_dict_disp[qid])
                    for aid in ques_dict_disp[qid]:
                        select_options.append(aid)
                    print(select_options)
                    print('ll')
                    print(question_with_options)
                    li = question_with_options[qid]
                    
                    print(li)
                    rest_options = set(li) - set(select_options)
                    print(rest_options)
                    cum_fre = 0
                    print(qid)
                    dict1 = ques_opt[qid]
                    srt = sorted(dict1, key=dict1.get)
                    for aid in reversed(srt):
                        question_results['table_statistics']['option'][aid]={}
                        freq_stats = {}
                        tmp = {}
                        freq_stats['name'] = aid
                        freq_stats['freq'] = len(ques_dict_disp[qid][aid])
                        tmp['frequency'] = len(ques_dict_disp[qid][aid])
                        freq_stats['percent'] = round(len(ques_dict_disp[qid][aid]) / (leng[qid] * 1.0) * 100,2)
                        tmp['percent'] = round(len(ques_dict_disp[qid][aid]) / (leng[qid] * 1.0) * 100,2)
                        question_results['table_statistics']['option'][aid]=tmp
                        cum_fre = (len(ques_dict_disp[qid][aid])) + cum_fre
                        freq_stats['cum_freq'] = cum_fre
                        freq_stats['cum_percent'] = round((cum_fre / (leng[qid] * 1.0) * 100),2)
                        question_results['options'].append(freq_stats)
                        
                    for bid in rest_options:
                        freq_stats = {}
                        freq_stats['name'] = bid
                        freq_stats['freq'] = 0
                        freq_stats['percent'] = 0
                        freq_stats['cum_freq'] = cum_fre
                        freq_stats['cum_percent'] = 100.0
                        question_results['options'].append(freq_stats)
                    
                    tmp2 = {}
                    tmp2['total'] = cum_fre
                    tmp2['total percent'] = float("{0:.2f}".format((cum_fre/(num_of_responses_2[qid]*1.0))*100))
                    question_results['table_statistics']['total_stats'] = tmp2
                
                
                        
                #samp = pd.read_json('F:/projectSurveyAnalysis/customer report docs/cr_backend_new2.json')
                samp=pd.DataFrame(dataSet)
                one = pd.DataFrame(samp['answers'])
                res = {}
                # assigning project ID - need to update this as per real time response file
                res['projectID'] = samp['projectId'][0]
                # do not have consistency in todatetime and fromdatetime
                res['fromdatetime'] = from_date
                res['todatetime'] = to_date
                # do not have 'type of analysis' input from json
                res['TypeofAnalysis'] = 'Custom Report'
                res['AnalysisList'] = []
                
                
                #creating question type dictionary
                
                questype = {}
                for i in range(one.shape[0]):
                    ques_per_person = one['answers'][i]
                    for ques in ques_per_person:
                        questype[ques['questionId']] = ques['question'][0]['type']
                        
                ques_name = {}
                for i in range(one.shape[0]):
                    ques_per_person = one['answers'][i]
                    for ques in ques_per_person:
                        ques_name[ques['questionId']] = ques['question'][0]['title']
                
                ques_dict_disp_cr = {}
                
                #questions = [9,30,26]
                questions = [10,32]
                
                ques_dict_disp_cr_final = {}
                for i in range(one.shape[0]):
                    ques_per_person = one['answers'][i]
                    for ques in ques_per_person:
                        if questype[ques['questionId']] != 'simple':
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
                        elif questype[ques['questionId']] == 'simple':
                            print(questype[ques['questionId']],'in simple')
                            if ques['questionId'] not in ques_dict_disp_cr:
                                ques_dict_disp_cr[ques['questionId']] = {}
                                if ques['assignedOptionValue'] not in ques_dict_disp_cr[ques['questionId']]:
                                    ques_dict_disp_cr[ques['questionId']][ques['assignedOptionValue']] = [
                                        ques['selectedOptionActualValue']]
                                else:
                                    ques_dict_disp_cr[ques['questionId']][ques['assignedOptionValue']].append(
                                        ques['selectedOptionActualValue'])
                            else:
                                if ques['assignedOptionValue'] not in ques_dict_disp_cr[ques['questionId']]:
                                    ques_dict_disp_cr[ques['questionId']][ques['assignedOptionValue']] = [
                                        ques['selectedOptionActualValue']]
                                else:
                                    ques_dict_disp_cr[ques['questionId']][ques['assignedOptionValue']].append(
                                        ques['selectedOptionActualValue'])
                
                ques_opt = {}
                for qid in ques_dict_disp_cr:
                    ques_opt[qid] = {}
                    for aid in ques_dict_disp_cr[qid]:
                        ques_opt[qid][aid] = len(ques_dict_disp_cr[qid][aid])
                        
                        
                for i in range(one.shape[0]):
                    ques_per_person = one['answers'][i]
                    for ques in ques_per_person:            
                        for i in ques_dict_disp_cr:
                            if ques['question'][0]['position'] in questions:
                                if(ques['questionId'] == i):
                                    #print(ques['question'][0]['position'])
                                    ques_dict_disp_cr_final[i] = {}
                                    for j in ques_dict_disp_cr[i]:
                                        #print(ques_dict_disp_cr[i][j])
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
                    print(l)
                    length = len(l)-1
                    if length > 4: 
                        for p in range(length):
                            #print(l[p])
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
                    else:
                        for p in range(length+1):
                            for r in keys:
                                if(ques_dict_disp_cr_final[i][r] == l[p]):
                                    ques_dict_disp_cr_final_sorted[i][r] = l[p]
                            
                ##################### defining top 5 stats 
                print('sorted')
                print(ques_dict_disp_cr_final_sorted)
                for qid in ques_dict_disp_cr_final:
                    top_five_stats = {}
                    top_five_stats['qid'] = qid
                    top_five_stats['qstring'] = ques_name[qid]
                    top_five_stats['qorder'] = question_position[qid]
                    top_five_stats['qType'] = questype[qid]
                    top_five_stats['noOfResponses'] = num_of_responses[qid]
                    top_five_stats['options'] = []
                    top_five_stats['statistics'] ={}
                    top_five_stats['table_statistics'] = {}
                    print('hey')
                    total = 0
                    #cal num of top 5 responses for each question
                    for i in ques_dict_disp_cr_final_sorted[qid]:  
                        total = total + ques_dict_disp_cr_final_sorted[qid][i]
                    print(total)
                    top_five_stats['table_statistics']['total_stats'] = {}
                    tmp = {}
                    tmp['total'] = total
                    tmp['total percent'] = float("{0:.2f}".format((total/(num_of_responses[qid]*1.0))*100))
                    top_five_stats['table_statistics']['total_stats'] = tmp
                    
                    order = 1
                    cum = 0
                    top_five_stats['table_statistics']['option'] = {}
                    
                    print('welcome1212')
                    print(ques_dict_disp_cr_final_sorted)
                    dict1 = ques_dict_disp_cr_final_sorted[qid]
                    srt = sorted(dict1, key=dict1.get)    
                    for i in reversed(srt):
                        print('bye')
                        top_five_stats['table_statistics']['option'][i]={}
                        option_dict = {}
                        tmp2 = {}
                        #option_dict['qid'] = i
                       
                        option_dict["name"] = i
                        option_dict["order"] = order
                        order = order+1
                        option_dict["frequency"] = ques_dict_disp_cr_final_sorted[qid][i]
                        tmp2["frequency"] = ques_dict_disp_cr_final_sorted[qid][i]
                        option_dict["percent"] = float("{0:.2f}".format(((ques_dict_disp_cr_final_sorted[qid][i])/(total*1.0))*100))
                        tmp2["percent"] = float("{0:.2f}".format(((ques_dict_disp_cr_final_sorted[qid][i])/(total*1.0))*100))
                        top_five_stats['table_statistics']['option'][i] = tmp2
                        cum = cum + ques_dict_disp_cr_final_sorted[qid][i]
                        option_dict["cumulativeFrequency"] = cum
                        option_dict["cumulativePercent"] = float("{0:.2f}".format((cum/(total*1.0))*100))
                        top_five_stats['options'].append(option_dict)
                    
                    print('bye1')
                    Stats_Cal(top_five_stats,ques_dict_disp_cr)
                    res['AnalysisList'].append(top_five_stats)
                ########################################
                    
                ###########BUILDING GROUPING 10-25 questions report
                
                
                # building grouped report for q no 9 - 25 :
                ques_dict_disp_group_final = {}
                #questions_group = [10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]
                questions_group = [12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27]
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
                            
                pos_neg_dict = {}
                pos_neg_dict['positive'] = {}
                pos_neg_dict['negative'] = {}
                for i in group_question_dict:
                    if i == 'Agree' or i == 'Strongly Agree':
                        for j in group_question_dict[i]:
                            if j not in pos_neg_dict['positive']:
                                pos_neg_dict['positive'][j] = group_question_dict[i][j]
                            else:
                                pos_neg_dict['positive'][j] = pos_neg_dict['positive'][j]+group_question_dict[i][j]
                    elif i == 'Disagree' or i == 'Strongly Disagree':
                         for j in group_question_dict[i]:
                            if j not in pos_neg_dict['negative']:
                                pos_neg_dict['negative'][j] = group_question_dict[i][j]
                            else:
                                pos_neg_dict['negative'][j] = pos_neg_dict['negative'][j]+group_question_dict[i][j]
                

                groups_sorted = {}
                for i in pos_neg_dict:
                    groups_sorted[i] = {}
                    l = []
                    keys = []
                    count = 0
                    for j in pos_neg_dict[i]:
                        keys.append(j)
                        l.append(pos_neg_dict[i][j])
                    l.sort(reverse = True)
                    length = len(l)-1
                    for p in range(length):
                        if(count<5):
                            if(l[p] == l[p+1]):
                                for r in keys:
                                    if(pos_neg_dict[i][r] == l[p]):
                                        groups_sorted[i][r] = l[p]
                            else:
                                for r in keys:
                                    if(pos_neg_dict[i][r] == l[p]):
                                        groups_sorted[i][r] = l[p]
                                count = count + 1
                
                    

    
####################

                group_analysis_dict = {}
                group_analysis_dict['qString'] = "GroupingQuestion"
                group_analysis_dict['qOrder'] = questions_group
                group_analysis_dict['qType'] = "MultipleChoice"
                group_analysis_dict['options'] = []
                num_of_resp = 0
                for group in pos_neg_dict:
                    group_stats = {}
                    group_stats['selectedOptionLabel'] = group
                    group_stats['group'] = []
                    total = 0
                    for i in groups_sorted[group]:
                        total = total + groups_sorted[group][i]
                    num_of_resp = num_of_resp + total
                        
                    cum=0
                    print('welcome143')
                    dict1 = groups_sorted[group]
                    srt = sorted(dict1, key=dict1.get)
                    print(groups_sorted)
                    for i in reversed(srt):
                        
                        tmp = {}
                        tmp["name"] = ques_name[i]
                        tmp['qid'] = i
                        tmp["frequency"] = groups_sorted[group][i]
                        cum = cum + groups_sorted[group][i]
                        tmp["cumulativeFrequency"] = cum
                        tmp["percent"] = float("{0:.2f}".format((groups_sorted[group][i]/(total*1.0))*100))
                        tmp["cumulativePercent"] = float("{0:.2f}".format((cum/(total*1.0))*100))
                        group_stats['group'].append(tmp)
                        
                    group_analysis_dict['options'].append(group_stats)
                group_analysis_dict['noOfResponses'] = num_of_resp      
                res['AnalysisList'].append(group_analysis_dict)            
                                
                
                
                #remain_ques_list = [9,30,33,34,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,31]
                #remain_ques_list = [4,6,9]
                remain_ques_list = [4,6,9,34,36,28]
                
                
                leng = {}
                for qid in ques_dict_disp_cr:
                    if question_position[qid] in remain_ques_list:
                        li = []
                        cum_fre = 0
                        for aid in ques_dict_disp_cr[qid]:
                            for item in (ques_dict_disp_cr[qid][aid]):
                                li.append(item)
                        leng[qid] = len(li)
                    
                print(leng)   
                ques_dict_disp_cr_final_2 = {}
                for i in range(one.shape[0]):
                    ques_per_person = one['answers'][i]
                    for ques in ques_per_person:            
                        for i in ques_dict_disp_cr:
                            #print(i)
                            #print(ques['questionId'])
                            #print(ques['question'][0]['position'])
                            #print(ques_dict_disp_cr_final_2)
                            if ques['question'][0]['position']  in remain_ques_list:
                                #print('rest')
                                #print(i)
                                #print(ques['questionId'])
                                if(ques['questionId'] == i):
                                    #print(ques['question'][0]['position'])
                                    #print('resk')
                                    ques_dict_disp_cr_final_2[i] = {}
                                    for j in ques_dict_disp_cr[i]:
                                        #print(ques_dict_disp_cr[i][j])
                                        #print(ques_dict_disp_cr_final_2)
                                        ques_dict_disp_cr_final_2[i][j] = len(ques_dict_disp_cr[i][j])
                                        
                
                #print(ques_dict_disp_cr_final_2)
                print('wow')
                num_of_responses_2={}
                for i in ques_dict_disp_cr_final_2:
                    sum = 0
                    for j in ques_dict_disp_cr_final_2[i]:
                        sum = sum + ques_dict_disp_cr_final_2[i][j]
                    num_of_responses_2[i]=sum
                
                print(num_of_responses_2)
                    
                #print(ques_dict_disp_cr.keys())
                for qid in ques_dict_disp_cr:
                    #print(qid)
                    if question_position[qid]  in remain_ques_list:
                        #print(question_position[qid])
                        #print(qid)
                        question_results = {}
                        question_results['qid'] = qid
                        question_results['qstring'] = ques_name[qid]
                        question_results['qorder'] = question_position[qid]
                        question_results['qType'] = questype[qid]
                        question_results['noOfResponses'] = num_of_responses_2[qid]
                        question_results['table_statistics'] = {}
                        
                        
                        question_results['options'] = []
                        question_results['statistics'] ={}
                        """
                        Stats_Cal(question_results, ques_dict_disp_cr)
                        print('wow2')
                        print(question_position[qid])
                        print(qid)
                        Freq_Cal(question_results, ques_dict_disp_cr)
                        print(question_results)
                        res['AnalysisList'].append(question_results)
                        """
                        
                        ######################################################
                        # multiple choice type questions
                        ######################################################
                        if (questype[qid] == 'multiple'):
                            print(' in multiple...')
                            Stats_Cal(question_results, ques_dict_disp_cr)
                            print(' iuuse here...')
                            Freq_Cal(question_results, ques_dict_disp_cr)
                            print('isse here')
                            question_results['OtherEntries'] = []
                            for i in range(one.shape[0]):
                                ques_per_person = one['answers'][i]
                                for ques in ques_per_person:
                                    if ques['selectedOptionDisplayValue'] == 'Other' and ques['questionId'] == qid:
                                        question_results['OtherEntries'].append(ques['selectedOptionActualValue'])
    
                            res['AnalysisList'].append(question_results)
    
    
                        ######################################################
                        # Simple type questions
                        ######################################################
    
                        if (questype[qid] == 'simple'):
                            print('in simple..')
                            question_results['text_items'] = []
                            for aid in ques_dict_disp_cr[qid]:
                                for text in ques_dict_disp_cr[qid][aid]:
                                    question_results['text_items'].append(text)
                            res['AnalysisList'].append(question_results)

                
                    
                
                        
                
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
            
     
    def CompareAnalysis(self, typeOfAnalysis, data_list, from_date, to_date ,options,json_data,Object):
        try:
            
            if (typeOfAnalysis == 'ComparisonAnalysis'):
                
                
                Object.logger.logActivity("INFO", "forming backend request for " + typeOfAnalysis, __name__)  
                
                
                resp = json_data
                
                print('helooooooooooooooo')
                resp1 = resp['pages'][0]
                print(resp.keys())
                resp2 = resp1['questions']
                
                question_with_options = {}
                for ques in resp2:
                    if ques['type'] == 'multiple':
                        print('in here,,')
                        question_with_options[ques['_id']] = []
                        ans = (ques['answerConfig'].keys())
                        for each_option in ques['answerConfig']['options']:
                            #print(ques['answerConfig'][opt][0])
                            print(each_option['title'])
                            question_with_options[ques['_id']].append(each_option['title'])
                print('queswithoptions')
                print(question_with_options)
                # for grid questions                
                question_with_options_grid = {}
                for ques in resp2:
                    if ques['type'] == 'grid':
                        tmp = []
                        for each_option in ques['answerConfig']['options']:
                            tmp.append((each_option['title']).strip())
                        question_with_options_grid[ques['_id']] = {}
                        for each_row in ques['answerConfig']['rows']:
                            question_with_options_grid[ques['_id']][(each_row['title']).strip()] = tmp

                print('grid positins')
                print(question_with_options_grid)
                
                
                
                ## framing required dataframes for analysis
                import pandas as pd
                #samp = pd.read_json('E:/work/caplabs_project_jan2017/comp_analy_samp_input.json')
                #samp2 = pd.read_json('E:/work/caplabs_project_jan2017/comp_ana_2_samp.json')
                print('hi')
                print(len(data_list))
                print('hello')
                dataSet_li = data_list
                samp_li = []
                for i in dataSet_li:
                    print('wsssp')
                    print(type(i))
                    samp_li.append(pd.DataFrame(i))
                    
                print(len(samp_li))
                ans_li = []
                for i in samp_li:
                    ans_li.append(pd.DataFrame(i['answers']))
                              
                print(len(ans_li))
                    
                
                #one = pd.DataFrame(samp['answers'])
                #two = pd.DataFrame(samp2['answers'])
                filters = options
                lis1 = []
                print('filters', filters)
                for j in range(len(ans_li)):
                    for i in range(ans_li[j].shape[0]):
                        ques_per_person = ans_li[j]['answers'][i]
                        for ques in ques_per_person:
                            if ques['questionId'] == filters[j]['questionId']:
                                if ques['selectedOptionPosition'] == filters[j]['answerPos'][0]:
                                    lis1.append(ques['selectedOptionDisplayValue'])
                        
                            
                        
                lis = list(set(lis1))
                print(lis)
                
                # ques_dict_disp maintains display value of option that user selected (for eg, if user selects red option for q1, it stores red )
                ques_dict_disp = {}
                
                res = {}
                # assigning project ID - need to update this as per real time response file
                res['projectID'] = samp_li[0]['projectId'][0]
                # do not have consistency in todatetime and fromdatetime
                res['fromdatetime'] = from_date
                res['todatetime'] = to_date
                
                # do not have 'type of analysis' input from json
                res['TypeofAnalysis'] = 'ComparisonAnalysis'
                
                res['AnalysisList'] = []
                
                # code which fetches question and its type . we need this for performing type wise analysis.

                
                
                questype = {}
                
                for j in range(len(ans_li)):
                    questype[lis[j]] = {}
                    for i in range(ans_li[j].shape[0]):
                        ques_per_person = ans_li[j]['answers'][i]
                        for ques in ques_per_person:
                            questype[lis[j]][ques['questionId']] = ques['question'][0]['type']
                print(questype)
                
                # ques_name is a dict which stores names of each question :
                ques_name = {}
                for j in range(len(ans_li)):
                    ques_name[lis[j]] = {}
                    for i in range(ans_li[j].shape[0]):
                        ques_per_person = ans_li[j]['answers'][i]
                        for ques in ques_per_person:
                            ques_name[lis[j]][ques['questionId']] = ques['question'][0]['title']
                            
                
                print(ques_name)
                
                
                # forming merged_question_name dictionary which contains names of all questions present in combined datasets
                merged_ques_name = {}
                for i in lis:
                    for j in ques_name[i]:
                        print(i, j)
                        merged_ques_name[j] = ques_name[i][j]
                print('list')
                print(merged_ques_name) 
                merged_ques_type = {}
                
                for i in lis:
                    for j in questype[i]:
                        merged_ques_type[j] = questype[i][j]
                print(merged_ques_type) 
                
                                
                # forming ques_dict_disp for red using one df:
                
                
                #ques_dict_disp
                # forming ques_dict_disp for red using one df:

                for j in range(len(ans_li)):
                    
                    ques_dict_disp[lis[j]] = {}
                    for i in range(ans_li[j].shape[0]):
                        ques_per_person = ans_li[j]['answers'][i]
                        for ques in ques_per_person:
                            if (questype[lis[j]][ques['questionId']] != 'grid') and (questype[lis[j]][ques['questionId']] != 'simple'):
                                if ques['questionId'] not in ques_dict_disp[lis[j]]:
                                    ques_dict_disp[lis[j]][ques['questionId']] = {}
                                    if ques['selectedOptionDisplayValue'] not in ques_dict_disp[lis[j]][ques['questionId']]:
                                        ques_dict_disp[lis[j]][ques['questionId']][ques['selectedOptionDisplayValue']] = [
                                            ques['assignedOptionValue']]
                                    else:
                                        ques_dict_disp[lis[j]][ques['questionId']][ques['selectedOptionDisplayValue']].append(
                                            ques['assignedOptionValue'])
                                else:
                                    if ques['selectedOptionDisplayValue'] not in ques_dict_disp[lis[j]][ques['questionId']]:
                                        ques_dict_disp[lis[j]][ques['questionId']][ques['selectedOptionDisplayValue']] = [
                                            ques['assignedOptionValue']]
                                    else:
                                        ques_dict_disp[lis[j]][ques['questionId']][ques['selectedOptionDisplayValue']].append(
                                            ques['assignedOptionValue'])
                                        
                            elif questype[lis[j]][ques['questionId']] == 'simple':
                                if ques['questionId'] not in ques_dict_disp[lis[j]]:
                                    ques_dict_disp[lis[j]][ques['questionId']] = {}
                                    if ques['assignedOptionValue'] not in ques_dict_disp[lis[j]][ques['questionId']]:
                                        ques_dict_disp[lis[j]][ques['questionId']][ques['assignedOptionValue']] = [
                                            ques['selectedOptionActualValue']]
                                    else:
                                        ques_dict_disp[lis[j]][ques['questionId']][ques['assignedOptionValue']].append(
                                            ques['selectedOptionActualValue'])
                                else:
                                    if ques['assignedOptionValue'] not in ques_dict_disp[lis[j]][ques['questionId']]:
                                        ques_dict_disp[lis[j]][ques['questionId']][ques['assignedOptionValue']] = [
                                            ques['selectedOptionActualValue']]
                                    else:
                                        ques_dict_disp[lis[j]][ques['questionId']][ques['assignedOptionValue']].append(
                                            ques['selectedOptionActualValue'])
                                    
                            else:
                                if ques['questionId'] not in ques_dict_disp[lis[j]]:
                                    ques_dict_disp[lis[j]][ques['questionId']] = {}
                                    if (ques['selectedOptionDisplayValue'].rsplit(',',1)[0]).strip() not in ques_dict_disp[lis[j]][ques['questionId']]:
                                        ques_dict_disp[lis[j]][ques['questionId']][(ques['selectedOptionDisplayValue'].rsplit(',',1)[0]).strip()] = {}
                                        if (ques['selectedOptionDisplayValue'].rsplit(',',1)[1]).strip() not in \
                                                ques_dict_disp[lis[j]][ques['questionId']][(ques['selectedOptionDisplayValue'].rsplit(',',1)[0]).strip()]:
                                            ques_dict_disp[lis[j]][ques['questionId']][(ques['selectedOptionDisplayValue'].rsplit(',',1)[0]).strip()][
                                                (ques['selectedOptionDisplayValue'].rsplit(',',1)[1]).strip()] = [
                                                ques['assignedOptionValue']]
                                        else:
                                            ques_dict_disp[lis[j]][ques['questionId']][(ques['selectedOptionDisplayValue'].rsplit(',',1)[0]).strip()][
                                                (ques['selectedOptionDisplayValue'].rsplit(',',1)[1]).strip()].append(
                                                ques['assignedOptionValue'])
                                    else:
                                        if (ques['selectedOptionDisplayValue'].rsplit(',',1)[1]).strip() not in \
                                                ques_dict_disp[lis[j]][ques['questionId']][(ques['selectedOptionDisplayValue'].rsplit(',',1)[0]).strip()]:
                                            ques_dict_disp[lis[j]][ques['questionId']][(ques['selectedOptionDisplayValue'].rsplit(',',1)[0]).strip()][
                                                (ques['selectedOptionDisplayValue'].rsplit(',',1)[1]).strip()] = [
                                                ques['assignedOptionValue']]
                                        else:
                                            ques_dict_disp[lis[j]][ques['questionId']][(ques['selectedOptionDisplayValue'].rsplit(',',1)[0]).strip()][
                                                (ques['selectedOptionDisplayValue'].rsplit(',',1)[1]).strip()].append(
                                                ques['assignedOptionValue'])
                                else:
                    
                                    if (ques['selectedOptionDisplayValue'].rsplit(',',1)[0]).strip() not in ques_dict_disp[lis[j]][ques['questionId']]:
                                        ques_dict_disp[lis[j]][ques['questionId']][(ques['selectedOptionDisplayValue'].rsplit(',',1)[0]).strip()] = {}
                                        if (ques['selectedOptionDisplayValue'].rsplit(',',1)[1]).strip() not in \
                                                ques_dict_disp[lis[j]][ques['questionId']][(ques['selectedOptionDisplayValue'].rsplit(',',1)[0]).strip()]:
                                            ques_dict_disp[lis[j]][ques['questionId']][(ques['selectedOptionDisplayValue'].rsplit(',',1)[0]).strip()][
                                                (ques['selectedOptionDisplayValue'].rsplit(',',1)[1]).strip()] = [
                                                ques['assignedOptionValue']]
                                        else:
                                            ques_dict_disp[lis[j]][ques['questionId']][(ques['selectedOptionDisplayValue'].rsplit(',',1)[0]).strip()][
                                                (ques['selectedOptionDisplayValue'].rsplit(',',1)[1]).strip()].append(
                                                ques['assignedOptionValue'])
                                    else:
                                        if (ques['selectedOptionDisplayValue'].rsplit(',',1)[1]).strip() not in \
                                                ques_dict_disp[lis[j]][ques['questionId']][(ques['selectedOptionDisplayValue'].rsplit(',',1)[0]).strip()]:
                                            ques_dict_disp[lis[j]][ques['questionId']][(ques['selectedOptionDisplayValue'].rsplit(',',1)[0]).strip()][
                                                (ques['selectedOptionDisplayValue'].rsplit(',',1)[1]).strip()] = [
                                                ques['assignedOptionValue']]
                                        else:
                                            ques_dict_disp[lis[j]][ques['questionId']][(ques['selectedOptionDisplayValue'].rsplit(',',1)[0]).strip()][
                                                (ques['selectedOptionDisplayValue'].rsplit(',',1)[1]).strip()].append(
                                                ques['assignedOptionValue'])
                    
                
                    
                
                print(ques_dict_disp.keys())
                                    
                #ques_dict_disp 
                import numpy as np

                # number of responses for each question wrt compare options 
                ques_num_resp = {}
                for i in lis:
                    ques_num_resp[i] = {} 
                    for qid in ques_dict_disp[i]:
                        length = []
                        for opt in ques_dict_disp[i][qid]:
                            for p in ques_dict_disp[i][qid][opt]:
                                length.append(p)
                        ques_num_resp[i][qid] = len(length)
                        
                        
                
                print(ques_num_resp)
                merged_ques_resp = {}
                
                for qid in merged_ques_name:
                    sum = 0
                    for j in range(len(lis)):
                        if qid in ques_num_resp[lis[j]]:
                            sum = sum + ques_num_resp[lis[j]][qid] 
                            merged_ques_resp[qid] = sum
                
                print(merged_ques_resp)
                
                
                
                
                gleng = {}
                grid_positions = {}
                for opt in ques_dict_disp:
                    grid_positions[opt] = {}
                    for qid in ques_dict_disp[opt]:
                        if questype[opt][qid]=='grid':
                            grid_positions[opt][qid] = []
                            for aid in ques_dict_disp[opt][qid]:
                                for position in ques_dict_disp[opt][qid][aid]:
                                    grid_positions[opt][qid].append(position)
                print('grid pos')
                print(grid_positions)
                for opt in ques_dict_disp:
                    gleng[opt] = {}
                    for qid in ques_dict_disp[opt]:
                        cum_fre = 0
                        if questype[opt][qid] == 'grid':
                            gleng[opt][qid] = {}
                            tmp = set(grid_positions[opt][qid])
                            temp2 = {}
                            for i in tmp:
                                temp2[i] = []
                            for aid in ques_dict_disp[opt][qid]:
                                for gid in (ques_dict_disp[opt][qid][aid]):
                                    for pos in tmp:
                                        if pos == gid:
                                            for item in (ques_dict_disp[opt][qid][aid][gid]):
                                                temp2[pos].append(item)
                            for p in tmp:
                                gleng[opt][qid][p] = len(temp2[p])
                print("gleng")
                print(gleng)
                
                
                
                
                        
                        
                
                
                # forming dictionary having question psition number of every question present in both datasets
                question_position ={}
                for j in range(len(lis)):
                    question_position[lis[j]] ={}
                    for i in range(ans_li[j].shape[0]):
                        ques_per_person = ans_li[j]['answers'][i]
                        for ques in ques_per_person:
                            question_position[lis[j]][ques['questionId']] = ques['question'][0]['position']
                        
                print(question_position)
                
                        
                merged_ques_position = {}
                for i in lis:
                    for j in question_position[i]:
                        merged_ques_position[j] = question_position[i][j]
                #merged_ques_position
                
                def Stats_Cal(question_results, ques_dict_disp):
    
                    question_results['compareStats'] = []
                    for option in ques_dict_disp:
                        li = []
                        tmp={}
                        
                        #question_results['compareStats'][option] = {}
                        if qid in ques_dict_disp[option]:
                            tmp['opName'] = option
                            for aid in ques_dict_disp[option][qid]:
                                    for item in (ques_dict_disp[option][qid][aid]):
                                        li.append(item)
                            # calculating statistics : mean,median,mode,variance,standard deviation
                            tmp['mean'] = float("{0:.2f}".format(np.mean(li)))
                            tmp['median'] = float("{0:.2f}".format(np.median(li)))
                            tmp['mode'] = pd.DataFrame(li).mode()[0].tolist()  ## mode can take multiple values - so there is no one single value?
                            tmp['variance'] = float("{0:.2f}".format(np.var(li)))
                            tmp['standard deviation'] = float("{0:.2f}".format(np.std(li)))
                        question_results['compareStats'].append(tmp)
                        
                
                # defining Cumulative frequency stats method:
                
                
                #print(ques_dict_disp)
                ques_opt = {}
                for optn in ques_dict_disp:
                    ques_opt[optn] ={}
                    for qid in ques_dict_disp[optn]:
                        ques_opt[optn][qid] = {}
                        for aid in ques_dict_disp[optn][qid]:
                            ques_opt[optn][qid][aid] = len(ques_dict_disp[optn][qid][aid])
                print('hey')      
                print(ques_opt)      
                def Freq_Cal(question_results, ques_dict_disp):

                    for option in ques_dict_disp:
                        temp = {}
                        cum_fre = 0
                        if qid in ques_dict_disp[option]:
                            temp['opName'] = option
                            select_options = []
                            for ai in ques_dict_disp[option][qid]:
                                select_options.append(ai)
                            li = question_with_options[qid]
                            rest_options = set(li) - set(select_options)
                            dict1 = ques_opt[option][qid]
                            srt = sorted(dict1, key=dict1.get)
                            temp['options'] = []
                            for aid in reversed(srt):
                                freq_stats = {}
                                freq_stats['name'] = aid
                                freq_stats['freq'] = len(ques_dict_disp[option][qid][aid])
                                freq_stats['percent'] = round(len(ques_dict_disp[option][qid][aid]) / (ques_num_resp[option][qid] * 1.0) * 100,2)
                                cum_fre = (len(ques_dict_disp[option][qid][aid])) + cum_fre
                                freq_stats['cum_freq'] = cum_fre
                                freq_stats['cum_percent'] = round((cum_fre / (ques_num_resp[option][qid] * 1.0) * 100),2)
                                temp['options'].append(freq_stats)
                                
                            for bid in rest_options:
                                freq_stats = {}
                                freq_stats['name'] = bid
                                freq_stats['freq'] = 0
                                freq_stats['percent'] = 0
                                freq_stats['cum_freq'] = cum_fre
                                freq_stats['cum_percent'] = 100.0
                                temp['options'].append(freq_stats)
                        question_results['compareOption'].append(temp)
                
                
                # defining Rank order stats method:
                def Rank_Stats(question_results, ques_dict_disp):
                    for option in ques_dict_disp:
                        temp={}
                        if qid in ques_dict_disp[option]:
                            temp['opName']=option
                            temp['options']=[]
                            for aid in ques_dict_disp[option][qid]:
                                rank_stats = {}
                                rank_stats['name'] = aid
                                rank_stats['ranks'] = {}
                                li = ques_dict_disp[option][qid][aid]
                                rank_count_dist = {x: li.count(x) for x in li}
                                rank_stats['ranks'] = rank_count_dist
                                temp['options'].append(rank_stats)
                        question_results['compareOption'].append(temp)
                        
                        
                for qid in merged_ques_name:
                    print('merged')
                    #print(merged_ques_name)
                    #print(res)
                    question_results = {}
                    question_results['qid'] = qid 
                    question_results['qstring'] =merged_ques_name[qid]
                    question_results['qType'] = merged_ques_type[qid]
                    question_results['qOrder'] = merged_ques_position[qid]
                    question_results['noOfResponses'] = merged_ques_resp[qid] # need to change here 
                    question_results['compareOption'] = []
                    #print(question_results)
                    
                    ######################################################
                    # multiple choice type questions
                    ######################################################
                    if (merged_ques_type[qid] == 'multiple'):
                        Stats_Cal(question_results, ques_dict_disp)
                        Freq_Cal(question_results, ques_dict_disp)
                        res['AnalysisList'].append(question_results)
                    
                    ######################################################
                    # numeric and SlidingScale type questions
                    ######################################################
                
                    if (merged_ques_type[qid] == 'numeric' or merged_ques_type[qid] == 'SlidingScale'):
                        Stats_Cal(question_results, ques_dict_disp)
                        res['AnalysisList'].append(question_results)
                        
                        
                    ######################################################
                    # rank type questions
                    ######################################################
                    if (merged_ques_type[qid] == 'rank'):
                        Rank_Stats(question_results, ques_dict_disp)
                        question_results['statistics'] = 'null'
                        res['AnalysisList'].append(question_results)
                        
                    ######################################################
                    # TextEntry type questions
                    ######################################################
                
                    if (merged_ques_type[qid] == 'simple'):
                        for option in ques_dict_disp:
                            temp={}
                            if qid in ques_dict_disp[option]:
                                temp['opName'] = option
                                temp['options'] = []
                                for key in ques_dict_disp[option][qid]:
                                    for text in ques_dict_disp[option][qid][key]:
                                        tmp = {}
                                        tmp['value'] = text
                                        temp['options'].append(tmp)
                            question_results['compareOption'].append(temp)
                                        
                        res['AnalysisList'].append(question_results)
                    
                
                    ######################################################
                    # Grid type questions
                    ######################################################
                    if (merged_ques_type[qid] == 'grid'):
                        
                        
                        # Stats_Cal(question_results,ques_dict_disp)
                        
                        question_results['compareStatments'] = {}
                        question_results['compareOption'] = {}
                        for option in ques_dict_disp:
                            question_results['compareOption'][option] = []
                            question_results['compareStatments'][option] = []
                            temp = {}
                            temp2 = {}
                            if qid in ques_dict_disp[option]:
                                temp['opName'] = option
                                temp['statements']=[]
                                temp2['opName'] = option
                                temp2['options'] = []
                                for rowid in ques_dict_disp[option][qid]:
                                    li = []
                                    temp_grid_stats = {}
                                    for gid in ques_dict_disp[option][qid][rowid]:
                                        for item in (ques_dict_disp[option][qid][rowid][gid]):
                                            li.append(item)
                                    temp_grid_stats['statement'] = rowid
                                    temp_grid_stats['order'] = 1
                                    temp_grid_stats['mean'] = round(np.mean(li),2)
                                    temp_grid_stats['median'] = round(np.median(li),2)
                                    temp_grid_stats['mode'] = pd.DataFrame(li).mode()[0].tolist() ## mode can take multiple values - so there is no one single value?
                                    temp_grid_stats['variance'] = round(np.var(li),2)
                                    temp_grid_stats['standard deviation'] = round(np.std(li),2)
                                    temp['statements'].append(temp_grid_stats)
                                
                                total = 0
                                for i in gleng[option][qid]:
                                    total = gleng[option][qid][i] + total
                                
                                cum_fre = 0
                                print('hiiiiiiiiiii')
                                
                                li = []
                                cou = 0
                                for j in question_with_options_grid[qid]:
                                    if(cou == 0):
                                        li = question_with_options_grid[qid][j]
                                        cou = cou + 1
                                
                                select_options=[]
                            
                                for i in ques_dict_disp[option][qid]:
                                    i = i.strip()
                                    select_options.append(i)
                                print(li)
                                select_options = list(gleng[option][qid].keys())
                                print(select_options)
                                print(gleng[option][qid])
                                dict1 = gleng[option][qid]
                                srt = sorted(dict1, key=dict1.get)
                                
                                rest_options = set(li) - set(select_options)
                                print(rest_options)
                                
                                for i in reversed(srt):
                                    #print(total)
                                    #print(i)
                                    freq_stats = {}
                                    freq_stats['name'] = i
                                    freq_stats['freq'] = gleng[option][qid][i]
                                    freq_stats['percent'] = round((gleng[option][qid][i] / (total * 1.0)*100),2)
                                    cum_fre = cum_fre + gleng[option][qid][i]
                                    freq_stats['cum_freq'] = cum_fre
                                    freq_stats['cum_percent'] = round((cum_fre / (total * 1.0)*100),2)
                                    temp2['options'].append(freq_stats)
                                    #print('in grid..')
                                for i in rest_options:
                                    freq_stats = {}
                                    freq_stats['name'] = i
                                    freq_stats['freq'] = 0
                                    freq_stats['percent'] = 0
                                    freq_stats['cum_freq'] = cum_fre
                                    freq_stats['cum_percent'] = 100.0
                                    temp2['options'].append(freq_stats)
                            #print(temp)
                            #print(temp2)
                            question_results['compareOption'][option].append(temp2)
                            question_results['compareStatments'][option].append(temp)
                            #print('question_results')
                            #print(question_results)
                
                        res['AnalysisList'].append(question_results)
                #print(res)
                print('ques')
                #print(ques_dict_disp)
                return res
        except Exception as err:
            Object.logger.logActivity("INFO", "error in processing data : " + str(err), __name__)
            
    def groupAnalysis(self, typeOfAnalysis, dataSet, from_date, to_date, grouplist, get_data, Object):
        try:
            Object.logger.logActivity("INFO", "dataSet : " + str(dataSet), __name__)
            print('hey you ...whats up')

            grid_ques = []
            for i in grouplist:
                grid_ques.append(i['questionId'])
            
            sub_ques = []
            for i in grouplist:
                sub_ques.append(i['RowLabel'])
            
            resp = get_data
                    
            resp1 = resp['pages'][0]
            resp2 = resp1['questions']
            j=1
            
            
            # for grid questions         
            question_with_options_grid = {}
            for ques in resp2:
                if ques['type'] == 'grid':
                    tmp = []
                    for each_option in ques['answerConfig']['options']:
                        tmp.append(each_option['title'])
                    question_with_options_grid[ques['_id']] = {}
                    for each_row in ques['answerConfig']['rows']:
                        question_with_options_grid[ques['_id']][each_row['title']] = tmp
                        
             
            #desired grid questions with their options
            grid_ques_options_list = []
            grid_ques_options_len = []        
            
            for qid in grid_ques:
                count = 0  
                for rowid in question_with_options_grid[qid]:
                    if count == 0:
                        grid_ques_options_list.append(question_with_options_grid[qid][rowid])
                        grid_ques_options_len.append(len(question_with_options_grid[qid][rowid]))
                        count = count + 1
            print("desired question_with_options_grid :")   
            print(question_with_options_grid)       
            print(grid_ques_options_len)
            print('list :')
            print(grid_ques_options_list)            
            # checking if options of different grid ques sent are the same
            bol = True
            if(len(set(grid_ques_options_len)) == 1 ):
                counter1 = 0
                for item1 in range(len(grid_ques_options_list)):
                    if(counter1 == 0):
                        temp1 = grid_ques_options_list[item1]
                        for item2 in range(len(grid_ques_options_list)):
                            if(counter1 == 0):
                                temp2 = grid_ques_options_list[item2]
                                if(set(temp1) != set(temp2)):
                                    bol = False
                                    counter1 = counter1+1
                                    
                                
                            
                        
                    
            if(bol):
                counter2 = 0
                for qid in question_with_options_grid:
                    for rowid in question_with_options_grid[qid]:
                        if(counter2 == 0):
                            options = question_with_options_grid[qid][rowid]
                            counter2 = counter2 + 1
                print(question_with_options_grid)
                print(grouplist)
                
                samp=pd.DataFrame(dataSet)
                #samp = pd.read_json('F:/projectSurveyAnalysis/QAbackedninput.json')
                
                one = pd.DataFrame(samp['answers'])
                ques_dict_disp = {}
                
                res = {}
                # assigning project ID - need to update this as per real time response file
                
                res['projectID'] = samp['projectId'][0]
                # do not have consistency in todatetime and fromdatetime
                res['fromdatetime'] = from_date
                res['todatetime'] = to_date
                
                # do not have 'type of analysis' input from json
                res['TypeofAnalysis'] = 'GroupAnalysis'
                
                res['AnalysisList'] = []
                group_results = {}
                
                # code which fetches question and its type . we need this for performing type wise analysis.
                
                
                questype = {}
                for i in range(one.shape[0]):
                    ques_per_person = one['answers'][i]
                    for ques in ques_per_person:
                        questype[ques['questionId']] = ques['question'][0]['type']
                # ques_name is a dict which stores names of each question :
                
                ques_name = {}
                for i in range(one.shape[0]):
                    ques_per_person = one['answers'][i]
                    for ques in ques_per_person:
                        ques_name[ques['questionId']] = ques['question'][0]['title']
                
                
                
                
                for i in range(one.shape[0]):
                    ques_per_person = one['answers'][i]
                    for ques in ques_per_person:  
                        if questype[ques['questionId']] == 'grid' :
                            if ques['questionId'] not in ques_dict_disp:
                                ques_dict_disp[ques['questionId']] = {}
                                if (ques['selectedOptionDisplayValue'].rsplit(',',1)[0]).strip() not in ques_dict_disp[ques['questionId']]:
                                    ques_dict_disp[ques['questionId']][(ques['selectedOptionDisplayValue'].rsplit(',',1)[0]).strip()] = {}
                                    if (ques['selectedOptionDisplayValue'].rsplit(',',1)[1]).strip() not in \
                                            ques_dict_disp[ques['questionId']][(ques['selectedOptionDisplayValue'].rsplit(',',1)[0]).strip()]:
                                        ques_dict_disp[ques['questionId']][(ques['selectedOptionDisplayValue'].rsplit(',',1)[0]).strip()][
                                            (ques['selectedOptionDisplayValue'].rsplit(',',1)[1]).strip()] = [
                                            ques['assignedOptionValue']]
                                    else:
                                        ques_dict_disp[ques['questionId']][(ques['selectedOptionDisplayValue'].rsplit(',',1)[0]).strip()][
                                            (ques['selectedOptionDisplayValue'].rsplit(',',1)[1]).strip()].append(
                                            ques['assignedOptionValue'])
                                else:
                                    if (ques['selectedOptionDisplayValue'].rsplit(',',1)[1]).strip() not in \
                                            ques_dict_disp[ques['questionId']][(ques['selectedOptionDisplayValue'].rsplit(',',1)[0]).strip()]:
                                        ques_dict_disp[ques['questionId']][(ques['selectedOptionDisplayValue'].rsplit(',',1)[0]).strip()][
                                            (ques['selectedOptionDisplayValue'].rsplit(',',1)[1]).strip()] = [
                                            ques['assignedOptionValue']]
                                    else:
                                        ques_dict_disp[ques['questionId']][(ques['selectedOptionDisplayValue'].rsplit(',',1)[0]).strip()][
                                            (ques['selectedOptionDisplayValue'].rsplit(',',1)[1]).strip()].append(
                                            ques['assignedOptionValue'])
                            else:
                
                                if (ques['selectedOptionDisplayValue'].rsplit(',',1)[0]).strip() not in ques_dict_disp[ques['questionId']]:
                                    ques_dict_disp[ques['questionId']][(ques['selectedOptionDisplayValue'].rsplit(',',1)[0]).strip()] = {}
                                    if (ques['selectedOptionDisplayValue'].rsplit(',',1)[1]).strip() not in \
                                            ques_dict_disp[ques['questionId']][(ques['selectedOptionDisplayValue'].rsplit(',',1)[0]).strip()]:
                                        ques_dict_disp[ques['questionId']][(ques['selectedOptionDisplayValue'].rsplit(',',1)[0]).strip()][
                                            (ques['selectedOptionDisplayValue'].rsplit(',',1)[1]).strip()] = [
                                            ques['assignedOptionValue']]
                                    else:
                                        ques_dict_disp[ques['questionId']][(ques['selectedOptionDisplayValue'].rsplit(',',1)[0]).strip()][
                                            (ques['selectedOptionDisplayValue'].rsplit(',',1)[1]).strip()].append(
                                            ques['assignedOptionValue'])
                                else:
                                    if (ques['selectedOptionDisplayValue'].rsplit(',',1)[1]).strip() not in \
                                            ques_dict_disp[ques['questionId']][(ques['selectedOptionDisplayValue'].rsplit(',',1)[0]).strip()]:
                                        ques_dict_disp[ques['questionId']][(ques['selectedOptionDisplayValue'].rsplit(',',1)[0]).strip()][
                                            (ques['selectedOptionDisplayValue'].rsplit(',',1)[1]).strip()] = [
                                            ques['assignedOptionValue']]
                                    else:
                                        ques_dict_disp[ques['questionId']][(ques['selectedOptionDisplayValue'].rsplit(',',1)[0]).strip()][
                                            (ques['selectedOptionDisplayValue'].rsplit(',',1)[1]).strip()].append(
                                            ques['assignedOptionValue'])
                print('here')
                
                print(ques_dict_disp)
                
                
                
                # 585c114d3952d75ffff6156g , 585c114d3952d75ffff6156e
                # Trump is bad
                # Obama is good
                #grid_ques = ['585c114d3952d75ffff6156g' , '585c114d3952d75ffff6156e']
                #sub_ques = ['Trump is bad' , 'Obama is good']
                
                #consolidated statistics
                group_results["ConsolidatedStatistics"] = {}
                consolidated_list = []
                
                
                for i in ques_dict_disp:
                    if i in grid_ques :
                        for j in ques_dict_disp[i]:
                            if j in sub_ques :
                                for option in ques_dict_disp[i][j]:
                                    for element in ques_dict_disp[i][j][option]:
                                        consolidated_list.append(element)
                                    
                temp = {}
                temp['noofResponses'] = len(consolidated_list)
                temp['mean'] = float("{0:.2f}".format(np.mean(consolidated_list)))
                temp['median'] = float("{0:.2f}".format(np.median(consolidated_list)))
                temp['mode'] = pd.DataFrame(consolidated_list).mode()[0].tolist()  ## mode can take multiple values - so there is no one single value?
                temp['variance'] = float("{0:.2f}".format(np.var(consolidated_list)))
                temp['standard deviation'] = float("{0:.2f}".format(np.std(consolidated_list)))
                
                group_results["ConsolidatedStatistics"]  = temp
                
                
                #Prompt Statistics
                
                group_results["PromptStatistics"] = []
                
                for i in ques_dict_disp:
                    if i in grid_ques :
                        for j in ques_dict_disp[i]:
                            if j in sub_ques :
                                prompt_list = []
                                prompt_dict = {}
                                for option in ques_dict_disp[i][j]:
                                    for element in ques_dict_disp[i][j][option]:
                                        prompt_list.append(element)
                                prompt_dict['name'] = j
                                prompt_dict['noofResponses'] = len(prompt_list)
                                prompt_dict['mean'] = float("{0:.2f}".format(np.mean(prompt_list)))
                                prompt_dict['median'] = float("{0:.2f}".format(np.median(prompt_list)))
                                prompt_dict['mode'] = pd.DataFrame(prompt_list).mode()[0].tolist()  ## mode can take multiple values - so there is no one single value?
                                prompt_dict['variance'] = float("{0:.2f}".format(np.var(prompt_list)))
                                prompt_dict['standard deviation'] = float("{0:.2f}".format(np.std(prompt_list)))
                                group_results["PromptStatistics"].append(prompt_dict)
                                
                
                # Group Statistics
                
                #options = ['agree','disagree','neutral']
                group_results['GroupStatistics'] = []
                option_wise_list = {}
                for i in ques_dict_disp:
                    if i in grid_ques :
                        for j in ques_dict_disp[i]:
                            if j in sub_ques :
                                 for option in ques_dict_disp[i][j]:
                                        if option not in option_wise_list:
                                            option_wise_list[option] = []
                                            for element in ques_dict_disp[i][j][option]:
                                                option_wise_list[option].append(element)
                                        else:
                                            for element in ques_dict_disp[i][j][option]:
                                                option_wise_list[option].append(element)
                                            
                                        
                                
                                
                
                print('namste')
                print(option_wise_list)
                ques_opt = {}
                for opt in option_wise_list:
                    ques_opt[opt] = len(option_wise_list[opt])  
                
                
                dict1 = ques_opt
                srt = sorted(dict1, key=dict1.get)
                
                select_options = list(option_wise_list.keys())
                rest_options = set(options) - set(select_options)
                total = len(consolidated_list)
                cum = 0
                for opt in reversed(srt):
                    option_wise_stats = {}
                    option_wise_stats['name'] = opt
                    leng = len(option_wise_list[opt])
                    option_wise_stats['frequency'] = leng             
                    option_wise_stats['percent'] = float("{0:.2f}".format((leng/(total*1.0))*100))
                    cum = cum + leng
                    option_wise_stats['cumulativeFrequency'] = cum
                    option_wise_stats['cumulativePercent'] = float("{0:.2f}".format((cum/(total*1.0))*100))
                    group_results['GroupStatistics'].append(option_wise_stats)
                    
                for opt in rest_options:
                    option_wise_stats = {}
                    option_wise_stats['name'] = opt
                    option_wise_stats['frequency'] = 0             
                    option_wise_stats['percent'] = 0
                    
                    option_wise_stats['cumulativeFrequency'] = cum
                    option_wise_stats['cumulativePercent'] = float("{0:.2f}".format((cum/(total*1.0))*100))
                    group_results['GroupStatistics'].append(option_wise_stats)
                
                
                print(option_wise_list)
                group_results
                res['AnalysisList'].append(group_results)
                return res
            else:
                failure = {}
                failure['status'] = 'Failed'
                failure['message'] = 'Please enter grid questions with same options'
                
                return failure

        except Exception as err:
            Object.logger.logActivity("INFO", "error in processing data : " + str(err), __name__)
                        
                        
    def TrendAnalysis(self, typeOfAnalysis, dataSet, from_date, to_date ,trend_type, get_data,Object):
        try:
            import datetime
            # reading sample json :
            samp1 = pd.DataFrame(dataSet)
            
            
            #from_date = "2017-02-14 07:00"
            mon = int(from_date[5:7])
            updated_mon = from_date[0:7]
            day = int(from_date[8:10])
            year = int(from_date[0:4])
            #trend_type = 'daily'
            
            data1 = pd.to_datetime(samp1['updatedAt'])
            hourlist = []
            daylist = []
            yearlist = []
            monthlist = []
            #print(data1)
            for i in data1:
                print(i)
                print(type(i))
                j = str(i)
                j = j[0:19]
                print(i)
                x = (datetime.datetime.strptime(j, "%Y-%m-%d  %H:%M:%S"))
                hourlist.append(x.hour)
                daylist.append(x.day)
                monthlist.append(x.month)
                yearlist.append(x.year)
                print(hourlist ,daylist, monthlist,yearlist)
            samp1['hour'] = hourlist
            samp1['day'] = daylist
            samp1['month'] = monthlist
            samp1['year'] = yearlist
            
            samp1['updated_month'] = samp1.year.map(str) + "-" + samp1.month.map(str)
            samp1['updated_date'] = samp1.updated_month + "-" + samp1.day.map(str)
            samp1['updated_time'] = samp1.hour.map(str) + ":00" + " to " + samp1.hour.map(str) + ":59" 
            
            if trend_type == 'yearly':
                trend_version = 'year'
            if trend_type == 'monthly':
                trend_version = 'updated_month'
            if trend_type == 'daily':
                trend_version = 'updated_date'
            if trend_type == 'hourly':
                trend_version = 'updated_time'
            #resp = pd.DataFrame('F:/projectSurveyAnalysis/QAgetreq.json')
            import json
            import numpy as np
            #with open('F:/projectSurveyAnalysis/QAgetreq.json') as data_file:    
                #resp = json.load(data_file)
            resp = get_data
            resp1 = resp['pages'][0]
            print(resp.keys())
            resp2 = resp1['questions']
            j=1
            #forming list of all questions in a project
            
            questions_list = []
            for ques in resp2:
                if(ques['type'] != 'decorator'):
                    questions_list.append(ques['_id'])
                    
                    
            questions_title_get_ret = {}
            for ques in resp2:
                if(ques['type'] != 'decorator'):
                    questions_title_get_ret[ques['_id']] = ques['title']
                    
            questions_position_get_ret = {}
            for ques in resp2:
                if(ques['type'] != 'decorator'):
                    questions_position_get_ret[ques['_id']] = ques['position']
                    
            question_with_options = {}
            for ques in resp2:
                if ques['type'] == 'multiple':
                    print('in here,,')
                    question_with_options[ques['_id']] = []
                    ans = (ques['answerConfig'].keys())
                    for each_option in ques['answerConfig']['options']:
                        #print(ques['answerConfig'][opt][0])
                        print(each_option['title'])
                        question_with_options[ques['_id']].append(each_option['title'])
            print(question_with_options)
                # for grid questions                
            question_with_options_grid = {}
            for ques in resp2:
                if ques['type'] == 'grid':
                    tmp = []
                    for each_option in ques['answerConfig']['options']:
                        tmp.append((each_option['title']).strip())
                    question_with_options_grid[ques['_id']] = {}
                    for each_row in ques['answerConfig']['rows']:
                        question_with_options_grid[ques['_id']][(each_row['title']).strip()] = tmp

            
            print('grid positins')
            print(question_with_options_grid)
            
            print('in request anaysis')
            # reading sample json :
            final_list = []
            trend_list = samp1[trend_version].unique()
            print(trend_list)
            for trend in trend_list:
                print('trendddd is hereee')
                print(trend)
                samp = samp1[samp1[trend_version] == trend]
                samp['new_col'] = range(0, len(samp))
                samp.set_index(samp['new_col'],inplace = True)
                #print(samp)
                #samp = pd.read_json('F:/projectSurveyAnalysis/QAoutput.json')
                #samp=pd.DataFrame(dataSet)
                print('in requirst analysis')
                print(trend_list)
                one = pd.DataFrame(samp['answers'])
                
                # ques_dict_disp maintains display value of option that user selected (for eg, if user selects red option for q1, it stores red )
                ques_dict_disp = {}
            
                res = {}
                # assigning project ID - need to update this as per real time response file
                res['projectID'] = samp['projectId'][0]
                # do not have consistency in todatetime and fromdatetime
                res['fromdatetime'] = from_date
                res['todatetime'] = to_date
            
                # do not have 'type of analysis' input from json
                res['TypeofAnalysis'] = 'TrendAnalysis'
            
                res['AnalysisList'] = []
            
                # code which fetches question and its type . we need this for performing type wise analysis.
            
            
                questype = {}
                #print(one.shape[0])
                for i in range(one.shape[0]):
                    ques_per_person = one['answers'][i]
                    for ques in ques_per_person:
                        questype[ques['questionId']] = ques['question'][0]['type']
                # ques_name is a dict which stores names of each question :
                ques_name = {}
                for i in range(one.shape[0]):
                    ques_per_person = one['answers'][i]
                    for ques in ques_per_person:
                        ques_name[ques['questionId']] = ques['question'][0]['title']

                for i in range(one.shape[0]):
                    ques_per_person = one['answers'][i]
                    for ques in ques_per_person:
                        if questype[ques['questionId']] != 'grid' and questype[ques['questionId']] != 'simple':
                            #print(questype[ques['questionId']])
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
                        elif questype[ques['questionId']] == 'simple':
                            if ques['questionId'] not in ques_dict_disp:
                                ques_dict_disp[ques['questionId']] = {}
                                if ques['assignedOptionValue'] not in ques_dict_disp[ques['questionId']]:
                                    ques_dict_disp[ques['questionId']][ques['assignedOptionValue']] = [
                                        ques['selectedOptionActualValue']]
                                else:
                                    ques_dict_disp[ques['questionId']][ques['assignedOptionValue']].append(
                                        ques['selectedOptionActualValue'])
                            else:
                                if ques['assignedOptionValue'] not in ques_dict_disp[ques['questionId']]:
                                    ques_dict_disp[ques['questionId']][ques['assignedOptionValue']] = [
                                        ques['selectedOptionActualValue']]
                                else:
                                    ques_dict_disp[ques['questionId']][ques['assignedOptionValue']].append(
                                        ques['selectedOptionActualValue'])
                        else:
                            if ques['questionId'] not in ques_dict_disp:
                                ques_dict_disp[ques['questionId']] = {}
                                if (ques['selectedOptionDisplayValue'].rsplit(',',1)[0]).strip() not in ques_dict_disp[ques['questionId']]:
                                    ques_dict_disp[ques['questionId']][(ques['selectedOptionDisplayValue'].rsplit(',',1)[0]).strip()] = {}
                                    if (ques['selectedOptionDisplayValue'].rsplit(',',1)[1]).strip() not in \
                                            ques_dict_disp[ques['questionId']][(ques['selectedOptionDisplayValue'].rsplit(',',1)[0]).strip()]:
                                        ques_dict_disp[ques['questionId']][(ques['selectedOptionDisplayValue'].rsplit(',',1)[0]).strip()][
                                            (ques['selectedOptionDisplayValue'].rsplit(',',1)[1]).strip()] = [
                                            ques['assignedOptionValue']]
                                    else:
                                        ques_dict_disp[ques['questionId']][(ques['selectedOptionDisplayValue'].rsplit(',',1)[0]).strip()][
                                            (ques['selectedOptionDisplayValue'].rsplit(',',1)[1]).strip()].append(
                                            ques['assignedOptionValue'])
                                else:
                                    if (ques['selectedOptionDisplayValue'].rsplit(',',1)[1]).strip() not in \
                                            ques_dict_disp[ques['questionId']][(ques['selectedOptionDisplayValue'].rsplit(',',1)[0]).strip()]:
                                        ques_dict_disp[ques['questionId']][(ques['selectedOptionDisplayValue'].rsplit(',',1)[0]).strip()][
                                            (ques['selectedOptionDisplayValue'].rsplit(',',1)[1]).strip()] = [
                                            ques['assignedOptionValue']]
                                    else:
                                        ques_dict_disp[ques['questionId']][(ques['selectedOptionDisplayValue'].rsplit(',',1)[0]).strip()][
                                            (ques['selectedOptionDisplayValue'].rsplit(',',1)[1]).strip()].append(
                                            ques['assignedOptionValue'])
                            else:

                                if (ques['selectedOptionDisplayValue'].rsplit(',',1)[0]).strip() not in ques_dict_disp[ques['questionId']]:
                                    ques_dict_disp[ques['questionId']][(ques['selectedOptionDisplayValue'].rsplit(',',1)[0]).strip()] = {}
                                    if (ques['selectedOptionDisplayValue'].rsplit(',',1)[1]).strip() not in \
                                            ques_dict_disp[ques['questionId']][(ques['selectedOptionDisplayValue'].rsplit(',',1)[0]).strip()]:
                                        ques_dict_disp[ques['questionId']][(ques['selectedOptionDisplayValue'].rsplit(',',1)[0]).strip()][
                                            (ques['selectedOptionDisplayValue'].rsplit(',',1)[1]).strip()] = [
                                            ques['assignedOptionValue']]
                                    else:
                                        ques_dict_disp[ques['questionId']][(ques['selectedOptionDisplayValue'].rsplit(',',1)[0]).strip()][
                                            (ques['selectedOptionDisplayValue'].rsplit(',',1)[1]).strip()].append(
                                            ques['assignedOptionValue'])
                                else:
                                    if (ques['selectedOptionDisplayValue'].rsplit(',',1)[1]).strip() not in \
                                            ques_dict_disp[ques['questionId']][(ques['selectedOptionDisplayValue'].rsplit(',',1)[0]).strip()]:
                                        ques_dict_disp[ques['questionId']][(ques['selectedOptionDisplayValue'].rsplit(',',1)[0]).strip()][
                                            (ques['selectedOptionDisplayValue'].rsplit(',',1)[1]).strip()] = [
                                            ques['assignedOptionValue']]
                                    else:
                                        ques_dict_disp[ques['questionId']][(ques['selectedOptionDisplayValue'].rsplit(',',1)[0]).strip()][
                                            (ques['selectedOptionDisplayValue'].rsplit(',',1)[1]).strip()].append(
                                            ques['assignedOptionValue'])
                print('here')
            
                print(ques_dict_disp)
                ques_num_resp = {}
                for qid in ques_dict_disp:
                    length = []
                    for opt in ques_dict_disp[qid]:
                        for p in ques_dict_disp[qid][opt]:
                            length.append(p)
                    ques_num_resp[qid] = len(length)
                #print(ques_num_resp)
            
            
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
                # code to calculate total entries for grid
                gleng = {}
                grid_positions = {}
            
                for qid in ques_dict_disp:
                    if questype[qid]=='grid':
                        grid_positions[qid] = []
                        for aid in ques_dict_disp[qid]:
                            for position in ques_dict_disp[qid][aid]:
                                grid_positions[qid].append(position)
                #print('grid pos')
            
                for qid in ques_dict_disp:
                    cum_fre = 0
                    if questype[qid] == 'grid':
                        gleng[qid] = {}
                        tmp = set(grid_positions[qid])
                        temp2 = {}
                        for i in tmp:
                            temp2[i] = []
                        for aid in ques_dict_disp[qid]:
                            for gid in (ques_dict_disp[qid][aid]):
                                for pos in tmp:
                                    if pos == gid:
                                        for item in (ques_dict_disp[qid][aid][gid]):
                                            temp2[pos].append(item)
                        for p in tmp:
                            gleng[qid][p] = len(temp2[p])
                #print("gleng")
                #print(ques_dict_disp)
                # defining statistics method:
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
                
                ques_opt = {}
                for qid in ques_dict_disp:
                    ques_opt[qid] = {}
                    for aid in ques_dict_disp[qid]:
                        ques_opt[qid][aid] = len(ques_dict_disp[qid][aid])
                        
                def Freq_Cal(question_results, ques_dict_disp):
                    cum_fre = 0
                    select_options = []
                    for aid in ques_dict_disp[qid]:
                        select_options.append(aid)
                    li = question_with_options[qid]
                    rest_options = set(li) - set(select_options)
                    dict1 = ques_opt[qid]
                    srt = sorted(dict1, key=dict1.get)
                    for aid in reversed(srt):
                        freq_stats = {}
                        freq_stats['name'] = aid
                        freq_stats['freq'] = len(ques_dict_disp[qid][aid])
                        freq_stats['percent'] = round(len(ques_dict_disp[qid][aid]) / (leng[qid] * 1.0) * 100,2)
                        cum_fre = (len(ques_dict_disp[qid][aid])) + cum_fre
                        freq_stats['cum_freq'] = cum_fre
                        freq_stats['cum_percent'] = round((cum_fre / (leng[qid] * 1.0) * 100),2)
                        question_results['options'].append(freq_stats)
                    for bid in rest_options:
                        freq_stats = {}
                        freq_stats['name'] = bid
                        freq_stats['freq'] = 0
                        freq_stats['percent'] = 0
                        freq_stats['cum_freq'] = cum_fre
                        freq_stats['cum_percent'] = 100.0
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
                # constructing question_position dictionary which is used for giving q_order :
                #creating question position dict:
                question_position ={}
                for i in range(one.shape[0]):
                    ques_per_person = one['answers'][i]
                    for ques in ques_per_person:
                        question_position[ques['questionId']] = ques['question'][0]['position']
                #q_order = 0
            
                #creating dict to find no of responses for each sub question in grid type:
                ques_len = {}
            
                for ques in ques_dict_disp:
                    if questype[ques] == 'grid':
                        ques_len[ques] = {}
                        for option in ques_dict_disp[ques]:
                            total = 0
                            for p in ques_dict_disp[ques][option]:
                                total = total + len(ques_dict_disp[ques][option][p])
                            ques_len[ques][option] = total
                #print('ques_ken')
                #print(ques_len)
            
                #now finding freq stats for each sub question in grid type for every option they have:
                grid_temp = {}
                for ques in ques_dict_disp:
                    if questype[ques] == 'grid':
                        print('in grid temp..')
                        grid_temp[ques] = {}
                        for option in ques_dict_disp[ques]:
                            grid_temp[ques][option] = []
                            cum = 0
                            ordr = 1
                            select_options=[]
                            print(option)
                            for i in ques_dict_disp[ques][option]:
                                i = i.lstrip()
                                select_options.append(i)
                                
                            ques_opt1 = {}
                            for rid in ques_dict_disp[ques]:
                                ques_opt1[rid] = {}
                                for aid in ques_dict_disp[ques][rid]:
                                    ques_opt1[rid][aid] = len(ques_dict_disp[ques][rid][aid])
                            print(ques_opt1)
                            print(ques)
                            dict1 = ques_opt1[option]
                            srt = sorted(dict1, key=dict1.get) 
                            
                            
                            print(select_options)
                            print('select')
                            li  = question_with_options_grid[ques][option]
                            rest_options = set(li) - set(select_options)
                            print('li')
                            print(li)
                            print(select_options)
                            print(rest_options)
                            for i in reversed(srt):
                                tmp = {}
                                tmp['name'] = i
                                le = len(ques_dict_disp[ques][option][i])
                                tmp['frequency'] = le
                                tmp['percent'] = float("{0:.2f}".format((le/(ques_len[ques][option]*1.0))*100))
                                cum = cum + le
                                tmp['cum_freq'] = cum
                                tmp['cum_percent'] = float("{0:.2f}".format((cum/(ques_len[ques][option]*1.0))*100))
                                tmp['order'] = ordr
                                ordr = ordr + 1
                                grid_temp[ques][option].append(tmp)
                            #assigning stats for non selected options in particular row
                            for i in rest_options:
                                tmp = {}
                                tmp['name'] = i
                                tmp['frequency'] = 0
                                tmp['percent'] = 0
                                tmp['cum_freq'] = cum
                                tmp['cum_percent'] = 100.0
                                tmp['order'] = ordr
                                ordr = ordr + 1
                                grid_temp[ques][option].append(tmp)
            
                #print('grid_temmp')
                #print(grid_temp)
                for qid in ques_dict_disp:
                    #q_order = q_order + 1
                    question_results = {}
                    question_results['qid'] = qid 
                    question_results['qstring'] =ques_name[qid]
                    question_results['qType'] = questype[qid]
                    question_results['qOrder'] = question_position[qid]
                    question_results['noOfAnswers'] = ques_num_resp[qid] # need to change here 
                    question_results['options'] = []
            
                    ######################################################
                    # multiple choice type questions
                    ######################################################
                    if (questype[qid] == 'multiple'):
                        print(' in multiple...')
                        Stats_Cal(question_results, ques_dict_disp)
                        Freq_Cal(question_results, ques_dict_disp)
                        question_results['OtherEntries'] = []
                        for i in range(one.shape[0]):
                            ques_per_person = one['answers'][i]
                            for ques in ques_per_person:
                                if ques['selectedOptionDisplayValue'] == 'Other' and ques['questionId'] == qid:
                                    question_results['OtherEntries'].append(ques['selectedOptionActualValue'])
            
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
                        print('in numeric..')
            
                        question_results['numeric_items'] = []
                        for aid in ques_dict_disp[qid]:
                            for num in ques_dict_disp[qid][aid]:
                                question_results['numeric_items'].append(num)
            
            
                        Stats_Cal(question_results, ques_dict_disp)
                        question_results['options'] = 'null'
                        res['AnalysisList'].append(question_results)
            
                    ######################################################
                    # Simple type questions
                    ######################################################
            
                    if (questype[qid] == 'simple'):
                        #print('in simple..')
                        question_results['text_items'] = []
                        for aid in ques_dict_disp[qid]:
                            for text in ques_dict_disp[qid][aid]:
                                question_results['text_items'].append(text)
                        res['AnalysisList'].append(question_results)
            
                    ######################################################
                    # Grid type questions
                    ######################################################
                    if (questype[qid] == 'grid'):
                        print('in grid..')
                        # Stats_Cal(question_results,ques_dict_disp)
                        question_results['options'] = []
                        question_results['statements'] = []
                        consolidated_list=[]
                        for rowid in ques_dict_disp[qid]:
                            li = []
                            temp_grid_stats = {}
                            for gid in ques_dict_disp[qid][rowid]:
                                for item in (ques_dict_disp[qid][rowid][gid]):
                                    li.append(item)
                            temp_grid_stats['statement'] = rowid
                            temp_grid_stats['order'] = 1
                            temp_grid_stats['mean'] = float("{0:.2f}".format(np.mean(li)))
                            temp_grid_stats['median'] = float("{0:.2f}".format(np.median(li)))
                            temp_grid_stats['mode'] = pd.DataFrame(li).mode()[0].tolist()  ## mode can take multiple values - so there is no one single value?
                            temp_grid_stats['variance'] = float("{0:.2f}".format(np.var(li)))
                            temp_grid_stats['standard deviation'] = float("{0:.2f}".format(np.std(li)))
                            temp_grid_stats['noofResponses'] = len(li)
                            temp_grid_stats['options'] = grid_temp[qid][rowid]
            
                            for i in li :
                                consolidated_list.append(i)
                            question_results['statements'].append(temp_grid_stats)
            
            
                        total = 0
            
            
                        question_results['statistics'] = {}
                        question_results['statistics']['mean'] = float("{0:.2f}".format(np.mean(consolidated_list)))
                        question_results['statistics']['median'] = float("{0:.2f}".format(np.median(consolidated_list)))
                        question_results['statistics']['mode'] = pd.DataFrame(consolidated_list).mode()[0].tolist()  ## mode can take multiple values - so there is no one single value?
                        question_results['statistics']['variance'] = float("{0:.2f}".format(np.var(consolidated_list)))
                        question_results['statistics']['standard deviation'] = float("{0:.2f}".format(np.std(consolidated_list)))
            
                        for p in gleng[qid]:
                            total = total + gleng[qid][p]
            
                        question_results['noOfAnswers'] = total
                        cum_fre = 0
                        select_options = []
                        for j in gleng[qid]:
                            select_options.append(j)
                        li = []
                        cou = 0
                        for j in question_with_options_grid[qid]:
                            if(cou == 0):
                                li = question_with_options_grid[qid][j]
                                cou = cou + 1
                        rest_options = set(li) - set(select_options)
                        
                        print('vanakam')
                        dict1 = gleng[qid]
                        srt = sorted(dict1, key=dict1.get)
            
            
                        for i in reversed(srt):
                            freq_stats = {}
                            freq_stats['name'] = i
                            freq_stats['freq'] = gleng[qid][i]
                            freq_stats['percent'] = round((gleng[qid][i] / (total * 1.0)*100),2)
                            cum_fre = cum_fre + gleng[qid][i]
                            freq_stats['cum_freq'] = cum_fre
                            freq_stats['cum_percent'] = round((cum_fre / (total * 1.0)*100),2)
                            question_results['options'].append(freq_stats)
            
                        for i in rest_options:
                            freq_stats = {}
                            freq_stats['name'] = i
                            freq_stats['freq'] = 0
                            freq_stats['percent'] = 0
                            freq_stats['cum_freq'] = cum_fre
                            freq_stats['cum_percent'] = 100.0
                            question_results['options'].append(freq_stats)
                        print('t end hereeeeeeeeeeeeeeeeeeee')
                        print(str(trend))
                        
                        res['AnalysisList'].append(question_results)
                print('result')
                res['year'] = str(trend)
                print(res)
                final_list.append(res)
    
    
            response = {}
            
            
            response['projectID'] = samp1['projectId'][0]
            # do not have consistency in todatetime and fromdatetime
            response['fromdatetime'] = from_date
            response['todatetime'] = to_date
            response['typeOfAnalysis'] = 'Trend Analysis'
            response['AnalysisList'] = []
            #questions_list = ['58a4f0c6338dae6276b4fe19','58a4f192338dae6276b4fe7a','58a4f26a338dae6276b4fee2']   
            print('yeatly')
            print(questions_list)
            for ques in questions_list:
                trend_result = {}
                trend = []
                noOfAnswers = 0
                trend_result['qid'] = ques
                print('helloooooooooooooooooooooooooooo')
                trend_result['qstring'] = questions_title_get_ret[ques]
                trend_result['qorder'] = questions_position_get_ret[ques]
                
                for trend_resp in final_list:
                    
                    
                    trend_temp = {}
                    for ques1 in trend_resp['AnalysisList']:
                        #print(ques1)
                        #print(ques1['qType'])
                        #print('trend temp')
                        #print(trend_temp)
                        #print(ques1['qid'])
                        #print(ques)
                        
                        if ques1['qid'] == ques and ques1['qType'] == 'multiple':
                            print('welcome')
                            trend_result['qstring'] = ques1['qstring']
                            
                            trend_result['qType'] = ques1['qType']
                            
                            trend_result['qOrder'] = ques1['qOrder']
                            
                            noOfAnswers = ques1['noOfAnswers'] + noOfAnswers
                            print('welcome3')
                            trend_temp[trend_resp['year']] = {}
                            print('welcome2')
                            trend_temp[trend_resp['year']]['OtherEntries'] = ques1['OtherEntries']
                            print('welcome1')
                            trend_temp[trend_resp['year']]['options'] = ques1['options']
                            trend_temp[trend_resp['year']]['statistics'] = ques1['statistics']
                            trend.append(trend_temp)
                            print(trend_temp)
                        elif ques1['qid'] == ques and ques1['qType'] == 'grid':
                            trend_result['qstring'] = ques1['qstring']
                            trend_result['qType'] = ques1['qType']
                            trend_result['qOrder'] = ques1['qOrder']
                            noOfAnswers = ques1['noOfAnswers'] + noOfAnswers
                            trend_temp[trend_resp['year']] = {}
                            trend_temp[trend_resp['year']]['options'] = ques1['options']
                            trend_temp[trend_resp['year']]['statistics'] = ques1['statistics']
                            trend_temp[trend_resp['year']]['statements'] = ques1['statements']
                            trend.append(trend_temp)
                        elif ques1['qid'] == ques and ques1['qType'] == 'numeric':
                            trend_result['qstring'] = ques1['qstring']
                            trend_result['qType'] = ques1['qType']
                            trend_result['qOrder'] = ques1['qOrder']
                            noOfAnswers = ques1['noOfAnswers'] + noOfAnswers
                            trend_temp[trend_resp['year']] = {}
                            trend_temp[trend_resp['year']]['options'] = ques1['options']
                            trend_temp[trend_resp['year']]['statistics'] = ques1['statistics']
                            trend_temp[trend_resp['year']]['numeric_items'] = ques1['numeric_items']
                            trend.append(trend_temp)
                        elif ques1['qid'] == ques and ques1['qType'] == 'rank':
                            trend_result['qstring'] = ques1['qstring']
                            trend_result['qType'] = ques1['qType']
                            trend_result['qOrder'] = ques1['qOrder']
                            noOfAnswers = ques1['noOfAnswers'] + noOfAnswers
                            trend_temp[trend_resp['year']] = {}
                            trend_temp[trend_resp['year']]['options'] = ques1['options']
                            trend_temp[trend_resp['year']]['statistics'] = ques1['statistics']
                            trend.append(trend_temp)
                        elif ques1['qid'] == ques and ques1['qType'] == 'simple':
                            trend_result['qstring'] = ques1['qstring']
                            trend_result['qType'] = ques1['qType']
                            trend_result['qOrder'] = ques1['qOrder']
                            noOfAnswers = ques1['noOfAnswers'] + noOfAnswers
                            trend_temp[trend_resp['year']] = {}
                            trend_temp[trend_resp['year']]['text_items'] = ques1['text_items']
                            trend.append(trend_temp)
                        elif ques1['qid'] == ques and ques1['qType'] == 'SlidingScale':
                            trend_result['qstring'] = ques1['qstring']
                            trend_result['qType'] = ques1['qType']
                            trend_result['qOrder'] = ques1['qOrder']
                            noOfAnswers = ques1['noOfAnswers'] + noOfAnswers
                            trend_temp[trend_resp['year']] = {}
                            trend_temp[trend_resp['year']]['options'] = ques1['options']
                            trend_temp[trend_resp['year']]['statistics'] = ques1['statistics']
                            trend_temp[trend_resp['year']]['numeric_items'] = ques1['numeric_items']
                            trend.append(trend_temp)
                            
                print('trendy')
                print(trend)
                """
                if trend_type == 'hourly':
                    x = samp1['hour'].unique()
                    for i in range(0,24):
                        if(i not in x):
                            trend_temp1 = {}
                            trend_temp1[ str(i) + ":00" + " to " + str(i) + ":59"] = []
                            trend.append(trend_temp1)
                elif trend_type == 'daily':
                    three_one_month_list = [1,3,5,7,8,10]
                    three_zero_even_month_list = [4,6,9,11]
                    february = [2]
                    december = [12]
                    #x = ['2017-2-16','2016-2-16']
                    x = samp1['updated_date'].unique()
                    if mon in three_one_month_list:
                        for i in range(day,32):
                            a = str(year) + '-' + str(mon) + '-' + str(i)
                            if a not in x:
                                trend_temp1 = {}
                                trend_temp1[ str(year) + '-' + str(mon) + "-" + str(i)] = []
                                trend.append(trend_temp1)
                        for j in range(1,day+1):
                            a = str(year) + '-' + str(mon+1) + '-' + str(j)
                            if a not in x:
                                trend_temp1 = {}
                                trend_temp1[ str(year) + '-' + str(mon+1) + "-" + str(j)] = []
                                trend.append(trend_temp1)
            
                    elif mon in three_zero_even_month_list:
                        for i in range(day,31):
                            a = str(year) + '-' + str(mon) + '-' + str(i)
                            if a not in x:
                                trend_temp1 = {}
                                trend_temp1[ str(year) + '-' + str(mon) + "-" + str(i)] = []
                                trend.append(trend_temp1)
                        for j in range(1,day+1):
                            a = str(year) + '-' + str(mon+1) + '-' + str(j)
                            if j not in x:
                                trend_temp1 = {}
                                trend_temp1[ str(year) + '-' + str(mon+1) + "-" + str(j)] = []
                                trend.append(trend_temp1)
            
                    elif mon in february:
                        for i in range(day,29):
                            a = str(year) + '-' + str(mon) + '-' + str(i)
                            if a not in x:
                                trend_temp1 = {}
                                trend_temp1[ str(year) + '-' + str(mon) + "-" + str(i)] = []
                                trend.append(trend_temp1)
                        for j in range(1,day+1):
                            a = str(year) + '-' + str(mon+1) + '-' + str(j)
                            if a not in x:
                                trend_temp1 = {}
                                trend_temp1[ str(year) + '-' + str(mon+1) + "-" + str(j)] = []
                                trend.append(trend_temp1)
            
                    elif mon in december:
                        for i in range(day,31):
                            a = str(year) + '-' + str(mon) + '-' + str(i)
                            if a not in x:
                                trend_temp1 = {}
                                trend_temp1[ str(year) + '-' + str(mon) + "-" + str(i)] = []
                                trend.append(trend_temp1)
                        for j in range(1,day+1):
                            a = str(year+1) + '-' + str(1) + '-' + str(j)
                            if a not in x:
                                trend_temp1 = {}
                                trend_temp1[ str(year+1) + '-' + str(1) + "-" + str(j)] = []
                                trend.append(trend_temp1)
                
                elif trend_type == 'monthly':
                    #x = ['2017-2']
                    x = samp1['updated_month'].unique()
                    for i in range(mon,13):
                        a = str(year) + '-' + str(i)
                        if a not in x:
                            trend_temp1 = {}
                            trend_temp1[ str(year) + "-" + str(i)] = []
                            trend.append(trend_temp1)      
                    for i in range(1,mon+1):
                        a = str(year+1) + '-' + str(i)
                        if a not in x:
                            trend_temp1 = {}
                            trend_temp1[ str(year+1) + "-" + str(i)] = []
                            trend.append(trend_temp1)
                """
                
                    
                print('RIPPPPPPPPPPPPp;')         
                trend_result['noOfAnswers'] = noOfAnswers
                trend_result['trend'] = trend
                response['AnalysisList'].append(trend_result)
            
                            
                            
                            
                        
                    
                
            return response
        except Exception as err:
            Object.logger.logActivity("INFO", "error in processing data : " + str(err), __name__)
        
        
    def OverviewAnalysis(self, typeOfAnalysis, dataSet, from_date, to_date,Object):
        try:
            
            import datetime
            # reading sample json :
            samp1 = pd.DataFrame(dataSet)
            
            print('welcome to overview analysis')
            final_list = {}
            print(len(from_date))
            print(type(from_date))
            #from_date = "2017-02-14 07:00"
            if len(from_date) > 0 and len(to_date) > 0:
                mon = int(from_date[5:7])
                updated_mon = from_date[0:7]
                day = int(from_date[8:10])
                year = int(from_date[0:4])
                #trend_type = 'daily'
                #print(samp1)
                
                data1 = pd.to_datetime(samp1['updatedAt'])
                hourlist = []
                daylist = []
                yearlist = []
                monthlist = []
                for i in data1:
                    j = str(i)
                    j = j[0:19]
                    print(i)
                    x = (datetime.datetime.strptime(j, "%Y-%m-%d  %H:%M:%S"))
                    hourlist.append(x.hour)
                    daylist.append(x.day)
                    monthlist.append(x.month)
                    yearlist.append(x.year)
                samp1['hour'] = hourlist
                samp1['day'] = daylist
                samp1['month'] = monthlist
                samp1['year'] = yearlist
                
                samp1['updated_month'] = samp1.year.map(str) + "-" + samp1.month.map(str)
                samp1['updated_date'] = samp1.updated_month + "-" + samp1.day.map(str)
                samp1['updated_time'] = samp1.hour.map(str) + ":00" + " to " + samp1.hour.map(str) + ":59" 
                
                trend_version = 'updated_date'
                print(samp1[trend_version])
                
                
                final_list['DailyResponses'] = []
                trend_list = samp1[trend_version].unique()
                print(trend_list)
                for trend in trend_list:
                    tmp = {}
                    print('trendddd is hereee')
                    print(trend)
                    samp = samp1[samp1[trend_version] == trend]
                    print(samp.shape)
                    tmp['Date'] = trend
                    tmp['Responses'] = samp.shape[0]
                    final_list['DailyResponses'].append(tmp)
                    
            final_list['ListofResponses'] = []
            for data in range(samp1.shape[0]):
                tmp = {}
                tmp['_id'] = samp1['_id'][data]
                tmp['updatedAt'] = samp1['updatedAt'][data]
                print(tmp)
                #print((samp1['distributionRecipientDetails'][data]['recipient'][0]))
                if len(samp1['distributionRecipientDetails'][data]['recipient']) == 0:
                    tmp['firstName'] = 'null'
                    tmp['lastName'] = 'null'
                    tmp['email'] = 'null'
                    tmp['phoneNumber'] = 'null'
                else:
                    details = samp1['distributionRecipientDetails'][data]['recipient'][0]
                    if 'firstName' in details:
                        tmp['firstName'] = details['firstName']
                    else:
                        tmp['firstName'] = 'null'
                    if 'lastName' in details:
                        tmp['lastName'] = details['lastName']
                    else:
                        tmp['lastName'] = 'null'
                    if 'email' in details:
                        tmp['email'] = details['email']
                    else:
                        tmp['email'] = 'null'
                    if 'phoneNumber' in details:
                        tmp['phoneNumber'] = details['phoneNumber']
                    else:
                        tmp['phoneNumber'] = 'null'
                tmp['Answers'] = len(samp1['answers'][data])
                
                variable = samp1['clientMetadata'][data]
                print(type(variable))
                if  variable is not None:
                    print('hey')
                    if 'ipAddress' in samp1['clientMetadata'][data]:
                        tmp['ipAddress'] =  samp1['clientMetadata'][data]['ipAddress']
                    else:
                        tmp['ipAddress'] = 'null'
                    if 'userAgent' in samp1['clientMetadata'][data]:
                        tmp['userAgent'] =  samp1['clientMetadata'][data]['userAgent']
                    else:
                        tmp['userAgent'] = 'null'
                    if 'channel' in samp1['distributionRecipientDetails'][data]:
                        tmp['channel'] =  samp1['distributionRecipientDetails'][data]['channel']
                    else:
                        tmp['channel'] = 'null'
                else:
                    tmp['channel'] = 'null'
                    tmp['userAgent'] = 'null'
                    tmp['ipAddress'] = 'null'
                     
                print(tmp)
                final_list['ListofResponses'].append(tmp)
            
            
            
            return final_list
            
            
        except Exception as err:
            Object.logger.logActivity("INFO", "error in processing data : " + str(err), __name__)
            
            
        
    
    
    
    



            
