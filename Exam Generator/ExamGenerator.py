#!/usr/bin/env python

import random
import pyqrcode
import copy
import simplecrypt
import os
import argparse
from fpdf import FPDF
from binascii import hexlify

class GenerateExam(object):
    def __init__(self, num_questions, num_versions):
        self.num_questions = num_questions
        self.num_versions = num_versions
        self.question_list = []
        self.question_dict = {0:'a',1:'b',2:'c',3:'d'}

    def input_q_and_a(self):
        for i in range(self.num_questions):
            question = input('Please type question {0}.'.format(i + 1))
            answer = input('Please type the answer.')
            filler_0 = input('Please type filler one.')
            filler_1 = input('Please type filler two.')
            filler_2 = input('Please type filler three.')
            
            self.answer_list = ['&3#' + answer, filler_0, filler_1, filler_2]# obviously exam answers cannot contain string &3# -- this needs to be updated!
            self.question_list.append([question, self.answer_list])
            self.answer_list = []
            
    def build_exam(self):
        for i in range(self.num_versions):
            self.new_question_list = copy.deepcopy(self.question_list)
            for m in range(len(self.new_question_list)):
                random.shuffle(self.new_question_list[m][1])
            random.shuffle(self.new_question_list)
            
            plain_text_answer_string = ''
            for j in range(len(self.new_question_list)):
                plain_text_answer_string = plain_text_answer_string + str(j + 1)
                for k in range(len(self.new_question_list[j][1])):
                    if self.new_question_list[j][1][k][:3] == '&3#':
                        self.new_question_list[j][1][k] = self.new_question_list[j][1][k][3:]
                        plain_text_answer_string = plain_text_answer_string + self.question_dict[k] + 'x'
                        
            cipher_text = hexlify(simplecrypt.encrypt('ChangeThisKey!',plain_text_answer_string))# encrypt answer string and convert binary to hex before making qr code
            qr_code = pyqrcode.create(cipher_text, error='M', version=14, mode='binary')# generate QR code
            qr_code.png('qrcode{0}.png'.format(i), scale=2, module_color=[0, 0, 0, 0], background=[0xff, 0xff, 0xff])# save as PNG  
            pdf=FPDF()
            pdf.alias_nb_pages()
            pdf.add_page()
            pdf.set_font('Arial','B',12)
            pdf.cell(190, 10, ' Name:______________________________                              Group:_____________', 1, 1, 'L')
            pdf.ln(75)
            pdf.image('qrcode{0}.png'.format(i), 7, 24, 50)
            pdf.image('gradebox.png', 180, 24, 15)
            pdf.image('grid.png', 60, 22, 110)
            pdf.set_font('Times', '', 8)
            for j in range(len(self.new_question_list)):
                    pdf.multi_cell(0, 5, str(j + 1) + '. ' + self.new_question_list[j][0], 0, 1)
                    pdf.multi_cell(0, 7, 'A. ' + self.new_question_list[j][1][0] + '          '\
                             'B. ' + self.new_question_list[j][1][1] + '          '\
                             'C. ' + self.new_question_list[j][1][2] + '          '\
                             'D. ' + self.new_question_list[j][1][3] + '          ', 0, 1
                             )
            pdf.output('exam{0}.pdf'.format(i), 'F')            
            
    def cleanup(self):
        for i in range(self.num_versions):
            try:
                os.remove('qrcode{0}.png'.format(i))
            except:
                pass
            
    def run(self):
        self.input_q_and_a()
        self.build_exam()
        self.cleanup()

##if __name__ == "__main__":
##    parser = argparse.ArgumentParser(description="ExamGenerator.py v1.0 Generate randomized multiple choice exams for grading with camera. (c) j.j. gerschler")
##    parser.add_argument("-q", "--questions", help="Number of questions per exam.")
##    parser.add_argument("-v", "--versions", help="Number of versions of exam.")
##
##    args = parser.parse_args()
##
##    new_exam = GenerateExam(int(args.questions), int(args.versions))
##    new_exam.run()
##
##    print("")
##    print("Done.")

new_exam = GenerateExam(3, 1)
new_exam.run()
