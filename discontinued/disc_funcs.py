plates=['hh']
drums=['bd','sn']
class voice_split:
    def plates_drums(pattern):
        voicing_1=[]
        voicing_2=[]
        i2=0
        for inst in pattern.inst_lines:
            if inst in plates:
                for d in pattern.inst_lines[inst]: #d-> duration
                    if ('r' not in d) : 
                        voicing_1.append(f"{inst}{d}")
                    else :voicing_1.append(f"{d}")
            elif(i2!=0):
                for d in pattern.inst_lines[inst]:
                    a=""
                    b=""
                    for i in voicing_2[i2]:
                        if i.isdigit():
                            b+=i
                        else:a+=i
                    i2=0
                    if ('r' not in d) and ('r' in voicing_2[i2]):
                        voicing_2[i2]=f"{inst}{d}"
                    elif ('r' not in d) and ('r' not in voicing_2[i2]):
                        voicing_2[i2]=f"<{inst} {a}>{b}"
                    elif ('r' in d) and ('r' in voicing_2[i2]):
                        voicing_2[i2]=f"{d}"
                        print(d)
                    i2+=1
            else:
                for d in pattern.inst_lines[inst]: #d-> duration
                    if ('r' not in d) : 
                        voicing_2.append(f"{inst}{d}")
                    else :voicing_2.append(f"{d}")
                i2=-1
        return(voicing_1,voicing_2)

#Padrão
class pattern:
    def __init__(self):
        self.ID=""
        self.tempo = 120
        self.sig = "4/4"
        self.inst_lines = {}

#                              modos de voicing
#single voicing
#dual voicing plates-v1 drums-v2 default para já
#dual voicing feet-v1 hands-v2



# Code generation
    
export_type={}
export_type['MIDI']="\midi{}"
export_type['PDF']="\layout{}"
    
def apply_export(export,patternlist):
    target_prog="\\version \"2.24.2\"\n"
    pattern=patternlist[export[0]]
    #criar header patterns para cada voz
    voice_mode='plates_drums'# depois ver outros modos de voices
    if voice_mode=='plates_drums':
        v1,v2=voice_split.plates_drums(pattern)#separar as vozes
    voiceone=f"{pattern.ID}vo" # tem que ser vo(voice one) e vt(voice two) porque o lilypond nao aceita numeros no nome
    target_prog += f"{pattern.ID}vo = \drummode "+"{"
    for note in v1:
        target_prog += f"{note} "
    target_prog+="}\n"
    voicetwo=f"{pattern.ID}vt"
    target_prog += f"{pattern.ID}vt = \drummode "+"{"
    for note in v2:
        target_prog += f"{note} "
    target_prog+="}\n\score{\n\\new DrumStaff <<\n" #começar "main"
    target_prog+=f"\\tempo 4 = {pattern.tempo}\n" #aplicar tempo
    target_prog+=f"\\time {pattern.sig}\n"
    target_prog+=f"\\new DrumVoice"+"{\\voiceOne"+f"\\{voiceone}"+"}\n"
    target_prog+=f"\\new DrumVoice"+"{\\voiceTwo"+f"\\{voicetwo}"+"}"
    target_prog+=">>\n"
    target_prog+=f"{export_type[export[2]]}"+"}"
#                               Escrever target file
    out = open(f"out/out_{pattern.ID}.ly", "w")
    out.write(target_prog)
    out.close()
    return(target_prog)