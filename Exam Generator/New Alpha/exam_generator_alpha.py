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
                for k in range(len(self.new_question_list[j][1])):
                    if self.new_question_list[j][1][k][:3] == '&3#':
                        self.new_question_list[j][1][k] = self.new_question_list[j][1][k][3:]
                        plain_text_answer_string += self.question_dict[k]
                        
            cipher_text = hexlify(simplecrypt.encrypt('ChangeThisKey!', plain_text_answer_string))
            cipher_text = cipher_text.decode('ascii').upper()
            qr_code = pyqrcode.create(cipher_text, error='M', version=8, mode='alphanumeric')# generate QR code
            qr_code.png('qrcode{0}.png'.format(i), scale=2, module_color=[0, 0, 0, 0], background=[0xff, 0xff, 0xff])# save as PNG
            
            pdf=FPDF()
            pdf.alias_nb_pages()
            pdf.set_left_margin(20)
            pdf.set_right_margin(20)
            pdf.set_top_margin(20)
            pdf.add_page()
            pdf.set_font('Arial','B',12)
            pdf.cell(0, 10, ' Name:______________________________                               Group:_____________', 1, 1, 'L')
            pdf.ln(70)
            pdf.image('qrcode{0}.png'.format(i), 30, 50)
            pdf.image('grid.png', 69, 32, 110)
            pdf.set_font('Times', '', 8)
            for j in range(len(self.new_question_list)):
                    pdf.multi_cell(0, 5, str(j + 1) + '. ' +
                                   self.new_question_list[j][0], 0, 1)
                    pdf.multi_cell(0, 5, 'A. {0}         B. {1}         C. {2}         D. {3}'.format(self.new_question_list[j][1][0],
                                                                                                      self.new_question_list[j][1][1],
                                                                                                      self.new_question_list[j][1][2],
                                                                                                      self.new_question_list[j][1][3], 0, 1))
            pdf.output('exam{0}.pdf'.format(i), 'F')            
            
    def cleanup(self):
        for i in range(self.num_versions):
            try:
                os.remove('qrcode{0}.png'.format(i))
            except:
                print("Can't remove png files.")
            
    def run(self):
        self.input_q_and_a()
        self.build_exam()
        self.cleanup()

# uncomment below to enable command line interface                                   

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

new_exam = GenerateExam(10, 2)# number of questions, number of versions
new_exam.run()
