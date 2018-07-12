import re
import sys
import requests
import json

investorAndCompanyNames = {}
companyNameAndCompanyValue = {}
investorNameAndAmountInvested = {}

def extractData(url):
    """Extracting Information From Link
    Args:
         param (str): Link from where data has to be scrapped.
    Returns:
            {
              investorAndCompanyNames (dictionary): Contains Investor name as key And All Company Names as value in which investor invested
              companyNameAndCompanyValue (dictionary): Contains Company Name as as key And Company Value estimated by investor
              investorNameAndAmountInvested (dictionary): Contains Investor Name as key And Total Amount invested by investor
            }
    
    """
    if(len(url)>0):
         #Getting JSON Data From URL Using Requests Module
        
         try:
             r = requests.get('https://gist.githubusercontent.com/murtuzakz/4bd887712703ff14c9b0f7c18229b332/raw/d0dd1c59016e2488dcbe0c8e710a1c5df9c3672e/season7.json')
         except requests.exceptions.RequestException as e:
             print("Oops! Kindly Check your Internet Connection")
             sys.exit(1)
         else:
             data = json.loads(r.text)

         #Analysing JSON Data as Dictionary
             
         for listOfEpisodes in data.keys():
             infoOfEpisodes = data[listOfEpisodes]
             for j in range(len(infoOfEpisodes)):
                 for investorsKey,nameOfInvestors in infoOfEpisodes[j].items():
                     
                     #Trying to find name of investors who funded for the respective companies
                     
                     if re.search("investors",investorsKey):
                        if nameOfInvestors:
                              listOfNames = []
                              temp = nameOfInvestors.find("and")#Case where name contains "and" just separating them
                              if(temp > 0): 
                                  listOfNames = nameOfInvestors.replace("and",",").split(',')
                                  listOfNames[0]=listOfNames[0].replace('\n','')
                                  listOfNames[1]=listOfNames[1].replace('\n','')
                              else:
                                  listOfNames = nameOfInvestors.split(",") #If there is no "and" in name then split on the basis of comma
                              for i in listOfNames:
                                  if (len(i)>1):
                                      
                                      #Taking Care of Special Case Whose name is "Kevin O'Lorean"
                                      
                                      if re.search("Kevin",i):
                                          lt = i.strip(' ').split(' ')
                                          if (len(lt)>2):
                                              i = lt[0]+" "+ lt[1]+lt[2]
                                          else:
                                              i = lt[0]+" " +lt[1]
                                      investorName = i.strip(' ')
                                      investorAndCompanyNames[investorName]=investorAndCompanyNames.setdefault(investorName,[])
                                      companyName = infoOfEpisodes[j]['company']['title']
                                      
                                      #Converting Unicode Company Name into 'utf-8'
                                      
                                      if re.search("\\xa0",companyName):
                                          encoded_str = companyName.encode('ascii','ignore')
                                          decoded_str = encoded_str.decode('utf-8')
                                          companyName = decoded_str
                                          investorAndCompanyNames[investorName].append(companyName)
                                      else:
                                         investorAndCompanyNames[investorName].append(companyName)
                                      companyNameAndCompanyValue[companyName]=companyNameAndCompanyValue.setdefault(companyName,1)
                                      
                                      #Separating the amount and percentage value invested by investor
                                      
                                      amount = infoOfEpisodes[j]['kitna']
                                      m = amount.split('for')
                                      match = re.search("\$((\d+\.\d+)|(\d+))K",m[0])
                                      if (match):
                                          investedAmountByInvestor = float(match.group(1))*1000
                                      match = re.search("\$((\d+\.\d+)|(\d+))M",m[0])
                                      if (match):
                                          investedAmountByInvestor = float(match.group(1))*1000000
                                      match = re.search("((\d+)|(\d+\.\d+))%",m[1])
                                      if (match):
                                          percent = float(match.group(1))
                                      companyValueInDollar = (investedAmountByInvestor/percent)*100
                                      companyNameAndCompanyValue[companyName]=round(companyValueInDollar)
                                      investorNameAndAmountInvested[investorName] = investorNameAndAmountInvested.setdefault(investorName,1)
                                      investorNameAndAmountInvested[investorName] += investedAmountByInvestor
    else:
        print("Empty String Given")


#Getting list of all investors in a sorted order who invested in more number of companies
def getListOfInvestorAndCompanyNames():
    ranked = sorted(investorAndCompanyNames.items(),key=lambda e:len(e[1]),reverse=True)#Doing Sorting Bases On Number Of Companies
    return ranked


#Representing list of company with their predicted full current value
def getListOfComapnyNameAndCompanyValue():
    ranked = sorted(companyNameAndCompanyValue.items(),key=lambda e:e[1],reverse=True)
    return ranked

#Representing Total Amount And Average Amount invested by an Investor
def getListOfInvestorAndInvestedAmount():
    ranked = sorted(investorNameAndAmountInvested.items(),key=lambda e:e[1],reverse=True)
    """for i in range(len(ranked)):
        #print("\n{} : Total Investment ${} , average investment ${:.2f}".format(ranked[i][0],ranked[i][1],ranked[i][1]/len(investorAndCompanyNames[ranked[i][0]])))
        pass"""
    return ranked

    
#Main Function
if __name__ == '__main__':
	extractData('https://gist.githubusercontent.com/murtuzakz/4bd887712703ff14c9b0f7c18229b332/raw/d0dd1c59016e2488dcbe0c8e710a1c5df9c3672e/season7.json')
	tupleInvNameAndCompName = getListOfInvestorAndCompanyNames()
	tupleCompNameAndValue = getListOfComapnyNameAndCompanyValue()
	tupleInvNameAndAmountInvested = getListOfInvestorAndInvestedAmount()
