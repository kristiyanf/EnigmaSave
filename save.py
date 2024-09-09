import configparser
import rotor

Rotor = rotor.Rotor
config = configparser.ConfigParser()

# WIRING TABLES

rotor_i =      ["EKMFLGDQVZNTOWYHXUSPAIBRCJ", ["Q"]]
rotor_ii =     ["AJDKSIRUXBLHWTMCQGZNPYFVOE", ["E"]]
rotor_iii =    ["BDFHJLCPRTXVZNYEIWGAKMUSQO", ["V"]]
rotor_iv =     ["ESOVPZJAYQUIRHXLNFTGKDCMWB", ["J"]]
rotor_v =      ["VZBRGITYUPSDNHLXAWMJQOFECK", ["Z"]]
rotor_vi =     ["JPGVOUMFYQBENHZRDKASXLICTW", ["Z", "M"]]
rotor_vii =    ["NZJHGRCXMYSWBOUFAIVLPEKQDT", ["Z", "M"]]
rotor_viii =   ["FKQHTLXOCBJSPDZRAMEWNIUYGV", ["Z", "M"]]
rotor_beta =    "LEYJVCNIXWPBQMDRTAKZGFUHOS"
rotor_gamma =   "FSOKANUERHMBTIYCWLQPZXVGJD"
reflector_a =   "EJMZALYXVBWFCRQUONTSPIKHGD"
reflector_b =   "YRUHQSLDPXNGOKMIEBFZCWVJAT"
reflector_c =   "FVPJIAOYEDRZXWGCTKUQSBNMHL"
reflector_tb =  "ENKQAUYWJICOPBLMDXZVFTHRGS"
reflector_tc =  "RDOBJNTKVEHMLFCWZAXGYIPSUQ"

# SETTINGS

# DEFAULT SETTINGS

config["SETTINGS"] = {}
config["SETTINGS"]["rotor_greek"] = ""
config["SETTINGS"]["rotor_left"] = "1"
config["SETTINGS"]["rotor_middle"] = "2"
config["SETTINGS"]["rotor_right"] = "3"
config["SETTINGS"]["reflector"] = "B"
config["SETTINGS"]["rotor_greek_ring_setting"] = config["SETTINGS"]["rotor_left_ring_setting"] = config["SETTINGS"]["rotor_middle_ring_setting"] = config["SETTINGS"]["rotor_right_ring_setting"] = config["SETTINGS"]["rotor_greek_position"] = config["SETTINGS"]["rotor_left_position"] = config["SETTINGS"]["rotor_middle_position"] = config["SETTINGS"]["rotor_right_position"] = "1"
config["SETTINGS"]["plugboard"] = ""

config.read("config.ini")

# WRITE TO CONFIG

def write_config():
    with open("config.ini", "w") as configfile:
        config.write(configfile)

# WRITE ROTOR FUNCTION

def input_configure_rotors(action):
    snake_case_action = action.lower().replace(" ", "_")
    if config["SETTINGS"]["rotor_greek"]:
        config["SETTINGS"]["rotor_greek_" + snake_case_action] = input("Set Greek rotor " + action + " (A-Z) or (1-26): ")
    else:
        config["SETTINGS"]["rotor_greek_" + snake_case_action] = "1"
    config["SETTINGS"]["rotor_left_" + snake_case_action] = input("Set left rotor " + action + " (A-Z) or (1-26): ")
    config["SETTINGS"]["rotor_middle_" + snake_case_action] = input("Set middle rotor " + action + " (A-Z) or (1-26): ")
    config["SETTINGS"]["rotor_right_" + snake_case_action] = input("Set right rotor " + action + " (A-Z) or (1-26): ")

# USER INPUT

def input_settings():
    if input("Do you want to change the settings? Yes or no (y/n): ") == "y":
        
        # INPUT GREEK WHEEL

        if input("Use Greek rotor? Yes or no (y/n): ").lower() == "y":
            config["SETTINGS"]["rotor_greek"] = input("Select Greek rotor (B/G): ")
        else:
            config["SETTINGS"]["rotor_greek"] = ""

        # INPUT ROTORS AND REFLECTOR

        config["SETTINGS"]["rotor_left"]=input("Select left rotor (1-8): ")
        config["SETTINGS"]["rotor_middle"]=input("Select middle rotor (1-8): ")
        config["SETTINGS"]["rotor_right"]=input("Select right rotor (1-8): ")
        config["SETTINGS"]["reflector"]=input("Select reflector (A/B/C/TB/TC): ")

        # INPUT ROTOR POSITIONS AND RING SETTINGS

        input_configure_rotors("ring setting")
        input_configure_rotors("position")

        # INPUT PLUGBOARD

        config["SETTINGS"]["plugboard"] = ""
        while(input("Add plug pairs? Yes or no (y/n): ").lower() == "y"):
            config["SETTINGS"]["plugboard"] = config["SETTINGS"]["plugboard"] + " " + input("Add plug pairs (WX YZ): ")        
    write_config()

# READ FROM CONFIG

def read_config():

    # READ GREEK WHEEL

    match config["SETTINGS"]["rotor_greek"].upper():
        case "G":
            rotor_greek = Rotor(rotor_gamma)
        case "B":
            rotor_greek = Rotor(rotor_beta)
        case _:
            rotor_greek = Rotor(rotor.alphabet)

    # READ ROTORS

    def get_rotor(slot):
        match config["SETTINGS"]["rotor_" + slot]:
            case "1":
                return Rotor(*rotor_i)
            case "2":
                return Rotor(*rotor_ii)
            case "3":
                return Rotor(*rotor_iii)
            case "4":
                return Rotor(*rotor_iv)
            case "5":
                return Rotor(*rotor_v)
            case "6":
                return Rotor(*rotor_vi)
            case "7":
                return Rotor(*rotor_vii)
            case "8":
                return Rotor(*rotor_viii)

    rotor_left = get_rotor("left")
    rotor_middle = get_rotor("middle")
    rotor_right = get_rotor("right")

    # READ REFLCTOR

    match config["SETTINGS"]["reflector"].upper():
        case "A":
            reflector = reflector_a
        case "B":
            reflector = reflector_b
        case "C":
            reflector = reflector_c
        case "TB":
            reflector = reflector_tb
        case "TC":
            reflector = reflector_tc

    # READ ROTOR FUNCTION

    def configure_rotors(rotor_function, action):
        action = action.lower().replace(" ", "_")
        rotor_function(rotor_greek, config["SETTINGS"]["rotor_greek_" + action])
        rotor_function(rotor_left, config["SETTINGS"]["rotor_left_" + action])
        rotor_function(rotor_middle, config["SETTINGS"]["rotor_middle_" + action])
        rotor_function(rotor_right, config["SETTINGS"]["rotor_right_" + action])

    # READ ROTOR POSITIONS AND RING SETTINGS

    configure_rotors(Rotor.ring_setting, "ring setting")
    configure_rotors(Rotor.rotor_position, "position")

    # READ PLUGBOARD

    plugboard = []
    plug_pairs = config["SETTINGS"]["plugboard"].upper().replace(" ", "").replace("  ", "")
    for i in range(int(len(plug_pairs)/2)):
        index = (i*2)
        for j in plugboard:
            if plug_pairs[index] in j or plug_pairs[index + 1] in j:
                print(plug_pairs[index] + plug_pairs[index + 1] + " is a duplicate of "+str(j)+" and wasn't added.")
                break
        else:
            plugboard.append((plug_pairs[index], plug_pairs[index + 1]))
    return rotor_greek, rotor_left, rotor_middle, rotor_right, reflector, plugboard