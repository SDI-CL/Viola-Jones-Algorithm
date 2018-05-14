#not exactly logging but who cares
# INFO is just for debugging and shift
# WARNING is for things that are nice to know but dont realy interrupt anything
# ERRO when shit goes south
from termcolor import colored
import time
class VJ_Logging:
    def __init__(self, name, log_level = 0):
        self.level = log_level
        self.file = open('./log/'+ name +'_log.log',"w")
        self.file.close()
        self.start_time = time.time()
        self.name = name
        self.fps_counter = 1
        self.fps_sum = 0

    def print_log(self,level,function,message):
        currTime = str(time.ctime())
        f = open('./log/'+ self.name +'_log.log','a')
        if (self.level == 0 ):
            if (level == 0):
                print colored('[INFO]','green') + "      [" + function + "] " + message
                f.write('[' + currTime +  '][INFO]' + "      [" + function + "] " + message + '\n')
            elif (level == 1):
                print colored('[WARNING]','yellow') + "    [" + function + "] " + message
                f.write('[' + currTime +  '][WARNING]' + "      [" + function + "] " + message + '\n')
            elif (level == 2):
                print colored('[ERROR]','red') + "     [" + function + "] " + message
                f.write('[' + currTime +  '][ERROR]' + "     [" + function + "] " + message + '\n')
        elif (self.level == 1):
            if (level == 1):
                print colored('[WARNING]','yellow') + "    [" + function + "] " + message
                f.write('[' + currTime +  '][WARNING]' + "      [" + function + "] " + message + '\n')
            elif (level == 2):
                print colored('[ERROR]','red') + "     [" + function + "] " + message
                f.write('[' + currTime +  '][ERROR]' + "     [" + function + "] " + message + '\n')
        elif (self.level == 2):
            if (level == 2):
                print colored('[ERROR]','red') + "     [" + function + "] " + message
                f.write('[' + currTime +  '][ERROR]' + "     [" + function + "] " + message + '\n')
        f.close()

    def log_boxes(self,objects):
        currTime = str(time.ctime())
        f = open('./log/'+ self.name +'_log.log','a')
        for (x,y,a,b,tag) in objects:
            print colored('[OBJECT]','green') + "    [" + tag + "] " + ' (' + str(x) + ',' + str(y) + ') (' + str(a) + ',' + str(b)+ ')'
            f.write('[' + currTime +  '][OBJECT]' + '    ['+tag + '](' + str(x) + ',' + str(y)+ ') (' + str(a) + ',' + str(b)+ ')\n')
        f.close()

    def log_fps(self, fps):


        print colored('[FPS]', 'green') + "    current FPS: " + str(int(fps)) 
        f = open('./log/'+ self.name +'_log.log','a')
        f.write("[FPS]    current FPS: " + str(int(fps))+"\n" )
        f.close()
