def rateHide(val):
    if val!="":
        data=""
        for i,v in enumerate(val):
            if v=="0":
                data=data+"A"
            if v=="1":
                data=data+"B"       
            if v=="2":
                data=data+"C"  
            if v=="3":
                data=data+"D"  
            if v=="4":
                data=data+"E"  
            if v=="5":
                data=data+"F"  
            if v=="6":
                data=data+"G"  
            if v=="7":
                data=data+"H"  
            if v=="8":
                data=data+"I"  
            if v=="9":
                data=data+"J"                                           
        return data    
    else:
        return "" 

          
