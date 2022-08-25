from array import array
import os
from re import search
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import TextAreaField,SubmitField
import spacy
from collections import OrderedDict
from difflib import SequenceMatcher


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
    fWord= False
    fWordSort = False
    nkWord= False
    cWord= False
    cSent= False
    cAlp = False
    cAlpNoSp = False
    cPar = False
    adj = False
    adp = False
    adv = False
    aux = False
    conj = False
    cconj = False
    det = False
    intj = False
    noun = False
    num = False
    part = False
    pron = False
    propn = False
    punct = False
    sconj = False
    sym = False
    verb = False
    x = False
    Nadj = []
    Nadp = []
    Nadv = []
    Naux = []
    Nconj = []
    Ncconj = []
    Ndet = []
    Nintj = []
    Nnoun = []
    Nnum = []
    Npart = []
    Npron = []
    Npropn = []
    Npunct = []
    Nsconj = []
    Nsym = []
    Nverb = []
    Nx = []
    Nnadj = False
    Nnadp = False
    Nnadv = False
    Nnaux = False
    Nnconj = False
    Nncconj = False
    Nndet = False
    Nnintj = False
    Nnnoun = False
    Nnnum = False
    Nnpart = False
    Nnpron = False
    Nnpropn = False
    Nnpunct = False
    Nnsconj = False
    Nnsym = False
    Nnverb = False
    Nnx = False
    Fadj = 0
    Fadp = 0
    Fadv = 0
    Faux = 0
    Fconj = 0
    Fcconj = 0
    Fdet = 0
    Fintj = 0
    Fnoun = 0
    Fnum = 0
    Fpart = 0
    Fpron = 0
    Fpropn = 0
    Fpunct = 0
    Fsconj = 0
    Fsym = 0
    Fverb = 0
    Fx = 0

    if form.validate_on_submit()and form.submit.data:
        message=form.message.data
        form.message.data=""
        # ประเภทคำ        
        words=message
        sChar=["\"",",","(",")","[","@","_","!","#","$","%","^","&","*","(",")","<",">","?","/","\\","|","}","{","~",":","]","=","+","-","‘","’","“","”"]
        for i in sChar:
            words=(words.split(i))
            space=" "+i+" "
            words=space.join(words)
        words = sp(words)
        Tag = {}
        adj = {}
        adp = {}
        adv = {}
        aux = {}
        conj = {}
        cconj = {}
        det = {}
        intj = {}
        noun = {}
        num = {}
        part = {}
        pron = {}
        propn = {}
        punct = {}
        sconj = {}
        sym = {}
        verb = {}
        x = {}
        for i in words:
            Tag[i]=spacy.explain(i.pos_)
            if i.pos_.lower()=="adj":
                adj[i]=spacy.explain(i.pos_)
                Nadj.append(str(i))
            elif i.pos_.lower()=="adp":
                adp[i]=spacy.explain(i.pos_)
                Nadp.append(str(i))
            elif i.pos_.lower()=="adv":
                adv[i]=spacy.explain(i.pos_)
                Nadv.append(str(i))
            elif i.pos_.lower()=="aux":
                aux[i]=spacy.explain(i.pos_)
                Naux.append(str(i))
            elif i.pos_.lower()=="conj":
                conj[i]=spacy.explain(i.pos_)
                Nconj.append(str(i))
            elif i.pos_.lower()=="cconj":
                cconj[i]=spacy.explain(i.pos_)
                Ncconj.append(str(i))
            elif i.pos_.lower()=="det":
                det[i]=spacy.explain(i.pos_)
                Ndet.append(str(i))
            elif i.pos_.lower()=="intj":
                intj[i]=spacy.explain(i.pos_)
                Nintj.append(str(i))
            elif i.pos_.lower()=="noun":
                noun[i]=spacy.explain(i.pos_)
                Nnoun.append(str(i))
            elif i.pos_.lower()=="num":
                num[i]=spacy.explain(i.pos_)
                Nnum.append(str(i))
            elif i.pos_.lower()=="part":
                part[i]=spacy.explain(i.pos_)
                Npart.append(str(i))
            elif i.pos_.lower()=="pron":
                pron[i]=spacy.explain(i.pos_)
                Npron.append(str(i))
            elif i.pos_.lower()=="propn":
                propn[i]=spacy.explain(i.pos_)
                Npropn.append(str(i))
            elif i.pos_.lower()=="punct":
                punct[i]=spacy.explain(i.pos_)
                Npunct.append(str(i))
            elif i.pos_.lower()=="sconj":
                sconj[i]=spacy.explain(i.pos_)
                Nsconj.append(str(i))
            elif i.pos_.lower()=="sym":
                sym[i]=spacy.explain(i.pos_)
                Nsym.append(str(i))
            elif i.pos_.lower()=="verb":
                verb[i]=spacy.explain(i.pos_)
                Nverb.append(str(i))
            elif i.pos_.lower()=="x":
                x[i]=spacy.explain(i.pos_)
                Nx.append(str(i))
        Awords=[]
        for i in Tag:
            Awords.append(str(i))
        words = " ".join(Awords)
        # คำไม่ซ้ำและความถี่คำ
        def word_count(str):
            counts = dict()
            sword=str.split()
            for word in sword:
                if word in counts:
                    counts[word] += 1
                else:
                    counts[word] = 1
            return counts
        fWord=(word_count(str(words).lower()))
        fWordSort=OrderedDict(sorted(fWord.items()))
        if fWord != False:
            nkWord=len(fWordSort)
        if adj != {}:
            Nadj=" ".join(Nadj)
            Nadj=(word_count(str(Nadj).lower()))
            Nnadj=len(Nadj)
        if adp != {}:
            Nadp=" ".join(Nadp)
            Nadp=(word_count(str(Nadp).lower()))
            Nnadp=len(Nadp)
        if adv != {}:
            Nadv=" ".join(Nadv)
            Nadv=(word_count(str(Nadv).lower()))
            Nnadv=len(Nadv)
        if aux != {}:
            Naux=" ".join(Naux)
            Naux=(word_count(str(Naux).lower()))
            Nnaux=len(Naux)
        if conj != {}:
            Nconj=" ".join(Nconj)
            Nconj=(word_count(str(Nconj).lower()))
            Nnconj=len(Nconj)
        if cconj != {}:
            Ncconj=" ".join(Ncconj)
            Ncconj=(word_count(str(Ncconj).lower()))
            Nncconj=len(Ncconj)
        if det != {}:
            Ndet=" ".join(Ndet)
            Ndet=(word_count(str(Ndet).lower()))
            Nndet=len(Ndet)
        if intj != {}:
            Nintj=" ".join(Nintj)
            Nintj=(word_count(str(Nintj).lower()))
            Nnintj=len(Nintj)
        if noun != {}:
            Nnoun=" ".join(Nnoun)
            Nnoun=(word_count(str(Nnoun).lower()))
            Nnnoun=len(Nnoun)
        if num != {}:
            Nnum=" ".join(Nnum)
            Nnum=(word_count(str(Nnum).lower()))
            Nnnum=len(Nnum)
        if part != {}:
            Npart=" ".join(Npart)
            Npart=(word_count(str(Npart).lower()))
            Nnpart=len(Npart)
        if pron != {}:
            Npron=" ".join(Npron)
            Npron=(word_count(str(Npron).lower()))
            Nnpron=len(Npron)
        if propn != {}:
            Npropn=" ".join(Npropn)
            Npropn=(word_count(str(Npropn).lower()))
            Nnpropn=len(Npropn)
        if punct != {}:
            Npunct=" ".join(Npunct)
            Npunct=(word_count(str(Npunct).lower()))
            Nnpunct=len(Npunct)
        if sconj != {}:
            Nsconj=" ".join(Nsconj)
            Nsconj=(word_count(str(Nsconj).lower()))
            Nnsconj=len(Nsconj)
        if sym != {}:
            Nsym=" ".join(Nsym)
            Nsym=(word_count(str(Nsym).lower()))
            Nnsym=len(Nsym)
        if verb != {}:
            Nverb=" ".join(Nverb)
            Nverb=(word_count(str(Nverb).lower()))
            Nnverb=len(Nverb)
        if x != {}:
            Nx=" ".join(Nx)
            Nx=(word_count(str(Nx).lower()))
            Nnx=len(Nx)
        for i in Nadj:
            check=False
            for j in adj:
                if (str(j).lower()==i and check==False):
                    Fadj += int(Nadj[i])
                    check= True
        for i in Nadp:
            check=False
            for j in adp:
                if (str(j).lower()==i and check==False):
                    Fadp += int(Nadp[i])
                    check= True
        for i in Nadv:
            check=False
            for j in adv:
                if (str(j).lower()==i and check==False):
                    Fadv += int(Nadv[i])
                    check= True
        for i in Naux:
            check=False
            for j in aux:
                if (str(j).lower()==i and check==False):
                    Faux += int(Naux[i])
                    check= True
        for i in Nconj:
            check=False
            for j in conj:
                if (str(j).lower()==i and check==False):
                    Fconj += int(Nconj[i])
                    check= True
        for i in Ncconj:
            check=False
            for j in cconj:
                if (str(j).lower()==i and check==False):
                    Fcconj += int(Ncconj[i])
                    check= True
        for i in Ndet:
            check=False
            for j in det:
                if (str(j).lower()==i and check==False):
                    Fdet += int(Ndet[i])
                    check= True
        for i in Nintj:
            check=False
            for j in intj:
                if (str(j).lower()==i and check==False):
                    Fintj += int(Nintj[i])
                    check= True
        for i in Nnoun:
            check=False
            for j in noun:
                if (str(j).lower()==i and check==False):
                    Fnoun += int(Nnoun[i])
                    check= True
        for i in Nnum:
            check=False
            for j in num:
                if (str(j).lower()==i and check==False):
                    Fnum += int(Nnum[i])
                    check= True
        for i in Npart:
            check=False
            for j in part:
                if (str(j).lower()==i and check==False):
                    Fpart += int(Npart[i])
                    check= True
        for i in Npron:
            check=False
            for j in pron:
                if (str(j).lower()==i and check==False):
                    Fpron += int(Npron[i])
                    check= True
        for i in Npropn:
            check=False
            for j in propn:
                if (str(j).lower()==i and check==False):
                    Fpropn += int(Npropn[i])
                    check= True
        for i in Npunct:
            check=False
            for j in punct:
                if (str(j).lower()==i and check==False):
                    Fpunct += int(Npunct[i])
                    check= True
        for i in Nsconj:
            check=False
            for j in sconj:
                if (str(j).lower()==i and check==False):
                    Fsconj += int(Nsconj[i])
                    check= True
        for i in Nsym:
            check=False
            for j in sym:
                if (str(j).lower()==i and check==False):
                    Fsym += int(Nsym[i])
                    check= True
        for i in Nverb:
            check=False
            for j in verb:
                if (str(j).lower()==i and check==False):
                    Fverb += int(Nverb[i])
                    check= True
        for i in Nx:
            check=False
            for j in x:
                if (str(j).lower()==i and check==False):
                    Fx += int(Nx[i])
                    check= True
        
        # นับค่าต่างๆ
        cWord=len(words.split())
        cSent=words.count(" . ")     
        cAlp=len(message)
        cAlpNoSp=len(message)-message.count(' ')
        cPar=message.count('\n')+1
    return render_template('base.html',form=form,message=message,Pmessage=Pmessage,Tag=Tag,fWord=fWord,fWordSort=fWordSort,
    nkWord=nkWord,cWord=cWord,cSent=cSent,cAlp=cAlp,cAlpNoSp=cAlpNoSp,cPar=cPar,adj=adj,adp=adp,adv=adv,aux=aux,conj=conj,
    cconj=cconj,det=det,intj=intj,noun=noun,num=num,part=part,pron=pron,propn=propn,punct=punct,sconj=sconj,sym=sym,
    verb=verb,x=x,Nadj=Nadj,Nadp=Nadp,Nadv=Nadv,Naux=Naux,Nconj=Nconj,Ncconj=Ncconj,Ndet=Ndet,Nintj=Nintj,Nnoun=Nnoun,
    Nnum=Nnum,Npart=Npart,Npron=Npron,Npropn=Npropn,Npunct=Npunct,Nsconj=Nsconj,Nsym=Nsym,Nverb=Nverb,Nx=Nx,Nnadj=Nnadj,
    Nnadp=Nnadp,Nnadv=Nnadv,Nnaux=Nnaux,Nnconj=Nnconj,Nncconj=Nncconj,Nndet=Nndet,Nnintj=Nnintj,Nnnoun=Nnnoun,Nnnum=Nnnum,
    Nnpart=Nnpart,Nnpron=Nnpron,Nnpropn=Nnpropn,Nnpunct=Nnpunct,Nnsconj=Nnsconj,Nnsym=Nnsym,Nnverb=Nnverb,Nnx=Nnx,Fadj=Fadj,
    Fadp=Fadp,Fadv=Fadv,Faux=Faux,Fconj=Fconj,Fcconj=Fcconj,Fdet=Fdet,Fintj=Fintj,Fnoun=Fnoun,Fnum=Fnum,Fpart=Fpart,Fpron=Fpron,
    Fpropn=Fpropn,Fpunct=Fpunct,Fsconj=Fsconj,Fsym=Fsym,Fverb=Fverb,Fx=Fx)

# Similarity part
class dupForm(FlaskForm):
    input1= TextAreaField("Input message 1",render_kw={'style':'width: 500px;height: 100px; overflow: auto; padding:5px 5px 5px 5px'}) 
    input2= TextAreaField("Input message 2",render_kw={'style':'width: 500px;height: 100px; overflow: auto; padding:5px 5px 5px 5px'}) 
    submit2= SubmitField("Send",render_kw={'style':'width: 50px;height: 30px;'})

@app.route('/similarity/',methods=["GET","POST"])
def duplicate():
    form2=dupForm()
    input1 = False
    input2 = False
    mes1 = False
    mes2 = False
    mes1L = False
    mes2L = False
    Ames= False
    ratio = False
    if form2.validate_on_submit()and form2.submit2.data:
        input1=form2.input1.data
        input2=form2.input2.data
        form2.input1.data=""
        form2.input2.data=""
        if (input1!="" and input2!=""):
            input1=input1.lower()
            input2=input2.lower()
            ratio = SequenceMatcher(a=input1,b=input2)
            ratio = f"{ratio.ratio()}"
            mes1=input1
            mes2=input2
            sChar=["\"",",",".","(",")","[","@","_","!","#","$","%","^","&","*","(",")","<",">","?","/","\\","|","}","{","~",":","]","=","+","-","'","‘","’","“","”"]
            for i in sChar:
                mes1=(mes1.split(i))
                mes2=(mes2.split(i))
                space=" "+i+" "
                mes1=space.join(mes1)
                mes2=space.join(mes2)
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

    return render_template('similarity.html',form2=form2,input1=input1,input2=input2,mes1=mes1,mes2=mes2,mes1L=mes1L,mes2L=mes2L,Ames=Ames,ratio=ratio)

# matching part
@app.route('/matching/',methods=["GET","POST"])
def matching():
    """Render the website's about page."""
    return render_template('matching.html')

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
