*** Settings ***
Library    ../lib/PhoneComponent.py    &{phone_A}    WITH NAME    P1
Library    ../lib/PhoneComponent.py    &{phone_B}    WITH NAME    P2
Library    ../lib/PhoneComponent.py    &{phone_C}    WITH NAME    P3
Library    ../lib/PhoneComponent.py    &{phone_D}    WITH NAME    P4
Library    ../lib/PhoneComponent.py    &{phone_E}    WITH NAME    P5


*** Variables ***
# DO NOT CHANGE THE ORDER OF THE PHONES. THIS COULD AFFECT THE EXECUTION
&{phone_A}    phoneModel=Mitel6930     ipAddress=10.112.91.21    extensionNumber=41015    phoneName=Ishan3 G
&{phone_B}    phoneModel=Mitel6867i    ipAddress=10.112.91.93    extensionNumber=80020    phoneName=Shivam2 S
&{phone_C}    phoneModel=Mitel6865i    ipAddress=10.112.91.31    extensionNumber=80019    phoneName=Manoj4 K
&{phone_D}    phoneModel=Mitel6869i    ipAddress=10.112.91.29    extensionNumber=80021    phoneName=Shivam3 S
&{phone_E}    phoneModel=Mitel6869i    ipAddress=10.112.91.94    extensionNumber=41006    phoneName=Surender2 S

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

Phone_C_Initialization
    ${PhoneA}=    GET LIBRARY INSTANCE    P3
    ${PhoneB}=    GET LIBRARY INSTANCE    P2
    ${PhoneC}=    GET LIBRARY INSTANCE    P1
    ${PhoneD}=    GET LIBRARY INSTANCE    P4
    ${PhoneE}=    GET LIBRARY INSTANCE    P5
    [Return]    ${PhoneA}    ${PhoneB}    ${PhoneC}    ${PhoneD}    ${PhoneE}

Phone_E_Initialization
    ${PhoneA}=    GET LIBRARY INSTANCE    P5
    ${PhoneB}=    GET LIBRARY INSTANCE    P4
    ${PhoneC}=    GET LIBRARY INSTANCE    P3
    ${PhoneD}=    GET LIBRARY INSTANCE    P2
    ${PhoneE}=    GET LIBRARY INSTANCE    P1
    [Return]    ${PhoneA}    ${PhoneB}    ${PhoneC}    ${PhoneD}    ${PhoneE}