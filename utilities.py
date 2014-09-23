# utilities


class Vec2(object):
    """ class for processing unit vectors """
    
    def __init__(self, x_or_pair, y = None):
        if y == None:
            self.x = x_or_pair[0]
            self.y = x_or_pair[1]
        else:
            self.x = x_or_pair
            self.y = y
        print("new coord = ", self.x, self.y)
            

class Vec2_group(object):
    def __init__(self):
        self.group_list = []
        print("i made a group list")
        
    def add2group(self, x, y = None):
        my_vec = Vec2(x, y)
        self.group_list.append(my_vec)
        
    def reset(self):
        self.group_list = []
    
    
################################################################################
## Unit Testing                                                               ##
################################################################################
if __name__ == "__main__":  
    
    vec2_group = Vec2_group()
    
    vec2_group.add2group(1,1)
    vec2_group.add2group(5,5)
    vec2_group.add2group([1,2],1)
    vec2_group.add2group([2,3])
    
    for vec in vec2_group.group_list:
        print("I count a vec: x =", vec.x, ", y =", vec.y)
        
    vec2_group.reset()
    print("resetting group")
    
    if vec2_group.group_list == []:
        print("there are no vecs")
    else:
        for vec in vec2_group.group_list:
            print("I count a vec: ", vec)