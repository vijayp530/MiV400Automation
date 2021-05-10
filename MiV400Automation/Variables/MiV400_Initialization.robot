*** Settings ***
Library    ../lib/PhoneComponent.py    &{phone_A}    WITH NAME    P1
Library    ../lib/PhoneComponent.py    &{phone_B}    WITH NAME    P2
Library    ../lib/PhoneComponent.py    &{phone_C}    WITH NAME    P3
Library    ../lib/PhoneComponent.py    &{phone_D}    WITH NAME    P4


*** Variables ***
#&{phone_A}    phoneModel=Mitel6920    ipAddress=10.211.140.32   extensionNumber=4810    phoneName=4810
#&{phone_A}    phoneModel=Mitel6930    ipAddress=10.112.123.172   extensionNumber=4165142532    phoneName=4165142532
&{phone_A}    phoneModel=Mitel6930    ipAddress=10.211.22.240   extensionNumber=3001   phoneName=User3001
&{phone_B}    phoneModel=Mitel6940    ipAddress=10.211.22.86   extensionNumber=3002    phoneName=User3002
&{phone_C}    phoneModel=Mitel6867i   ipAddress=10.211.22.241   extensionNumber=3003    phoneName=User3003
&{phone_D}    phoneModel=Mitel6865i   ipAddress=10.211.22.242   extensionNumber=3000    phoneName=3000
#&{phone_B}    phoneModel=Mitel6865i     ipAddress=10.211.22.242    extensionNumber=3000    phoneName=3000

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





