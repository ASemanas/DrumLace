from lark import *
from aux import pattern
from string import ascii_lowercase
from lark.tree import pydot__tree_to_png
from funcs import alg_function
import sys
#                            funçoes auxiliares do visitor
def nsaux(note_length,instrument,tree): #sequencia de notas num array so serve para quialtras
    global ID
    notes=[]
    for i in tree.children:
        if (i=='X' or i=='x'):
            notes.append(str(int(note_length)*2))
        elif (i=='.'):
            notes.append(f"r{int(note_length)*2}")
        elif(i.data=="tuplet"):
            notes.append(tuplet(note_length,instrument,tree))
    return notes

def tuplet(note_length,instrument,tree):
    l=len(tree.children)
    str=nsaux(note_length,instrument,tree)
    tupstr=f"t{l}/2{str}"
    patternlist[ID][index].inst_lines[instrument].append(tupstr)
    return(tupstr)

def noteseq(note_length,instrument,tree):
    global ID,index
    for i in tree.children:
        if (i=='X' or i=='x'):
            patternlist[ID][index].inst_lines[instrument].append(str(note_length))
        elif (i=='.'):
            patternlist[ID][index].inst_lines[instrument].append(f"r{note_length}")
        elif (i=='d' or i=='D'):
            patternlist[ID][index].inst_lines[instrument].append(f"d{note_length}")
        elif(i.data=="tuplet"):
            tuplet(note_length,instrument,i)

def notes(instrument,self,tree):
        global patterns
        for i in range(0,len(tree.children),2):
            note_length=tree.children[i]
            noteseq(note_length,instrument,tree.children[i+1])
            
#                                VISITOR

patternlist={}
exportlist=[]

class PatternProg(Visitor):
    def pattern_asg(self,tree):
        global patterns,ID
        id=pattern()
        ID=str(tree.children[0])
        id.ID = ID
        patternlist[ID]= [id]

    def identity(self,tree):
        target=tree.children[0]
        patternlist[ID]=patternlist[target].copy()

    def drum_description (self,tree):
        global patterns,ID,index,orig_ID
        index=0
        orig_ID=ID
        patternlist[ID][index].sig=str(tree.children[0])
        patternlist[ID][index].tempo = int(tree.children[1])

    def instrument_lines (self,tree):
        global patterns,inst_index,index
        for j in range(0,len(tree.children),2):
            inst = str(tree.children[j]).lower()
            if inst not in patternlist[ID][index].inst_lines.keys():
                inst_index=-1
                patternlist[ID][index].inst_lines[inst]=[]
            else:
                inst_index+=1
                inst=f'{inst}{ascii_lowercase[inst_index]}'
                patternlist[ID][index].inst_lines[inst]=[]
            notes(inst,self,tree.children[j+1])
    
    def new_time (self,tree):
        global patterns,ID,index,orig_ID
        index+=1
        #nota cada um acresecenta uma letra ao anterior padrao,padraoa,padraoab etc...
        id=pattern()
        ID=f'{orig_ID}{ascii_lowercase[index-1]}'
        id.ID = ID
        ID=orig_ID
        patternlist[orig_ID].append(id)
        patternlist[ID][index]= id
        patternlist[ID][index].sig=str(tree.children[0])
        patternlist[ID][index].tempo = int(tree.children[1])
        #patternlist[orig_ID].append(id)
        #print(patternlist)

    def export (self,tree):
        global exportlist
        match(len(tree.children[1].children)):
            case(2):
                for j in range(0,len(tree.children),2):
                    id = tree.children[j]
                    file_path = tree.children[j+1].children[0]
                    file_path=file_path.replace("'",'')
                    file_type = tree.children[j+1].children[1]
                    exportlist.append((str(id),str(file_path),str(file_type))) 
            case (1):
                for j in range(0,len(tree.children),2):
                    id = tree.children[j]
                    file_path = f"./out"
                    file_type = tree.children[j+1].children[0]
                    exportlist.append((str(id),str(file_path),str(file_type))) 
            case (0):
                for j in range(0,len(tree.children),2):
                    id = tree.children[j]
                    file_path = f"./out"
                    file_type = "PDF"
                    exportlist.append((str(id),str(file_path),str(file_type))) 
                    file_type = "MIDI"
                    exportlist.append((str(id),str(file_path),str(file_type)))
                    file_type = "WAV"
                    exportlist.append((str(id),str(file_path),str(file_type)))  
    
    def play (self,tree):
        global exportlist
        for j in range(0,len(tree.children)):
            id = tree.children[j]
            file_path='./out'
            file_type='Play'
            exportlist.append((str(id),str(file_path),str(file_type)))
            
    def concatenation2(self,tree):
        global patterns,ID,conc_count
        conc_count=0
        match (str(type(tree.children[0])),str(type(tree.children[1]))):
            case ("<class 'lark.tree.Tree'>","<class 'lark.lexer.Token'>"):
                #print(str(type(tree.children[0])))
                c=PatternProg().visit_topdown(tree.children[0])
                tree.children[0]=ID
            case("<class 'lark.lexer.Token'>","<class 'lark.tree.Tree'>"):
                c=PatternProg().visit_topdown(tree.children[1])
                tree.children[1]=ID
            case("<class 'lark.tree.Tree'>","<class 'lark.tree.Tree'>"):
                c=PatternProg().visit_topdown(tree.children[0])
                tree.children[0]=ID
                c=PatternProg().visit_topdown(tree.children[1])
                tree.children[1]=ID
            case ("<class 'lark.lexer.Token'>","<class 'lark.lexer.Token'>"):
                pass
            case _:
                print("Error concat children not a Token or A Tree")     
        conc_count+=1
        a_s=str(tree.children[0])
        b_s=str(tree.children[1])
        a=[]
        for i in patternlist[a_s]:
            a_tmp=pattern()
            a_tmp=pattern.copy(a_tmp,i)
            a.append(a_tmp)
        b=[]
        for j in patternlist[b_s]:
            b_tmp=pattern()
            b_tmp=pattern.copy(b_tmp,j)
            b.append(b_tmp)
        #print(a[0].sig)
        c=pattern()
        c=pattern.copy(c,a[0])
        c.ID=ID
        patternlist[ID]=[]
        patternlist[ID].append(c)
        for i in a[1:]:
            #i.ID=f'{ID}_{i.ID}'
            patternlist[ID].append(i)
        for j in b:
            #i.ID=f'{ID}_{i.ID}'
            patternlist[ID].append(j)
    def parallel2(self,tree):
        match (str(type(tree.children[0])),str(type(tree.children[1]))):
            case ("<class 'lark.tree.Tree'>","<class 'lark.lexer.Token'>"):
                #print(str(type(tree.children[0])))
                c=PatternProg().visit_topdown(tree.children[0])
                tree.children[0]=ID
            case("<class 'lark.lexer.Token'>","<class 'lark.tree.Tree'>"):
                c=PatternProg().visit_topdown(tree.children[1])
                tree.children[1]=ID
            case("<class 'lark.tree.Tree'>","<class 'lark.tree.Tree'>"):
                c=PatternProg().visit_topdown(tree.children[0])
                tree.children[0]=ID
                c=PatternProg().visit_topdown(tree.children[1])
                tree.children[1]=ID
            case ("<class 'lark.lexer.Token'>","<class 'lark.lexer.Token'>"):
                pass
            case _:
                print("Error parallel children not a Token or A Tree")
        a_s=str(tree.children[0])
        b_s=str(tree.children[1])
        a=[]
        for i in patternlist[a_s]:
            a_tmp=pattern()
            a_tmp=pattern.copy(a_tmp,i)
            a.append(a_tmp)
        b=[]
        for j in patternlist[b_s]:
            b_tmp=pattern()
            b_tmp=pattern.copy(b_tmp,j)
            b.append(b_tmp)
        for i in range(len(b)):
            for inst in b[i].inst_lines:
                if inst in a[i].inst_lines:
                    a[i].inst_lines[f'{inst}p']=b[i].inst_lines[inst]
                else:
                    a[i].inst_lines[inst]=b[i].inst_lines[inst]
        #print(a[0].inst_lines)
        patternlist[ID]=a
    def looping(self,tree):
        global ID,loop_count
        loop_count=0
        match (str(type(tree.children[0]))):
            case "<class 'lark.tree.Tree'>":
                #print ("Tree")
                c=PatternProg().visit_topdown(tree.children[0])
                tree.children[0]=ID
                #print(c)
            case "<class 'lark.lexer.Token'>":
                #print(type(tree.children[0])==Token)
                pass
            case _:
                print("Error looping children not a Token or A Tree")
        pat=patternlist[str(tree.children[0])]
        Num=int(tree.children[1])
        c=pattern()
        c.ID=ID
        patternlist[ID]=[]
        for p in pat:
            c=pattern()
            c=pattern.copy(c,p)
            patternlist[ID].append(c)
        for i in range(Num-1):
            j=0
            for p in pat:
                a=pattern()
                a=pattern.copy(a,p)
                a.ID=f'{ID}_{ascii_lowercase[i]}{ascii_lowercase[j]}'
                patternlist[ID].append(a)
                j+=1
        #print(patternlist)

    def func(self,tree):
        global ID
        func_ID=tree.children[0]
        args=[]
        ch_i=0
        for child in tree.children[1:]:
            ch_i+=1
            match str(type(child)):
                case "<class 'lark.lexer.Token'>":
                    match (child.type):
                        case 'ID':
                            args.append(patternlist[str(child)])
                        case 'INT':
                            args.append(int(child))
                        case 'DECIMAL':
                            args.append(float(child))
                case "<class 'lark.tree.Tree'>":
                    PatternProg().visit_topdown(child)
                    tree.children[ch_i]=ID
                    args.append(patternlist[ID])
        pat=pattern()
        pat=alg_function.find_f(func_ID,args)
        pat[0].ID=ID
        patternlist[ID]=pat
        #print(pat)