*** Settings ***
Library    ../lib/PhoneComponent.py    &{phone_A}    WITH NAME    P1
Library    ../lib/PhoneComponent.py    &{phone_B}    WITH NAME    P2
Library    ../lib/PhoneComponent.py    &{phone_C}    WITH NAME    P3
Library    ../lib/PhoneComponent.py    &{phone_D}    WITH NAME    P4


*** Variables ***

&{phone_A}    phoneModel=Mitel6930    ipAddress=10.112.123.183    extensionNumber=5004    phoneName=5004
&{phone_B}    phoneModel=Mitel6920    ipAddress=10.112.123.196    extensionNumber=5000    phoneName=5000
&{phone_C}    phoneModel=Mitel6867i   ipAddress=10.112.123.95     extensionNumber=5006    phoneName=5006
&{phone_D}    phoneModel=Mitel6865i   ipAddress=10.112.123.177    extensionNumber=5005    phoneName=5005
#&{phone_E}    phoneModel=Mitel6940     ipAddress=10.112.123.102    extensionNumber=    phoneName=

*** Keywords ***
Phone_A_Initialization
    ${PhoneA}=    GET LIBRARY INSTANCE    P1
    ${PhoneB}=    GET LIBRARY INSTANCE    P2
    ${PhoneC}=    GET LIBRARY INSTANCE    P3
    ${PhoneD}=    GET LIBRARY INSTANCE    P4
    [Return]    ${PhoneA}    ${PhoneB}    ${PhoneC}    ${PhoneD}

Phone_B_Initialization
    ${PhoneA}=    GET LIBRARY INSTANCE    P2
    ${PhoneB}=    GET LIBRARY INSTANCE    P1
    ${PhoneC}=    GET LIBRARY INSTANCE    P3
    ${PhoneD}=    GET LIBRARY INSTANCE    P4
    [Return]    ${PhoneA}    ${PhoneB}    ${PhoneC}    ${PhoneD}

Phone_C_Initialization
    ${PhoneA}=    GET LIBRARY INSTANCE    P3
    ${PhoneB}=    GET LIBRARY INSTANCE    P2
    ${PhoneC}=    GET LIBRARY INSTANCE    P1
    ${PhoneD}=    GET LIBRARY INSTANCE    P4
    [Return]    ${PhoneA}    ${PhoneB}    ${PhoneC}    ${PhoneD}

Phone_D_Initialization
    ${PhoneA}=    GET LIBRARY INSTANCE    P4
    ${PhoneB}=    GET LIBRARY INSTANCE    P3
    ${PhoneC}=    GET LIBRARY INSTANCE    P2
    ${PhoneD}=    GET LIBRARY INSTANCE    P1
    [Return]    ${PhoneA}    ${PhoneB}    ${PhoneC}    ${PhoneD}