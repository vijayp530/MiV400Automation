*** Settings ***
Library    ../lib/PhoneComponent.py    &{phone_A}    WITH NAME    P1
Library    ../lib/PhoneComponent.py    &{phone_B}    WITH NAME    P2
Library    ../lib/PhoneComponent.py    &{phone_C}    WITH NAME    P3
Library    ../lib/PhoneComponent.py    &{phone_D}    WITH NAME    P4
#Library    ../lib/PhoneComponent.py    &{phone_E}    WITH NAME    P5
#Library    ../lib/PhoneComponent.py    &{phone_F}    WITH NAME    P6


*** Variables ***
&{phone_A}    phoneModel=Mitel6930    ipAddress=10.112.123.117    extensionNumber=1019    phoneName=Test User 1019    hq_rsa=hq_rsa_pit
&{phone_B}    phoneModel=Mitel6920    ipAddress=10.112.123.14     extensionNumber=1011    phoneName=Test User 1011    hq_rsa=hq_rsa_pit
&{phone_C}    phoneModel=Mitel6920    ipAddress=10.112.123.50     extensionNumber=1010    phoneName=Test User 1010    hq_rsa=hq_rsa_pit
&{phone_D}    phoneModel=Mitel6910    ipAddress=10.112.123.36     extensionNumber=1008    phoneName=Test User 1008    hq_rsa=hq_rsa_pit

*** Keywords ***
MiCloud_PhoneA_Initialization
    ${PhoneA}=    GET LIBRARY INSTANCE    P1
    ${PhoneB}=    GET LIBRARY INSTANCE    P2
    ${PhoneC}=    GET LIBRARY INSTANCE    P3
    ${PhoneD}=    GET LIBRARY INSTANCE    P4
#    ${PhoneE}=    GET LIBRARY INSTANCE    P5
#    ${PhoneF}=    GET LIBRARY INSTANCE    P6
##    ${PhoneG}=    GET LIBRARY INSTANCE    P7
    [Return]    ${PhoneA}    ${PhoneB}    ${PhoneC}    ${PhoneD}    #${PhoneE}    #${PhoneF}    ${PhoneG}

MiCloud_PhoneB_Initialization
    ${PhoneA}=    GET LIBRARY INSTANCE    P2
    ${PhoneB}=    GET LIBRARY INSTANCE    P1
    ${PhoneC}=    GET LIBRARY INSTANCE    P3
    ${PhoneD}=    GET LIBRARY INSTANCE    P4
#    ${PhoneE}=    GET LIBRARY INSTANCE    P5
#    ${PhoneF}=    GET LIBRARY INSTANCE    P6
##    ${PhoneG}=    GET LIBRARY INSTANCE    P7
    [Return]    ${PhoneA}    ${PhoneB}    ${PhoneC}    ${PhoneD}    #${PhoneE}    #${PhoneF}    ${PhoneG}

MiCloud_PhoneC_Initialization
    ${PhoneA}=    GET LIBRARY INSTANCE    P3
    ${PhoneB}=    GET LIBRARY INSTANCE    P2
    ${PhoneC}=    GET LIBRARY INSTANCE    P1
    ${PhoneD}=    GET LIBRARY INSTANCE    P4
#    ${PhoneE}=    GET LIBRARY INSTANCE    P5
#    ${PhoneF}=    GET LIBRARY INSTANCE    P6
##    ${PhoneG}=    GET LIBRARY INSTANCE    P7
    [Return]    ${PhoneA}    ${PhoneB}    ${PhoneC}    ${PhoneD}    #${PhoneE}    #${PhoneF}    ${PhoneG}

MiCloud_PhoneD_Initialization
    ${PhoneA}=    GET LIBRARY INSTANCE    P4
    ${PhoneB}=    GET LIBRARY INSTANCE    P2
    ${PhoneC}=    GET LIBRARY INSTANCE    P3
    ${PhoneD}=    GET LIBRARY INSTANCE    P1
#    ${PhoneE}=    GET LIBRARY INSTANCE    P5
#    ${PhoneF}=    GET LIBRARY INSTANCE    P6
##    ${PhoneG}=    GET LIBRARY INSTANCE    P7
    [Return]    ${PhoneA}    ${PhoneB}    ${PhoneC}    ${PhoneD}    #${PhoneE}    #${PhoneF}    ${PhoneG}

#Phone_E_Initialization
#    ${PhoneA}=    GET LIBRARY INSTANCE    P5
#    ${PhoneB}=    GET LIBRARY INSTANCE    P4
#    ${PhoneC}=    GET LIBRARY INSTANCE    P3
#    ${PhoneD}=    GET LIBRARY INSTANCE    P2
#    ${PhoneE}=    GET LIBRARY INSTANCE    P1
##    ${PhoneF}=    GET LIBRARY INSTANCE    P6
##    ${PhoneG}=    GET LIBRARY INSTANCE    P7
#    [Return]    ${PhoneA}    ${PhoneB}    ${PhoneC}    ${PhoneD}    ${PhoneE}    #${PhoneF}    ${PhoneG}

# 123.202
# 123.83
# 123.38
