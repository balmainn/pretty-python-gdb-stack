from pygments import highlight
from pygments.style import Style
from pygments.token import *
from pygments.lexers.c_cpp import CLexer
from pygments.formatters import Terminal256Formatter, HtmlFormatter
import sys 
import re
fname = "simple_program.c"
with open(fname,'r') as f:
    code = f.read()
lexer = CLexer() 
s = 'vs'
formatter = HtmlFormatter(style=s)
result = highlight(code, lexer, formatter)
css = formatter.get_style_defs()


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
# i = 0
# for c,color in zip(classesList,colorsList):
#     tmp = ""
#     if notFirstRun:
#         result = res      
#     #c = classesList[i]
#     #color = colorsList[i]
#     #print(f"class and color : {c[:-1]}, {color}")    
#     res = re.sub(f"""<span class="{c[:-1]}">""",color,result)
#     tmp = res 
#     print (i, res)
#     #res2 = re.sub("</span>","</font>",res)
#     notFirstRun = True
#     i = i +1
#     #print(res2)
#     #print(i)
#     #res3 = re.sub("""<span class="w"> +<\/font>""","""<span> </span>""",res2)
# #print(res3)
# full  = highlight(code, lexer, formatter)
lines = result.splitlines()
ms = []
for i in range(len(lines)):
    
    line = lines[i]
    m = re.split("<span|</span>",line)
    ms.append(m)

for line in lines:
    print(line)
# i = 0
# j = 0
# for line in ms:
#     for thing in line:
#         print(thing)

# for i in range(len(ms)):
#     for j in range(len(ms[i])):
#         print(f"{i} , {j} , x{ms[i][j]}x")
        
import re 
line = """<span class="n">printf</span><span class="p">(</span><span class="s">&quot;function: %d</span><span class="se">\n</span><span class="s">&quot;</span><span class="p">,</span><span class="w"> </span><span class="n">t</span><span class="p">);</span><span class="w"></span>"""
word = re.findall(">.*<",line)
print(word)

print(css)