#Created by Jemie Effendy - 2 March 2016
# -*- coding: utf-8 -*-
import sys
import csv
import xml.etree.ElementTree

class JournalInfo:
	#Constructor
	def __init__(self, PMID, ISSN, ISSNLinking, journalYear, journalMonth, journalDay, journalTitle, isoAbbreviation, articleTitle, numberOfAuthor, lastNameFA, firstNameFA, affiliationFA, lastNameLA, firstNameLA, affiliationLA):
		self.PMID = PMID 
		self.ISSN = ISSN
		self.ISSNLinking = ISSNLinking
		self.journalYear = journalYear
		self.journalMonth = journalMonth
		self.journalDay = journalDay
		self.journalTitle = journalTitle
		self.isoAbbreviation = isoAbbreviation
		self.articleTitle = articleTitle
		self.numberOfAuthor = numberOfAuthor
		self.lastNameFA = lastNameFA
		self.firstNameFA = firstNameFA
		self.affiliationFA = affiliationFA
		self.lastNameLA = lastNameLA
		self.firstNameLA = firstNameLA
		self.affiliationLA = affiliationLA

	def changeDetailToArray(self):
		return [self.PMID, self.ISSN, self.ISSNLinking, self.journalYear, self.journalMonth, self.journalDay, self.journalTitle.encode('utf-8'), self.isoAbbreviation, self.articleTitle.encode('utf-8'), self.numberOfAuthor, self.lastNameFA.encode('utf-8'), self.firstNameFA.encode('utf-8'), self.affiliationFA.encode('utf-8'), self.lastNameLA.encode('utf-8'), self.firstNameLA.encode('utf-8'), self.affiliationLA.encode('utf-8')]


if (len(sys.argv) != 2) :
	print("Please input path to your file")
	sys.exit(0)

e = xml.etree.ElementTree.parse(sys.argv[1]).getroot()

journalInfo = [["PMID","ISSN", "ISSNLinking","Journal Publication Year", "Journal Publication Month", "Journal Publication Day", "Journal Publication Title", "ISOAbbreviation","Article Name", "Number of Author","Last Name First Author","Fore Name First Author", "Affilication First Author", "Last Name Last Author", "Fore Name Last Author", "Affiliation Last Author"]]

for pubMedArticles in e.findall('PubmedArticle'):
	PMID = ""
	ISSN = ""
	ISSNLinking = ""
	journalYear = ""
	journalMonth = ""
	journalDay = ""
	journalTitle = ""
	isoAbbreviation = ""
	articleTitle = ""
	numberOfAuthor = 0
	lastNameFA = ""
	firstNameFA = ""
	affiliationFA = ""
	lastNameLA = ""
	firstNameLA = ""
	affiliationLA = ""

	medlineCitation = pubMedArticles.find('MedlineCitation')
	article = medlineCitation.find('Article')
	journal = article.find('Journal')
	authorList = article.find('AuthorList')
	medLineJournalInfo = medlineCitation.find('MedlineJournalInfo')

	PMID = medlineCitation.find('PMID').text
	if (journal.find('ISSN') != None):
		ISSN = journal.find('ISSN').text
	if (medLineJournalInfo.find('ISSNLinking') != None):
		ISSNLinking = medLineJournalInfo.find('ISSNLinking').text
	journalYearXML = journal.find('JournalIssue').find('PubDate').find('Year')
	if (journalYearXML != None):
		journalYear = int(journalYearXML.text)
	else:
		#Handling medline date
		medlineDateXML = journal.find('JournalIssue').find('PubDate').find('MedlineDate')
		medlineDate = medlineDateXML.text.split()
		journalYear = medlineDate[0]
		if (len(medlineDate) > 1):
			journalMonth = medlineDate[1]
		if (len(medlineDate) > 2):
			journalDay=medlineDate[2]
	journalMonthXML = journal.find('JournalIssue').find('PubDate').find('Month')
	if (journalMonthXML != None):
		journalMonth = journalMonthXML.text
	journalDayXML = journal.find('JournalIssue').find('PubDate').find('Day')
	if (journalDayXML != None):
		journalDay = int(journalDayXML.text)
	journalTitle = journal.find('Title').text
	isoAbbreviation = journal.find('ISOAbbreviation').text
	articleTitle = article.find('ArticleTitle').text
	index = 0
	if (authorList != None):
		numberOfAuthor = len(authorList.findall('Author'));
		for author in authorList.findall('Author'):
			if (index == 0):
				if (author.find('LastName') != None):
					lastNameFA = author.find('LastName').text
				else:
					lastNameFA = author.find('CollectiveName').text
				if (author.find('ForeName') != None):
					firstNameFA = author.find('ForeName').text
				affiliationInfoXML = author.find('AffiliationInfo')
				if (affiliationInfoXML != None):
					affiliationFA = author.find('AffiliationInfo').find('Affiliation').text
			else:
				if (author.find('LastName') != None):
					lastNameLA = author.find('LastName').text
				else:
					lastNameLA = author.find('CollectiveName').text
				if (author.find('ForeName') != None):
					firstNameLA = author.find('ForeName').text
				affiliationInfoXML = author.find('AffiliationInfo')
				if (affiliationInfoXML != None):
					affiliationLA = author.find('AffiliationInfo').find('Affiliation').text
			index = index + 1
	journalObj = JournalInfo(PMID, ISSN, ISSNLinking, journalYear, journalMonth, journalDay, journalTitle, isoAbbreviation, articleTitle, numberOfAuthor,lastNameFA, firstNameFA, affiliationFA, lastNameLA, firstNameLA, affiliationLA)
	journalInfo.append(journalObj.changeDetailToArray())

with open('output.csv','wb') as csvfile:
	spamwriter = csv.writer(csvfile)
	for journal in  journalInfo:
		print(journal);
		spamwriter.writerow(journal)
