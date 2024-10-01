from aux import pattern

class alg_function:
    def find_f(func_id,args):
        return(function_list[func_id](args))
    def reverse(args):
        if len (args)>1:
            print('warning reverse only takes 1 argument but more were given')
        pat=[]
        for p in range(len(args[0])-1,-1,-1):
            patt=pattern()
            patt=pattern.copy(patt,args[0][p])
            pat.append(patt)
        for i in range(len(pat)-1,-1,-1):
            for inst in pat[i].inst_lines:
                temp_list=[]
                for j in range(len(pat[i].inst_lines[inst])-1,-1,-1):
                    temp_list.append(pat[i].inst_lines[inst][j])
                pat[i].inst_lines[inst]=temp_list
        return pat
    def change_speed(args):
        pat=[]
        speed_var=args[1]
        for p in args[0]:
            patt=pattern()
            patt=pattern.copy(patt,p)
            patt.tempo=int(patt.tempo*speed_var)
            pat.append(patt)
        return pat

       
function_list={}
function_list['rev']=alg_function.reverse
function_list['scale']=alg_function.change_speed