import re,math
from fractions import Fraction

class pattern:
    def __init__(self):
        self.ID=""
        self.tempo = 120
        self.sig = "4/4"
        self.inst_lines = {}
        self.ly = ""

export_type={}
export_type['MIDI']="\midi{}"
export_type['WAV']="\midi{}"
export_type['Play']="\midi{}"
export_type['PDF']="\layout{}"

def calc_time(inst_line): #calcula o tempo de cada linha de inst
    valuelist=[]
    total_time=0
    for note in inst_line:
        if (note[0]=='r'):
            note=note[1:]
        elif (note[0]=='t'):
            note=note.split("[")[1][1]
        elif (note[0]=='d'):
            note=note[1:]
        a=(1/int(note))*1.5 # duração da nota
        valuelist.append(a)
        total_time+=a
    return(total_time)

# faz padding para que todas as linhas tenham o tamanho da maior
def pad (inst_lines,time_sig): 
    time=[]
    inst_number={}
    i=0
    a,b=time_sig.split('/')
    b=1/float(b)
    bar_time=float(a)*b #tempo de um compasso (1=wholenote/semibreve)
    #print(bar_time)
    for inst in inst_lines:
        time.append((calc_time(inst_lines[inst]),i))
        inst_number[i]=inst
        i+=1
    ref=max(time)#maior linha
    #print(f'ref:{ref}')
    i=0
    for inst in inst_lines:
        pad=0
        if ((time[i][0]==ref[0])and (time[i][1]==ref[0])):
            print("yo")  
        if time[i][0]<ref[0]:
            dif=ref[0]-time[i][0]
            #print(f"dif:{dif}")
            if dif>bar_time:
                pad=math.floor(dif/bar_time)
                j=0
                while j<pad:
                    inst_lines[inst].append(f"r1")
                    j+=1
            p=frac_decomp(dif-pad)
            for fr in p:
                inst_lines[inst].append(f"r{fr}")
            #print(inst_lines[inst])
        i+=1
    #print("end of cycle")

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
        fr_list.append(x)
        nr = x*nr-dr
        dr=dr*x
    return(fr_list)

def export_ly(export,patternlist):
    target_prog="\\version \"2.24.2\"\n"
    pattern=patternlist[export[0]]
    #criar header patterns para cada voz
    voices=[]
    for inst in pattern.inst_lines.keys():
        voices.append(inst)
    for voice in voices:
        target_prog += f"{pattern.ID}{voice} = \drummode " +"{"
        for note in pattern.inst_lines[voice]:
            if note[0] == "t":#grouping/tuplets
               tempstr=f"\\tuple"
               tempstr+=str(note.split("[")[0])
               tempstr+="{"
               a=note.split("[")[1].split("'")
               for i in range(1,len(a),2):
                   if a[i][0]!="r":
                    tempstr+=f"{voice}{a[i]} "
                   else:
                    tempstr+=f"{a[i]} "
               tempstr+="}"
               target_prog += tempstr
            elif note[0] == "d":
                target_prog += f"{voice}{note[1:]}. " #hit
            elif note[0] != "r":
                target_prog += f"{voice}{note} " #hit
            else: target_prog += f"s{note[1:]} "# pausa
        target_prog+="}\n"
    target_prog+="\score{\n\\new DrumStaff \\with { drumStyleTable = #weinberg-drums-style } <<\n" #começar "main"
    target_prog+=f"\\tempo 4 = {pattern.tempo}\n\\time {pattern.sig}\n\\voices 1"
    for i in range(len(voices)-1):
        target_prog += f",{i+2}"
    target_prog+="\n"
    for voice in voices:
        target_prog += "{"+f"\\shiftOn\\{pattern.ID}{voice}"+"}\n"
    target_prog+=">>\n"
    target_prog+=f"{export_type[export[2]]}"+"}"
#                               Escrever target file
    out = open(f"out/{pattern.ID}{export[2]}.ly", "w")
    out.write(target_prog)
    out.close()
    #print(target_prog)
    return(target_prog)

def export_sh (export,patternlist):
    shell="#!/bin/bash\n\nly=\"./lilypond-2.24.2/bin/lilypond \"\n\n"
    export_path=f"{export[1]}"
    export_type=export[2]
    pattern=patternlist[export[0]]
    ID=pattern.ID+f"{export_type}"
    shell+=f"target='./out/{ID}.ly'\n"
    shell+=f"$ly -o {export_path} $target"
    if (export_type=='WAV'):
        shell+=f";fluidsynth -g 5 -F {export_path}/{ID}.wav {export_path}/{ID}.midi"
        shell+=f";rm {export_path}/{ID}.midi"
    if (export_type=='PDF'):
        shell += f";xdg-open {export_path}/{ID}.pdf"
    if (export_type=='Play'):
        shell+=f";fluidsynth -g 5 -F {export_path}/{ID}.wav {export_path}/{ID}.midi"
        shell+=f";aplay {export_path}/{ID}.wav"
        shell+=f";rm {export_path}/{ID}.midi"
        shell+=f";rm {export_path}/{ID}.wav"
    shell += ";rm $target"
    out = open(f"out/shell/{ID}{export_type}.sh", "w")
    out.write(shell)
    out.close()