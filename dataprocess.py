from datetime import *
import string
import copy
import random

import datetime

def unix_time(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    dt = datetime.datetime.combine(dt, datetime.time())
    delta = dt - epoch
    return delta.total_seconds()

def unix_time_millis(dt):
    return unix_time(dt) * 1000.0

class Patient:
    def __init__(self):
        self.age=0
        self.gender=0#0 for male, 1 for female
        #prescriptions
        self.prscrp={}
        #period
        self.totalPeriod={}
        #episode length
        self.totalEpisodeLen={}
        self.avgEpisodeLen={}
        self.maxEpisodeLen={}
        self.minEpisodeLen={}
        #CSA
        self.csa={}
        self.csaIntervalLen={}
        self.avgCSA={}
        self.maxCSA={}
        self.minCSA={}
        #CMG
        self.cmg={}
        self.cmgIntervalLen={}
        self.avgCMG={}
        self.maxCMG={}
        self.minCMG={}
        #MPR
        self.MPR={}
        self.MPR30Day={}
        self.MPRCI={}
        #gap and overlap
        self.gapOverlap={}
        self.avgGapLen={}
        self.avgOverlapLen={}
        #30-day and 90-day prescriptions
        self.day30={}
        self.day90={}

class Drug:
    def __init__(self):
        self.totalPeriod=[]
        self.totalEpisodeLen=[]
        self.avgEpisodeLen=[]
        self.maxEpisodeLen=[]
        self.minEpisodeLen=[]
        self.avgCSA=[]
        self.maxCSA=[]
        self.minCSA=[]
        self.avgCMG=[]
        self.maxCMG=[]
        self.minCMG=[]
        self.MPR=[]

def process(fileName, drugList=[], gender=[], ageMin=0, ageMax=100, gap=0, overlap=0):
    #read data
    f=file(fileName, 'r')
    patients={}#PatientID -> Patient, Patient.prscrp: DrugID -> [(StartDate, EndDate)], Patient.stats: DrugID -> value
    for line in f:
        if line[-1]=='\n':
            line=line[0:-1]
        seg=line.split('\t')
        if seg[0] not in patients:#add new patient
            patients[seg[0]]=Patient()
            #random age and gender
            patients[seg[0]].age=random.randint(0, 100)
            patients[seg[0]].gender=random.randint(0, 1)
            for drug in drugList:#add drugs
                patients[seg[0]].prscrp[drug]=[]
                patients[seg[0]].totalPeriod[drug]=0
                patients[seg[0]].totalEpisodeLen[drug]=0
                patients[seg[0]].avgEpisodeLen[drug]=0
                patients[seg[0]].maxEpisodeLen[drug]=0
                patients[seg[0]].minEpisodeLen[drug]=0
                patients[seg[0]].csa[drug]=[]
                patients[seg[0]].csaIntervalLen[drug]=[]
                patients[seg[0]].avgCSA[drug]=0
                patients[seg[0]].maxCSA[drug]=0
                patients[seg[0]].minCSA[drug]=0
                patients[seg[0]].cmg[drug]=[]
                patients[seg[0]].cmgIntervalLen[drug]=[]
                patients[seg[0]].avgCMG[drug]=0
                patients[seg[0]].maxCMG[drug]=0
                patients[seg[0]].minCMG[drug]=0
                patients[seg[0]].MPR[drug]=0
                patients[seg[0]].MPR30Day[drug]=[]
                patients[seg[0]].MPRCI[drug]=[]
                patients[seg[0]].gapOverlap[drug]=[]
                patients[seg[0]].avgGapLen[drug]=0
                patients[seg[0]].avgOverlapLen[drug]=0
                patients[seg[0]].day30[drug]=0
                patients[seg[0]].day90[drug]=0
        #TODO: filter by gender, age
        if seg[1] in patients[seg[0]].prscrp:#add prescription
            #startSeg=seg[2].split('/')
            #endSeg=seg[3].split('/')
            startSeg=seg[2].split('-')
            endSeg=seg[3].split(' ')[0].split('-')
            dates=[]
            #dates.append(date(string.atoi(startSeg[2]), string.atoi(startSeg[0]), string.atoi(startSeg[1])))
            #dates.append(date(string.atoi(endSeg[2]), string.atoi(endSeg[0]), string.atoi(endSeg[1])))
            dates.append(date(string.atoi(startSeg[0]), string.atoi(startSeg[1]), string.atoi(startSeg[2])))
            dates.append(date(string.atoi(endSeg[0]), string.atoi(endSeg[1]), string.atoi(endSeg[2])))
            if (dates[1]-dates[0]).days==30:
                patients[seg[0]].day30[seg[1]]+=1
            if (dates[1]-dates[0]).days==90:
                patients[seg[0]].day90[seg[1]]+=1
            #remove gaps and overlaps
            records=patients[seg[0]].prscrp[seg[1]]
            if len(records)>0:
                if records[len(records)-1][1]<dates[0]:#gap
                    patients[seg[0]].gapOverlap[seg[1]].append((records[len(records)-1][1], dates[0], 0))
                if records[len(records)-1][1]>dates[0]:#overlap
                    patients[seg[0]].gapOverlap[seg[1]].append((records[len(records)-1][1], dates[0], 1))
                if (records[len(records)-1][1]<dates[0] and (dates[0]-records[len(records)-1][1]).days<gap)\
                   or (records[len(records)-1][1]>dates[0] and (records[len(records)-1][1]-dates[0]).days<overlap):
                    records[len(records)-1][1]=dates[1]
                else:
                    if records[len(records)-1][1]>dates[0] and (records[len(records)-1][1]-dates[0]).days>overlap:
                        overlapLen=(records[len(records)-1][1]-dates[0]).days
                        dates[0]=dates[0]+datetime.timedelta(days=overlapLen)
                        dates[1]=dates[1]+datetime.timedelta(days=overlapLen)
                    patients[seg[0]].prscrp[seg[1]].append(dates)
            else:
                patients[seg[0]].prscrp[seg[1]].append(dates)
    f.close()
    
    #compute values
    for patientID, patient in patients.iteritems():
        for drugID, drugRecords in patient.prscrp.items():
            if len(drugRecords)>0:
                #compute total period of medicatio time
                patient.totalPeriod[drugID]=(drugRecords[len(drugRecords)-1][1]-drugRecords[0][0]).days
                #compute episode length
                episodeLens=[]
                for record in drugRecords:
                    episodeLens.append((record[1]-record[0]).days)
                patient.totalEpisodeLen[drugID]=sum(episodeLens)
                patient.avgEpisodeLen[drugID]=sum(episodeLens)*1.0/len(episodeLens)
                patient.maxEpisodeLen[drugID]=max(episodeLens)
                patient.minEpisodeLen[drugID]=min(episodeLens)
                #compute CSA
                for i in range(len(drugRecords)-1):
                    supplyLen=(drugRecords[i][1]-drugRecords[i][0]).days
                    intervalLen=(drugRecords[i+1][0]-drugRecords[i][0]).days
                    if intervalLen>0:
                        patient.csa[drugID].append(supplyLen*1.0/intervalLen)
                        patient.csaIntervalLen[drugID].append(intervalLen)
                    else:
                        patient.csa[drugID].append(1.0)
                        patient.csaIntervalLen[drugID].append(0)
                patient.avgCSA[drugID]=1.0
                patient.maxCSA[drugID]=1.0
                patient.minCSA[drugID]=1.0
                if len(patient.csa[drugID])>0:
                    patient.avgCSA[drugID]=sum(patient.csa[drugID])*1.0/len(patient.csa[drugID])
                    patient.maxCSA[drugID]=max(patient.csa[drugID])
                    patient.minCSA[drugID]=min(patient.csa[drugID])
                #compute CMG
                for i in range(len(drugRecords)-1):
                    gapLen=(drugRecords[i+1][0]-drugRecords[i][1]).days
                    intervalLen=(drugRecords[i+1][0]-drugRecords[i][0]).days
                    if gapLen<0:
                        gapLen=0
                    if intervalLen>0:
                        patient.cmg[drugID].append(gapLen*1.0/intervalLen)
                        patient.cmgIntervalLen[drugID].append(intervalLen)
                    else:
                        patient.cmg[drugID].append(0.0)
                        patient.cmgIntervalLen[drugID].append(0)
                patient.avgCMG[drugID]=0.0
                patient.maxCMG[drugID]=0.0
                patient.minCMG[drugID]=0.0
                if len(patient.cmg[drugID])>0:
                    patient.avgCMG[drugID]=sum(patient.cmg[drugID])*1.0/len(patient.cmg[drugID])
                    patient.maxCMG[drugID]=max(patient.cmg[drugID])
                    patient.minCMG[drugID]=min(patient.cmg[drugID])  
                #compute MPR
                supplyLen=0
                for i in range(len(drugRecords)-1):
                    if drugRecords[i][1]>drugRecords[i+1][0]:
                        supplyLen+=(drugRecords[i+1][0]-drugRecords[i][0]).days
                    else:
                        supplyLen+=(drugRecords[i][1]-drugRecords[i][0]).days
                supplyLen+=(drugRecords[len(drugRecords)-1][1]-drugRecords[len(drugRecords)-1][0]).days
                patient.MPR[drugID]=0
                if patient.totalPeriod[drugID]>0:
                    patient.MPR[drugID]=supplyLen*1.0/patient.totalPeriod[drugID]
                #compute 30-day MPRs
                startDate=drugRecords[0][0]
                endDate=drugRecords[len(drugRecords)-1][1]
                newRecords=[]
                for i in range(len(drugRecords)):#merge overlaps
                    if len(newRecords)>0:
                        if (newRecords[len(newRecords)-1][1]-drugRecords[i][0]).days>=-1:
                            newRecords[len(newRecords)-1][1]=drugRecords[i][1]
                        else:
                            newRecords.append(drugRecords[i])
                    else:
                        newRecords.append(drugRecords[i])
                index=0
                while startDate<endDate:
                    nextEndDate=min(startDate+datetime.timedelta(days=30), endDate)
                    if (nextEndDate-startDate).days<30:
                        break
                    interval=(nextEndDate-startDate).days
                    supplyLen=0
                    while startDate<nextEndDate:
                        startDate=max(startDate, min(nextEndDate, newRecords[index][0]))
                        tempLen=(min(nextEndDate, newRecords[index][1])-startDate).days
                        supplyLen+=tempLen
                        startDate=startDate+datetime.timedelta(days=tempLen)
                        if startDate<nextEndDate:
                            index+=1
                    patient.MPR30Day[drugID].append(supplyLen*1.0/interval)
                #compute 30-day MPR CI
                avgMPR30=0.0
                if len(patient.MPR30Day[drugID])>0:
                    avgMPR30=sum(patient.MPR30Day[drugID])*1.0/len(patient.MPR30Day[drugID])
                stdErr=0.0
                for i in range(len(patient.MPR30Day[drugID])):
                    stdErr+=(patient.MPR30Day[drugID][i]-avgMPR30)*(patient.MPR30Day[drugID][i]-avgMPR30)
                if len(patient.MPR30Day[drugID])>0:
                    stdErr/=len(patient.MPR30Day[drugID])
                stdErr=stdErr**0.5
                patient.MPRCI[drugID].append(avgMPR30-1.96*stdErr)
                patient.MPRCI[drugID].append(avgMPR30+1.96*stdErr)
                #compute average gap and overlap lengths
                gapLen=[]
                overlapLen=[]
                for i in range(len(patient.gapOverlap[drugID])):
                    if patient.gapOverlap[drugID][i][2]==0:
                        gapLen.append((patient.gapOverlap[drugID][i][1]-patient.gapOverlap[drugID][i][0]).days)
                    else:
                        overlapLen.append((patient.gapOverlap[drugID][i][0]-patient.gapOverlap[drugID][i][1]).days)
                if len(gapLen)>0:
                    patient.avgGapLen[drugID]=sum(gapLen)*1.0/len(gapLen)
                if len(overlapLen)>0:
                    patient.avgOverlapLen[drugID]=sum(overlapLen)*1.0/len(overlapLen)

    #printPatients(patients)
    #writePatients(patients)

    #collect stats
    drugStats={}
    for drugID in drugList:
        drugStats[drugID]=Drug()
    for patientID, patient in patients.items():
        for drugID in drugList:
            if patient.totalPeriod[drugID]>0:#filter patients who never take current drug
                drugStats[drugID].totalPeriod.append(patient.totalPeriod[drugID])
                drugStats[drugID].totalEpisodeLen.append(patient.totalEpisodeLen[drugID])
                drugStats[drugID].avgEpisodeLen.append(patient.avgEpisodeLen[drugID])
                drugStats[drugID].maxEpisodeLen.append(patient.maxEpisodeLen[drugID])
                drugStats[drugID].minEpisodeLen.append(patient.minEpisodeLen[drugID])
                drugStats[drugID].avgCSA.append(patient.avgCSA[drugID])
                drugStats[drugID].maxCSA.append(patient.maxCSA[drugID])
                drugStats[drugID].minCSA.append(patient.minCSA[drugID])
                drugStats[drugID].avgCMG.append(patient.avgCMG[drugID])
                drugStats[drugID].maxCMG.append(patient.maxCMG[drugID])
                drugStats[drugID].minCMG.append(patient.minCMG[drugID])
                drugStats[drugID].MPR.append(patient.MPR[drugID])
    #sort stats
    for drugID in drugList:
        drugStats[drugID].totalPeriod.sort()
        drugStats[drugID].totalEpisodeLen.sort()
        drugStats[drugID].avgEpisodeLen.sort()
        drugStats[drugID].maxEpisodeLen.sort()
        drugStats[drugID].minEpisodeLen.sort()
        drugStats[drugID].avgCSA.sort()
        drugStats[drugID].maxCSA.sort()
        drugStats[drugID].minCSA.sort()
        drugStats[drugID].avgCMG.sort()
        drugStats[drugID].maxCMG.sort()
        drugStats[drugID].minCMG.sort()
        drugStats[drugID].MPR.sort()

    return patients, drugStats


def patientsJSON(patients):
    
    patientsList = []
    for patientID, patient in patients.items():

        patientsDetails = {}

        drugsList = []

        for drugID, drugRecords in patient.prscrp.items():
            drug = {}
            drug["drug_id"] = drugID
            drug["total_period"] = patient.totalPeriod[drugID]
            drug["total_episode_length"] = patient.totalEpisodeLen[drugID]
            drug["average_episode_length"] = patient.avgEpisodeLen[drugID]
            drug["max_episode_length"] = patient.maxEpisodeLen[drugID]
            drug["min_episode_length"] = patient.minEpisodeLen[drugID]
            drug["csa"] = patient.csa[drugID]
            drug["csa_interval_len"] = patient.cmgIntervalLen[drugID]
            drug["average_csa"] = patient.avgCSA[drugID]
            drug["max_csa"] = patient.maxCSA[drugID]
            drug["min_csa"] = patient.minCSA[drugID]
            drug["cmg"] = patient.cmg[drugID]
            drug["cmg_interval_len"] = patient.cmgIntervalLen[drugID]
            drug["mpr_30"] = patient.MPR30Day[drugID]
            drug["avg_cmg"] = patient.avgCMG[drugID]
            drug["max_cmg"] = patient.maxCMG[drugID]
            drug["min_cmg"] = patient.minCMG[drugID]
            drug["mpr"] = patient.MPR[drugID]
            drug["period"] = map(lambda x: [ unix_time_millis(x[0]), unix_time_millis(x[1]), x[2] ], patient.gapOverlap[drugID])
            drug["avg_gap_length"] = patient.avgGapLen[drugID]
            drug["avg_overlap_length"] = patient.avgOverlapLen[drugID]
            drug["day_30"] = patient.day30[drugID]
            drug["day_90"] = patient.day90[drugID]
 

            drugsList.append(drug)


        patientsDetails["drug_details"] = drugsList
        patientsDetails["patient_id"] = patientID
        patientsDetails["gender"] = patient.gender
        patientsDetails["age"] = patient.age
        

        patientsList.append(patientsDetails)


    return patientsList



def drugsJSON(drugStats, drugList):

    drugs = {}

    for drugID in drugList:
        drug = {}
        
        drug['total_period'] = drugStats[drugID].totalPeriod
        drug['total_episode_length'] = drugStats[drugID].totalEpisodeLen
        drug['average_episode_length'] = drugStats[drugID].avgEpisodeLen
        drug['max_episode_length'] = drugStats[drugID].maxEpisodeLen
        drug['min_episode_length'] = drugStats[drugID].minEpisodeLen
        drug['average_csa'] = drugStats[drugID].avgCSA
        drug['max_csa'] = drugStats[drugID].maxCSA
        drug['min_csa'] = drugStats[drugID].minCSA
        drug['avg_cmg'] = drugStats[drugID].avgCMG
        drug['max_cmg'] = drugStats[drugID].maxCMG
        drug['min_cmg'] = drugStats[drugID].minCMG
        drug['mpr'] = drugStats[drugID].MPR

        drugs[drugID] = drug

    return drugs

             
#following functions are for debugging
def printPatients(patients):
    for patientID, patient in patients.items():
        print patientID
        print 'Age: '+str(patient.age)
        print 'Gender: '+str(patient.gender)
        for drugID, drugRecords in patient.prscrp.items():
            print '\t'+str(drugID)
            print '\t\tTotal Period: '+str(patient.totalPeriod[drugID])
            print '\t\tTotal Episode Length: '+str(patient.totalEpisodeLen[drugID])
            print '\t\tAverage Episode Length: '+str(patient.avgEpisodeLen[drugID])
            print '\t\tMax Episode Length: '+str(patient.maxEpisodeLen[drugID])
            print '\t\tMin Episode Length: '+str(patient.minEpisodeLen[drugID])
            print '\t\tCSA: '+str(patient.csa[drugID])
            print '\t\tCSA Interval Lengths: '+str(patient.csaIntervalLen[drugID])
            print '\t\tAverage CSA: '+str(patient.avgCSA[drugID])
            print '\t\tMax CSA: '+str(patient.maxCSA[drugID])
            print '\t\tMin CSA: '+str(patient.minCSA[drugID])
            print '\t\tCMG: '+str(patient.cmg[drugID])
            print '\t\tCMG Interval Lengths: '+str(patient.cmgIntervalLen[drugID])
            print '\t\tAverage CMG: '+str(patient.avgCMG[drugID])
            print '\t\tMax CMG: '+str(patient.maxCMG[drugID])
            print '\t\tMin CMG: '+str(patient.minCMG[drugID])
            print '\t\tMPR: '+str(patient.MPR[drugID])
            print '\t\t30-Day MPRs: '+str(patient.MPR30Day[drugID])
            print '\t\t30-Day MPR CI: '+str(patient.MPRCI[drugID])
            print '\t\t30-Day Prescriptions: '+str(patient.day30[drugID])
            print '\t\t90-Day Prescriptions: '+str(patient.day90[drugID])
            print '\t\tAverage Gap Length: '+str(patient.avgGapLen[drugID])
            print '\t\tAverage Overlap Length: '+str(patient.avgOverlapLen[drugID])

def writePatients(patients):
    f=file('data/test.txt', 'w')
    for patientID, patient in patients.items():
        for drugID, drugRecords in patient.prscrp.items():
            if patient.totalPeriod[drugID]>=750:
                f.write(patientID+'\t'+drugID+'\n')
                f.write('30-Day MPRs: '+str(patient.MPR30Day[drugID])+'\n')
    f.close()

def printDrugStats(drugStats, drugList):
    for drugID in drugList:
        print drugID
        print 'Total Period:'
        print drugStats[drugID].totalPeriod
        print 'Total Episode Length:'
        print drugStats[drugID].totalEpisodeLen
        print 'Average Episode Length:'
        print drugStats[drugID].avgEpisodeLen
        print 'Max Episode Length:'
        print drugStats[drugID].maxEpisodeLen
        print 'Min Episode Length:'
        print drugStats[drugID].minEpisodeLen
        print 'Average CSA:'
        print drugStats[drugID].avgCSA
        print 'Max CSA:'
        print drugStats[drugID].maxCSA
        print 'Min CSA:'
        print drugStats[drugID].minCSA
        print 'Average CMG:'
        print drugStats[drugID].avgCMG
        print 'Max CMG:'
        print drugStats[drugID].maxCMG
        print 'Min CMG:'
        print drugStats[drugID].minCMG
        print 'MPR:'
        print drugStats[drugID].MPR

def mergeFilesByDate(fileList, mergedFileName='data/AceBetaDiur.txt', startDate=date(2007, 1, 1), endDate=date(2012, 1, 1)):
    f=file(mergedFileName, 'w')
    for fileName in fileList:
        ff=file(fileName, 'r')
        data=ff.readlines()
        ff.close()
        for line in data:
            if line[-1]=='\n':
                line=line[0:-1]
            seg=line.split('\t')
            startSeg=seg[2].split('-')
            endSeg=seg[3].split(' ')[0].split('-')
            itemStartDate=date(string.atoi(startSeg[0]), string.atoi(startSeg[1]), string.atoi(startSeg[2]))
            itemEndDate=date(string.atoi(endSeg[0]), string.atoi(endSeg[1]), string.atoi(endSeg[2]))
            if itemStartDate>=startDate and itemStartDate<=endDate and itemEndDate>=startDate and itemEndDate<=endDate:
                f.write(line+'\n')
    f.close()

def getMedicationLength(fileList, medLenFileName='data/medLen.txt', sortedMedLenFileName='data/sortedMedLen.txt'):
    f1=file(medLenFileName, 'w')
    f2=file(sortedMedLenFileName, 'w')
    medLens=[]
    startDates={}
    endDates={}
    for fileName in fileList:
        ff=file(fileName, 'r')
        for line in ff:
            if line[-1]=='\n':
                line=line[0:-1]
            seg=line.split('\t')
            startSeg=seg[2].split('-')
            endSeg=seg[3].split(' ')[0].split('-')
            startDate=date(string.atoi(startSeg[0]), string.atoi(startSeg[1]), string.atoi(startSeg[2]))
            endDate=date(string.atoi(endSeg[0]), string.atoi(endSeg[1]), string.atoi(endSeg[2]))
            if seg[0] in startDates:
                if startDate<startDates[seg[0]]:
                    startDates[seg[0]]=startDate
                if endDate>endDates[seg[0]]:
                    endDates[seg[0]]=endDate
            else:
                startDates[seg[0]]=startDate
                endDates[seg[0]]=endDate
        ff.close()
    for patientID in startDates:
        medLen=(endDates[patientID]-startDates[patientID]).days
        medLens.append(medLen)
        f1.write(patientID+'\t'+str(medLen)+'\n')
    f1.close()
    medLens.sort()
    for medLen in medLens:
        f2.write(str(medLen)+'\n')
    f2.close()

def mergeFilesByMedLen(fileList, medLenFileName='data/medLen.txt', mergedFileName='data/AceBetaDiur.txt', medLenThreshold=30):
    f1=file(medLenFileName, 'r')
    medLens={}
    for line in f1:
        if line[-1]=='\n':
            line=line[0:-1]
        seg=line.split('\t')
        medLen=string.atoi(seg[1])
        if medLen>medLenThreshold:
            medLens[seg[0]]=string.atoi(seg[1])
    f1.close()
    f2=file(mergedFileName, 'w')
    for fileName in fileList:
        ff=file(fileName, 'r')
        for line in ff:
            seg=line.split('\t')
            if seg[0] in medLens:
                f2.write(line)
        ff.close()
    f2.close()

def mergeFilesByRandom(fileList, medLenFileName='data/medLen.txt', mergedFileName='data/Ace_Beta_Diur_3SamplingRate.txt', ratio=0.03):
    f1=file(medLenFileName, 'r')
    medLens={}
    for line in f1:
        if line[-1]=='\n':
            line=line[0:-1]
        seg=line.split('\t')
        medLen=string.atoi(seg[1])
        p=random.random()
        if p<ratio:
            medLens[seg[0]]=medLen
    f1.close()
    f2=file(mergedFileName, 'w')
    for fileName in fileList:
        ff=file(fileName, 'r')
        for line in ff:
            seg=line.split('\t')
            if seg[0] in medLens:
                f2.write(line)
        ff.close()
    f2.close()

#mergeFilesByRandom(fileList=['data/AceOnly.txt', 'data/BetaOnly.txt', 'data/DiurOnly.txt'])
#mergeFilesByMedLen(fileList=['data/AceOnly.txt', 'data/BetaOnly.txt', 'data/DiurOnly.txt'], medLenThreshold=750)
#getMedicationLength(['data/AceOnly.txt', 'data/BetaOnly.txt', 'data/DiurOnly.txt'])
#mergeFilesByDate(fileList=['data/AceOnly.txt', 'data/BetaOnly.txt', 'data/DiurOnly.txt'], startDate=date(2008, 11, 1), endDate=date(2008, 12, 31))
process('data/Ace_Beta_Diur_3SamplingRate.txt', drugList=['1', '3', '5'], overlap=0, gap=0)

