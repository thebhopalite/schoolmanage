from flask import *
from flaskext.mysql import MySQL
mysql=MySQL()
#mysql=connection()

myapp=Flask(__name__)

mymarks=Blueprint('mymarks',__name__)

myapp.config['MYSQL_DATABASE_USER']='root'
myapp.config['MYSQL_DATABASE_PASSWORD']=''
myapp.config['MYSQL_DATABASE_HOST']='localhost'
myapp.config['MYSQL_DATABASE_DB']='school_db'

mysql.init_app(myapp)

def division(percent):
    if(percent>=60):
        return("First Division")
    elif(percent>=45):
        return("Second Division")
    elif(percent>=33):
        return("Third Division")
    else:
        return("Fail")
def grade(percent):
    if(percent>=90):
        return "A+"
    elif(percent>=80):
        return "A"
    elif(percent>=70):
        return "B+"
    elif(percent>=60):
        return "B"
    elif(percent>=50):
        return "C+"
    elif(percent>=40):
        return "C"
    elif(percent>=33):
        return "D"
    else:
        return "F"


@mymarks.route('/marksEntry')
def marksEntry():
    return render_template('markEntry.html')

@mymarks.route('/getStudent',methods=['POST'])
def getStudent():
    sclass=request.form['sclass']
    section=request.form['section']
    session=request.form['session']
    exam=request.form['exam']
    info=[sclass,section,session,sclass,section,session,exam]
    mycon=mysql.connect()
    mycur=mycon.cursor()
    mycur.execute("select enroll,concat(fname,' ',lname),sclass,section,session from student where sclass=%s and section=%s and session=%s and status='pursing' and enroll NOT IN (select enroll from one_to_five WHERE sclass=%s and section=%s and session=%s and exam=%s)",info)
    info.append(exam)
    students=mycur.fetchall()
    return render_template('markEntry.html',students=students,info=info)


@mymarks.route('/submitone_to_five',methods=['POST'])
def submitone_to_five():
    flag=0
    data = [request.form['enroll'],
        request.form['session'],
        request.form['sclass'],
        request.form['section'],
        request.form['exam'],
        request.form['math'],
        request.form['english'],
        request.form['hindi'],
        request.form['evs']]

    subjects=[int(request.form['math'])+int(request.form['english'])+int(request.form['hindi'])+int(request.form['evs'])]
    for per in subjects:
        if(int(per)<33):
            flag=1
    total=sum(subjects)
    percent=total/4
    if(flag==1):
        div="--"
        result="Fail"
    else:
        div=division(percent)
        result="Pass"
        grad=grade(percent)
    data.append(total)
    data.append(percent)
    data.append(div)
    data.append(result)
    data.append(grad)
    mycon = mysql.connect()
    mycur = mycon.cursor()
    mycur.execute("INSERT INTO `one_to_five`(`enroll`,`session`,`sclass`,`section`,`exam`,`math`,`english`,`hindi`,`evs`,`total`,`percent`,`division`,`result`,`grade`)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
        data)
    return "Done"

@mymarks.route('/submitsix_to_eight',methods=['POST'])
def submitsix_to_eight():
    flag=0
    data = [request.form['enroll'],
        request.form['session'],
        request.form['sclass'],
        request.form['section'],
        request.form['exam'],
        request.form['math'],
        request.form['english'],
        request.form['hindi'],
        request.form['social'],
        request.form['science']]
    subjects=[int(request.form['math'])+int(request.form['english'])+int(request.form['hindi'])+int(request.form['social'])+int(request.form['science'])]
    for per in subjects:
        if(int(per)<33):
            flag=1
    total=sum(subjects)
    percent=total/5
    if(flag==1):
        div="--"
        result="Fail"
    else:
        div=division(percent)
        result="Pass"
        grad=grade(percent)

    data.append(total)
    data.append(percent)
    data.append(div)
    data.append(result)
    data.append(grad)
    mycon = mysql.connect()
    mycur = mycon.cursor()
    mycur.execute("INSERT INTO `six_to_eight`(`enroll`,`session`,`sclass`,`section`,`exam`,`math`,`english`,`hindi`,`social`,`science`,`total`,`percent`,`division`,`result`,`grade`)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
        data)
    return "Done"

@mymarks.route('/submitnine_to_ten',methods=['POST'])
def submitnine_to_ten():
    flag=0
    data = [request.form['enroll'],
        request.form['session'],
        request.form['sclass'],
        request.form['section'],
        request.form['exam'],
        request.form['math'],
        request.form['english'],
        request.form['hindi'],
        request.form['social'],
        request.form['science'],
            request.form['sciencePr']]
    subjects=[int(request.form['math'])+int(request.form['english'])+int(request.form['hindi'])+int(request.form['social'])+int(request.form['science'])]
    for per in subjects:
        if(int(per)<33):
            flag=1
    if(int(request.form['sciencePr'])<8):
        flag=1
    total=(sum(subjects)+int(request.form['sciencePr']))
    percent=total/5
    if(flag==1):
        div="--"
        result="Fail"
    else:
        div=division(percent)
        result="Pass"
        grad=grade(percent)

    data.append(total)
    data.append(percent)
    data.append(div)
    data.append(result)
    data.append(grad)
    mycon = mysql.connect()
    mycur = mycon.cursor()
    mycur.execute("INSERT INTO `nine_to_ten`(`enroll`,`session`,`sclass`,`section`,`exam`,`math`,`english`,`hindi`,`social`,`science`,`sciencePr`,`total`,`percent`,`division`,`result`,`grade`)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
        data)
    return "Done"


@mymarks.route('/submittedmarks')
def submittedmarks():
        return render_template("submittedmarks.html")



@mymarks.route('/marksentry',methods=['POST'])
def marksentry():
    sclass = request.form['sclass']
    section = request.form['section']
    session = request.form['session']
    exam = request.form['exam']
    info = [sclass, section, session, sclass, section, session, exam]
    data=[sclass,section]
    mycon = mysql.connect()
    mycur = mycon.cursor()
    if(sclass=='I' or sclass=='II' or sclass=='III' or sclass=='IV' or sclass=='V'):
        mycur.execute("select * from one_to_five where sclass=%s and section=%s",data)
        students = mycur.fetchall()
        return render_template("submittedmarks.html", students=students, info=info)

    elif(sclass=='VI' or sclass=='VII' or sclass=='VIII'):
        mycur.execute("select * from six_to_eight where sclass=%s and section=%s", data)
        students = mycur.fetchall()
        return render_template("submittedmarks1.html", students=students, info=info)
    else:
        mycur.execute("select * from nine_to_ten where sclass=%s and section=%s", data)
        students = mycur.fetchall()
        return render_template("submittedmarks2.html", students=students, info=info)
    return("None")


@mymarks.route('/marksheetprint',methods=['GET'])
def marksheetprint():
    enroll = request.args.get('enroll')
    exam = request.args.get('exam')
    session = request.args.get('session')
    sclass = request.args.get('sclass')
    mycon = mysql.connect()
    mycur = mycon.cursor()
    mycur.execute("select * from student where enroll=%s"%enroll)
    data = mycur.fetchall()
    details=[enroll,sclass,session,exam]
    if(sclass=='I' or sclass=='II' or sclass=='III' or sclass=='IV' or sclass=='V'):
        mycur.execute("select * from one_to_five where enroll=%s and sclass=%s and session=%s and exam=%s",details)
        marks = mycur.fetchall()
        return render_template('marksheetprint.html', info=data, marks=marks)
    elif(sclass=='VI' or sclass=='VII' or sclass=='VIII'):
        mycur.execute("select * from six_to_eight where enroll=%s and sclass=%s and session=%s and exam=%s", details)
        marks = mycur.fetchall()
        return render_template('marksheetprint1.html', info=data, marks=marks)
        #return(str(data))
    else:
        mycur.execute("select * from nine_to_ten where enroll=%s and sclass=%s and session=%s and exam=%s", details)
        marks = mycur.fetchall()
        return render_template('marksheetprint2.html', info=data, marks=marks)
    return("none")

@mymarks.route('/profileprint',methods=['GET'])
def profileprint():
    enroll = request.args.get('enroll')
    sclass = request.args.get('sclass')
    mycon = mysql.connect()
    mycur = mycon.cursor()
    details = [enroll, sclass]
    mycur.execute("select * from student where enroll=%s and sclass=%s", details)
    data = mycur.fetchall()
    return render_template('profileprint.html', info=data)

@mymarks.route('/printfeesreceipt',methods=['GET'])
def printfeesreceipt():
    receipt = request.args.get('receiptno')
    mycon = mysql.connect()
    mycur = mycon.cursor()
    mycur.execute("select * from fees where receipt=%s",receipt)
    data= mycur.fetchall()   
    return render_template('printfeesreceipt.html',info=data)
