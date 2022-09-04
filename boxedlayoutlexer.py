from pygments import highlight
from pygments.style import Style
from pygments.token import *
from pygments.lexers.c_cpp import CLexer
from pygments.formatters import Terminal256Formatter, HtmlFormatter
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import *
import sys


# # Subclass QMainWindow to customize your application's main window


from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton

#for l in lines:
#     print(l)
import re
class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        
            #styles ['default', 'emacs', 'friendly', 'friendly_grayscale', 'colorful', 'autumn', 
            # 'murphy', 'manni', 'material', 'monokai', 'perldoc', 'pastie', 'borland', 'trac', 
            # 'native', 'fruity', 'bw', 'vim', 'vs', 'tango', 'rrt', 'xcode', 'igor', 
            # 'paraiso-light', 'paraiso-dark', 'lovelace', 'algol', 'algol_nu', 'arduino', 
            # 'rainbow_dash', 'abap', 'solarized-dark', 'solarized-light', 'sas', 'stata', 
            # 'stata-light', 'stata-dark', 'inkpot', 'zenburn', 'gruvbox-dark', 'gruvbox-light', 
            # 'dracula', 'one-dark', 'lilypond']
        s = 'vs'
        
        fname = "simple_program.c"
        self.setWindowTitle(f"{fname} Code Window")
        with open(fname,'r') as f:
            code = f.read()
        lexer = CLexer() 
        
        formatter = HtmlFormatter(style=s)
        result = highlight(code, lexer, formatter)
        print(result)
        css = formatter.get_style_defs()
        self.layout = QGridLayout() 
        
        text2 = [] 
        
     
        lines = css.splitlines()
     
        classesList = []
        colorsList = []
        print (result)
        for line in lines:
    #if i > 5:
            color = "<font"
            m = re.split("{|}",line)
            print(line)
            print(m[0][1:])
            print(m[1], m[1][1])
            if(m[1][1]=='f'):
                colorsList.append("")
            else:
                cout = re.sub(': ',"=",m[1])
                color = color+ cout[:-1] +">"
                colorsList.append(color)
            classesList.append(m[0][1:])
            #i = i + 1
        classesList.append("w")
        colorsList.append("<font color=#000000>")
        notFirstRun = False
        for c,color in zip(classesList,colorsList):
            if notFirstRun:
                result = res3
            #c = classesList[i]
            #color = colorsList[i]
            print(f"class and color : {c[:-1]}, {color}")    
            res = re.sub(f"""<span class="{c[:-1]}">""",color,result)
            res2 = re.sub("</span>","</font>",res)
            notFirstRun = True
            #print(res2)
            #print(i)
            res3 = res2
            #res3 = re.sub("""<span class="w"> +<\/font>""","""  """,res2)
            #res4 = re.sub(f"""<span class="n">""","xxxxxxxxxxx<font>",res3)
            breaktext = QLabel("")
        for line in res3.splitlines():
            label = QLabel("")
            label.setText("\n")
            text2.append(label)
            print(line)
        #-1 gets rid of the </pre></div> artifact at the end of the list
        # for i in range(len(text2)-1):
        #     self.layout.addWidget(text2[i])
        label2 = QLabel("")    
        label2.setText(res3)
        #self.layout.addWidget(label2,1,1)
        breaknum =14
        bst = ""
        for i in range(len(res3.splitlines())):
            if(i == breaknum):
                bst = bst + f"{i}--->\n"
                
            else:
                bst=bst+f"{i}\n"
        label1 = QLabel("")
        label1.setText(bst)        
        self.layout.addWidget(label1,0,0)
        self.layout.addWidget(label2,0,1)
        #text2.setText(res2)
        
        #text1.setStyleSheet("color:red")
        #text2.setStyleSheet(cssStyle)
        # layout.addWidget(text1)
        # layout.addWidget(text2)

        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)


#print(result)

app = QApplication(sys.argv)
#app.setStyleSheet(css)
window = MainWindow()
window.show()

app.exec()

#print("~~~~~~")
#print(result)
import re

# fc = """<font color="#000080">"""
# res = re.sub("""<span class="cp">""",fc,result)
# res2 = re.sub("</span>","</font>",res)
#print(res2)


# fname = "simple_program.c"
# with open(fname,'r') as f:
#     code = f.read()
# lexer = CLexer() 
# s = 'vs'
# formatter = HtmlFormatter(style=s)
# result = highlight(code, lexer, formatter)
# lines = result.splitlines()
# uniqueCtr = 0
# outarr = []
# for i in range(len(lines)):
#     print(lines[i])
#     st = ""
#     for j in range(len(lines[i])):
#         st = st+lines[i][j]
#         if(st == "<span"):
#             uniqueSpanNumber = 0
#             st = f"<span{uniqueCtr}"
#             pairedSpan = ""
#             rep = lines[i][j].replace("</span>",f"</span{uniqueCtr}",uniqueCtr)
#             rep = lines[i][j].replace("</span>",f"</span{uniqueCtr}",uniqueCtr-1)
#             uniqueCtr=uniqueCtr+1
#             print("REP:",rep)
            
#             # for k in range(len(lines[i])+j+1):
                
#             #     if lines[i][k] == "<":
#             #         lines[i][k:7] = f"</span{uniqueCtr}"
#             #         uniqueCtr=uniqueCtr+1
#     outarr.append(st)
# for o in outarr:
#     print(o)    