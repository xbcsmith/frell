#!/usr/bin/env python
import sys

trex = """
      `osyhys/.-                        
  -+yhNMNMMMMNmNMmyo+:-..`              
`dMMMNs- :MMM/ `mMm/+sdNMMMNmmhs+:.     
yMMMMNhys`mMM`  hM-     -hMmMMMMMy++o-  
 hMMMMMMh yMd: -MM-      sN-hMMMMMMNhhs 
  `+MMMs  -MMMNydMMdsooodMMMMMMMMMMMMMM/
   .MMMdyshMMMMMMMMNddmMMMMMMMMMMNNMNmNs
  .mMMMMMMMMMNyo``     .//syhdmNh.:y` ` 
  /:/dMMMMMMMNNNd+`        `  +-        
    .:+mMMMMMMMMMMMhs.                  
       `yMMMMMMMMMMMMN+.                
         :NMMMMMMMMMMMMNs:.             
          .dMMMMMMMMMMMMMMN:+. `-       
           `sNMMMMMMMMMMMMMMMmdmy+o-.   
              ...-/++oosyhdNMMMMMMMMo   
                            ./shhyo. 
"""

trex_error = """
      `oMmMhsarc/.-                        
  -+yhNMNMMMMNmNMmyo+:-..`              
`dMMMNs- :MMM/ `mMm/+sdNMMMNmmhs+:.     
yMMMMNhys`mMM`  hM-     -hMmMMMMMy++o-  
 hMMMMMMh yMd: -MM-      sN-hMMMMMMNhhs 
  `+MMMs  -MMMNydMMdsooodMMMMMMMMMMMMMM/
   .MMMdyshMMMMMMMMNddmMMMMMMMMMMNNMNmNs
  .mMMMMMMMMMNyo``     .//syhdmNh.:y0mm0 
  /:/dMMMMMMMNNNd+`        ````  //  //     
    .:+mMMMMMMMMMMMhs.           `   ` 
       `yMMMMMMMMMMMMN+.     %s           
         :NMMMMMMMMMMMMNs:.             
          .dMMMMMMMMMMMMMMN:+. `^       
           `sNMMMMMMMMMMMMMMMmdmy+o-.   
              ...-/++oosyhdNMMMMMMMMo   
                            ./shhy. 

"""

trex_error_half = """
      `oMmMhsarc/.-                        
  -+yhNMNMMMMNmNMmyo+:-..`              
`dMMMNs- :MMM/ `mMm/+sdNMMMNmmhs+:.     
yMMMMNhys`mMM`  hM-     -hMmMMMMMy++o-  
 hMMMMMMh yMd: -MM-      sN-hMMMMMMNhhs 
  `+MMMs  -MMMNydMMdsooodMMMMMMMMMMMMMM/
   .MMMdyshMMMMMMMMNddmMMMMMMMMMMNNMNmNs
  .mMMMMMMMMMNyo``     .//syhdmNh.:y0mm0 
  /:/dMMMMMMMNNNd+`        ````  //  //     
       `yMMMMMMMMMMMMN+.     %s           
          .dMMMMMMMMMMMMMMN:+. `^       
           `sNMMMMMMMMMMMMMMMmdmy+o-.   
              ...-/++oosyhdNMMMMMMMMo   
                            ./shhy. 

"""

trex_error_full = """
      `oMmMhsarc/.-                        
  -+yhNMNMMMMNmNMmyo+:-..`              
`dMMMNs- :MMM/ `mMm/+sdNMMMNmmhs+:.     
yMMMMNhys`mMM`  hM-     -hMmMMMMMy++o-  
 hMMMMMMh yMd: -MM-      sN-hMMMMMMNhhs 
  `+MMMs  -MMMNydMMdsooodMMMMMMMMMMMMMM/
   .MMMdyshMMMMMMMMNddmMMMMMMMMMMNNMNmNs
  .mMMMMMMMMMNyo``     .//syhdmNh.:y0mm0 
  /:/dMMMMMMMNNNd+`         ````  //  //     
          .dMMMMMMMMMMMMMMN:+.%s`^       
           `sNMMMMMMMMMMMMMMMmdmy+o-.   
              ...-/++oosyhdNMMMMMMMMo   
                            ./shhy. 

"""


def trex_eat(crapola):
    trex_list = [ trex_error, trex_error_half, trex_error_full ]
    if not isinstance(crapola, (list, tuple)):
        crapola = [ crapola ]
    for crap in crapola:
        print trex
        while crap:
            for err in trex_list:
                for i in range(0, len(err.split())):
                    print " ",err % crap, " \r"  
                    print " ",err % crap[3:], "\r"
                    print " ",err % crap[:3], "\r"
                crap = crap[1:] or None
        print "  "
    
def debugExceptHook(type, value, tb):
    import epdb
    import traceback
    print "T-Rex Hates %s" % type.__name__
    print str(type)
    traceback.print_exception(type, value, tb)
    epdb.post_mortem(tb)

def main(args):
    trex_eat(args[1])

if __name__ == '__main__':
    sys.excepthook = debugExceptHook
    main(sys.argv)
