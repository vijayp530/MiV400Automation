*** Settings ***
Library    ../lib/PhoneComponent.py    &{phone_A}    WITH NAME    P1
Library    ../lib/PhoneComponent.py    &{phone_B}    WITH NAME    P2
Library    ../lib/PhoneComponent.py    &{phone_C}    WITH NAME    P3
Library    ../lib/PhoneComponent.py    &{phone_D}    WITH NAME    P4
Library    ../lib/PhoneComponent.py    &{phone_E}    WITH NAME    P5


*** Variables ***
&{phone_A}    phoneModel=Mitel6930     ipAddress=10.112.91.72    extensionNumber=9053331137    phoneName=9053331137
&{phone_B}    phoneModel=Mitel6867i    ipAddress=10.112.91.151   extensionNumber=9053331138    phoneName=9053331138
&{phone_C}    phoneModel=Mitel6865i    ipAddress=10.112.91.64    extensionNumber=9053331139    phoneName=9053331139
&{phone_D}    phoneModel=Mitel6869i    ipAddress=10.112.91.225   extensionNumber=9053331136    phoneName=9053331136
&{phone_E}    phoneModel=Mitel6867i    ipAddress=10.112.91.47    extensionNumber=9053331140    phoneName=9053331140

#&{phone_A}    phoneModel=Mitel6930     ipAddress=10.112.91.223    extensionNumber=9053331141    phoneName=9053331141    #hq_rsa=hq_rsa
#&{phone_B}    phoneModel=Mitel6867i    ipAddress=10.112.91.38     extensionNumber=9053331137    phoneName=9053331137    #hq_rsa=hq_rsa
#&{phone_C}    phoneModel=Mitel6867i    ipAddress=10.112.91.224     extensionNumber=9053331139    phoneName=9053331139    #hq_rsa=hq_rsa
#&{phone_D}    phoneModel=Mitel6869i    ipAddress=10.112.91.225     extensionNumber=9053331138    phoneName=9053331138    #hq_rsa=hq_rsa

*** Keywords ***
Phone_A_Initialization
    ${PhoneA}=    GET LIBRARY INSTANCE    P1
    ${PhoneB}=    GET LIBRARY INSTANCE    P2
    ${PhoneC}=    GET LIBRARY INSTANCE    P3
    ${PhoneD}=    GET LIBRARY INSTANCE    P4
    ${PhoneE}=    GET LIBRARY INSTANCE    P5
    [Return]    ${PhoneA}    ${PhoneB}    ${PhoneC}    ${PhoneD}    ${PhoneE}

Phone_B_Initialization
    ${PhoneA}=    GET LIBRARY INSTANCE    P2
    ${PhoneB}=    GET LIBRARY INSTANCE    P1
    ${PhoneC}=    GET LIBRARY INSTANCE    P3
    ${PhoneD}=    GET LIBRARY INSTANCE    P4
    ${PhoneE}=    GET LIBRARY INSTANCE    P5
    [Return]    ${PhoneA}    ${PhoneB}    ${PhoneC}    ${PhoneD}    ${PhoneE}