import os
from re import search
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import TextAreaField,SubmitField
import spacy
from collections import OrderedDict
import re
import contractions

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'this_should_be_configured')

# Count part
class myForm(FlaskForm):
    message= TextAreaField("Input message",render_kw={'style':'width: 500px;height: 200px; overflow: auto; padding:5px 5px 5px 5px'}) 
    submit= SubmitField("Send",render_kw={'style':'width: 50px;height: 30px;'})

@app.route('/',methods=["GET","POST"])
def home():
    form=myForm()
    sp = spacy.load('en_core_web_sm')
    message = False
    Pmessage = False
    Tag= False
    nTag = False
    fWord= False
    fWordSort = False
    nkWord= False
    cWord= False
    cSent= False
    cAlp = False
    cAlpNoSp = False
    cPar = False   
    if form.validate_on_submit()and form.submit.data:
        message=form.message.data
        form.message.data=""
        # ประเภทคำ        
        Pmessage = contractions.fix(message)
        words = [x.strip("\"\.,()[@_!#$%^&*()<>?/\|}{~:]=+-'‘’“”") for x in Pmessage.split()]
        words = " ".join(words)
        words = sp(words)
        Tag={}
        for i in words:
            Tag[i]=spacy.explain(i.pos_)
        Awords=[]
        for i in Tag:
            Awords.append(str(i))
        words = " ".join(Awords)
        # คำไม่ซ้ำและความถี่คำ
        def word_count(str):
            counts = dict()
            sword = [x.strip("\".,()[@_!#$%^&*()<>?/\|}{~:]=+-'‘’“”") for x in str.split()]    
            for word in sword:
                if word in counts:
                    counts[word] += 1
                else:
                    counts[word] = 1
            return counts
        fWord=(word_count(str(words).lower()))
        fWordSort=OrderedDict(sorted(fWord.items()))
        # คำทั้งหมด
        cWord=len(words.split())
        # นับประโยค
        cSent=message.count(".")
        if Tag != False:
            nTag=len(Tag)      
        if fWord != False:
            nkWord=len(fWord)
        cAlp=len(message)
        cAlpNoSp=len(message)-message.count(' ')
        cPar=message.count('\n')+1
    return render_template('base.html',form=form,message=message,Pmessage=Pmessage,Tag=Tag,nTag=nTag,fWord=fWord,fWordSort=fWordSort,nkWord=nkWord,cWord=cWord,cSent=cSent,cAlp=cAlp,cAlpNoSp=cAlpNoSp,cPar=cPar)

# Duplicate part
class dupForm(FlaskForm):
    input1= TextAreaField("Input message 1",render_kw={'style':'width: 500px;height: 100px; overflow: auto; padding:5px 5px 5px 5px'}) 
    input2= TextAreaField("Input message 2",render_kw={'style':'width: 500px;height: 100px; overflow: auto; padding:5px 5px 5px 5px'}) 
    submit2= SubmitField("Send",render_kw={'style':'width: 50px;height: 30px;'})

@app.route('/duplicate/',methods=["GET","POST"])
def duplicate():
    form2=dupForm()
    input1 = False
    input2 = False
    mes1 = False
    mes2 = False
    mes1L = False
    mes2L = False
    Ames= False
    if form2.validate_on_submit()and form2.submit2.data:
        input1=form2.input1.data
        input2=form2.input2.data
        form2.input1.data=""
        form2.input2.data=""
        if (input1!="" and input2!=""):
            mes1 = [x.strip("\"\.,()[@_!#$%^&*()<>?/\|}{~:]=+-'‘’“”") for x in input1.split()]
            mes1 = " ".join(mes1)
            mes2 = [x.strip("\"\.,()[@_!#$%^&*()<>?/\|}{~:]=+-'‘’“”") for x in input2.split()]
            mes2 = " ".join(mes2)
            mes1=(mes1.split("."))
            mes2=(mes2.split("."))
            mes1=" . ".join(mes1)
            mes2=" . ".join(mes2)
            mes1=mes1.split()
            mes2=mes2.split()
            mes1L=len(mes1)
            mes2L=len(mes2)
            Ames=[]
            if (mes2L==1 or mes1L==1):
                if (mes1L>=mes2L):
                    for i in mes1:
                        mes2="".join(mes2)
                        if(i==mes2):
                            Ames.append("*DUPLICATE*")
                        else:
                            Ames.append(i)
                else:
                    for i in mes2:
                        mes1="".join(mes1)
                        if(i==mes1):
                            Ames.append("*DUPLICATE*")
                        else:
                            Ames.append(i)
            else:
                if (mes1L>=mes2L):
                    mes1=" ".join(mes1)
                    mes2=" ".join(mes2)
                    mes1=mes1.split(mes2)
                    mes1=("*DUPLICATE*").join(mes1)
                    mes1=mes1.split()
                    mes2=" ".join(mes2)
                else:
                    mes1=" ".join(mes1)
                    mes2=" ".join(mes2)
                    mes2=mes2.split(mes1)
                    mes2=("*DUPLICATE*").join(mes2)
                    mes2=mes2.split()
                    mes1=" ".join(mes1)

    return render_template('duplicate.html',form2=form2,input1=input1,input2=input2,mes1=mes1,mes2=mes2,mes1L=mes1L,mes2L=mes2L,Ames=Ames)

# About us part
@app.route('/about')
def about():
    """Render the website's about page."""
    return render_template('about.html')



# Fix bugs part
@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
