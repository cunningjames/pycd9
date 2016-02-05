def ev_fill(decimal_part):
    """Pad the first decimal part with zeros, taking into account E / V codes.
    """
    
    if decimal_part.startswith("V"):
        return "V" + decimal_part[1:].zfill(2)
    elif decimal_part.startswith("E"):
        return "E" + decimal_part[1:].zfill(3)
    else:
        return decimal_part.zfill(3)

def ev_strip(short):
    """Strip zeros, taking into account E / V codes.
    """
    
    if short.startswith("E") or short.startswith("V"):
        return short[0] + short[1:].lstrip("0")
    else:
        return short.lstrip("0")

def decimal_to_short(decimal_code):
    """Converts decimal ICD9 codes to short codes. Attempts to replicate the behavior of
    the R ICD9 library.
    """
    
    decimal_code = str(decimal_code)

    unpacked = decimal_code.split(".")

    if len(unpacked) == 1:
        if len(decimal_code) <= 3 or (decimal_code.startswith("E") and len(decimal_code) <= 4):
            return ev_fill(decimal_code)
        else:
            return ""
    else:
        return "".join([ev_fill(unpacked[0]), unpacked[1]])


def short_to_decimal(short_code):
    """Converts short ICD9 codes to decimal codes. Attempts to replicate the behavior of 
    the R ICD9 library.
    """
    
    if len(short_code) <= 3 or (short_code.startswith("E") and len(short_code) <= 4):
        return ev_strip(short_code)
    elif short_code.startswith("E"):
        return ev_strip(short_code[:4]) + "." + short_code[4:]
    else:
        return ev_strip(short_code[:3]) + "." + short_code[3:]


def barell_isrcode(code):
    """Give the nature of an injury.
    """

    str_code = str(code)
    if   len(str_code) == 3: str_code += "00"
    elif len(str_code) == 4: str_code += "0"

    dx13 = int(str_code[0:3])
    dx14 = int(str_code[0:4]) 
    dx15 = int(str_code[0:5])
    D5   = int(str_code[-1])
    
    # Fractures:
    if 800 <= dx13 <= 829:
        isrcode = 1

    # Dislocations:
    elif 830 <= dx13 <= 839:
        isrcode = 2

    # Sprains / strains:
    elif 840 <= dx13 <= 848:
        isrcode = 3

    # Internal organ:
    elif (860 <= dx13 <= 869) or (850 <= dx13 <= 854) or \
         dx13 == 952 or dx15 == 99555:
        isrcode = 4

    # Open wounds:
    elif (870 <= dx13 <= 884) or (890 <= dx13 <= 894):
        isrcode = 5

    # Amputations:
    elif (885 <= dx13 <= 887) or (895 <= dx13 <= 897):
        isrcode = 6

    # Blood vessels:
    elif 900 <= dx13 <= 904:
        isrcode = 7

    # Superficial:
    elif 910 <= dx13 <= 924:
        isrcode = 8

    # Crushing:
    elif 925 <= dx13 <= 929:
        isrcode = 9

    # Burns:
    elif 940 <= dx13 <= 949:
        isrcode = 10

    # Nerves:
    elif (950 <= dx13 <= 951) or (953 <= dx13 <= 957):
        isrcode = 11

    # Unspecified:
    elif dx13 == 959:
        isrcode = 12

    # System-wide and late effects:
    elif (930 <= dx13 <= 939) or (960 <= dx13 <= 994) or (905 <= dx13 <= 908) or \
         (9090 <= dx14 <= 9092) or dx13 == 958 or (99550 <= dx15 <= 99554) or \
         dx15 == 99559 or dx14 == 9094 or dx14 == 9099 or (99580 <= dx15 <= 99585):
        isrcode = 13

    # Not a classifiable injury:
    else:
        isrcode = 0

    return isrcode

def barell_isrsite(x):
    str_code = str(code)
    if   len(str_code) == 3: str_code += "00"
    elif len(str_code) == 4: str_code += "0"

    dx13 = int(str_code[0:3])
    dx14 = int(str_code[0:4]) 
    dx15 = int(str_code[0:5])
    D5   = int(str_code[-1])

    # TYPE 1 TBI
    if (8001  <= dx14 <= 8004)  or (8006  <= dx14 <= 8009)  or \
       (80003 <= dx15 <= 80005) or (80053 <= dx15 <= 80055) or \
       (8011  <= dx14 <= 8014)  or (8016  <= dx14 <= 8019)  or \
       (80103 <= dx15 <= 80105) or (80153 <= dx15 <= 80155) or \
       (8031  <= dx14 <= 8034)  or (8036  <= dx14 <= 8039)  or \
       (80303 <= dx15 <= 80305) or (80353 <= dx15 <= 80355) or \
       (8041  <= dx14 <= 8044)  or (8046  <= dx14 <= 8049)  or \
       (80403 <= dx15 <= 80405) or (80453 <= dx15 <= 80455) or \
       (8502  <= dx14 <= 8504)  or (851   <= dx13 <= 854)   or \
       (9501  <= dx14 <= 9503)  or dx15 == 99555:
        isrsite = 1

    # TYPE 2 TBI
    elif dx15 in [80000, 80002, 80006, 80009, 80100, 80102, 80106, 80109,
                  80300, 80302, 80306, 80309, 80400, 80402, 80406, 80409,
                  80050, 80052, 80056, 80059, 80150, 80152, 80156, 80159,
                  80350, 80352, 80356, 80359, 80450, 80452, 80456, 80459] or \
         dx14 in [8500, 8501, 8505, 8509]:
        isrsite = 2

    # TYPE 3 TBI
    elif dx15 in [80001, 80051, 80101, 80151, 80301, 80351, 80401, 80451]:
        isrsite = 3

    # OTHER HEAD
    elif dx13 == 951 or dx14 in [8730, 8731, 8738, 8739] or \
         (dx13 == 941 and D5 == 6) or dx15 == 95901:
        isrsite = 4

    # FACE
    elif dx13 in [802, 830, 872] or dx14 in [8480, 8481] or \
         (8732 <= dx14 <= 8737) or (dx13 == 941 and D5 == 1) or \
         (dx13 == 941 and 3 <= D5 <= 5) or (dx13 == 941 and D5 == 7):
        isrsite = 5

    # EYE
    elif dx14 in [9500, 9509] or (870 <= dx13 <= 871) or \
         dx13 in [921, 918, 940] or (dx13 == 941 and D5 == 2):
        isrsite = 6

    # NECK
    elif (8075 <= dx14 <= 8076) or dx14 == 8482 or dx14 == 9252 or \
         dx14 == 9530 or dx14 == 9540 or dx13 == 874 or \
         (dx13 == 941 and D5 == 8):
        isrsite = 7

    # HEAD,FACE,NECK UNSPEC
    elif dx14 == 9251 or dx13 == 900 or dx14 == 9570 or dx13 == 910 or \
       dx13 == 920 or dx14 == 9470 or dx15 == 95909 or \
       (dx13 == 941 and (D5 == 0 or D5 == 9)):
        isrsite = 8

    # CERVICAL SCI
    elif (8060 <= dx14 <= 8061) or dx14 == 9520:
        isrsite = 9

    # THORACIC/DORSAL SCI
    elif (8062 <= dx14 <= 8063) or dx14 == 9521:
        isrsite = 10

    # LUMBAR SCI
    elif (8064 <= dx14 <= 8065) or (dx14 == 9522):
        isrsite = 11

    # SACRUM COCCYX SCI
    elif (8066 <= dx14 <= 8067) or (9523 <= dx14 <= 9524):
        isrsite = 12

    # SPINE+BACK UNSPEC SCI
    elif (8068 <= dx14 <= 8069) or (9528 <= dx14 <= 9529):
        isrsite = 13

    # CERVICAL VCI
    elif (8050 <= dx14 <= 8051) or (8390 <= dx14 <= 8391) or dx14 == 8470:
        isrsite = 14

    # THORACIC/DORSAL VCI
    elif (8052 <= dx14 <= 8053) or (83921 == dx15 or 83931 == dx15) or dx14 == 8471:
        isrsite = 15

    # LUMBAR VCI
    elif (8054 <= dx14 <= 8055) or (83920 == dx15 or 83930 == dx15) or dx14 == 8472:
        isrsite = 16

    # SACRUM COCCYX VCI
    elif (8056 <= dx14 <= 8057) or (83941 == dx15 or 83942 == dx15) or \
         (83951 <= dx15 <= 83952) or (8473 <= dx14 <= 8474):
        isrsite = 17
        
    # SPINE,BACK UNSPEC VCI
    elif (8058 <= dx14 <= 8059) or (83940 == dx15 or 83949 == dx15) or \
         (83950 == dx15 or dx15 == 83959):
        isrsite = 18

    # CHEST
    elif (8070 <= dx14 <= 8074) or dx15 == 83961 or dx15 == 83971 or (8483 <= dx14 <= 8484) or \
         dx15 == 92619 or (860 <= dx13 <= 862) or dx13 == 901 or dx14 == 9531 or dx13 == 875 or \
         dx14 == 8790 or dx14 == 8791 or dx14 == 9220 or dx14 == 9221 or dx15 == 92233 or \
         (dx13 == 942 and (D5 == 1 or D5 == 2)):
        isrsite = 19

    # ABDOMEN
    elif (863 <= dx13 <= 866) or dx13 == 868 or (9020 <= dx14 <= 9024) or \
         dx14 == 9532 or dx14 == 9535 or (8792 <= dx14 <= 8795) or \
         dx14==9222 or (dx13==942 and D5==3) or dx14==9473:
        isrsite=20

    # PELVIS+UROGENITAL
    elif dx13 == 808 or dx15 == 83969 or dx15 == 83979 or dx13 == 846 or \
         dx14 == 8485 or dx14 == 9260 or dx15 == 92612 or dx13 == 867 or \
         dx14 == 9025 or (90281 <= dx15 <= 90282) or dx14 == 9533 or \
         (877 <= dx13 <= 878) or dx14 == 9224 or (dx13 == 942 and D5 == 5) or \
         dx14 == 9474:
        isrsite = 21

    # TRUNK
    elif dx13 == 809 or (9268 <= dx14 <= 9269) or dx14 == 9541 or \
         (9548 <= dx14 <= 9549) or (8796 <= dx14 <= 8797) or \
         (9228 <= dx14<=9229) or dx13 == 911 or (dx13 == 942 and D5 == 0) or \
         (dx13 == 942 and D5 == 9) or dx14 == 9591:
        isrsite = 22

    # BACK+BUTTOCK
    elif dx14 == 8479 or dx15 == 92611 or dx13 == 876 or dx15 == 92232 or \
         dx15 == 92231 or (dx13 == 942 and D5 == 4):
        isrsite = 23

    # SHOULDER&UPPER ARM
    elif (810 <= dx13 <= 812) or dx13 == 831 or dx13 == 840 or dx13 == 880 or \
       8872 <= dx14 <= 8873 or (dx13 == 943 and 3 <= D5 <= 6) or dx13 == 912 or \
       dx14 == 9230 or dx14 == 9270 or dx14 == 9592:
        isrsite = 24

    # FOREARM&ELBOW
    elif dx13 == 813 or dx13 == 832 or dx13 == 841 or \
         (dx13 == 881 and 0 <= D5 <= 1) or (8870 <= dx14 <= 8871) or \
         dx14 == 9231 or dx14 == 9271 or (dx13 == 943 and 1 <= D5 <= 2):
        isrsite = 25

    # HAND&WRIST&FINGERS
    elif (814 <= dx13 <= 817) or (833 <= dx13 <= 834) or dx13 == 842 or \
         (dx13 == 881 and D5 == 2) or 882 <= dx13 <= 883 or \
         885 <= dx13 <= 886 or 914 <= dx13 <= 915 or 9232 <= dx14 <= 9233 or \
         9272 <= dx14 <= 9273 or dx13 == 944 or 9594 <= dx14 <= 9595:
        isrsite = 26

    # OTHER&UNSPEC UPPER EXTREM
    elif dx13 == 818 or dx13 == 884 or 8874 <= dx14 <= 8877 or dx13 == 903 or \
         dx13 == 913 or dx14 == 9593 or 9238 <= dx14 <= 9239 or \
         9278 <= dx14 <= 9279 or dx14 == 9534 or dx13 == 955 or \
         (dx13 == 943 and (D5 == 0 or D5 == 9)):
        isrsite = 27

    # HIP
    elif dx13 == 820 or dx13 == 835 or dx13 == 843 or \
         dx15 == 92401 or dx15 == 92801:
        isrsite = 28

    # UPPER LEG&THIGH
    elif dx13 == 821 or 8972 <= dx14 <= 8973 or dx15 == 92400 or \
         dx15 == 92800 or (dx13 == 945 and D5 == 6):
        isrsite = 29

    # KNEE
    elif dx13 == 822 or dx13 == 836 or 8440 <= dx14 <= 8443 or \
         dx15 == 92411 or dx15 == 92811 or (dx13 == 945 and D5 == 5):
        isrsite = 30

    # LOWER LEG&ANKLE
    elif 823 <= dx13 <= 824 or 8970 <= dx14 <= 8971 or dx13 == 837 or \
         dx14 == 8450 or dx15 == 92410 or dx15 == 92421 or dx15 == 92810 or \
         dx15 == 92821 or (dx13 == 945 and 3 <= D5 <= 4):
        isrsite = 31

    # FOOT&TOES
    elif 825 <= dx13 <= 826 or dx13 == 838 or dx14 == 8451 or \
         892 <= dx13 <=  893 or 895 <= dx13 <= 896 or dx13 == 917 or \
         dx15 == 92420 or dx14 ==  9243 or dx15 == 92820 or dx14 == 9283 or \
         (dx13 == 945 and 1 <= D5 <= 2):
        isrsite = 32

    # OTHER&UNSPEC LOWER EXTREM
    elif dx13 == 827 or 8448 <= dx14 <= 8449 or 890 <= dx13 <= 891 or \
         dx13 == 894 or 8974 <= dx14 <= 8977 or 9040 <= dx14 <= 9048 or \
         dx13 == 916 or 9244 <= dx14 <= 9245 or dx14 == 9288 or \
         dx14 == 9289 or 9596 <= dx14 <= 9597 or \
         (dx13 == 945 and (D5 == 0 or D5 == 9)):
        isrsite = 33

    # OTHER,MULTIPLE,NEC
    elif dx13 == 828 or dx13 == 819 or dx15 == 90287 or dx15 == 90289 or \
         dx14 == 9538 or 9471 <= dx14 <= 9472 or dx13 == 956:
        isrsite = 34

    # UNSPECIFIED
    elif dx13 == 829 or 8398 <= dx14 <= 8399 or 8488 <= dx14 <= 8489 or \
         dx13 == 869 or (8798 <= dx14 <= 8799) or dx14 == 9029 or \
         dx14 == 9049 or dx13 == 919 or 9248 <= dx14 <= 9249 or dx13 == 929 or \
         dx13 == 946 or 9478 <= dx14 <= 9479 or 948 <= dx13 <= 949 or \
         dx14 == 9539 or dx14 == 9571 or 9578 <= dx14 <= 9579 or \
         9598 <= dx14 <= 9599:
        isrsite = 35

    # SYSTEM WIDE & LATE EFFECTS
    elif (930 <= dx13 <= 939) or (960 <= dx13 <= 994) or \
         (905 <= dx13  <= 908) or (9090 <= dx14 <= 9092) or dx13 == 958 or \
         (99550 <= dx15  <= 99554) or dx15 == 99559 or dx14 == 9094 or \
         dx14 == 9099 or (99580 <= dx15 <= 99585):
        isrsite = 36

    # None of the above
    else:
        isrsite = 0

    return isrsite

def barell_isrsite2(x):
    dx13 = int(x.dx13) if x.dx13 != ''  else 0
    dx14 = int(x.dx14) if x.dx14 != ''  else 0
    dx15 = int(x.dx15) if x.dx15 != ''  else 0
    D5   = int(x.D5) if x.dx15 != ''  else 0
    
    isrsite = barell_isrsite(x)

    # TBI
    if isrsite >= 1 and isrsite <= 3: isrsite2 = 1
    
    # OTH HEAD,FACE,NECK
    elif isrsite >= 4 and isrsite <= 8: isrsite2 = 2

    # SCI
    elif isrsite >= 9 and isrsite <= 13: isrsite2 = 3

    # VCI
    elif isrsite >= 14 and isrsite <= 18: isrsite2 = 4

    # TORSO
    elif isrsite >= 19 and isrsite <= 23: isrsite2 = 5

    # UPPER EXTREMITY
    elif isrsite >= 24 and isrsite <= 27: isrsite2 = 6

    # LOWER EXTREMITY
    elif isrsite >= 28 and isrsite <= 33: isrsite2 = 7

    # OTHER & UNSPECIFIED
    elif isrsite >= 34 and isrsite <= 35: isrsite2 = 8

    # SYSTEM WIDE & LATE EFFECTS
    elif isrsite == 36: isrsite2 = 9

    # Not a classifiable injury
    else: isrsite2 = 0

    return isrsite2

def barell_isrsite3(x):
    dx13 = int(x.dx13) if x.dx13 != ''  else 0
    dx14 = int(x.dx14) if x.dx14 != ''  else 0
    dx15 = int(x.dx15) if x.dx15 != ''  else 0
    D5   = int(x.D5) if x.dx15 != ''  else 0
    
    isrsite = barell_isrsite(x)

    # HEAD&NECK
    if isrsite >= 1 and isrsite <= 8: isrsite3 = 1

    # SPINE&BACK
    elif isrsite >= 9 and isrsite <= 18: isrsite3 = 2

    # TORSO
    elif isrsite >= 19 and isrsite <= 23: isrsite3 = 3

    # EXTREMITIES
    elif isrsite >= 24 and isrsite <= 33: isrsite3 = 4

    # UNCLASSIFIABLE BY SITE
    elif isrsite >= 34 and isrsite <= 36: isrsite3 = 5

    # Not a classifiable injury
    else: isrsite3 = 0

    return isrsite3

def label_site(isrsite):
    
    if isrsite == 1: ISM = 'TYPE 1 TBI'
    elif isrsite == 2: ISM = 'TYPE 2 TBI'
    elif isrsite == 3: ISM = 'TYPE 3 TBI'
    elif isrsite == 4: ISM = 'OTHER HEAD'
    elif isrsite == 5: ISM = 'FACE'
    elif isrsite == 6: ISM = 'EYE'
    elif isrsite == 7: ISM = 'NECK'
    elif isrsite == 8: ISM = 'HEAD,FACE,NECK UNSPEC'
    elif isrsite == 9: ISM = 'CERVICAL SCI'
    elif isrsite == 10: ISM = 'THORACIC/DORSAL SCI'
    elif isrsite == 11: ISM = 'LUMBAR SCI'
    elif isrsite == 12: ISM = 'SACRUM COCCYX SCI'
    elif isrsite == 13: ISM = 'SPINE+BACK UNSPEC SCI'
    elif isrsite == 14: ISM = 'CERVICAL VCI'
    elif isrsite == 15: ISM = 'THORACIC/DORSAL VCI'
    elif isrsite == 16: ISM = 'LUMBAR VCI'
    elif isrsite == 17: ISM = 'SACRUM COCCYX VCI'
    elif isrsite == 18: ISM = 'SPINE,BACK UNSPEC VCI'
    elif isrsite == 19: ISM = 'CHEST'
    elif isrsite == 20: ISM = 'ABDOMEN'
    elif isrsite == 21: ISM = 'PELVIS+UROGENITAL'
    elif isrsite == 22: ISM = 'TRUNK'
    elif isrsite == 23: ISM = 'BACK+BUTTOCK'
    elif isrsite == 24: ISM = 'SHOULDER&UPPER ARM'
    elif isrsite == 25: ISM = 'FOREARM&ELBOW'
    elif isrsite == 26: ISM = 'HAND&WRIST&FINGERS'           
    elif isrsite == 27: ISM = 'OTHER&UNSPEC UPPER EXTREM'   
    elif isrsite == 28: ISM = 'HIP'
    elif isrsite == 29: ISM = 'UPPER LEG&THIGH'
    elif isrsite == 30: ISM = 'KNEE'
    elif isrsite == 31: ISM = 'LOWER LEG&ANKLE'             
    elif isrsite == 32: ISM = 'FOOT&TOES' 
    elif isrsite == 33: ISM = 'OTHER&UNSPEC LOWER EXTREM'                  
    elif isrsite == 34: ISM = 'OTHER,MULTIPLE,NEC'
    elif isrsite == 35: ISM = 'UNSPECIFIED'
    elif isrsite == 36: ISM = 'SYSTEM WIDE & LATE EFFECTS'
    else: ISM = ''

    return ISM

def label_site2(isrsite2):

    if isrsite2 == 1: I2M = 'TBI'
    elif isrsite2 == 2: I2M = 'OTH HEAD,FACE,NECK'
    elif isrsite2 == 3: I2M = 'SCI'
    elif isrsite2 == 4: I2M = 'VCI'
    elif isrsite2 == 5: I2M = 'TORSO'
    elif isrsite2 == 6: I2M = 'UPPER EXTREMITY'
    elif isrsite2 == 7: I2M = 'LOWER EXTREMITY'
    elif isrsite2 == 8: I2M = 'OTHER & UNSPECIFIED'
    elif isrsite2 == 9: I2M = 'SYSTEM WIDE & LATE EFFECTS'
    else: I2M = ''

    return I2M

def label_site3(isrsite3):

    if isrsite3 == 1: I3M = 'HEAD&NECK'
    elif isrsite3 == 2: I3M = 'SPINE&BACK'
    elif isrsite3 == 3: I3M = 'TORSO'
    elif isrsite3 == 4: I3M = 'EXTREMITIES'
    elif isrsite3 == 5: I3M = 'UNCLASSIFIABLE BY SITE';
    else: I3M = ''

    return I3M

def label_code(isrcode):

    if isrcode == 1: INM = 'FRACTURES '
    elif isrcode == 2: INM = 'DISLOCATION'
    elif isrcode == 3: INM = 'SPRAINS&STRAINS'
    elif isrcode == 4: INM = 'INTERNAL ORGAN '
    elif isrcode == 5: INM = 'OPEN WOUNDS'
    elif isrcode == 6: INM = 'AMPUTATIONS'
    elif isrcode == 7: INM = 'BLOOD VESSELS'
    elif isrcode == 8: INM = 'SUPERFIC/CONT'
    elif isrcode == 9: INM = 'CRUSHING'
    elif isrcode == 10: INM = 'BURNS'
    elif isrcode == 11: INM = 'NERVES'
    elif isrcode == 12: INM = 'UNSPECIFIED'
    elif isrcode == 13: INM = 'SYSTEM WIDE & LATE EFFECTS'
    else: INM = ''

    return INM
