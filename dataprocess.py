from datetime import *
import string
import copy

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
        self.prscrp={}
        self.totalPeriod={}
        self.totalEpisodeLen={}
        self.avgEpisodeLen={}
        self.maxEpisodeLen={}
        self.minEpisodeLen={}
        self.avgCSA={}
        self.maxCSA={}
        self.minCSA={}
        self.avgCMG={}
        self.maxCMG={}
        self.minCMG={}
        self.MPR={}
        self.gapOverlap={}

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
    data=f.readlines()
    f.close()
    patients={}#PatientID -> Patient, Patient.prscrp: DrugID -> [(StartDate, EndDate)], Patient.stats: DrugID -> value
    for line in data:
        if line[-1]=='\n':
            line=line[0:-1]
        seg=line.split('\t')
        if seg[0] not in patients:#add new patient
            patients[seg[0]]=Patient()
            for drug in drugList:#add drugs
                patients[seg[0]].prscrp[drug]=[]
                patients[seg[0]].totalPeriod[drug]=0
                patients[seg[0]].totalEpisodeLen[drug]=0
                patients[seg[0]].avgEpisodeLen[drug]=0
                patients[seg[0]].maxEpisodeLen[drug]=0
                patients[seg[0]].minEpisodeLen[drug]=0
                patients[seg[0]].avgCSA[drug]=0
                patients[seg[0]].maxCSA[drug]=0
                patients[seg[0]].minCSA[drug]=0
                patients[seg[0]].avgCMG[drug]=0
                patients[seg[0]].maxCMG[drug]=0
                patients[seg[0]].minCMG[drug]=0
                patients[seg[0]].MPR[drug]=0
                patients[seg[0]].gapOverlap[drug]=[]
        #TODO: filter by gender, age
        if seg[1] in patients[seg[0]].prscrp:#add prescription
            startSeg=seg[2].split('/')
            endSeg=seg[3].split('/')
            dates=[]
            dates.append(date(string.atoi(startSeg[2]), string.atoi(startSeg[0]), string.atoi(startSeg[1])))
            dates.append(date(string.atoi(endSeg[2]), string.atoi(endSeg[0]), string.atoi(endSeg[1])))
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
                    patients[seg[0]].prscrp[seg[1]].append(dates)
            else:
                patients[seg[0]].prscrp[seg[1]].append(dates)

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
                csa=[]
                for i in range(len(drugRecords)-1):
                    supplyLen=(drugRecords[i][1]-drugRecords[i][0]).days
                    intervalLen=(drugRecords[i+1][0]-drugRecords[i][0]).days
                    if intervalLen>0:
                        csa.append(supplyLen*1.0/intervalLen)
                    else:
                        csa.append(1.0)
                patient.avgCSA[drugID]=1.0
                patient.maxCSA[drugID]=1.0
                patient.minCSA[drugID]=1.0
                if len(csa)>0:
                    patient.avgCSA[drugID]=sum(csa)*1.0/len(csa)
                    patient.maxCSA[drugID]=max(csa)
                    patient.minCSA[drugID]=min(csa)
                #compute CMG
                cmg=[]
                for i in range(len(drugRecords)-1):
                    gapLen=(drugRecords[i+1][0]-drugRecords[i][1]).days
                    intervalLen=(drugRecords[i+1][0]-drugRecords[i][0]).days
                    if gapLen<0:
                        gapLen=0
                    if intervalLen>0:
                        cmg.append(gapLen*1.0/intervalLen)
                    else:
                        cmg.append(0.0)
                patient.avgCMG[drugID]=0.0
                patient.maxCMG[drugID]=0.0
                patient.minCMG[drugID]=0.0
                if len(cmg)>0:
                    patient.avgCMG[drugID]=sum(cmg)*1.0/len(cmg)
                    patient.maxCMG[drugID]=max(cmg)
                    patient.minCMG[drugID]=min(cmg)  
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

    #printPatients(patients)

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
            drug["average_csa"] = patient.avgCSA[drugID]
            drug["max_csa"] = patient.maxCSA[drugID]
            drug["min_csa"] = patient.minCSA[drugID]
            drug["avg_cmg"] = patient.avgCMG[drugID]
            drug["max_cmg"] = patient.maxCMG[drugID]
            drug["min_cmg"] = patient.minCMG[drugID]
            drug["mpr"] = patient.MPR[drugID]
            drug["period"] = map(lambda x: [ unix_time_millis(x[0]), unix_time_millis(x[1]), x[2] ], patient.gapOverlap[drugID])

            drugsList.append(drug)

        patientsDetails["drug_details"] = drugsList
        patientsDetails["patient_id"] = patientID

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
        for drugID, drugRecords in patient.prscrp.items():
            print '\t'+str(drugID)
            print '\t\tTotal Period: '+str(patient.totalPeriod[drugID])
            print '\t\tTotal Episode Length: '+str(patient.totalEpisodeLen[drugID])
            print '\t\tAverage Episode Length: '+str(patient.avgEpisodeLen[drugID])
            print '\t\tMax Episode Length: '+str(patient.maxEpisodeLen[drugID])
            print '\t\tMin Episode Length: '+str(patient.minEpisodeLen[drugID])
            print '\t\tAverage CSA: '+str(patient.avgCSA[drugID])
            print '\t\tMax CSA: '+str(patient.maxCSA[drugID])
            print '\t\tMin CSA: '+str(patient.minCSA[drugID])
            print '\t\tAverage CMG: '+str(patient.avgCMG[drugID])
            print '\t\tMax CMG: '+str(patient.maxCMG[drugID])
            print '\t\tMin CMG: '+str(patient.minCMG[drugID])
            print '\t\tMPR: '+str(patient.MPR[drugID])

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

#process('data.txt', drugList=['41', '42'], overlap=0, gap=0)

