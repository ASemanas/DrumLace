import math
from fractions import Fraction
import sys

user=str(sys.argv[2])
user=user.split("//tmp/")[1]

class pattern:
    def __init__(self):
        self.ID=""
        self.tempo = 120
        self.sig = "4/4"
        self.inst_lines = {}
    def copy(self,pattern):
        self.ID=f'{pattern.ID}_copy'
        self.tempo = pattern.tempo
        self.sig = pattern.sig
        self.inst_lines=pattern.inst_lines.copy()
        return(self)
    

export_type={}
export_type['MIDI']="\midi{}"
export_type['WAV']="\midi{}"
export_type['Play']="\midi{}"
export_type['PDF']="\layout{}"

def calc_time(inst_line): #calcula o tempo de cada linha de inst
    valuelist=[]
    total_time=0
    for note in inst_line:
        mult=1
        if (note[0]=='r'):
            note=note[1:]
        elif (note[0]=='t'):
            note=int(note.split("[")[1][1])/2
        elif (note[0]=='d'):
            note=note[1:]  
            mult=1.5 
        a=(1/int(note))*mult # duração da nota
        valuelist.append(a)
        total_time+=a
    if not len(inst_line):
        total_time=0
    return(total_time)

# faz padding para que todas as linhas tenham o tamanho da maior
def pad (inst_lines,time_sig): 
    time=[]
    inst_number={}
    i=0
    a,b=time_sig.split('/')
    b=1/float(b)
    bar_time=float(a)*b #tempo de um compasso (1=wholenote/semibreve)
    for inst in inst_lines:
        time.append((calc_time(inst_lines[inst]),i))
        inst_number[i]=inst
        i+=1
    #print(time)
    ref=max(time)#maior linha
    #print(ref)
    i=0
    for inst in inst_lines:
        pad=0
        dif=ref[0]-time[i][0]
        #if ((time[i][0]==ref[0]) and (time[i][1]==ref[0])):
        #    print("yo")
        if time[i][0]<=ref[0]:
            if dif>=bar_time:
                #print(time_sig)
                match (time_sig):
                    case '4/4':
                        pad=math.floor(dif/bar_time)
                        j=0
                        while j<pad:
                            inst_lines[inst].append(f"r1")
                            j+=1
        p=frac_decomp(dif-pad)
        for fr in p:
            inst_lines[inst].append(f"r{fr}")
        #print(inst,pad)
        i+=1

#decomposição de frações greedy algorithm for egypcian fractions com alteração
#para ser tudo par
def frac_decomp(number):
    nr=Fraction(number).numerator
    dr=Fraction(number).denominator
    fr_list=[]#lista de frações
    while nr!=0:
        x= math.ceil(dr/nr)
        if x%2 !=0 :
            x-=1
        if (x>0):
            fr_list.append(x)
        nr = x*nr-dr
        dr=dr*x
    return(fr_list)

#falta fazer função de espaços em branco para sequencia
inst_list=['hh','bd','sn','tomfl','cymc']
def patterns(pattern):#cria as linhas de notas para o "header"
    target_prog=""
    voices=[]
    for inst in pattern.inst_lines.keys():
        voices.append(inst)
    for voice in voices:
        target_prog += f"{pattern.ID}_{voice} = \drummode " +"{"
        if voice not in inst_list:
            voicet=voice[:-1]
        else:
            voicet=voice
        for note in pattern.inst_lines[voice]:
            if note[0] == "t":#grouping/tuplets
               tempstr=f"\\tuple"
               tempstr+=str(note.split("[")[0])
               tempstr+="{"
               a=note.split("[")[1].split("'")
               for i in range(1,len(a),2):
                   if a[i][0]!="r":
                    tempstr+=f"{voicet}{a[i]} "
                   else:
                    tempstr+=f"s{a[i][1:]} "
               tempstr+="}"
               target_prog += tempstr
            elif note[0] == "d":
                target_prog += f"{voicet}{note[1:]}. " #hit
            elif note[0] != "r":
                target_prog += f"{voicet}{note} " #hit
            else: target_prog += f"s{note[1:]} "# pausa
        target_prog+="}\n"
    return(target_prog,voices)

def compare_voices(voice1,voice2):#compara as vozes para ver se já existem ou não
    for i in voice2:
        if i not in voice1:
            voice1.append(i)

def export_ly (export,patternlist):#cria ficheiros LilyPond
    target_prog="\\version \"2.24.2\"\n"
    pattern=patternlist[export[0]]
    voice1=patterns(pattern[0])[1]
    for pat in pattern: 
        compare_voices(voice1,patterns(pat)[1])#criar um array de vozes geral
    for pat in pattern: 
        for voice in voice1:
            if voice not in pat.inst_lines:
                pat.inst_lines[voice]=[]
        pad(pat.inst_lines,pat.sig)
    for pat in pattern:  
        target_prog+=patterns(pat)[0]
    target_prog+="\score{\n\\new DrumStaff \\with { drumStyleTable = #weinberg-drums-style } <<\n" #começar "main"
    target_prog+=f"\\voices 1"
    for i in range(len(voice1)-1):
          target_prog += f",{i+2}"
    for i in voice1:
        on=0
        target_prog+="\n{"
        for pat in pattern:
            if i in pat.inst_lines and on==0:
                target_prog +=f"\\shiftOff\\tempo 4 = {pat.tempo}\\time {pat.sig}\\{pat.ID}_{i}"
                on=1
            elif i in pat.inst_lines:
                #print(pat.ID,pat.sig)
                target_prog +=f"\\tempo 4 = {pat.tempo}\\time {pat.sig}\\{pat.ID}_{i}"
        target_prog+="}"
    target_prog+=">>\n"
    target_prog+=f"{export_type[export[2]]}"+"}"
#                               Escrever target file
    out = open(f"out/{user}pattern{export[2]}.ly", "w")
    out.write(target_prog)
    out.close()
    #print(target_prog)
    return(target_prog)
 
def export_sh (export,patternlist):#cria ficheiros Shell
    shell="#!/bin/bash\n\nly=\"./lilypond-2.24.2/bin/lilypond \"\n\n"
    export_path=f"{export[1]}"
    export_type=export[2]
    #pattern=patternlist[export[0]]
    ID=f"{user}pattern"+f"{export_type}"
    shell+=f"target='./out/{ID}.ly'\n"
    shell+=f"$ly -o {export_path} $target"
    if (export_type=='WAV'):
        shell+=f";fluidsynth ./soundfonts/GM.sf2 -g 5 -F {export_path}/{ID}.wav {export_path}/{ID}.midi"
        shell+=f";rm {export_path}/{ID}.midi"
    if (export_type=='Play'):
        shell+=f";fluidsynth ./soundfonts/GM.sf2 -g 5 -F {export_path}/{ID}.wav {export_path}/{ID}.midi"
        shell+=f";aplay {export_path}/{ID}.wav"
        shell+=f";rm {export_path}/{ID}.midi"
        shell+=f";rm {export_path}/{ID}.wav"
    shell += ";rm $target"
    out = open(f"out/shell/{ID}.sh", "w")
    #print(shell)
    out.write(shell)
    out.close()