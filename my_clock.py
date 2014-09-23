################################################################################
## my_clock
################################################################################
import pygame


################################################################################

class Time_clock(object):
    """ tracks total time, countdowns """
    def __init__(self):
        clock = pygame.time.Clock()
        self.time_passed = 0
        self.time_count = 0
        self.clock_out = ""
        
    def post_clock(self):
        """ outputs string of current time """
        d_hour = int(self.time_count/50/60/60)
        d_min = int(self.time_count/50/60)
        d_sec = int(self.time_count/50 %60)
        if d_sec > 59:
            d_sec = 0
        dt_hour = str(d_hour)
        dt_min = str(d_min)
        dt_sec = str(d_sec)
        if len(dt_hour) < 2:
            dt_hour = "0" + dt_hour        
        if len(dt_min) < 2:
            dt_min = "0" + dt_min
        if len(dt_sec) < 2:
            dt_sec = "0" + dt_sec
        self.clock_out = dt_hour + ":" + dt_min + ":" + dt_sec
        #print(d_hour, d_min, d_sec)
        #print(dt_hour, dt_min, dt_sec)
        #print(self.clock_out)
        #print()
        return(self.clock_out)
        
    def tick(self):
        self.time_count += 1
        et_group.et_update()
        
class Event_timer(object):
    """ create event timer parent class  - child class has results """
    def __init__(self):
        self.start = time.time_count
        self.end = self.start + 150 # event parent class has 3 second duration
            
    def add_delay(self, delay):
        if delay != 0:
            self.end = self.start + delay
        
class et_dummy(Event_timer): #uses default values and only prints out notice
    def __init__(self, delay = 0):
        Event_timer.__init__(self)
        self.end = self.start + 150 #                                           include on all events, length (150 default)
        self.add_delay(delay) #                                                 include on all events with delay (150 default)
        print("adding event. end:", self.end)
        
    def et_result(self):
        self.message = "Boom! timer done"
        print(self.message, self.start, self.end, time.time_count)
               
class Et_group(object):
    """ group of event objects """
    def __init__(self):
        self.group_list = []
        
    def remove_all_et(self):
        self.group_list = []
        
    def add_et(self, delay = 0, event_type = "dummy"):
        if event_type == "dummy":
            new_event = et_dummy(delay)
            self.group_list.append(new_event)       
        
    def et_update(self):
        for event in self.group_list:
            if event.end <= time.time_count:
                event.et_result()
                self.group_list.remove(event)
            

################################################################################
## Test
################################################################################        

if __name__ == "__main__":  
    
    
    clock = pygame.time.Clock() #                                               This line must be in the program
    time = Time_clock() #                                                       This line must be in the program
    et_group = Et_group() #                                                     This line must be in the program
    

    for event_no in range(0,15):
        et_group.add_et(delay = (event_no + 1) * 36)

    test_flag = False
    while test_flag == False:
        time.time_passed = clock.tick(50) #                                     This line must be in the game loop
        time.tick() #                                                           This line must be in the game loop
        print(time.time_count, time.post_clock())
        
        if time.time_count == 150:
            print()
            print("adding an event")
            print()
            #et_group.add_et(start=time.time_count)
            et_group.add_et()
            
        if time.time_count == 200:
            print()
            print("adding an event")
            print()
            #et_group.add_et(start=time.time_count) 
            et_group.add_et()  
        
        
        if time.time_count > 500:
            test_flag = True
    
    if (len(et_group.group_list)) > 0:
        print("some events remain:", len(et_group.group_list), "   Removing...")
        et_group.remove_all_et()    
            
    print()
    print("Events remaining:", len(et_group.group_list))        
            
    print()    
    print("Done")