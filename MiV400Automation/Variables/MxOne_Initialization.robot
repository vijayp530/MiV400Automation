*** Settings ***
Library    ../lib/PhoneComponent.py    &{phone_A}    WITH NAME    P1
Library    ../lib/PhoneComponent.py    &{phone_B}    WITH NAME    P2
Library    ../lib/PhoneComponent.py    &{phone_C}    WITH NAME    P3
#Library    ../lib/PhoneComponent.py    &{phone_D}    WITH NAME    P4
#Library    ../lib/PhoneComponent.py    &{phone_E}    WITH NAME    P5


*** Variables ***

# SANITY PHONES
&{phone_A}    phoneModel=Mitel6930     ipAddress=10.112.123.21    extensionNumber=4165142503    phoneName=4165142503
#&{phone_B}    phoneModel=Mitel6930     ipAddress=10.112.123.119   extensionNumber=4165142501    phoneName=4165142501
#&{phone_C}    phoneModel=Mitel6920     ipAddress=10.112.123.146   extensionNumber=4165142502    phoneName=4165142502
&{phone_B}    phoneModel=Mitel6867i    ipAddress=10.112.123.30    extensionNumber=4165142504    phoneName=4165142504
#&{phone_E}    phoneModel=Mitel6865i    ipAddress=10.112.123.177   extensionNumber=4165142505    phoneName=4165142505
&{phone_C}    phoneModel=Mitel6940     ipAddress=10.112.123.73    extensionNumber=4165142502    phoneName=4165142502

#&{phone_A}    phoneModel=Mitel6930     ipAddress=10.112.123.139      extensionNumber=4165142501    phoneName=4165142501
#&{phone_D}    phoneModel=Mitel6930     ipAddress=10.112.91.72        extensionNumber=4165142504    phoneName=4165142504
#&{phone_A}    phoneModel=Mitel6930    ipAddress=10.112.123.55      extensionNumber=4165142521    phoneName=4165142521
#&{phone_B}    phoneModel=Mitel6930    ipAddress=10.112.123.39     extensionNumber=4165142518    phoneName=4165142518
#&{phone_D}    phoneModel=Mitel6865i    ipAddress=10.112.123.91    extensionNumber=4165142515    phoneName=4165142515
#&{phone_C}    phoneModel=Mitel6867i    ipAddress=10.112.123.23       extensionNumber=4165142539    phoneName=4165142539
#&{phone_A}    phoneModel=Mitel6930    ipAddress=10.112.123.177      extensionNumber=4165142526    phoneName=4165142526
#&{phone_C}    phoneModel=Mitel6920    ipAddress=10.112.123.197    extensionNumber=4165142519    phoneName=4165142519

# ARABIC LANGUAGE
#&{phone_B}    phoneModel=Mitel6920    ipAddress=10.112.123.146    extensionNumber=4165142501    phoneName=4165142501    #hq_rsa=hq_rsa
#&{phone_A}    phoneModel=Mitel6930    ipAddress=10.112.123.139    extensionNumber=4165142502    phoneName=4165142502    #hq_rsa=hq_rsa
#&{phone_A}    phoneModel=Mitel6930    ipAddress=10.112.123.190    extensionNumber=4165142526    phoneName=4165142526    #hq_rsa=hq_rsa
#&{phone_C}    phoneModel=Mitel6920    ipAddress=10.112.123.60    extensionNumber=4165142527    phoneName=4165142527    #hq_rsa=hq_rsa

#
#10.112.91.151   6867i    4165142503
#10.112.123.166    6920    4165142512
#10.112.91.107    6865i    4165142511
# 10.112.123.135

*** Keywords ***
Phone_A_Initialization
    ${PhoneA}=    GET LIBRARY INSTANCE    P1
    ${PhoneB}=    GET LIBRARY INSTANCE    P2
    ${PhoneC}=    GET LIBRARY INSTANCE    P3
#    ${PhoneD}=    GET LIBRARY INSTANCE    P4
#    ${PhoneE}=    GET LIBRARY INSTANCE    P5
    [Return]    ${PhoneA}    ${PhoneB}    ${PhoneC}    #${PhoneD}    #${PhoneE}

Phone_B_Initialization
    ${PhoneA}=    GET LIBRARY INSTANCE    P2
    ${PhoneB}=    GET LIBRARY INSTANCE    P1
    ${PhoneC}=    GET LIBRARY INSTANCE    P3
    ${PhoneD}=    GET LIBRARY INSTANCE    P4
    ${PhoneE}=    GET LIBRARY INSTANCE    P5
    [Return]    ${PhoneA}    ${PhoneB}    ${PhoneC}    ${PhoneD}    ${PhoneE}

Phone_C_Initialization
    ${PhoneA}=    GET LIBRARY INSTANCE    P3
    ${PhoneB}=    GET LIBRARY INSTANCE    P2
    ${PhoneC}=    GET LIBRARY INSTANCE    P1
    ${PhoneD}=    GET LIBRARY INSTANCE    P4
    ${PhoneE}=    GET LIBRARY INSTANCE    P5
    [Return]    ${PhoneA}    ${PhoneB}    ${PhoneC}    ${PhoneD}    ${PhoneE}

Phone_D_Initialization
    ${PhoneA}=    GET LIBRARY INSTANCE    P4
    ${PhoneB}=    GET LIBRARY INSTANCE    P3
    ${PhoneC}=    GET LIBRARY INSTANCE    P2
    ${PhoneD}=    GET LIBRARY INSTANCE    P1
    [Return]    ${PhoneA}    ${PhoneB}    ${PhoneC}    ${PhoneD}

Phone_E_Initialization
    ${PhoneA}=    GET LIBRARY INSTANCE    P5
    ${PhoneB}=    GET LIBRARY INSTANCE    P4
    ${PhoneC}=    GET LIBRARY INSTANCE    P3
    ${PhoneD}=    GET LIBRARY INSTANCE    P2
    ${PhoneE}=    GET LIBRARY INSTANCE    P1
    [Return]    ${PhoneA}    ${PhoneB}    ${PhoneC}    ${PhoneD}    ${PhoneE}


# Network 30-5
# 10.112.123.183           6930         Asterisk
# 123.84                   6930         Asterisk
# 123.91                   6865i        Asterisk
# 123.30                   6867i        Asterisk         Arabic
