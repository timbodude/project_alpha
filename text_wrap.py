################################################################################
## text_wrap
################################################################################
""" Breaks up text and wraps it so that it fits within a specified length. 
    - Length can be preset with a default: maxwidth = 150
    - Font should be predetermined in params.py

"""

import pygame
from itertools import chain
 
def truncline(text, font, maxwidth):
    real=len(text)       
    stext=text           
    l=font.size(text)[0]
    cut=0
    a=0                  
    done=1
    old = None
    while l > maxwidth:
        a=a+1
        n=text.rsplit(None, a)[0]
        if stext == n:
            cut += 1
            stext= n[:-cut]
        else:
            stext = n
        l=font.size(stext)[0]
        real=len(stext)               
        done=0                        
    return real, done, stext             
        
def wrapline(text, font, maxwidth): 
    done=0                      
    wrapped=[]                  
                               
    while not done:             
        nl, done, stext=truncline(text, font, maxwidth) 
        wrapped.append(stext.strip())                  
        text=text[nl:]                                 
    return wrapped
 
def wrap_multi_line(text, font, maxwidth):
    """ returns text taking new lines into account.
    """
    lines = chain(*(wrapline(line, font, maxwidth) for line in text.splitlines()))
    return list(lines)

################################################################################
## TEST
################################################################################
if __name__ == "__main__": 
    pygame.init() 
    font=pygame.font.Font(None, 17)
    print(wrapline("Now is the time for all good men to come to the aid of their country", font, 120))
    print()
    for line in wrapline("I'm a lumberjack, a happy boogie band dancer man, a real goer. Know what I mean, say no more! Nudge, nudge, wink, wink. A nudge is as good as a wink to a blind man.", font, 150):
        print(line)
        
    print()
    print("--DONE--")