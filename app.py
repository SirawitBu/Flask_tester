import os
from re import search
from flask import Flask, render_template

from flask_wtf import FlaskForm
from wtforms import TextAreaField,SubmitField
import spacy
from collections import OrderedDict
from difflib import SequenceMatcher

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'this_should_be_configured')

# Count mode part
class myForm(FlaskForm):
    message= TextAreaField("Input message",render_kw={'style':'width: 98%;height: 200px; overflow: auto; padding:5px 5px 5px 5px;border: 2px solid black;border-radius: 0.5em;'}) 
    submit= SubmitField("Send",render_kw={'style':'font-size: 20px;border-radius: 0.5em;'})
@app.route('/',methods=["GET","POST"])
def home():
    # ประกาศตัวแปร
    form=myForm()
    sp = spacy.load('en_core_web_sm')
    message = False
    Pmessage = False
    Tag= {}
    fWord= False
    fWordSort = False
    nkWord= False
    cWord= 0
    cSent= 0
    cPar = 0
    adj = {}
    adp = {}
    adv = {}
    conj = {}
    det = {}
    intj = {}
    noun = {}
    num = {}
    pron = {}
    punct = {}
    sym = {}
    verb = {}
    x = {}
    Nadj = []
    Nadp = []
    Nadv = []
    Nconj = []
    Ndet = []
    Nintj = []
    Nnoun = []
    Nnum = []
    Npron = []
    Npunct = []
    Nsym = []
    Nverb = []
    Nx = []
    Nnadj = False
    Nnadp = False
    Nnadv = False
    Nnconj = False
    Nndet = False
    Nnintj = False
    Nnnoun = False
    Nnnum = False
    Nnpron = False
    Nnpunct = False
    Nnsym = False
    Nnverb = False
    Nnx = False
    Fadj = 0
    Fadp = 0
    Fadv = 0
    Fconj = 0
    Fdet = 0
    Fintj = 0
    Fnoun = 0
    Fnum = 0
    Fpron = 0
    Fpunct = 0
    Fsym = 0
    Fverb = 0
    Fx = 0
    cOther = 0
    if form.validate_on_submit()and form.submit.data:
        # จัดการข้อความที่รับเข้ามา
        message=form.message.data
        form.message.data=""
        words=message
        saChar=["\"",",","(",")","[","@","_","!","#","$","%","^","&","*","(",")","<",">","?","/","\\","|","}","{","~",":","]","=","+","'","‘","’","“","”",".","0","1","2","3","4","5","6","7","8","9"]
        for i in saChar:
            cawords=(words.split(i))
            cawords=" ".join(cawords)
        cawords=cawords.split()
        words=(words.split("’"))
        words="'".join(words)        
        sChar=["\"",",","(",")","[","@","_","!","#","$","%","^","&","*","(",")","<",">","?","/","\\","|","}","{","~",":","]","=","+","‘","’","“","”"]
        for i in sChar:
            words=(words.split(i))
            space=" "+i+" "
            words=space.join(words)
        words=words.split()
        words=" ".join(words)
        # ใช้spacy หาPart of speech ของแต่ละคำ
        words = sp(words)
        for i in words:
            if i.pos_.lower()=="adj":
                Tag[i]=spacy.explain(i.pos_)
                adj[i]=spacy.explain(i.pos_)
                Nadj.append(str(i))
            elif i.pos_.lower()=="adp" or i.pos_.lower()=="part":
                Tag[i]="preposition"
                adp[i]="preposition"
                Nadp.append(str(i))
            elif i.pos_.lower()=="adv":
                Tag[i]=spacy.explain(i.pos_)
                adv[i]=spacy.explain(i.pos_)
                Nadv.append(str(i))
            elif i.pos_.lower()=="conj" or i.pos_.lower()=="cconj" or i.pos_.lower()=="sconj":
                Tag[i]="conjunction"
                conj[i]="conjunction"
                Nconj.append(str(i))
            elif i.pos_.lower()=="det":
                Tag[i]=spacy.explain(i.pos_)
                det[i]=spacy.explain(i.pos_)
                Ndet.append(str(i))
            elif i.pos_.lower()=="intj":
                Tag[i]=spacy.explain(i.pos_)
                intj[i]=spacy.explain(i.pos_)
                Nintj.append(str(i))
            elif i.pos_.lower()=="noun" or i.pos_.lower()=="propn":
                Tag[i]="noun"
                noun[i]="noun"
                Nnoun.append(str(i))
            elif i.pos_.lower()=="num":
                Tag[i]=spacy.explain(i.pos_)
                num[i]=spacy.explain(i.pos_)
                Nnum.append(str(i))
            elif i.pos_.lower()=="pron":
                Tag[i]=spacy.explain(i.pos_)
                pron[i]=spacy.explain(i.pos_)
                Npron.append(str(i))
            elif i.pos_.lower()=="punct":
                Tag[i]=spacy.explain(i.pos_)
                punct[i]=spacy.explain(i.pos_)
                Npunct.append(str(i))
            elif i.pos_.lower()=="sym":
                Tag[i]=spacy.explain(i.pos_)
                sym[i]=spacy.explain(i.pos_)
                Nsym.append(str(i))
            elif i.pos_.lower()=="verb" or i.pos_.lower()=="aux":
                Tag[i]="verb"
                verb[i]="verb"
                Nverb.append(str(i))
            elif i.pos_.lower()=="x":
                Tag[i]=spacy.explain(i.pos_)
                x[i]=spacy.explain(i.pos_)
                Nx.append(str(i))
            else:
                Tag[i]=spacy.explain(i.pos_)
        # Awords=[]
        # for i in Tag:
        #     Awords.append(str(i))
        # words = " ".join(Awords)
        # ฟังก์ชันนับจำนวนคำ
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
        # นับจำนวนคำทั้งหมด และความถี่ของแต่ละคำ
        if fWord != False:
            nkWord=len(fWordSort)
        if adj != {}:
            Nadj=" ".join(Nadj)
            Nadj=(word_count(str(Nadj).lower()))
            Nnadj=len(Nadj)
            for i in Nadj:
                check=False
                for j in adj:
                    if (str(j).lower()==i and check==False):
                        Fadj += int(Nadj[i])
                        check= True
        if adp != {}:
            Nadp=" ".join(Nadp)
            Nadp=(word_count(str(Nadp).lower()))
            Nnadp=len(Nadp)
            for i in Nadp:
                check=False
                for j in adp:
                    if (str(j).lower()==i and check==False):
                        Fadp += int(Nadp[i])
                        check= True
        if adv != {}:
            Nadv=" ".join(Nadv)
            Nadv=(word_count(str(Nadv).lower()))
            Nnadv=len(Nadv)
            for i in Nadv:
                check=False
                for j in adv:
                    if (str(j).lower()==i and check==False):
                        Fadv += int(Nadv[i])
                        check= True
        if conj != {}:
            Nconj=" ".join(Nconj)
            Nconj=(word_count(str(Nconj).lower()))
            Nnconj=len(Nconj)
            for i in Nconj:
                check=False
                for j in conj:
                    if (str(j).lower()==i and check==False):
                        Fconj += int(Nconj[i])
                        check= True
        if det != {}:
            Ndet=" ".join(Ndet)
            Ndet=(word_count(str(Ndet).lower()))
            Nndet=len(Ndet)
            for i in Ndet:
                check=False
                for j in det:
                    if (str(j).lower()==i and check==False):
                        Fdet += int(Ndet[i])
                        check= True
        if intj != {}:
            Nintj=" ".join(Nintj)
            Nintj=(word_count(str(Nintj).lower()))
            Nnintj=len(Nintj)
            for i in Nintj:
                check=False
                for j in intj:
                    if (str(j).lower()==i and check==False):
                        Fintj += int(Nintj[i])
                        check= True
        if noun != {}:
            Nnoun=" ".join(Nnoun)
            Nnoun=(word_count(str(Nnoun).lower()))
            Nnnoun=len(Nnoun)
            for i in Nnoun:
                check=False
                for j in noun:
                    if (str(j).lower()==i and check==False):
                        Fnoun += int(Nnoun[i])
                        check= True
        if num != {}:
            Nnum=" ".join(Nnum)
            Nnum=(word_count(str(Nnum).lower()))
            Nnnum=len(Nnum)
            for i in Nnum:
                check=False
                for j in num:
                    if (str(j).lower()==i and check==False):
                        Fnum += int(Nnum[i])
                        check= True
        if pron != {}:
            Npron=" ".join(Npron)
            Npron=(word_count(str(Npron).lower()))
            Nnpron=len(Npron)
            for i in Npron:
                check=False
                for j in pron:
                    if (str(j).lower()==i and check==False):
                        Fpron += int(Npron[i])
                        check= True
        if punct != {}:
            Npunct=" ".join(Npunct)
            Npunct=(word_count(str(Npunct).lower()))
            Nnpunct=len(Npunct)
            for i in Npunct:
                check=False
                for j in punct:
                    if (str(j).lower()==i and check==False):
                        Fpunct += int(Npunct[i])
                        check= True
        if sym != {}:
            Nsym=" ".join(Nsym)
            Nsym=(word_count(str(Nsym).lower()))
            Nnsym=len(Nsym)
            for i in Nsym:
                check=False
                for j in sym:
                    if (str(j).lower()==i and check==False):
                        Fsym += int(Nsym[i])
                        check= True
        if verb != {}:
            Nverb=" ".join(Nverb)
            Nverb=(word_count(str(Nverb).lower()))
            Nnverb=len(Nverb)
            for i in Nverb:
                check=False
                for j in verb:
                    if (str(j).lower()==i and check==False):
                        Fverb += int(Nverb[i])
                        check= True
        if x != {}:
            Nx=" ".join(Nx)
            Nx=(word_count(str(Nx).lower()))
            Nnx=len(Nx)
            for i in Nx:
                check=False
                for j in x:
                    if (str(j).lower()==i and check==False):
                        Fx += int(Nx[i])
                        check= True
        # นับค่าต่างๆ
        cWord=len(cawords)
        # นับประโยค
        for i in Tag:
            check=False
            if (str(i).lower()=="." and check==False):
                        cSent += 1
                        check= True 
        # นับพารากราฟ
        cPar=message.count('\n')+1
        # นับคำอื่น ๆ เช่นประเภทตัวเลขหรือสัญลักษณ์
        cOther= Fnum+Fsym
    return render_template('base.html',form=form,message=message,Pmessage=Pmessage,Tag=Tag,fWord=fWord,fWordSort=fWordSort,
    nkWord=nkWord,cWord=cWord,cSent=cSent,cPar=cPar,cOther=cOther,adj=adj,adp=adp,adv=adv,conj=conj,
    det=det,intj=intj,noun=noun,num=num,pron=pron,punct=punct,sym=sym,
    verb=verb,x=x,Nadj=Nadj,Nadp=Nadp,Nadv=Nadv,Nconj=Nconj,Ndet=Ndet,Nintj=Nintj,Nnoun=Nnoun,
    Nnum=Nnum,Npron=Npron,Npunct=Npunct,Nsym=Nsym,Nverb=Nverb,Nx=Nx,Nnadj=Nnadj,
    Nnadp=Nnadp,Nnadv=Nnadv,Nnconj=Nnconj,Nndet=Nndet,Nnintj=Nnintj,Nnnoun=Nnnoun,Nnnum=Nnnum,
    Nnpron=Nnpron,Nnpunct=Nnpunct,Nnsym=Nnsym,Nnverb=Nnverb,Nnx=Nnx,Fadj=Fadj,
    Fadp=Fadp,Fadv=Fadv,Fconj=Fconj,Fdet=Fdet,Fintj=Fintj,Fnoun=Fnoun,Fnum=Fnum,
    Fpron=Fpron,Fpunct=Fpunct,Fsym=Fsym,Fverb=Fverb,Fx=Fx)

# Similarity mode part
class dupForm(FlaskForm):
    input1= TextAreaField("Main message",render_kw={'style':'width: 99%;height: 100px; overflow: auto; padding:5px 5px 5px 5px;border: 2px solid black;border-radius: 0.5em;'}) 
    input2= TextAreaField("Message to compare",render_kw={'style':'width: 99%;height: 50px; overflow: auto; padding:5px 5px 5px 5px;border: 2px solid black;border-radius: 0.5em;'}) 
    submit2= SubmitField("Send",render_kw={'style':'font-size: 20px;border-radius: 0.5em;'})
@app.route('/similarity/',methods=["GET","POST"])
def similarity():
    # ประกาศตัวแปร
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
        # จัดการข้อความที่รับมา
        input1=form2.input1.data
        input2=form2.input2.data
        form2.input1.data=""
        form2.input2.data=""
        if (input1!="" and input2!=""):
            input1=input1.lower()
            input2=input2.lower()
            # หา%ความเหมือน
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
            # หาคำที่ซ้ำกัน
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

# Matching mode part
@app.route('/matching/',methods=["GET","POST"])
def matching():
    # ประกาศตัวแปร
    form=myForm()
    message=False
    msl1 = []
    msl2 = []
    msl3 = []
    msl4 = []
    msl5 = []
    msl6 = []
    msl7 = []
    msl8 = []
    msl9 = []
    msl10 = []
    Nmsl1 = {}
    Nmsl2 = {}
    Nmsl3 = {}
    Nmsl4 = {}
    Nmsl5 = {}
    Nmsl6 = {}
    Nmsl7 = {}
    Nmsl8 = {}
    Nmsl9 = {}
    Nmsl10 = {}
    Nnmsl1 = False
    Nnmsl2 = False
    Nnmsl3 = False
    Nnmsl4 = False
    Nnmsl5 = False
    Nnmsl6 = False
    Nnmsl7 = False
    Nnmsl8 = False
    Nnmsl9 = False
    Nnmsl10 = False
    Fmsl1 = 0
    Fmsl2 = 0
    Fmsl3 = 0
    Fmsl4 = 0
    Fmsl5 = 0
    Fmsl6 = 0
    Fmsl7 = 0
    Fmsl8 = 0
    Fmsl9 = 0
    Fmsl10 = 0
    aword = 0
    asword = 0
    aswordp = 0
    # test=False
    if form.validate_on_submit()and form.submit.data:
        # จัดการข้อความที่รับเข้ามา
        message=form.message.data
        form.message.data=""
        words=message
        saChar=["\"",",","(",")","[","@","_","!","#","$","%","^","&","*","(",")","<",">","?","/","\\","|","}","{","~",":","]","=","+","'","‘","’","“","”",".","0","1","2","3","4","5","6","7","8","9"]
        for i in saChar:
            aword=(words.split(i))
            aword=" ".join(aword)
        aword=aword.split()
        sChar=["\"",",","(",")","[","@","_","!","#","$","%","^","&","*","(",")","<",">","?","/","\\","|","}","{","~",":","]","=","+","'","‘","’","“","”",".","0","1","2","3","4","5","6","7","8","9"]
        for i in sChar:
            words=(words.split(i))
            words=" ".join(words)
        words=words.split()
        # คำแต่ละคำใน Sublist ต่างๆ
        sl1=["analyse","analysed","analyser","analysers","analyses","analysing","analysis","analyst","analysts","analytic","analytical","analytically","analyze","analyzed","analyzes","analyzing","approach","approachable","approached","approaches","approaching","unapproachable","area","areas","assess","assessable","assessed","assesses","assessing","assessment","assessments","reassess","reassessed","reassessing","reassessment","unassessed","assume","assumed","assumes","assuming","assumption","assumptions","authority","authoritative","authorities","available","availability","unavailable","benefit","beneficial","beneficiary","beneficiaries","benefited","benefiting","benefits","concept","conception","concepts","conceptual","conceptualisation","conceptualise","conceptualised","conceptualises","conceptualising","conceptually","consist","consisted","consistency","consistent","consistently","consisting","consists","inconsistencies","inconsistency","inconsistent","constitute","constituencies","constituency","constituent","constituents","constituted","constitutes","constituting","constitution","constitutions","constitutional","constitutionally","constitutive","unconstitutional","context","contexts","contextual","contextualise","contextualised","contextualising","uncontextualised","contextualize","contextualized","contextualizing","uncontextualized","contract","contracted","contracting","contractor","contractors","contracts","create","created","creates","creating","creation","creations","creative","creatively","creativity","creator","creators","recreate","recreated","recreates","recreating","data","define","definable","defined","defines","defining","definition","definitions","redefine","redefined","redefines","redefining","undefined","derive","derivation","derivations","derivative","derivatives","derived","derives","deriving","distribute","distributed","distributing","distribution","distributional","distributions","distributive","distributor","distributors","redistribute","redistributed","redistributes","redistributing","redistribution","economy","economic","economical","economically","economics","economies","economist","economists","uneconomical","environment","environmental","environmentalist","environmentalists","environmentally","environments","establish","disestablish","disestablished","disestablishes","disestablishing","disestablishment","established","establishes","establishing","establishment","establishments","estimate","estimated","estimates","estimating","estimation","estimations","over-estimate","overestimate","overestimated","overestimates","overestimating","underestimate","underestimated","underestimates","underestimating","evident","evidenced","evidence","evidential","evidently","export","exported","exporter","exporters","exporting","exports","factor","factored","factoring","factors","finance","financed","finances","financial","financially","financier","financiers","financing","formula","formulae","formulas","formulate","formulated","formulating","formulation","formulations","reformulate","reformulated","reformulating","reformulation","reformulations","function","functional","functionally","functioned","functioning","functions","identify","identifiable","identification","identified","identifies","identifying","identities","identity","unidentifiable","income","incomes","indicate","indicated","indicates","indicating","indication","indications","indicative","indicator","indicators","individual","individualised","individuality","individualism","individualist","individualists","individualistic","individually","individuals","interpret","interpretation","interpretations","interpretative","interpreted","interpreting","interpretive","interprets","misinterpret","misinterpretation","misinterpretations","misinterpreted","misinterpreting","misinterprets","reinterpret","reinterpreted","reinterprets","reinterpreting","reinterpretation","reinterpretations","involve","involved","involvement","involves","involving","uninvolved","issue","issued","issues","issuing","labour","labor","labored","labors","laboured","labouring","labours","legal","illegal","illegality","illegally","legality","legally","legislate","legislated","legislates","legislating","legislation","legislative","legislator","legislators","legislature","major","majorities","majority","method","methodical","methodological","methodologies","methodology","methods","occur","occurred","occurrence","occurrences","occurring","occurs","reoccur","reoccurred","reoccurring","reoccurs","percent","percentage","percentages","period","periodic","periodical","periodically","periodicals","periods","policy","policies","principle","principled","principles","unprincipled","proceed","procedural","procedure","procedures","proceeded","proceeding","proceedings","proceeds","process","processed","processes","processing","require","required","requirement","requirements","requires","requiring","research","researched","researcher","researchers","researches","researching","respond","responded","respondent","respondents","responding","responds","response","responses","responsive","responsiveness","unresponsive","role","roles","section","sectioned","sectioning","sections","sector","sectors","significant","insignificant","insignificantly","significance","significantly","signified","signifies","signify","signifying","similar","dissimilar","similarities","similarity","similarl","source","sourced","sources","sourcing","specific","specifically","specification","specifications","specificity","specifics","structure","restructure","restructured","restructures","restructuring","structural","structurally","structured","structures","structuring","unstructured","theory","theoretical","theoretically","theories","theorist","theorists","vary","invariable","invariably","variability","variable","variables","variably","variance","variant","variants","variation","variations","varied","varies","varying"]
        sl2=["achieve","achievable","achieved","achievement","achievements","achieves","achieving","acquire","acquired","acquires","acquiring","acquisition","acquisitions","administrate","administrates","administration","administrations","administrative","administratively","administrator","administrators","affect","affected","affecting","affective","affectively","affects","unaffected","appropriate","appropriacy","appropriately","appropriateness","inappropriacy","inappropriate","inappropriately","aspect","aspects","assist","assistance","assistant","assistants","assisted","assisting","assists","unassisted","category","categories","categorisation","categorise","categorised","categorises","categorising","categorization","categorized","categorizes","categorizing","chapter","chapters","commission","commissioned","commissioner","commissioners","commissioning","commissions","community","communities","complex","complexities","complexity","compute","computation","computational","computations","computable","computer","computed","computerised","computers","computing","conclude","concluded","concludes","concluding","conclusion","conclusions","conclusive","conclusively","inconclusive","inconclusively","conduct","conducted","conducting","conducts","consequent","consequence","consequences","consequently","construct","constructed","constructing","construction","constructions","constructive","constructs","reconstruct","reconstructed","reconstructing","reconstruction","reconstructs","consume","consumed","consumer","consumers","consumes","consuming","consumption","credit","credited","crediting","creditor","creditors","credits","culture","cultural","culturally","cultured","cultures","uncultured","design","designed","designer","designers","designing","designs","distinct","distinction","distinctions","distinctive","distinctively","distinctly","indistinct","indistinctly","element","elements","equate","equated","equates","equating","equation","equations","evaluate","evaluated","evaluates","evaluating","evaluation","evaluations","evaluative","re-evaluate","re-evaluated","re-evaluates","re-evaluating","re-evaluation","feature","featured","features","featuring","final","finalise","finalised","finalises","finalising","finalize","finalized","finalizes","finalizing","finality","finally","finals","focus","focused","focuses","focusing","focussed","focussing","refocus","refocused","refocuses","refocusing","refocussed","refocusses","refocussing","impact","impacted","impacting","impacts","injure","injured","injures","injuries","injuring","injury","uninjured","institute","instituted","institutes","instituting","institution","institutional","institutionalise","institutionalised","institutionalises","institutionalising","institutionalized","institutionalizes","institutionalizing","institutionally","institutions","invest","invested","investing","investment","investments","investor","investors","invests","reinvest","reinvested","reinvesting","reinvestment","reinvests","item","itemisation","itemise","itemised","itemises","itemising","items","journal","journals","maintain","maintained","maintaining","maintains","maintenance","normal","abnormal","abnormally","normalisation","normalise","normalised","normalises","normalising","normalization","normalize","normalized","normalizes","normalizing","normality","normally","obtain","obtainable","obtained","obtaining","obtains","unobtainable","participate","participant","participants","participated","participates","participating","participation","participatory","perceive","perceived","perceives","perceiving","perception","perceptions","positive","positively","potential","potentially","previous","previously","primary","primarily","purchase","purchased","purchaser","purchasers","purchases","purchasing","range","ranged","ranges","ranging","region","regional","regionally","regions","regulate","deregulated","deregulates","deregulating","deregulation","regulated","regulates","regulating","regulation","regulations","regulator","regulators","regulatory","unregulated","relevant","irrelevance","irrelevant","relevance","reside","resided","residence","resident","residential","residents","resides","residing","resource","resourced","resourceful","resources","resourcing","unresourceful","under-resourced","restrict","restricted","restricting","restriction","restrictions","restrictive","restrictively","restricts","unrestricted","unrestrictive","secure","insecure","insecurities","insecurity","secured","securely","secures","securing","securities","security","seek","seeking","seeks","sought","select","selected","selecting","selection","selections","selective","selectively","selector","selectors","selects","site","sites","strategy","strategic","strategies","strategically","strategist","strategists","survey","surveyed","surveying","surveys","text","texts","textual","tradition","nontraditional","traditional","traditionalist","traditionally","traditions","transfer","transferable","transference","transferred","transferring","transfers"]
        sl3=["alternative","alternatively","alternatives","circumstance","circumstances","comment","commentaries","commentary","commentator","commentators","commented","commenting","comments","compensate","compensated","compensates","compensating","compensation","compensations","compensatory","component","componentry","components","consent","consensus","consented","consenting","consents","considerable","considerably","constant","constancy","constantly","constants","inconstancy","inconstantly","constrain","constrained","constraining","constrains","constraint","constraints","unconstrained","contribute","contributed","contributes","contributing","contribution","contributions","contributor","contributors","convene","convention","convenes","convened","convening","conventional","conventionally","conventions","unconventional","coordinate","coordinated","coordinates","coordinating","coordination","coordinator","coordinators","co-ordinate","co-ordinated","co-ordinates","co-ordinating","co-ordination","co-ordinator","co-ordinators","core","cores","coring","cored","corporate","corporates","corporation","corporations","correspond","corresponded","correspondence","corresponding","correspondingly","corresponds","criteria","criterion","deduce","deduced","deduces","deducing","deduction","deductions","demonstrate","demonstrable","demonstrably","demonstrated","demonstrates","demonstrating","demonstration","demonstrations","demonstrative","demonstratively","demonstrator","demonstrators","document","documentation","documented","documenting","documents","dominate","dominance","dominant","dominated","dominates","dominating","domination","emphasis","emphasise","emphasised","emphasising","emphasize","emphasized","emphasizes","emphasizing","emphatic","emphatically","ensure","ensured","ensures","ensuring","exclude","excluded","excludes","excluding","exclusion","exclusionary","exclusionist","exclusions","exclusive","exclusively","framework","frameworks","fund","funded","funder","funders","funding","funds","illustrate","illustrated","illustrates","illustrating","illustration","illustrations","illustrative","immigrate","immigrant","immigrants","immigrated","immigrates","immigrating","immigration","imply","implied","implies","implying","initial","initially","instance","instances","interact","interacted","interacting","interaction","interactions","interactive","interactively","interacts","justify","justifiable","justifiably","justification","justifications","justified","justifies","justifying","unjustified","layer","layered","layering","layers","link","linkage","linkages","linked","linking","links","locate","located","locating","location","locations","relocate","relocated","relocates","relocating","relocation","maximise","max","maximised","maximises","maximising","maximisation","maximize","maximized","maximizes","maximizing","maximization","maximum","minor","minorities","minority","minors","negate","negative","negated","negates","negating","negatively","negatives","outcome","outcomes","partner","partners","partnership","partnerships","philosophy","philosopher","philosophers","philosophical","philosophically","philosophies","philosophise","philosophised","philosophises","philosophising","philosophize","philosophized","philosophizes","philosophizing","physical","physically","proportion","disproportion","disproportionate","disproportionately","proportional","proportionally","proportionate","proportionately","proportions","publish","published","publisher","publishers","publishes","publishing","unpublished","react","reacted","reacts","reacting","reaction","reactionaries","reactionary","reactions","reactive","reactivate","reactivation","reactor","reactors","register","deregister","deregistered","deregistering","deregisters","deregistration","registered","registering","registers","registration","rely","reliability","reliable","reliably","reliance","reliant","relied","relies","relying","unreliable","remove","removable","removal","removals","removed","removes","removing","scheme","schematic","schematically","schemed","schemes","scheming","sequence","sequenced","sequences","sequencing","sequential","sequentially","sex","sexes","sexism","sexual","sexuality","sexually","shift","shifted","shifting","shifts","specify","specifiable","specified","specifies","specifying","unspecified","sufficient","sufficiency","insufficient","insufficiently","sufficiently","task","tasks","technical","technically","technique","techniques","technology","technological","technologically"]
        sl4=["access","accessed","accesses","accessibility","accessible","accessing","inaccessible","adequate","adequacy","adequately","inadequacies","inadequacy","inadequate","inadequately","annual","annually","apparent","apparently","approximate","approximated","approximately","approximates","approximating","approximation","approximations","attitude","attitudes","attribute","attributable","attributed","attributes","attributing","attribution","civil","code","coded","codes","coding","commit","commitment","commitments","commits","committed","committing","communicate","communicable","communicated","communicates","communicating","communication","communications","communicative","communicatively","uncommunicative","concentrate","concentrated","concentrates","concentrating","concentration","confer","conference","conferences","conferred","conferring","confers","contrast","contrasted","contrasting","contrastive","contrasts","cycle","cycled","cycles","cyclic","cyclical","cycling","debate","debatable","debated","debates","debating","despite","dimension","dimensional","dimensions","multidimensional","domestic","domestically","domesticate","domesticated","domesticating","domestics","emerge","emerged","emergence","emergent","emerges","emerging","error","erroneous","erroneously","errors","ethnic","ethnicity","goal","goals","grant","granted","granting","grants","hence","hypothesis","hypotheses","hypothesise","hypothesised","hypothesises","hypothesising","hypothesize","hypothesized","hypothesizes","hypothesizing","hypothetical","hypothetically","implement","implementation","implemented","implementing","implements","implicate","implicated","implicates","implicating","implication","implications","impose","imposed","imposes","imposing","imposition","integrate","integrated","integrates","integrating","integration","internal","internalise","internalised","internalises","internalising","internalize","internalized","internalizes","internalizing","internally","investigate","investigated","investigates","investigating","investigation","investigations","investigative","investigator","investigators","job","jobs","label","labeled","labeling","labelled","labelling","labels","mechanism","mechanisms","obvious","obviously","occupy","occupancy","occupant","occupants","occupation","occupational","occupations","occupied","occupier","occupiers","occupies","occupying","option","optional","options","output","outputs","overall","parallel","paralleled","parallelled","paralleling","parallels","unparalleled","parameter","parameters","phase","phased","phases","phasing","predict","predictability","predictable","predictably","predicted","predicting","prediction","predictions","predicts","unpredictability","unpredictable","principal","principally","prior","professional","professionally","professionals","professionalism","project","projected","projecting","projection","projections","projects","promote","promoted","promoter","promoters","promotes","promoting","promotion","promotions","regime","regimes","resolve","resolution","resolved","resolves","resolving","unresolved","retain","retained","retaining","retainer","retainers","retains","retention","retentive","series","statistic","statistician","statisticians","statistical","statistically","statistics","status","stress","stressed","stresses","stressful","stressing","unstressed","subsequent","subsequently","sum","summation","summed","summing","sums","summary","summaries","summarise","summarised","summarises","summarising","summarisation","summarisations","summarization","summarizations","summarize","summarized","summarizes","summarizing","undertake","undertaken","undertakes","undertaking","undertook"]
        sl5=["academy","academia","academic","academically","academics","academies","adjust","adjusted","adjusting","adjustment","adjustments","adjusts","readjust","readjusted","readjusting","readjustment","readjustments","readjusts","alter","alterable","alteration","alterations","altered","altering","alternate","alternating","alters","unalterable","unaltered","amend","amended","amending","amendment","amendments","amends","aware","awareness","unaware","capacity","capacities","incapacitate","incapacitated","challenge","challenged","challenger","challengers","challenges","challenging","clause","clauses","compound","compounded","compounding","compounds","conflict","conflicted","conflicting","conflicts","consult","consultancy","consultant","consultants","consultation","consultations","consultative","consulted","consults","consulting","contact","contactable","contacted","contacting","contacts","decline","declined","declines","declining","discrete","discretely","discretion","discretionary","indiscrete","indiscretion","draft","drafted","drafting","drafts","redraft","redrafted","redrafting","redrafts","enable","enabled","enables","enabling","energy","energetic","energetically","energies","enforce","enforced","enforcement","enforces","enforcing","entity","entities","equivalent","equivalence","evolve","evolution","evolved","evolving","evolves","evolutionary","evolutionist","evolutionists","expand","expanded","expanding","expands","expansion","expansionism","expansive","expose","exposed","exposes","exposing","exposure","exposures","external","externalisation","externalise","externalised","externalises","externalising","externality","externalization","externalize","externalized","externalizes","externalizing","externally","facilitate","facilitated","facilitates","facilities","facilitating","facilitation","facilitator","facilitators","facility","fundamental","fundamentally","generate","generated","generates","generating","generation","generations","image","imagery","images","liberal","liberalise","liberalism","liberalisation","liberalised","liberalises","liberalising","liberalization","liberalize","liberalized","liberalizes","liberalizing","liberate","liberated","liberates","liberation","liberations","liberating","liberator","liberators","liberally","liberals","licence","licences","license","licensed","licensing","licenses","unlicensed","logic","illogical","illogically","logical","logically","logician","logicians","margin","marginal","marginally","margins","medical","medically","mental","mentality","mentally","modify","modification","modifications","modified","modifies","modifying","unmodified","monitor","monitored","monitoring","monitors","unmonitored","network","networked","networking","networks","notion","notions","objective","objectively","objectivity","orient","orientate","orientated","orientates","orientation","orientating","oriented","orienting","orients","reorient","reorientation","perspective","perspectives","precise","imprecise","precisely","precision","prime","primacy","psychology","psychological","psychologically","psychologist","psychologists","pursue","pursued","pursues","pursuing","pursuit","pursuits","ratio","ratios","reject","rejected","rejecting","rejection","rejects","rejections","revenue","revenues","stable","instability","stabilisation","stabilise","stabilised","stabilises","stabilising","stabilization","stabilize","stabilized","stabilizes","stabilizing","stability","unstable","style","styled","styles","styling","stylish","stylise","stylised","stylises","stylising","stylize","stylized","stylizes","stylizing","substitute","substituted","substitutes","substituting","substitution","sustain","sustainable","sustainability","sustained","sustaining","sustains","sustenance","unsustainable","symbol","symbolic","symbolically","symbolise","symbolises","symbolised","symbolising","symbolism","symbolize","symbolized","symbolizes","symbolizing","symbols","target","targeted","targeting","targets","transit","transited","transiting","transition","transitional","transitions","transitory","transits","trend","trends","version","versions","welfare","whereas"]
        sl6=["abstract","abstraction","abstractions","abstractly","abstracts","accurate","accuracy","accurately","inaccuracy","inaccuracies","inaccurate","acknowledge","acknowledged","acknowledges","acknowledging","acknowledgement","acknowledgemens","aggregate","aggregated","aggregates","aggregating","aggregation","allocate","allocated","allocates","allocating","allocation","allocations","assign","assigned","assigning","assignment","assignments","assigns","reassign","reassigned","reassigning","reassigns","unassigned","attach","attached","attaches","attaching","attachment","attachments","unattached","author","authored","authoring","authors","authorship","bond","bonded","bonding","bonds","brief","brevity","briefed","briefing","briefly","briefs","capable","capabilities","capability","incapable","cite","citation","citations","cited","citing","cites","cooperate","cooperated","cooperates","cooperating","cooperation","cooperative","cooperatively","co-operate","co-operated","co-operates","co-operation","co-operative","co-operatively","discriminate","discriminated","discriminates","discriminating","discrimination","display","displayed","displaying","displays","diverse","diversely","diversification","diversified","diversifies","diversify","diversifying","diversity","domain","domains","edit","edited","editing","edition","editions","editor","editorial","editorials","editors","edits","enhance","enhanced","enhancement","enhances","enhancing","estate","estates","exceed","exceeded","exceeding","exceeds","expert","expertise","expertly","experts","explicit","explicitly","federal","federation","federations","fee","fees","flexible","flexibility","inflexible","inflexibility","furthermore","gender","genders","ignorant","ignorance","ignore","ignored","ignores","ignoring","incentive","incentives","incidence","incident","incidentally","incidents","incorporate","incorporated","incorporates","incorporating","incorporation","index","indexed","indexes","indexing","inhibit","inhibited","inhibiting","inhibition","inhibitions","inhibits","initiate","initiated","initiates","initiating","initiation","initiations","initiative","initiatives","initiator","initiators","input","inputs","instruct","instruction","instructed","instructing","instructions","instructive","instructor","instructors","instructs","intelligent","intelligence","intelligently","unintelligent","interval","intervals","lecture","lectured","lecturer","lecturers","lectures","lecturing","migrate","migrant","migrants","migrated","migrates","migrating","migration","migrations","migratory","minimum","ministry","ministered","ministering","ministerial","ministries","motive","motivate","motivated","motivates","motivating","motivation","motivations","motives","unmotivated","neutral","neutralisation","neutralise","neutralised","neutralises","neutralising","neutrality","neutralization","neutralize","neutralized","neutralizes","neutralizing","nevertheless","overseas","precede","preceded","precedence","precedent","precedes","preceding","unprecedented","presume","presumably","presumed","presumes","presuming","presumption","presumptions","presumptuous","rational","irrational","rationalisation","rationalisations","rationalise","rationalised","rationalises","rationalising","rationalism","rationality","rationalization","rationalizations","rationalize","rationalized","rationalizes","rationally","recover","recoverable","recovered","recovering","recovers","recovery","reveal","revealed","revealing","reveals","revelation","revelations","scope","subsidy","subsidiary","subsidies","subsidise","subsidised","subsidises","subsidising","subsidize","subsidized","subsidizes","subsidizing","tape","taped","tapes","taping","trace","traceable","traced","traces","tracing","transform","transformation","transformations","transformed","transforming","transforms","transport","transportation","transported","transporter","transporters","transporting","transports","underlie","underlay","underlies","underlying","utilise","utilisation","utilised","utilises","utilising","utiliser","utilisers","utility","utilities","utilization","utilize","utilized","utilizes","utilizing"]
        sl7=["adapt","adaptability","adaptable","adaptation","adaptations","adapted","adapting","adaptive","adapts","adult","adulthood","adults","advocate","advocacy","advocated","advocates","advocating","aid","aided","aiding","aids","unaided","channel","channelled","channelling","channels","chemical","chemically","chemicals","classic","classical","classics","comprehensive","comprehensively","comprise","comprised","comprises","comprising","confirm","confirmation","confirmed","confirming","confirms","contrary","contrarily","convert","conversion","conversions","converted","convertible","converting","converts","couple","coupled","coupling","couples","decade","decades","definite","definitely","definitive","indefinite","indefinitely","deny","deniable","denial","denials","denied","denies","denying","undeniable","differentiate","differentiated","differentiates","differentiating","differentiation","dispose","disposable","disposal","disposed","disposes","disposing","dynamic","dynamically","dynamics","eliminate","eliminated","eliminates","eliminating","elimination","empirical","empirically","empiricism","equip","equipment","equipped","equipping","equips","extract","extracted","extracting","extraction","extracts","file","filed","files","filing","finite","infinite","infinitely","foundation","foundations","globe","global","globally","globalisation","globalization","grade","graded","grades","grading","guarantee","guaranteed","guaranteeing","guarantees","hierarchy","hierarchical","hierarchies","identical","identically","ideology","ideological","ideologically","ideologies","infer","inference","inferences","inferred","inferring","infers","innovate","innovation","innovated","innovates","innovating","innovations","innovative","innovator","innovators","insert","inserted","inserting","insertion","inserts","intervene","intervened","intervenes","intervening","intervention","interventions","isolate","isolated","isolates","isolating","isolation","isolationism","media","mode","modes","paradigm","paradigms","phenomenon","phenomena","phenomenal","priority","priorities","prioritisation","prioritise","prioritised","prioritises","prioritising","prioritization","prioritize","prioritized","prioritizes","prioritizing","prohibit","prohibited","prohibiting","prohibition","prohibitions","prohibitive","prohibits","publication","publications","quote","quotation","quotations","quoted","quotes","quoting","release","released","releases","releasing","reverse","reversal","reversed","reverses","reversible","reversing","reversals","irreversible","simulate","simulated","simulates","simulating","simulation","sole","solely","somewhat","submit","submission","submissions","submits","submitted","submitting","successor","succession","successions","successive","successively","successors","survive","survival","survived","survives","surviving","survivor","survivors","thesis","theses","topic","topical","topics","transmit","transmission","transmissions","transmitted","transmitting","transmits","ultimate","ultimately","unique","uniquely","uniqueness","visible","visibility","visibly","invisible","invisibility","voluntary","voluntarily","volunteer","volunteering","volunteered","volunteers"]
        sl8=["abandon","abandoned","abandoning","abandonment","abandons","accompany","accompanied","accompanies","accompaniment","accompanying","unaccompanied","accumulate","accumulated","accumulating","accumulation","accumulates","ambiguous","ambiguities","ambiguity","unambiguous","unambiguously","append","appendix","appended","appends","appending","appendices","appendixes","appreciate","appreciable","appreciably","appreciated","appreciates","appreciating","appreciation","unappreciated","arbitrary","arbitrariness","arbitrarily","automate","automatic","automated","automates","automating","automatically","automation","bias","biased","biases","biasing","unbiased","chart","charted","charting","charts","uncharted","clarify","clarification","clarified","clarifies","clarifying","clarity","commodity","commodities","complement","complementary","complemented","complementing","complements","conform","conformable","conformability","conformance","conformation","conformed","conforming","conformist","conformists","conformity","conforms","nonconformist","nonconformists","nonconformity","non-conformist","non-conformists","non-conformity","contemporary","contemporaries","contradict","contradicted","contradicting","contradiction","contradictions","contradictory","contradicts","crucial","crucially","currency","currencies","denote","denotation","denotations","denoted","denotes","denoting","detect","detectable","detected","detecting","detection","detective","detectives","detector","detectors","detects","deviate","deviated","deviates","deviating","deviation","deviations","displace","displaced","displacement","displaces","displacing","drama","dramas","dramatic","dramatically","dramatise","dramatised","dramatising","dramatises","dramatisation","dramatisations","dramatist","dramatists","dramatization","dramatizations","dramatize","dramatized","dramatizes","dramatizing","eventual","eventuality","eventually","exhibit","exhibited","exhibiting","exhibition","exhibitions","exhibits","exploit","exploitation","exploited","exploiting","exploits","fluctuate","fluctuated","fluctuates","fluctuating","fluctuation","fluctuations","guideline","guidelines","highlight","highlighted","highlighting","highlights","implicit","implicitly","induce","induced","induces","inducing","induction","inevitable","inevitability","inevitably","infrastructure","infrastructures","inspect","inspected","inspecting","inspection","inspections","inspector","inspectors","inspects","intense","intensely","intenseness","intensification","intensified","intensifies","intensify","intensifying","intension","intensity","intensive","intensively","manipulate","manipulated","manipulates","manipulating","manipulation","manipulations","manipulative","minimise","minimised","minimises","minimising","minimize","minimized","minimizes","minimizing","nuclear","offset","offsets","offsetting","paragraph","paragraphing","paragraphs","plus","pluses","practitioner","practitioners","predominant","predominance","predominantly","predominate","predominated","predominates","predominating","prospect","prospective","prospects","radical","radically","radicals","random","randomly","randomness","reinforce","reinforced","reinforcement","reinforcements","reinforces","reinforcing","restore","restoration","restored","restores","restoring","revise","revised","revises","revising","revision","revisions","schedule","reschedule","rescheduled","reschedules","rescheduling","scheduled","schedules","scheduling","unscheduled","tense","tension","tensely","tenser","tensest","tensions","terminate","terminal","terminals","terminated","terminates","terminating","termination","terminations","theme","themes","thematic","thematically","thereby","uniform","uniformity","uniformly","vehicle","vehicles","via","virtual","virtually","visual","visualise","visualised","visualising","visualisation","visualize","visualized","visualizing","visualization","visually","widespread"]
        sl9=["accommodate","accommodated","accommodates","accommodating","accommodation","analogy","analogies","analogous","anticipate","anticipated","anticipates","anticipating","anticipation","unanticipated","assure","assurance","assurances","assured","assuredly","assures","assuring","attain","attainable","attained","attaining","attainment","attainments","attains","unattainable","behalf","bulk","bulky","cease","ceased","ceaseless","ceases","ceasing","coherent","coherence","coherently","incoherent","incoherently","coincide","coincided","coincides","coinciding","coincidence","coincidences","coincident","coincidental","commence","commenced","commences","commencement","commencing","recommences","recommenced","recommencing","compatible","compatibility","incompatibility","incompatible","concurrent","concurrently","confine","confined","confines","confining","unconfined","controversy","controversies","controversial","controversially","uncontroversial","converse","conversely","device","devices","devote","devoted","devotedly","devotes","devoting","devotion","devotions","diminish","diminished","diminishes","diminishing","diminution","undiminished","distort","distorted","distorting","distortion","distortions","distorts","duration","erode","eroded","erodes","eroding","erosion","ethic","ethical","ethically","ethics","unethical","format","formatted","formatting","formats","found","founded","founder","founders","founding","unfounded","inherent","inherently","insight","insightful","insights","integral","intermediate","manual","manually","manuals","mature","immature","immaturity","maturation","maturational","matured","matures","maturing","maturity","mediate","mediated","mediates","mediating","mediation","medium","military","minimal","minimalisation","minimalise","minimalises","minimalised","minimalising","minimalist","minimalists","minimalistic","minimalization","minimalize","minimalized","minimalizes","minimalizing","minimally","mutual","mutually","norm","norms","overlap","overlapped","overlapping","overlaps","passive","passively","passivity","portion","portions","preliminary","preliminaries","protocol","protocols","qualitative","qualitatively","refine","refined","refinement","refinements","refines","refining","relax","relaxation","relaxed","relaxes","relaxing","restrain","restrained","restraining","restrains","restraint","restraints","unrestrained","revolution","revolutionary","revolutionaries","revolutionise","revolutionised","revolutionises","revolutionising","revolutionist","revolutionists","revolutionize","revolutionized","revolutionizes","revolutionizing","revolutions","rigid","rigidities","rigidity","rigidly","route","routed","routes","routing","scenario","scenarios","sphere","spheres","spherical","spherically","subordinate","subordinates","subordination","supplement","supplementary","supplemented","supplementing","supplements","suspend","suspended","suspending","suspends","suspension","team","teamed","teaming","teams","temporary","temporarily","trigger","triggered","triggering","triggers","unify","unification","unified","unifies","unifying","violate","violated","violates","violating","violation","violations","vision","visions"]
        sl10=["adjacent","albeit","assemble","assembled","assembles","assemblies","assembling","assembly","collapse","collapsed","collapses","collapsible","collapsing","colleague","colleagues","compile","compilation","compilations","compiled","compiles","compiling","conceive","conceivable","conceivably","conceived","conceives","conceiving","inconceivable","inconceivably","convince","convinced","convinces","convincing","convincingly","unconvinced","depress","depressed","depresses","depressing","depression","encounter","encountered","encountering","encounters","enormous","enormity","enormously","forthcoming","incline","inclination","inclinations","inclined","inclines","inclining","integrity","intrinsic","intrinsically","invoke","invoked","invokes","invoking","levy","levies","likewise","nonetheless","notwithstanding","odd","odds","ongoing","panel","panelled","panelling","panels","persist","persisted","persistence","persistent","persistently","persisting","persists","pose","posed","poses","posing","reluctance","reluctant","reluctantly","socalled","straightforward","undergo","undergoes","undergoing","undergone","underwent","whereby"]
        # หาคำที่เหมือนในSublist
        for i in words:
            for j in sl1:
                if i.lower()==j.lower():
                    msl1.append(i.lower())
            for j in sl2:
                if i.lower()==j.lower():
                    msl2.append(i.lower())
            for j in sl3:
                if i.lower()==j.lower():
                    msl3.append(i.lower())
            for j in sl4:
                if i.lower()==j.lower():
                    msl4.append(i.lower())
            for j in sl5:
                if i.lower()==j.lower():
                    msl5.append(i.lower())
            for j in sl6:
                if i.lower()==j.lower():
                    msl6.append(i.lower())
            for j in sl7:
                if i.lower()==j.lower():
                    msl7.append(i.lower())
            for j in sl8:
                if i.lower()==j.lower():
                    msl8.append(i.lower())
            for j in sl9:
                if i.lower()==j.lower():
                    msl9.append(i.lower())
            for j in sl10:
                if i.lower()==j.lower():
                    msl10.append(i.lower())
        # ฟังก์ชันนับจำนวนคำและความถี่ของแต่ละคำ
        def word_count(str):
            counts = dict()
            sword=str.split()
            for word in sword:
                if word in counts:
                    counts[word] += 1
                else:
                    counts[word] = 1
            return counts
        # นับจำนวนคำและความถี่ของแต่ละคำ
        if msl1 != []:
            Nmsl1=" ".join(msl1)
            Nmsl1=word_count(Nmsl1)
            Nmsl1=OrderedDict(sorted(Nmsl1.items()))
            Nnmsl1=len(Nmsl1)
            for i in Nmsl1:
                check=False
                for j in msl1:
                    if (j==i and check==False):
                        Fmsl1 += int(Nmsl1[i])
                        check= True
        if msl2 != []:
            Nmsl2=" ".join(msl2)
            Nmsl2=word_count(Nmsl2)
            Nmsl2=OrderedDict(sorted(Nmsl2.items()))
            Nnmsl2=len(Nmsl2)
            for i in Nmsl2:
                check=False
                for j in msl2:
                    if (j==i and check==False):
                        Fmsl2 += int(Nmsl2[i])
                        check= True
        if msl3 != []:
            Nmsl3=" ".join(msl3)
            Nmsl3=word_count(Nmsl3)
            Nmsl3=OrderedDict(sorted(Nmsl3.items()))
            Nnmsl3=len(Nmsl3)
            for i in Nmsl3:
                check=False
                for j in msl3:
                    if (j==i and check==False):
                        Fmsl3 += int(Nmsl3[i])
                        check= True
        if msl4 != []:
            Nmsl4=" ".join(msl4)
            Nmsl4=word_count(Nmsl4)
            Nmsl4=OrderedDict(sorted(Nmsl4.items()))
            Nnmsl4=len(Nmsl4)
            for i in Nmsl4:
                check=False
                for j in msl4:
                    if (j==i and check==False):
                        Fmsl4 += int(Nmsl4[i])
                        check= True
        if msl5 != []:
            Nmsl5=" ".join(msl5)
            Nmsl5=word_count(Nmsl5)
            Nmsl5=OrderedDict(sorted(Nmsl5.items()))
            Nnmsl5=len(Nmsl5)
            for i in Nmsl5:
                check=False
                for j in msl5:
                    if (j==i and check==False):
                        Fmsl5 += int(Nmsl5[i])
                        check= True
        if msl6 != []:
            Nmsl6=" ".join(msl6)
            Nmsl6=word_count(Nmsl6)
            Nmsl6=OrderedDict(sorted(Nmsl6.items()))
            Nnmsl6=len(Nmsl6)
            for i in Nmsl6:
                check=False
                for j in msl6:
                    if (j==i and check==False):
                        Fmsl6 += int(Nmsl6[i])
                        check= True
        if msl7 != []:
            Nmsl7=" ".join(msl7)
            Nmsl7=word_count(Nmsl7)
            Nmsl7=OrderedDict(sorted(Nmsl7.items()))
            Nnmsl7=len(Nmsl7)
            for i in Nmsl7:
                check=False
                for j in msl7:
                    if (j==i and check==False):
                        Fmsl7 += int(Nmsl7[i])
                        check= True
        if msl8 != []:
            Nmsl8=" ".join(msl8)
            Nmsl8=word_count(Nmsl8)
            Nmsl8=OrderedDict(sorted(Nmsl8.items()))
            Nnmsl8=len(Nmsl8)
            for i in Nmsl8:
                check=False
                for j in msl8:
                    if (j==i and check==False):
                        Fmsl8 += int(Nmsl8[i])
                        check= True
        if msl9 != []:
            Nmsl9=" ".join(msl9)
            Nmsl9=word_count(Nmsl9)
            Nmsl9=OrderedDict(sorted(Nmsl9.items()))
            Nnmsl9=len(Nmsl9)
            for i in Nmsl9:
                check=False
                for j in msl9:
                    if (j==i and check==False):
                        Fmsl9 += int(Nmsl9[i])
                        check= True
        if msl10 != []:
            Nmsl10=" ".join(msl10)
            Nmsl10=word_count(Nmsl10)
            Nmsl10=OrderedDict(sorted(Nmsl10.items()))
            Nnmsl10=len(Nmsl10)
            for i in Nmsl10:
                check=False
                for j in msl10:
                    if (j==i and check==False):
                        Fmsl10 += int(Nmsl10[i])
                        check= True
        # จำนวนคำทั้งหมด
        aword=len(aword)
        # จำนวนคำที่มีใน Sublistทั้งหมด
        asword = Fmsl1+Fmsl2+Fmsl3+Fmsl4+Fmsl5+Fmsl6+Fmsl7+Fmsl8+Fmsl9+Fmsl10
        # %ของจำนวนคำที่มีใน Sublistเทียบกับทั้งหมด
        aswordp = "{:.4f}".format((asword*100)/aword)
    # test=""
    # test=test.split("“")
    # test="\"".join(test)
    # test=test.split("”")
    # test=("\"").join(test)
    return render_template('matching.html',form=form,message=message,
    msl1=msl1,msl2=msl2,msl3=msl3,msl4=msl4,msl5=msl5,msl6=msl6,msl7=msl7,msl8=msl8,msl9=msl9,msl10=msl10,
    Nmsl1=Nmsl1,Nmsl2=Nmsl2,Nmsl3=Nmsl3,Nmsl4=Nmsl4,Nmsl5=Nmsl5,Nmsl6=Nmsl6,Nmsl7=Nmsl7,Nmsl8=Nmsl8,Nmsl9=Nmsl9,Nmsl10=Nmsl10,
    Nnmsl1=Nnmsl1,Nnmsl2=Nnmsl2,Nnmsl3=Nnmsl3,Nnmsl4=Nnmsl4,Nnmsl5=Nnmsl5,Nnmsl6=Nnmsl6,Nnmsl7=Nnmsl7,Nnmsl8=Nnmsl8,Nnmsl9=Nnmsl9,Nnmsl10=Nnmsl10,
    Fmsl1=Fmsl1,Fmsl2=Fmsl2,Fmsl3=Fmsl3,Fmsl4=Fmsl4,Fmsl5=Fmsl5,Fmsl6=Fmsl6,Fmsl7=Fmsl7,Fmsl8=Fmsl8,Fmsl9=Fmsl9,Fmsl10=Fmsl10,
    aword=aword,asword=asword,aswordp=aswordp)


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
