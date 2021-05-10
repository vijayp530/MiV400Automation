*** Settings ***
Resource   ../RobotKeywords/Setup_And_Teardown.robot
Resource   ../RobotKeywords/Boss_API_Keywords.robot

Library    ../lib/MyListner.py

Test Timeout     25 minutes
Suite Setup      RUN KEYWORDS    Phones Initialization    Get Dut Details
Test Setup       Check Phone Connection
Test Teardown    Generic Test Teardown
Suite Teardown   RUN KEYWORD AND IGNORE ERROR    RUN KEYWORDS    Check Phone Connection    Generic Test Teardown

*** Test Cases ***

759997: TC018-Hold, Unhold, Mute, unmute
    [Tags]    Owner:Ram    Reviewer:    Hold/Mute    notApplicableForMiCloud    #759997     # one way audio path
    [Timeout]    35 minutes
    &{MOHFeatures}=  Create Dictionary    option=1    fileName=MOH_150
    Given using ${bossPortal} I want to enable MOH features using ${MOHFeatures}
    Then i want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then answer the call on ${phone2} using ${offHook}
    Then verify audio path between ${phone1} and ${phone2}
    Then press hardkey as ${mute} on ${phone1}
    Then verify no audio path from ${phone1} to ${phone2}
    Then verify one way audio from ${phone2} to ${phone1}
    Then put the linekey ${line1} of ${phone1} on ${hold}
    Then verify moh audio on ${phone2} for 150 frequency
    Then put the linekey ${line1} of ${phone1} on ${unhold}
    Then verify no moh audio on ${phone2}
    Then press hardkey as ${mute} on ${phone1}
    Then verify audio path between ${phone1} and ${phone2}
    And disconnect the call from ${phone2}
    [Teardown]    Disable MOH features Teardown

759998: TC019-Make inbound/outbound call
    [Tags]    Owner:Ram    Reviewer:    makeCall     #759998    6910
    Given I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then answer the call on ${phone2} using ${offHook}
    Then verify audio path between ${phone1} and ${phone2}
    Then I want to make a two party call between ${phone3} and ${phone1} using ${offHook}
    Then answer the call on ${phone1} using ${line2}
    Then verify audio path between ${phone1} and ${phone3}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then verify no audio path from ${phone1} to ${phone2}
    Then verify no audio path from ${phone2} to ${phone1}
    Then disconnect the call from ${phone2}
    And disconnect the call from ${phone3}

760000: TC021-Check call history and VM messages
    [Tags]    Owner:Ram    Reviewer:    CallHistory/VM    notApplicableFor6910    760000
    Given I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then Disconnect the call from ${phone1}
    Then press hardkey as ${callersList} on ${phone1}
    Then on ${phone1} verify display message ${all}
    Then on ${phone1} verify display message ${missed}
    Then on ${phone1} verify display message ${outgoing}
    Then on ${phone1} verify display message ${received}
    Then press hardkey as ${goodBye} on ${phone1}
    Then login into voicemailbox for ${phone1} using ${voicemailpassword}
    Then on ${phone1} verify display message ${voicemailDisplay['inbox']}
    Then on ${phone1} verify display message ${voicemailDisplay['saved']}
    Then on ${phone1} verify display message ${voicemailDisplay['deleted']}
    And press hardkey as ${goodBye} on ${phone1}

760028: TC049-Merge two P2P calls into a Mesh call
    [Tags]    Owner:Ram    Reviewer:     MeshCall    notApplicableFor6910
    Given I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then answer the call on ${phone2} using ${offHook}
    Then verify audio path between ${phone1} and ${phone2}
    Then I want to make a two party call between ${phone3} and ${phone1} using ${offHook}
    Then answer the call on ${phone1} using ${line2}
    Then verify audio path between ${phone1} and ${phone3}
    Then on ${phone1} press the softkey ${merge} in AnswerState
    Then Conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then verify the led state of ${line2} as ${off} on ${phone1}
    Then disconnect the call from ${phone2}
    And disconnect the call from ${phone3}

760029: TC050-Merge 3 P2P calls into a Make Me Call
    [Tags]    Owner:Ram    Reviewer:     MakeMe    notApplicableFor6910
    [Timeout]    35 minutes
    Given I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then answer the call on ${phone2} using ${offHook}
    Then verify audio path between ${phone1} and ${phone2}
    Then I want to make a two party call between ${phone3} and ${phone1} using ${offHook}
    Then answer the call on ${phone1} using ${line2}
    Then verify audio path between ${phone1} and ${phone3}
    Then on ${phone1} press the softkey ${merge} in AnswerState
    Then Conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then verify the led state of ${line2} as ${off} on ${phone1}
    Then I want to make a two party call between ${phone4} and ${phone1} using ${offHook}
    Then answer the call on ${phone1} using ${line2}
    Then verify audio path between ${phone1} and ${phone4}
    Then on ${phone1} press the softkey ${merge} in AnswerState
    Then Four party Conference call audio verification between ${phone1} ${phone2} ${phone3} and ${phone4}
    Then verify the led state of ${line2} as ${off} on ${phone1}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}
    And disconnect the call from ${phone4}

760030: TC051-Silent Coach a caller
    [Tags]    Owner:Ram    Reviewer:     silentCoach    notApplicableFor6910    760030
    &{COSDetails} =  Create Dictionary    Name=${fullyFeatured}   AllowSilentMonitorInitiation=True    SilentMonitorAccept=1
    Given using ${bossPortal} I want to change telephony features values using ${COSDetails}
    Then using ${bossPortal} I program ${silentCoach} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with ExtensionValue
    Then On ${phone1} verify display message ${silentCoach}
    Then I want to make a two party call between ${phone2} and ${phone3} using ${offHook}
    Then Answer the call on ${phone3} using ${offHook}
    Then On ${phone2} verify ${line1} icon state as ${callAppearanceActive}
    Then On ${phone3} verify ${line1} icon state as ${callAppearanceActive}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} wait for 10 seconds
    Then Verify audio path between ${phone1} and ${phone2}
    Then Verify one way audio from ${phone3} to ${phone1}
    Then Verify no audio path from ${phone1} to ${phone3}
    Then On ${phone1} verify display message ${silentCoach}
    Then On ${phone1} verify display message ${drop}
    Then On ${phone1} verify display message ${monitor}
    Then On ${phone1} verify ${line1} icon state as ${callAppearanceConfActive}      # ask Support
    Then On ${phone2} verify ${line1} icon state as ${callAppearanceConfActive}      # ask Support
    Then On ${phone3} verify ${line1} icon state as ${callAppearanceActive}
    Then disconnect the call from ${phone2}
    And disconnect the call from ${phone3}
    [Teardown]    RUN KEYWORDS    Default Call Appearance    CoS Features Custom Teardown

760031: TC052-Silent Monitor a Caller
    [Tags]    Owner:Ram    Reviewer:     silentMonitor      notApplicableFor6910
    &{COSDetails} =  Create Dictionary    Name=${fullyFeatured}   AllowSilentMonitorInitiation=True    SilentMonitorAccept=1
    Given using ${bossPortal} I want to change telephony features values using ${COSDetails}
    Then using ${bossPortal} I program ${silentMonitor} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with ExtensionValue
    Then On ${phone1} verify display message ${displayMessage['silentMonitor']}
    Then I want to make a two party call between ${phone2} and ${phone3} using ${offHook}
    Then Answer the call on ${phone3} using ${offHook}
    Then On ${phone2} verify ${line1} icon state as ${callAppearanceActive}
    Then On ${phone3} verify ${line1} icon state as ${callAppearanceActive}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} wait for 10 seconds
    Then Verify no audio path from ${phone1} to ${phone2}
    Then Verify one way audio from ${phone3} to ${phone1}
    Then Verify no audio path from ${phone1} to ${phone3}
    Then On ${phone1} verify display message ${displayMessage['silentMonitor']}
    Then On ${phone1} verify display message ${drop}
    Then On ${phone1} verify ${line1} icon state as ${callAppearanceConfActive}    # ask Support
    Then On ${phone3} verify ${line1} icon state as ${callAppearanceActive}
    Then disconnect the call from ${phone2}
    And disconnect the call from ${phone3}
    [Teardown]    RUN KEYWORDS    Default Call Appearance    CoS Features Custom Teardown

760011: TC032-Place outbound call with collected digits when ...
    [Tags]    Owner:Ram    Reviewer:        makeCall     6910    760011
    Given on ${phone1} enter number ${phone2}
    Then On ${phone1} verify display message ${phone2}
    Then On ${phone1} Wait for 5 seconds
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then answer the call on ${phone2} using ${offHook}
    And disconnect the call from ${phone2}

760012: TC033-Press dial in call history
    [Tags]    Owner:Ram    Reviewer:Vikhyat    CallHistory     notApplicableFor6910
    Given I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then answer the call on ${phone2} using ${offHook}
    Then disconnect the call from ${phone2}
    Then Press the call history button on ${phone1} and folder ${all} and ${details}
    Then On ${phone1} verify display message ${phone2}
    Then on ${phone1} press ${softkey} ${bottomKey1} for 1 times
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then answer the call on ${phone2} using ${offHook}
    And disconnect the call from ${phone2}

760001: TC022-Test Directory on phone
    [Tags]    Owner:Aman    Reviewer:Ram    directory    notApplicableFor6910    760001
    Given Press hardkey as ${directory} on ${phone1}
    Then on ${phone1} verify display message ${directory}
    Then on ${phone1} press ${hardKey} ${scrollRight} for 1 times
    Then on ${phone1} press ${hardKey} ${scrollDown} for 2 times
    Then Verify ${byFirst} naming directory format on ${phone1}
    And Press hardkey as ${goodBye} on ${phone1}

    Given On ${phone1} verify directory with ${default} of ${phone1}
    Then On ${phone1} press the key ${close} in state ${directory}
    Then Press hardkey as ${scrollLeft} on ${phone1}
    Then On ${phone1} press the key ${byLast} in state ${directory}
    Then Press hardkey as ${scrollRight} on ${phone1}
    Then On ${phone1} press ${hardKey} ${scrollDown} for 12 times
    Then Verify ${byLast} naming directory format on ${phone1}
    And Press hardkey as ${goodBye} on ${phone1}
    [Teardown]    Default Directory Settings

760032: TC053-Silent Coach a caller but hang-up before established.
    [Tags]    Owner:Aman    Reviewer:    silentMonitor    notApplicableFor6910
    &{COSDetails} =  Create Dictionary    Name=${fullyFeatured}   AllowSilentMonitorInitiation=True    SilentMonitorAccept=1
    Given using ${bossPortal} I want to change telephony features values using ${COSDetails}
    Then using ${bossPortal} I program ${silentMonitor} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 0 with ExtensionValue
    Then On ${phone1} verify display message ${displayMessage['silentMonitor']}
    Then I want to make a two party call between ${phone2} and ${phone3} using ${offHook}
    Then answer the call on ${phone3} using ${offHook}
    Then Verify audio path between ${phone2} and ${phone3}
    Then On ${phone2} verify ${line1} icon state as ${callAppearanceActive}
    Then On ${phone3} verify ${line1} icon state as ${callAppearanceActive}
    Then I want to press line key ${programKey1} on phone ${phone1}
    Then Press hardkey as ${goodBye} on ${phone1}
    Then Verify audio path between ${phone2} and ${phone3}
    Then I want to verify on ${phone2} negative display message ${silentCoach}
    Then on ${phone1} verify the softkeys in ${idle}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then disconnect the call from ${phone2}
    [Teardown]    RUN KEYWORDS    Default Call Appearance    CoS Features Custom Teardown

760033: TC054-Cancel an outgoing call (Missed call count should not increase)
    [Tags]    Owner:Aman    Reviewer:    call    6910    760033
    Given on ${phone1} enter number ${phone2}
    Then Press hardkey as ${goodBye} on ${phone1}
    Then on ${phone1} verify the softkeys in ${idle}
    Then on ${phone2} verify the softkeys in ${idle}
	And i want to verify on ${phone2} negative display message Missed Calls

884524: TC055 - DTP-55048 - Consult Xfer to VM- Drop - unhold 1st call leg
    [Tags]    Owner:Aman    Reviewer:Vikhyat    transfer   notApplicableFor6910
    Given I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then answer the call on ${phone2} using ${offHook}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then on ${phone1} press the softkey ${transfer} in AnswerState
    Then on ${phone1} enter number ${phone3}
    Then on ${phone1} press the softkey ${consult} in TransferState
    Then on ${phone1} wait for 5 seconds
    Then on ${phone3} press the softkey ${toVm} in RingingState
    Then On ${phone1} verify display message ${displayVoiceMail}
    Then on ${phone1} press the softkey ${drop} in TransferState
    Then on ${phone1} press the softkey ${transfer} in AnswerState
    Then on ${phone1} enter number ${phone3}
    Then on ${phone1} press the softkey ${consult} in TransferState
    Then on ${phone1} wait for 5 seconds
    Then on ${phone3} press the softkey ${toVm} in RingingState
    Then On ${phone1} verify display message ${displayVoiceMail}
    Then on ${phone1} press the softkey ${drop} in TransferState
    Then on ${phone1} press the softkey ${pickup} in AnswerState
    Then Verify audio path between ${phone1} and ${phone2}
    And disconnect the call from ${phone2}

760025: TC046-Xmon operation when user has a P2P Call
    [Tags]    Owner:Aman    Reviewer:    XMON    notApplicableFor6910
    &{extensionDetails1}    Create Dictionary    ring_delay=none   show_caller_id=never    no_connected=unused    with_connected=unused    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails1} and extension of ${phone2} and softkey position 3 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['monitorExtn']}
    &{extensionDetails2}    Create Dictionary    ring_delay=none   show_caller_id=never    no_connected=unused    with_connected=unused    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails2} and extension of ${phone3} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['monitorExtn']}
    Then I want to make a two party call between ${phone4} and ${phone2} using ${offHook}
    Then On ${phone1} verify the led state of ${line4} as ${blink} and led color as ${red}
    Then On ${phone1} verify ${line4} icon state as ${xmonRinging}
    Then answer the call on ${phone2} using ${offHook}
    Then verify the led state of ${line4} as ${on} on ${phone1}
    Then verify the led state of ${line5} as ${off} on ${phone1}
    And disconnect the call from ${phone2}
    [Teardown]    RUN KEYWORDS    Default Call Appearance    Generic Test Teardown

760003: TC024-Test access via Putty works
    [Tags]    Owner:Aman    Reviewer:    putty
    Given I want to ${open} ${phone1} ip using connection type SSH under putty

759985: TC006-Access user's History view (All, Missed, Outgoing, Received)
    [Tags]    Owner:Vikhyat    Reviewer:Anish    callHistory    notApplicableFor6910    759985
    Given I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then Answer the call on ${phone2} using ${offHook}
    Then Disconnect the call from ${phone1}

    Then I want to make a two party call between ${phone2} and ${phone1} using ${offHook}
    Then Verify ringing state on ${phone2} and ${phone1}
    Then Disconnect the call from ${phone2}

    Then I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then Verify ringing state on ${phone1} and ${phone2}
    Then Answer the call on ${phone2} using ${offHook}
    Then Disconnect the call from ${phone2}

    Then Press the call history button on ${phone1} and folder ${all} and ${quit}
    Then Press the call history button on ${phone1} and folder ${missed} and ${quit}
    Then Press the call history button on ${phone1} and folder ${outgoing} and ${quit}
    And Press the call history button on ${phone1} and folder ${received} and ${quit}

760019: TC040-Place a Make Me Call with 4 users
    [Tags]    Owner:Vikhyat    Reviewer:Anish    conference    760019
    [Timeout]  35 minutes
    Given I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then Answer the call on ${phone2} using ${offHook}
    Then Verify audio path between ${phone1} and ${phone2}
    Then On ${phone1} press the softkey ${conference} in AnswerState
    Then On ${phone1} enter number ${phone3}
    Then On ${phone1} press the softkey ${dial} in DialingState
    Then Answer the call on ${phone3} using ${offHook}
    Then Verify audio path between ${phone1} and ${phone3}
    Then On ${phone1} press the softkey ${conference} in AnswerState
    Then Add the ${phone4} in 3 parties conference call on ${phone1}
    Then On ${phone1} verify display message ${conferenced3Calls}
    Then Four party Conference call audio verification between ${phone1} ${phone2} ${phone3} and ${phone4}
    Then Disconnect the call from ${phone2}
    Then Disconnect the call from ${phone3}
    And Disconnect the call from ${phone4}

760020: TC041-Place a 3 way mesh call - Hold and Unhold
    [Tags]    Owner:Vikhyat    Revewer:Anish    conference
    Given I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then Answer the call on ${phone2} using ${offHook}
    Then I want to make a conference call between ${phone1},${phone2} and ${phone3} using ${directConference}
    Then Conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then Put the linekey ${line1} of ${phone1} on ${hold}
    Then On ${phone1} verify ${line1} icon state as ${callAppearanceLocalHold}
    Then Verify no audio path from ${phone1} to ${phone2}
    Then Verify no audio path from ${phone1} to ${phone3}
    Then Verify audio path between ${phone3} and ${phone2}
    Then Put the linekey ${line1} of ${phone1} on ${unhold}
    Then Conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then Disconnect the call from ${phone2}
    And Disconnect the call from ${phone3}

760022: TC043-Hang up a Make Me call with 4 or more participants
    [Tags]    Owner:Vikhyat    Reviewer:Anish    conference
    Given I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then Answer the call on ${phone2} using ${offHook}
    Then I want to make a conference call between ${phone1},${phone2} and ${phone3} using ${consultiveConference}
    Then Add the ${phone4} in 3 parties conference call on ${phone1}
    Then Four party Conference call audio verification between ${phone1} ${phone2} ${phone3} and ${phone4}
    Then I want to verify on ${phone1} negative display message ${phone2}
    Then On ${phone1} verify display message ${conferenced3Calls}
    Then On ${phone4} press the softkey ${drop} in ConferenceCallState
    Then On ${phone2} press the softkey ${drop} in ConferenceCallState
    Then On ${phone3} press the softkey ${drop} in ConferenceCallState

    Then On ${phone1} verify the softkeys in ${idleState}
    Then On ${phone2} verify the softkeys in ${idleState}
    Then On ${phone3} verify the softkeys in ${idleState}
    And On ${phone4} verify the softkeys in ${idleState}

759988: TC009-Place call from filtered Directory list
    [Tags]    Owner:Vikhyat    Reviewer:    directory    notApplicableFor6910    759988     # need to check create user method
    [Setup]    RUN KEYWORDS  Check Phone Connection    Create user Setup
    &{telephonyDetails1}=    CREATE DICTIONARY    FirstName=First    LastName=Last    AllowTelephonyPresence=True
    ${extn1}=   using ${bossPortal} I want to create user using ${telephonyDetails1}

    &{telephonyDetails2}=    CREATE DICTIONARY    FirstName=Lane    LastName=Finney    AllowTelephonyPresence=True
    ${extn2}=   using ${bossPortal} I want to create user using ${telephonyDetails2}

    &{telephonyDetails3}=    CREATE DICTIONARY    FirstName=Name First    LastName=Name Last    AllowTelephonyPresence=True
    ${extn3}=   using ${bossPortal} I want to create user using ${telephonyDetails3}

    Given Press hardkey as ${directory} on ${phone1}
    Then On ${phone1} dial number 34#52
    Then On ${phone1} verify display message ${extn1}
    Then On ${phone1} verify display message First Last

    Then On ${phone1} verify display message ${extn2}
    Then On ${phone1} verify display message Lane Finney

    Then On ${phone1} verify display message ${extn3}
    Then On ${phone1} verify display message Name First Name Last

    Then I want to verify on ${phone1} negative display message ${phone2}

    Then using ${bossPortal} I want to delete extension ${extn1}
    Then using ${bossPortal} I want to delete extension ${extn2}
    And using ${bossPortal} I want to delete extension ${extn3}
    [Teardown]    Create User Teardown

760005: TC026-Verify inbound and outbound caller ID
    [Tags]    Owner:Avishek    760005
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudSpeaker}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then disconnect the call from ${phone2}
    Then I want to make a two party call between ${phone1} and ${phone3} using ${loudSpeaker}
    Then answer the call on ${phone3} using ${loudSpeaker}
    Then Verify the Caller id on ${phone3} and ${phone1} display
    And disconnect the call from ${phone3}

760006: TC027-Incoming Call Answer through soft key
    [Tags]    Owner:Avishek
    Given I want to make a two party call between ${phone2} and ${phone1} using ${loudSpeaker}
    Then answer the call on ${phone1} using SoftKey
    Then verify audio path between ${phone1} and ${phone2}
    And disconnect the call from ${phone1}

760013: TC034-Caller ID is displayed when ring back ...    # why does this no applicable for 6910
    [Tags]    Owner:Abhishekkhanchi    Reviewer:
    Given on ${phone1} enter number ${phone2}
    Then press hardkey as ${offHook} on ${phone1}
    Then Verify extension ${number} of ${phone1} on ${phone2}
    And Press hardkey as ${goodBye} on ${phone1}

760015: TC036-Focus points to most recent call
    [Tags]    Owner:Abhishekkhanchi    Reviewer:     notApplicableFor6910
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then Verify the led state of ${line1} as blink on ${phone2}
    Then verify the caller id on ${phone1} and ${phone2} display
    Then on ${phone1} Wait for 5 seconds
    Then Disconnect the call from ${phone1}
    Then Press the call history button on ${phone2} and folder ${missed} and ${nothing}
    Then Verify extension ${number} of ${phone1} on ${phone2}
    Then Press hardkey as ${goodBye} on ${phone2}
    Then Press the call history button on ${phone1} and folder ${outgoing} and ${nothing}
    Then Verify extension ${number} of ${phone2} on ${phone1}
    Then Press hardkey as ${goodBye} on ${phone1}
    Then I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then Verify the led state of Line1 as blink on ${phone2}
    Then verify the caller id on ${phone1} and ${phone2} display
    Then Answer the call on ${phone2} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Disconnect the call from ${phone2}
    Then Press the call history button on ${phone2} and folder ${received} and ${nothing}
    Then Verify extension ${number} of ${phone1} on ${phone2}
    And Press hardkey as ${goodBye} on ${phone1}

760016: TC037-Press programmed Speed Dial button to add ...
    [Tags]    Owner:Abhishekkhanchi    Reviewer:AvishekRanjan    notApplicableFor6910    # line 5 should be active after answering the call
    Given using ${bossPortal} I program ${dialNumber} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['dialNumber']}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then Answer the call on ${phone2} using ${offHook}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then verify the led state of ${line5} as ${on} on ${phone1}           # can check Busy Dial Number icon here
    Then Verify audio path between ${phone2} and ${phone1}
    And Disconnect the call from ${phone2}
    [Teardown]    RUN KEYWORDS    Default Call Appearance    Generic Test Teardown

760017: TC038-PARK a Call
    [Tags]    Owner:Abhishekkhanchi    Reviewer:     notApplicableFor6910    760017
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then Verify the led state of ${line1} as blink on ${phone2}
    Then Answer the call on ${phone2} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then I want to Park the call from ${phone1} on ${phone3} using ${default} and ${park}
    Then on ${phone1} Wait for 5 seconds
    Then Verify the led state of ${line1} as ${blink} on ${phone3}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}

    Then I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then Verify the led state of ${line1} as ${blink} on ${phone2}
    Then Answer the call on ${phone2} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then I want to Park the call from ${phone1} on ${phone3} using ${default} and ${park}
    Then Verify the led state of ${line1} as ${blink} on ${phone3}
    Then on ${phone3} wait for 60 seconds
    Then Verify the led state of ${line1} as ${blink} on ${phone1}
    Then Answer the call on ${phone1} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then On ${phone3} verify the softkeys in ${idleState}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone1}

    &{MOHFeatures}    CREATE DICTIONARY    option=1    fileName=MOH_50
    Then using ${bossPortal} I want to enable MOH features using ${MOHFeatures}
    Then using ${bossPortal} I want to modify usergroups MOH for ${executives} with filename MOH_200
    Then I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then Verify the led state of Line1 as blink on ${phone2}
    Then Answer the call on ${phone2} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then I want to Park the call from ${phone1} on ${phone3} using ${default} and ${Park}
    Then on ${phone1} Wait for 5 seconds
    Then Verify the led state of Line1 as blink on ${phone3}
    Then verify MOH audio on ${phone2} for 200 frequency
    Then Put the linekey ${line1} of ${phone3} on ${unhold}
    Then Verify audio path between ${phone2} and ${phone3}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}
    And disconnect the call from ${phone1}
    [Teardown]    Disable MOH features Teardown

760018: TC039-Unpark a Held Call
    [Tags]    Owner:Abhishekkhanchi    Reviewer:     notApplicableFor6910
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then Verify the led state of ${line1} as ${blink} on ${phone2}
    Then Answer the call on ${phone2} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then I want to Park the call from ${phone1} on ${phone3} using ${default} and ${Park}
    Then On ${phone1} Wait for 5 seconds
    Then Verify the led state of ${line1} as ${blink} on ${phone3}
    Then I want to unPark the call from ${phone3} on ${phone1} using ${default} and ${dial}
    Then On ${phone1} Wait for 5 seconds
    Then Verify audio path between ${phone2} and ${phone1}
    Then Disconnect the call from ${phone4}
    And Disconnect the call from ${phone2}

759993: TC014-Receive Blind Transfer
    [Tags]     Owner:Anish     Reviewer:Aman     blindTransfer    759993
    Given I want to make a two party call between ${phone3} and ${phone2} using ${offHook}
    Then On ${phone2} verify ${line1} icon state as ${callAppearanceIncoming}
    Then Answer the call on ${phone2} using ${offHook}
    Then Verify audio path between ${phone3} and ${phone2}
    Then On ${phone3} verify ${line1} icon state as ${callAppearanceActive}
    Then On ${phone2} verify ${line1} icon state as ${callAppearanceActive}
    Then on ${phone3} press the softkey ${transfer} in AnswerState
    Then On ${phone2} verify ${line1} icon state as ${callAppearanceRemoteHold}
    Then Verify the led state of ${line1} as ${blink} on ${phone3}
    Then on ${phone3} enter number ${phone1}
    Then on ${phone3} press the softkey ${transfer} in DialingState
    Then On ${phone3} verify display message ${callTransferred}
    Then Verify the Caller id on ${phone2} and ${phone1} display
    Then Verify ringing state on ${phone2} and ${phone1}
    Then Answer the call on ${phone1} using ${offHook}
    Then Verify audio path between ${phone2} and ${phone1}
    Then On ${phone1} verify ${line1} icon state as ${callAppearanceActive}
    Then On ${phone2} verify ${line1} icon state as ${callAppearanceActive}
    Then On ${phone3} verify the softkeys in ${idleState}
    And Disconnect the call from ${phone1}

759994: TC015-Connect call with another user then terminate
    [Tags]    Owner:Anish    Reviewer:Aman    twoPartyCall
    Given I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then On ${phone2} verify ${line1} icon state as ${callAppearanceIncoming}
    Then Answer the call on ${phone2} using ${offHook}
    Then Verify audio path between ${phone1} and ${phone2}
    Then On ${phone1} verify ${line1} icon state as ${callAppearanceActive}
    Then On ${phone2} verify ${line1} icon state as ${callAppearanceActive}
    And Press hardkey as ${goodBye} on ${phone1}

759995: TC016-Basic 3-way conference
    [Tags]    Owner:Anish    Reviewer:Aman    conference
    Given I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then On ${phone2} verify ${line1} icon state as ${callAppearanceIncoming}
    Then Answer the call on ${phone2} using ${offHook}
    Then Verify audio path between ${phone1} and ${phone2}
    Then On ${phone1} verify ${line1} icon state as ${callAppearanceActive}
    Then On ${phone2} verify ${line1} icon state as ${callAppearanceActive}
    Then I want to make a conference call between ${phone1},${phone2} and ${phone3} using ${directConference}
    Then Conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then Disconnect the call from ${phone3}
    And Disconnect the call from ${phone2}

760027: TC048-Xmon operation when monitored phone has a Conference call
    [Tags]    Owner:Anish    Reviewer:Aman    xmonConf    notApplicableFor6910    760027
    &{extensionDetails}=  Create Dictionary    ring_delay=dont_ring    no_connected=unused    with_connected=unused    button_box=0    show_caller_id=Never
    Given Using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 3 with ExtensionValue
    Then Using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone3} and softkey position 4 with ExtensionValue
    Then On ${phone1} verify display message ${displayMessage["monitorExtn"]}
    Then I want to make a two party call between ${phone2} and ${phone3} using ${offHook}
    Then On ${phone1} verify the led state of ${line5} as ${blink} and led color as ${red}
    Then On ${phone1} verify ${line5} icon state as ${xmonRinging}
    Then Answer the call on ${phone3} using ${offHook}
    Then On ${phone1} verify the led state of ${line5} as ${on} and led color as ${red}
    Then On ${phone1} verify ${line5} icon state as ${xmonActive}
    Then I want to make a conference call between ${phone2},${phone3} and ${phone4} using ${consultiveConference}
    Then Conference call audio verify between ${phone4} ${phone2} and ${phone3}
    Then On ${phone1} verify the led state of ${line5} as ${on} and led color as ${red}
    Then On ${phone1} verify the led state of ${line4} as ${on} and led color as ${red}
    Then On ${phone1} verify ${line5} icon state as ${xmonConference}        # uncomment this when the support is there
    Then On ${phone1} verify ${line4} icon state as ${xmonConference}        # uncomment this when the support is there
    Then Disconnect the call from ${phone3}
    And Disconnect the call from ${phone2}
    [Teardown]    RUN KEYWORDS    Default Call Appearance    Generic Test Teardown

760007: TC028-From Directory Detailed Contacts view, use 5-way ...
    [Tags]    Owner:Avishek    760007
    Given On ${phone1} verify directory with ${directoryAction['searchOnly']} of ${phone2}
    Then press hardkey as ${enter} on ${phone1}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then answer the call on ${phone2} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    And disconnect the call from ${phone2}

760008: TC029-From Directory, select a user press SPEAKER ...
    [Tags]    Owner:Avishek    760008
    Given On ${phone1} verify directory with ${directoryAction['searchOnly']} of ${phone2}
    Then press hardkey as ${handsFree} on ${phone1}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then answer the call on ${phone2} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    And disconnect the call from ${phone2}

759989: TC010-Access user's Visual Voicemail view (Inbox, Saved, Deleted)
    [Tags]    Owner:Anuj    Reviewer:Vikhyat    voicemail    notApplicableFor6910    759989
    Given Delete voicemail message on ${inbox} for ${phone1} using ${voicemailPassword}
    Then Leave voicemail message from ${phone2} on ${phone1}
#    Then Leave voicemail message from ${phone2} on ${phone1}     # only one is also fine
#    Then Leave voicemail message from ${phone2} on ${phone1}
    Then Login into voicemailbox for ${phone1} using ${voicemailpassword}
#    Then On ${phone1} verify display message ${voicemailDisplay['inbox']}
#    Then On ${phone1} verify display message ${voicemailDisplay['saved']}
#    Then On ${phone1} verify display message ${voicemailDisplay['deleted']}
    Then Press hardkey as ${scrollRight} on ${phone1}
    Then Verify extension ${number} of ${phone2} on ${phone1}
    Then on ${phone1} verify display message ${play}
    Then on ${phone1} press the softkey ${play} in VoiceMailState
    Then on ${phone1} verify display message ${pause}
    Then on ${phone1} press the softkey ${save} in VoiceMailState
    Then Press hardkey as ${ScrollLeft} on ${phone1}
    Then Press hardkey as ${ScrollDown} on ${phone1}
    Then Press hardkey as ${ScrollRight} on ${phone1}
    Then Verify extension ${number} of ${phone2} on ${phone1}
    Then Move voicemail message from ${savedToDelete} folder for ${phone1}
    Then Verify extension ${number} of ${phone2} on ${phone1}
    Then Move voicemail message from ${deleteToInbox} folder for ${phone1}
    Then Verify extension ${number} of ${phone2} on ${phone1}
    And Press hardkey as ${goodBye} on ${phone1}

759992: TC013-Verify the call appearance on an inbound
    [Tags]    Owner:Anuj    Reviewer:Vikhyat    callappearance    759992
    Then press hardkey as ${offhook} on ${phone1}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then Verify the led state of ${line2} as ${blink} on ${phone1}
    And Press hardkey as ${goodBye} on ${phone2}

760023: TC044-Hang up the participants of a Mesh call
    [Tags]    Owner:Anuj    Reviewer:Vikhyat    conferencecall    760023
    Given i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then i want to make a conference call between ${phone1},${phone2} and ${phone3} using ${consultiveConference}
    Then conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}
    Then On ${phone1} verify the softkeys in ${idleState}
    Then On ${phone2} verify the softkeys in ${idleState}
    And On ${phone3} verify the softkeys in ${idleState}

759990: TC011-Call Back from user's Visual Voicemail
    [Tags]    Owner:Anuj    Reviewer:Vikhyat    voicemail    notApplicableFor6910    759990
    Given Leave voicemail message from ${phone2} on ${phone1}
    Then login into voicemailbox for ${phone1} using ${voicemailpassword}
    Then On ${phone1} verify display message ${voicemailDisplay['inbox']}
    Then On ${phone1} verify display message ${voicemailDisplay['saved']}
    Then On ${phone1} verify display message ${voicemailDisplay['deleted']}
    Then Press hardkey as ${scrollRight} on ${phone1}
    Then verify extension ${number} of ${phone2} on ${phone1}
    Then on ${phone1} press ${softkey} ${bottomkey2} for 1 times
    Then On ${phone2} dial number #
    Then on ${phone1} wait for 50 seconds
    Then Press hardkey as ${goodBye} on ${phone1}
    Then Login into voicemailbox for ${phone2} using ${voicemailpassword}
    Then Press hardkey as ${ScrollRight} on ${phone1}
    Then Verify extension ${number} of ${phone1} on ${phone2}
    And Press hardkey as ${goodBye} on ${phone1}
    [Teardown]    Generic Test Teardown

760024: TC045-Place a New call using Xmon key
    [Tags]    Owner:Anuj    Reviewer:Vikhyat    xmon    notApplicableFor6910    760024
    &{extensionDetails} =  Create Dictionary  ring_delay=none   show_caller_id=never    no_connected=dial_number    with_connected=dial_number    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone2}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then Disconnect the call from ${phone1}
    And using ${bossportal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4
    [Teardown]    RUN KEYWORDS    Default Call Appearance    Generic Test Teardown

759986: TC007-Return call from user's History
    [Tags]    Owner:Vikhyat    Reviewer:    callHistory
    Given I want to use fac ${privateCall} on ${phone1} to ${phone2}
    Then On ${phone2} verify display message ${callerBlocked}
    Then Answer the call on ${phone2} using ${offHook}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Disconnect the call from ${phone2}
    Then Press the call history button on ${phone1} and folder ${all} and ${details}
    Then On ${phone1} verify display message ${phone2}
    Then On ${phone1} press the key ${dial} in state ${callHistory}
    Then Verify ringing state on ${phone1} and ${phone2}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then Disconnect the call from ${phone2}

760009: TC030-Sort Directory by Last Name via softkey ...
    [Tags]    Owner:Vikhyat    Reviewer:    directorySort    notApplicableFor6910    760009
    Given On ${phone1} verify directory with ${default} of ${phone1}
    Then On ${phone1} press the key ${close} in state ${directory}
    Then Press hardkey as ${scrollLeft} on ${phone1}
    Then On ${phone1} press the key ${byLast} in state ${directory}
    Then Press hardkey as ${scrollRight} on ${phone1}
    Then On ${phone1} press ${hardKey} ${scrollDown} for 10 times
    Then Verify ${byLast} naming directory format on ${phone1}
    Then Press hardkey as ${goodBye} on ${phone1}
    [Teardown]    Default Directory Settings

760010: TC031-Missed Call Indicator for Calls
    [Tags]    Owner:Vikhyat    Reviewer:    missedCalls    #01/12/2020
    Given I want to make a two party call between ${phone2} and ${phone1} using ${offHook}
    Then Verify ringing state on ${phone2} and ${phone1}
    Then Disconnect the call from ${phone2}
    Then On ${phone1} verify display message Missed Call
    And Press the call history button on ${phone1} and folder ${missed} and ${quit}

905187: TC057- Make call to huntgroup extension
    [Tags]    Owner:Vikhyat    Reviewer:    huntGroup    notApplicableFor6910    #01/12/2020
    [Setup]    Hunt Group Custom Setup
    @{members}   Create List      ${phone2}    ${phone3}
    &{huntGroupDetails} =  Create Dictionary    BackupExtension=${phone2}    GroupMembers=${members}   GroupName=HG_VK   IncludeInSystem=False    MakeExtnPrivate=False    HuntPattern=4    RingsPerMember=3    NoAnswerRings=4    CallMemberWhenForwarding=True    SkipMemberOnCall=True    CallStackFull=${EMPTY}    NoAnswer=${EMPTY}
    ${HGExtension} =     using ${bossPortal} I want to create hunt group user extension with ${huntGroupDetails}

    Given On ${phone1} dial number ${HGExtension}
    Then on ${phone1} press the softkey ${dial} in DialingState
    Then Verify the led state of ${line1} as ${blink} on ${phone2}
    Then Verify the led state of ${line1} as ${blink} on ${phone3}
    Then Answer the call on ${phone2} using ${offHook}
    Then Verify audio path between ${phone1} and ${phone2}
    Then On the ${phone3} verify softkeys in different state using ${idleState}
    Then Verify extension ${name} of ${phone1} on ${phone2}
    Then Disconnect the call from ${phone1}
    [Teardown]    Hunt Group Custom Teardown

#760004: TC025-Assign & Unassign user Ext with TUI 7-3-1
#    [Tags]    Owner:Aman    Reviewer:Ram    anyPhone    assignUser    760004
#    Given on ${phone1} dial number #
#    Then on ${phone1} Wait for 5 seconds
#    Then on ${phone1} dial number ${loginVoicemail}
#    Then on ${phone1} Wait for 1 seconds
#    Then on ${phone1} dial number 7
#    Then on ${phone1} Wait for 1 seconds
#    Then on ${phone1} dial number 3
#    Then on ${phone1} Wait for 1 seconds
#    Then on ${phone1} dial number 2
#    Then on ${phone1} Wait for 25 seconds
#    Then On ${phone1} verify display message ${available}
#    Given on ${phone1} dial number ##
#    Then on ${phone1} Wait for 5 seconds
#    Then on ${phone1} enter number ${phone2}
#    Then on ${phone1} Wait for 2 seconds
#    Then on ${phone1} dial number ${loginVoicemail}
#    Then on ${phone1} Wait for 2 seconds
#    Then on ${phone1} dial number 7
#    Then on ${phone1} Wait for 2 seconds
#    Then on ${phone1} dial number 3
#    Then on ${phone1} Wait for 2 seconds
#    Then on ${phone1} dial number 1
#    Then on ${phone1} Wait for 25 seconds
#    Then Verify extension ${number} of ${phone2} on ${phone1}
#    Then i want to make a two party call between ${phone3} and ${phone2} using ${offHook}
#    Then answer the call on ${phone1} using ${offHook}
#    Then Verify audio path between ${phone1} and ${phone3}
#    Then Disconnect the call from ${phone1}
#    And on ${phone1} verify the softkeys in ${idleState}
#    [Teardown]      Assign Extension Custom Teardown

#759981: TC003-Register phone as Available state – place call to and join a Conference Bridge Then assign user with VM menu options 7-3-1 - Place call and open user's History
#    [Tags]    Owner:Abhishekkhanchi    Reviewer:     ucb    assignUser    notApplicableFor6910    need to check
#    [Setup]    Assign Extension Custom Setup
#    Then on ${phone1} dial number #
#    Then on ${phone1} Wait for 5 seconds
#    Then on ${phone1} dial number ${loginVoicemail}
#    Then on ${phone1} Wait for 3 seconds
#    Then on ${phone1} dial number 7
#    Then on ${phone1} Wait for 1 seconds
#    Then on ${phone1} dial number 3
#    Then on ${phone1} Wait for 1 seconds
#    Then on ${phone1} dial number 2
#    Then on ${phone1} Wait for 25 seconds
#    Then on ${phone1} verify display message ${available}
#    Then On ${phone1} Wait for 2 seconds
#    Then on ${phone1} press the key ${conference} in state ${idle}
#    Then on ${phone1} enter number ${accessCode}
#    Then on ${phone1} verify display message ${conference}
#    Then On ${phone1} Wait for 2 seconds
#    Then disconnect the call from ${phone1}
#    Then on ${phone1} dial number #
#    Then on ${phone1} Wait for 5 seconds
#    Then on ${phone1} enter number ${phone1}
#    Then on ${phone1} dial number ${loginVoicemail}
#    Then on ${phone1} Wait for 3 seconds
#    Then on ${phone1} dial number 7
#    Then on ${phone1} Wait for 1 seconds
#    Then on ${phone1} dial number 3
#    Then on ${phone1} Wait for 1 seconds
#    Then on ${phone1} dial number 1
#    Then on ${phone1} Wait for 5 seconds
#    Then Verify extension ${number} of ${phone1} on ${phone1}
#    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
#    Then Verify the led state of ${line1} as ${blink} on ${phone1}
#    Then Answer the call on ${phone1} using ${loudspeaker}
#    Then Verify audio path between ${phone2} and ${phone1}
#    Then disconnect the call from ${phone1}
#    Then I want to make a two party call between ${phone1} and ${phone2} using ${programKey1}
#    Then Disconnect the call from ${phone1}
#    Then Press the call history button on ${phone1} and folder ${outgoing} and ${details}
#    Then Verify extension ${number} of ${phone2} on ${phone1}
#    Then Press hardkey as ${goodBye} on ${phone1}
#    [Teardown]    Assign Extension Custom Teardown

#759984: TC005-Static IP - Register and Assign phone
#    [Tags]    Owner:Abhishekkhanchi    Reviewer:     notApplicableFor6910
#    Given on ${phone1} dial number #
#    Then on ${phone1} Wait for 5 seconds
#    Then on ${phone1} dial number ${loginVoicemail}
#    Then on ${phone1} Wait for 3 seconds
#    Then on ${phone1} dial number 7
#    Then on ${phone1} Wait for 1 seconds
#    Then on ${phone1} dial number 3
#    Then on ${phone1} Wait for 1 seconds
#    Then on ${phone1} dial number 2
#    Then on ${phone1} Wait for 25 seconds
#    Then on ${phone1} verify display message ${available}
#    &{Details} =  Create Dictionary      DHCP=${disable}
#    Then I want to configure Network parameters using ${Details} for ${phone1}
#    Then Reboot ${phone1}
#    Then on ${phone1} move to network_settings to ipaddress settings
#    Then On ${phone1} Wait for 4 seconds
#    Then Enter selfipaddress on ${phone1} to ipaddress settings
#    Then Press hardkey as ${goodBye} on ${phone1}
#    Then on ${phone1} dial number #
#    Then on ${phone1} Wait for 5 seconds
#    Then on ${phone1} enter number ${phone1}
#    Then on ${phone1} dial number ${loginVoicemail}
#    Then on ${phone1} Wait for 3 seconds
#    Then on ${phone1} dial number 7
#    Then on ${phone1} Wait for 1 seconds
#    Then on ${phone1} dial number 3
#    Then on ${phone1} Wait for 1 seconds
#    Then on ${phone1} dial number 1
#    Then on ${phone1} Wait for 5 seconds
#    Then Verify extension ${number} of ${phone1} on ${phone1}


#760833
#856364
# 91.55     6930#!/bin/python3
                #
                #
                #
                #import math
                #import os
                #import random
                #import re
                #import sys
                #
                #
                #
                #
                ## UDyTn6mHqBpBur
                ## 6UDTyn0Hm*BqBp*ur
                #def decryptPassword(s):
                #    print(s)
                #    decrypted_string = ''
                #    nums = ''
                #    i = 0
                #    j = -1
                #
                #
                #
                #    while s[i].isdigit():
                #        nums += s[i]
                #        i += 1
                #
                #
                #
                #    i = 0
                #    while i < (len(s)-1):
                #        print(i, end=' ')
                #        print(s[i], end=' ')
                #        if s[i].isalpha():
                #            print("isAlpha", end=' ')
                #            if s[i].isupper() and s[i+1].islower():
                #                decrypted_string = decrypted_string + s[i+1] + s[i]
                #                i +=1
                #            else:
                #                decrypted_string += s[i]
                #            print(decrypted_string)
                #        elif s[i] == '0':
                #            print("Is 0", end=' ')
                #            decrypted_string += nums[j]
                #            j -= 1
                #            print(decrypted_string)
                #            i += 1
                #
                #
                #
                #    if s[-1] == '0':
                #        decrypted_string += nums[0]
                #    else:
                #        decrypted_string += s[-1]
                #
                #
                #
                #    return decrypted_string
                #
                #
                #
                #
                #
                #if __name__ == '__main__':
                #    fptr = open(os.environ['OUTPUT_PATH'], 'w')
                #
                #
                #
                #    s = input()
                #
                #
                #
                #    result = decryptPassword(s)
                #
                #
                #
                #    fptr.write(result + '\n')
                #
                #
                #
                #    fpt


