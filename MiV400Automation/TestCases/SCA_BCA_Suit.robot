*** Settings ***
Resource   ../RobotKeywords/Setup_And_Teardown.robot
Library    ../lib/MyListner.py

Test Timeout     25 minutes
Suite Setup      RUN KEYWORDS    Phones Initialization    Get Dut Details
Test Setup       Check Phone Connection
Test Teardown    RUN KEYWORDS    Default Call Appearance    Generic Test Teardown
Suite Teardown   RUN KEYWORD AND IGNORE ERROR    RUN KEYWORDS    Check Phone Connection    Generic Test Teardown

*** Test Cases ***
751232: TC:01 Inbound call -hold/unhold on Boss
    [Tags]    Owner:Ram    Reviewer:Vikhyat     SCA    holdUnhold    notApplicableFor6910    751232
    [Setup]    Telephony Feature Custom Setup
    &{telephonydetails} =  Create Dictionary    sca_enabled=True
    ${scaExtn} =  using ${bossPortal} on ${phone1} I want to enable SCA using ${telephonydetails}

    &{modifySCAExtension}=    CREATE DICTIONARY    extension=${scaExtn}   backupExtn=${phone1}    allowBridgeConferencing=true
    Given Using ${bossPortal} I want to modify Bridge Call Appearance extension using ${modifySCAExtension}

    &{BCAdetails} =  Create Dictionary    user_extension=${phone2}    button_box=0    soft_key=1    function=Bridge Call Appearance    label=BCA    target_extension=${scaExtn}    CallStackPosition=1    SecondaryType=Dial Tone
    Given using ${bossPortal} I want to create bca on ${phone2} using ${BCAdetails}
    Then on ${phone3} dial number ${scaExtn}
    Then on ${phone3} press the softkey ${dial} in dialingstate
    Then On ${phone1} Wait for 3 seconds
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then verify the led state of ${line2} as ${blink} on ${phone2}
    Then I want to press line key ${programKey1} on phone ${phone1}
    Then verify audio path between ${phone1} and ${phone3}
    Then Put the linekey ${line1} of ${phone1} on ${hold}
    Then On ${phone1} verify ${line1} icon state as ${bcaLocalHold}
    Then On ${phone2} verify ${line2} icon state as ${bcaLocalHold}
    Then On ${phone1} verify display message ${cancel}
    Then On ${phone3} verify ${line1} icon state as ${callAppearanceRemoteHold}
    Then On ${phone3} verify display message ${scaExtn}
    Then On ${phone1} press ${softkey} ${programKey1} for 1 times
    Then On ${phone1} verify the softkeys in ${talk}
    Then verify audio path between ${phone1} and ${phone3}
    And disconnect the call from ${phone3}
    [Teardown]    Telephony Feature Custom Teardown

751242: TC13: BCA Conference
    [Tags]    Owner:Aman    Reviewer:Vikhyat    BCA    SCA    conference    751242
    [Setup]    Telephony Feature Custom Setup
    &{telephonydetails}=  Create Dictionary    sca_enabled=True
    ${scaExtn} =  using ${bossPortal} on ${phone2} I want to enable SCA using ${telephonydetails}
    &{modifySCAExtension}=    CREATE DICTIONARY    extension=${scaExtn}   backupExtn=${phone3}    allowBridgeConferencing=true
    Given Using ${bossPortal} I want to modify Bridge Call Appearance extension using ${modifySCAExtension}

    &{BCAdetails1}=    Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=3    function=Bridge Call Appearance    label=BCA1    target_extension=${scaExtn}       CallStackPosition=1
    &{BCAdetails2}=    Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=4    function=Bridge Call Appearance    label=BCA2    target_extension=${scaExtn}       CallStackPosition=2
    Given using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails1}
    Given using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails2}
    Then On ${phone1} verify display message BCA1
    Then On ${phone1} verify display message BCA2

    Then on ${phone3} dial number ${scaExtn}
    Then on ${phone1} wait for 2 seconds
    Then verify the led state of ${line1} as ${blink} on ${phone2}
    Then verify the led state of ${line4} as ${blink} on ${phone1}
    Then Answer the call on ${phone1} using ${programKey4}
    Then on ${phone4} dial number ${scaExtn}
    Then on ${phone1} wait for 2 seconds
    Then verify the led state of ${line2} as ${blink} on ${phone2}
    Then verify the led state of ${line5} as ${blink} on ${phone1}
    Then Answer the call on ${phone1} using ${programKey5}
    Then verify the led state of ${line4} as ${blink} on ${phone1}
    Then verify the led state of ${line5} as ${on} on ${phone1}
    Then on ${phone1} press ${softKey} ${bottomKey2} for 1 times
    Then I want to press line key ${programKey4} on phone ${phone1}
    Then On ${phone1} Wait for 5 seconds
    Then verify the led state of ${line4} as ${on} on ${phone1}
    Then verify the led state of ${line5} as ${off} on ${phone1}
#    Then On ${phone1} verify ${line4} icon state as ${bcaConferenceActive}
#    Then On ${phone3} verify ${line1} icon state as ${callAppearanceConfActive}
#    Then On ${phone4} verify ${line1} icon state as ${callAppearanceConfActive}
    Then conference call audio verify between ${phone1} ${phone3} and ${phone4}
    Then On ${phone2} press ${softkey} ${programKey1} for 1 times
    Then On ${phone1} Wait for 5 seconds
#    Then On ${phone1} verify ${line4} icon state as ${bcaConferenceActive}
#    Then On ${phone2} verify ${line1} icon state as ${bcaConferenceActive}
#    Then On ${phone3} verify ${line1} icon state as ${callAppearanceConfActive}
#    Then On ${phone4} verify ${line1} icon state as ${callAppearanceConfActive}
    Then four party conference call audio verification between ${phone1} ${phone2} ${phone3} and ${phone4}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}
    And disconnect the call from ${phone4}
    [Teardown]    Telephony Feature Custom Teardown

751243: TC14: BCA Conference
    [Tags]    Owner:Aman    Reviewer:Vikhyat    BCA    SCA    conference    751243
    [Setup]    Telephony Feature Custom Setup
    &{telephonydetails} =  Create Dictionary    sca_enabled=True
    ${scaExtn} =  using ${bossPortal} on ${phone2} I want to enable SCA using ${telephonydetails}

    &{modifySCAExtension}=    CREATE DICTIONARY    extension=${scaExtn}   backupExtn=${phone3}    allowBridgeConferencing=true
    Given Using ${bossPortal} I want to modify Bridge Call Appearance extension using ${modifySCAExtension}

    &{BCAdetails} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=3    function=Bridge Call Appearance    label=BCA1    target_extension=${scaExtn}       CallStackPosition=1
    Then using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails}
    Then On ${phone1} verify display message BCA1

    Then I want to make a two party call between ${phone3} and ${phone4} using ${offHook}
    Then Answer the call on ${phone4} using ${offHook}
    Then Verify the Caller id on ${phone3} and ${phone4} display
    Then On ${phone4} press the softkey ${conference} in AnswerState
    Then On ${phone4} dial number ${scaExtn}
    Then On ${phone4} press ${softKey} ${bottomKey2} for 1 times
    Then Verify the led state of ${line1} as ${blink} on ${phone2}
    Then Verify the led state of ${line4} as ${blink} on ${phone1}
    Then Answer the call on ${phone1} using ${programKey4}
#    Then On ${phone1} verify ${line4} icon state as ${bcaConferenceActive}
#    Then On ${phone3} verify ${line1} icon state as ${callAppearanceConfActive}
#    Then On ${phone4} verify ${line1} icon state as ${callAppearanceConfActive}
    Then On ${phone1} verify display on a 3 party conference call
    Then conference call audio verify between ${phone1} ${phone3} and ${phone4}
    Then I want to press line key ${programKey1} on phone ${phone2}
    Then On ${phone1} Wait for 5 seconds
    Then On ${phone1} verify display on a 4 party conference call
#    Then On ${phone1} verify ${line4} icon state as ${bcaConferenceActive}
#    Then On ${phone2} verify ${line1} icon state as ${bcaConferenceActive}
#    Then On ${phone3} verify ${line1} icon state as ${callAppearanceConfActive}
#    Then On ${phone4} verify ${line1} icon state as ${callAppearanceConfActive}
    Then Four party conference call audio verification between ${phone1} ${phone2} ${phone3} and ${phone4}
    Then Disconnect the call from ${phone2}
    Then Disconnect the call from ${phone3}
    And Disconnect the call from ${phone4}
    [Teardown]    Telephony Feature Custom Teardown

751231: TC02: Outbound Call - Hold on Boss , unhold on Admin
    [Tags]    Owner:Aman    Reviewer:Vikhyat    BCA    SCA    holdUnhold    751231
    [Setup]    Telephony Feature Custom Setup
    &{telephonydetails} =  Create Dictionary    sca_enabled=True
    ${scaExtn}=  using ${bossPortal} on ${phone2} I want to enable SCA using ${telephonydetails}

    &{modifySCAExtension}=    CREATE DICTIONARY    extension=${scaExtn}   backupExtn=${phone3}    allowBridgeConferencing=true
    Given Using ${bossPortal} I want to modify Bridge Call Appearance extension using ${modifySCAExtension}

    &{BCAdetails} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=3    function=Bridge Call Appearance    label=BCA1    target_extension=${scaExtn}       CallStackPosition=1
    Given using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails}
    Then On ${phone1} verify display message BCA1
    Then I want to make a two party call between ${phone2} and ${phone3} using ${offHook}
    Then Answer the call on ${phone3} using ${offHook}
    Then Verify audio path between ${phone2} and ${phone3}
    Then On ${phone2} verify ${line1} icon state as ${bcaActive}
    Then On ${phone3} verify ${line1} icon state as ${callAppearanceActive}
    Then On ${phone1} verify ${line4} icon state as ${bcaJoin}
    Then Verify the led state of ${line4} as ${on} on ${phone1}

    Then On ${phone2} press ${softkey} ${programKey1} for 1 times
    Then Verify the led state of ${line1} as ${blink} on ${phone2}
    Then On ${phone2} verify ${line1} icon state as ${bcaLocalHold}
    Then On ${phone1} verify ${line4} icon state as ${bcaLocalHold}
    Then Verify the led state of ${line4} as ${blink} on ${phone1}
    Then On ${phone2} verify display message ${unhold}
    Then On ${phone2} verify display message ${cancel}

    Then On ${phone1} press ${hardKey} ${programKey4} for 1 times
    Then On ${phone1} Wait for 5 seconds
    Then Verify audio path between ${phone1} and ${phone3}
    Then On ${phone1} verify ${line4} icon state as ${bcaActive}
    Then On ${phone2} verify ${line1} icon state as ${bcaJoin}
    Then Disconnect the call from ${phone1}
    And Disconnect the call from ${phone3}
    [Teardown]    Telephony Feature Custom Teardown

751244: TC15: Host holds, admin attempts to join
    [Tags]    Owner:Vikhyat    Reviewer:    SCA    holdUnhold    751244
    [Setup]    Telephony Feature Custom Setup
    &{telephonydetails} =  Create Dictionary    sca_enabled=True
    ${scaExtn} =  using ${bossPortal} on ${phone2} I want to enable SCA using ${telephonydetails}

    &{modifySCAExtension}=    CREATE DICTIONARY    extension=${scaExtn}   backupExtn=${phone3}    allowBridgeConferencing=true
    Then Using ${bossPortal} I want to modify Bridge Call Appearance extension using ${modifySCAExtension}

    &{bcaDetails} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=3    function=Bridge Call Appearance    label=${bca}    target_extension=${scaExtn}    CallStackPosition=1    SecondaryType=Dial Tone
    Given using ${bossPortal} I want to create bca on ${phone1} using ${bcaDetails}
    Then On ${phone1} verify display message ${bca}

    Then I want to make a two party call between ${phone1} and ${phone3} using ${programKey4}
    Then Answer the call on ${phone3} using ${offHook}
    Then I want to make a conference call between ${phone1},${phone3} and ${phone4} using ${consultiveConference}
    Then Conference call audio verify between ${phone1} ${phone3} and ${phone4}
    Then Put the linekey ${line4} of ${phone1} on ${hold}
    Then On ${phone1} verify ${line4} icon state as ${bcaLocalHold}
    Then On ${phone2} press ${softkey} ${programKey1} for 1 times
    Then On ${phone2} verify display on a 4 party conference call
    Then On ${phone1} verify display message ${conferenced3Calls}

    Then Verify the led state of ${line4} as ${blink} on ${phone1}
    Then On ${phone1} verify ${line4} icon state as ${bcaLocalHold}
    Then Verify no audio path from ${phone1} to ${phone2}
    Then Disconnect the call from ${phone2}
    Then Disconnect the call from ${phone3}
    And Disconnect the call from ${phone4}
    [Teardown]    Telephony Feature Custom Teardown

751245: TC16: Participant holds
    [Tags]    Owner:Vikhyat    Reviewer:    SCA    holdUnhold    751245
    [Setup]    Telephony Feature Custom Setup
    [Timeout]    35 minutes
    &{telephonydetails} =  Create Dictionary    sca_enabled=True
    ${scaExtn} =  using ${bossPortal} on ${phone2} I want to enable SCA using ${telephonydetails}

    &{modifySCAExtension}=    CREATE DICTIONARY    extension=${scaExtn}   backupExtn=${phone3}    allowBridgeConferencing=true
    Then Using ${bossPortal} I want to modify Bridge Call Appearance extension using ${modifySCAExtension}

    &{bcaDetails} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=3    function=Bridge Call Appearance    label=${bca}    target_extension=${scaExtn}    CallStackPosition=1    SecondaryType=Dial Tone
    Given using ${bossPortal} I want to create bca on ${phone1} using ${bcaDetails}
    Then On ${phone1} verify display message ${bca}

    Then On ${phone3} dial number ${scaExtn}
    Then on ${phone3} press the softkey ${dial} in DialingState
    Then Answer the call on ${phone2} using ${offHook}
    Then On ${phone1} press ${softkey} ${programKey4} for 1 times
    Then On ${phone1} Wait for 5 seconds
    Then Conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then Put the linekey ${line4} of ${phone1} on ${hold}
    Then On ${phone1} verify ${line4} icon state as ${bcaLocalHold}
    Then Add the ${phone4} in 3 parties conference call on ${phone2}

    Then On ${phone1} verify display message ${conferenced3Calls}
    Then On ${phone2} verify display on a 4 party conference call
    Then On ${phone3} verify display on a 4 party conference call
    Then On ${phone4} verify display on a 4 party conference call

    Then Verify audio path between ${phone4} and ${phone2}
    Then Verify no audio path from ${phone1} to ${phone4}
    Then Put the linekey ${line4} of ${phone1} on ${unhold}
    Then On ${phone1} verify display on a 4 party conference call
    Then On ${phone2} verify display on a 4 party conference call
    Then On ${phone3} verify display on a 4 party conference call
    Then On ${phone4} verify display on a 4 party conference call

    Then Four party Conference call audio verification between ${phone1} ${phone2} ${phone3} and ${phone4}
    Then Disconnect the call from ${phone2}
    Then Disconnect the call from ${phone3}
    And Disconnect the call from ${phone4}

    [Teardown]    Telephony Feature Custom Teardown

751230: Setup
    [Tags]    Owner:Vikhyat    Reviewer:    SCA    conference    lockUnlock    751230
    [Setup]    Telephony Feature Custom Setup
    &{telephonydetails}=  Create Dictionary    sca_enabled=True
    ${scaExtn} =  using ${bossPortal} on ${phone2} I want to enable SCA using ${telephonydetails}

    &{modifySCAExtension}=    CREATE DICTIONARY    extension=${scaExtn}   backupExtn=${phone3}    allowBridgeConferencing=true
    Then Using ${bossPortal} I want to modify Bridge Call Appearance extension using ${modifySCAExtension}


    &{bcaDetails1}=  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=3    function=Bridge Call Appearance    label=${bca}1    target_extension=${scaExtn}    CallStackPosition=1    EnableAutoAnswerWhenRinging=True
    Given using ${bossPortal} I want to create bca on ${phone1} using ${bcaDetails1}
    Then On ${phone1} verify display message ${bca}1

    &{bcaDetails2}=  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=4    function=Bridge Call Appearance    label=${bca}2    target_extension=${scaExtn}    CallStackPosition=2    EnableAutoAnswerWhenRinging=True
    Given using ${bossPortal} I want to create bca on ${phone1} using ${bcaDetails2}
    Then On ${phone1} verify display message ${bca}2

    Then On ${phone3} dial number ${scaExtn}
    Then On ${phone1} Wait for 5 seconds
    Then Verify the led state of ${line4} as ${blink} on ${phone1}
    Then Verify the led state of ${line5} as ${off} on ${phone1}
    Then Answer the call on ${phone2} using ${loudSpeaker}
    Then Verify audio path between ${phone2} and ${phone3}

    Then On ${phone1} verify ${line4} icon state as ${bcaJoin}
    Then On ${phone2} press the softkey ${lock} in AnswerState
    Then On ${phone1} verify ${line4} icon state as ${bcaNoJoin}
    Then On ${phone1} press ${softkey} ${programKey4} for 1 times
    Then On ${phone1} verify display message ${actionNotPermitted}
    Then On ${phone2} press the softkey ${unLock} in AnswerState
    Then On ${phone1} verify ${line4} icon state as ${bcaJoin}
    Then On ${phone1} press ${softkey} ${programKey4} for 1 times
    Then On ${phone1} verify display on a 3 party conference call
    Then On ${phone2} verify display on a 3 party conference call
    Then Conference call audio verify between ${phone1} ${phone2} and ${phone3}

    Then On ${phone4} dial number ${scaExtn}
    Then On ${phone4} press the softkey ${dial} in DialingState
    Then Verify the led state of ${line2} as ${blink} on ${phone2}
    Then Verify the led state of ${line5} as ${blink} on ${phone1}
    Then Answer the call on ${phone1} using ${programKey5}
    Then On ${phone1} press the softkey ${conference} in AnswerState
    Then On ${phone1} press ${softkey} ${programKey4} for 1 times
    Then On ${phone1} Wait for 5 seconds
    Then verify the led state of ${line4} as ${on} on ${phone1}
    Then verify the led state of ${line5} as ${off} on ${phone1}
    Then On ${phone1} verify ${line4} icon state as ${bcaConferenceActive}
    Then On ${phone2} verify ${line1} icon state as ${bcaActive}
#    Then On ${phone3} verify ${line1} icon state as ${callAppearanceConfActive}
#    Then On ${phone4} verify ${line1} icon state as ${callAppearanceConfActive}
    Then Four party conference call audio verification between ${phone1} ${phone2} ${phone3} and ${phone4}
    Then Disconnect the call from ${phone1}
    Then Disconnect the call from ${phone2}
    And Disconnect the call from ${phone3}
    [Teardown]    Telephony Feature Custom Teardown

751236: TC07: Lock - PTP
    [Tags]    Owner:Avishek    Reviewer:Vikhyat    SCA    lockUnlock    751236
    [Setup]    Telephony Feature Custom Setup
    &{telephonydetails} =  Create Dictionary    sca_enabled=True
    ${scaExtn} =   Using ${bossPortal} on ${phone3} I want to enable SCA using ${telephonydetails}

    &{modifySCAExtension}=    CREATE DICTIONARY    extension=${scaExtn}   backupExtn=${phone3}    allowBridgeConferencing=true
    Then Using ${bossPortal} I want to modify Bridge Call Appearance extension using ${modifySCAExtension}

    &{BCAdetails} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=3    function=Bridge Call Appearance    label=BCA2    target_extension=${scaExtn}    RingDelayBeforeAlert=0      CallStackPosition=1    SecondaryType=Dial tone
    Given using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails}
    &{BCAdetails} =  Create Dictionary    user_extension=${phone2}    button_box=0    soft_key=3    function=Bridge Call Appearance    label=BCA1    target_extension=${scaExtn}    RingDelayBeforeAlert=0      CallStackPosition=1    SecondaryType=Dial tone
    Given using ${bossPortal} I want to create bca on ${phone2} using ${BCAdetails}
    Then on ${phone1} verify display message BCA2
    Then on ${phone2} verify display message BCA1

    Then on ${phone4} dial number ${scaExtn}
    Then On ${phone4} press the softkey ${dial} in DialingState
    Then Verify the led state of ${line4} as ${blink} on ${phone2}
    Then Answer the call on ${phone1} using ${programKey4}
    Then verify audio path between ${phone1} and ${phone4}
    Then On ${phone1} verify ${line4} icon state as ${bcaActive}
    Then On ${phone2} verify ${line4} icon state as ${bcaJoin}

    Then On ${phone1} Wait for 10 seconds
    Then On ${phone1} press the softkey ${lock} in AnswerState
    Then On ${phone2} verify ${line4} icon state as ${bcaNoJoin}
    Then On ${phone2} press ${softkey} ${programKey4} for 1 times
    Then On ${phone2} verify display message ${actionNotPermitted}
    Then Disconnect the call from ${phone1}
    And Disconnect the call from ${phone4}
    [Teardown]    Telephony Feature Custom Teardown

751237: TC08: Lock - Mesh conf - admin locks
    [Tags]    Owner:Avishek    Reviewer:Vikhyat    SCA    lockUnlock    751237
	[Setup]    Telephony Feature Custom Setup
    &{telephonydetails} =  Create Dictionary    sca_enabled=True
    ${scaExtn} =   Using ${bossPortal} on ${phone3} I want to enable SCA using ${telephonydetails}

    &{modifySCAExtension}=    CREATE DICTIONARY    extension=${scaExtn}   backupExtn=${phone3}    allowBridgeConferencing=true
    Then Using ${bossPortal} I want to modify Bridge Call Appearance extension using ${modifySCAExtension}

    &{BCAdetails} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=3    function=Bridge Call Appearance    label=BCA1    target_extension=${scaExtn}    RingDelayBeforeAlert=0      CallStackPosition=1    SecondaryType=Dial tone
    Given using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails}
    &{BCAdetails} =  Create Dictionary    user_extension=${phone2}    button_box=0    soft_key=3    function=Bridge Call Appearance    label=BCA2    target_extension=${scaExtn}    RingDelayBeforeAlert=0      CallStackPosition=1    SecondaryType=Dial tone
    Given using ${bossPortal} I want to create bca on ${phone2} using ${BCAdetails}
    Then on ${phone1} verify display message BCA1
    Then on ${phone2} verify display message BCA2

    Then on ${phone4} dial number ${scaExtn}
    Then On ${phone4} press the softkey ${dial} in DialingState
    Then Verify the led state of ${line4} as ${blink} on ${phone1}
    Then Verify the led state of ${line4} as ${blink} on ${phone2}
    Then Answer the call on ${phone1} using ${programKey4}
    Then verify audio path between ${phone1} and ${phone4}
    Then On ${phone1} verify ${line4} icon state as ${bcaActive}
    Then On ${phone2} verify ${line4} icon state as ${bcaJoin}
    Then On ${phone1} press the softkey ${lock} in AnswerState
    Then On ${phone2} verify ${line4} icon state as ${bcaNoJoin}
    Then On ${phone3} verify ${line1} icon state as ${bcaJoin}

    Then On ${phone3} press ${softkey} ${programKey1} for 1 times
    Then On ${phone3} Wait for 5 seconds
    Then On ${phone1} verify ${line4} icon state as ${bcaConferenceActive}
    Then On ${phone3} verify ${line1} icon state as ${bcaConferenceActive}
    Then On ${phone1} verify display on a 3 party conference call
    Then On ${phone3} verify display on a 3 party conference call
    Then On ${phone4} verify display on a 3 party conference call
    Then Conference call audio verify between ${phone1} ${phone4} and ${phone3}

    Then On ${phone2} press ${softkey} ${programKey4} for 1 times
    Then On ${phone2} verify display message Action not permitted
    Then Disconnect the call from ${phone2}
    And Disconnect the call from ${phone4}
    [Teardown]    Telephony Feature Custom Teardown

751238: TC09: Lock - Mesh conf - Boss locks
    [Tags]    Owner:Avishek    Reviewer:Vikhyat    SCA    lockUnlock    751238
	[Setup]    Telephony Feature Custom Setup
    &{telephonydetails} =  Create Dictionary    sca_enabled=True
    ${scaExtn} =   Using ${bossPortal} on ${phone3} I want to enable SCA using ${telephonydetails}

    &{modifySCAExtension}=    CREATE DICTIONARY    extension=${scaExtn}   backupExtn=${phone3}    allowBridgeConferencing=true
    Then Using ${bossPortal} I want to modify Bridge Call Appearance extension using ${modifySCAExtension}

    &{BCAdetails} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=3    function=Bridge Call Appearance    label=BCA1    target_extension=${scaExtn}    RingDelayBeforeAlert=0      CallStackPosition=1    SecondaryType=Dial tone
    Given using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails}
    &{BCAdetails} =  Create Dictionary    user_extension=${phone2}    button_box=0    soft_key=3    function=Bridge Call Appearance    label=BCA2    target_extension=${scaExtn}    RingDelayBeforeAlert=0      CallStackPosition=1    SecondaryType=Dial tone
    Given using ${bossPortal} I want to create bca on ${phone2} using ${BCAdetails}
    Then on ${phone1} verify display message BCA1
    Then on ${phone2} verify display message BCA2

    Then on ${phone4} dial number ${scaExtn}
    Then On ${phone4} press the softkey ${dial} in DialingState
    Then Verify the led state of ${line4} as ${blink} on ${phone1}
    Then Answer the call on ${phone1} using ${programKey4}
    Then On ${phone1} verify ${line4} icon state as ${bcaActive}
    Then On ${phone2} verify ${line4} icon state as ${bcaJoin}
    Then On ${phone3} press ${softkey} ${programKey1} for 1 times
    Then On ${phone3} Wait for 5 seconds
    Then On ${phone1} verify ${line4} icon state as ${bcaConferenceActive}
    Then On ${phone3} verify ${line1} icon state as ${bcaConferenceActive}
    Then On ${phone1} verify display on a 3 party conference call
    Then On ${phone3} verify display on a 3 party conference call
    Then On ${phone4} verify display on a 3 party conference call

    Then On ${phone3} press the softkey ${lock} in ConferenceCallState
    Then On ${phone2} verify ${line4} icon state as ${bcaNoJoin}
    Then On ${phone2} press ${softkey} ${programKey4} for 1 times
    Then On ${phone2} verify display message ${actionNotPermitted}

    Then On ${phone1} press the softkey ${unlock} in ConferenceCallState
    Then On ${phone2} verify ${line4} icon state as ${bcaJoin}
    Then On ${phone2} press ${softkey} ${programKey4} for 1 times
    Then On ${phone2} Wait for 5 seconds
    Then On ${phone2} verify ${line4} icon state as ${bcaConferenceActive}
    Then On ${phone1} verify display on a 4 party conference call
    Then On ${phone2} verify display on a 4 party conference call
    Then On ${phone3} verify display on a 4 party conference call
    Then On ${phone4} verify display on a 4 party conference call
    Then Four party conference call audio verification between ${phone1} ${phone2} ${phone3} and ${phone4}
    Then Disconnect the call from ${phone1}
    Then Disconnect the call from ${phone2}
    And Disconnect the call from ${phone3}
    [Teardown]    Telephony Feature Custom Teardown

760833: Park/Unpark for BCA
    [Tags]    Owner:Gaurav    Reviewer:Vikhyat    BCA    parkUnpark    760833
    [Setup]    BCA Custom Setup
    &{createBCAExtension} =  CREATE DICTIONARY    name=760833   backupExtn=${phone3}    switch=2    callStackDepth=2    forwardAfter=2    callStackFull=${EMPTY}   noAnswer=${EMPTY}    outboundCallerID=${EMPTY}    allowBridgeConferencing=true   defaultPrivacySettings=0
    ${bcaExtn}=    using ${bossPortal} I want to create Bridge Call Appearance extension using ${createBCAExtension}

    &{BCAdetails} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=3    function=Bridge Call Appearance    label=BCA    target_extension=${bcaExtn}    RingDelayBeforeAlert=0      CallStackPosition=1    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=Dial tone
    Given using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails}
    Then on ${phone1} verify display message BCA

    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then Answer the call on ${phone1} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then On ${phone1} press the softkey ${park} in AnswerState
    Then On ${phone1} press ${softkey} ${programKey4} for 1 times
    Then On ${phone1} Wait for 5 seconds
    Then On ${phone1} verify ${line4} icon state as ${bcaLocalHold}
    Then on ${phone1} press ${softKey} ${bottomKey2} for 1 times
    Then On ${phone1} press ${softkey} ${programKey4} for 1 times
    Then On ${phone1} Wait for 5 seconds
    Then Verify audio path between ${phone1} and ${phone2}
    Then Disconnect the call from ${phone2}
    [Teardown]    BCA Custom Teardown

856364: DTP-53394 - Drop Participants in Conf
    [Tags]    Owner:Gaurav    Reviewer:    BCA
    [Setup]    Telephony Feature Custom Setup
    &{telephonydetails} =  Create Dictionary    sca_enabled=True
    ${scaExtn} =  using ${bossPortal} on ${phone2} I want to enable SCA using ${telephonydetails}
    &{BCAdetails} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=3    function=Bridge Call Appearance    label=BCA1    target_extension=${scaExtn}       CallStackPosition=1     allowBridgeConferencing=true
    Given using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails}
    Then I want to make a two party call between ${phone1} and ${phone3} using ${programKey4}
    Then answer the call on ${phone3} using ${offHook}
    Then I want to make a conference call between ${phone1},${phone3} and ${phone4} using ${directConference}
    Then Conference call audio verify between ${phone1} ${phone3} and ${phone4}
    Then press hardkey as ${scrollDown} on ${phone1}
    Then on ${phone1} Press ${softKey} ${bottomKey1} for 1 times
    Then Verify audio path between ${phone1} and ${phone3}
    Then On ${phone4} verify the softkeys in ${idleState}
    Then disconnect the call from ${phone1}

    Then I want to make a two party call between ${phone1} and ${phone3} using ${programKey4}
    Then answer the call on ${phone3} using ${offHook}
    Then I want to make a conference call between ${phone1},${phone3} and ${phone4} using ${directConference}
    Then Conference call audio verify between ${phone1} ${phone3} and ${phone4}
    Then on ${phone1} Press ${softKey} ${bottomKey1} for 1 times
    Then Verify audio path between ${phone1} and ${phone4}
    Then On ${phone3} verify the softkeys in ${idleState}
    And disconnect the call from ${phone1}
    [Teardown]    Telephony Feature Custom Teardown

751240: TC11: Blind Conference inbound call
    [Tags]    Owner:Ram    Reviewer:     SCA      notApplicableFor6910     751240
    [Setup]    Telephony Feature Custom Setup
    &{telephonydetails} =  Create Dictionary    sca_enabled=True
    ${scaExtn} =  using ${bossPortal} on ${phone1} I want to enable SCA using ${telephonydetails}
    &{modifySCAExtension}=    CREATE DICTIONARY    extension=${scaExtn}   backupExtn=${phone3}    allowBridgeConferencing=true
    Given Using ${bossPortal} I want to modify Bridge Call Appearance extension using ${modifySCAExtension}
    &{BCAdetails1} =  Create Dictionary    user_extension=${phone2}    button_box=0    soft_key=2    function=Bridge Call Appearance    label=BCA1    target_extension=${scaExtn}       CallStackPosition=1     allowBridgeConferencing=true
    &{BCAdetails2} =  Create Dictionary    user_extension=${phone2}    button_box=0    soft_key=3    function=Bridge Call Appearance    label=BCA2    target_extension=${scaExtn}       CallStackPosition=2     allowBridgeConferencing=true
    Then using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails1}
    Then using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails2}
    &{hotlines}    create dictionary    ConnectedCallFunctionID=intercom    account_name=Automation    part_name=SC1    button_box=0
    Then using ${bossPortal} I program ${hotline} on ${phone1} using ${hotlines} and extension of ${phone2} and softkey position 4 with ExtensionValue
    Then using ${bossPortal} I program ${hotline} on ${phone2} using ${hotlines} and extension of ${phone1} and softkey position 4 with ExtensionValue
    Then on ${phone3} dial number ${scaExtn}
    Then on ${phone3} press ${softKey} ${bottomKey1} for 1 times
    Then I want to press line key ${programKey1} on phone ${phone1}
    Then on ${phone4} dial number ${scaExtn}
    Then on ${phone4} press ${softKey} ${bottomKey1} for 1 times
    Then I want to press line key ${programKey4} on phone ${phone2}
    Then On ${phone2} Wait for 3 seconds
    Then I want to press line key ${programKey5} on phone ${phone2}
    Then On ${phone2} Wait for 5 seconds
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then On ${phone1} Wait for 2 seconds
    Then I want to press line key ${programKey4} on phone ${phone2}
    Then on ${phone2} press ${softKey} ${bottomKey2} for 1 times
    Then I want to press line key ${programKey3} on phone ${phone2}
    Then on ${phone2} verify display message ${leave}
    Then verify the led state of ${line4} as ${off} on ${phone2}
    Then I want to verify on ${phone1} negative display message ${leave}
    Then disconnect the call from ${phone2}
    And disconnect the call from ${phone3}
    [Teardown]    Telephony Feature Custom Teardown

#751239: TC10: Toggle Lock/Unlock prog key
#    [Tags]    Owner:Vikhyat    Reviewer:    lockUnlock    SCA    751239
#    [Setup]    Telephony Feature Custom Setup
#    # Setup:
#          #Configure Lock unlock prog key for Boss and admin2
#          #Allow conferencing option is enabled
#          #
#          #A calls Boss
#          #Admin Answers NOTE: Lock unlock prog key icon is orange on Admin1 (LED is lit if admin is 6930)
#          #Admin hits lock
#
#
#
#    [Teardown]    Telephony Feature Custom Teardown
