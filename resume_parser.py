### import our libraries
##importing our libraries
import pandas as pd
import docx2pdf
from docx2pdf import convert
import PyPDF2
import nltk
from nltk import ne_chunk,pos_tag,word_tokenize
from nltk.tree import Tree
import pandas 
import phonenumbers
import re
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')
stopwords=set(stopwords.words('english'))
import nltk


                        # OUR CODE START HERE
#parsing our pdf

path=str(input('give me the path of your resume:'))
if path[-3:]!='pdf':
    print("we are converting your file")
    convert(path,r'C:\Users\asus\Documents\new_file.pdf')
    path=r'C:\Users\asus\Documents\new_file.pdf'
def parsing_pdf(path):
    file =open(path,'rb')
    pdf_reader=PyPDF2.PdfFileReader(file)
    global clear_text
    clear_text=''
    global text
    text=""
    num_of_pages=pdf_reader.numPages
    for i in range(num_of_pages):
        text+= pdf_reader.getPage(i).extractText()+"  " # return a text format of the pdf resume
    text=text.replace('\n', ' ')
    filtered_words=[word for word in word_tokenize(text) if word not in stopwords]
    clear_text=''
    for word in filtered_words:
            clear_text=clear_text+word +' '
    text=clear_text
    
                
    
parsing_pdf(path)

    
        
def extracting_names(text):
    chunks=ne_chunk(pos_tag(word_tokenize(text))) 
    global names
    names=[]                                                         
    for chunk in chunks:
        if type(chunk)==Tree and chunk.label()=='PERSON':
                for leaf in chunk.leaves():
                    names.append(leaf[0])               #return a list that contain potential name of person  
                    
                    
def extracting_email(text):
    reg_exps=['\S+ @ gmail.com']
    for reg_exp in reg_exps:  
        global email
        email =re.findall(reg_exp,text)                 
extracting_email(text)
extracting_names(text)


#we will try to find the exacte name of the person  
user_name=email[0][:email[0].index('@')]
real_name=" "
for name in names:
    if name.lower() in user_name:
        real_name+=name + " "
        
        
    
def extracting_adress(text):
    data=pd.read_csv(r"C:\Users\asus\Downloads\ma.csv")
    df_data=pd.DataFrame(data)
    for citi in df_data['city']:
        if citi  in text:
            our_city=citi
            break
        else:
            our_city=""
    if our_city!="":
        numbers=[]
        for word in pos_tag(word_tokenize(text)):
            if word[1]=='CD' and our_city in text[text.index(word[0]):]:
                numbers.append(word[0])
        global adress
        adress=""
        for item in numbers:
            our_substring=text[text.index(item):text.index(item)+30]
            if our_city in our_substring:          
                adress+=our_substring[our_substring.index(item):our_substring.index(our_city)+1+len(our_city)]+""
                break 
    else:
        print('no morrocan address')
        adress=''
       
        
def extracting_phonenumber(text):
    global phone_number
    phone_number=[]
    if '06' in text:
        phone_number.append(text[text.index('06'):text.index('06')+14])
    else:
        phone_number.append('none')

            
extracting_phonenumber(text)
    
        
def extracting_education(text):
    chunks=ne_chunk(pos_tag(word_tokenize(text))) 
    reserved_names=['School','University','College','Baccalaureat','Master','Licence','Doctorat']
    global names
    names=[]
    global institution
    institution=[]
    global level
    level=[]
    for chunk in chunks:
        if type(chunk)==Tree and chunk.label()=='ORGANIZATION':
                for leaf in chunk.leaves():
                    names.append(leaf[0])    ##it include the names of organization that can be a name institute
    for name in names:
        if name in reserved_names :
            institution.append(text[text.index(name):text.index(name)+len(name)+30])
    for name in reserved_names:
        if name in text and name not in institution:
            level.append(text[text.index(name):text.index(name)+len(name)+30])   
            
            
def extracting_experience(text):
    job_title=['Team_Leader','Manager','Assistant_Manager','Executive','Student','Director','Developer''Coordinator','Administrator',
               'Controller','Officer','Organizer','Supervisor','Superintendent',
               'Head','Overseer','Chief','Foreman','Controller','Principal','President','Lead','Intern','Engeneer']
    global experiences
    experiences=[]
    for job  in job_title:
        if job.lower() in text :
            job=job.lower()
            experiences.append(text[text.index(job):text.index(job)+len(job)])
        elif job in text:
            experiences.append(text[text.index(job):text.index(job)+len(job)])



extracting_experience(text)

            
            
            
            
            

print('PERSONAL INFORAMTIONS:')
extracting_phonenumber(text)       
extracting_adress(text)    
print('name:',real_name)
print('email address:',email[0])
print('phone_number:',phone_number[0])
print('adress:',adress)
extracting_education(text)
print('EDUCATION:')
for item in institution:
    print(institution)
for item in level:
    print(item)
extracting_experience(text)
print('EXPERIENCE:')
for item in experiences:
    print(item)



