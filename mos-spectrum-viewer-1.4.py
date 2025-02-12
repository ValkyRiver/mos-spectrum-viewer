# MOS Spectrum Viewer 1.4 by Valky River

from tkinter import *
import math
import colorsys
import winsound

def beep(mode, L, s, Lstep, sstep):
    current = 0
    winsound.Beep(440, 600)
    for ls in mode:
        if ls == "L":
            current += Lstep
        else:
            current += sstep
        winsound.Beep(int(440 * 2**(current/((L*Lstep)+(s*sstep)))), 600)

def invertgen(gen):
    if gen == "bright":
        return "dark"
    else:
        return "bright"

horizontalscale = 1440
verticalscale = 480
horizontalbuffer = 60
verticalbuffer = 120
textsize = 8

root = Tk()
C = Canvas(root)
C.pack(fill=BOTH, expand=1)
root.geometry(str(horizontalscale + horizontalbuffer*2) + "x" + str(verticalscale + verticalbuffer + 160))
root.title("MOS Spectrum Viewer")

def mos(L=5, s=2, tetlimit=55, gen="bright", mode=3, Lstep=2, sstep=1):

    # reset any previous calls of this function
    C.delete("all")

    # calculate step pattern (in its darkest mode)
    period = 1200 / math.gcd(L, s)
    steps = []; smalls = []
    for sm in range(s):
        smalls.append(int((L+s)/s * sm))
    for st in range(L+s):
        if st in smalls:
            steps.append("s")
        else:
            steps.append("L")

    # calculate generators
    L1 = int(L / math.gcd(L, s)); s1 = int(s / math.gcd(L, s))
    steps2 = steps + steps
    brightgenerator = -1; darkgenerator = -1
    brights = -1; darks = -1
    for size in range(1, L1+s1):
        composites = []; a = 0
        for pos in range(L1+s1):
            composites.append(sorted(steps2[pos:pos+size]))
            if len(composites) >= 1:
                if tuple(composites[0]) == tuple(sorted(steps2[pos:pos+size])):
                    a += 1
        if a == 1:
            brightgenerator = size
            brights = composites[-1].count("s")
        if a == L1+s1 - 1:
            darkgenerator = size
            darks = composites[0].count("s")
    equalizedbright = 1200/(L+s) * brightgenerator
    collapsedbright = 1200/L * (brightgenerator-brights)
    equalizeddark = 1200/(L+s) * darkgenerator
    collapseddark = 1200/L * (darkgenerator-darks)

    if gen == "bright":
        generator = brightgenerator
        lowerlimit = min(equalizedbright, collapsedbright)
        upperlimit = max(equalizedbright, collapsedbright)
        if equalizedbright > collapsedbright:
            collapsedside = "left"
        else:
            collapsedside = "right"
    elif gen == "dark":
        generator = darkgenerator
        lowerlimit = min(equalizeddark, collapseddark)
        upperlimit = max(equalizeddark, collapseddark)
        if equalizeddark > collapseddark:
            collapsedside = "left"
        else:
            collapsedside = "right"

    # calculate modes, ordered dark to bright
    modes = []
    for m in range(L+s):
        modes.append(steps2[((m*darkgenerator)%(L+s)):((m*darkgenerator)%(L+s))+L+s])

    # render left side cents
    C.create_polygon(0,0,0,verticalscale+360,horizontalscale + 480,verticalscale+360,horizontalscale + 480,0, outline="#FFF", fill="#FFF", width=0)
    C.create_text(horizontalbuffer + horizontalscale - 8.3*textsize, verticalbuffer - 12*textsize, text="MOS Spectrum Viewer 1.4", font=("Arial", int(textsize), "bold"))
    C.create_text(horizontalbuffer + horizontalscale - 4.3*textsize, verticalbuffer - 10.4*textsize, text="by Valky River", font=("Arial", int(textsize), "bold"))
    C.create_text(horizontalbuffer + horizontalscale - 13.8*textsize, verticalbuffer - 5*textsize, text=str(L)+"L "+str(s)+"s SPECTRUM", font=("Arial", int(2.5*textsize), "bold"))
    C.create_text(horizontalbuffer + horizontalscale/2, verticalbuffer - 4.2*textsize, text="Size of generator (cents)", font=("Arial", int(1.5*textsize), "bold"))
    C.create_text(horizontalbuffer + horizontalscale/2, verticalscale + verticalbuffer + textsize*9.6, text="TETs (up to "+str(tetlimit)+")", font=("Arial", int(1.5*textsize), "bold"))
    C.create_text(horizontalbuffer-42, verticalbuffer + verticalscale/2, text="Interval size (in cents)", font=("Arial", int(1.5*textsize), "bold"), angle = 90, fill="#CCC")
    for c1 in range(13):
        C.create_line(horizontalbuffer, ((verticalscale/12)*c1 + verticalbuffer), horizontalscale+horizontalbuffer, (40*c1 + verticalbuffer), fill="#DDD", width=3)
        if c1 == 12:
            C.create_text(horizontalbuffer - 1.6*textsize, ((verticalscale/12)*c1 + verticalbuffer), text=str(1200 - 100*c1), font=("Arial", textsize, "bold"), fill="#CCC")
        elif c1 >= 3:
            C.create_text(horizontalbuffer - 2.3*textsize, ((verticalscale/12)*c1 + verticalbuffer), text=str(1200 - 100*c1), font=("Arial", textsize, "bold"), fill="#CCC")
        else:
            C.create_text(horizontalbuffer - 2.6*textsize, ((verticalscale/12)*c1 + verticalbuffer), text=str(1200 - 100*c1), font=("Arial", textsize, "bold"), fill="#CCC")

    # render generator cents
    centsshow = math.ceil((upperlimit - lowerlimit) / (textsize*5))
    for integercent in range(math.ceil(lowerlimit / centsshow), int(upperlimit / centsshow) + 1):
        C.create_text(horizontalscale*(((integercent*centsshow)-lowerlimit)/(upperlimit-lowerlimit)) + horizontalbuffer, verticalbuffer - 1.6*textsize, text=str(integercent*centsshow), font=("Arial", textsize, "bold"), fill="#000")

    # render modes
    collapseddegs = [0]
    for ind, ls in enumerate(modes[mode-1]):
        if ls == "L":
            collapseddegs.append(collapseddegs[ind] + 1)
        else:
            collapseddegs.append(collapseddegs[ind])
    for note in range(L+s+1):
        n = (note/(L+s) + 0.7) % 1
        tup = colorsys.hsv_to_rgb(n, 0.5, (math.sin(2*math.pi*(n + (4/7)))/13) + (12/13))
        hx = []
        for elem in tup:
            if int(elem*255) <= 15:
                hx.append("0"+((str(hex(int(elem*255))).upper()+"d")[2:-1]))
            else:
                hx.append((str(hex(int(elem*255))).upper()+"d")[2:-1])
        modecolor = "#"+"".join(hx)
        if collapsedside == "left":
            C.create_line(horizontalbuffer, verticalbuffer + verticalscale-((verticalscale/L)*collapseddegs[note]), horizontalbuffer+horizontalscale, verticalbuffer + verticalscale-((verticalscale/(L+s))*note), fill=modecolor, width=3)
        else:        
            C.create_line(horizontalbuffer, verticalbuffer + verticalscale-((verticalscale/(L+s))*note), horizontalbuffer+horizontalscale, verticalbuffer + verticalscale-((verticalscale/L)*collapseddegs[note]), fill=modecolor, width=3)
            
    # render tets
    gensizes = []; gensizeamounts = []; nonmos = []
    for TET in range(1, tetlimit+1):
        draw = False
        hasgen = False
        for step in range(TET):
            if round((1200 / TET) * step, 8) >= round(lowerlimit, 8) and round((1200 / TET) * step, 8) <= round(upperlimit, 8) and TET % math.gcd(L, s) == 0:
                hasgen = True
                if round((1200 / TET) * step, 8) in gensizes:
                    gensizeamounts[gensizes.index(round((1200 / TET) * step, 8))] += 1
                    x = horizontalscale*((((1200 / TET) * step)-lowerlimit)/(upperlimit-lowerlimit)) + horizontalbuffer
                    if round((1200 / TET) * (step-1), 8) >= round(lowerlimit, 8) and round((1200 / TET) * (step-1), 8) <= round(upperlimit, 8) and round((1200 / TET) * (step+1), 8) >= round(lowerlimit, 8) and round((1200 / TET) * (step+1), 8) <= round(upperlimit, 8):
                        C.create_text(x, verticalscale + verticalbuffer + 1.6*textsize*gensizeamounts[gensizes.index(round((1200 / TET) * step, 8))], text=str(TET)+"~", font=("Arial", textsize, "bold"), fill="#8CA")
                    elif round((1200 / TET) * (step+1), 8) >= round(lowerlimit, 8) and round((1200 / TET) * (step+1), 8) <= round(upperlimit, 8):
                        C.create_text(x, verticalscale + verticalbuffer + 1.6*textsize*gensizeamounts[gensizes.index(round((1200 / TET) * step, 8))], text=str(TET)+"b", font=("Arial", textsize, "bold"), fill="#8CA")
                    elif round((1200 / TET) * (step-1), 8) >= round(lowerlimit, 8) and round((1200 / TET) * (step-1), 8) <= round(upperlimit, 8):
                        C.create_text(x, verticalscale + verticalbuffer + 1.6*textsize*gensizeamounts[gensizes.index(round((1200 / TET) * step, 8))], text=str(TET)+"#", font=("Arial", textsize, "bold"), fill="#8CA")
                    else:
                        C.create_text(x, verticalscale + verticalbuffer + 1.6*textsize*gensizeamounts[gensizes.index(round((1200 / TET) * step, 8))], text=str(TET), font=("Arial", textsize, "bold"), fill="#8CA")
                else:
                    gensizes.append(round((1200 / TET) * step, 8)); gensizeamounts.append(1)
                    draw = True
                    x = horizontalscale*((((1200 / TET) * step)-lowerlimit)/(upperlimit-lowerlimit)) + horizontalbuffer
                    C.create_line(x, verticalscale + verticalbuffer, x, verticalbuffer, fill="#656565", width=3)
                    if round((1200 / TET) * (step-1), 8) >= round(lowerlimit, 8) and round((1200 / TET) * (step-1), 8) <= round(upperlimit, 8) and round((1200 / TET) * (step+1), 8) >= round(lowerlimit, 8) and round((1200 / TET) * (step+1), 8) <= round(upperlimit, 8):
                        C.create_text(x, verticalscale + verticalbuffer + 1.6*textsize, text=str(TET)+"~", font=("Arial", textsize, "bold"), fill="#000")
                    elif round((1200 / TET) * (step+1), 8) >= round(lowerlimit, 8) and round((1200 / TET) * (step+1), 8) <= round(upperlimit, 8):
                        C.create_text(x, verticalscale + verticalbuffer + 1.6*textsize, text=str(TET)+"b", font=("Arial", textsize, "bold"), fill="#000")
                    elif round((1200 / TET) * (step-1), 8) >= round(lowerlimit, 8) and round((1200 / TET) * (step-1), 8) <= round(upperlimit, 8):
                        C.create_text(x, verticalscale + verticalbuffer + 1.6*textsize, text=str(TET)+"#", font=("Arial", textsize, "bold"), fill="#000")
                    else:
                        C.create_text(x, verticalscale + verticalbuffer + 1.6*textsize, text=str(TET), font=("Arial", textsize, "bold"), fill="#000")
                    for step1 in range(TET+1):
                         C.create_oval(x - 3, (verticalscale/TET)*step1 + verticalbuffer + 3, x + 3, (verticalscale/TET)*step1 + verticalbuffer - 3, fill="#445")
        if not hasgen:
            nonmos.append(str(TET))
    C.create_text(horizontalbuffer + horizontalscale/2, verticalscale + verticalbuffer + textsize*12, text="TETs with more than one valid generator are suffixed with b or # (~ for mids)", font=("Arial", textsize, "bold"))
    C.create_text(horizontalbuffer + horizontalscale/2, verticalscale + verticalbuffer + textsize*13.7, text="TETs in green are multiples of lower TETs that share the same generator", font=("Arial", textsize, "bold"))
    if len(nonmos) != 0:
        C.create_text(horizontalbuffer + horizontalscale/2, verticalscale + verticalbuffer + textsize*15.4, text="TETs with no "+str(L)+"L "+str(s)+"s: "+", ".join(nonmos), font=("Arial", textsize, "bold"))
        
    # render menu 
    
    lup = Button(C, font=("Arial", textsize), text="▲", command = lambda: [mos(L+1, s, tetlimit, gen, 1, Lstep, sstep), lup.destroy(), modebutton.destroy(), playmos.destroy(), parent.destroy(), daughter1.destroy(), daughter2.destroy(), sister.destroy(), neutral.destroy(), playmos.destroy()])
    if L == 1:
        ldown = Button(C, font=("Arial", textsize), text="▼", state="disabled")
    else:
        ldown = Button(C, font=("Arial", textsize), text="▼", command = lambda: [mos(L-1, s, tetlimit, gen, 1, Lstep, sstep), ldown.destroy(), modebutton.destroy(), playmos.destroy(), parent.destroy(), daughter1.destroy(), daughter2.destroy(), sister.destroy(), neutral.destroy(), playmos.destroy()])
    lup.place(x=textsize,y=textsize); ldown.place(x=textsize,y=textsize*4.1)
    C.create_text(textsize*2.19, textsize*8.5, text=str(L)+"L", font=("Arial", textsize, "bold"))
    
    sup = Button(C, font=("Arial", textsize), text="▲", command = lambda: [mos(L, s+1, tetlimit, gen, 1, Lstep, sstep), sup.destroy(), modebutton.destroy(), playmos.destroy(), parent.destroy(), daughter1.destroy(), daughter2.destroy(), sister.destroy(), neutral.destroy(), playmos.destroy()])
    if s == 1:
        sdown = Button(C, font=("Arial", textsize), text="▼", state="disabled")
    else:
        sdown = Button(C, font=("Arial", textsize), text="▼", command = lambda: [mos(L, s-1, tetlimit, gen, 1, Lstep, sstep), sdown.destroy(), modebutton.destroy(), playmos.destroy(), parent.destroy(), daughter1.destroy(), daughter2.destroy(), sister.destroy(), neutral.destroy(), playmos.destroy()])
    sup.place(x=textsize*4.3,y=textsize); sdown.place(x=textsize*4.3,y=textsize*4.1)
    C.create_text(textsize*5.49, textsize*8.5, text=str(s)+"s", font=("Arial", textsize, "bold"))

    tetup = Button(C, font=("Arial", textsize), text="▲", command = lambda: [mos(L, s, tetlimit+1, gen, mode, Lstep, sstep), tetup.destroy(), modebutton.destroy(), playmos.destroy(), parent.destroy(), daughter1.destroy(), daughter2.destroy(), sister.destroy(), neutral.destroy(), playmos.destroy()])
    if tetlimit == 1:
        tetdown = Button(C, font=("Arial", textsize), text="▼", state="disabled")
    else:
        tetdown = Button(C, font=("Arial", textsize), text="▼", command = lambda: [mos(L, s, tetlimit-1, gen, mode, Lstep, sstep), tetdown.destroy(), modebutton.destroy(), playmos.destroy(), parent.destroy(), daughter1.destroy(), daughter2.destroy(), sister.destroy(), neutral.destroy(), playmos.destroy()])
    tetup.place(x=textsize*7.6,y=textsize); tetdown.place(x=textsize*7.6,y=textsize*4.1)
    C.create_text(textsize*8.79, textsize*8.5, text="TETs", font=("Arial", textsize, "bold"))
    C.create_text(textsize*8.79, textsize*10, text="≤"+str(tetlimit), font=("Arial", textsize, "bold"))
    
    geninv = Button(C, font=("Arial", textsize, "bold"), text="Invert generator", command = lambda: [mos(L, s, tetlimit, invertgen(gen), mode, Lstep, sstep), geninv.destroy(), modebutton.destroy(), playmos.destroy(), parent.destroy(), daughter1.destroy(), daughter2.destroy(), sister.destroy(), neutral.destroy(), playmos.destroy()])
    geninv.place(x=textsize*11.5,y=textsize)

    daughter1 = Button(C, font=("Arial", textsize, "bold"), text="Daughter: "+str(L+s)+"L "+str(L)+"s", command = lambda: [mos(L+s, L, tetlimit, invertgen(gen), 1, Lstep, sstep), modebutton.destroy(), playmos.destroy(), parent.destroy(), daughter1.destroy(), daughter2.destroy(), sister.destroy(), neutral.destroy(), playmos.destroy()])
    daughter1.place(x=textsize*11.5,y=textsize*4.1)
    
    daughter2 = Button(C, font=("Arial", textsize, "bold"), text="Daughter: "+str(L)+"L "+str(L+s)+"s", command = lambda: [mos(L, L+s, tetlimit, gen, 1, Lstep, sstep), modebutton.destroy(), playmos.destroy(), parent.destroy(), daughter1.destroy(), daughter2.destroy(), sister.destroy(), neutral.destroy(), playmos.destroy()])
    daughter2.place(x=textsize*11.5,y=textsize*7.2)

    if L == s:
        parent = Button(C, font=("Arial", textsize, "bold"), text="Parent: "+str(L)+"-TET", state="disabled")
    elif L > s:
        parent = Button(C, font=("Arial", textsize, "bold"), text="Parent: "+str(s)+"L "+str(L-s)+"s", command = lambda: [mos(s, L-s, tetlimit, invertgen(gen), 1, Lstep, sstep), modebutton.destroy(), playmos.destroy(), parent.destroy(), daughter1.destroy(), daughter2.destroy(), sister.destroy(), neutral.destroy(), playmos.destroy()])
    else:
        parent = Button(C, font=("Arial", textsize, "bold"), text="Parent: "+str(L)+"L "+str(s-L)+"s", command = lambda: [mos(L, s-L, tetlimit, gen, 1, Lstep, sstep), modebutton.destroy(), playmos.destroy(), parent.destroy(), daughter1.destroy(), daughter2.destroy(), sister.destroy(), neutral.destroy(), playmos.destroy()])
    parent.place(x=textsize*25.45,y=textsize)

    if L == s:
        sister = Button(C, font=("Arial", textsize, "bold"), text="Sister: self", state="disabled")
    else:
        sister = Button(C, font=("Arial", textsize, "bold"), text="Sister: "+str(s)+"L "+str(L)+"s", command = lambda: [mos(s, L, tetlimit, invertgen(gen), 1, Lstep, sstep), modebutton.destroy(), playmos.destroy(), parent.destroy(), daughter1.destroy(), daughter2.destroy(), sister.destroy(), neutral.destroy(), playmos.destroy()])
    sister.place(x=textsize*25.45,y=textsize*4.1)

    if L == s:
        neutral = Button(C, font=("Arial", textsize, "bold"), text="Neutral: "+str(L+s)+"-TET", state="disabled")
    elif L > s:
        neutral = Button(C, font=("Arial", textsize, "bold"), text="Neutral: "+str(L-s)+"L "+str(2*s)+"s", command = lambda: [mos(L-s, 2*s, tetlimit, gen, 1, Lstep, sstep), modebutton.destroy(), playmos.destroy(), parent.destroy(), daughter1.destroy(), daughter2.destroy(), sister.destroy(), neutral.destroy(), playmos.destroy()])
    else:
        neutral = Button(C, font=("Arial", textsize, "bold"), text="Neutral: "+str(2*L)+"L "+str(s-L)+"s", command = lambda: [mos(2*L, s-L, tetlimit, gen, 1, Lstep, sstep), modebutton.destroy(), playmos.destroy(), parent.destroy(), daughter1.destroy(), daughter2.destroy(), sister.destroy(), neutral.destroy(), playmos.destroy()])
    neutral.place(x=textsize*25.45,y=textsize*7.2)

    modebutton = Button(C, font=("Arial", textsize, "bold"), text="Mode "+str(((mode-1)%int((L+s)/math.gcd(L, s)))+1)+": "+"".join(modes[mode-1]), command = lambda: [mos(L, s, tetlimit, gen, (mode+1) % int((L+s)/math.gcd(L, s)), Lstep, sstep), modebutton.destroy(), playmos.destroy(), parent.destroy(), daughter1.destroy(), daughter2.destroy(), sister.destroy(), neutral.destroy(), playmos.destroy()])
    modebutton.place(x=textsize*38.1,y=textsize)

    ldown1 = Button(C, font=("Arial", textsize), text="◀", command = lambda: [mos(L, s, tetlimit, gen, mode, Lstep-1, sstep), ldown1.destroy(), modebutton.destroy(), playmos.destroy(), parent.destroy(), daughter1.destroy(), daughter2.destroy(), sister.destroy(), neutral.destroy(), playmos.destroy()])
    lup1 = Button(C, font=("Arial", textsize), text="▶", command = lambda: [mos(L, s, tetlimit, gen, mode, Lstep+1, sstep), lup1.destroy(), modebutton.destroy(), playmos.destroy(), parent.destroy(), daughter1.destroy(), daughter2.destroy(), sister.destroy(), neutral.destroy(), playmos.destroy()])
    sdown1 = Button(C, font=("Arial", textsize), text="◀", command = lambda: [mos(L, s, tetlimit, gen, mode, Lstep, sstep-1), sdown1.destroy(), modebutton.destroy(), playmos.destroy(), parent.destroy(), daughter1.destroy(), daughter2.destroy(), sister.destroy(), neutral.destroy(), playmos.destroy()])
    sup1 = Button(C, font=("Arial", textsize), text="▶", command = lambda: [mos(L, s, tetlimit, gen, mode, Lstep, sstep+1), sup1.destroy(), modebutton.destroy(), playmos.destroy(), parent.destroy(), daughter1.destroy(), daughter2.destroy(), sister.destroy(), neutral.destroy(), playmos.destroy()])
    
    if Lstep == sstep:
        ldown1 = Button(C, font=("Arial", textsize), text="◀", state="disabled")
        sup1 = Button(C, font=("Arial", textsize), text="▶", state="disabled")
    if Lstep == 1:
        ldown1 = Button(C, font=("Arial", textsize), text="◀", state="disabled")
    if sstep == 0:
        sdown1 = Button(C, font=("Arial", textsize), text="◀", state="disabled")
    C.create_text(textsize*40.1, textsize*5.6, text="L = " + str(Lstep), font=("Arial", textsize, "bold"))
    C.create_text(textsize*40.1, textsize*8.7, text="s = " + str(sstep), font=("Arial", textsize, "bold"))
    
    ldown1.place(x=textsize*43.1,y=textsize*4.1)
    lup1.place(x=textsize*45,y=textsize*4.1)
    sdown1.place(x=textsize*43.1,y=textsize*7.2)
    sup1.place(x=textsize*45,y=textsize*7.2)
    
    playmos = Button(C, font=("Arial", int(textsize*1), "bold"), text="Mode "+str(((mode-1)%int((L+s)/math.gcd(L, s)))+1)+"\nof "+str(L)+"L "+str(s)+"s\nin "+str((L*Lstep)+(s*sstep))+"-TET", command = lambda: [beep(modes[mode-1], L, s, Lstep, sstep)])
    playmos.place(x=textsize*47.3,y=textsize*4.1)
    

mos(5, 2, 55, "bright", 3, 2, 1)

    
