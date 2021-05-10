*** Settings ***
Library    ../lib/PhoneComponent.py    &{phone_A}    WITH NAME    A1
Library    ../lib/PhoneComponent.py    &{phone_B}    WITH NAME    A2
Library    ../lib/PhoneComponent.py    &{phone_C}    WITH NAME    A3
#Library    ../lib/PhoneComponent_vk.py    &{phone_D}    WITH NAME    A4

*** Variables ***

##&{phone_A}    phoneModel=Mitel6930    ipAddress=10.112.123.44    extensionNumber=4165142541    phoneName=4165142541    hq_rsa=hq_rsa
#&{phone_A}    phoneModel=Mitel6867i    ipAddress=10.112.123.81    extensionNumber=4165142542    phoneName=4165142542    hq_rsa=hq_rsa
#&{phone_B}    phoneModel=Mitel6865i    ipAddress=10.112.123.51    extensionNumber=4165142541    phoneName=4165142541    hq_rsa=hq_rsa
#&{phone_C}    phoneModel=Mitel6867i    ipAddress=10.112.123.23    extensionNumber=4165142544    phoneName=4165142544    hq_rsa=hq_rsa
##&{phone_A}    phoneModel=Mitel6930    ipAddress=10.112.123.67    extensionNumber=4165142536    phoneName=4165142536    hq_rsa=hq_rsa
##&{phone_B}    phoneModel=Mitel6920    ipAddress=10.112.123.157    extensionNumber=4165142535    phoneName=4165142535    hq_rsa=hq_rsa


#&{phone_D}    phoneModel=Mitel6920     ipAddress=10.112.123.146      extensionNumber=4165142502    phoneName=4165142502
&{phone_C}    phoneModel=Mitel6930    ipAddress=10.112.123.43     extensionNumber=4165142502    phoneName=4165142502
#&{phone_B}    phoneModel=Mitel6867i    ipAddress=10.112.123.30       extensionNumber=4165142503    phoneName=4165142503
&{phone_A}    phoneModel=Mitel6930    ipAddress=10.112.123.175      extensionNumber=4165142526    phoneName=4165142526


*** Keywords ***
Asterisk_PhoneA_Initialization
    ${PhoneA}=    GET LIBRARY INSTANCE    A1
    ${PhoneB}=    GET LIBRARY INSTANCE    A2
    ${PhoneC}=    GET LIBRARY INSTANCE    A3
    #${PhoneD}=    GET LIBRARY INSTANCE    A4
    #[Return]    ${PhoneA}    ${PhoneB}
    [return]    ${PhoneA}    ${PhoneB}    ${PhoneC}    #${PhoneD}

Asterisk_PhoneB_Initialization
    ${PhoneA}=    GET LIBRARY INSTANCE    A2
    ${PhoneB}=    GET LIBRARY INSTANCE    A1
    ${PhoneC}=    GET LIBRARY INSTANCE    A3
    #${PhoneD}=    GET LIBRARY INSTANCE    A4
    [return]    ${PhoneA}    ${PhoneB}    ${PhoneC}    #${PhoneD}