import os
import runpy
import sys
from time import time 
from os import walk
import subprocess

baseball = './20_newsgroups/rec.sport.baseball'
baseballNames = next(walk(baseball), (None, None, []))[2]  # [] if no file
baseballNames.sort()

hardware = './20_newsgroups/comp.sys.mac.hardware'
hardwareNames = next(walk(hardware), (None, None, []))[2]  # [] if no file
hardwareNames.sort()

print(hardwareNames)

os.environ['PYTHONINSPECT'] = 'True'
t=time()
argv=sys.argv[1:len(sys.argv)]

sys.argv = ['--index', '20news_letter', '--file', './20_newsgroups/rec.sport.baseball/0009000','./20_newsgroups/comp.sys.mac.hardware/0003009']
argv = sys.argv
runpy.run_path('./TFIDFViewer.py', run_name='__main__')

nameBaseball = '0009000'
nameHard = '0003009'
#os.system('python3 TFIDFViewer.py --index 20news_letter --file ./20_newsgroups/rec.sport.baseball/'+ nameBaseball +' ./20_newsgroups/comp.sys.mac.hardware/'+ nameHard)
#os.system('python3 TFIDFViewer.py --index 20news_letter --file ./20_newsgroups/rec.sport.baseball/'+ bNames +' ./20_newsgroups/comp.sys.mac.hardware/'+ hNames)
#subprocess.call([sys.executable, 'TFIDFViewer.py ', '--index', '20news_letter', '--file', './20_newsgroups/rec.sport.baseball/0009000','./20_newsgroups/comp.sys.mac.hardware/0003009'])

#for bNames in baseballNames:
 #   for hNames in hardwareNames:
  #      runpy.run_path('./TFIDFViewer.py',  run_name='__main__')
   #     break
exit()

