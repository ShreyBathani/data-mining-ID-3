# app/views.py

from flask import Flask, render_template, request

from app import app
import math

@app.route('/')
def show_template():
    return render_template("template.html", data = '', l=[], len=0, len1=0, gain=dict(), lgain=0, entr=dict(), lentr=0, check=False)


@app.route('/', methods=['POST'])
def getdata():
    data = request.form['textarea_data']
    l = []
    strn = ""
    for ch in data:
        if ch != "\n":
            strn += ch
        else:
            strn = strn.strip()
            if(len(strn.split(';'))>1):
                l.append(strn.split(';'))
            elif(len(strn.split(','))>1): 
                l.append(strn.split(','))
            elif(len(strn.split(' '))>1): 
                l.append(strn.split(' '))
            strn = ""
    strn = strn.strip()
    if(len(strn.split(';'))>1):
        l.append(strn.split(';'))
    elif(len(strn.split(','))>1): 
        l.append(strn.split(','))
    elif(len(strn.split(' '))>1): 
        l.append(strn.split(' '))
    
    flag=0
    for i in range(1,len(l)):
        if (len(l[i])!=len(l[0])):
            flag=1
            break

    if (len(l)<3):
        return render_template("template.html", data = 'Enter Valid Data!!', l=[], len=0, len1=0, gain=dict(), lgain=0, entr=dict(), lentr=0, check=False)
    elif (flag==1):
        return render_template("template.html", data = 'Enter Valid Data!!', l=[], len=0, len1=0, gain=dict(), lgain=0, entr=dict(), lentr=0, check=False)
    # entropy of class attribute
    #   -a         |   a   |     -b         |   b   |
    # ------- log2 |-------| + ------- log2 |-------|
    #  a + b       | a + b |    a + b       | a + b |
    else:
        cal = dict()
        for i in range(1,len(l)):
            if l[i][-1] not in cal:
                cal[l[i][-1]] = 1
            else:
                cal[l[i][-1]] += 1

        class_attr = [(k, v) for k, v in cal.items()]

        main_class_ent = 0  
        main_denom = class_attr[0][1]
        if len(class_attr) == 2 : 
            main_denom += class_attr[1][1]
        for tuple in class_attr:
            main_class_ent = main_class_ent + (-tuple[1]/main_denom)*math.log2(tuple[1]/main_denom)

        gain = dict()
        entr = dict()

        for i in range(len(l[0])-1):
            cal = dict()
            for j in range(1,len(l)):
                if l[j][i] not in cal:
                    cal[l[j][i]]  = dict()
                    if l[j][-1] not in cal[l[j][i]]:
                        cal[l[j][i]][l[j][-1]] = 1
                    else:
                        cal[l[j][i]][l[j][-1]] += 1 
                else:
                    if l[j][-1] not in cal[l[j][i]]:
                        cal[l[j][i]][l[j][-1]] = 1
                    else:
                        cal[l[j][i]][l[j][-1]] += 1

            info_gain = dict()
            ent_of_attr = 0

            for (key,value)in cal.items():
                class_attr = [(k, v) for k, v in value.items()]
                class_ent = 0
                denom = class_attr[0][1]  
                if len(class_attr) == 2:
                    denom += class_attr[1][1]
                for tuple in class_attr:
                    class_ent = class_ent + (-tuple[1]/denom)*math.log2(tuple[1]/denom)
                info_gain[key] = class_ent
                
                # entropy of attribute  E(pi+ni)/(main_denom)*(info_gain[i]) , (pi+ni) = denom
                ent_of_attr = ent_of_attr + (denom/main_denom)*class_ent
    
            gain[l[0][i]] = float(str(main_class_ent - ent_of_attr)[0:9])
            entr[l[0][i]] = float(str(ent_of_attr)[0:9])
        return render_template("template.html", data = '', l=l, len=len(l[0]), len1=len(l), gain=gain,lgain=len(gain), entr=entr, lentr=len(entr), check=True)