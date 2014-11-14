################################################################################
## messages
################################################################################

from random import randint, choice

################################################################################

win = ("You've Won!", "Congrats!", "Prizes await!", "WooHoo!", "That's the way!", "Todd is an alien.")

playing = ("Game On!")

enter_school = ("So you want to go to school.", "Education is not for the weak minded.")

enter_school_again = ("So you want to get more school.", "Back to the old drawing board.")

school = ( "Belmont", "Bloody Bone", "Prizdon", "Leponderly", 
           "The Jane Post School Of Grace For Girls", "Rathburns")
skills = ( "archery", "mumbly peg", "cheating", "stealth", "armor", "hand2hand", 
           "intimidation", "combat", "pizza", "picking up chicks")

creep_na = ( "Treeba", "Belch", "Fluh", "Areh", "Nic Nac", "Cetch", "Derd", 
             "Blone", "Elvis", "Freig", "Gutter", "Hwie", "Invel", "Jwoob", 
             "Klux", "Lup", "Jon Jon Joe", "Giba", "Doga", "Mloog", "Paddy", 
             "Nloog", "Floop", "Sloop", "Kloog", "Aarp", "Yaarp", "Laarp", 
             "Oorp", "Wac", "Plod", "Ree", "Todd the Flea", "Skug", "Skoogs", 
             "Tup", "Lyuk", "Ulbina the Amazing", "Vlip", "Wad", "Yap", 
             "Chunch")

first_na = ( "Aran", "Jessil", "Anderu", "Todad", "Todah", "Krixtean", 
             "Jothan", "Timbao", "Anitum", "Jon", "Robard", "Abrim", "Izik", 
             "Jukab", "Benan", "Rebe", "Tierst", "Sande", "Faiter", "Japor", 
             "Mokan", "Ashan")

################################################################################
## npc names

# Last Names:

#Identifier A (parent name would be another first name plus an extension)
sir_na_ex = ( "son", "child", "sire", "ido", "man", "let", "sire", "geld", "lin", 
              "luke", "bob", "in", "ain", "a", "smith", "mac", "bod", "ito", "et"
              " the Younger", " Jr.", " Little", "ous", "an", "ke", "ac", "and", 
              "sman", "boy")
sir_na_pre = ( "A ", "ap ", "Mc", "Mac", "Alm ", "Bet ", "da ", "De", "Kil ", 
               "Fitz ", "Le", "Na", "Van ", "Von ", "Naka ")

#Identifier A' (parent name based on personal trait plus opt sir_na_ext)
pers_tr_col = (  "Gray", "Gold", "Yellow", "Stout", "Strong", "Little", "Tiny",
                 "Long", "Green", "White", "No", "Thin", "Great", "Strange", 
                 "Pointed", "Brass", "Iron", "Stoney", "Broken", "Frost", 
                 "Burnt", "Slack", "Quick", "Broken", "Black", "Brown", "Sweet")
                
pers_tr_obj = (  "beard", "head", "arm", "reach", "tooth", "foot", "bottom", 
                 "belly", "joy", "pocket", "jacket", "boot", "button", "hammer",
                 "door", "hearth", "gable", "heart")  

#Identifier B (occupation, with a possibility of a parent name extension)
occ_na = ( "Bottler", "Cobbler", "Miller", "Bowyer", "Barber", "Drey", "Baker",
           "Farmer", "Sapper", "Black", "Tailor", "Merc", "Harper", "Schol", 
           "Sage", "Cart", "Ascet", "Barrister", "Journeyman", "Herald", "Nun", 
           "Scribe", "Lords", "Reeves", "Squire", "Armorer", "Smith", "Binder", 
           "Booker", "Brewer", "Mason", "Bricker", "Butcher", "Chandler", 
           "Carpenter", "Cartwright", "Wright", "Clothier", "Shoemaker", "Cook", 
           "Cooper", "Dyer", "Engraver", "Furrier", "Trapper", "Glasser", 
           "Goldsmith", "Silversmith", "Hatter", "Keeper", "Jeweler", "Joiner", 
           "Leatherworker", "Banks", "Banker", "Potter", "Tinker", "Peddler", 
           "Trader", "Vintner", "Weaver", "Boatman", "Coachman", "Fisherman", 
           "Fisher", "Graves", "Digs", "Groom", "Herder","Hunter", "Trapper", 
           "Messenger", "Miner", "Painter", "Limner", "Peddler", "Ratcatcher", 
           "Sailor", "Butler", "Steward", "Stevedore", "Hunter", "Forester", 
           "Ranger", "Warden", "Gatekeeper", "Tollkeep", "Jailer", "Watchman", 
           "Beggar", "Ragsman", "Minstrel", "Dancer", "Clown", "Bailiff", 
           "Knight", "Reeve", "Watchman", "Drummer", "Booth", "Boothman", 
           "Chapman", "Drover", "Lighterman", "Skinner", "Poulter", "Spicer", 
           "Thresher", "Weir", "Monger", "Bard", "Barker", "Geiger", "Fiddler", 
           "Piper", "Ackerman", "Fowler", "Hawker", "Hawks", "Hayward", "Ostler", 
           "Parker", "Reaper", "Plowman", "Shepherd", "Herdsman", "Thresher", 
           "Tillerman", "Woolcomber", "Tutor", "Hobbler", "Pilot", "Franklin", 
           "Palmer", "Pilgrim", "Tenter", "Saddler", "Roofer", "Tanner", 
           "Beacher", "Culter", "Glover", "Armorer", "Brewer", "Founder", 
           "Besom", "Bodger", "Bottelier", "Brody", "Dasher", "Buttonmaker", 
           "Campaner", "Coiner", "Cordwainer", "Currier", "Delver", "Disher", 
           "Draper", "Dyer", "Fletcher", "Gilder", "Fuller", "Girdler", "Panter", 
           "Glazier", "Grinder", "Hacker", "Horner", "Horn", "Knacker", "Napier",  
           "Knapper", "Lance", "Lancier", "Latoner", "Limner", "Linener", 
           "Lorimer", "Luthier", "Mailer", "Marler", "Nedeller", "Plattner", 
           "Plumber", "Pointer", "Purser", "Quarryman", "Quilter", "Roper", 
           "Reedmaker", "Salter", "Shingler", "Sawyer", "Siever", "Smelter", 
           "Spooner", "Spurrer", "Tapicer", "Tasseler", "Thacker", "Thacher", 
           "Thonger", "Tyler", "Tiler", "Webber", "Carter", "Bagger", "Bags",
           "Carver", "Ceiler", "Clouter", "Dapifer", "Ditcher", "Diver", "Hoggard", 
           "Drayman", "Farrier", "Hurdler", "Lawyer", "Linkman", "Marshal", 
           "Pavior", "Pavyler", "Potboy", "Raker", "Stainer", "Tapster", "Forger",
           "Teamster", "Carver", "Trencherman", "Wattler", "Beamer", "Bloomer", 
           "Blower", "Bluffer", "Borler", "Bottomer", "Fawkner", "Feller", 
           "Hooper", "Hodsman", "Mercer", "Monger", "Mudlark", "Porter", "Poulter"
           "Seedsman", "Shrager", "Slater", "Spinner", "Sticher", "Sutler", 
           "Cutler", "Tasker", "Tosher", "Travers", "Warrener", "Yoeman", "Page", 
           "Grocer", "Cottar", "Castellain", "Paver", "Priest", "Fisher")

#Identifier C (location plus an extension)
#(town names) - we could do the same thing for town names plus extension

town_na = ( "Boane", "Geshon", "Welloron", "Matomayt", "Champa", "Summer", 
            "Winter", "Spring", "Gold", "Silver", "Copper", "Stone", "Harvest", 
            "Ar", "Bail", "Can", "Dill", "Elk", "Fra", "Grip", "Huit", "Lan",
            "Morow", "Napa", "Lees", "Ord", "Pan", "Role", "Stay", "Tap", "Nell")

#Identifier D Geographic names plus an extension
geo_na = ( "Cliff", "Brook", "Meadow", "Forest", "River", "Valley", "Fort", 
           "Spring", "Heather", "Glen", "Haven", "Lake", "Pond", "Shallows", 
           "Gallows", "Post", "Port", "Shallows", "Gulf", "Gulch", "Swift",
           "Home", "Fall", "Twins", "Crook", "Deer", "Raven", "Hawk", "Wolf", 
           "Bear", "New", "Old", "Barren", "Bleak", "One", "Two", "Far", 
           "Middle", "Mews")

# C/D extension
geo_na_ex = ( "town", "ton", "ville", "shire", "s", "apolis", "ford", "sted", 
              "ite", "vale", "dell", "etta", "et", "set", "let", "ling", "dale", 
              " Falls", " Brooks", "heather", "haven", "spring", "hill", "forks", 
              "bluffs", "hollow", "holm", "by", "beck", "burg", "cox", " Hill",
              " Forge", " Gate", "ia", "in", "lay", "ley", "lin", "ot", " End", 
              " Grove", "toft", " Knoll", " Green", " Town", "well", " Village", 
              "worth", " Field", "land", "ings", " Orchard", " Rapids", "field", 
              " City", "son", "mont", " Crossing", "ford", "ridge", "ster", 
              "narrows", " Rift", "ine")

################################################################################

HERO_WINS = 0
ENEMY_WINS = 0

################################################################################

class Reader(object):
    """ various tools for printing unit and message information """
    def __init__(self):
        dummy = False
    
    def prt_unit_history(self, unit):
        print("This unit attended:", unit.story["school"]) # school
        print("Skills in:", unit.skills) # unit skills
        
################################################################################        
        
def pawn_name_maker(allow_dual = False): # TODO - add a dual_name option
    """ creates a first and last name from variables
        allow_dual = True allows 2-word last names
        allow_dual = False not allows 2-word last names """
    variant = randint(0, 10) # variants: 1st name, trade, town, trait
    #select first name
    first_name = choice(first_na)
    last_name = ""
    if variant < 4: # based on sire_name
        if randint(0,3) < 2:
            last_name = choice(first_na) + choice(sir_na_ex)
        else: 
            last_name = choice(sir_na_pre) + choice(first_na)
    elif variant > 3 and variant < 7: # based on trade
        last_name = choice(occ_na) 
        last_name = ending_remover(last_name)            
        last_name += choice(sir_na_ex) 
    elif variant == 7 or variant == 8: # based on location
        last_name = town_name_maker(False) + choice(sir_na_ex) 
    else:
        if randint(0,6) < 5:
            last_name = choice(pers_tr_col) + choice(pers_tr_obj)
        else: last_name = choice(pers_tr_col) + choice(pers_tr_obj) + choice(sir_na_ex)
    return(first_name + " " + last_name)

################################################################################
def town_name_maker(allow_dual = True):
    """ creates a town name from variables 
        allow_dual = True allows 2-word names
        allow_dual = False does not allow 2-word names - for use in char names """
    
    variant = randint(0, 4)
    if variant == 0: #based on 1st name
        if randint(0,2) == 0 and allow_dual:
            town_name = choice(first_na) + " " + choice(geo_na)
        else: 
            town_name = choice(first_na) + choice(geo_na_ex)
    elif variant == 1: #based on occupation
        if randint(0,2) == 0 and allow_dual:
            town_name = choice(occ_na) + " " + choice(geo_na)
        else: 
            town_name = choice(occ_na) 
            town_name = ending_remover(town_name)            
            town_name += choice(geo_na_ex)
    elif variant == 2: #based on town name
        subvariant = randint(0,4)
        if subvariant == 0:
            town_name = choice(town_na)
        elif subvariant == 1 and allow_dual:
            town_name = choice(town_na) + " " + choice(geo_na)
        else: 
            town_name = choice(town_na) + choice(geo_na_ex)
    else: # based on geographic name
        if randint(0,2) == 0 and allow_dual:
            town_name = choice(geo_na) + " " + choice(geo_na)
        else: 
            town_name = choice(geo_na) + choice(geo_na_ex)
    return(town_name)
################################################################################

def ending_remover(text):
    """ returns word after parsing out endings from sent text: 
        -er, -ing, -man, -or (sometimes replaces with -s if doesn't end in -s)
    """
    #print("ending_remover being used on:", text)
    text = text.rstrip("yer")
    text = text.rstrip("ing")
    text = text.rstrip("or")
    text = text.rstrip("man")
    return(text)
    
        

        
################################################################################
## Unit Testing                                                               ##
################################################################################
if __name__ == "__main__":  
    print(win)
    reader = Reader()
    print("Done")
    
    print()
    print("50 Towns:")    
    for attempt in range(0,50):
        print(town_name_maker())
        
    print()
    print("50 names:")
    for attempt in range(0,50):
        print(pawn_name_maker(allow_dual = False))    
    
    print("-- DONE --")