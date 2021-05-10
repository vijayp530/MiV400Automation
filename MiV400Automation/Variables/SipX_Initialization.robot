*** Settings ***
Library    ../lib/PhoneComponent.py    &{phone_S1}    WITH NAME    S1
Library    ../lib/PhoneComponent.py    &{phone_S2}    WITH NAME    S2


*** Variables ***
&{phone_S1}    phoneModel=    ipAddress=    extensionNumber=    phoneName=
&{phone_S2}    phoneModel=    ipAddress=   extensionNumber=    phoneName=

*** Keywords ***
SipX_PhoneA_Initialization
    ${PhoneA}=    GET LIBRARY INSTANCE    S1
    ${PhoneB}=    GET LIBRARY INSTANCE    S2
    [return]    ${PhoneA}    ${PhoneB}

SipX_PhoneB_Initialization
    ${PhoneA}=    GET LIBRARY INSTANCE    S2
    ${PhoneB}=    GET LIBRARY INSTANCE    S1
    [return]    ${PhoneA}    ${PhoneB}