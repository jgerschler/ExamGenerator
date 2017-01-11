#!/usr/bin/env python

import random, pyqrcode, copy, simplecrypt, os, argparse
from fpdf import FPDF
from binascii import hexlify

class generateExam(object):
    def __init__(self, numQuestions, numVersions):
        self.numQuestions = numQuestions
        self.numVersions = numVersions
        self.questionList = []
        self.questionDict = {0:'a',1:'b',2:'c',3:'d'}
        #self.answerList = []# remove if not needed

    def input_q_and_a(self):
        for i in range(self.numQuestions):
            question = raw_input('Please type question ' + str(i+1) + '.')
            answer = raw_input('Please type the answer.')
            filler1 = raw_input('Please type filler one.')
            filler2 = raw_input('Please type filler two.')
            filler3 = raw_input('Please type filler three.')
            
            self.answerList = ['&3#'+answer, filler1, filler2, filler3]# obviously exam answers cannot contain string &3# -- this needs to be updated!
            self.questionList.append([question,self.answerList])
            self.answerList = []
            
    def build_exam(self):
        for i in range(self.numVersions):
            self.newQuestionList = copy.deepcopy(self.questionList)
            for m in range(len(self.newQuestionList)):
                random.shuffle(self.newQuestionList[m][1])
            random.shuffle(self.newQuestionList)
            
            plainTextAnswerString = ''
            for j in range(len(self.newQuestionList)):
                plainTextAnswerString = plainTextAnswerString + str(j+1)
                for k in range(len(self.newQuestionList[j][1])):
                    if self.newQuestionList[j][1][k][:3] == '&3#':
                        self.newQuestionList[j][1][k] = self.newQuestionList[j][1][k][3:]
                        plainTextAnswerString = plainTextAnswerString + self.questionDict[k] + 'x'
                        
            cipherText = hexlify(simplecrypt.encrypt('ChangeThisKey!',plainTextAnswerString))# encrypt answer string and convert binary to hex before making qr code
            qr_code = pyqrcode.create(cipherText, error='M', version=14, mode='binary')# generate QR code
            qr_code.png('qrcode'+str(i)+'.png', scale=2, module_color=[0, 0, 0, 0], background=[0xff, 0xff, 0xff])# save as PNG  
            pdf=FPDF()
            pdf.alias_nb_pages()
            pdf.add_page()
            pdf.set_font('Arial','B',12)
            pdf.cell(190,10,' Name:______________________________         '\
            '                                      Group:_____________',1,1,'L')
            pdf.ln(75)
            pdf.image('qrcode'+str(i)+'.png',7,24,50)
            pdf.image('gradebox.png',180,24,15)
            pdf.image('grid.png',60,22,110)
            pdf.set_font('Times','',8)
            for j in range(len(self.newQuestionList)):
                    pdf.multi_cell(0,5,str(j+1)+'. '+self.newQuestionList[j][0],0,1)
                    pdf.multi_cell(0,7,'A. '+self.newQuestionList[j][1][0]+'          '\
                             'B. '+self.newQuestionList[j][1][1]+'          '\
                             'C. '+self.newQuestionList[j][1][2]+'          '\
                             'D. '+self.newQuestionList[j][1][3]+'          ',0,1
                             )
            pdf.output('exam'+str(i)+'.pdf','F')            
            
    def cleanup(self):
        for i in range(self.numVersions):
            try:
                os.remove('qrcode'+str(i)+'.png')
            except:
                pass
            
    def run(self):
        self.input_q_and_a()
        self.build_exam()
        self.cleanup()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ExamGenerator.py v1.0 Generate randomized multiple choice exams for grading with camera. (c) j.j. gerschler")
    parser.add_argument("-q", "--questions", help="Number of questions per exam.")
    parser.add_argument("-v", "--versions", help="Number of versions of exam.")

    args = parser.parse_args()

    NewExam = generateExam(int(args.questions), int(args.versions))
    NewExam.run()

    print("")
    print("Done.")
