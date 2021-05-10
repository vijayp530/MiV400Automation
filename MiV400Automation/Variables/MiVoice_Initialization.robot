*** Settings ***
Library    ../lib/PhoneComponent.py    &{phone_A}    WITH NAME    p1
Library    ../lib/PhoneComponent.py    &{phone_B}    WITH NAME    p2
Library    ../lib/PhoneComponent.py    &{phone_C}    WITH NAME    p3
Library    ../lib/PhoneComponent.py    &{phone_D}    WITH NAME    p4
Library    ../lib/PhoneComponent.py    &{phone_E}    WITH NAME    p5
Library    ../lib/PhoneComponent.py    &{phone_F}    WITH NAME    p6
#Library    ../lib/PhoneComponent.py    &{phone_G1}    WITH NAME    p7

*** Variables ***
&{phone_A}    phoneModel=Mitel6930    ipAddress=10.112.123.179     extensionNumber=4021    phoneName=auto user4021    hq_rsa=hq_rsa
&{phone_B}    phoneModel=Mitel6920    ipAddress=10.112.123.186     extensionNumber=4071    phoneName=auto user4071    hq_rsa=hq_rsa
&{phone_C}    phoneModel=Mitel6920    ipAddress=10.112.123.157     extensionNumber=4020    phoneName=auto user4020    hq_rsa=hq_rsa
&{phone_D}    phoneModel=Mitel6920    ipAddress=10.112.123.113     extensionNumber=4014    phoneName=auto user4014    hq_rsa=hq_rsa
&{phone_E}    phoneModel=Mitel6940    ipAddress=10.112.123.40      extensionNumber=4011    phoneName=auto user4011    hq_rsa=hq_rsa
&{phone_F}    phoneModel=Mitel6910    ipAddress=10.112.123.82      extensionNumber=4006    phoneName=auto user4006    hq_rsa=hq_rsa

#&{phone_A}    phoneModel=Mitel6930    ipAddress=10.112.123.108     extensionNumber=4070    phoneName=auto user4070    hq_rsa=hq_rsa

*** Keywords ***
Phone_A_Initialization_MiVoice
    ${PhoneA}=    GET LIBRARY INSTANCE    P1
    ${PhoneB}=    GET LIBRARY INSTANCE    P2
    ${PhoneC}=    GET LIBRARY INSTANCE    P3
    ${PhoneD}=    GET LIBRARY INSTANCE    P4
    ${PhoneE}=    GET LIBRARY INSTANCE    P5
    ${PhoneF}=    GET LIBRARY INSTANCE    P6
    [Return]    ${PhoneA}    ${PhoneB}    ${PhoneC}    ${PhoneD}    ${PhoneE}    ${PhoneF}

Phone_B_Initialization_MiVoice
    ${PhoneA}=    GET LIBRARY INSTANCE    P2
    ${PhoneB}=    GET LIBRARY INSTANCE    P1
    ${PhoneC}=    GET LIBRARY INSTANCE    P3
    ${PhoneD}=    GET LIBRARY INSTANCE    P4
    ${PhoneE}=    GET LIBRARY INSTANCE    P5
    ${PhoneF}=    GET LIBRARY INSTANCE    P6
    [Return]    ${PhoneA}    ${PhoneB}    ${PhoneC}    ${PhoneD}    ${PhoneE}    ${PhoneF}

Phone_C_Initialization_MiVoice
    ${PhoneA}=    GET LIBRARY INSTANCE    P3
    ${PhoneB}=    GET LIBRARY INSTANCE    P2
    ${PhoneC}=    GET LIBRARY INSTANCE    P1
    ${PhoneD}=    GET LIBRARY INSTANCE    P4
    ${PhoneE}=    GET LIBRARY INSTANCE    P5
    ${PhoneF}=    GET LIBRARY INSTANCE    P6
    [Return]    ${PhoneA}    ${PhoneB}    ${PhoneC}    ${PhoneD}    ${PhoneE}    ${PhoneF}

Phone_E_Initialization_MiVoice
    ${PhoneA}=    GET LIBRARY INSTANCE    P5
    ${PhoneB}=    GET LIBRARY INSTANCE    P4
    ${PhoneC}=    GET LIBRARY INSTANCE    P3
    ${PhoneD}=    GET LIBRARY INSTANCE    P2
    ${PhoneE}=    GET LIBRARY INSTANCE    P1
    ${PhoneF}=    GET LIBRARY INSTANCE    P6
    [Return]    ${PhoneA}    ${PhoneB}    ${PhoneC}    ${PhoneD}    ${PhoneE}    ${PhoneF}

Phone_F_Initialization_MiVoice
    ${PhoneA}=    GET LIBRARY INSTANCE    P6
    ${PhoneB}=    GET LIBRARY INSTANCE    P5
    ${PhoneC}=    GET LIBRARY INSTANCE    P4
    ${PhoneD}=    GET LIBRARY INSTANCE    P3
    ${PhoneE}=    GET LIBRARY INSTANCE    P2
    ${PhoneF}=    GET LIBRARY INSTANCE    P1
    [Return]    ${PhoneA}    ${PhoneB}    ${PhoneC}    ${PhoneD}    ${PhoneE}    ${PhoneF}
