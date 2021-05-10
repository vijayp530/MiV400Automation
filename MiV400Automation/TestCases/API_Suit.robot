
*** Settings ***
Resource    ../RobotKeywords/Setup_And_Teardown.robot
Resource    ../RobotKeywords/Boss_API_Keywords.robot

Suite Setup    RUN KEYWORDS    Phones Initialization    Get DUT Details
Test Setup     Check Phone Connection
Test Teardown  RUN KEYWORDS    Default Call Appearance    Generic Test Teardown
Suite Teardown    RUN KEYWORD AND IGNORE ERROR    RUN KEYWORDS    Check Phone Connection    Default Availability State
...                                                               Generic Test Teardown
Test Timeout    20 minutes

*** Test Cases ***
135548: Silent Monitor with permissions, target on conference call
    [Tags]    Owner:Ram    Reviewer:Avishek    SilentMonitor
    [Timeout]    25 minutes
    Given I want to make a two party call between ${phone2} and ${phone3} using ${loudspeaker}
    Then Answer the call on ${phone3} using ${loudSpeaker}
    Then Verify audio path between ${phone2} and ${phone3}
    Then I want to make a conference call between ${phone2},${phone3} and ${phone4} using ${consultiveConference}
    Then Conference call audio verify between ${phone2} ${phone3} and ${phone4}
    Then press hookmode ${offHook} on phone ${phone1}
    Then I want to use fac Silentmonitor on ${phone1} to ${phone2}
    Then on ${phone1} wait for 5 seconds
    Then On ${phone1} verify display message ${silentMonitor}
    Then On ${phone1} verify display message ${displayMessage['notPermit']}
    Then disconnect the call from ${phone3}
    Then disconnect the call from ${phone2}
    And disconnect the call from ${phone1}

    Given using ${bossPortal} I program ${silentMonitor} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with noExtensionValue
    Then On ${phone1} verify display message ${displayMessage['silentMonitor']}
    Then I want to make a two party call between ${phone2} and ${phone3} using ${loudspeaker}
    Then Answer the call on ${phone3} using ${loudSpeaker}
    Then Verify audio path between ${phone2} and ${phone3}
    Then I want to make a conference call between ${phone2},${phone3} and ${phone4} using ${consultiveConference}
    Then Conference call audio verify between ${phone2} ${phone3} and ${phone4}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} enter number ${phone1}
    Then on ${phone1} wait for 5 seconds
    Then On ${phone1} verify display message ${silentMonitor}
    Then On ${phone1} verify display message ${displayMessage['notPermit']}
    Then disconnect the call from ${phone3}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone1}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4

    Given using ${bossPortal} I program ${silentMonitor} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with ExtensionValue
    Then On ${phone1} verify display message ${displayMessage['silentMonitor']}
    Then I want to make a two party call between ${phone2} and ${phone3} using ${loudspeaker}
    Then Answer the call on ${phone3} using ${loudSpeaker}
    Then Verify audio path between ${phone2} and ${phone3}
    Then I want to make a conference call between ${phone2},${phone3} and ${phone4} using ${consultiveConference}
    Then Conference call audio verify between ${phone2} ${phone3} and ${phone4}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} wait for 5 seconds
    Then On ${phone1} verify display message ${silentMonitor}
    Then On ${phone1} verify display message ${displayMessage['notPermit']}
    Then disconnect the call from ${phone3}
    Then disconnect the call from ${phone2}
    And disconnect the call from ${phone1}

290858: Silent Coach button with extension target not programmed- On Hook
    [Tags]    Owner:Ram    Reviewer:Avishek    SilentCoach
    Given using ${bossPortal} I program ${silentCoach} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 1 with noExtensionValue
    Then On ${phone1} verify display message ${silentCoach}
    Then I want to make a two party call between ${phone2} and ${phone3} using ${loudspeaker}
    Then Answer the call on ${phone3} using ${loudSpeaker}
    Then I want to press line key ${programKey2} on phone ${phone1}
    Then On ${phone1} verify display message ${silentCoach}
    Then On ${phone1} verify display message >
    Then on ${phone1} enter number ${phone3}
    Then on ${phone1} wait for 5 seconds
    Then Verify audio path between ${phone2} and ${phone3}
    Then Verify no audio path from ${phone1} to ${phone2}
    Then Verify one way audio from ${phone2} to ${phone1}
    Then disconnect the call from ${phone1}
    Then Verify the Caller id on ${phone2} and ${phone3} display
    And disconnect the call from ${phone3}

147410: phone returns to Silent Coach during a Silent Monitor call
    [Tags]    Owner:Ram    Reviewer:Aman    silentMonitor
    Given using ${bossPortal} I program ${silentCoach} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with ExtensionValue
    Then On ${phone1} verify display message ${silentCoach}
    Then I want to make a two party call between ${phone2} and ${phone3} using ${loudSpeaker}
    Then answer the call on ${phone3} using ${loudSpeaker}
    Then Verify audio path between ${phone2} and ${phone3}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} wait for 10 seconds
    Then On ${phone1} verify display message ${silentCoach}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then Verify audio path between ${phone2} and ${phone3}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Verify one way audio from ${phone3} to ${phone1}
    Then Verify no audio path from ${phone1} to ${phone3}
    Then on ${phone1} press ${softKey} ${bottomKey2} for 1 times
    Then On ${phone1} verify display message ${silentMonitor}
    Then Verify audio path between ${phone2} and ${phone3}
    Then Verify one way audio from ${phone3} to ${phone1}
    Then Verify one way audio from ${phone2} to ${phone1}
    Then Verify no audio path from ${phone1} to ${phone2}
    Then Verify no audio path from ${phone1} to ${phone3}
    Then on ${phone1} press ${softKey} ${bottomKey2} for 1 times
    Then On ${phone1} verify display message ${silentCoach}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then Verify audio path between ${phone2} and ${phone3}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Verify one way audio from ${phone3} to ${phone1}
    Then Verify no audio path from ${phone1} to ${phone3}
    Then disconnect the call from ${phone1}
    And disconnect the call from ${phone3}

558038: Silent Coach button with extension target programmed- On Hook
    [Tags]    Owner:Ram    Reviewer:AbhishekPathak    SilentCoach
    Given using ${bossPortal} I program ${silentCoach} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with ExtensionValue
    Then On ${phone1} verify display message ${silentCoach}
    Then I want to make a two party call between ${phone2} and ${phone3} using ${loudspeaker}
    Then answer the call on ${phone3} using ${loudSpeaker}
    Then Verify audio path between ${phone2} and ${phone3}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} wait for 10 seconds
    Then Verify audio path between ${phone1} and ${phone2}
    Then Verify one way audio from ${phone3} to ${phone1}
    Then Verify no audio path from ${phone1} to ${phone3}
    Then On ${phone1} verify display message ${silentCoach}
    Then On ${phone1} verify display message ${drop}
    Then On ${phone1} verify display message ${monitor}
    Then On ${phone1} verify display message ${barge}
    Then On ${phone1} verify display message ${leave}
    Then Verify extension ${number} of ${phone2} on ${phone1}
    Then Verify extension ${number} of ${phone3} on ${phone1}
    Then on ${phone1} press the softkey ${drop} in AnswerState
    Then On ${phone1} verify the softkeys in ${idle}
    Then Verify the Caller id on ${phone2} and ${phone3} display
    And disconnect the call from ${phone2}

558048: Agent or Customer hangs up during a Silent Coach call
    [Tags]    Owner:Ram    Reviewer:AbhishekPathak    SilentCoach
    Given using ${bossPortal} I program ${silentMonitor} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with ExtensionValue
    Then On ${phone1} verify display message ${displayMessage['silentMonitor']}
    Then I want to make a two party call between ${phone2} and ${phone3} using ${offHook}
    Then answer the call on ${phone3} using ${offHook}
    Then Verify audio path between ${phone2} and ${phone3}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} wait for 10 seconds
    Then Verify one way audio from ${phone2} to ${phone1}
    Then Verify one way audio from ${phone3} to ${phone1}
    Then Verify no audio path from ${phone1} to ${phone3}
    Then Verify no audio path from ${phone1} to ${phone2}
    Then on ${phone1} press ${softKey} ${bottomKey2} for 1 times
    Then On ${phone1} verify display message ${silentCoach}
    Then Verify audio path between ${phone2} and ${phone3}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Verify one way audio from ${phone3} to ${phone1}
    Then Verify no audio path from ${phone1} to ${phone3}
    Then disconnect the call from ${phone3}
    Then On ${phone3} verify the softkeys in ${idle}
    Then On ${phone1} verify the softkeys in ${idle}
    And On ${phone2} verify the softkeys in ${idle}

139883: unpark - xmon
    [Tags]    Owner:Ram    Reviewer:AbhishekPathak    Xmon
    &{extensionDetails} =  Create Dictionary  ring_delay=1   show_caller_id=only_when_ringing    no_connected=unused    with_connected=unused    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone3} and softkey position 4 with ExtensionValue
    Then On ${phone1} verify display message ${displayMessage['monitorExtn']}
    Then I want to make a two party call between ${phone1} and ${phone2} using ${loudSpeaker}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then I want to Park the call from ${phone1} on ${phone3} using ${default} and ${timeout}
    Then On ${phone1} verify display message ${callParked}
    Then on ${phone1} wait for 5 seconds
    Then on ${phone1} press ${softKey} ${bottomKey2} for 1 times
    Then On ${phone1} verify display message ${unpark}
    Then On ${phone1} verify display message ${backSpace}
    Then On ${phone1} verify display message ${cancel}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} wait for 5 seconds
    Then Verify audio path between ${phone1} and ${phone2}
    And disconnect the call from ${phone2}

559819: Whisper Page: pressing xmon key on monitoring phone while being on active call
    [Tags]    Owner:Ram    Reviewer:AbhishekPathak    Xmon
    &{extensionDetails} =  Create Dictionary  ring_delay=1   show_caller_id=only_when_ringing    no_connected=whisper_page    with_connected=unused    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone3} and softkey position 4 with ExtensionValue
    Then On ${phone1} verify display message ${displayMessage['monitorExtn']}
    Then I want to make a two party call between ${phone1} and ${phone2} using ${loudSpeaker}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} wait for 5 seconds
    Then verify the led state of ${line5} as ${off} on ${phone1}
    Then on ${phone3} verify the softkeys in ${idle}
    Then verify the led state of speaker as ${off} on ${phone3}
    And disconnect the call from ${phone2}

559822: Whisper Page : Incoming call to target extension; press xmon key in idle state
    [Tags]    Owner:Ram    Reviewer:AbhishekPathak    Xmon
    &{extensionDetails} =  Create Dictionary  ring_delay=dont_ring   show_caller_id=never    no_connected=whisper_page    with_connected=unused    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone3} and softkey position 4 with ExtensionValue
    Then On ${phone1} verify display message ${displayMessage['monitorExtn']}
    Then I want to make a two party call between ${phone2} and ${phone3} using ${loudSpeaker}
    Then verify the led state of ${line5} as ${blink} on ${phone1}
    Then answer the call on ${phone3} using ${loudSpeaker}
    Then verify the led state of ${line5} as ${on} on ${phone1}
    Then Verify audio path between ${phone3} and ${phone2}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then Verify audio path between ${phone1} and ${phone3}
    Then disconnect the call from ${phone2}
    And disconnect the call from ${phone1}

559837: XMON, CID Never - 1 active call on target
    [Tags]    Owner:Ram    Reviewer:AbhishekPathak    Xmon
    &{extensionDetails} =  Create Dictionary  ring_delay=dont_ring   show_caller_id=never    no_connected=dial_number    with_connected=dial_number    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 4 with ExtensionValue
    Then On ${phone1} verify display message ${displayMessage['monitorExtn']}
    Then I want to make a two party call between ${phone2} and ${phone3} using ${loudSpeaker}
    Then answer the call on ${phone3} using ${loudSpeaker}
    Then Verify audio path between ${phone2} and ${phone3}
    Then verify the led state of ${line5} as ${on} on ${phone1}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then verify the led state of ${line2} as ${blink} on ${phone2}
    Then verify the led state of ${line5} as ${blink} on ${phone1}
    Then disconnect the call from ${phone1}
    And disconnect the call from ${phone3}

559839: XMON, CID Never - 1 incoming call on target
    [Tags]    Owner:Ram    Reviewer:AbhishekPathak    Xmon
    &{extensionDetails} =  Create Dictionary  ring_delay=dont_ring   show_caller_id=never    no_connected=dial_number    with_connected=dial_number    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 4 with ExtensionValue
    Then On ${phone1} verify display message ${displayMessage['monitorExtn']}
    Then I want to make a two party call between ${phone3} and ${phone2} using ${loudSpeaker}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then On ${phone1} Wait for 5 seconds
    Then Verify audio path between ${phone1} and ${phone3}
    Then Verify the Caller id on ${phone1} and ${phone3} display
    Then verify the led state of ${line5} as ${on} on ${phone1}
    Then On ${phone2} verify the softkeys in ${idle}
    And disconnect the call from ${phone3}

559848: XMON, CID Only When Ringing - 1 incoming call on target
    [Tags]    Owner:Ram    Reviewer:AbhishekPathak    Xmon
    &{extensionDetails} =  Create Dictionary  ring_delay=dont_ring   show_caller_id=only_when_ringing    no_connected=dial_number    with_connected=dial_number    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 4 with ExtensionValue
    Then On ${phone1} verify display message ${displayMessage['monitorExtn']}
    Then I want to make a two party call between ${phone3} and ${phone2} using ${loudSpeaker}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then Verify extension ${number} of ${phone3} on ${phone1}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then On ${phone1} Wait for 5 seconds
    Then Verify audio path between ${phone1} and ${phone3}
    Then Verify the Caller id on ${phone1} and ${phone3} display
    Then verify the led state of ${line5} as ${on} on ${phone1}
    Then On ${phone2} verify the softkeys in ${idle}
    And disconnect the call from ${phone3}

559809: dial number : pressing xmon key on monitoring phone while being on active call
    [Tags]    Owner:Ram    Reviewer:AbhishekPathak    Xmon
    &{extensionDetails} =  Create Dictionary  ring_delay=dont_ring   show_caller_id=only_when_ringing    no_connected=dial_number    with_connected=unused    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 4 with ExtensionValue
    Then On ${phone1} verify display message ${displayMessage['monitorExtn']}
    Then I want to make a two party call between ${phone1} and ${phone3} using ${loudSpeaker}
    Then answer the call on ${phone3} using ${loudSpeaker}
    Then Verify audio path between ${phone1} and ${phone3}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then verify the led state of ${line5} as ${off} on ${phone1}
    Then Verify the Caller id on ${phone1} and ${phone3} display
    Then On ${phone2} verify the softkeys in ${idle}
    And disconnect the call from ${phone3}

559812: Dial Number: Incoming call to target extension; press xmon key in idle state
    [Tags]    Owner:Ram    Reviewer:AbhishekPathak    Xmon
    &{extensionDetails} =  Create Dictionary  ring_delay=dont_ring   show_caller_id=only_when_ringing    no_connected=dial_number    with_connected=unused    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 4 with ExtensionValue
    Then On ${phone1} verify display message ${displayMessage['monitorExtn']}
    Then I want to make a two party call between ${phone3} and ${phone2} using ${loudSpeaker}
    Then verify the led state of ${line5} as ${blink} on ${phone1}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then Verify audio path between ${phone2} and ${phone3}
    Then verify the led state of ${line5} as ${on} on ${phone1}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} wait for 5 seconds
    Then verify the led state of ${line2} as ${blink} on ${phone2}
    Then Verify ringing state on ${phone1} and ${phone2}
    Then verify the led state of ${line1} as ${on} on ${phone2}
    Then disconnect the call from ${phone1}
    And disconnect the call from ${phone3}

559816: Intercom: : Holding a call
    [Tags]    Owner:Ram    Reviewer:AbhishekPathak    Xmon
    &{extensionDetails} =  Create Dictionary  ring_delay=dont_ring   show_caller_id=never    no_connected=intercom    with_connected=unused    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 4 with ExtensionValue
    Then On ${phone1} verify display message ${displayMessage['monitorExtn']}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify the led state of ${line5} as ${on} on ${phone1}
    Then Verify audio path between ${phone2} and ${phone1}
    Then Put the linekey ${line1} of ${phone2} on ${hold}
    Then verify the led state of ${line5} as ${blink} on ${phone1}
    And disconnect the call from ${phone1}

559871: CallerID - Always - DUT idle state - A receives inbound call - Connected
    [Tags]    Owner:Ram    Reviewer:AbhishekPathak    Xmon
    &{extensionDetails} =  Create Dictionary  ring_delay=dont_ring   show_caller_id=always    no_connected=unused    with_connected=unused    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 4 with ExtensionValue
    Then On ${phone1} verify display message ${displayMessage['monitorExtn']}
    Then I want to make a two party call between ${phone3} and ${phone2} using ${loudSpeaker}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then verify the led state of ${line5} as ${blink} on ${phone1}
    Then Verify extension ${number} of ${phone3} on ${phone1}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then Verify audio path between ${phone2} and ${phone3}
    Then Verify extension ${number} of ${phone3} on ${phone1}
    Then disconnect the call from ${phone1}
    Then I want to verify on ${phone1} negative display message ${phone3}
    And disconnect the call from ${phone3}


559879: CallerID - When ringing - DUT idle state - A receives inbound call - Cancel
    [Tags]    Owner:Ram    Reviewer:    Xmon
    &{extensionDetails} =  Create Dictionary  ring_delay=dont_ring   show_caller_id=only_when_ringing    no_connected=unused    with_connected=unused    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 4 with ExtensionValue
    Then On ${phone1} verify display message ${displayMessage['monitorExtn']}
    Then I want to make a two party call between ${phone3} and ${phone2} using ${loudSpeaker}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then verify the led state of ${line5} as ${blink} on ${phone1}
    Then Verify extension ${number} of ${phone3} on ${phone1}
    Then disconnect the call from ${phone3}
    And I want to verify on ${phone1} negative display message ${phone3}

559880: CallerID - When ringing - DUT idle state - A receives inbound call - Connected
    [Tags]    Owner:Ram    Reviewer:    Xmon
    &{extensionDetails} =  Create Dictionary  ring_delay=dont_ring   show_caller_id=only_when_ringing    no_connected=unused    with_connected=unused    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 4 with ExtensionValue
    Then On ${phone1} verify display message ${displayMessage['monitorExtn']}
    Then I want to make a two party call between ${phone3} and ${phone2} using ${loudSpeaker}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then verify the led state of ${line5} as ${blink} on ${phone1}
    Then Verify extension ${number} of ${phone3} on ${phone1}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then Verify audio path between ${phone2} and ${phone3}
    Then I want to verify on ${phone1} negative display message ${phone3}
    Then disconnect the call from ${phone3}
    And I want to verify on ${phone1} negative display message ${phone3}


559888: CallerID - Never - DUT idle state - A receives inbound call - Cancel
    [Tags]    Owner:Ram    Reviewer:    Xmon
    &{extensionDetails} =  Create Dictionary  ring_delay=dont_ring   show_caller_id=never    no_connected=unused    with_connected=unused    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 4 with ExtensionValue
    Then On ${phone1} verify display message ${displayMessage['monitorExtn']}
    Then I want to make a two party call between ${phone3} and ${phone2} using ${loudSpeaker}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then verify the led state of ${line5} as ${blink} on ${phone1}
    Then I want to verify on ${phone1} negative display message ${phone3}
    Then disconnect the call from ${phone3}
    And I want to verify on ${phone1} negative display message ${phone3}

559890: CallerID - Never - DUT idle state - A makes outbound call - Connected
    [Tags]    Owner:Ram    Reviewer:    Xmon
    &{extensionDetails} =  Create Dictionary  ring_delay=dont_ring   show_caller_id=never    no_connected=unused    with_connected=unused    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 4 with ExtensionValue
    Then On ${phone1} verify display message ${displayMessage['monitorExtn']}
    Then I want to make a two party call between ${phone3} and ${phone2} using ${loudSpeaker}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then verify the led state of ${line5} as ${blink} on ${phone1}
    Then I want to verify on ${phone1} negative display message ${phone3}
    And disconnect the call from ${phone3}

559892: CallerID - Never - DUT connected state - A receives inbound call
    [Tags]    Owner:Ram    Reviewer:    Xmon
    &{extensionDetails} =  Create Dictionary  ring_delay=dont_ring   show_caller_id=never    no_connected=unused    with_connected=unused    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 4 with ExtensionValue
    Then On ${phone1} verify display message ${displayMessage['monitorExtn']}
    Then I want to make a two party call between ${phone1} and ${phone4} using ${loudSpeaker}
    Then answer the call on ${phone4} using ${loudSpeaker}
    Then Verify audio path between ${phone1} and ${phone4}
    Then I want to make a two party call between ${phone3} and ${phone2} using ${loudSpeaker}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then verify the led state of ${line5} as ${blink} on ${phone1}
    Then I want to verify on ${phone1} negative display message ${phone3}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then Verify audio path between ${phone2} and ${phone3}
    Then I want to verify on ${phone1} negative display message ${phone3}
    Then disconnect the call from ${phone3}
    Then verify the caller id on ${phone1} and ${phone4} display
    And disconnect the call from ${phone4}

559899: TC03: Ring delay before alert set to None - Offhook - onhook from DUT
    [Tags]    Owner:Ram    Reviewer:    Xmon
    &{extensionDetails} =  Create Dictionary  ring_delay=none   show_caller_id=only_when_ringing    no_connected=unused    with_connected=unused    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 4 with ExtensionValue
    Then On ${phone1} verify display message ${displayMessage['monitorExtn']}
    Then I want to make a two party call between ${phone3} and ${phone2} using ${loudSpeaker}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then Verify extension ${number} of ${phone3} on ${phone1}
    Then Press hookMode ${offHook} on phone ${phone1}
    Then Press hookMode ${onHook} on phone ${phone1}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then Verify extension ${number} of ${phone3} on ${phone1}
    And disconnect the call from ${phone3}

559980: make a call from A to B. Set C ext. mon to ONLY WHEN RINGING
    [Tags]    Owner:Ram    Reviewer:    Xmon
    &{extensionDetails} = Create Dictionary  ring_delay=none   show_caller_id=only_when_ringing    no_connected=unused    with_connected=unused    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 4 with ExtensionValue
    Then On ${phone1} verify display message ${displayMessage['monitorExtn']}
    Then I want to make a two party call between ${phone3} and ${phone2} using ${loudSpeaker}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then Verify extension ${number} of ${phone3} on ${phone1}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then Verify audio path between ${phone2} and ${phone3}
    Then I want to verify on ${phone1} negative display message ${phone3}
    Then verify the led state of ${line5} as ${on} on ${phone1}
    And disconnect the call from ${phone3}

560004: (connected call : Whisper page)when monitoring phone is Ringing and target extension is on Active call
    [Tags]    Owner:Ram    Reviewer:    Xmon
    &{extensionDetails} =  Create Dictionary  ring_delay=none   show_caller_id=always    no_connected=unused    with_connected=whisper_page    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 4 with ExtensionValue
    Then On ${phone1} verify display message ${displayMessage['monitorExtn']}
    Then I want to make a two party call between ${phone3} and ${phone2} using ${offHook}
    Then answer the call on ${phone2} using ${offHook}
    Then Verify audio path between ${phone2} and ${phone3}
    Then verify the led state of ${line5} as ${on} on ${phone1}
    Then I want to make a two party call between ${phone4} and ${phone1} using ${loudSpeaker}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then Verify extension ${number} of ${phone3} on ${phone1}
    Then I want to verify on ${phone1} negative display message ${phone2}
    Then verify the led state of ${line2} as ${off} on ${phone1}
    Then verify the led state of ${line2} as ${off} on ${phone2}
    Then disconnect the call from ${phone3}
    And disconnect the call from ${phone4}

560005:Pressing xmon key (with connected call : Transfer Blind)when target extension is ringing
    [Tags]    Owner:Ram    Reviewer:    Xmon
    &{extensionDetails} =  Create Dictionary  ring_delay=none   show_caller_id=always    no_connected=unused    with_connected=transfer_blind    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 4 with ExtensionValue
    Then On ${phone1} verify display message ${displayMessage['monitorExtn']}
    Then I want to make a two party call between ${phone3} and ${phone2} using ${loudSpeaker}
    Then I want to make a two party call between ${phone4} and ${phone1} using ${loudSpeaker}
    Then answer the call on ${phone1} using ${line1}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then verify the led state of ${line5} as ${on} on ${phone1}
    Then Verify extension ${number} of ${phone3} on ${phone1}
    Then On ${phone2} verify the softkeys in ${idle}
    Then disconnect the call from ${phone3}
    And disconnect the call from ${phone4}

560006: (connected call : Transfer Blind )when monitoring phone is in held state and target extension is ringing back
    [Tags]    Owner:Ram    Reviewer:    Xmon
    &{extensionDetails} =  Create Dictionary  ring_delay=none   show_caller_id=always    no_connected=unused    with_connected=transfer_blind    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 4 with ExtensionValue
    Then On ${phone1} verify display message ${displayMessage['monitorExtn']}
    Then I want to make a two party call between ${phone2} and ${phone3} using ${loudSpeaker}
    Then answer the call on ${phone3} using ${line1}
    Then Verify audio path between ${phone2} and ${phone3}
    Then verify the led state of ${line5} as ${on} on ${phone1}
    Then I want to make a two party call between ${phone1} and ${phone4} using ${loudSpeaker}
    Then answer the call on ${phone4} using ${line1}
    Then Put the linekey ${line1} of ${phone1} on ${hold}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then Verify extension ${number} of ${phone4} on ${phone2}
    Then verify the led state of ${line5} as ${blink} on ${phone1}
    Then verify the led state of ${line2} as ${blink} on ${phone2}
    Then disconnect the call from ${phone3}
    And disconnect the call from ${phone4}

560009: Pressing xmon key (with connected call : Intercom )when target extension is ringing
    [Tags]    Owner:Ram    Reviewer:    Xmon
    &{extensionDetails} =  Create Dictionary  ring_delay=none   show_caller_id=always    no_connected=unused    with_connected=intercom    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 4 with ExtensionValue
    Then On ${phone1} verify display message ${displayMessage['monitorExtn']}
    Then I want to make a two party call between ${phone3} and ${phone2} using ${loudSpeaker}
    Then I want to make a two party call between ${phone4} and ${phone1} using ${loudSpeaker}
    Then answer the call on ${phone1} using ${line1}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then Verify audio path between ${phone1} and ${phone3}
    Then On ${phone2} verify the softkeys in ${idle}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then verify the led state of ${line5} as ${on} on ${phone1}
    Then verify no audio path from ${phone1} to ${phone4}
    Then verify no audio path from ${phone4} to ${phone1}
    Then disconnect the call from ${phone3}
    And disconnect the call from ${phone4}

560013: Pressing xmon key (with connected call : Transfer Consultative )when target extension is ringing back
    [Tags]    Owner:Ram    Reviewer:    Xmon
    &{extensionDetails} =  Create Dictionary  ring_delay=none   show_caller_id=always    no_connected=unused    with_connected=transfer_consultative    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 4 with ExtensionValue
    Then On ${phone1} verify display message ${displayMessage['monitorExtn']}
    Then I want to make a two party call between ${phone2} and ${phone3} using ${loudSpeaker}
    Then I want to make a two party call between ${phone4} and ${phone1} using ${loudSpeaker}
    Then answer the call on ${phone1} using ${line1}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then verify the led state of ${line2} as ${blink} on ${phone2}
    Then verify the led state of ${line5} as ${blink} on ${phone1}
    Then on ${phone2} wait for 10 seconds
    Then verify the led state of ${line2} as ${blink} on ${phone2}
    Then disconnect the call from ${phone3}
    Then disconnect the call from ${phone1}
    And disconnect the call from ${phone2}

560018: (connected call : Transfer Intercom)when monitoring phone is in held state and target extension is ringing
    [Tags]    Owner:Ram    Reviewer:    Xmon
    &{extensionDetails} =  Create Dictionary  ring_delay=none   show_caller_id=always    no_connected=unused    with_connected=transfer_intercom    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 4 with ExtensionValue
    Then On ${phone1} verify display message ${displayMessage['monitorExtn']}
    Then I want to make a two party call between ${phone4} and ${phone1} using ${loudSpeaker}
    Then I want to make a two party call between ${phone3} and ${phone2} using ${loudSpeaker}
    Then answer the call on ${phone1} using ${line1}
    Then press hardkey as ${holdState} on ${phone1}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then verify the led state of ${line5} as ${on} on ${phone1}
    Then Verify audio path between ${phone1} and ${phone3}
    Then disconnect the call from ${phone3}
    And disconnect the call from ${phone4}

557936: Group page during Whisper Page call
    [Tags]    Owner:Ram    Reviewer:    PagingGroup
    [Setup]    Paging Group Custom Setup
    @{members}   Create List      ${phone1}    ${phone2}
    &{pagingGroups} =  Create Dictionary    PagingGroupName=HCL   PageListName=HCL    GroupMembers=${members}   PagingDelay=1    PriorityPage=true    RingsPerMember=10    PriorityPageAudioPath=1    MakeExtensionPrivate=False
    ${PGExtension}=    using ${bossPortal} I want to create paging groups using ${pagingGroups}
    Given using ${bossPortal} I program ${whisperPage} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with ExtensionValue
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then verify audio path between ${phone1} and ${phone2}
    Then Verify the led state of ${line2} as ${off} on ${phone1}
    Then Verify the led state of ${line2} as ${off} on ${phone2}
    Then on ${phone3} dial number ${PGExtension}
    Then Verify the led state of ${line1} as ${off} on ${phone1}
    Then Verify the led state of ${line1} as ${off} on ${phone2}
    Then Verify the led state of ${line2} as ${on} on ${phone1}
    Then Verify the led state of ${line2} as ${on} on ${phone2}
    Then On ${phone1} verify display message ${PGExtension}
    Then disconnect the call from ${phone1}
    Then disconnect the call from ${phone2}

    Given I want to use fac Whisperpage on ${phone1} to ${phone2}
    Then on ${phone1} press the softkey ${dial} in DialingState
    Then verify audio path between ${phone1} and ${phone2}
    Then Verify the led state of ${line2} as ${off} on ${phone1}
    Then Verify the led state of ${line2} as ${off} on ${phone2}
    Then on ${phone3} dial number ${PGExtension}
    Then Verify the led state of ${line1} as ${off} on ${phone1}
    Then Verify the led state of ${line1} as ${off} on ${phone2}
    Then Verify the led state of ${line2} as ${on} on ${phone1}
    Then Verify the led state of ${line2} as ${on} on ${phone2}
    Then On ${phone1} verify display message ${PGExtension}
    Then disconnect the call from ${phone1}
    And disconnect the call from ${phone2}
    [Teardown]     Paging Group Custom Teardown

557943: Inbound call during Priority Page
    [Tags]    Owner:Ram    Reviewer:    PagingGroup
    [Setup]    Paging Group Custom Setup
    @{members}   Create List      ${phone1}    ${phone2}
    &{pagingGroups} =  Create Dictionary    PagingGroupName=HCL   PageListName=HCL    GroupMembers=${members}   PagingDelay=1    PriorityPage=true    RingsPerMember=10    PriorityPageAudioPath=1    MakeExtensionPrivate=False
    ${PGExtension}=    using ${bossPortal} I want to create paging groups using ${pagingGroups}
    Given on ${phone3} dial number ${PGExtension}
    Then on ${phone1} verify display message ${PGExtension}
    Then on ${phone2} verify display message ${PGExtension}
    Then on ${phone4} dial number ${PGExtension}
    Then on ${phone4} verify display message ${busy}
    Then disconnect the call from ${phone1}
    And disconnect the call from ${phone2}
    [Teardown]    Paging Group Custom Teardown

557940: View Call History during group Page
    [Tags]    Owner:Ram    Reviewer:    PagingGroup
    [Setup]    Paging Group Custom Setup
    @{members}   Create List      ${phone1}    ${phone2}
    &{pagingGroups} =  Create Dictionary    PagingGroupName=HCL   PageListName=HCL    GroupMembers=${members}   PagingDelay=1    PriorityPage=true    RingsPerMember=10    PriorityPageAudioPath=1    MakeExtensionPrivate=False
    ${PGExtension}=    using ${bossPortal} I want to create paging groups using ${pagingGroups}
    Given on ${phone3} dial number ${PGExtension}
    Then on ${phone1} wait for 3 seconds
    Then on ${phone1} verify display message ${PGExtension}
    Then on ${phone2} verify display message ${PGExtension}
    Then press hardkey as ${redial} on ${phone1}
    Then on ${phone1} wait for 5 seconds
    Then on ${phone1} verify display message ${callHistory}
    Then press hardkey as ${goodBye} on ${phone1}
    Then disconnect the call from ${phone1}
    Then disconnect the call from ${phone2}
    And using ${bossPortal} I want to delete paging groups ${PGExtension} and paging extension list ${pagingGroups['PageListName']}


    @{members}   Create List      ${phone1}    ${phone2}
    &{pagingGroups} =  Create Dictionary    PagingGroupName=HCL   PageListName=HCL    GroupMembers=${members}   PagingDelay=1    PriorityPage=false    RingsPerMember=10    PriorityPageAudioPath=1    MakeExtensionPrivate=False
    ${PGExtension}=    using ${bossPortal} I want to create paging groups using ${pagingGroups}
    Given on ${phone3} dial number ${PGExtension}
    Then on ${phone1} wait for 3 seconds
    Then on ${phone1} verify display message ${PGExtension}
    Then on ${phone2} verify display message ${PGExtension}
    Then press hardkey as ${redial} on ${phone1}
    Then on ${phone1} wait for 5 seconds
    Then on ${phone1} verify display message ${callHistory}
    Then press hardkey as ${goodBye} on ${phone1}
    Then disconnect the call from ${phone1}
    And disconnect the call from ${phone2}
    [Teardown]    paging group custom teardown

557951: View Directory during Priority Page
    [Tags]    Owner:Ram    Reviewer:    PagingGroup
    [Setup]    Paging Group Custom Setup
    @{members}   Create List      ${phone1}    ${phone2}
    &{pagingGroups} =  Create Dictionary    PagingGroupName=HCL   PageListName=HCL    GroupMembers=${members}   PagingDelay=1    PriorityPage=true    RingsPerMember=10    PriorityPageAudioPath=2    MakeExtensionPrivate=False
    ${PGExtension}=    using ${bossPortal} I want to create paging groups using ${pagingGroups}
    Given on ${phone3} dial number ${PGExtension}
    Then on ${phone1} wait for 3 seconds
    Then on ${phone1} verify display message ${PGExtension}
    Then on ${phone2} verify display message ${PGExtension}
    Then press hardkey as ${directory} on ${phone1}
    Then on ${phone1} wait for 5 seconds
    Then on ${phone1} verify display message ${directory}
    Then press hardkey as ${goodBye} on ${phone1}
    Then disconnect the call from ${phone1}
    And disconnect the call from ${phone2}
    [Teardown]    Paging Group Custom Teardown

559072: Admin1 BCA Calls A, Admin2 BCA Calls B, Admin1 BCA confs Admin2 call, Admin2 locks, Admin1 returns to A, joins.
    [Tags]    Owner:Ram    Reviewer:Aman    BCA
    [Setup]    BCA Custom Setup
    &{createBCAExtension1} =  Create Dictionary    name=Ram1   backupExtn=${phone3}    switch=2    callStackDepth=2    forwardAfter=2    callStackFull=${EMPTY}   noAnswer=${EMPTY}    outboundCallerID=${EMPTY}    allowBridgeConferencing=true   defaultPrivacySettings=0
    &{createBCAExtension2} =  Create Dictionary    name=Ram2   backupExtn=${phone3}    switch=2    callStackDepth=2    forwardAfter=2    callStackFull=${EMPTY}   noAnswer=${EMPTY}    outboundCallerID=${EMPTY}    allowBridgeConferencing=true   defaultPrivacySettings=0
    ${bcaExtn1}=    using ${bossPortal} I want to create Bridge Call Appearance extension using ${createBCAExtension1}
    ${bcaExtn2}=    using ${bossPortal} I want to create Bridge Call Appearance extension using ${createBCAExtension2}
    &{BCAdetails1} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=3    function=Bridge Call Appearance    label=BCA1    target_extension=${bcaExtn1}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${phone3}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=Dial Extension
    &{BCAdetails2} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=4    function=Bridge Call Appearance    label=BCA2    target_extension=${bcaExtn2}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${phone4}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=Dial extension
    &{BCAdetails3} =  Create Dictionary    user_extension=${phone2}    button_box=0    soft_key=2    function=Bridge Call Appearance    label=BCA2    target_extension=${bcaExtn2}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${phone4}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=Dial extension
    Given using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails1}
    Then using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails2}
    Then using ${bossPortal} I want to create bca on ${phone2} using ${BCAdetails3}
    Then on ${phone1} verify display message BCA1
    Then on ${phone1} verify display message BCA2
    Then on ${phone2} verify display message BCA2
    Then I want to press line key ${programKey4} on phone ${phone1}
    Then answer the call on ${phone3} using ${loudSpeaker}
    Then I want to press line key ${programKey3} on phone ${phone2}
    Then answer the call on ${phone4} using ${loudSpeaker}
    Then on ${phone1} press the softkey ${conference} in AnswerState
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then Conference call audio verify between ${phone2} ${phone3} and ${phone4}
    Then verify the led state of ${line4} as ${off} on ${phone1}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then four party conference call audio verification between ${phone1} ${phone2} ${phone3} and ${phone4}
    Then on ${phone2} press the softkey ${lock} in ConferenceCallState
    Then press hardkey as ${holdState} on ${phone1}
    Then verify the led state of ${line5} as ${blink} on ${phone1}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then four party conference call audio verification between ${phone1} ${phone2} ${phone3} and ${phone4}
    Then disconnect the call from ${phone4}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}
    [Teardown]    BCA Custom Teardown

559074: Admin1 BCA Calls A, Admin2 BCA Calls B, Admin1 holds call, Admin2 joins, Admin1 unholds.
    [Tags]    Owner:Ram    Reviewer:    BCA
    [Setup]    BCA Custom Setup
    &{createBCAExtension1} =  Create Dictionary    name=Ram1   backupExtn=${phone3}    switch=2    callStackDepth=2    forwardAfter=2    callStackFull=${EMPTY}   noAnswer=${EMPTY}    outboundCallerID=${EMPTY}    allowBridgeConferencing=true   defaultPrivacySettings=0
    &{createBCAExtension2} =  Create Dictionary    name=Ram2   backupExtn=${phone3}    switch=2    callStackDepth=2    forwardAfter=2    callStackFull=${EMPTY}   noAnswer=${EMPTY}    outboundCallerID=${EMPTY}    allowBridgeConferencing=true   defaultPrivacySettings=0
    ${bcaExtn1}=    using ${bossPortal} I want to create Bridge Call Appearance extension using ${createBCAExtension1}
    ${bcaExtn2}=    using ${bossPortal} I want to create Bridge Call Appearance extension using ${createBCAExtension2}
    &{BCAdetails1} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=3    function=Bridge Call Appearance    label=BCA1    target_extension=${bcaExtn1}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${phone3}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=Dial Extension
    &{BCAdetails2} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=4    function=Bridge Call Appearance    label=BCA2    target_extension=${bcaExtn2}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${phone4}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=Dial extension
    &{BCAdetails3} =  Create Dictionary    user_extension=${phone2}    button_box=0    soft_key=2    function=Bridge Call Appearance    label=BCA1    target_extension=${bcaExtn1}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${phone3}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=Dial extension
    Given using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails1}
    Then using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails2}
    Then using ${bossPortal} I want to create bca on ${phone2} using ${BCAdetails3}
    Then on ${phone1} verify display message BCA1
    Then on ${phone1} verify display message BCA2
    Then on ${phone2} verify display message BCA1
    Then I want to press line key ${programKey3} on phone ${phone2}
    Then answer the call on ${phone3} using ${loudSpeaker}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then answer the call on ${phone4} using ${loudSpeaker}
    Then press hardkey as ${holdState} on ${phone2}
    Then verify the led state of ${line3} as ${blink} on ${phone2}
    Then on ${phone1} press the softkey ${conference} in AnswerState
    Then I want to press line key ${programKey4} on phone ${phone1}
    Then verify the led state of ${line4} as ${on} on ${phone1}
    Then verify the led state of ${line5} as ${off} on ${phone1}
    Then Conference call audio verify between ${phone1} ${phone3} and ${phone4}
    Then Verify extension ${number} of ${phone3} on ${phone1}
    Then Verify extension ${number} of ${phone4} on ${phone1}
    Then I want to press line key ${programKey3} on phone ${phone2}
    Then four party conference call audio verification between ${phone1} ${phone2} ${phone3} and ${phone4}
    Then on ${phone1} press ${softKey} ${bottomKey3} for 1 times
    Then Verify extension ${number} of ${phone2} on ${phone1}
    Then Verify extension ${number} of ${phone3} on ${phone1}
    Then Verify extension ${number} of ${phone4} on ${phone1}
    Then disconnect the call from ${phone4}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}
    [Teardown]    BCA Custom Teardown

559080: Admin1 holds call, admin2 picks up, admin2 hangs up, doesnt see prompt
    [Tags]    Owner:Ram    Reviewer:    BCA
    [Setup]    BCA Custom Setup
    &{createBCAExtension1} =  Create Dictionary    name=bca   backupExtn=${phone3}    switch=2    callStackDepth=2    forwardAfter=2    callStackFull=${EMPTY}   noAnswer=${EMPTY}    outboundCallerID=${EMPTY}    allowBridgeConferencing=true   defaultPrivacySettings=0
    ${bcaExtn1}=    using ${bossPortal} I want to create Bridge Call Appearance extension using ${createBCAExtension1}
    &{BCAdetails1} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=3    function=Bridge Call Appearance    label=BCA1    target_extension=${bcaExtn1}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${phone3}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=Dial Extension
    Given using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails1}
    Then using ${bossPortal} I want to create bca on ${phone2} using ${BCAdetails1}
    Then I want to press line key ${programKey4} on phone ${phone1}
    Then answer the call on ${phone3} using ${loudSpeaker}
    Then verify audio path between ${phone1} and ${phone3}
    Then press hardkey as ${holdState} on ${phone1}
    Then I want to press line key ${programKey4} on phone ${phone2}
    Then verify the led state of ${line4} as ${off} on ${phone1}
    Then verify audio path between ${phone2} and ${phone3}
    Then disconnect the call from ${phone2}
    Then verify the led state of ${line4} as ${off} on ${phone2}
    [Teardown]    BCA Custom Teardown

559083: BCA Conf enabled, locked. Admin1 BCA Calls A, Admin2 BCA Calls B, Admin1 joins.
    [Tags]    Owner:Ram    Reviewer:    BCA
    [Setup]    BCA Custom Setup
    &{createBCAExtension1} =  Create Dictionary    name=bca1   backupExtn=${phone3}    switch=2    callStackDepth=2    forwardAfter=2    callStackFull=${EMPTY}   noAnswer=${EMPTY}    outboundCallerID=${EMPTY}    allowBridgeConferencing=true   defaultPrivacySettings=0
    &{createBCAExtension2} =  Create Dictionary    name=bca2   backupExtn=${phone3}    switch=2    callStackDepth=2    forwardAfter=2    callStackFull=${EMPTY}   noAnswer=${EMPTY}    outboundCallerID=${EMPTY}    allowBridgeConferencing=true   defaultPrivacySettings=0
    ${bcaExtn1}=    using ${bossPortal} I want to create Bridge Call Appearance extension using ${createBCAExtension1}
    ${bcaExtn2}=    using ${bossPortal} I want to create Bridge Call Appearance extension using ${createBCAExtension2}
    &{BCAdetails1} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=3    function=Bridge Call Appearance    label=BCA1    target_extension=${bcaExtn1}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${phone3}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=Dial Extension
    &{BCAdetails2} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=4    function=Bridge Call Appearance    label=BCA2    target_extension=${bcaExtn2}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${phone4}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=Dial extension
    &{BCAdetails3} =  Create Dictionary    user_extension=${phone2}    button_box=0    soft_key=2    function=Bridge Call Appearance    label=BCA2    target_extension=${bcaExtn2}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${phone4}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=Dial extension
    Given using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails1}
    Then using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails2}
    Then using ${bossPortal} I want to create bca on ${phone2} using ${BCAdetails3}
    Then on ${phone1} verify display message BCA1
    Then on ${phone1} verify display message BCA2
    Then on ${phone2} verify display message BCA2
    Then I want to press line key ${programKey4} on phone ${phone1}
    Then answer the call on ${phone3} using ${loudSpeaker}
    Then verify audio path between ${phone1} and ${phone3}
    Then I want to press line key ${programKey3} on phone ${phone2}
    Then answer the call on ${phone4} using ${loudSpeaker}
    Then verify audio path between ${phone2} and ${phone4}
    Then on ${phone2} press the softkey ${lock} in AnswerState
    Then on ${phone1} press the softkey ${conference} in AnswerState
    Then I want to press line key ${programKey5} on phone ${phone1}
    And on ${phone1} verify display message ${actionNotPermitted}
    [Teardown]    BCA Custom Teardown

135543: Barge In with permissions, target on conference call
    [Tags]    Owner:Ram    Reviewer:Aman    BargeIn
    &{COSDetails} =  Create Dictionary    Name=${fullyFeatured}   AllowBargeInInitiation=True    BargeInAccept=1
    Given using ${bossPortal} I want to change telephony features values using ${COSDetails}
    Then I want to make a two party call between ${phone2} and ${phone3} using ${loudspeaker}
    Then Answer the call on ${phone3} using ${loudSpeaker}
    Then Verify audio path between ${phone2} and ${phone3}
    Then I want to make a conference call between ${phone2},${phone3} and ${phone4} using ${consultiveConference}
    Then Conference call audio verify between ${phone2} ${phone3} and ${phone4}
    Then press hookmode ${offHook} on phone ${phone1}
    Then I want to use fac Bargein on ${phone1} to ${phone2}
    Then on ${phone1} wait for 5 seconds
    Then On ${phone1} verify display message ${bargeIn}
    Then On ${phone1} verify display message ${displayMessage['notPermit']}
    Then disconnect the call from ${phone3}
    Then disconnect the call from ${phone1}
    [Teardown]    CoS Features Custom Teardown

558100: Silent Monitor with permissions, target on a call
    [Tags]    Owner:Ram    Reviewer:Aman    SilentMonitor
    &{COSDetails} =  Create Dictionary    Name=${fullyFeatured}   AllowSilentMonitorInitiation=True    SilentMonitorAccept=1
    Given using ${bossPortal} I want to change telephony features values using ${COSDetails}
    Then I want to make a two party call between ${phone2} and ${phone3} using ${loudspeaker}
    Then answer the call on ${phone3} using ${loudSpeaker}
    Then Verify audio path between ${phone2} and ${phone3}
    Then press hookmode ${offHook} on phone ${phone1}
    Then I want to use fac Silentmonitor on ${phone1} to ${phone2}
    Then on ${phone1} wait for 10 seconds
    Then On ${phone1} verify display message ${silentMonitor}
    Then Verify one way audio from ${phone3} to ${phone1}
    Then Verify one way audio from ${phone2} to ${phone1}
    Then Verify no audio path from ${phone1} to ${phone2}
    Then Verify no audio path from ${phone1} to ${phone3}
    Then Verify audio path between ${phone2} and ${phone3}
    Then I want to verify on ${phone2} negative display message ${phone1}
    Then I want to verify on ${phone3} negative display message ${phone1}
    Then disconnect the call from ${phone1}
    Then disconnect the call from ${phone3}
    [Teardown]    CoS Features Custom Teardown

139886: Toggle between Consult & Resume during Silent Coach
    [Tags]    Owner:Ram    Reviewer:Avishek    SilentCoach
    &{COSDetails} =  Create Dictionary    Name=${fullyFeatured}   AllowSilentMonitorInitiation=True    SilentMonitorAccept=1
    Given using ${bossPortal} I want to change telephony features values using ${COSDetails}
    Then I want to make a two party call between ${phone2} and ${phone3} using ${loudspeaker}
    Then Answer the call on ${phone3} using ${loudSpeaker}
    Then I want to use fac Silentcoach on ${phone1} to ${phone2}
    Then on ${phone1} wait for 10 seconds
    Then on ${phone1} verify display message ${silentCoach}
    Then I want to verify on ${phone2} negative display message ${transfer}
    Then I want to verify on ${phone2} negative display message ${conference}
    Then Verify audio path between ${phone2} and ${phone3}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Verify one way audio from ${phone3} to ${phone1}
    Then on ${phone2} press ${softKey} ${bottomKey2} for 1 times
    Then Verify one way audio from ${phone3} to ${phone2}
    Then Verify no audio path from ${phone2} to ${phone3}
    Then on ${phone2} press ${softKey} ${bottomKey2} for 1 times
    Then Verify audio path between ${phone2} and ${phone3}
    Then disconnect the call from ${phone1}
    And disconnect the call from ${phone3}

    Given I want to make a two party call between ${phone2} and ${phone3} using ${loudspeaker}
    Then Answer the call on ${phone3} using ${loudSpeaker}
    Then I want to use fac Silentmonitor on ${phone1} to ${phone2}
    Then on ${phone1} wait for 10 seconds
    Then on ${phone1} verify display message ${silentMonitor}
    Then Verify audio path between ${phone2} and ${phone3}
    Then Verify one way audio from ${phone2} to ${phone1}
    Then Verify one way audio from ${phone3} to ${phone1}
    Then Verify no audio path from ${phone1} to ${phone2}
    Then Verify no audio path from ${phone1} to ${phone3}
    Then on ${phone2} verify display message ${transfer}
    Then on ${phone2} verify display message ${conference}
    Then disconnect the call from ${phone2}
    [Teardown]    CoS Features Custom Teardown

557935: Group Page during active call
    [Tags]    Owner:Ram    Reviewer:    PagingGroup
    [Setup]    Paging Group Custom Setup
    @{members}   Create List      ${phone1}    ${phone2}
    &{pagingGroups} =  Create Dictionary    PagingGroupName=HCL   PageListName=HCL    GroupMembers=${members}   PagingDelay=1    PriorityPage=false    RingsPerMember=10    PriorityPageAudioPath=2    MakeExtensionPrivate=False
    ${PGExtension}=    using ${bossPortal} I want to create paging groups using ${pagingGroups}
    Given I want to make a two party call between ${phone3} and ${phone1} using ${loudSpeaker}
    Then answer the call on ${phone1} using ${loudSpeaker}
    Then verify audio path between ${phone1} and ${phone3}
    Then on ${phone4} dial number ${PGExtension}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then verify the led state of ${line2} as ${blink} on ${phone1}
    Then I want to press line key ${programKey2} on phone ${phone1}
    Then on ${phone1} verify display message ${PGExtension}
    Then on ${phone2} verify display message ${PGExtension}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then disconnect the call from ${phone3}
    Then disconnect the call from ${phone4}
    [Teardown]    Paging Group Custom Teardown

557944: Outbound call during Priority Page
    [Tags]    Owner:Ram    Reviewer:    PagingGroup
    [Setup]    Paging Group Custom Setup
    @{members}   Create List      ${phone1}    ${phone2}
    &{pagingGroups} =  Create Dictionary    PagingGroupName=HCL   PageListName=HCL    GroupMembers=${members}   PagingDelay=1    PriorityPage=true    RingsPerMember=10    PriorityPageAudioPath=2    MakeExtensionPrivate=False
    ${PGExtension}=    using ${bossPortal} I want to create paging groups using ${pagingGroups}
    Given on ${phone3} dial number ${PGExtension}
    Then on ${phone1} wait for 3 seconds
    Then on ${phone1} verify display message ${PGExtension}
    Then on ${phone2} verify display message ${PGExtension}
    Then I want to press line key ${programKey2} on phone ${phone1}
    Then on ${phone1} verify display message >
    Then verify the led state of ${line1} as ${off} on ${phone1}
    Then verify the led state of ${line2} as ${on} on ${phone1}
    Then disconnect the call from ${phone1}
    Then disconnect the call from ${phone3}
    [Teardown]    Paging Group Custom Teardown

557957: TC005 Not selecting priority paging Parameter
    [Tags]    Owner:Ram    Reviewer:    PagingGroup
    [Setup]    Paging Group Custom Setup
    @{members}   Create List      ${phone1}    ${phone2}
    &{pagingGroups} =  Create Dictionary    PagingGroupName=HCL   PageListName=HCL    GroupMembers=${members}   PagingDelay=1    PriorityPage=false    RingsPerMember=10    PriorityPageAudioPath=2    MakeExtensionPrivate=False
    ${PGExtension}=    using ${bossPortal} I want to create paging groups using ${pagingGroups}
    Given I want to make a two party call between ${phone3} and ${phone1} using ${loudSpeaker}
    Then Answer the call on ${phone1} using ${loudSpeaker}
    Then verify audio path between ${phone1} and ${phone3}
    Then on ${phone4} dial number ${PGExtension}
    Then on ${phone2} wait for 3 seconds
    Then on ${phone2} verify display message ${PGExtension}
    Then verify the led state of ${line1} as ${on} on ${phone2}
    Then on ${phone1} verify display message ${PGExtension}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then verify the led state of ${line2} as ${blink} on ${phone1}
    Then disconnect the call from ${phone3}
    Then disconnect the call from ${phone4}
    Then disconnect the call from ${phone1}
    [Teardown]    Paging Group Custom Teardown

557958: TC006 Enable Make extension private
    [Tags]    Owner:Ram    Reviewer:    PagingGroup
    [Setup]    Paging Group Custom Setup
    @{members}   Create List      ${phone1}    ${phone2}
    &{pagingGroups} =  Create Dictionary    PagingGroupName=HCL   PageListName=HCL    GroupMembers=${members}   PagingDelay=1    PriorityPage=true    RingsPerMember=10    PriorityPageAudioPath=2    MakeExtensionPrivate=True
    ${PGExtension}=    using ${bossPortal} I want to create paging groups using ${pagingGroups}
    Given on ${phone3} dial number ${PGExtension}
    Then on ${phone1} wait for 3 seconds
    Then I want to verify on ${phone1} negative display message ${PGExtension}
    Then I want to verify on ${phone2} negative display message ${PGExtension}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then verify the led state of ${line1} as ${on} on ${phone2}
    Then disconnect the call from ${phone3}
    [Teardown]    Paging Group Custom Teardown

557780: TC007 Top-Down Pattern in HG members
    [Tags]    Owner:Ram    Reviewer:    HG
    [Setup]    Hunt Group Custom Setup
    @{members}   Create List      ${phone2}    ${phone3}
    &{huntGroupDetails} =  Create Dictionary    BackupExtension=${phone4}    GroupMembers=${members}   GroupName=HG_Ram1   IncludeInSystem=True    MakeExtnPrivate=False    HuntPattern=1    RingsPerMember=3    NoAnswerRings=4    CallMemberWhenForwarding=True    SkipMemberOnCall=True    CallStackFull=${EMPTY}    NoAnswer=${EMPTY}
    ${HGExtension} =     using ${bossPortal} I want to create hunt group user extension with ${huntGroupDetails}
    Given on ${phone1} dial number ${HGExtension}
    Then on ${phone1} press the softkey ${dial} in DialingState
    Then on ${phone2} verify display message ${huntGroupDetails['GroupName']}
    Then on ${phone3} wait for 10 seconds
    Then on ${phone3} verify display message ${huntGroupDetails['GroupName']}
    Then disconnect the call from ${phone1}
    [Teardown]    Hunt Group Custom Teardown

557781: TC008 Simultaneous Pattern in HG members
    [Tags]    Owner:Ram    Reviewer:    HG
    [Setup]    Hunt Group Custom Setup
    @{members}   Create List      ${phone2}    ${phone3}
    &{huntGroupDetails} =  Create Dictionary    BackupExtension=${phone4}    GroupMembers=${members}   GroupName=HG_Ram   IncludeInSystem=True    MakeExtnPrivate=False    HuntPattern=4    RingsPerMember=3    NoAnswerRings=4    CallMemberWhenForwarding=True    SkipMemberOnCall=True    CallStackFull=${EMPTY}    NoAnswer=${EMPTY}
    ${HGExtension} =     using ${bossPortal} I want to create hunt group user extension with ${huntGroupDetails}
    Given on ${phone1} dial number ${HGExtension}
    Then on ${phone1} press the softkey ${dial} in DialingState
    Then on ${phone2} verify display message ${huntGroupDetails['GroupName']}
    Then on ${phone3} verify display message ${huntGroupDetails['GroupName']}
    Then disconnect the call from ${phone1}
    [Teardown]    Hunt Group Custom Teardown

557806: TC036 Transfering a HG call to another HG
    [Tags]    Owner:Ram    Reviewer:    HG
    [Setup]    Hunt Group Custom Setup
    @{members}   Create List      ${phone1}    ${phone2}
    &{huntGroupDetails} =  Create Dictionary    BackupExtension=${phone4}    GroupMembers=${members}   GroupName=HG_Ram   IncludeInSystem=True    MakeExtnPrivate=False    HuntPattern=4    RingsPerMember=3    NoAnswerRings=4    CallMemberWhenForwarding=True    SkipMemberOnCall=True    CallStackFull=${EMPTY}    NoAnswer=${EMPTY}
    ${HGExtension} =     using ${bossPortal} I want to create hunt group user extension with ${huntGroupDetails}
    @{members}   Create List      ${phone4}    ${phone5}
    &{huntGroupDetails1} =  Create Dictionary    BackupExtension=${phone4}    GroupMembers=${members}   GroupName=HG_Ram1   IncludeInSystem=True    MakeExtnPrivate=False    HuntPattern=4    RingsPerMember=3    NoAnswerRings=4    CallMemberWhenForwarding=True    SkipMemberOnCall=True    CallStackFull=${EMPTY}    NoAnswer=${EMPTY}
    ${HGExtension1} =     using ${bossPortal} I want to create hunt group user extension with ${huntGroupDetails1}
    Given on ${phone3} dial number ${HGExtension}
    Then on ${phone3} press the softkey ${dial} in DialingState
    Then on ${phone1} verify display message ${huntGroupDetails['GroupName']}
    Then on ${phone2} verify display message ${huntGroupDetails['GroupName']}
    Then answer the call on ${phone1} using ${loudSpeaker}
    Then on ${phone1} press the softkey ${transfer} in AnswerState
    Then on ${phone1} dial number ${HGExtension1}
    Then on ${phone1} wait for 3 seconds
    Then on ${phone4} verify display message ${huntGroupDetails1['GroupName']}
    Then on ${phone5} verify display message ${huntGroupDetails1['GroupName']}
    Then disconnect the call from ${phone3}
    [Teardown]    Hunt Group Custom Teardown

559830:XMON, CID Always - held conference on target
    [Tags]    Owner:Ram    Reviewer:    Xmon
    &{extensionDetails} =  Create Dictionary  ring_delay=0   show_caller_id=always    no_connected=dial_number    with_connected=unused    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 4 with ExtensionValue
    Then On ${phone1} verify display message ${displayMessage['monitorExtn']}
    Then I want to make a two party call between ${phone2} and ${phone3} using ${loudSpeaker}
    Then answer the call on ${phone3} using ${loudSpeaker}
    Then I want to make a conference call between ${phone2},${phone3} and ${phone4} using ${directConference}
    Then Conference call audio verify between ${phone2} ${phone3} and ${phone4}
    Then press hardkey as ${holdState} on ${phone2}
    Then verify the led state of ${line1} as ${blink} on ${phone2}
    Then verify the led state of ${line5} as ${on} on ${phone1}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then verify the led state of ${line5} as ${blink} on ${phone1}
    Then verify the led state of ${line2} as ${blink} on ${phone2}
    Then disconnect the call from ${phone1}
    Then disconnect the call from ${phone3}
    Then disconnect the call from ${phone4}

560071: User in paging group dials paging extension
    [Tags]    Owner:Ram    Reviewer:    PagingGroup
    [Setup]    Paging Group Custom Setup
    @{members}   Create List      ${phone1}    ${phone2}    ${phone3}
    &{pagingGroups} =  Create Dictionary    PagingGroupName=HCL   PageListName=HCL    GroupMembers=${members}   PagingDelay=1    PriorityPage=true    RingsPerMember=10    PriorityPageAudioPath=2    MakeExtensionPrivate=False
    ${PGExtension}=    using ${bossPortal} I want to create paging groups using ${pagingGroups}
    Given on ${phone1} dial number ${PGExtension}
    Then on ${phone2} wait for 3 seconds
    Then on ${phone2} verify display message ${PGExtension}
    Then on ${phone3} verify display message ${PGExtension}
    Then On ${phone1} verify the softkeys in ${talk}
    Then disconnect the call from ${phone1}
    [Teardown]    Paging Group Custom Teardown

558489: Enter digits to dial valid extension, then lift handset
    [Tags]    Owner:Ram    Reviewer:    DigitsDelay    notApplicableForMiCloud
    Given using ${bossPortal} I want to change Delay after collecting digits value to 3000
    Then on ${phone1} enter number ${phone2}
    Then press hardkey as ${offHook} on ${phone1}
    Then verify the caller id on ${phone1} and ${phone2} display
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then verify the led state of speaker as ${off} on ${phone1}
    Then verify audio path between ${phone1} and ${phone2}
    And disconnect the call from ${phone2}
    [Teardown]    Telephony Options Custom Teardown


557127: Edit Delay after collecting digits.enter (star67) with valid digits (internal or external)
    [Tags]    Owner:Ram    Reviewer:    DigitDelay    notApplicableForMiCloud
    Given using ${bossPortal} I want to change Delay after collecting digits value to 2000
    Then I want to use fac ${privateCall} on ${phone1} to ${phone2}
    Then On ${phone2} verify display message ${callerId_blocked}
    Then disconnect the call from ${phone1}
    [Teardown]    Telephony Options Custom Teardown

560079:Priority Page during active call
    [Tags]    Owner:Ram    Reviewer:    PagingGroup
    [Setup]    Paging Group Custom Setup
    @{members}   Create List      ${phone1}    ${phone2}
    &{pagingGroups} =  Create Dictionary    PagingGroupName=HCL   PageListName=HCL    GroupMembers=${members}   PagingDelay=1    PriorityPage=true    RingsPerMember=10    PriorityPageAudioPath=2    MakeExtensionPrivate=False
    ${PGExtension}=    using ${bossPortal} I want to create paging groups using ${pagingGroups}
    Given I want to make a two party call between ${phone1} and ${phone3} using ${loudSpeaker}
    Then answer the call on ${phone3} using ${loudSpeaker}
    Then verify audio path between ${phone1} and ${phone3}
    Then on ${phone4} dial number ${PGExtension}
    Then on ${phone1} wait for 3 seconds
    Then on ${phone1} verify display message ${PGExtension}
    Then on ${phone2} verify display message ${PGExtension}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then verify the led state of ${line2} as ${on} on ${phone1}
    Then disconnect the call from ${phone4}
    Then verify audio path between ${phone1} and ${phone3}
    Then disconnect the call from ${phone3}
    [Teardown]     Paging Group Custom Teardown

559791: XMon - Active+Held
    [Tags]    Owner:Ram    Reviewer:    Xmon
    &{extensionDetails} =  Create Dictionary  ring_delay=1   show_caller_id=only_when_ringing    no_connected=unused    with_connected=unused    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 4 with ExtensionValue
    Then On ${phone1} verify display message ${displayMessage['monitorExtn']}
    Then verify the led state of ${line5} as ${off} on ${phone1}
    Then I want to make a two party call between ${phone2} and ${phone3} using ${loudSpeaker}
    Then answer the call on ${phone3} using ${loudSpeaker}
    Then Verify audio path between ${phone2} and ${phone3}
    Then verify the led state of ${line5} as ${on} on ${phone1}
    Then I want to make a two party call between ${phone4} and ${phone2} using ${loudSpeaker}
    Then answer the call on ${phone2} using ${line2}
    Then Verify audio path between ${phone4} and ${phone2}
    Then verify the led state of ${line5} as ${blink} on ${phone1}
    Then disconnect the call from ${phone4}
    Then disconnect the call from ${phone3}

559971: Hang up displays when XMON progbutton is pressed
    [Tags]    Owner:Ram    Reviewer:    Xmon
    &{extensionDetails} =  Create Dictionary  ring_delay=1   show_caller_id=only_when_ringing    no_connected=dial_number    with_connected=unused    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 4 with ExtensionValue
    Then On ${phone1} verify display message ${displayMessage['monitorExtn']}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then On ${phone1} verify display message ${drop}
    Then disconnect the call from ${phone1}


557135:Edit Delay after collecting digits. Press #
   [Tags]    Owner:Ram    Reviewer:    DigitDelay      notApplicableForMiCloud
    Given using ${bossPortal} I want to change Delay after collecting digits value to 2000
    Then on ${phone1} dial number #
    Then On ${phone1} verify display message ${voiceMailLogin}
    Then disconnect the call from ${phone1}
    [Teardown]    Telephony Options Custom Teardown

557136: Edit Delay after collecting digits. press call appearance. enter valid digits (internal or external)
    [Tags]    Owner:Ram    Reviewer:    DigitDelay    notApplicableForMiCloud
    Given using ${bossPortal} I want to change Delay after collecting digits value to 2000
    Then press hardkey as ${line1} on ${phone1}
    Then on ${phone1} enter number ${phone2}
    Then verify ringing state on ${phone1} and ${phone2}
    Then disconnect the call from ${phone1}
    [Teardown]    Telephony Options Custom Teardown

558099: Silent Monitor with permissions, target idle
    [Tags]    Owner:Ram    Reviewer:    SilentMonitorEnabled      notApplicableForMiCloud
    &{COSDetails} =  Create Dictionary    Name=${fullyFeatured}    AllowSilentMonitorInitiation=True
    Given using ${bossPortal} I want to change telephony features values using ${COSDetails}
    Then I want to make a two party call between ${phone2} and ${phone3} using ${loudSpeaker}
    Then answer the call on ${phone3} using ${loudSpeaker}
    Then on ${phone1} verify the softkeys in ${idle}
    Then press hardkey as ${offHook} on ${phone1}
    Then I want to use fac Silentmonitor on ${phone1} to ${phone2}
    Then on ${phone1} wait for 5 seconds
    Then On ${phone1} verify display message ${silentMonitor}
    And disconnect the call from ${phone2}
    [Teardown]    CoS Features Custom Teardown

558549: Display Dialing in the focused session window when entered a digit On Hook
    [Tags]    Owner:Ram    Reviewer:    dial    notApplicableForMiCloud
    Given using ${bossPortal} I want to change Delay after collecting digits value to 7000
    Then On ${phone1} dial partial number of ${phone2} with firstDigit
    Then verify ringing state on ${phone1} and ${phone2}
    Then disconnect the call from ${phone1}
    [Teardown]    Telephony Options Custom Teardown

558012: uncheck allow pickup and press pickup
    [Tags]    Owner:Ram    Reviewer:    CallPickupDisabled
    &{COSDetails} =  Create Dictionary    Name=${fullyFeatured}   AllowCallPickup=False
    Given using ${bossPortal} I want to change telephony features values using ${COSDetails}
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then I want to verify on ${phone1} negative display message ${pickUp}
    [Teardown]    CoS Features Custom Teardown

558013: uncheck allow pickup and press unpark
    [Tags]    Owner:Ram    Reviewer:    CallPickupDisabled
    &{COSDetails} =  Create Dictionary    Name=${fullyFeatured}    AllowCallPickup=False
    Given using ${bossPortal} I want to change telephony features values using ${COSDetails}
    Then on ${phone1} press ${softKey} ${bottomKey2} for 1 times
    Then I want to verify on ${phone1} negative display message ${unPark}
    [Teardown]    CoS Features Custom Teardown

561076: Call History: CoS is allowed initiation
    [Tags]    Owner:Ram    Reviewer:    IntercomEnabled      notApplicableForMiCloud
    &{COSDetails} =  Create Dictionary    Name=${fullyFeatured}   AllowIntercomInitiation=True
    Given using ${bossPortal} I want to change telephony features values using ${COSDetails}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${line1}
    Then disconnect the call from ${phone2}
    Then Press the call history button on ${phone1} and folder ${missed} and ${details}
    Then On ${phone1} verify display message ${intercom}
    [Teardown]    CoS Features Custom Teardown

559972: Hang up not displayed when XMON call target is answered
    [Tags]    Owner:Ram    Reviewer:    Xmon
    &{extensionDetails} =  Create Dictionary  ring_delay=1   show_caller_id=only_when_ringing    no_connected=dial_number    with_connected=unused    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 4 with ExtensionValue
    Then On ${phone1} verify display message ${displayMessage['monitorExtn']}
    Then I want to make a two party call between ${phone3} and ${phone2} using ${loudSpeaker}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then I want to verify on ${phone1} negative display message ${drop}
    Then I want to make a two party call between ${phone3} and ${phone1} using ${line2}
    Then answer the call on ${phone1} using ${loudSpeaker}
    Then On ${phone1} verify display message ${drop}
    Then I want to make a two party call between ${phone2} and ${phone4} using ${line2}
    Then answer the call on ${phone4} using ${loudSpeaker}
    Then On ${phone1} verify display message ${drop}
    Then disconnect the call from ${phone4}
    Then disconnect the call from ${phone1}
    Then on ${phone2} press ${Softkey} ${bottomKey1} for 2 times
    Then disconnect the call from ${phone1}


559850: XMON, CID Only When Ringing - held conference on target
    [Tags]    Owner:Ram    Reviewer:    Xmon
    &{extensionDetails} =  Create Dictionary  ring_delay=0   show_caller_id=only_when_ringing    no_connected=unused    with_connected=unused    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 4 with ExtensionValue
    Then On ${phone1} verify display message ${displayMessage['monitorExtn']}
    Then I want to make a two party call between ${phone2} and ${phone3} using ${loudSpeaker}
    Then answer the call on ${phone3} using ${loudSpeaker}
    Then I want to make a conference call between ${phone2},${phone3} and ${phone4} using ${directConference}
    Then Conference call audio verify between ${phone2} ${phone3} and ${phone4}
    Then press hardkey as ${holdState} on ${phone2}
    Then verify the led state of ${line1} as ${blink} on ${phone2}
    Then verify the led state of ${line5} as ${on} on ${phone1}
    Then on ${phone1} press ${softKey} ${bottomKey2} for 1 times
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then I want to verify on ${phone1} negative display message ${unpark}
    Then disconnect the call from ${phone3}
    Then disconnect the call from ${phone4}


562010: Silent monitor with *17
    [Tags]    Owner:Ram    Reviewer:    SilentMonitor
    &{COSDetails} =  Create Dictionary    Name=${fullyFeatured}   AllowSilentMonitorInitiation=True    IntercomAccept=1
    Given using ${bossPortal} I want to change telephony features values using ${COSDetails}
    Then I want to make a two party call between ${phone2} and ${phone3} using ${loudSpeaker}
    Then answer the call on ${phone3} using ${loudSpeaker}
    Then I want to use fac Silentmonitor on ${phone1} to ${phone2}
    Then On ${phone1} verify display message ${silentMonitor}
    Then verify one way audio from ${phone2} to ${phone1}
    Then verify one way audio from ${phone3} to ${phone1}
    Then verify audio path between ${phone2} and ${phone3}
    Then disconnect the call from ${phone2}
    [Teardown]    CoS Features Custom Teardown

559882: CallerID - When ringing - DUT dialing state - A receives inbound call
    [Tags]    Owner:Ram    Reviewer:    Call    notApplicableForMiCloud
    Given using ${bossPortal} I want to change Delay after collecting digits value to 10000
    Then On ${phone1} dial partial number of ${phone2} with ${firsttwo}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudSpeaker}
    Then verify the caller id on ${phone2} and ${phone1} display
    Then disconnect the call from ${phone2}
    [Teardown]    Telephony Options Custom Teardown

562011:Silent Coach with *22
    [Tags]    Owner:Ram    Reviewer:    SilentCoach
    &{COSDetails} =  Create Dictionary    Name=${fullyFeatured}   AllowSilentMonitorInitiation=True    SilentMonitorAccept=1
    Given using ${bossPortal} I want to change telephony features values using ${COSDetails}
    Then I want to make a two party call between ${phone2} and ${phone3} using ${loudSpeaker}
    Then answer the call on ${phone3} using ${loudSpeaker}
    Then I want to use fac Silentcoach on ${phone1} to ${phone2}
    Then On ${phone1} verify display message ${silentCoach}
    Then verify one way audio from ${phone3} to ${phone1}
    Then verify audio path between ${phone1} and ${phone2}
    Then verify audio path between ${phone2} and ${phone3}
    Then disconnect the call from ${phone3}
    [Teardown]    CoS Features Custom Teardown

559306: TC32: A calls Boss, B intercoms Admin
    [Tags]    Owner:Ram    Reviewer:    SCA
    [Setup]    Telephony Feature Custom Setup
    &{telephonydetails} =  Create Dictionary    sca_enabled=True
    ${scaExtn} =  using ${bossPortal} on ${phone2} I want to enable SCA using ${telephonydetails}
    &{BCAdetails} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=4    function=Bridge Call Appearance    label=BCA    target_extension=${scaExtn}
    Given using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails}
    Then on ${phone3} dial number ${scaExtn}
    Then on ${phone3} wait for 5 seconds
    Then verify the led state of ${line1} as ${blink} on ${phone2}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then I want to use fac Intercom on ${phone4} to ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then verify audio path between ${phone1} and ${phone3}
    Then disconnect the call from ${phone3}
    Then disconnect the call from ${phone4}
    [Teardown]    Telephony Feature Custom Teardown

558682: TC010: BCA 2 incoming calls
    [Tags]    Owner:Ram    Reviewer:    BCA
    [Setup]    bca custom setup
    &{createBCAExtension1} =  Create Dictionary    name=bca1   backupExtn=${phone3}    switch=2    callStackDepth=4
    ${bcaExtn}=    using ${bossPortal} I want to create Bridge Call Appearance extension using ${createBCAExtension1}
    &{BCAdetails1} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=1    function=Bridge Call Appearance    label=BCA1    target_extension=${bcaExtn}    CallStackPosition=1    SecondaryType=Dial Tone
    &{BCAdetails2} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=2    function=Bridge Call Appearance    label=BCA2    target_extension=${bcaExtn}    CallStackPosition=2    SecondaryType=Dial Tone
    Given using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails1}
    Then using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails2}
    Then on ${phone2} dial number ${bcaExtn}
    Then on ${phone2} press the softkey ${dial} in dialingstate
    Then on ${phone3} dial number ${bcaExtn}
    Then on ${phone3} press the softkey ${dial} in dialingstate
    Then I want to press line key ${programKey2} on phone ${phone1}
    Then I want to press line key ${programKey3} on phone ${phone1}
    Then Verify extension ${number} of ${phone3} on ${phone1}
    Then I want to verify on ${phone2} negative display message ${transfer}
    Then verify the led state of ${line2} as ${blink} on ${phone1}
    Then verify the led state of ${line3} as ${on} on ${phone1}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}
    [Teardown]    bca custom teardown

559038: Boss conf A B and C, Boss holds, Admin call D on own line, joins with conf button
    [Tags]    Owner:Ram    Reviewer:    SCA
    [Setup]    Telephony Feature Custom Setup
    &{telephonydetails} =  Create Dictionary    sca_enabled=True
    ${scaExtn} =  using ${bossPortal} on ${phone1} I want to enable SCA using ${telephonydetails}
    &{createBCAExtension1} =  Create Dictionary    extension=${scaExtn}    backupExtn=${phone1}    allowBridgeConferencing=true   defaultPrivacySettings=0
    ${bcaExtn}=    using ${bossPortal} I want to modify Bridge Call Appearance extension using ${createBCAExtension1}
    &{BCAdetails1} =  Create Dictionary    user_extension=${phone2}    button_box=0    soft_key=1    function=Bridge Call Appearance    label=BCA1    target_extension=${bcaExtn}    CallStackPosition=1    SecondaryType=Dial Tone
    Given using ${bossPortal} I want to create bca on ${phone2} using ${BCAdetails1}
    Then I want to make a two party call between ${phone1} and ${phone3} using ${loudSpeaker}
    Then answer the call on ${phone3} using ${loudSpeaker}
    Then I want to make a conference call between ${phone1},${phone3} and ${phone4} using ${directConference}
    Then Add the ${phone5} in 3 parties conference call on ${phone1}
    Then press hardkey as ${holdState} on ${phone1}
    Then I want to make a two party call between ${phone2} and ${phone6} using ${loudSpeaker}
    Then answer the call on ${phone6} using ${loudSpeaker}
    Then on ${phone2} press ${softKey} ${bottomKey2} for 1 times
    Then I want to press line key ${programKey2} on phone ${phone2}
    Then on ${phone1} wait for 5 seconds
    Then press hardkey as ${holdState} on ${phone1}
    Then Five party Conference call audio verification between ${phone1} ${phone3} ${phone4} ${phone5} and ${phone6}
    Then on ${phone1} press ${softKey} ${bottomKey3} for 1 times
    Then verify extension ${number} of ${phone6} on ${phone1}
    Then on ${phone2} verify the softkeys in ${idle}
    Then disconnect the call from ${phone1}
    Then disconnect the call from ${phone3}
    Then disconnect the call from ${phone4}
    Then disconnect the call from ${phone5}
    [Teardown]    Telephony Feature Custom Teardown

559228: MERGE BCA-SCA calls
    [Tags]    Owner:Ram    Reviewer:    SCA
    [Setup]    Telephony Feature Custom Setup
    &{telephonydetails} =  Create Dictionary    sca_enabled=True
    ${scaExtn} =  using ${bossPortal} on ${phone1} I want to enable SCA using ${telephonydetails}
    &{createBCAExtension1} =  Create Dictionary    extension=${scaExtn}    backupExtn=${phone1}    allowBridgeConferencing=true   defaultPrivacySettings=0
    ${bcaExtn}=    using ${bossPortal} I want to modify Bridge Call Appearance extension using ${createBCAExtension1}
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudSpeaker}
    Then Answer the call on ${phone2} using ${loudSpeaker}
    Then I want to make a conference call between ${phone1},${phone2} and ${phone3} using ${directConference}
    Then I want to make a two party call between ${phone4} and ${phone1} using ${loudSpeaker}
    Then Answer the call on ${phone1} using ${programKey2}
    Then on ${phone1} press ${softKey} ${bottomKey3} for 1 times
    Then I want to make a two party call between ${phone1} and ${phone5} using ${line2}
    Then answer the call on ${phone5} using ${loudSpeaker}
    Then on ${phone1} press ${softKey} ${bottomKey3} for 1 times
    Then on ${phone1} press ${softKey} ${bottomKey3} for 1 times
    Then verify extension ${number} of ${phone2} on ${phone1}
    Then verify extension ${number} of ${phone3} on ${phone1}
    Then verify extension ${number} of ${phone4} on ${phone1}
    Then verify extension ${number} of ${phone5} on ${phone1}
    Then disconnect the call from ${phone1}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}
    Then disconnect the call from ${phone4}
    [Teardown]    Telephony Feature Custom Teardown

733087: dial digits, backspace key appears- onhook
    [Tags]    Owner:Ram    Reviewer:    Dial    notApplicableForMiCloud
    Given using ${bossPortal} I want to change Delay after collecting digits value to 5000
    Then On ${phone1} dial partial number of ${phone2} with firstDigit
    Then disconnect the call from ${phone1}

    Given press hardkey as ${offHook} on ${phone1}
    Then On ${phone1} dial partial number of ${phone2} with firstDigit
    Then disconnect the call from ${phone1}

    Given press hardkey as ${handsFree} on ${phone1}
    Then On ${phone1} dial partial number of ${phone2} with firstDigit
    Then disconnect the call from ${phone1}
    [Teardown]       Telephony Options Custom Teardown

759699: Transfer a call by pressing Hotline Intercom button
    [Tags]    Owner:Ram    Reviewer:    Hotline
    &{hotlines}    create dictionary    ConnectedCallFunctionID=intercom    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${hotline} on ${phone1} using ${hotlines} and extension of ${phone3} and softkey position 4 with ExtensionValue
    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudSpeaker}
    Then answer the call on ${phone1} using ${loudSpeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then on ${phone1} press the softkey ${transfer} in AnswerState
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then verify the caller id on ${phone1} and ${phone3} display
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone1}


557145: TC03: send off screen call to VM
    [Tags]    Owner:Ram    Reviewer:    CallStackDepth
    [Setup]    Telephony Feature Custom Setup
    &{telephonydetails} =  Create Dictionary    CallStackDepth=1
    Given using ${bossPortal} on ${phone1} I want to change Call stack depth using ${telephonydetails}
    Then I want to make a two party call between ${phone1} and ${phone2} using ${loudSpeaker}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then I want to make a two party call between ${phone3} and ${phone1} using ${loudSpeaker}
    Then On ${phone3} verify display message ${displayVoiceMail}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}
    [Teardown]    Telephony Feature Custom Teardown

557143: TC01: answer off screen call
    [Tags]    Owner:Ram    Reviewer:    OffScreen
    Given using ${bossPortal} I program 1 Call Appearance button on ${phone1}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then i want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then verify extension ${number} of ${phone3} on ${phone1}
    Then on ${phone1} press the softkey ${answer} in ringingstate
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}
    And using ${bossPortal} I remove unused keys on ${phone1}

755783: Extension Assignment, Password Change Checkbox=False
    [Tags]    Owner:Ram    Reviewer:    AssignUser    notApplicableForMiCloud
    [Setup]    RUN KEYWORDS    Telephony Feature Custom Setup    Assign Extension Custom Setup
    &{telephonydetails} =  Create Dictionary    VM_pwd_change_on_next_login=False
    Given using ${bossPortal} on ${phone1} I want to uncheck voicemail password on next login using ${telephonydetails}
    Then On ${phone1} navigate to ${unassignUser} settings
    Then On ${phone1} verify display message ${available}
    Then Go to assign user on ${phone1} and ${phone1} in ${unAssigned}
    Then I want to verify on ${phone1} negative display message ${newVMpassword}
    Then verify extension ${number} of ${phone1} on ${phone1}
    [Teardown]    RUN KEYWORDS    Telephony Feature Custom Teardown    Assign Extension Custom Teardown

559700: Ringdown dialed call on handset
    [Tags]    Owner:Ram    Reviewer:    Ringdown
    [Setup]    Telephony Feature Custom Setup
    &{telephonydetails} =  Create Dictionary     EnableDelayedRingdown=True    RingdownNumber=${phone2}    RingdownDelay=5
    Given using ${bossPortal} on ${phone1} I want to modify telephone features using ${telephonydetails}
    Then press hardkey as ${handsFree} on ${phone1}
    Then on ${phone1} wait for 5 seconds
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then verify extension ${number} of ${phone2} on ${phone1}
    Then disconnect the call from ${phone1}
    [Teardown]    Telephony Feature Custom Teardown

754899: extension monitoring when call is active
    [Tags]    Owner:Ram    Reviewer:    XMON
    &{extensionDetails} =  Create Dictionary  ring_delay=1   show_caller_id=always    no_connected=unused    with_connected=transfer_consultative    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 2 with ExtensionValue
    Then On ${phone1} verify display message ${displayMessage['monitorExtn']}
    Then I want to make a two party call between ${phone3} and ${phone2} using ${offHook}
    Then On ${phone1} verify ${line3} icon state as MONITOR_EXT_RINGING
    Then answer the call on ${phone2} using ${offHook}
    Then On ${phone1} verify ${line3} icon state as MONITOR_EXT_BUSY
    And disconnect the call from ${phone2}

752560: Priority page during Whisper Page call
    [Tags]    Owner:Ram    Reviewer:    PagingGroup
    [setup]    Paging Group Custom Setup
    @{members}   Create List      ${phone1}
    &{pagingGroups} =  Create Dictionary    PagingGroupName=HCL_RK   PageListName=HCL_RK    GroupMembers=${members}    PriorityPage=true    RingsPerMember=2    PriorityPageAudioPath=1
    ${PGExtension}=    using ${bossPortal} I want to create paging groups using ${pagingGroups}
    Given using ${bossPortal} I program ${whisperPage} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then verify extension ${number} of ${phone2} on ${phone1}
    Then on ${phone3} dial number ${PGExtension}
    Then on ${phone2} verify the softkeys in ${idle}
    Then On ${phone1} verify display message ${PGExtension}
    Then disconnect the call from ${phone1}
    [Teardown]   paging group custom teardown

145263: phone (Intercom target) on active call during
    [Tags]    Owner:Ram    Reviewer:Aman    Intercom
    Given I want to make a two party call between ${phone2} and ${phone3} using ${loudSpeaker}
    Then Answer the call on ${phone3} using ${loudSpeaker}
    Then Verify audio path between ${phone2} and ${phone3}
    Then I want to use fac Intercom on ${phone1} to ${phone2}
    Then on ${phone1} wait for 5 seconds
    Then Verify ringing state on ${phone1} and ${phone2}
    Then verify the led state of ${line2} as ${blink} on ${phone2}
    Then on ${phone1} wait for 10 seconds
    Then Verify ringing state on ${phone1} and ${phone2}
    Then verify the led state of ${line2} as ${blink} on ${phone2}
    Then disconnect the call from ${phone3}
    And disconnect the call from ${phone1}

290857: Initialize Silent Coach when 69xx phone not in main screen
    [Tags]    Owner:Ram    Reviewer:Avishek    SilentCoach
    Given using ${bossPortal} I program ${silentCoach} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 1 with ExtensionValue
    Then On ${phone1} verify display message ${silentCoach}
    Then I want to make a two party call between ${phone2} and ${phone3} using ${loudspeaker}
    Then Answer the call on ${phone3} using ${loudSpeaker}
    Then Verify audio path between ${phone2} and ${phone3}
    Then Press hardkey as ${directory} on ${phone1}
    Then I want to press line key ${programKey2} on phone ${phone1}
    Then On ${phone1} verify display message ${directory}
    Then On ${phone1} verify display message ${quit}
    Then disconnect the call from ${phone3}

290862: Silent Coach fails when Agent is on hold
    [Tags]    Owner:Ram    Reviewer:Avishek    SilentCoach
    Given using ${bossPortal} I program ${silentCoach} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 1 with ExtensionValue
    Then On ${phone1} verify display message ${silentCoach}
    Then I want to make a two party call between ${phone2} and ${phone3} using ${loudspeaker}
    Then Answer the call on ${phone3} using ${loudSpeaker}
    Then Verify audio path between ${phone2} and ${phone3}
    Then Put the linekey ${line1} of ${phone2} on ${hold}
    Then I want to press line key ${programKey2} on phone ${phone1}
    Then on ${phone1} wait for 5 seconds
    Then On ${phone1} verify display message ${displayMessage['notPermit']}
    Then disconnect the call from ${phone3}

147446: Supervisor hangs up during a Silent Coach call
    [Tags]    Owner:Ram    Reviewer:Avishek    SilentCoach
    Given using ${bossPortal} I program ${silentMonitor} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 1 with ExtensionValue
    Then On ${phone1} verify display message ${displayMessage['silentMonitor']}
    Then I want to make a two party call between ${phone2} and ${phone3} using ${loudspeaker}
    Then Answer the call on ${phone3} using ${loudSpeaker}
    Then Verify audio path between ${phone2} and ${phone3}
    Then I want to press line key ${programKey2} on phone ${phone1}
    Then on ${phone1} wait for 10 seconds
    Then on ${phone1} press ${softKey} ${bottomKey2} for 1 times
    Then on ${phone1} wait for 3 seconds
    Then Verify audio path between ${phone1} and ${phone2}
    Then Verify audio path between ${phone2} and ${phone3}
    Then Verify one way audio from ${phone3} to ${phone1}
    Then Verify no audio path from ${phone1} to ${phone3}
    Then disconnect the call from ${phone1}
    Then Verify the Caller id on ${phone2} and ${phone3} display
    Then disconnect the call from ${phone3}

139887: Transition from Silent Monitor(17)Silent Coach(22) using Star Codes
    [Tags]    Owner:Ram    Reviewer:Avishek    SilentCoach
    Given I want to make a two party call between ${phone2} and ${phone3} using ${loudspeaker}
    Then Answer the call on ${phone3} using ${loudSpeaker}
    Then I want to use fac Silentmonitor on ${phone1} to ${phone2}
    Then on ${phone1} wait for 10 seconds
    Then on ${phone1} verify display message ${silentMonitor}
    Then on ${phone1} press ${softKey} ${bottomKey2} for 1 times
    Then on ${phone1} verify display message ${silentCoach}
    Then Verify audio path between ${phone2} and ${phone3}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Verify one way audio from ${phone3} to ${phone1}
    Then Verify no audio path from ${phone1} to ${phone3}
    Then I want to verify on ${phone2} negative display message ${transfer}
    Then I want to verify on ${phone2} negative display message ${conference}
    Then on ${phone1} press the softkey ${drop} in AnswerState
    Then On ${phone1} verify the softkeys in ${idle}
    And disconnect the call from ${phone2}

    Given I want to make a two party call between ${phone2} and ${phone3} using ${loudspeaker}
    Then Answer the call on ${phone3} using ${loudSpeaker}
    Then I want to use fac Silentcoach on ${phone1} to ${phone2}
    Then on ${phone1} wait for 10 seconds
    Then on ${phone1} verify display message ${silentCoach}
    Then on ${phone1} press ${softKey} ${bottomKey2} for 1 times
    Then on ${phone1} verify display message ${silentMonitor}
    Then Verify audio path between ${phone2} and ${phone3}
    Then Verify one way audio from ${phone2} to ${phone1}
    Then Verify one way audio from ${phone3} to ${phone1}
    Then Verify no audio path from ${phone1} to ${phone2}
    Then Verify no audio path from ${phone1} to ${phone3}
    Then on ${phone2} verify display message ${transfer}
    Then on ${phone2} verify display message ${conference}
    And disconnect the call from ${phone1}

560022: (connected call : Transfer Whisper)when monitoring phone is in held state and target extension is ringing
    [Tags]    Owner:Ram    Reviewer:    Xmon    first
    &{extensionDetails} =  Create Dictionary  ring_delay=none   show_caller_id=always    no_connected=unused    with_connected=transfer_whisper    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 4 with ExtensionValue
    Then On ${phone1} verify display message ${displayMessage['monitorExtn']}
	Then I want to make a two party call between ${phone3} and ${phone2} using ${loudSpeaker}
	Then I want to make a two party call between ${phone4} and ${phone1} using ${loudSpeaker}
    Then answer the call on ${phone1} using ${line1}
    Then press hardkey as ${holdState} on ${phone1}
	Then I want to press line key ${programKey5} on phone ${phone1}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then verify the led state of ${line5} as ${on} on ${phone1}
	Then Verify audio path between ${phone1} and ${phone3}
	Then On ${phone2} verify the softkeys in ${idle}
    Then disconnect the call from ${phone3}
    Then disconnect the call from ${phone4}


560024: (Connected call : Transfer Whisper)when monitoring phone is Ringing and target extension is on HELD call
	[Tags]    Owner:Ram    Reviewer:    first
    &{extensionDetails} =  Create Dictionary  ring_delay=none   show_caller_id=always    no_connected=unused    with_connected=transfer_Whisper    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 4 with ExtensionValue
    Then On ${phone1} verify display message ${displayMessage['monitorExtn']}
	Then I want to make a two party call between ${phone3} and ${phone2} using ${loudSpeaker}
	Then answer the call on ${phone2} using ${line1}
	Then Verify audio path between ${phone2} and ${phone3}
	Then Put the linekey ${line1} of ${phone3} on ${hold}
	Then I want to make a two party call between ${phone4} and ${phone1} using ${loudSpeaker}
	Then I want to press line key ${programKey5} on phone ${phone1}
    Then I want to press line key ${programKey5} on phone ${phone1}
	Then On ${phone1} verify display message ${phone3}
	Then verify the led state of ${line5} as ${on} on ${phone1}
	Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone4}


759696: Press Hotline Intercom button while on active call
    [Tags]    Owner:Ram    Reviewer:    Hotline    first
    &{hotlines}    create dictionary    ConnectedCallFunctionID=intercom    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${hotline} on ${phone1} using ${hotlines} and extension of ${phone3} and softkey position 4 with ExtensionValue
    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudSpeaker}
    Then answer the call on ${phone1} using ${loudSpeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then verify audio path between ${phone1} and ${phone3}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}

754900: extension monitoring in ringing state
     [Tags]    Owner:Ram    Reviewer:    transfer    first
     &{extensionDetails} =  Create Dictionary  ring_delay=1   show_caller_id=always    no_connected=unused    with_connected=transfer_consultative    account_name=Automation    part_name=SC1    button_box=0
     Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 2 with ExtensionValue
     Then On ${phone1} verify display message ${displayMessage['monitorExtn']}
     Then I want to make a two party call between ${phone3} and ${phone2} using ${offHook}
     Then On ${phone1} verify ${line3} icon state as ${xmonRinging}
     And disconnect the call from ${phone1}

754408: XMon - Idle monitoring states
    [Tags]    Owner:Ram    Reviewer:    XMON    first
    &{extensionDetails} =  Create Dictionary  ring_delay=1   show_caller_id=always    no_connected=unused    with_connected=transfer_consultative    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 2 with ExtensionValue
    Then On ${phone1} verify display message ${displayMessage['monitorExtn']}
    And On ${phone1} verify ${line3} icon state as ${xmonIdle}

    Given leave voicemail message from ${phone3} on ${phone2}
    Then On ${phone1} verify ${line3} icon state as ${xmonIdleMWI}
    And delete voicemail message on ${inbox} for ${phone2} using ${voicemailpassword}

    Given on ${phone2} navigate to ${availability} settings
    Then Modify call handler mode on ${phone2} to ${always} in ${doNotDisturb}
    Then on ${phone2} press ${softKey} ${bottomKey1} for 1 times
    Then on ${phone2} press the softkey ${quit} in SettingState
    Then On ${phone1} verify ${line3} icon state as ${xmonIdleDND}
    And Change the phone state to default state on ${phone2}
    [Teardown]    run keywords  Default Availability State   Generic Test Teardown

754898:Extension monitoring while dialing out
     [Tags]    Owner:Ram    Reviewer:    transfer    first
     &{extensionDetails} =  Create Dictionary  ring_delay=1   show_caller_id=always    no_connected=unused    with_connected=transfer_consultative    account_name=Automation    part_name=SC1    button_box=0
     Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 2 with ExtensionValue
     Then On ${phone1} verify display message ${displayMessage['monitorExtn']}
     Then I want to make a two party call between ${phone2} and ${phone3} using ${offHook}
     Then On ${phone1} verify ${line3} icon state as ${xmonBusy}
     And disconnect the call from ${phone2}

752544: Priority Page press Hold, Transfer or Conference key
    [Tags]    Owner:Ram    Reviewer:    PagingGroup    first
    [setup]    Paging Group Custom Setup
    @{members}   Create List      ${phone1}
    &{pagingGroups} =  Create Dictionary    PagingGroupName=HCL_RK   PageListName=HCL_RK    GroupMembers=${members}    PriorityPage=true    RingsPerMember=2    PriorityPageAudioPath=1
    ${PGExtension}=    using ${bossPortal} I want to create paging groups using ${pagingGroups}
    Given on ${phone2} dial number ${PGExtension}
    Then On ${phone1} verify display message ${PGExtension}
    Then press hardkey as ${holdstate} on ${phone1}
    Then on ${phone1} verify display message Hold not permitted on this call
    Then disconnect the call from ${phone2}
    [Teardown]   paging group custom teardown

753634: Admin gets call from caller A, Conferences in B, B leaves, Admin hangs up no prompt
    [Tags]    Owner:Ram    Reviewer:    BCA    first
    [Setup]    bca custom setup
    &{createBCAExtension} =  Create Dictionary    name=bca   backupExtn=${phone3}    switch=2    allowBridgeConferencing=true   defaultPrivacySettings=0
    ${bcaExtn}=    using ${bossPortal} I want to create Bridge Call Appearance extension using ${createBCAExtension}
    &{BCAdetails} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=3    function=Bridge Call Appearance    label=BCA    target_extension=${bcaExtn}    RingDelayBeforeAlert=0      show_caller_id_option=always    SecondaryType=Dial Tone
    Given using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails}
    Then I want to press line key ${programKey4} on phone ${phone1}
    Then on ${phone1} enter number ${phone2}
    Then on ${phone2} wait for 3 seconds
    Then answer the call on ${phone2} using ${offHook}
    Then on ${phone1} press ${softKey} ${bottomKey2} for 1 times
    Then on ${phone1} enter number ${phone3}
    Then on ${phone1} press ${softKey} ${bottomKey2} for 1 times
    Then answer the call on ${phone3} using ${offHook}
    Then on ${phone3} wait for 3 seconds
    Then disconnect the call from ${phone3}
    Then disconnect the call from ${phone1}
    Then On ${phone1} verify ${line4} icon state as BCA_IDLE
    [Teardown]     BCA Custom Teardown

759554: attempt barge in with no main screen focus
    [Tags]    Owner:Ram    Reviewer:    PKM_bargeIn    first
    &{COSDetails} =  Create Dictionary    Name=${fullyFeatured}   AllowBargeInInitiation=True    BargeInAccept=1
    Given using ${bossPortal} I want to change telephony features values using ${COSDetails}
    Then using ${bossPortal} I program ${silentMonitor} on ${phone1} using ${bossDetailsPKM} and extension of ${phone2} and softkey position 1 with ExtensionValue
    Then verify display message Silent Monit on PKM for ${phone1}
    Then I want to make a two party call between ${phone2} and ${phone3} using ${offHook}
    Then answer the call on ${phone3} using ${offHook}
    Then verify audio path between ${phone3} and ${phone2}
    Then press hardkey as ${directory} on ${phone1}
    Then on ${phone1} verify display message ${directory}
    Then I want to press pkm line key ${programKey2} on ${phone1}
    Then on ${phone1} verify display message ${directory}
    Then disconnect the call from ${phone2}
    Then using ${bossPortal} remove the function key on ${phone1} using ${bossDetailsPKM} and softkey position 1
    [Teardown]    CoS Features Custom Teardown

759670: phone Progbutton Transfer Intercom
    [Tags]    Owner:Ram    Reviewer:    PKM_TransferIntercom    first
    Given using ${bossPortal} I program ${transferIntercom} on ${phone1} using ${bossDetailsPKM} and extension of ${phone2} and softkey position 1 with ExtensionValue
    Then verify display message ${transferIntercom} on PKM for ${phone1}
    Then I want to make a two party call between ${phone3} and ${phone1} using ${offHook}
    Then answer the call on ${phone1} using ${offHook}
    Then I want to press pkm line key ${programKey2} on ${phone1}
    Then on ${phone1} verify display message ${drop}
    Then on ${phone1} verify display message ${transfer}
    Then verify the pkm led state of ${programKey2} as ${on} on ${phone1}
    Then verify extension ${number} of ${phone1} on ${phone2}
    Then on ${phone1} press ${softkey} ${bottomKey3} for 1 times
    Then on ${phone1} verify display message ${callTransferred}
    Then disconnect the call from ${phone3}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetailsPKM} and softkey position 1

145249: dial digits, cancel appears -offhook
    [Tags]    Owner:Ram    Reviewer:Avishek    Dial    first    notApplicableForMiCloud
    Given using ${bossPortal} I want to change Delay after collecting digits value to 5000
    Then Press hookMode ${offHook} on phone ${phone1}
    Then on ${phone1} dial number 1
    Then On ${phone1} verify display message ${cancel}
    Then on ${phone1} dial number 2
    Then On ${phone1} verify display message ${cancel}
    Then on ${phone1} dial number 3
    Then On ${phone1} verify display message ${cancel}
    Then Press hardkey as ${goodBye} on ${phone1}
    Then on ${phone1} wait for 3 seconds
    Given Press hardkey as ${handsFree} on ${phone1}
    Then on ${phone1} dial number 1
    Then On ${phone1} verify display message ${cancel}
    Then on ${phone1} dial number 2
    Then On ${phone1} verify display message ${cancel}
    Then on ${phone1} dial number 3
    Then On ${phone1} verify display message ${cancel}
    Then Press hookMode ${onHook} on phone ${phone1}
    [Teardown]       Telephony Options Custom Teardown

145270: phone dials all digits in the input box
    [Tags]    Owner: Ram    Reviewer: Avishek    dialInvalid    first    notApplicableForMiCloud
    Given using ${bossPortal} I want to change Delay after collecting digits value to 5000
    Then Press hookMode ${offHook} on phone ${phone1}
    Then on ${phone1} dial number ${invalidNumber}
    Then On ${phone1} verify display message ${backupAutoAttendant}
    And Press hookMode ${onHook} on phone ${phone1}
    [Teardown]       Telephony Options Custom Teardown

145230: back space key functionality
    [Tags]    Owner:Ram    Reviewer:Avishek    Dial    first    notApplicableForMiCloud
    Given using ${bossPortal} I want to change Delay after collecting digits value to 10000
    Then on ${phone1} dial number 1
    Then On ${phone1} verify display message ${backspace}
    Then on ${phone1} dial number 2
    Then On ${phone1} verify display message ${backspace}
    Then on ${phone1} dial number 3
    Then On ${phone1} verify display message ${backspace}
    Then on ${phone1} press the softkey ${backspace} in DialingState
    Then On ${phone1} verify display message ${backspace}
    Then on ${phone1} press the softkey ${backspace} in DialingState
    Then On ${phone1} verify display message ${backspace}
    Then on ${phone1} press the softkey ${backspace} in DialingState
    And On ${phone1} verify the softkeys in ${idle}
    [Teardown]       Telephony Options Custom Teardown

145243: dial key, invalid extension
    [Tags]    Owner:Ram    Reviewer:Manoj    Dial    first    notApplicableForMiCloud
    Given using ${bossPortal} I want to change Delay after collecting digits value to 7000
    Then Press hardkey as ${handsFree} on ${phone1}
    Then on ${phone1} dial number ${invalidExtension}
    Then on ${phone1} press the softkey ${dial} in DialingState
    Then On ${phone1} verify display message ${backupAutoAttendant}
    Then Press hardkey as ${goodBye} on ${phone1}
    Then on ${phone1} wait for 3 seconds
    Given Press hookMode ${OffHook} on phone ${phone1}
    Then on ${phone1} dial number ${invalidExtension}
    Then on ${phone1} press the softkey ${dial} in DialingState
    Then On ${phone1} verify display message ${backupAutoAttendant}
    And Press hookMode ${onHook} on phone ${phone1}
    [Teardown]       Telephony Options Custom Teardown

145330: Display Off Hook and Dialing in the focused session window when entered a digit Off Hook
    [Tags]    Owner:Ram    Reviewer:Avishek    Dial    first    notApplicableForMiCloud
    Given using ${bossPortal} I want to change Delay after collecting digits value to 7000
    Then Press hookMode ${offHook} on phone ${phone1}
    Then on ${phone1} dial number 1
    Then On ${phone1} verify display message ${one}
    And Press hookMode ${onHook} on phone ${phone1}
    [Teardown]       Telephony Options Custom Teardown

145755: Show Focus when Dialing
    [Tags]    Owner:Ram    Reviewer:    Call    first    notApplicableForMiCloud
    Given using ${bossPortal} I want to change Delay after collecting digits value to 5000
    Then Press hookMode ${offHook} on phone ${phone1}
    Then on ${phone1} verify display message >
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then on ${phone1} dial number 12
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudSpeaker}
    Then Verify the led state of ${line2} as ${blink} on ${phone1}
    Then answer the call on ${phone1} using ${programKey2}
    Then verify audio path between ${phone1} and ${phone2}
    Then on ${phone1} press ${softKey} ${programKey3} for 1 times
    Then on ${phone1} verify display message >
    Then Verify the led state of ${line3} as ${on} on ${phone1}
    Then disconnect the call from ${phone2}
    [Teardown]       Telephony Options Custom Teardown

145749: make call, onhook call view
    [Tags]    Owner:Ram    Reviewer:    Call    first    notApplicableForMiCloud
    Given using ${bossPortal} I want to change Delay after collecting digits value to 5000
    Then on ${phone1} dial number 1
    Then on ${phone1} verify display message ${dial}
    Then on ${phone1} verify display message ${backspace}
    Then on ${phone1} verify display message ${cancel}
    And Verify the led state of ${line1} as ${on} on ${phone1}
    [Teardown]       Telephony Options Custom Teardown

753874: BB424 - BCA, CID Only When Ringing - answer incoming call
    [Tags]    Owner:Ram    Reviewer:    BCA    first
    [Setup]    bca custom setup
    &{createBCAExtension} =  Create Dictionary    name=bca   backupExtn=${phone3}    switch=2    allowBridgeConferencing=true   defaultPrivacySettings=0
    ${bcaExtn}=    using ${bossPortal} I want to create Bridge Call Appearance extension using ${createBCAExtension}
    &{BCAdetails} =  Create Dictionary    user_extension=${phone1}    button_box=1    soft_key=3    function=Bridge Call Appearance    label=BCA    target_extension=${bcaExtn}    RingDelayBeforeAlert=0      show_caller_id_option=only_when_ringing    SecondaryType=Dial Tone
    Given using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails}
    Then on ${phone2} dial number ${bcaExtn}
    Then verify display message ${phone2} on PKM for ${phone1}
    Then on ${phone1} verify display message ${phone2}
    Then verify the pkm led state of ${programKey4} as ${blink} on ${phone1}
    Then verify ${line4} icon state as ${bcaIncomingCall} on pkm for ${phone1}
    Then I want to press PKM line key ${programKey4} on ${phone1}
    Then verify display message BCA on PKM for ${phone1}
    Then on ${phone1} verify display message ${phone2}
    Then verify the pkm led state of ${programKey4} as ${on} on ${phone1}
    And disconnect the call from ${phone1}
    [Teardown]     BCA Custom Teardown

753876: BB424 - BCA, CID Only When Ringing - incoming call answered by other user
    [Tags]    Owner:Ram    Reviewer:    BCA    first
    [Setup]    bca custom setup
    &{createBCAExtension} =  Create Dictionary    name=bca    backupExtn=${phone3}    switch=2    allowBridgeConferencing=false   defaultPrivacySettings=0
    ${bcaExtn}=    using ${bossPortal} I want to create Bridge Call Appearance extension using ${createBCAExtension}
    &{BCAdetails} =  Create Dictionary    user_extension=${phone1}    button_box=1    soft_key=3    function=Bridge Call Appearance    label=BCA    target_extension=${bcaExtn}    RingDelayBeforeAlert=0      show_caller_id_option=only_when_ringing    SecondaryType=Dial Tone
    &{BCAdetails1} =  Create Dictionary    user_extension=${phone3}    button_box=0    soft_key=3    function=Bridge Call Appearance    label=BCA    target_extension=${bcaExtn}    RingDelayBeforeAlert=0      show_caller_id_option=only_when_ringing    SecondaryType=Dial Tone
    Given using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails}
    Then using ${bossPortal} I want to create bca on ${phone3} using ${BCAdetails1}
    Then on ${phone2} dial number ${bcaExtn}
    Then verify display message ${phone2} on PKM for ${phone1}
    Then verify the pkm led state of ${programKey4} as ${blink} on ${phone1}
    Then verify ${line4} icon state as ${bcaIncomingCall} on pkm for ${phone1}
    Then Verify the led state of ${line4} as ${blink} on ${phone3}
    Then on ${phone3} verify display message ${phone2}
    Then I want to press line key ${programKey4} on phone ${phone3}
    Then verify the pkm led state of ${programKey4} as ${on} on ${phone1}
    Then verify display message BCA on PKM for ${phone1}
    Then on ${phone3} verify display message BCA
    Then I want to verify on ${phone1} negative display message ${phone3}
    And disconnect the call from ${phone2}
    [Teardown]     BCA Custom Teardown

753870: BB424 - BCA, CID Never - held BCA call
    [Tags]    Owner:Ram    Reviewer:    BCA    first
    [Setup]    bca custom setup
    &{createBCAExtension} =  Create Dictionary    name=bca    backupExtn=${phone3}    switch=2    allowBridgeConferencing=true   defaultPrivacySettings=0
    ${bcaExtn}=    using ${bossPortal} I want to create Bridge Call Appearance extension using ${createBCAExtension}
    &{BCAdetails} =  Create Dictionary    user_extension=${phone1}    button_box=1    soft_key=3    function=Bridge Call Appearance    label=BCA    target_extension=${bcaExtn}    RingDelayBeforeAlert=0      show_caller_id_option=never   SecondaryType=Dial Tone
    &{BCAdetails1} =  Create Dictionary    user_extension=${phone3}    button_box=0    soft_key=3    function=Bridge Call Appearance    label=BCA    target_extension=${bcaExtn}    RingDelayBeforeAlert=0      show_caller_id_option=never    SecondaryType=Dial Tone
    Given using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails}
    Then using ${bossPortal} I want to create bca on ${phone3} using ${BCAdetails1}
    Then on ${phone2} dial number ${bcaExtn}
    Then verify the pkm led state of ${programKey4} as ${blink} on ${phone1}
    Then I want to verify on ${phone1} negative display message ${phone2}
    Then I want to press line key ${programKey4} on phone ${phone3}
    Then press hardkey as ${holdState} on ${phone3}
    Then I want to verify on ${phone3} negative display message ${phone2}
    Then I want to press PKM line key ${programKey4} on ${phone1}
    Then verify audio path between ${phone1} and ${phone2}
    Then on ${phone1} verify display message ${phone2}
    Then verify the pkm led state of ${programKey4} as ${on} on ${phone1}
    And disconnect the call from ${phone2}
    [Teardown]     BCA Custom Teardown

753872: BB424 - BCA, CID Never - in-use state with BCA Conferencing enabled
    [Tags]    Owner:Ram    Reviewer:    BCA    secod
    [Setup]    bca custom setup
    &{createBCAExtension} =  Create Dictionary    name=bca    backupExtn=${phone3}    switch=2    allowBridgeConferencing=true   defaultPrivacySettings=0
    ${bcaExtn}=    using ${bossPortal} I want to create Bridge Call Appearance extension using ${createBCAExtension}
    &{BCAdetails} =  Create Dictionary    user_extension=${phone1}    button_box=1    soft_key=3    function=Bridge Call Appearance    label=BCA    target_extension=${bcaExtn}    RingDelayBeforeAlert=0      show_caller_id_option=never   SecondaryType=Dial Tone
    &{BCAdetails1} =  Create Dictionary    user_extension=${phone3}    button_box=0    soft_key=3    function=Bridge Call Appearance    label=BCA    target_extension=${bcaExtn}    RingDelayBeforeAlert=0      show_caller_id_option=never    SecondaryType=Dial Tone
    Given using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails}
    Then using ${bossPortal} I want to create bca on ${phone3} using ${BCAdetails1}
    Then on ${phone2} dial number ${bcaExtn}
    Then on ${phone2} press ${softKey} ${bottomKey1} for 1 times
    Then I want to press line key ${programKey4} on phone ${phone3}
    Then on ${phone3} PKM verify negative display message ${phone2}
    Then verify ${line4} icon state as bca Solid orange on pkm for ${phone1}
    Then on ${phone3} press the softkey ${lock} in AnswerState
    Then on ${phone3} PKM verify negative display message ${phone2}
    Then verify ${line4} icon state as bca Solid red on pkm for ${phone1}
    Then on ${phone3} press the softkey ${unlock} in AnswerState
    Then on ${phone3} PKM verify negative display message ${phone2}
    Then verify ${line4} icon state as bca Solid orange on pkm for ${phone1}
    Then I want to press PKM line key ${programKey4} on ${phone1}
    Then verify ${line4} icon state as ${bcaConferenceActive} on pkm for ${phone1}
    Then conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then on ${phone1} verify display message ${phone2}
    Then on ${phone1} verify display message ${phone3}
    Then disconnect the call from ${phone2}
    And disconnect the call from ${phone3}
    [Teardown]     BCA Custom Teardown


754823: Press Send Digits Over Call progbutton during an active call
    [Tags]    Owner:Ram    Reviewer:    SendDigitsOverCall    second
    &{sendDigits}=    Create Dictionary   digits=1234#    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${sendDigitsOverCall} on ${phone1} using ${sendDigits} and extension of ${phone2} and softkey position 4 with ExtensionValue
    Then leave voicemail message from ${phone2} on ${phone1}
    Then login into voicemailbox for ${phone1} using ${voicemailpassword}
    Then verify voicemail windows ${inbox} icons value as 1 on ${phone1}
    Then press hardkey as ${goodBye} on ${phone1}
    Then on ${phone1} dial number #
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} wait for 2 seconds
    Then on ${phone1} dial number 1
    Then disconnect the call from ${phone1}
    Then login into voicemailbox for ${phone1} using ${voicemailpassword}
    Then verify voicemail windows ${inbox} icons value as 0 on ${phone1}

759673: Press Transfer Whisper programmable
    [Tags]    Owner:Ram    Reviewer:    PKM    second
    &{COSDetails} =  Create Dictionary    Name=${fullyFeatured}   AllowIntercomInitiation=True    IntercomAccept=1
    Given using ${bossPortal} I want to change telephony features values using ${COSDetails}
    Then using ${bossPortal} I program ${transferWhisper} on ${phone1} using ${bossDetailsPKM} and extension of ${phone2} and softkey position 1 with ExtensionValue
    Then verify display message ${transferWhisper} on PKM for ${phone1}
    Then I want to make a two party call between ${phone3} and ${phone1} using ${offHook}
    Then answer the call on ${phone1} using ${offHook}
    Then I want to press pkm line key ${programKey2} on ${phone1}
    Then verify audio path between ${phone1} and ${phone3}
    Then on ${phone1} press ${softKey} ${bottomKey3} for 1 times
    Then on ${phone2} verify display message ${phone3}
    Then on ${phone1} verify display message ${pickUp}
    Then disconnect the call from ${phone3}
    Then using ${bossPortal} remove the function key on ${phone1} using ${bossDetailsPKM} and softkey position 1
    [Teardown]    CoS Features Custom Teardown

752709: phone dials *67 to Block Caller ID for the call
    [Tags]    Owner:Ram    Reviewer:    blockCallerID    second
    [Setup]    Telephony Feature Custom Setup
    &{telephonydetails} =  Create Dictionary     MakeExtensionPrivate=False
    Given using ${bossPortal} on ${phone1} I want to modify telephone features using ${telephonydetails}
    Then I want to use fac ${privateCall} on ${phone1} to ${phone3}
    Then on ${phone3} verify display message ${callerId_blocked}
    Then disconnect the call from ${phone1}

559105: Add programable buttons for SCA
    [Tags]    Owner:Ram    Reviewer:    SCA    second
    [Setup]    Telephony Feature Custom Setup
    &{telephonydetails} =  Create Dictionary    sca_enabled=True
    ${scaExtn} =  using ${bossPortal} on ${phone2} I want to enable SCA using ${telephonydetails}
    &{BCAdetails} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=1    function=Bridge Call Appearance    label=BCA    target_extension=${scaExtn}    CallStackPosition=1    SecondaryType=Dial Tone
    Given using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails}
    Then on ${phone3} dial number ${scaExtn}
    Then on ${phone3} press the softkey ${dial} in dialingstate
    Then verify the led state of ${line2} as ${blink} on ${phone1}
    Then I want to press line key ${programKey2} on phone ${phone1}
    Then verify audio path between ${phone1} and ${phone3}
    And disconnect the call from ${phone3}
    [Teardown]    Telephony Feature Custom Teardown

759997: TC018-Hold, Unhold, Mute, unmute
    [Tags]    Owner:Ram    Reviewer:    Hold/Mute    notApplicableForMiCloud
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

759998: TC019-Make inbound/outbound call
    [Tags]    Owner:Ram    Reviewer:    makeCall    latest
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
    [Tags]    Owner:Ram    Reviewer:    CallHistory/VM
    Given press hardkey as ${callersList} on ${phone1}
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

559324:MERGE Hotline call with other call
    [Tags]    Owner:SaurabhSharma    Reviewer    hotline    second
    &{hotlines}    CREATE DICTIONARY    ConnectedCallFunctionID=dial number    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${hotline} on ${phone1} using ${hotlines} and extension of ${phone2} and softkey position 4 with extensionValue
    Then on ${phone1} verify display message ${hotline}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then answer the call on ${phone2} using ${programKey1}
    Then Verify audio path between ${phone1} and ${phone2}
    Then i want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then On ${phone1} Wait for 2 seconds
    Then answer the call on ${phone1} using ${programKey1}
    Then Verify audio path between ${phone3} and ${phone1}
    Then on ${phone1} press the softkey ${merge} in ConferenceCallState
    Then verify extension ${number} of ${phone2} on ${phone1}
    Then verify extension ${number} of ${phone3} on ${phone1}
    Then disconnect the call from ${phone1}
    Then disconnect the call from ${phone3}
    And using ${bossPortal} I remove unused keys on ${phone1}

559322: HoldUnhold Hotline call
    [Tags]    Owner:SaurabhSharma    Reviewer    hotline_speeddial    second
    &{hotlines}    CREATE DICTIONARY    ConnectedCallFunctionID=dial number    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${hotline} on ${phone1} using ${hotlines} and extension of ${phone2} and softkey position 4 with extensionValue
    Given using ${bossPortal} I program ${hotline} on ${phone2} using ${hotlines} and extension of ${phone1} and softkey position 4 with extensionValue
    Then on ${phone1} verify display message ${hotline}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then answer the call on ${phone2} using ${programKey5}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Verify the led state of ${line5} as ${on} on ${phone1}
    Then Put the linekey ${line5} of ${phone1} on ${hold}
    Then Verify the led state of ${line5} as ${blink} on ${phone1}
    Then press hookmode ${hookOff} on phone ${phone1}
    Then Verify the led state of ${line5} as ${on} on ${phone1}
    Then Put the linekey ${line5} of ${phone2} on ${hold}
    Then Verify the led state of ${line5} as ${blink} on ${phone2}
    Then press hookmode ${hookOff} on phone ${phone2}
    Then Verify the led state of ${line5} as ${on} on ${phone2}
    Then Put the linekey ${line5} of ${phone1} on ${hold}
    Then Verify the led state of ${line5} as ${blink} on ${phone1}
    Then Put the linekey ${line5} of ${phone2} on ${hold}
    Then Verify the led state of ${line5} as ${blink} on ${phone2}
    Then press hookmode ${hookOff} on phone ${phone1}
    Then press hookmode ${hookOff} on phone ${phone2}
    Then disconnect the call from ${phone2}
    And using ${bossPortal} I remove unused keys on ${phone1}
    And using ${bossPortal} I remove unused keys on ${phone2}


559328 : Transfer, Conference, Park with Hotline call
   [Tags]    Owner:SaurabhSharma    Reviewer    hotline_speeddial    second
    &{hotlines}    CREATE DICTIONARY    ConnectedCallFunctionID=dial number    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${hotline} on ${phone1} using ${hotlines} and extension of ${phone2} and softkey position 4 with extensionValue
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then answer the call on ${phone2} using ${programKey1}
    Then On ${phone1} verify display message ${drop}
    Then disconnect the call from ${phone2}
    And using ${bossPortal} I remove unused keys on ${phone1}

560354: TC019 'transfer intercom' to received call
    [Tags]    Owner:Vikhyat    Reviewer:    second
    Given using ${bossPortal} I program ${transferIntercom} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['transferIntercom']}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudSpeaker}
    Then Answer the call on ${phone1} using ${loudSpeaker}
    Then Verify the led state of ${line5} as ${on} on ${phone1}
    Then Verify audio path between ${phone1} and ${phone2}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then Verify the led state of ${line2} as ${blink} on ${phone2}
    Then Verify ringing state on ${phone1} and ${phone2}
    Then Press hardkey as ${goodBye} on ${phone2}
    Then Put the linekey ${line1} of ${phone1} on ${unHold}
    And Disconnect the call from ${phone2}

556922: With partial digit entry, do not answer incoming call
    [Tags]    Owner:Vikhyat    Reviewer:    delayDigits    second    notApplicableForMiCloud
    Given using ${bossPortal} I want to change Delay after collecting digits value to 12000
    Then On ${phone1} dial partial number of ${phone2} with ${firstTwo}
    Then on ${phone2} enter number ${phone1}
    Then on ${phone2} press the softkey ${dial} in DialingState
    Then Verify the led state of ${line2} as ${blink} on ${phone1}
    Then On ${phone1} Wait for 20 seconds
    Then on ${phone2} verify display message ${displayVoiceMail}
    Then Press hardkey as ${goodBye} on ${phone2}
    And On ${phone1} verify the softkeys in ${idle}
    [Teardown]    Telephony Options Custom Teardown

559345: Configure XMon progbutton; call XMon from another phone
    [Tags]    Owner:Vikhyat    Reviewer:    Xmon    second
    &{extensionDetails} =  Create Dictionary  ring_delay=none   show_caller_id=never    no_connected=dial_number    with_connected=dial_number    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then I want to make a two party call between ${phone3} and ${phone2} using ${loudSpeaker}
    Then Verify the led state of ${line5} as ${blink} on ${phone1}
    Then on ${phone1} press ${hardKey} ${programKey5} for 2 times
    Then Verify the Caller id on ${phone1} and ${phone3} display
    Then Verify audio path between ${phone1} and ${phone3}
    And Disconnect the call from ${phone1}

559019: A,B,C on call, conference in BCA(Admin), BCA line 2 calls D, uses conference button to join.
    [Tags]    Owner:Vikhyat    Reviewer:    BCA    second
    [Setup]    BCA Custom Setup

    &{createBCAExtension1}=  Create Dictionary    name=bca_vk1   backupExtn=${phone3}    switch=2    callStackDepth=2    forwardAfter=2    callStackFull=${EMPTY}   noAnswer=${EMPTY}    outboundCallerID=${EMPTY}    allowBridgeConferencing=true   defaultPrivacySettings=0
    ${bcaExt1}=    using ${bossPortal} I want to create Bridge Call Appearance extension using ${createBCAExtension1}
    &{bcaDetails1}=  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=3    function=Bridge Call Appearance    label=${bca}    target_extension=${bcaExt1}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${EMPTY}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=${EMPTY}
    using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails1}

    &{createBCAExtension2}=  Create Dictionary    name=bca_vk2   backupExtn=${phone3}    switch=2    callStackDepth=2    forwardAfter=2    callStackFull=${EMPTY}   noAnswer=${EMPTY}    outboundCallerID=${EMPTY}    allowBridgeConferencing=true   defaultPrivacySettings=0
    ${bcaExt2}=    using ${bossPortal} I want to create Bridge Call Appearance extension using ${createBCAExtension2}
    &{bcaDetails2}=  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=4    function=Bridge Call Appearance    label=${bca}    target_extension=${bcaExt2}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${EMPTY}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=${EMPTY}
    using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails2}

    Given I want to make a two party call between ${phone2} and ${phone3} using ${offHook}
    Then Answer the call on ${phone3} using ${offHook}
    Then I want to make a conference call between ${phone2},${phone3} and ${phone4} using ${directConference}
    Then Conference call audio verify between ${phone2} ${phone3} and ${phone4}
    Then on ${phone3} press the softkey ${conference} in ConferenceCallState
    Then on ${phone3} dial number ${bcaExt1}
    Then verify the led state of ${line4} as ${blink} on ${phone1}
    Then Answer the call on ${phone1} using ${programKey4}
    Then On ${phone1} Wait for 5 seconds
    Then on ${phone3} press the softkey ${conference} in ConferenceCallState
    Then On ${phone1} Wait for 5 seconds
    Then Press hardkey as ${programKey5} on ${phone1}
    Then on ${phone1} enter number ${phone5}
    Then Verify the led state of ${line1} as ${blink} on ${phone5}
    Then Answer the call on ${phone5} using ${loudSpeaker}
    Then Verify audio path between ${phone1} and ${phone5}
    Then On ${phone1} press the softkey ${conference} in conferencecallstate
    Then Press hardkey as ${programKey4} on ${phone1}
    Then on ${phone5} verify display message ${conference}
    Then Five party Conference call audio verification between ${phone1} ${phone2} ${phone3} ${phone4} and ${phone5}
    Then Disconnect the call from ${phone1}
    Then Disconnect the call from ${phone2}
    Then Disconnect the call from ${phone3}
    Then Disconnect the call from ${phone4}
    And Disconnect the call from ${phone5}
    [Teardown]    BCA Custom Teardown

559054: Admin makes 2 way conf on SCA line1, Admin leaves, gets dialog, parks call, Admin joins 3rd caller in
    [Tags]    Owner:Vikhyat    Reviewer:    BCA    second
    [Setup]    BCA Custom Setup

    &{createBCAExtension}=  Create Dictionary    name=bca_vk1   backupExtn=${phone3}    switch=2    callStackDepth=1    forwardAfter=2    callStackFull=${EMPTY}   noAnswer=${EMPTY}    outboundCallerID=${EMPTY}    allowBridgeConferencing=true   defaultPrivacySettings=0
    ${bcaExt1}=    using ${bossPortal} I want to create Bridge Call Appearance extension using ${createBCAExtension}
    &{bcaDetails1}=  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=4    function=Bridge Call Appearance    label=${bca}    target_extension=${bcaExt1}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${EMPTY}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=${EMPTY}
    using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails1}

    Given I want to make a two party call between ${phone1} and ${phone3} using ${programKey5}
    Then Answer the call on ${phone3} using ${loudSpeaker}
    Then I want to make a conference call between ${phone1},${phone3} and ${phone4} using ${directConference}
    Then Conference call audio verify between ${phone1} ${phone3} and ${phone4}
    Then I want to make a two party call between ${phone5} and ${phone1} using ${loudSpeaker}
    Then Answer the call on ${phone1} using ${line1}
    Then On ${phone1} press the softkey ${conference} in answerstate
    Then Press hardkey as ${programKey5} on ${phone1}
    Then Verify the led state of ${line1} as ${off} on ${phone1}
    Then Four party Conference call audio verification between ${phone1} ${phone3} ${phone4} and ${phone5}
    Then Disconnect the call from ${phone1}
    Then Verify the led state of ${line5} as ${off} on ${phone1}
    Then Conference call audio verify between ${phone3} ${phone4} and ${phone5}
    Then Disconnect the call from ${phone3}
    And Disconnect the call from ${phone4}

    [Teardown]    BCA Custom Teardown

559385: ToVM from Boss phone
    [Tags]    Owner: Vikhyat    Reviewer:    SCA    second
    [Setup]    Telephony Feature Custom Setup
    &{telephonydetails}=  Create Dictionary    sca_enabled=True
    ${scaExtn} =  using ${bossPortal} on ${phone1} I want to enable SCA using ${telephonydetails}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${offHook}
    Then on ${phone1} press ${softKey} ${bottomKey2} for 1 times
    Then Verify the led state of ${line1} as ${off} on ${phone1}
    Then on ${phone2} verify display message ${displayVoiceMail}
    Then On ${phone2} Wait for 20 seconds
    Then Press hardkey as ${goodBye} on ${phone2}
    Then Login into voicemailBox for ${phone1} using ${voicemailPassword}
    Then Verify extension ${number} of ${phone2} on ${phone1}
    Then Press hardkey as ${goodBye} on ${phone1}

    &{telephonydetails}=  Create Dictionary    sca_enabled=False
    ${scaExtn} =  using ${bossPortal} on ${phone1} I want to disable SCA using ${telephonydetails}
    [Teardown]    Telephony Feature Custom Teardown

753998: ToVM from Boss phone
    [Tags]    Owner:Vikhyat    Reviewer:    SCA    second
    [Setup]    Telephony Feature Custom Setup
    &{telephonydetails}=  Create Dictionary    sca_enabled=True
    ${scaExtn} =  using ${bossPortal} on ${phone1} I want to enable SCA using ${telephonydetails}
    Given Delete voicemail message on ${inbox} for ${phone1} using ${voicemailPassword}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudSpeaker}
    Then on ${phone1} press ${softKey} ${bottomKey2} for 1 times
    Then Verify the led state of ${line1} as ${off} on ${phone1}
    Then on ${phone2} verify display message ${displayVoiceMail}
    Then On ${phone2} Wait for 20 seconds
    Then Press hardkey as ${goodBye} on ${phone2}
    Then Login into voicemailBox for ${phone1} using ${voicemailPassword}
    Then Verify extension ${number} of ${phone2} on ${phone1}
    And Press hardkey as ${goodBye} on ${phone1}

    &{telephonydetails}=  Create Dictionary    sca_enabled=False
    ${scaExtn} =  using ${bossPortal} on ${phone1} I want to disable SCA using ${telephonydetails}
    [Teardown]    Telephony Feature Custom Teardown


755797: User Options, Password Change Checkbox=False
    [Tags]    Owner:Vikhyat    Reviewer:    vmPasswordChange    second    notApplicableForMiCloud
    [Setup]    RUN KEYWORDS    Telephony Feature Custom Setup    Assign Extension Custom Setup
    &{telephonydetails} =  Create Dictionary    VM_pwd_change_on_next_login=False
    Given using ${bossPortal} on ${phone1} I want to uncheck voicemail password on next login using ${telephonydetails}
    Given On ${phone1} navigate to ${unassignUser} settings
    Then on ${phone1} Wait for 10 seconds
    Then On ${phone1} verify display message ${available}
    Then Go to assign user on ${phone1} and ${phone1} in ${unAssigned}
    Then On ${phone1} Wait for 10 seconds
    Then Verify extension ${number} of ${phone1} on ${phone1}
    Then Press hardkey as ${menu} on ${phone1}
    Then on ${phone1} dial number ${voicemailPassword}
    Then On ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then I want to verify on ${phone1} negative display message ${newVoiceMailPasswordDisplay}
    And Press hardkey as ${goodBye} on ${phone1}

    [Teardown]    RUN KEYWORDS    Telephony Feature Custom Teardown    Assign Extension Custom Teardown

755799: Visual Voicemail, Password Change Checkbox=False
    [Tags]    Owner:Vikhyat     Reviewer:    vmPasswordChange    second    notApplicableForMiCloud
    [Setup]    RUN KEYWORDS    Telephony Feature Custom Setup    Assign Extension Custom Setup
    &{telephonydetails} =  Create Dictionary    VM_pwd_change_on_next_login=False
    Given using ${bossPortal} on ${phone1} I want to uncheck voicemail password on next login using ${telephonydetails}
    Given On ${phone1} navigate to ${unassignUser} settings
    Then on ${phone1} Wait for 10 seconds
    Then On ${phone1} verify display message ${available}
    Then Go to assign user on ${phone1} and ${phone1} in ${unAssigned}
    Then On ${phone1} Wait for 10 seconds
    Then Verify extension ${number} of ${phone1} on ${phone1}
    Then Press hardkey as ${voiceMail} on ${phone1}
    Then On ${phone1} verify display message ${voiceMailLoginScreenDisplay}
    Then On ${phone1} dial number ${voiceMailPassword}
    Then On ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then On ${phone1} verify display message ${visualVoicemailScreen}
    And Press hardkey as ${goodBye} on ${phone1}

    [Teardown]    RUN KEYWORDS    Telephony Feature Custom Teardown    Assign Extension Custom Teardown

755800: Visual Voicemail, Password Change Checkbox=True
    [Tags]    Owner:Vikhyat    Reviewer:    vmPasswordChange    second    notApplicableForMiCloud
    [Setup]    RUN KEYWORDS    Telephony Feature Custom Setup    Assign Extension Custom Setup
    Given On ${phone1} navigate to ${unassignUser} settings
    Then on ${phone1} Wait for 10 seconds
    Then On ${phone1} verify display message ${available}
    Then Go to assign user on ${phone1} and ${phone1} in ${unAssigned}
    Then On ${phone1} Wait for 10 seconds
    Then Verify extension ${number} of ${phone1} on ${phone1}

    &{telephonydetails} =  Create Dictionary    VM_pwd_change_on_next_login=True
    Given using ${bossPortal} on ${phone1} I want to check voicemail password on next login using ${telephonydetails}
    Then Change voicemail password from ${voiceMailPassword} to ${newVoiceMailPassword} for ${phone1}
    Then Press hardkey as ${goodBye} on ${phone1}

#     changing the password back to default
    &{telephonydetails} =  Create Dictionary    VM_pwd_change_on_next_login=True
    Given using ${bossPortal} on ${phone1} I want to check voicemail password on next login using ${telephonydetails}
    Then Change voicemail password from ${newVoiceMailPassword} to ${voiceMailPassword} for ${phone1}
    And Press hardkey as ${goodBye} on ${phone1}

    [Teardown]    RUN KEYWORDS    Set Default Voicemail Password    Assign Extension Custom Teardown

752708: phone dials *18 for BusyOut Hunt Group
    [Tags]    Owner:Vikhyat    Reviewer:    huntgroup    second
    [Setup]    Hunt Group Custom Setup
    @{members}   Create List    ${phone2}
    &{huntGroupDetails} =  Create Dictionary    BackupExtension=${phone1}    GroupMembers=${members}   GroupName=HG_VK   IncludeInSystem=True    MakeExtnPrivate=False    HuntPattern=4    RingsPerMember=3    NoAnswerRings=4    CallMemberWhenForwarding=True    SkipMemberOnCall=False    CallStackFull=${EMPTY}    NoAnswer=${EMPTY}
    ${hgExtension} =     using ${bossPortal} I want to create hunt group user extension with ${huntGroupDetails}
    Given On ${phone1} dial number ${hgExtension}
    Then Verify the led state of ${line1} as ${blink} on ${phone2}
    Then On ${phone1} verify display message ${huntGroupDetails['GroupName']}
    Then Press hardkey as ${goodBye} on ${phone1}
    Then I want to use fac ${busyOutHuntGroupFAC} on ${phone1} to ${hgExtension}
    Then On ${phone1} Wait for 5 seconds
    Then On ${phone1} dial number ${hgExtension}
    Then On ${phone1} verify display message ${busy}
    Then On ${phone1} Wait for 5 seconds
    Then I want to use fac ${busyOutHuntGroupFAC} on ${phone1} to ${hgExtension}
    Then On ${phone1} Wait for 5 seconds
    Then On ${phone1} dial number ${hgExtension}
    Then On ${phone1} verify display message ${huntGroupDetails['GroupName']}
    Then Verify the led state of ${line1} as ${blink} on ${phone2}
    And Press hardkey as ${goodBye} on ${phone1}
    [Teardown]    Hunt Group Custom Teardown

759693: Press Hotline Intercom button to initiate a call
    [Tags]    Owner:Vikhyat    Reviewer:    hotline    second
    &{hotlineDetails}    CREATE DICTIONARY    ConnectedCallFunctionID=intercom    account_name=Automation    part_name=SC1    button_box=0
    Given Using ${bossPortal} I program ${hotline} on ${phone1} using ${hotlineDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${hotline}
    Then Press hardkey as ${programKey5} on ${phone1}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then Verify audio path between ${phone1} and ${phone2}
    And Press hardkey as ${goodBye} on ${phone1}

754347: Place Outbound call when Hotline Intercom button set
    [Tags]    Owner:Vikhyat    Reviewer:    hotline    third
    &{hotlineDetails}    CREATE DICTIONARY    ConnectedCallFunctionID=intercom    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${hotline} on ${phone1} using ${hotlineDetails} and extension of ${phone2} and softkey position 1 with extensionValue
    Then On ${phone1} verify display message ${hotline}
    Then I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then Answer the call on ${phone2} using ${offHook}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then I want to make a two party call between ${phone3} and ${phone1} using ${offHook}
    Then Answer the call on ${phone1} using ${softKey}
    Then Verify the led state of ${line3} as ${on} on ${phone1}
    Then Verify audio path between ${phone1} and ${phone3}
    Then Disconnect the call from ${phone2}
    Then Disconnect the call from ${phone3}
    And Using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 1


751744: Edit Delay after collecting digits. disable INTERCOM. enter valid digits.
    [Tags]    Owner:Vikhyat    Reviewer:    delayDigits_intercom    third    notApplicableForMiCloud
    Given Using ${bossPortal} I want to change Delay after collecting digits value to 4000

    &{COSDetails} =  CREATE DICTIONARY    Name=${fullyFeatured}     AllowIntercomInitiation=False
    Given Using ${bossPortal} I want to change telephony features values using ${COSDetails}

    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudSpeaker}
    Then Press hardkey as ${goodBye} on ${phone2}
    Then Press the call history button on ${phone1} and folder ${all} and ${details}
    Then I want to verify on ${phone1} negative display message ${intercom}
    And Press hardkey as ${goodBye} on ${phone1}
    [Teardown]    RUN KEYWORDS    Telephony Options Custom Teardown    CoS Features Custom Teardown

753636: Admin makes 2 way conf on SCA line1, Admin leaves, gets dialog, drops call
    [Tags]    Owner:Vikhyat    Reviewer:    SCA    third
    [Setup]    Telephony Feature Custom Setup
    &{telephonydetails}=  Create Dictionary    sca_enabled=True
    ${scaExtn} =  using ${bossPortal} on ${phone2} I want to enable SCA using ${telephonydetails}

    &{bcaDetails} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=3    function=Bridge Call Appearance    label=${bca}    target_extension=${scaExtn}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${EMPTY}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=${EMPTY}
    Given using ${bossPortal} I want to create bca on ${phone1} using ${bcaDetails}
    Then on ${phone1} verify display message ${bca}
    Then Press hardkey as ${programKey4} on ${phone1}
    Then on ${phone1} enter number ${phone3}
    Then On ${phone1} Wait for 5 seconds
    Then Answer the call on ${phone3} using ${offHook}
    Then Verify audio path between ${phone1} and ${phone3}
    Then I want to make a conference call between ${phone1},${phone3} and ${phone4} using ${directConference}
    Then Conference call audio verify between ${phone1} ${phone3} and ${phone4}
    Then press hardkey as ${goodBye} on ${phone1}
    Then Verify the Caller id on ${phone3} and ${phone4} display
    Then verify the led state of ${line4} as ${off} on ${phone1}
    Then Verify audio path between ${phone3} and ${phone4}
    Then disconnect the call from ${phone3}

    &{telephonydetails}=  Create Dictionary    sca_enabled=False
    ${scaExtn} =  using ${bossPortal} on ${phone2} I want to disable SCA using ${telephonydetails}
    [Teardown]    Telephony Feature Custom Teardown

754453: XMON, CID Never - held conference on target
    [Tags]    Owner:Vikhyat    Reviewer:    xmon    third
    &{extensionDetails} =  CREATE DICTIONARY  ring_delay=none   show_caller_id=never    no_connected=dial_number    with_connected=dial_number    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then I want to make a two party call between ${phone2} and ${phone3} using ${loudSpeaker}
    Then Answer the call on ${phone3} using ${loudSpeaker}
    Then I want to make a conference call between ${phone2},${phone3} and ${phone4} using ${directConference}
    Then Conference call audio verify between ${phone2} ${phone3} and ${phone4}
    Then Put the linekey ${line1} of ${phone2} on ${hold}
    Then Verify the led state of ${line5} as ${on} on ${phone1}
    Then On ${phone1} press ${hardKey} ${programKey5} for 2 times
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then Answer the call on ${phone2} using ${softKey}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then Verify the led state of ${line1} as ${blink} on ${phone2}
    Then Disconnect the call from ${phone1}
    Then Disconnect the call from ${phone3}
    And Disconnect the call from ${phone4}

754360: Place Outbound call when Hotline speed dial button set
    [Tags]    Owner:Vikhyat    Reviewer:    hotline    third
    &{hotlines}    CREATE DICTIONARY    ConnectedCallFunctionID=dial number    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${hotline} on ${phone1} using ${hotlines} and extension of ${phone2} and softkey position 1 with ExtensionValue
    Then I want to make a two party call between ${phone1} and ${phone2} using ${loudSpeaker}
    Then Answer the call on ${phone2} using ${loudSpeaker}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then Verify audio path between ${phone1} and ${phone2}
    Then I want to make a two party call between ${phone3} and ${phone1} using ${loudSpeaker}
    Then Answer the call on ${phone1} using ${softKey}
    Then Verify the led state of ${line3} as ${on} on ${phone1}
    Then Disconnect the call from ${phone2}
    And Disconnect the call from ${phone3}

755786: Regression - Access Directory, Password Change Checkbox=True
    [Tags]    Owner:Vikhyat    Reviewer:    vmPasswordChange    third    notApplicableForMiCloud
    [Setup]    Telephony Feature Custom Setup
    &{telephonydetails} =  Create Dictionary    VM_pwd_change_on_next_login=True
    Given using ${bossPortal} on ${phone1} I want to check voicemail password on next login using ${telephonydetails}
    Then Press hardkey as ${directory} on ${phone1}
    Then On ${phone1} verify display message ${directory}
    Then I want to verify on ${phone1} negative display message ${newVoiceMailPasswordDisplay}
    Then Press hardkey as ${goodBye} on ${phone1}
    [Teardown]    Set Default Voicemail Password

755787: Regression - Access History, Password Change Checkbox=False
    [Tags]    Owner:Vikhyat    Reviewer:    vmPasswordChange    third    notApplicableForMiCloud
    [Setup]    Telephony Feature Custom Setup
    &{telephonydetails} =  Create Dictionary    VM_pwd_change_on_next_login=False
    Given using ${bossPortal} on ${phone1} I want to uncheck voicemail password on next login using ${telephonydetails}
    Then Press hardkey as ${callersList} on ${phone1}
    Then On ${phone1} verify display message ${callHistory}
    Then I want to verify on ${phone1} negative display message ${newVoiceMailPasswordDisplay}
    Then Press hardkey as ${goodBye} on ${phone1}
    [Teardown]    Set Default Voicemail Password

755788: Regression - Access History, Password Change Checkbox=True
    [Tags]    Owner:Vikhyat    Reviewer:    vmPasswordChange    third    notApplicableForMiCloud
    [Setup]    Telephony Feature Custom Setup
    &{telephonydetails} =  Create Dictionary    VM_pwd_change_on_next_login=True
    Given using ${bossPortal} on ${phone1} I want to check voicemail password on next login using ${telephonydetails}
    Then Press hardkey as ${callersList} on ${phone1}
    Then On ${phone1} verify display message ${callHistory}
    Then I want to verify on ${phone1} negative display message ${newVoiceMailPasswordDisplay}
    Then Press hardkey as ${goodBye} on ${phone1}
    [Teardown]    Set Default Voicemail Password

753758: Admin has meetme on BCA line, A, already in meetme calls admin, attempts to join
    [Tags]    Owner:Vikhyat    Reviewer:    ucbConference    third
    [Setup]    BCA Custom Setup
    &{createBCAExtension}=  Create Dictionary    name=bca_vk   backupExtn=${phone3}    switch=2    callStackDepth=2    forwardAfter=2    callStackFull=${EMPTY}   noAnswer=${EMPTY}    outboundCallerID=${EMPTY}    allowBridgeConferencing=true   defaultPrivacySettings=0
    ${bcaExt}=    using ${bossPortal} I want to create Bridge Call Appearance extension using ${createBCAExtension}
    &{bcaDetails}=  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=3    function=Bridge Call Appearance    label=${bca}    target_extension=${bcaExt}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${EMPTY}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=${EMPTY}
    Given using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails}
    Then Press hardkey as ${programKey4} on ${phone1}
    Then On ${phone1} dial number ${ucbExtension}
    Then On ${phone1} Wait for 4 seconds
    Then on ${phone1} enter number ${accessCode}

    Then On ${phone2} dial number ${ucbExtension}
    Then On ${phone2} Wait for 4 seconds
    Then on ${phone2} enter number ${accessCode}

    Then On ${phone3} dial number ${ucbExtension}
    Then On ${phone3} Wait for 4 seconds
    Then on ${phone3} enter number ${accessCode}

    Then On ${phone4} dial number ${ucbExtension}
    Then On ${phone4} Wait for 4 seconds
    Then on ${phone4} enter number ${accessCode}

    Then On ${phone5} dial number ${ucbExtension}
    Then On ${phone5} Wait for 4 seconds
    Then on ${phone5} enter number ${accessCode}

    Then On ${phone1} verify display message ${conferenceExt}
    Then On ${phone2} verify display message ${conferenceExt}
    Then On ${phone3} verify display message ${conferenceExt}
    Then On ${phone4} verify display message ${conferenceExt}
    Then On ${phone5} verify display message ${conferenceExt}

    Then I want to make a two party call between ${phone2} and ${phone1} using ${programKey2}
    Then Answer the call on ${phone1} using ${programKey1}
    Then Verify audio path between ${phone1} and ${phone2}
    Then On ${phone1} press the softkey ${conference} in AnswerState
    Then Press hardkey as ${programKey4} on ${phone1}
    Then Verify the led state of ${line1} as ${blink} on ${phone2}
    Then Verify the led state of ${line2} as ${on} on ${phone2}
    Then Five party Conference call audio verification between ${phone1} ${phone2} ${phone3} ${phone4} and ${phone5}
    Then Disconnect the call from ${phone5}
    Then Disconnect the call from ${phone4}
    Then Disconnect the call from ${phone3}
    Then Disconnect the call from ${phone2}
    Then Put the linekey ${line1} of ${phone2} on ${unhold}
    Then Disconnect the call from ${phone2}
    And Disconnect the call from ${phone1}
    [Teardown]    BCA Custom Teardown

753759: Admin has meetme on BCA line, Calls A on boss2 line, joins.
    [Tags]    Owner:Vikhyat    Reviewer:    ucbConference    third
    [Setup]    Telephony Feature Custom Setup
    &{telephonydetails}=  Create Dictionary    sca_enabled=True
    ${scaExtn1} =  using ${bossPortal} on ${phone2} I want to enable SCA using ${telephonydetails}
    &{createBCAExtension1}=  Create Dictionary    extension=${scaExtn1}   backupExtn=${phone3}    allowBridgeConferencing=true
    Given Using ${bossPortal} I want to modify Bridge Call Appearance extension using ${createBCAExtension1}

    &{telephonydetails}=  Create Dictionary    sca_enabled=True
    ${scaExtn2} =  using ${bossPortal} on ${phone3} I want to enable SCA using ${telephonydetails}
    &{createBCAExtension2}=  Create Dictionary    extension=${scaExtn2}   backupExtn=${phone3}    allowBridgeConferencing=true
    Given Using ${bossPortal} I want to modify Bridge Call Appearance extension using ${createBCAExtension2}

    &{bcaDetails1}=  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=3    function=Bridge Call Appearance    label=${bca}    target_extension=${scaExtn1}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${EMPTY}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=${EMPTY}
    Given using ${bossPortal} I want to create bca on ${phone1} using ${bcaDetails1}

    &{bcaDetails2}=  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=4    function=Bridge Call Appearance    label=${bca}    target_extension=${scaExtn2}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${EMPTY}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=${EMPTY}
    Given using ${bossPortal} I want to create bca on ${phone1} using ${bcaDetails2}

    Then Press hardkey as ${programKey4} on ${phone1}
    Then On ${phone1} dial number ${ucbExtension}
    Then On ${phone1} Wait for 4 seconds
    Then on ${phone1} enter number ${accessCode}

    Then On ${phone2} dial number ${ucbExtension}
    Then On ${phone2} Wait for 4 seconds
    Then on ${phone2} enter number ${accessCode}

    Then On ${phone3} dial number ${ucbExtension}
    Then On ${phone3} Wait for 4 seconds
    Then on ${phone3} enter number ${accessCode}

    Then On ${phone5} dial number ${ucbExtension}
    Then On ${phone5} Wait for 4 seconds
    Then on ${phone5} enter number ${accessCode}

    Then On ${phone6} dial number ${ucbExtension}
    Then On ${phone6} Wait for 4 seconds
    Then on ${phone6} enter number ${accessCode}

    Then On ${phone1} verify display message ${conferenceExt}
    Then On ${phone2} verify display message ${conferenceExt}
    Then On ${phone3} verify display message ${conferenceExt}
    Then On ${phone5} verify display message ${conferenceExt}
    Then On ${phone6} verify display message ${conferenceExt}

    Then I want to make a two party call between ${phone1} and ${phone4} using ${programKey5}
    Then Answer the call on ${phone4} using ${offHook}
    Then On ${phone1} press the softkey ${conference} in AnswerState
    Then Press hardkey as ${programKey4} on ${phone1}
    Then On ${phone4} verify display message ${conferenceExt}
    Then Disconnect the call from ${phone6}
    Then Disconnect the call from ${phone5}
    Then Disconnect the call from ${phone4}
    Then Disconnect the call from ${phone3}
    Then Disconnect the call from ${phone2}
    [Teardown]    Telephony Feature Custom Teardown

753943: Boss Dial from Directory
    [Tags]    Owner:Vikhyat    Reviewer:        SCA    third
    [Setup]    Telephony Feature Custom Setup
    &{telephonydetails}=  Create Dictionary    sca_enabled=True
    ${scaExtn} =  using ${bossPortal} on ${phone1} I want to enable SCA using ${telephonydetails}

    Then On ${phone1} press directory and ${dial} of ${phone2}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    And Disconnect the call from ${phone1}
    [Teardown]    Telephony Feature Custom Teardown

754901: extension monitoring in hold state
    [Tags]    Owner:Vikhyat    Reviewer:    xMon    third
    &{extensionDetails} =    Create Dictionary    ring_delay=dont_ring    show_caller_id=only_when_ringing    no_connected=dial_number    with_connected=transfer_consultative    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then On ${phone1} verify ${line5} icon state as ${xmonIdle}
    Then I want to make a two party call between ${phone3} and ${phone2} using ${offHook}
    Then Answer the call on ${phone2} using ${offHook}
    Then On ${phone1} Wait for 5 seconds
    Then On ${phone1} verify ${line5} icon state as ${xmonBusy}
    Then Put the linekey ${line1} of ${phone3} on ${hold}
    Then On ${phone1} verify ${line5} icon state as ${xmonBusy}
    And Disconnect the call from ${phone2}

759708: Press Hotline speed dial button while incoming call
    [Tags]    Owner:Vikhyat    Reviewer:    hotline    third
    &{hotlineDetails}    CREATE DICTIONARY    ConnectedCallFunctionID=dial number    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${hotline} on ${phone1} using ${hotlineDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then I want to make a two party call between ${phone3} and ${phone1} using ${offHook}
    Then Press hardkey as ${programKey5} on ${phone1}
    Then Verify the led state of ${line1} as ${blink} on ${phone1}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then Verify the led state of ${line1} as ${blink} on ${phone2}
    Then Disconnect the call from ${phone2}
    And Disconnect the call from ${phone3}

754350: Press Hotline Intercom button while a call is on Hold
    [Tags]    Owner:Vikhyat    Reviewer:    hotline    third
    &{hotlineDetails}    CREATE DICTIONARY    ConnectedCallFunctionID=intercom    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${hotline} on ${phone1} using ${hotlineDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${hotline}
    Then I want to make a two party call between ${phone3} and ${phone1} using ${offHook}
    Then Answer the call on ${phone1} using ${offHook}
    Then On ${phone1} verify ${line1} icon state as ${callAppearanceActive}
    Then Verify audio path between ${phone1} and ${phone3}
    Then Put the linekey ${line1} of ${phone1} on ${hold}
    Then On ${phone1} verify ${line1} icon state as ${callAppearanceLocalHold}
    Then Press hardkey as ${programKey5} on ${phone1}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then Verify audio path between ${phone1} and ${phone2}
    Then Disconnect the call from ${phone2}
    And Disconnect the call from ${phone3}

758238: Phone sends digits over VM
    [Tags]    Owner:Vikhyat    Reviewer:    sendDigitsOverVm        third
    Given Leave voicemail message from ${phone2} on ${phone1}

    &{sendDigitsDetails}    CREATE DICTIONARY    account_name=Automation    part_name=SC1    button_box=0    digits=${loginVoicemail}
    Given using ${bossPortal} I program ${sendDigitsOverCall} on ${phone1} using ${sendDigitsDetails} and extension of ${phone1} and softkey position 3 with noExtensionValue
    Then On ${phone1} dial number #
    Then On ${phone1} verify display message ${voiceMailLogin}
    Then On ${phone1} press ${softkey} ${programKey2} for 1 times
    Then On ${phone1} dial number 1
    Then On ${phone1} Wait for 5 seconds
    Then Press hardkey as ${goodBye} on ${phone1}
    Then Verify the led state of ${messageWaitingIndicator} as ${off} on ${phone1}

754396: Correct state shown on monitoring phone after phone reboot
    [Tags]    Owner:Vikhyat    Reviewer:    xMon        third
    &{extensionDetails}    Create Dictionary    ring_delay=none   show_caller_id=never    no_connected=dial_number    with_connected=dial_number    account_name=Automation    part_name=SC1    button_box=0
    Given Using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 3 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['monitorExtn']}
    Then On ${phone1} verify ${line4} icon state as ${xmonIdle}
    Then Reboot ${phone1}
    Then On ${phone1} verify ${line4} icon state as ${xmonIdle}

    Then On ${phone2} navigate to ${availability} settings
    Then Modify call handler mode on ${phone2} to ${always} in ${doNotDisturb}
    Then On ${phone2} press the softkey ${save} in SettingState
    Then On ${phone2} press the softkey ${quit} in SettingState
    Then On ${phone1} verify ${line4} icon state as ${xmonIdleDND}
    Then Reboot ${phone1}
    Then On ${phone1} verify ${line4} icon state as ${xmonIdleDND}
    Then On ${phone1} navigate to ${availability} settings
    Then Modify call handler mode on ${phone2} to ${noAnswer} in ${available}
    Then On ${phone2} press the softkey ${save} in SettingState
    Then On ${phone2} press the softkey ${quit} in SettingState

    Then Leave voicemail message from ${phone2} on ${phone1}
    Then On ${phone1} verify ${line4} icon state as ${xmonIdleMWI}
    Then Reboot ${phone1}
    Then On ${phone1} verify ${line4} icon state as ${xmonIdleMWI}
    Then Delete voicemail message on ${inbox} for ${phone1} using ${voicemailPassword}

    Then I want to make a two party call between ${phone3} and ${phone2} using ${offHook}
    Then Answer the call on ${phone2} using ${offHook}
    Then On ${phone1} verify ${line4} icon state as ${xmonActive}
    Then Reboot ${phone1}
    Then On ${phone1} verify ${line4} icon state as ${xmonActive}
    Then Disconnect the call from ${phone2}
    [Teardown]    RUN KEYWORDS    Generic Test Teardown    Default Availability State

759546: Correct state shown on monitoring phone after phone reboot
    [Tags]    Owner:Vikhyat    Reviewer:    xMon    third
    &{extensionDetails}    Create Dictionary    ring_delay=none   show_caller_id=never    no_connected=dial_number    with_connected=dial_number    account_name=Automation    part_name=SC1    button_box=1
    Given Using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 0 with extensionValue
    Then verify display message ${displayMessage['monitorExtn']} on PKM for ${phone1}
    Then Verify ${line1} icon state as ${xmonIdle} on PKM for ${phone1}
    Then Reboot ${phone1}
    Then Verify ${line1} icon state as ${xmonIdle} on PKM for ${phone1}

    Then On ${phone2} navigate to ${availability} settings
    Then Modify call handler mode on ${phone2} to ${always} in ${doNotDisturb}
    Then On ${phone2} press the softkey ${save} in SettingState
    Then On ${phone2} press the softkey ${quit} in SettingState
    Then Verify ${line1} icon state as ${xmonIdleDND} on PKM for ${phone1}
    Then Reboot ${phone1}
    Then Verify ${line1} icon state as ${xmonIdleDND} on PKM for ${phone1}
    Then On ${phone2} navigate to ${availability} settings
    Then Modify call handler mode on ${phone2} to ${noAnswer} in ${available}
    Then On ${phone2} press the softkey ${save} in SettingState
    Then On ${phone2} press the softkey ${quit} in SettingState

    Then Leave voicemail message from ${phone3} on ${phone2}
    Then Verify ${line1} icon state as ${xmonIdleMWI} on PKM for ${phone1}
    Then Reboot ${phone1}
    Then Verify ${line1} icon state as ${xmonIdleMWI} on PKM for ${phone1}

    Then I want to make a two party call between ${phone3} and ${phone2} using ${offHook}
    Then Answer the call on ${phone2} using ${offHook}
    Then Verify ${line1} icon state as ${xmonActive} on PKM for ${phone1}
    Then Reboot ${phone1}
    Then Verify ${line1} icon state as ${xmonActive} on PKM for ${phone1}
    Then Disconnect the call from ${phone2}
    [Teardown]    RUN KEYWORDS    Generic Test Teardown    Default Availability State

752436: Conference Intercom XMON extension, Part 1
    [Tags]    Owner:Vikhyat    Reviewer:    xMon    third
    &{extensionDetails}    Create Dictionary    ring_delay=none   show_caller_id=never    no_connected=unused    with_connected=unused    account_name=Automation    part_name=SC1    button_box=0
    Given Using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone3} and softkey position 1 with noExtensionValue
    Then On ${phone1} verify display message ${displayMessage['monitorExtn']}

    Then Using ${bossPortal} I program ${conferenceIntercom} on ${phone1} using ${buttonDetails} and extension of ${none} and softkey position 2 with ${extMode}
    Then On ${phone1} verify display message ${displayMessage['conferenceIntercom']}

    Then I want to make a two party call between ${phone2} and ${phone1} using ${offHook}
    Then Answer the call on ${phone1} using ${offHook}
    Then On ${phone1} press ${softKey} ${programKey3} for 1 times
    Then On ${phone1} press ${softKey} ${programKey2} for 1 times
    Then Verify the Caller id on ${phone1} and ${phone3} display
    Then On ${phone3} verify display message ${drop}
    Then On ${phone1} press ${softKey} ${bottomKey2} for 1 times
    Then Conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then Disconnect the call from ${phone2}
    Then Disconnect the call from ${phone3}

    Then I want to make a two party call between ${phone2} and ${phone1} using ${offHook}
    Then Answer the call on ${phone1} using ${offHook}
    Then I want to make a conference call between ${phone1},${phone2} and ${phone4} using ${directConference}
    Then On ${phone1} press ${softKey} ${programKey3} for 1 times
    Then On ${phone1} press ${softKey} ${programKey2} for 1 times
    Then Verify the Caller id on ${phone1} and ${phone3} display
    Then On ${phone3} verify display message ${drop}
    Then On ${phone1} press ${softKey} ${bottomKey2} for 1 times
    Then Four party Conference call audio verification between ${phone1} ${phone2} ${phone3} and ${phone4}
    Then Disconnect the call from ${phone2}
    Then Disconnect the call from ${phone3}
    Then Disconnect the call from ${phone4}

    Then I want to make a two party call between ${phone2} and ${phone1} using ${offHook}
    Then Answer the call on ${phone1} using ${offHook}
    Then I want to make a conference call between ${phone1},${phone2} and ${phone4} using ${directConference}
    Then Add the ${phone5} in 4 parties conference call on ${phone1}
    Then On ${phone1} press ${softKey} ${programKey3} for 1 times
    Then On ${phone1} press ${softKey} ${programKey2} for 1 times
    Then Verify the Caller id on ${phone1} and ${phone3} display
    Then On ${phone3} verify display message ${drop}
    Then On ${phone1} press ${softKey} ${bottomKey2} for 1 times
    Then Five party Conference call audio verification between ${phone1} ${phone2} ${phone3} ${phone4} and ${phone5}
    Then Disconnect the call from ${phone2}
    Then Disconnect the call from ${phone3}
    Then Disconnect the call from ${phone4}
    Then Disconnect the call from ${phone5}

759682: Prog Buttons- Whisper Page Mute-3
    [Tags]    Owner:Vikhyat     Reviewer:    whisperPage    third
    Given Using ${bossPortal} I program ${whisperPageMute} on ${phone1} using ${bossDetailsPKM} and extension of ${none} and softkey position 0 with extensionValue
    Given Using ${bossPortal} I program ${whisperPage} on ${phone3} using ${bossDetails} and extension of ${phone1} and softkey position 3 with extensionValue
    Then Verify negative display message ${whisperPageMute} on PKM attached to ${phone1}
    Then Verify display message ${whisperPage} on PKM for ${phone1}
    Then I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then Answer the call on ${phone2} using ${offHook}
    Then Verify audio path between ${phone1} and ${phone2}
    Then On ${phone3} press ${softKey} ${programKey4} for 1 times
    Then Verify audio path between ${phone1} and ${phone3}
    Then Verify no audio path from ${phone3} to ${phone2}
    Then I want to press PKM line key ${programKey1} on ${phone1}
    Then Verify no audio path from ${phone1} to ${phone2}
    Then Verify one way audio from ${phone2} to ${phone1}
    Then Verify audio path between ${phone1} and ${phone3}
    Then Disconnect the call from ${phone2}
    Then Disconnect the call from ${phone1}

759591: Prog. Buttons - funny characters - Any symbol is allowed for a label.
    [Tags]    Owner:Vikhyat    Reviewer:    nameCheck    third
    &{bossPortalLongName}    CREATE DICTIONARY    account_name=Automation    part_name=SC1    button_box=1    label='Pickup"
    Given Using ${bossPortal} I program ${pickUp} on ${phone1} using ${bossDetailsPKM} and extension of ${phone2} and softkey position 1 with extensionValue
    Then Verify display message 'Pickup" on PKM for ${phone1}

759593: Prog. Buttons - funny characters - Change name of user to include symbol characters.
    [Tags]    Owner:Vikhyat    Reviewer:    nameCheck    fourth
    &{bossPortalLongName}    CREATE DICTIONARY    account_name=Automation    part_name=SC1    button_box=1    label='Pickup"
    Given Using ${bossPortal} I program ${pickUp} on ${phone1} using ${bossDetailsPKM} and extension of ${phone2} and softkey position 1 with extensionValue
    Then Verify display message 'Pickup" on PKM for ${phone1}

753667: Admin makes 2 way conf on SCA line1, Admin leaves, gets dialog, parks call, Admin joins 3rd caller in
    [Tags]    Owner:Vikhyat    Reviewer:    BCA    fourth
    [Setup]    BCA Custom Setup

    &{createBCAExtension}=  Create Dictionary    name=bca_vk1   backupExtn=${phone3}    switch=2    callStackDepth=1    forwardAfter=2    callStackFull=${EMPTY}   noAnswer=${EMPTY}    outboundCallerID=${EMPTY}    allowBridgeConferencing=true   defaultPrivacySettings=0
    ${bcaExt1}=    using ${bossPortal} I want to create Bridge Call Appearance extension using ${createBCAExtension}
    &{bcaDetails1}=  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=4    function=Bridge Call Appearance    label=${bca}    target_extension=${bcaExt1}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${EMPTY}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=${EMPTY}
    using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails1}

    Given I want to make a two party call between ${phone1} and ${phone3} using ${programKey5}
    Then Answer the call on ${phone3} using ${loudSpeaker}
    Then I want to make a conference call between ${phone1},${phone3} and ${phone4} using ${directConference}
    Then Conference call audio verify between ${phone1} ${phone3} and ${phone4}
    Then I want to make a two party call between ${phone5} and ${phone1} using ${loudSpeaker}
    Then Answer the call on ${phone1} using ${line1}
    Then On ${phone1} press the softkey ${conference} in answerstate
    Then Press hardkey as ${programKey5} on ${phone1}
    Then Verify the led state of ${line1} as ${off} on ${phone1}
    Then Four party Conference call audio verification between ${phone1} ${phone3} ${phone4} and ${phone5}
    Then Disconnect the call from ${phone1}
    Then Verify the led state of ${line5} as ${off} on ${phone1}
    Then Conference call audio verify between ${phone3} ${phone4} and ${phone5}
    Then Disconnect the call from ${phone3}
    Then Disconnect the call from ${phone4}
    [Teardown]    BCA Custom Teardown

127829: TC002 - Progbutton Transfer Blind destination configured (call not answered)
    [Tags]     Owner:Aman      Reviewer:Surender       blind_transfer    fourth
    Given using ${bossPortal} I program ${transferBlind} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['transferBlind']}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then On ${phone1} Wait for 2 seconds
    Then On ${phone1} verify display message ${displayMessage['callTransferred']}
    Then Answer the call on ${phone3} using ${loudspeaker}
    Then Verify audio path between ${phone2} and ${phone3}
    Then disconnect the call from ${phone2}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4


127831:TC004 - Progbutton Transfer Blind destination not configured (call not answered)
    [Tags]     Owner:Aman      Reviewer:Ram       blind_transfer    fourth
    Given using ${bossPortal} I program ${transferBlind} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with noExtensionValue
    Then On ${phone1} verify display message ${displayMessage['transferBlind']}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then On ${phone1} verify display message ${backspace}
    Then On ${phone1} verify display message ${cancel}
    Then I want to verify on ${phone1} negative display message ${consult}
    Then on ${phone1} enter number ${phone3}
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then On ${phone1} Wait for 2 seconds
    Then Answer the call on ${phone3} using ${loudspeaker}
    Then Verify audio path between ${phone2} and ${phone3}
    Then On ${phone1} verify the softkeys in ${idleState}
    Then disconnect the call from ${phone2}
    Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} enter number ${phone3}
    Then On ${phone1} Wait for 5 seconds
    Then Answer the call on ${phone3} using ${loudspeaker}
    Then Verify audio path between ${phone2} and ${phone3}
    Then On ${phone1} verify the softkeys in ${idleState}
    Then disconnect the call from ${phone2}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4

127832:TC005 - Progbutton Transfer progbutton (Transfer Blind or Transfer Consult) destination configured
    [Tags]     Owner:Aman      Reviewer:Avishek         blind_transfer    fourth
    Given using ${bossPortal} I program ${transferBlind} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['transferBlind']}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then On ${phone1} Wait for 2 seconds
    Then On ${phone1} verify display message ${displayMessage['callTransferred']}
    Then On ${phone3} verify display message ${Transfer}
    Then Answer the call on ${phone3} using ${loudspeaker}
    Then Verify audio path between ${phone2} and ${phone3}
    Then disconnect the call from ${phone2}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4

127833:TC006 - Progbutton Transfer progbutton (Transfer Blind) destination not configured
    [Tags]     Owner:Aman      Reviewer:Avishek       blind_transfer    fourth
    Given using ${bossPortal} I program ${transferBlind} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with noExtensionValue
    Then On ${phone1} verify display message ${displayMessage['transferBlind']}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then On ${phone1} verify display message ${Transfer}
    Then Verify extension ${number} of ${phone2} on ${phone1}
    Then disconnect the call from ${phone2}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4

210077:TC011 Press transfer blind key in Idle state
    [Tags]     Owner:Aman      Reviewer:Avishek       blind_transfer    fourth
    Given using ${bossPortal} I program ${transferBlind} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['transferBlind']}
    Then On ${phone1} verify the softkeys in ${idleState}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then On ${phone1} verify the softkeys in ${idleState}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4

221434:TC005 Hold and press transfer intercom key
    [Tags]     Owner:Aman      Reviewer:Avishek      transfer_intercom    fourth
    Given using ${bossPortal} I program ${transferIntercom} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with noExtensionValue
    Then On ${phone1} verify display message ${displayMessage['transferIntercom']}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then Answer the call on ${phone1} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Press hardkey as ${HoldState} on ${phone1}
    Then On ${phone1} Wait for 2 seconds
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then Verify the Caller id on ${phone2} and ${phone1} display
    Then Press hardkey as ${HoldState} on ${phone1}
    Then On ${phone1} Wait for 2 seconds
    Then disconnect the call from ${phone2}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4

221438:TC009 phone Progbutton Transfer Intercom
    [Tags]     Owner:Aman      Reviewer:Avishek       transfer_intercom    fourth
    Given using ${bossPortal} I program ${transferIntercom} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['transferIntercom']}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then Answer the call on ${phone1} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then On ${phone1} verify display message ${Transfer}
    Then On ${phone1} verify display message ${Drop}
    Then disconnect the call from ${phone3}
    Then disconnect the call from ${phone2}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4

221439:TC010 Program 'transfer intercom' key without extension
    [Tags]     Owner:Aman      Reviewer:Ram        transfer_intercom    fourth
    Given using ${bossPortal} I program ${transferIntercom} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with noExtensionValue
    Then On ${phone1} verify display message ${displayMessage['transferIntercom']}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then Answer the call on ${phone1} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} enter number ${phone3}
    Then On ${phone1} Wait for 6 seconds
    Then Verify audio path between ${phone1} and ${phone3}
    Then On ${phone1} verify display message ${transfer}
    Then On ${phone1} verify display message ${drop}
    Then disconnect the call from ${phone3}
    Then disconnect the call from ${phone2}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4

221441:TC012 Press transfer intercom key in Idle state
    [Tags]     Owner:Aman      Reviewer:Ram        transfer_intercom    fourth
    Given using ${bossPortal} I program ${transferIntercom} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['transferIntercom']}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then On ${phone1} verify the softkeys in ${idleState}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4

188420: TC001 Creating a Programmed key 'Dial Number(speed dial)'
    [Tags]     Owner:Aman      Reviewer:Ram        speed_dial    fourth
    Given using ${bossPortal} I program ${dialNumber} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['dialNumber']}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4

188431: TC002 Creating a 'speed dial' program key without a label
    [Tags]     Owner:Aman      Reviewer:       speed_dial    fourth
    Given using ${bossPortal} I program ${dialNumber} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 3 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['dialNumber']}
    Then using ${bossPortal} I program ${dialNumber} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['dialNumber']}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 3
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4

193264: TC001 Icon for speed dial program key
    [Tags]     Owner:Aman      Reviewer:       speed_dial    fourth
    Given using ${bossPortal} I program ${dialNumber} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['dialNumber']}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then On ${phone2} Wait for 3 seconds
    Then Answer the call on ${phone2} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then on ${phone1} press the softkey ${Drop} in AnswerState
    Then On ${phone1} verify display message Dial Number
    Then on ${phone1} verify the softkeys in ${idleState}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4

193265: TC002 Change state to DND - icon Idle
    [Tags]     Owner:Aman      Reviewer:       speed_dial    fourth
    Given using ${bossPortal} I program ${dialNumber} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['dialNumber']}
    Then on ${phone2} navigate to ${availability} settings
    Then Modify call handler mode on ${phone2} to ${always} in ${doNotDisturb}
    Then on ${phone2} press ${softKey} ${bottomKey1} for 1 times
    Then Press hardkey as ${goodBye} on ${phone2}
    Then On ${phone1} verify display message Dial Number
    Then Change the phone state to default state on ${phone2}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4
    [Teardown]    RUN KEYWORDS    Generic Test Teardown    Default Availability State

193266: TC003 leave a VM and check icon
    [Tags]     Owner:Aman      Reviewer:       speed_dial    fourth
    Given using ${bossPortal} I program ${dialNumber} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['dialNumber']}
    Then Delete voicemail message on ${inbox} for ${phone2} using ${voicemailPassword}
    Then Leave voicemail message from ${phone1} on ${phone2}
    Then Login into voicemailBox for ${phone2} using ${voicemailPassword}
    Then Press hardkey as ${scrollRight} on ${phone2}
    Then on ${phone2} press the softkey ${open} in VoiceMailState
    Then Verify extension ${number} of ${phone1} on ${phone2}
    Then Press hardkey as ${goodBye} on ${phone2}
    Then On ${phone1} verify display message ${displayMessage['dialNumber']}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4

193267: TC004 Outgoing call from target extension
    [Tags]     Owner:Aman      Reviewer:       speed_dial    fourth
    Given using ${bossPortal} I program ${dialNumber} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['dialNumber']}
    Then I want to make a two party call between ${phone2} and ${phone3} using ${loudspeaker}
    Then Verify the led state of ${line5} as ${on} on ${phone1}
    Then Press hardkey as ${goodBye} on ${phone2}
    Then Verify the led state of ${line5} as ${off} on ${phone1}
    Then I want to make a two party call between ${phone2} and ${phone3} using ${loudspeaker}
    Then Verify the led state of ${line5} as ${on} on ${phone1}
    Then Press hardkey as ${goodBye} on ${phone2}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4

193268: TC005 Speed dial icon for call hold
    [Tags]     Owner:Aman      Reviewer:       speed_dial    fourth
    Given using ${bossPortal} I program ${dialNumber} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['dialNumber']}
    Then I want to make a two party call between ${phone2} and ${phone3} using ${loudspeaker}
    Then Answer the call on ${phone3} using ${loudspeaker}
    Then Verify audio path between ${phone2} and ${phone3}
    Then Verify the led state of ${line5} as ${on} on ${phone1}
    Then Press hardkey as ${HoldState} on ${phone2}
    Then Verify the led state of ${line5} as ${on} on ${phone1}
    Then Press hardkey as ${HoldState} on ${phone2}
    Then Verify the led state of ${line5} as ${on} on ${phone1}
    Then disconnect the call from ${phone2}
    Then Verify the led state of ${line5} as ${off} on ${phone1}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4

146965: TC04: Press Dial Mailbox button; destination configured
    [Tags]     Owner:Aman      Reviewer:       dial_mailbox    fourth
    Given using ${bossPortal} I program ${dialMailbox} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['dialMailbox']}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then On ${phone1} Wait for 4 seconds
    Then On ${phone1} verify display message Voice Mail
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then disconnect the call from ${phone1}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4

247381: TC010 Program multiple Transfer Whisper keys on phone
    [Tags]     Owner:Aman      Reviewer:       transfer_whisper    fourth
    Given using ${bossPortal} I program ${transferWhisper} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with noExtensionValue
    Then On ${phone1} verify display message ${displayMessage['transferToWhisper']}
    Given using ${bossPortal} I program ${transferWhisper} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 5 with noExtensionValue
    Then On ${phone1} verify display message ${displayMessage['transferToWhisper']}
    Then I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then Answer the call on ${phone2} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} enter number ${phone3}
    Then On ${phone1} Wait for 5 seconds
    Then Verify the led state of ${line4} as ${off} on ${phone1}
    Then Verify the led state of ${line5} as ${off} on ${phone1}
    Then Verify audio path between ${phone1} and ${phone3}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}
    Then using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 5

247382: TC011 Press Transfer Whisper key in Idle state
    [Tags]     Owner:Aman      Reviewer:       transfer_whisper    fifth
    Given using ${bossPortal} I program ${transferWhisper} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['transferToWhisper']}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} verify the softkeys in ${idleState}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4

283890: TC36: Transfer blind: Transfering call with XMON key
    [Tags]     Owner:Aman      Reviewer:       xmon      fifth
    &{extensionDetails} =  Create Dictionary    ring_delay=1    show_caller_id=only_when_ringing    no_connected=unused    with_connected=transfer_blind    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['monitorExtn']}
    Then on ${phone2} verify the softkeys in ${idleState}
    Then I want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then Answer the call on ${phone1} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone3}
    Then Verify the led state of ${line5} as ${off} on ${phone1}
    Then on ${phone1} press the softkey ${Transfer} in AnswerState
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone3} wait for 5 seconds
    Then Verify ringing state on ${phone1} and ${phone2}
    Then Verify the led state of ${line1} as ${blink} on ${phone1}
    Then Verify the led state of ${line1} as ${on} on ${phone3}
    Then Answer the call on ${phone2} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then on ${phone1} press the softkey ${Transfer} in TransferState
    Then Verify the led state of ${line5} as ${on} on ${phone1}
    Then disconnect the call from ${phone3}
    And using ${bossPortal} remove the function key on ${phone1} using ${extensionDetails} and softkey position 4

283893: TC37: Transfer blind : Conf call with XMON key
    [Tags]     Owner:Aman      Reviewer:       xmon    fifth
    &{extensionDetails} =  Create Dictionary    ring_delay=1    show_caller_id=only_when_ringing    no_connected=unused    with_connected=transfer_blind    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['monitorExtn']}
    Then on ${phone2} verify the softkeys in ${idleState}
    Then I want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then Answer the call on ${phone1} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone3}
    Then Verify the led state of ${line5} as ${off} on ${phone1}
    Then on ${phone1} press the softkey ${conference} in AnswerState
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone3} wait for 5 seconds
    Then Verify ringing state on ${phone1} and ${phone2}
    Then Verify the led state of ${line1} as ${blink} on ${phone1}
    Then Verify the led state of ${line1} as ${on} on ${phone3}
    Then Answer the call on ${phone2} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then on ${phone1} press the softkey ${conference} in ConferenceCallState
    Then Conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then Verify the led state of ${line5} as ${on} on ${phone1}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}
    And using ${bossPortal} remove the function key on ${phone1} using ${extensionDetails} and softkey position 4

560343:TC006 Mute call and press transfer intercom key
    [Tags]     Owner:Aman      Reviewer:        transfer_intercom    fifth
    Given using ${bossPortal} I program ${transferIntercom} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['transferIntercom']}
    Then I want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then Answer the call on ${phone1} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone3}
    Then Press hardkey as ${mute} on ${phone1}
    Then Verify one way audio from ${phone3} to ${phone1}
    Then verify no audio path from ${phone1} to ${phone3}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then verify the caller id on ${phone1} and ${phone2} display
    Then Verify one way audio from ${phone2} to ${phone1}
    Then verify no audio path from ${phone1} to ${phone2}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4

560351: TC016 Pressing 'transfer intercom' key in ringing state
    [Tags]     Owner:Aman      Reviewer:        transfer_intercom    fifth
    Given using ${bossPortal} I program ${transferIntercom} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['transferIntercom']}
    Then I want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then Verify ringing state on ${phone3} and ${phone1}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then Verify ringing state on ${phone3} and ${phone1}
    Then on ${phone2} verify the softkeys in ${idleState}
    Then disconnect the call from ${phone3}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4

558368: TC019 Making a transfer whisper call from call history
    [Tags]     Owner:Aman      Reviewer:       transfer_whisper    fifth
    Given using ${bossPortal} I program ${transferWhisper} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with noExtensionValue
    Then On ${phone1} verify display message ${displayMessage['transferToWhisper']}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then Press hardkey as ${goodBye} on ${phone1}
    Then I want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then Answer the call on ${phone1} using ${loudspeaker}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then On ${phone1} verify display message >
    Then Press the call history button on ${phone1} and folder ${missed} and ${select}
    Then Verify audio path between ${phone1} and ${phone2}
    Then on ${phone1} press the softkey ${transfer} in TransferState
    Then Answer the call on ${phone2} using ${loudspeaker}
    Then Verify the Caller id on ${phone2} and ${phone3} display
    Then On ${phone1} verify the softkeys in ${IdleState}
    Then Press hardkey as ${goodBye} on ${phone3}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4

127828:TC001 - Progbutton Transfer Blind destination configured (call answered)
    [Tags]      Owner:Aman      Reviewer:Surender      blind_transfer    fifth
    Given using ${bossPortal} I program ${transferBlind} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['transferBlind']}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then Answer the call on ${phone1} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then On ${phone1} Wait for 2 seconds
    Then On ${phone1} verify display message ${displayMessage['callTransferred']}
    Then Answer the call on ${phone3} using ${loudspeaker}
    Then Verify audio path between ${phone2} and ${phone3}
    Then disconnect the call from ${phone2}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4

127830:TC003-Progbutton Transfer Blind destination not configured (call answered)
    [Tags]     Owner:Aman      Reviewer:Ram       blind_transfer    fifth
    Given using ${bossPortal} I program ${transferBlind} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with noExtensionValue
    Then On ${phone1} verify display message ${displayMessage['transferBlind']}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then Answer the call on ${phone1} using ${loudspeaker}
   Then Verify audio path between ${phone1} and ${phone2}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then On ${phone1} verify display message ${transfer}
    Then I want to verify on ${phone1} negative display message ${consult}
    Then on ${phone1} enter number ${phone3}
    Then On ${phone1} verify display message ${backspace}
    Then on ${phone1} press the softkey ${Transfer} in TransferState
    Then On ${phone1} verify display message ${displayMessage['callTransferred']}
    Then Answer the call on ${phone3} using ${loudspeaker}
    Then Verify audio path between ${phone2} and ${phone3}
    Then On ${phone1} verify the softkeys in ${idle}
    Then disconnect the call from ${phone2}
    Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then Answer the call on ${phone1} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} enter number ${phone3}
    Then On ${phone1} Wait for 4 seconds
    Then On ${phone1} verify display message ${displayMessage['callTransferred']}
    Then Answer the call on ${phone3} using ${loudspeaker}
    Then Verify audio path between ${phone2} and ${phone3}
    Then On ${phone1} verify the softkeys in ${idle}
    Then disconnect the call from ${phone2}

227963:TC01-a: Progbutton Transfer To Mailbox - With a target extension (Incoming Call)
    [Tags]     Owner:Aman      Reviewer:Ram       transfer_to_mailbox    fifth
    Given using ${bossPortal} I program ${transferToMailbox} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['transferToMailbox']}
    Then Delete voicemail message on ${inbox} for ${phone3} using ${voicemailPassword}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then On ${phone2} Wait for 15 seconds
    Then disconnect the call from ${phone2}
    Then Login into voicemailBox for ${phone3} using ${voicemailPassword}
    Then Press hardkey as ${scrollRight} on ${phone3}
    Then Verify extension ${number} of ${phone2} on ${phone3}
    Then Press hardkey as ${goodBye} on ${phone3}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4

221446:TC017 Transfer intercom from directory
    [Tags]       Owner:Aman      Reviewer:Ram      transfer_intercom    fifth
    Given using ${bossPortal} I program ${transferIntercom} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with noExtensionValue
    Then On ${phone1} verify display message ${displayMessage['transferIntercom']}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then Answer the call on ${phone1} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then On ${phone1} verify display message >
    Then On ${phone1} verify directory with ${directoryAction['selectOnly']} of ${phone3}
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then Answer the call on ${phone3} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone3}
    Then Verify the Caller id on ${phone2} and ${phone1} display
    Then Verify the Caller id on ${phone3} and ${phone1} display
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4

188434: TC015 Make an outgoing call with speed dial key
    [Tags]     Owner:Aman      Reviewer:Anuj       speed_dial    fifth
    Given using ${bossPortal} I program ${dialNumber} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['dialNumber']}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then On ${phone2} Wait for 3 seconds
    Then Answer the call on ${phone2} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then disconnect the call from ${phone1}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4

188435: TC016 Press the speed dial key to transfer the call
    [Tags]     Owner:Aman      Reviewer:Anuj        speed_dial    fifth
    Given using ${bossPortal} I program ${dialNumber} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['dialNumber']}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then Answer the call on ${phone1} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then on ${phone1} press the softkey ${transfer} in AnswerState
    Then Verify the led state of ${line1} as ${blink} on ${phone1}
    Then On ${phone1} verify display message >
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then On ${phone1} Wait for 2 seconds
    Then Verify the led state of ${line1} as ${blink} on ${phone3}
    Then Answer the call on ${phone3} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone3}
    Then on ${phone1} press the softkey ${transfer} in AnswerState
    Then Verify audio path between ${phone2} and ${phone3}
    Then On ${phone1} verify the softkeys in ${idle}
    Then disconnect the call from ${phone2}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4

188436: TC017 Press the speed dial key to add call to conferenece
    [Tags]     Owner:Aman      Reviewer:Anuj        speed_dial    fifth
    Given using ${bossPortal} I program ${dialNumber} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['dialNumber']}
    Then I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then Answer the call on ${phone2} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then on ${phone1} press the softkey ${Conference} in AnswerState
    Then Verify the led state of ${line1} as ${blink} on ${phone1}
    Then On ${phone1} verify display message >
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then On ${phone1} Wait for 2 seconds
    Then Verify the led state of ${line1} as ${blink} on ${phone3}
    Then On ${phone3} Wait for 2 seconds
    Then Answer the call on ${phone3} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone3}
    Then on ${phone1} press the softkey ${Conference} in ConferenceCallState
    Then conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then disconnect the call from ${phone1}
    Then disconnect the call from ${phone2}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4

188462: TC029 Reboot phone after programming the speed dial keys
    [Tags]     Owner:Aman      Reviewer:Anuj       speed_dial
    Given using ${bossPortal} I program ${dialNumber} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['dialNumber']}
    Then Reboot ${phone1}
    Then On ${phone1} verify display message ${displayMessage['dialNumber']}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4

193273: TC010 outgoing call with speed dial key
    [Tags]     Owner:Aman      Reviewer:Anuj       speed_dial    fifth
    Given using ${bossPortal} I program ${dialNumber} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['dialNumber']}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then Verify the Caller id on ${phone2} and ${phone1} display
    Then Answer the call on ${phone2} using ${loudspeaker}
    Then Verify the led state of ${line5} as ${on} on ${phone1}
    Then disconnect the call from ${phone1}
    Then Verify the led state of ${line5} as ${off} on ${phone1}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4

193275: TC012 Press the speed dial key to transfer the call
    [Tags]     Owner:Aman      Reviewer:Anuj       speed_dial    fifth
    Given using ${bossPortal} I program ${dialNumber} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['dialNumber']}
    Then I want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then Answer the call on ${phone1} using ${loudspeaker}
    Then Verify the Caller id on ${phone3} and ${phone1} display
    Then on ${phone1} press the softkey ${Transfer} in AnswerState
    Then Verify the led state of ${line1} as ${blink} on ${phone1}
    Then On ${phone1} verify display message >
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then On ${phone1} Wait for 4 seconds
    Then Verify the led state of ${line1} as ${blink} on ${phone2}
    Then Verify the led state of ${line5} as ${off} on ${phone1}
    Then Answer the call on ${phone2} using ${loudspeaker}
    Then Verify the led state of ${line5} as ${on} on ${phone1}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then Verify the Caller id on ${phone1} and ${phone3} display
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4

146967: TC06: Program Dial Mailbox
    [Tags]     Owner:Aman      Reviewer:Anuj       dial_mailbox    fifth
    Given using ${bossPortal} I program ${dialMailbox} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['dialMailbox']}
    Then Delete voicemail message on ${inbox} for ${phone2} using ${voicemailPassword}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then On ${phone1} Wait for 50 seconds
    Then Check Connection and disconnect the ${phone1}
    Then Login into voicemailBox for ${phone2} using ${voicemailPassword}
    Then Press hardkey as ${scrollRight} on ${phone2}
    Then on ${phone2} press the softkey ${open} in VoiceMailState
    Then Verify extension ${number} of ${phone1} on ${phone2}
    Then Press hardkey as ${goodBye} on ${phone2}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4

560361: TC02-b: Progbutton Transfer To Mailbox - Without a target extension (Connected Call)
    [Tags]     Owner:Aman      Reviewer:       transfer_to_mailbox    fifth
    Given using ${bossPortal} I program ${transferToMailbox} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['transferToMailbox']}
    Then Delete voicemail message on ${inbox} for ${phone3} using ${voicemailPassword}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then Answer the call on ${phone1} using ${loudspeaker}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then On ${phone1} Wait for 15 seconds
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone1}
    Then Login into voicemailBox for ${phone3} using ${voicemailPassword}
    Then Press hardkey as ${scrollRight} on ${phone3}
    Then On ${phone3} verify display message ${play}
    Then Press hardkey as ${goodBye} on ${phone3}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4
    Given using ${bossPortal} I program ${transferToMailbox} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with noExtensionValue
    Then On ${phone1} verify display message ${displayMessage['transferToMailbox']}
    Then Delete voicemail message on ${inbox} for ${phone3} using ${voicemailPassword}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then Answer the call on ${phone1} using ${loudspeaker}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} enter number ${phone3}
    Then on ${phone1} press the softkey ${ToVm} in TransferState
    Then On ${phone1} Wait for 15 seconds
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone1}
    Then Login into voicemailBox for ${phone3} using ${voicemailPassword}
    Then Press hardkey as ${scrollRight} on ${phone3}
    Then On ${phone3} verify display message ${play}
    Then Press hardkey as ${goodBye} on ${phone3}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4

560362: TC02-c: Progbutton Transfer To Mailbox - Without a target extension (Held call)
    [Tags]     Owner:Aman      Reviewer:       transfer_to_mailbox    fifth
    Given using ${bossPortal} I program ${transferToMailbox} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['transferToMailbox']}
    Then Delete voicemail message on ${inbox} for ${phone3} using ${voicemailPassword}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then Answer the call on ${phone1} using ${loudspeaker}
    Then Press hardkey as ${HoldState} on ${phone1}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then On ${phone1} Wait for 15 seconds
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone1}
    Then Login into voicemailBox for ${phone3} using ${voicemailPassword}
    Then Press hardkey as ${scrollRight} on ${phone3}
    Then On ${phone3} verify display message ${play}
    Then Press hardkey as ${goodBye} on ${phone3}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4
    Given using ${bossPortal} I program ${transferToMailbox} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with noExtensionValue
    Then On ${phone1} verify display message ${displayMessage['transferToMailbox']}
    Then Delete voicemail message on ${inbox} for ${phone3} using ${voicemailPassword}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then Answer the call on ${phone1} using ${loudspeaker}
    Then Press hardkey as ${HoldState} on ${phone1}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} enter number ${phone3}
    Then on ${phone1} press the softkey ${ToVm} in TransferState
    Then On ${phone1} Wait for 15 seconds
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone1}
    Then Login into voicemailBox for ${phone3} using ${voicemailPassword}
    Then Press hardkey as ${scrollRight} on ${phone3}
    Then On ${phone3} verify display message ${play}
    Then Press hardkey as ${goodBye} on ${phone3}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4

557824: Intercom XMON extension
    [Tags]     Owner:Aman      Reviewer:       xmon    fifth
    &{extensionDetails} =  Create Dictionary    ring_delay=1    show_caller_id=only_when_ringing    no_connected=unused    with_connected=unused    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${intercom} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 3 with noExtensionValue
    Then On ${phone1} verify display message ${intercom}
    Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['monitorExtn']}
    Then I want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then Answer the call on ${phone1} using ${loudspeaker}
    Then I want to press line key ${programKey4} on phone ${phone1}
    Then Verify the led state of ${line1} as ${blink} on ${phone1}
    Then Verify the led state of ${line1} as ${on} on ${phone3}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then Verify extension ${number} of ${phone3} on ${phone1}
    Then Verify audio path between ${phone1} and ${phone2}
    Then disconnect the call from ${phone2}
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then disconnect the call from ${phone1}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 3
    And using ${bossPortal} remove the function key on ${phone1} using ${extensionDetails} and softkey position 4

557825:No active calls; press intercom progbutton
    [Tags]     Owner:Aman      Reviewer:       xmon    fifth
    &{extensionDetails} =  Create Dictionary    ring_delay=1    show_caller_id=only_when_ringing    no_connected=unused    with_connected=unused    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${intercom} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 3 with noExtensionValue
    Then On ${phone1} verify display message ${intercom}
    Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['monitorExtn']}
    Then I want to press line key ${programKey4} on phone ${phone1}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then Verify extension ${number} of ${phone2} on ${phone1}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Verify the led state of ${line5} as ${on} on ${phone1}
    Then disconnect the call from ${phone2}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 3
    And using ${bossPortal} remove the function key on ${phone1} using ${extensionDetails} and softkey position 4

557826:Transfer Intercom XMON extension
    [Tags]     Owner:Aman      Reviewer:       xmon    sixth
    &{extensionDetails} =  Create Dictionary    ring_delay=1    show_caller_id=only_when_ringing    no_connected=unused    with_connected=unused    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${transferIntercom} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 3 with noExtensionValue
    Then On ${phone1} verify display message ${displayMessage['transferIntercom']}
    Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['monitorExtn']}
    Then I want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then Answer the call on ${phone1} using ${loudspeaker}
    Then I want to press line key ${programKey4} on phone ${phone1}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then Verify extension ${number} of ${phone2} on ${phone1}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Verify the led state of ${line5} as ${on} on ${phone1}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 3
    And using ${bossPortal} remove the function key on ${phone1} using ${extensionDetails} and softkey position 4

558362: TC013 Mute the Transfer Whisper call
    [Tags]     Owner:Aman      Reviewer:       transfer_whisper    sixth
    Given using ${bossPortal} I program ${transferwhisper} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['transferToWhisper']}
    Then I want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then Answer the call on ${phone1} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone3}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then Verify audio path between ${phone1} and ${phone2}
    Then On ${phone1} verify display message ${transfer}
    Then On ${phone1} verify display message ${drop}
    Then Press hardkey as ${mute} on ${phone1}
    Then Verify one way audio from ${phone2} to ${phone1}
    Then disconnect the call from ${phone1}
    Then disconnect the call from ${phone3}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4

558364: TC015 Pressing 'Transfer Whisper' key in ringing state
    [Tags]     Owner:Aman      Reviewer:       transfer_whisper    sixth
    Given using ${bossPortal} I program ${transferwhisper} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['transferToWhisper']}
    Then I want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then Verify ringing state on ${phone3} and ${phone1}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then Verify ringing state on ${phone3} and ${phone1}
    Then Verify the led state of ${line5} as ${off} on ${phone1}
    Then on ${phone2} verify the softkeys in ${idle}
    Then disconnect the call from ${phone3}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4

558365: TC016 Transfer Whisper Call from directory
    [Tags]     Owner:Aman      Reviewer:       transfer_whisper    sixth
    Given using ${bossPortal} I program ${transferwhisper} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with noExtensionValue
    Then On ${phone1} verify display message ${displayMessage['transferToWhisper']}
    Then I want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then Answer the call on ${phone1} using ${loudspeaker}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then On ${phone1} verify display message >
    Then On ${phone1} verify directory with ${directoryAction['selectOnly']} of ${phone2}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then Verify audio path between ${phone1} and ${phone2}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4

559654: TC009 Program the last softkey as 'dial number(speed dial)'
    [Tags]     Owner:Aman      Reviewer:       speed_dial
    Given using ${bossPortal} I program ${dialNumber} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 5 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['dialNumber']}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 5

559655: TC010 Rename the two softkeys as speed dial with same target extension
    [Tags]     Owner:Aman      Reviewer:       speed_dial    sixth
    Given using ${bossPortal} I program ${dialNumber} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 3 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['dialNumber']}
    Then using ${bossPortal} I program ${dialNumber} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['dialNumber']}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone2} wait for 4 seconds
    Then Answer the call on ${phone2} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Verify the led state of ${line4} as ${on} on ${phone1}
    Then Verify the led state of ${line5} as ${on} on ${phone1}
    Then disconnect the call from ${phone2}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 3
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4

559658: TC013 Speed Dial keys on two phones having same target extension
    [Tags]     Owner:Aman      Reviewer:       speed_dial    sixth
    Given using ${bossPortal} I program ${dialNumber} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['dialNumber']}
    Given using ${bossPortal} I program ${whisperPage} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 3 with extensionValue
    Then On ${phone1} verify display message ${whisperPage}
    Given using ${bossPortal} I program ${dialNumber} on ${phone3} using ${bossDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['dialNumber']}
    Then I want to press line key ${programKey4} on phone ${phone1}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Verify the led state of ${line5} as ${on} on ${phone1}
    Then Verify the led state of ${line5} as ${on} on ${phone3}
    Then disconnect the call from ${phone2}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 3
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4
    And using ${bossPortal} remove the function key on ${phone3} using ${bossDetails} and softkey position 4

559663: TC018 press speed dial key when holding a call
    [Tags]     Owner:Aman      Reviewer:       speed_dial    sixth
    Given using ${bossPortal} I program ${dialNumber} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['dialNumber']}
    Then I want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then Answer the call on ${phone1} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone3}
    Then Press hardkey as ${holdState} on ${phone1}
    Then verify no audio path from ${phone1} to ${phone3}
    Then verify no audio path from ${phone3} to ${phone1}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then Verify ringing state on ${phone1} and ${phone2}
    Then Answer the call on ${phone2} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4

559664: TC019 press speed dial key while being on active call
    [Tags]     Owner:Aman      Reviewer:       speed_dial    sixth
    Given using ${bossPortal} I program ${dialNumber} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['dialNumber']}
    Then I want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then Answer the call on ${phone1} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone3}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then Verify ringing state on ${phone1} and ${phone2}
    Then Verify the led state of ${line1} as ${blink} on ${phone1}
    Then Answer the call on ${phone2} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4


560327:TC007 - Hold call and press blind transfer key
    [Tags]      Owner:Aman      Reviewer:      blind_transfer    sixth
    Given using ${bossPortal} I program ${transferBlind} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['transferBlind']}
    Then I want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then Answer the call on ${phone1} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone3}
    Then Press hardkey as ${holdState} on ${phone1}
    Then verify no audio path from ${phone3} to ${phone1}
    Then verify no audio path from ${phone1} to ${phone3}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then On ${phone1} verify display message ${displayMessage['callTransferred']}
    Then Answer the call on ${phone2} using ${loudspeaker}
    Then Verify audio path between ${phone2} and ${phone3}
    Then on ${phone1} verify the softkeys in ${idle}
    Then disconnect the call from ${phone2}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4

560332:TC012 hang up after pressing the blind transfer key
    [Tags]      Owner:Aman      Reviewer:      blind_transfer    sixth
    Given using ${bossPortal} I program ${transferBlind} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['transferBlind']}
    Then I want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then Answer the call on ${phone1} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone3}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then On ${phone1} verify display message ${displayMessage['callTransferred']}
    Then Press hardkey as ${goodBye} on ${phone1}
    Then Answer the call on ${phone2} using ${loudspeaker}
    Then Verify audio path between ${phone2} and ${phone3}
    Then on ${phone1} verify the softkeys in ${idle}
    Then disconnect the call from ${phone2}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4

559588: Hold the 'Conference Intercom' call
    [Tags]      Owner:Aman      Reviewer:      conference_intercom    sixth
    Given using ${bossPortal} I program ${conferenceIntercom} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['conferenceIntercom']}
    Then I want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then Answer the call on ${phone1} using ${loudspeaker}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then On ${phone1} verify display message ${drop}
    Then On ${phone1} verify display message ${conference}
    Then Press hardkey as ${holdState} on ${phone1}
    Then Verify the led state of ${line1} as ${blink} on ${phone1}
    Then verify no audio path from ${phone1} to ${phone2}
    Then verify no audio path from ${phone2} to ${phone1}
    Then verify no audio path from ${phone1} to ${phone3}
    Then verify no audio path from ${phone3} to ${phone1}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4

559590: Conference Intercom Call from directory
    [Tags]      Owner:Aman      Reviewer:      conference_intercom    sixth
    Given using ${bossPortal} I program ${conferenceIntercom} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with noExtensionValue
    Then On ${phone1} verify display message ${displayMessage['conferenceIntercom']}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then Answer the call on ${phone1} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then On ${phone1} verify display message >
    Then On ${phone1} verify directory with ${directoryAction['selectOnly']} of ${phone3}
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then Verify audio path between ${phone1} and ${phone3}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4

557801: TC031 Holding a HG call
    [Tags]    Owner:Aman    Reviewer:    hunt_group    sixth
    [Setup]    Hunt Group Custom Setup
    @{members}   Create List      ${phone1}    ${phone2}
    &{huntGroupDetails} =  Create Dictionary    BackupExtension=${phone3}    GroupMembers=${members}   GroupName=HG_Aman   IncludeInSystem=True    MakeExtnPrivate=False    HuntPattern=4    RingsPerMember=2    NoAnswerRings=4    CallMemberWhenForwarding=True    SkipMemberOnCall=True    CallStackFull=${EMPTY}    NoAnswer=${EMPTY}
    ${HGExtension} =     using ${bossPortal} I want to create hunt group user extension with ${huntGroupDetails}
    Given on ${phone3} dial number ${HGExtension}
    Then on ${phone1} verify display message ${huntGroupDetails['GroupName']}
    Then on ${phone2} verify display message ${huntGroupDetails['GroupName']}
    Then answer the call on ${phone1} using ${loudSpeaker}
    Then Verify audio path between ${phone1} and ${phone3}
    Then Press hardkey as ${holdState} on ${phone1}
    Then Verify the led state of ${line1} as ${blink} on ${phone1}
    Then disconnect the call from ${phone3}
    And using ${bossPortal} I want to remove hunt group user extension ${HGExtension}
    [Teardown]    Hunt Group Custom Teardown

557802: TC032 Transfer the HG Call
    [Tags]    Owner:Aman    Reviewer:         hunt_group      notApplicableForMiCloud    sixth
    [Setup]    Hunt Group Custom Setup
    @{members}   Create List      ${phone1}    ${phone2}
    &{huntGroupDetails} =  Create Dictionary    BackupExtension=${phone3}    GroupMembers=${members}   GroupName=HG_Aman   IncludeInSystem=True    MakeExtnPrivate=False    HuntPattern=4    RingsPerMember=2    NoAnswerRings=4    CallMemberWhenForwarding=True    SkipMemberOnCall=True    CallStackFull=${EMPTY}    NoAnswer=${EMPTY}
    ${HGExtension} =     using ${bossPortal} I want to create hunt group user extension with ${huntGroupDetails}
    Given on ${phone3} dial number ${HGExtension}
    Then on ${phone1} verify display message ${huntGroupDetails['GroupName']}
    Then on ${phone2} verify display message ${huntGroupDetails['GroupName']}
    Then answer the call on ${phone1} using ${loudSpeaker}
    Then Verify audio path between ${phone1} and ${phone3}
    Then Transfer call from ${phone1} to ${phone2} using ${blindTransfer}
    Then Verify the Caller id on ${phone2} and ${phone3} display
    Then disconnect the call from ${phone3}
    And using ${bossPortal} I want to remove hunt group user extension ${HGExtension}
    [Teardown]    Hunt Group Custom Teardown

561574: TC01: key display after pressing # key
    [Tags]    Owner:Aman    Reviewer:    soft_key_verify      notApplicableForMiCloud    sixth
    Given using ${bossPortal} I want to change Delay after collecting digits value to 6000
    Then on ${phone1} dial number #
    Then On ${phone1} verify display message ${dial}
    Then On ${phone1} verify display message ${backSpace}
    Then On ${phone1} verify display message ${cancel}
    Then press hardkey as ${goodBye} on ${phone1}
    Then Press hookMode ${offHook} on phone ${phone1}
    Then on ${phone1} dial number #
    Then On ${phone1} verify display message ${dial}
    Then On ${phone1} verify display message ${backSpace}
    Then On ${phone1} verify display message ${cancel}
    Then press hardkey as ${goodBye} on ${phone1}
    And using ${bossPortal} I want to change Delay after collecting digits value to 3000
    [Teardown]    Telephony Options Custom Teardown

558085: Barge In with permissions, target idle
    [Tags]    Owner:Aman    Reviewer:Anuj    cos    sixth
    &{COSDetails} =  Create Dictionary    Name=${fullyFeatured}     AcceptBargeInDN1=True    BargeInAccept=0
    Given using ${bossPortal} I want to change telephony features values using ${COSDetails}
    Then on ${phone1} verify the softkeys in ${idle}
    Then i want to make a two party call between ${phone3} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then Press hookMode ${offHook} on phone ${phone1}
    Then I want to use fac Bargein on ${phone1} to ${phone2}
    Then on ${phone1} verify display message ${bargeIn}
    Then On ${phone1} verify display message ${displayMessage['notPermit']}
    Then disconnect the call from ${phone3}
    [Teardown]    CoS Features Custom Teardown

558086: Barge In with permissions, target on a call
    [Tags]    Owner:Aman    Reviewer:Anuj    cos    sixth
    &{COSDetails} =  Create Dictionary    Name=${fullyFeatured}     AcceptBargeInDN1=True    BargeInAccept=1
    Given using ${bossPortal} I want to change telephony features values using ${COSDetails}
    Then i want to make a two party call between ${phone3} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then Press hookMode ${offHook} on phone ${phone1}
    Then I want to use fac Bargein on ${phone1} to ${phone2}
    Then conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then verify extension ${number} of ${phone2} on ${phone1}
    Then verify extension ${number} of ${phone3} on ${phone1}
    Then verify extension ${number} of ${phone1} on ${phone2}
    Then verify extension ${number} of ${phone3} on ${phone2}
    Then verify extension ${number} of ${phone1} on ${phone3}
    Then verify extension ${number} of ${phone2} on ${phone3}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}
    [Teardown]    CoS Features Custom Teardown

562016: Disable SC, SM and BI from Mitel Director; select SC, SM, BI in Connect Client
    [Tags]    Owner:Aman    Reviewer:Anuj    cos      notApplicableForMiCloud    sixth
    &{COSDetails} =  Create Dictionary    Name=${fullyFeatured}     AllowBargeInInitiation=False      BargeInAccept=0    AllowSilentMonitorInitiation=False    SilentMonitorAccept=0
    Given using ${bossPortal} I want to change telephony features values using ${COSDetails}
    Then i want to make a two party call between ${phone3} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then I want to use fac Bargein on ${phone1} to ${phone2}
    Then on ${phone1} verify display message ${bargeIn}
    Then On ${phone1} verify display message ${displayMessage['notPermit']}
    Then Press hardkey as ${goodBye} on ${phone1}
    Then I want to use fac Silentmonitor on ${phone1} to ${phone2}
    Then on ${phone1} verify display message ${silentMonitor}
    Then On ${phone1} verify display message ${displayMessage['notPermit']}
    Then Press hardkey as ${goodBye} on ${phone1}
    Then I want to use fac Silentcoach on ${phone1} to ${phone2}
    Then on ${phone1} verify display message ${silentCoach}
    Then On ${phone1} verify display message ${displayMessage['notPermit']}
    Then disconnect the call from ${phone3}
    [Teardown]    CoS Features Custom Teardown

558731: Outbound call from BCA - Make me conf - hold
    [Tags]    Owner:Aman    Reviewer:    BCA    sixth
    [Setup]    BCA Custom Setup
    &{createBCAExtension1} =  Create Dictionary    name=bca_Aman1   backupExtn=${phone2}    switch=2    callStackDepth=2    forwardAfter=2    callStackFull=${EMPTY}   noAnswer=${EMPTY}    outboundCallerID=${EMPTY}    allowBridgeConferencing=true   defaultPrivacySettings=0
    &{createBCAExtension2} =  Create Dictionary    name=bca_Aman2   backupExtn=${phone3}    switch=2    callStackDepth=2    forwardAfter=2    callStackFull=${EMPTY}   noAnswer=${EMPTY}    outboundCallerID=${EMPTY}    allowBridgeConferencing=true   defaultPrivacySettings=0
    &{createBCAExtension3} =  Create Dictionary    name=bca_Aman3   backupExtn=${phone4}    switch=2    callStackDepth=2    forwardAfter=2    callStackFull=${EMPTY}   noAnswer=${EMPTY}    outboundCallerID=${EMPTY}    allowBridgeConferencing=true   defaultPrivacySettings=0
    &{createBCAExtension4} =  Create Dictionary    name=bca_Aman4   backupExtn=${phone5}    switch=2    callStackDepth=2    forwardAfter=2    callStackFull=${EMPTY}   noAnswer=${EMPTY}    outboundCallerID=${EMPTY}    allowBridgeConferencing=true   defaultPrivacySettings=0

    ${bcaExtn1}=    using ${bossPortal} I want to create Bridge Call Appearance extension using ${createBCAExtension1}
    ${bcaExtn2}=    using ${bossPortal} I want to create Bridge Call Appearance extension using ${createBCAExtension2}
    ${bcaExtn3}=    using ${bossPortal} I want to create Bridge Call Appearance extension using ${createBCAExtension3}
    ${bcaExtn4}=    using ${bossPortal} I want to create Bridge Call Appearance extension using ${createBCAExtension4}

    &{BCAdetails1} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=3    function=Bridge Call Appearance    label=BCA    target_extension=${bcaExtn1}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${phone5}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=Dial Extension
    &{BCAdetails2} =  Create Dictionary    user_extension=${phone2}    button_box=0    soft_key=3    function=Bridge Call Appearance    label=BCA    target_extension=${bcaExtn1}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${phone5}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=Dial Extension
    &{BCAdetails3} =  Create Dictionary    user_extension=${phone3}    button_box=0    soft_key=3    function=Bridge Call Appearance    label=BCA    target_extension=${bcaExtn1}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${phone5}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=Dial Extension
    &{BCAdetails4} =  Create Dictionary    user_extension=${phone4}    button_box=0    soft_key=3    function=Bridge Call Appearance    label=BCA    target_extension=${bcaExtn1}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${phone5}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=Dial Extension

    Given using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails1}
    Then using ${bossPortal} I want to create bca on ${phone2} using ${BCAdetails2}
    Then using ${bossPortal} I want to create bca on ${phone3} using ${BCAdetails3}
    Then using ${bossPortal} I want to create bca on ${phone4} using ${BCAdetails4}
    Then on ${phone1} verify display message BCA
    Then on ${phone2} verify display message BCA
    Then on ${phone3} verify display message BCA
    Then on ${phone4} verify display message BCA
    Then I want to press line key ${programKey4} on phone ${phone1}
    Then answer the call on ${phone5} using ${loudSpeaker}
    Then Verify audio path between ${phone1} and ${phone5}
    Then verify the led state of ${line4} as ${on} on ${phone2}
    Then on ${phone2} verify the softkeys in ${idle}
    Then verify the led state of ${line4} as ${on} on ${phone3}
    Then on ${phone3} verify the softkeys in ${idle}
    Then verify the led state of ${line4} as ${on} on ${phone4}
    Then on ${phone4} verify the softkeys in ${idle}
    Then I want to press line key ${programKey4} on phone ${phone2}
    Then On ${phone3} Wait for 3 seconds
    Then I want to press line key ${programKey4} on phone ${phone3}
    Then On ${phone4} Wait for 3 seconds
    Then I want to press line key ${programKey4} on phone ${phone4}
    Then four party conference call audio verification between ${phone1} ${phone2} ${phone3} and ${phone4}
    Then on ${phone1} press the softkey ${show} in ConferenceCallState
    Then verify extension ${number} of ${phone2} on ${phone1}
    Then verify extension ${number} of ${phone3} on ${phone1}
    Then verify extension ${number} of ${phone4} on ${phone1}
    Then verify extension ${number} of ${phone5} on ${phone1}
    Then verify the led state of ${line4} as ${on} on ${phone1}
    Then verify the led state of ${line4} as ${on} on ${phone2}
    Then verify the led state of ${line4} as ${on} on ${phone3}
    Then verify the led state of ${line4} as ${on} on ${phone4}
    Then press hardkey as ${holdState} on ${phone1}
    Then conference call audio verify between ${phone2} ${phone3} and ${phone4}
    Then verify the led state of ${line4} as ${blink} on ${phone1}
    Then press hardkey as ${holdState} on ${phone2}
    Then Verify audio path between ${phone3} and ${phone4}
    Then verify the led state of ${line4} as ${blink} on ${phone1}
    Then verify the led state of ${line4} as ${blink} on ${phone2}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}
    Then disconnect the call from ${phone4}
    Then disconnect the call from ${phone5}
    Then using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4
    Then using ${bossPortal} I want to delete Bridge Call Appearance extension using ${bcaExtn1}
    Then using ${bossPortal} remove the function key on ${phone2} using ${bossDetails} and softkey position 4
    Then using ${bossPortal} I want to delete Bridge Call Appearance extension using ${bcaExtn2}
    Then using ${bossPortal} remove the function key on ${phone3} using ${bossDetails} and softkey position 4
    Then using ${bossPortal} I want to delete Bridge Call Appearance extension using ${bcaExtn3}
    Then using ${bossPortal} remove the function key on ${phone4} using ${bossDetails} and softkey position 4
    And using ${bossPortal} I want to delete Bridge Call Appearance extension using ${bcaExtn4}
    [Teardown]    BCA Custom Teardown

560120: Press Hold prior to pressing Park or progbutton (1 call on hold)
    [Tags]    Owner:Aman    Reviewer:    park    sixth
    Given using ${bossPortal} I program ${park} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with ExtensionValue
    Then on ${phone1} verify display message ${park}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then press hardkey as ${holdState} on ${phone1}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then Verify the Caller id on ${phone2} and ${phone3} display
    Then Verify the led state of ${line5} as ${on} on ${phone1}
    Then disconnect the call from ${phone2}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4

559005: Boss1 calls Boss2, Boss3 calls Boss1, Boss 1 can join.Boss2 gets call from boss4, join.
    [Tags]      Owner:Aman      Reviewer:      sca    notApplicableForMiCloud    seventh
    [Setup]    Telephony Feature Custom Setup
    &{telephonydetails} =  Create Dictionary    sca_enabled=True
    ${scaExtn1} =  using ${bossPortal} on ${phone1} I want to enable SCA using ${telephonydetails}
    ${scaExtn2} =  using ${bossPortal} on ${phone2} I want to enable SCA using ${telephonydetails}
    ${scaExtn3} =  using ${bossPortal} on ${phone3} I want to enable SCA using ${telephonydetails}
    ${scaExtn4} =  using ${bossPortal} on ${phone4} I want to enable SCA using ${telephonydetails}

    Given on ${phone1} dial number ${scaExtn2}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then press hardkey as ${holdState} on ${phone1}
    Then on ${phone3} dial number ${scaExtn1}
    Then answer the call on ${phone1} using ${programKey2}
    Then on ${phone1} press the softkey ${conference} in AnswerState
    Then I want to press line key ${programKey1} on phone ${phone1}
    Then verify the led state of ${line2} as ${off} on ${phone1}
    Then conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then press hardkey as ${holdState} on ${phone2}
    Then on ${phone4} dial number ${scaExtn2}
    Then answer the call on ${phone2} using ${programKey2}
    Then on ${phone2} press the softkey ${conference} in AnswerState
    Then I want to press line key ${programKey1} on phone ${phone2}
    Then four party conference call audio verification between ${phone1} ${phone2} ${phone3} and ${phone4}
    Then disconnect the call from ${phone1}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}

    &{telephonydetails} =  Create Dictionary    sca_enabled=False
    ${scaExtn1} =  using ${bossPortal} on ${phone1} I want to disable SCA using ${telephonydetails}
    ${scaExtn2} =  using ${bossPortal} on ${phone1} I want to disable SCA using ${telephonydetails}
    ${scaExtn3} =  using ${bossPortal} on ${phone1} I want to disable SCA using ${telephonydetails}
    ${scaExtn4} =  using ${bossPortal} on ${phone1} I want to disable SCA using ${telephonydetails}
    [Teardown]    Telephony Feature Custom Teardown

558973: Admin SCA calls A, Admin hotline calls Boss, Admin joins
    [Tags]    Owner:Aman    Reviewer:    SCA    notApplicableForMiCloud    seventh
    [Setup]    Telephony Feature Custom Setup
    &{telephonydetails} =  Create Dictionary    sca_enabled=True
    ${scaExtn1} =  using ${bossPortal} on ${phone2} I want to enable SCA using ${telephonydetails}
    &{hotlines}    CREATE DICTIONARY    ConnectedCallFunctionID=dial number    account_name=Automation    part_name=SC1    button_box=0
    &{BCAdetails1} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=3    function=Bridge Call Appearance    label=BCA    target_extension=${scaExtn1}    RingDelayBeforeAlert=0      CallStackPosition=1      SecondaryType=Dial Tone
    Given using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails1}
    Then using ${bossPortal} I program ${hotline} on ${phone1} using ${hotlines} and extension of ${phone2} and softkey position 4 with extensionValue
    Then on ${phone1} verify display message ${hotline}
    Then I want to make a two party call between ${phone1} and ${phone3} using ${programKey4}
    Then answer the call on ${phone3} using ${loudspeaker}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone2} wait for 3 seconds
    Then answer the call on ${phone2} using ${programKey1}
    Then i want to verify on ${phone1} negative display message ${conference}
    Then i want to verify on ${phone1} negative display message ${merge}
    Then disconnect the call from ${phone1}
    Then disconnect the call from ${phone2}
    Then using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 3
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4
    &{telephonydetails} =  Create Dictionary    sca_enabled=False
    ${scaExtn1} =  using ${bossPortal} on ${phone2} I want to disable SCA using ${telephonydetails}
    [Teardown]    Telephony Feature Custom Teardown

754456: XMON, CID Never - multiple held calls on target, no incoming calls
    [Tags]    Owner:Aman        Reviewer:       xmon    seventh
    &{extensionDetails} =    Create Dictionary    ring_delay=dont_ring    show_caller_id=never    no_connected=unused    with_connected=unused    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then on ${phone1} verify display message ${displayMessage['monitorExtn']}
    Then i want to make a two party call between ${phone3} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then i want to make a two party call between ${phone4} and ${phone2} using ${loudspeaker}
    Then I want to press line key ${programKey2} on phone ${phone2}
    Then press hardkey as ${holdState} on ${phone2}
    Then verify the led state of ${line1} as ${blink} on ${phone2}
    Then verify the led state of ${line2} as ${blink} on ${phone2}
    Then On ${phone1} verify ${line5} icon state as ${xmonHold}
    Then On ${phone1} verify the led state of ${line5} as ${blink} and led color as ${red}
    Then I want to verify on ${phone1} negative display message ${phone3}
    Then I want to verify on ${phone1} negative display message ${phone4}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} verify display message ${unpark}
    Then on ${phone1} verify display message ${cancel}
    Then on ${phone1} verify display message Call 1
    Then I want to verify on ${phone1} negative display message ${phone3}
    Then on ${phone1} Press ${hardkey} ${scrollDown} for 1 times
    Then on ${phone1} verify display message Call 2
    Then I want to verify on ${phone1} negative display message ${phone4}
    Then on ${phone1} Press ${softKey} ${bottomKey1} for 1 times
    Then Verify audio path between ${phone1} and ${phone4}
    Then Verify extension ${number} of ${phone4} on ${phone1}
    Then On ${phone1} verify ${line5} icon state as ${xmonBusy}
    Then On ${phone1} verify the led state of ${line5} as ${blink} and led color as ${red}
    Then I want to verify on ${phone2} negative display message ${phone4}
    Then verify extension ${number} of ${phone3} on ${phone2}
    Then verify the led state of ${line1} as ${blink} on ${phone2}
    Then I want to Park the call from ${phone1} on ${phone2} using ${default} and ${Park}
    Then On ${phone1} verify the softkeys in ${idleState}
    Then I want to press line key ${programKey2} on phone ${phone2}
    Then press hardkey as ${holdState} on ${phone2}
    Then i want to make a two party call between ${phone5} and ${phone2} using ${loudspeaker}
    Then I want to press line key ${programKey3} on phone ${phone2}
    Then verify the led state of ${line1} as ${blink} on ${phone2}
    Then verify the led state of ${line2} as ${blink} on ${phone2}
    Then verify the led state of ${line3} as ${on} on ${phone2}
    Then On ${phone1} verify ${line5} icon state as ${xmonBusyHold}
    Then On ${phone1} verify the led state of ${line5} as ${blink} and led color as ${red}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} verify display message ${unpark}
    Then on ${phone1} verify display message ${cancel}
    Then on ${phone1} verify display message Call 1
    Then I want to verify on ${phone1} negative display message ${phone3}
    Then on ${phone1} Press ${hardkey} ${scrollDown} for 1 times
    Then on ${phone1} verify display message ${unpark}
    Then on ${phone1} verify display message ${cancel}
    Then on ${phone1} verify display message Call 2
    Then I want to verify on ${phone1} negative display message ${phone4}
    Then on ${phone1} Press ${hardkey} ${scrollDown} for 1 times
    Then i want to verify on ${phone1} negative display message ${unpark}
    Then on ${phone1} verify display message Call 3
    Then I want to verify on ${phone1} negative display message ${phone5}
    Then on ${phone1} Press ${hardkey} ${scrollUp} for 2 times
    Then on ${phone1} Press ${softKey} ${bottomKey1} for 1 times
    Then On ${phone1} verify ${line5} icon state as ${xmonBusy}
    Then verify extension ${number} of ${phone3} on ${phone1}
    Then on ${phone1} verify the led state of ${line5} as ${blink} and led color as ${red}
    Then disconnect the call from ${phone1}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone4}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4


753640: Admin makes 2 way conf on SCA line1, Boss BCA Confs conf, admin leaves-no dialog, boss leaves-dialog answers no.
    [Tags]    Owner:Aman        Reviewer:       bca    seventh
    [Setup]   Telephony Feature Custom Setup
    &{telephonydetails} =  Create Dictionary    sca_enabled=True
    ${scaExtn} =  using ${bossPortal} on ${phone2} I want to enable SCA using ${telephonydetails}
    &{createBCAExtension1} =  Create Dictionary    extension=${scaExtn}    backupExtn=${phone1}    allowBridgeConferencing=true   defaultPrivacySettings=0
    ${bcaExtn}=    using ${bossPortal} I want to modify Bridge Call Appearance extension using ${createBCAExtension1}
    &{BCAdetails} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=4    function=Bridge Call Appearance    label=BCA    target_extension=${bcaExtn}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${EMPTY}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=${EMPTY}
    Given using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails}
    Then on ${phone1} verify display message ${bca}
    Then I want to make a two party call between ${phone1} and ${phone3} using ${programkey5}
    Then answer the call on ${phone3} using ${loudSpeaker}
    Then I want to make a conference call between ${phone1},${phone3} and ${phone4} using ${consultiveConference}
    Then i want to press line key ${programKey1} on phone ${phone2}
    Then on ${phone1} Press ${softKey} ${bottomKey1} for 1 times
    Then Verify the led state of ${line5} as ${on} on ${phone1}
    Then on ${phone2} Press ${softKey} ${bottomKey1} for 1 times
    Then Verify the led state of ${line5} as ${off} on ${phone1}
    And disconnect the call from ${phone4}
    ${scaExtn} =  using ${bossPortal} on ${phone2} I want to disable SCA using ${telephonydetails}
    [Teardown]    Telephony Feature Custom Teardown

753250: attempt barge in with no main screen focus
    [Tags]    Owner:Aman        Reviewer:       barge_in    seventh
    &{COSDetails} =  Create Dictionary    Name=${fullyFeatured}     AllowBargeInInitiation=True      BargeInAccept=1
    Given using ${bossPortal} I want to change telephony features values using ${COSDetails}
    Then using ${bossPortal} I program ${bargeIn} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then on ${phone1} verify display message ${bargeIn}
    Then i want to make a two party call between ${phone2} and ${phone3} using ${loudspeaker}
    Then answer the call on ${phone3} using ${loudspeaker}
    Then Verify audio path between ${phone2} and ${phone3}
    Then Verify the led state of ${line5} as ${on} on ${phone1}
    Then press hardkey as ${directory} on ${phone1}
    Then on ${phone1} verify display message ${directory}
    Then Verify the led state of ${line5} as ${off} on ${phone1}
    Then i want to verify on ${phone1} negative display message ${bargeIn}
    Then i want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} verify display message ${directory}
    Then Verify the led state of ${line5} as ${off} on ${phone1}
    Then press hardkey as ${goodbye} on ${phone1}
    Then disconnect the call from ${phone2}
    Then using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4
    &{COSDetails} =  Create Dictionary    Name=${fullyFeatured}
    And using ${bossPortal} I want to change telephony features values using ${COSDetails}
    [Teardown]    CoS Features Custom Teardown

759684: LED Buttons- Toggle Functions- Whisper Page Mute- Active
    [Tags]    Owner:Aman        Reviewer:       PKM    seventh
    Given using ${bossPortal} I program ${whisperPageMute} on ${phone1} using ${bossDetailsPKM} and extension of ${phone2} and softkey position 4 with noExtensionValue
    Then verify display message ${whisperPage} on PKM for ${phone1}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then press hardkey as ${offhook} on ${phone3}
    Then I want to use fac ${whisperPageFAC} on ${phone3} to ${phone1}
    Then Verify audio path between ${phone1} and ${phone3}
    Then Verify the PKM led state of ${programKey5} as ${on} on ${phone1}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetailsPKM} and softkey position 4

759717: TC006 Configure any random key as mobile line key
    [Tags]    Owner:Aman        Reviewer:       mobileLine    seventh
    Given using ${bossPortal} I program ${mobileLine} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with noExtensionValue
    Then On ${phone1} verify display message ${displayMessage['connect']}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then On ${phone1} verify display message ${displayMessage['bluetooth']}
    Then press hardkey as ${goodBye} on ${phone1}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4

753638: Admin makes 2 way conf on SCA line1, Admin leaves, gets dialog, parks call, B leaves, Admin unholds has audio to A.
    [Tags]    Owner:Aman        Reviewer:       bca    seventh
    [Setup]   Telephony Feature Custom Setup
    &{telephonydetails} =  Create Dictionary    sca_enabled=True
    ${scaExtn} =  using ${bossPortal} on ${phone2} I want to enable SCA using ${telephonydetails}
    &{createBCAExtension1} =  Create Dictionary    extension=${scaExtn}    backupExtn=${phone4}    allowBridgeConferencing=true   defaultPrivacySettings=0
    ${bcaExtn}=    using ${bossPortal} I want to modify Bridge Call Appearance extension using ${createBCAExtension1}
    &{BCAdetails} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=4    function=Bridge Call Appearance    label=BCA    target_extension=${bcaExtn}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${EMPTY}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=${EMPTY}
    Given using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails}
    Then on ${phone1} verify display message ${bca}
    Then I want to make a two party call between ${phone1} and ${phone3} using ${programkey5}
    Then answer the call on ${phone3} using ${loudSpeaker}
    Then I want to make a conference call between ${phone1},${phone3} and ${phone4} using ${consultiveConference}
    Then on ${phone1} press the softkey ${leave} in ConferenceCallState
    Then On ${phone1} verify the softkeys in ${idleState}
    Then I want to Park the call from ${phone4} on ${scaExtn} using ${default} and ${Park}
    Then On ${phone3} verify the softkeys in ${idleState}
    Then Verify the Caller id on ${phone1} and ${phone3} display
    Then press hardkey as ${holdState} on ${phone1}
    Then disconnect the call from ${phone1}
    Then On ${phone1} verify the softkeys in ${idleState}
    ${scaExtn} =  using ${bossPortal} on ${phone2} I want to disable SCA using ${telephonydetails}
    [Teardown]    Telephony Feature Custom Teardown

752451: HQ user - A calls B - A consult transfers calls to C - C holds the Call
    [Tags]    Owner:Aman        Reviewer:       MOH    seventh    notApplicableForMiCloud
    &{MOHFeatures}    option=1    filename='MOH'
    Given using ${bossPortal} I want to enable MOH features using ${MOHFeatures}
    Then i want to make a two party call between ${phone2} and ${phone3} using ${loudspeaker}
    Then answer the call on ${phone3} using ${loudspeaker}
    Then Verify audio path between ${phone2} and ${phone3}
    Then Transfer call from ${phone2} to ${phone1} using ${consultiveTransfer}
    Then press hardkey as ${holdState} on ${phone1}
    Then verify MOH audio on ${phone1}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}
    &{MOHFeatures}    option=0
    And using ${bossPortal} I want to disable MOH features using ${MOHFeatures}


752450: HQ user - A calls B - B blind transfers call to C - C parks the call
    [Tags]    Owner:Aman        Reviewer:       MOH    seventh
    Then i want to make a two party call between ${phone2} and ${phone3} using ${loudspeaker}
    Then answer the call on ${phone3} using ${loudspeaker}
    Then Verify audio path between ${phone2} and ${phone3}
    Then Transfer call from ${phone3} to ${phone1} using ${blindTransfer}
    Then on ${phone1} press the softkey ${park} in AnswerState
    Then verify MOH audio on ${phone1}
    Then on ${phone1} enter number ${phone3}
    Then on ${phone1} wait for 2 seconds
    Then verify the caller id on ${phone2} and ${phone3} display
    Then On ${phone1} verify the softkeys in ${IdleState}
    Then disconnect the call from ${phone2}

227254: Dropping a Consult Conference call
    [Tags]    Owner:Anuj      Reviewer:Ram      Conference    seventh
    Given using ${bossPortal} I program ${ConferenceConsultative} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with noExtensionValue
    Then On ${phone1} verify display message ${displayMessage['conferenceConsult']}
    Then I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then Answer the call on ${phone2} using ${loudSpeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} enter number ${phone3}
    Then on ${phone1} wait for 2 seconds
    Then Verify extension ${number} of ${phone1} on ${phone3}
    Then Answer the call on ${phone3} using ${loudSpeaker}
    Then Verify audio path between ${phone1} and ${phone3}
    Then On ${phone1} verify display message ${Drop}
    Then On ${phone1} verify display message ${Conference}
    Then on ${phone1} press the softkey ${Drop} in ConferenceCallState
    Then on ${phone3} verify the softkeys in ${IdleState}
    Then verify no audio path from ${phone1} to ${phone2}
    Then verify no audio path from ${phone2} to ${phone1}
    Then disconnect the call from ${phone2}

227737:Press 'Conference Consult' key in Idle state
    [Tags]      Owner:Anuj     Reviewer:Avishek    Conference    seventh
    Given using ${bossPortal} I program ${ConferenceConsultative} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage["conferenceConsult"]}
    Then on ${phone1} verify the softkeys in ${IdleState}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} verify the softkeys in ${IdleState}

227937:Press 'Conference Intercom' key in Idle state
    [Tags]      Owner:Anuj     Reviewer:Avishek    Conference    seventh
    Given using ${bossPortal} I program ${ConferenceIntercom} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['conferenceIntercom']}
    Then on ${phone1} verify the softkeys in ${IdleState}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} verify the softkeys in ${IdleState}


227929:Dropping Intercom Conference call
    [Tags]     Owner:Anuj     Reviewer:Avishek    Conference    seventh
    Given using ${bossPortal} I program ${ConferenceIntercom} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with noExtensionValue
    Then On ${phone1} verify display message ${displayMessage['conferenceIntercom']}
    Then I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then Answer the call on ${phone2} using ${loudSpeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then on ${phone1} verify display message >
    Then on ${phone1} enter number ${phone3}
    Then on ${phone1} wait for 2 seconds
    Then Verify audio path between ${phone1} and ${phone3}
    Then on ${phone1} wait for 2 seconds
    Then on ${phone1} press the softkey ${Drop} in ConferenceCallState
    Then on ${phone3} verify the softkeys in ${IdleState}
    Then verify no audio path from ${phone1} to ${phone2}
    Then verify no audio path from ${phone2} to ${phone2}
    Then disconnect the call from ${phone2}

231460:Blind Conference target disconnect the call
    [Tags]      Owner:Anuj     Reviewer:    Conference    seventh
    Given using ${bossPortal} I program ${conferenceBlind} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['conferenceBlind']}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then Answer the call on ${phone1} using ${loudSpeaker}
    Then Verify audio path between ${phone2} and ${phone1}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then Answer the call on ${phone3} using ${loudSpeaker}
    Then on ${phone1} wait for 2 seconds
    Then Conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then press hardkey as ${goodbye} on ${phone3}
    Then Verify audio path between ${phone1} and ${phone2}
    Then disconnect the call from ${phone2}

227736:Program multiple 'Conference Consult' keys on phone
    [Tags]      Owner:Anuj       Reviewer:     Conference    seventh
    Given using ${bossPortal} I program ${ConferenceConsultative} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 2 with extensionValue
    Given using ${bossPortal} I program ${ConferenceConsultative} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 3 with extensionValue
    Given using ${bossPortal} I program ${ConferenceConsultative} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['conferenceConsult']}
    Then I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then Answer the call on ${phone2} using ${loudSpeaker}
    Then Verify audio path between ${phone2} and ${phone1}
    Then I want to press line key ${programKey4} on phone ${phone1}
    Then On ${phone1} Wait for 2 seconds
    Then Answer the call on ${phone3} using ${loudSpeaker}
    Then Verify audio path between ${phone3} and ${phone1}
    Then Verify the led state of ${line3} as ${on} on ${phone1}
    Then Verify the led state of ${line4} as ${on} on ${phone1}
    Then Verify the led state of ${line5} as ${on} on ${phone1}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone1}

146950:Supervisor disconnects after Agent Joins Conference during Silent Monitor
    [Tags]      Owner:Anuj       Reviewer:         Silent_Monitor    seventh
    Given using ${bossPortal} I program ${silentMonitor} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 1 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['silentMonitor']}
    Then I want to make a two party call between ${phone2} and ${phone3} using ${loudspeaker}
    Then Answer the call on ${phone3} using ${loudSpeaker}
    Then Verify audio path between ${phone3} and ${phone2}
    Then I want to press line key ${programKey2} on phone ${phone1}
    Then Verify one way audio from ${phone2} to ${phone1}
    Then Verify one way audio from ${phone3} to ${phone1}
    Then verify no audio path from ${phone1} to ${phone2}
    Then verify no audio path from ${phone1} to ${phone3}
    Then Put the linekey ${line1} of ${phone2} on ${hold}
    Then I want to make a two party call between ${phone4} and ${phone2} using ${loudspeaker}
    Then I want to press line key ${programKey2} on phone ${phone2}
    Then Verify audio path between ${phone4} and ${phone2}
    Then on ${phone2} press the softkey ${merge} in ConferenceCallState
    Then Conference call audio verify between ${phone4} ${phone3} and ${phone2}
    Then on ${phone1} verify the softkeys in ${IdleState}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}

127824:Progbutton Transfer Consultative destination configured (call not answered)
    [Tags]      Owner:Anuj     Reviewer:    Transfer    seventh
    Given using ${bossPortal} I program ${Transfer Consultative} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['transferConsult']}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then On ${phone1} verify display message ${Answer}

195208:Cancel the answered transfer Consultative call
    [Tags]      Owner:Anuj     Reviewer:    Transfer    seventh
    Given using ${bossPortal} I program ${Transfer Consultative} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['transferConsult']}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then Answer the call on ${phone1} using ${loudSpeaker}
    Then Verify audio path between ${phone2} and ${phone1}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then On ${phone1} Wait for 2 seconds
    Then On ${phone1} verify display message ${RingingState}
    Then answer the call on ${phone3} using ${loudSpeaker}
    Then Verify audio path between ${phone3} and ${phone1}
    Then on ${phone1} press the softkey ${Drop} in AnswerState
    Then I want to press line key ${programKey1} on phone ${phone1}
    Then Verify audio path between ${phone2} and ${phone1}
    Then disconnect the call from ${phone2}

195210:press the transfer consultative key on idle screen
    [Tags]      Owner:Anuj     Reviewer:    Transfer    seventh
    Given using ${bossPortal} I program ${Transfer Consultative} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['transferConsult']}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} verify the softkeys in ${IdleState}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} verify the softkeys in ${IdleState}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} verify the softkeys in ${IdleState}

195211:Targeted phone hang up the answered transfer consult call
    [Tags]      Owner:Anuj     Reviewer:    Transfer    eightth
    Given using ${bossPortal} I program ${transferConsultative} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['transferConsult']}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then Answer the call on ${phone1} using ${loudSpeaker}
    Then Verify audio path between ${phone2} and ${phone1}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then On ${phone1} Wait for 2 seconds
    Then answer the call on ${phone3} using ${loudSpeaker}
    Then Verify audio path between ${phone3} and ${phone1}
    Then verify the led state of ${line1} as ${on} on ${phone2}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then press hardkey as ${goodbye} on ${phone1}
    Then on ${phone1} verify the softkeys in ${IdleState}
    Then disconnect the call from ${phone2}

147236:Park call to DID or System Extension
    [Tags]      Owner:Anuj     Reviewer:     park    eightth
    Given using ${bossPortal} I program ${park} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${park}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then Verify audio path between ${phone2} and ${phone1}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then On ${phone1} Wait for 10 seconds
    Then on ${phone1} verify the softkeys in ${IdleState}
    Then Verify extension ${number} of ${phone2} on ${phone3}
    Then disconnect the call from ${phone2}

147250:Park&Page button while idle
    [Tags]      Owner:Anuj     Reviewer:    park    eightth
    Given using ${bossPortal} I program ${park} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${park}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} verify the softkeys in ${IdleState}


147272:TC01: Pickup call
    [Tags]      Owner:Anuj     Reviewer:     pickup    eightth
    Given using ${bossPortal} I program ${pickupUnpark} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${pickAndUnpar}
    Then I want to make a two party call between ${phone2} and ${phone3} using ${loudspeaker}
    Then Verify ringing state on ${phone2} and ${phone3}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then On ${phone1} Wait for 2 seconds
    Then Verify audio path between ${phone2} and ${phone1}
    Then on ${phone3} verify the softkeys in ${IdleState}
    Then disconnect the call from ${phone2}

147274:TC06: Unpark failure
    [Tags]      Owner:Anuj     Reviewer:     unpark    eightth
    &{pmargst} =  Create Dictionary  lineKey=${programKey5}
    &{pressLineKey} =  Create Dictionary  action_name=pressLineKey   pmargs=&{pmargst}
    Given using ${bossPortal} I program ${pickupUnpark} on ${phone3} using ${bossDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then On ${phone3} verify display message ${pickAndUnpar}
    Then on ${phone3} due to action ${pressLineKey} popup raised verify message ${noCallsToUnpark} with wait of 0

186381:TC005 Check call history after whisper page
    [Tags]      Owner:Anuj     Reviewer:     whisper_page    eightth
    Given using ${bossPortal} I program ${whisperPage} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${whisperPage}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then Verify ringing state on ${phone2} and ${phone1}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then Verify the led state of ${line1} as ${on} on ${phone3 }
    Then Check Connection and disconnect the ${phone1}
    Then Check Connection and disconnect the ${phone2}
    Then press the call history button on ${phone1} and folder ${Outgoing} and ${Details}
    Then Verify extension ${number} of ${phone3} on ${phone1}
    Then press the call history button on ${phone3} and folder ${Received} and ${Details}
    Then Verify extension ${number} of ${phone1} on ${phone1}
    Then disconnect the call from ${phone1}


186382:TC006 Dial a whisper page while being on a call
    [Tags]      Owner:Anuj     Reviewer:    whisper_page    eightth
    Given using ${bossPortal} I program ${whisperPage} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${whisperPage}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then On ${phone1} Wait for 2 seconds
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then verify the led state of ${line1} as ${on} on ${phone2}



186387:TC011 Make an incoming call when phone is on whisper page call
    [Tags]      Owner:Anuj     Reviewer:    whisper_page    eightth
    Given using ${bossPortal} I program ${whisperPage} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${whisperPage}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then On ${phone1} Wait for 2 seconds
    Then i want to make a two party call between ${phone2} and ${phone3} using ${loudspeaker}
    Then Verify ringing state on ${phone2} and ${phone3}
    Then verify the led state of ${line2} as ${blink} on ${phone3}
    Then Verify ringing state on ${phone2} and ${phone3}

186395:TC001 Creating a Programmed button called whisper page
    [Tags]      Owner:Anuj     Reviewer:    whisper_page    eightth
    Given using ${bossPortal} I program ${whisperPage} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${whisperPage}


147479:Whisper page button with extension target programmed- Off Hook
    [Tags]      Owner:Anuj     Reviewer:    whisper_page    eightth
    Given using ${bossPortal} I program ${whisperPage} on ${phone2} using ${bossDetails} and extension of ${phone1} and softkey position 4 with extensionValue
    Then On ${phone2} verify display message ${whisperPage}
    Then i want to make a two party call between ${phone1} and ${phone3} using ${loudspeaker}
    Then Verify ringing state on ${phone1} and ${phone3}
    Then answer the call on ${phone3} using ${loudspeaker}
    Then Press hookMode ${OffHook} on phone ${phone2}
    Then I want to press line key ${programKey5} on phone ${phone2}
    Then On ${phone1} Wait for 2 seconds
    Then Verify audio path between ${phone2} and ${phone1}
    Then verify no audio path from ${phone2} to ${phone3}
    Then on ${phone2} press the softkey ${Drop} in AnswerState
    Then Verify audio path between ${phone1} and ${phone3}
    Then disconnect the call from ${phone3}

147480:Whisper page button with extension target programmed- On Hook
    [Tags]      Owner:Anuj     Reviewer:    whisper_page    eightth
    Given using ${bossPortal} I program ${whisperPage} on ${phone2} using ${bossDetails} and extension of ${phone1} and softkey position 4 with extensionValue
    Then On ${phone2} verify display message ${whisperPage}
    Then i want to make a two party call between ${phone1} and ${phone3} using ${loudspeaker}
    Then answer the call on ${phone3} using ${loudspeaker}
    Then I want to press line key ${programKey5} on phone ${phone2}
    Then Verify audio path between ${phone2} and ${phone1}
    Then verify no audio path from ${phone2} to ${phone3}
    Then on ${phone2} press the softkey ${Drop} in AnswerState
    Then Verify audio path between ${phone1} and ${phone3}
    Then disconnect the call from ${phone1}

219017:TC003 Pressing whisper Mute key with regular and whisper page active call
    [Tags]      Owner:Anuj     Reviewer:    whisper_page    eightth
    Given using ${bossPortal} I program ${whisperPageMute} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with noExtensionValue
    Given using ${bossPortal} I program ${whisperPage} on ${phone3} using ${bossDetails} and extension of ${phone1} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${whisperPage}
    Then On ${phone3} verify display message ${whisperPage}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then I want to press line key ${programKey5} on phone ${phone3}
    Then Verify audio path between ${phone3} and ${phone1}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} verify display message ${unmute}



219053:TC006 Pressing whisper page mute key again after whisper page mute key is pressed
    [Tags]      Owner:Anuj     Reviewer:    whisper_page    eightth
    Given using ${bossPortal} I program ${whisperPageMute} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with noExtensionValue
    Then On ${phone1} verify display message ${whisperPage}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then i want to use fac Whisperpage on ${phone3} to ${phone1}
    Then Verify audio path between ${phone3} and ${phone1}
    Then on ${phone1} wait for 2 seconds
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} verify display message ${unmute}
    Then verify no audio path from ${phone1} to ${phone2}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} verify display message ${mute}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Verify audio path between ${phone1} and ${phone3}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}


219323:TC007 Pressing 'mute' key when regular and whisper page calls are active
    [Tags]      Owner:Anuj     Reviewer:    whisper_page    eightth
    Given using ${bossPortal} I program ${whisperPageMute} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with noExtensionValue
    Then On ${phone1} verify display message ${whisperPage}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then i want to use fac Whisperpage on ${phone3} to ${phone1}
    Then Verify audio path between ${phone3} and ${phone1}
    Then on ${phone1} wait for 2 seconds
    Then on ${phone1} press ${softKey} ${bottomKey3} for 1 times
    Then Verify audio path between ${phone3} and ${phone1}
    Then verify no audio path from ${phone1} to ${phone2}
    Then on ${phone1} verify display message ${unmute}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}

219325:TC011 Whisper page mute key LED after receiving whisper page call
    [Tags]      Owner:Anuj     Reviewer:    whisper_page    eightth
    Given using ${bossPortal} I program ${whisperPageMute} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with noExtensionValue
    Given using ${bossPortal} I program ${whisperPage} on ${phone3} using ${bossDetails} and extension of ${phone1} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${whisperPage}
    Then On ${phone3} verify display message ${whisperPage}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then I want to press line key ${programKey5} on phone ${phone3}
    Then Verify audio path between ${phone3} and ${phone1}
    Then verify the led state of ${line5} as ${on} on ${phone1}

559603:Mute the Conference Blind call
    [Tags]      Owner:Anuj     Reviewer:    Conference    eightth
    Given using ${bossPortal} I program ${conferenceBlind} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['conferenceBlind']}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone3} wait for 2 seconds
    Then answer the call on ${phone3} using ${line1}
    Then on ${phone3} wait for 10 seconds
    Then conference call audio verify between ${phone2} ${phone1} and ${phone3}
    Then press hardkey as ${mute} on ${phone2}
    Then verify no audio path from ${phone2} to ${phone1}
    Then verify no audio path from ${phone2} to ${phone3}
    Then Verify audio path between ${phone1} and ${phone3}
    Then disconnect the call from ${phone2}
    And disconnect the call from ${phone3}

227252: Prog Button Consult Conference (without extension)
    [Tags]    Owner:Anuj     Reviewer:Ram      Conference    eightth
    Given using ${bossPortal} I program ${ConferenceConsultative} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with noExtensionValue
    Then On ${phone1} verify display message ${displayMessage["conferenceConsult"]}
    Then I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then Answer the call on ${phone2} using ${loudSpeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then On ${phone1} verify display message ${consult}
    Then On ${phone1} verify display message ${cancel}
    Then on ${phone1} enter number ${phone3}
    Then on ${phone1} press ${softkey} ${bottomKey1} for 1 times
    Then Answer the call on ${phone3} using ${line1}
    Then On ${phone1} verify display message ${drop}
    Then On ${phone1} verify display message ${conference}
    Then on ${phone1} press the softkey ${conference} in AnswerState
    Then Conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then disconnect the call from ${phone2}
    And disconnect the call from ${phone1}

227251:Prog Button Consult Conference (with extension)
    [Tags]    Owner:Anuj      Reviewer:Ram      Conference    eightth
    Given using ${bossPortal} I program ${ConferenceConsultative} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage["conferenceConsult"]}
    Then I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then Answer the call on ${phone2} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then On ${phone1} Wait for 2 seconds
    Then Answer the call on ${phone3} using ${loudSpeaker}
    Then On ${phone1} verify display message ${drop}
    Then On ${phone1} verify display message ${conference}
    Then on ${phone1} press the softkey ${conference} in AnswerState
    Then on ${phone1} wait for 2 seconds
    Then Conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then disconnect the call from ${phone1}
    Then disconnect the call from ${phone3}

227926:Prog Button Conference Intercom (with extension)
    [Tags]     Owner:Anuj     Reviewer:Avishek    Conference    eightth
    Given using ${bossPortal} I program ${ConferenceIntercom} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['conferenceIntercom']}
    Then I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then Answer the call on ${phone2} using ${loudSpeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then verify the led state of ${line1} as ${on} on ${phone3}
    Then on ${phone1} press the softkey ${conference} in AnswerState
    Then Conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone1}

227927:Prog Button Conference Intercom (without extension)
    [Tags]     Owner:Anuj     Reviewer:Avishek    Conference    eightth
    Given using ${bossPortal} I program ${ConferenceIntercom} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with noExtensionValue
    Then On ${phone1} verify display message ${displayMessage['conferenceIntercom']}
    Then I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then Answer the call on ${phone2} using ${loudSpeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} wait for 2 seconds
    Then On ${phone1} verify display message ${intercom}
    Then On ${phone1} verify display message ${cancel}
    Then on ${phone1} enter number ${phone3}
    Then on ${phone1} wait for 5 seconds
    Then Verify audio path between ${phone1} and ${phone3}
    Then on ${phone1} press the softkey ${conference} in AnswerState
    Then on ${phone1} wait for 2 seconds
    Then Conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone1}

231360:Prog Button Blind Conference (Destination configured)
    [Tags]   Owner:Anuj     Reviewer:Avishek    Conference    ninth
    Given using ${bossPortal} I program ${conferenceBlind} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['conferenceBlind']}
    Then I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then Answer the call on ${phone2} using ${loudSpeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then On ${phone1} Wait for 2 seconds
    Then Verify the led state of ${line1} as ${blink} on ${phone3}
    Then Answer the call on ${phone3} using ${loudSpeaker}
    Then Conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}

231361:Prog Button Blind Conference (Destination not configured)
    [Tags]   Owner:Anuj    Reviewer:Aman    Conference    ninth
    Given using ${bossPortal} I program ${conferenceBlind} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with noExtensionValue
    Then On ${phone1} verify display message ${displayMessage['conferenceBlind']}
    Then I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then Answer the call on ${phone2} using ${loudSpeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then On ${phone1} Wait for 2 seconds
    Then On ${phone1} verify display message ${Conference}
    Then On ${phone1} verify display message ${Cancel}
    Then On ${phone1} verify display message >
    Then on ${phone1} enter number ${phone3}
    Then On ${phone3} Wait for 4 seconds
    Then Answer the call on ${phone3} using ${loudSpeaker}
    Then Conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}


127822:Progbutton Transfer Consultative destination not configured (call not answered)
    [Tags]      Owner:Anuj     Reviewer:Aman    Transfer    ninth
    Given using ${bossPortal} I program ${Transfer Consultative} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with noExtensionValue
    Then On ${phone1} verify display message ${displayMessage['transferConsult']}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then verify ringing state on ${phone2} and ${phone1}
    Then disconnect the call from ${phone2}

147275:TC05: Unpark with multiple calls
    [Tags]      Owner:Anuj     Reviewer:Aman    Unpark    ninth
    Given using ${bossPortal} I program ${pickupUnpark} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${pickAndUnpar}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then i want to park the call from ${phone1} on ${phone3} using ${default} and ${timeout}
    Then On ${phone1} Wait for 6 seconds
    Then I want to make a two party call between ${phone4} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then i want to park the call from ${phone1} on ${phone3} using ${default} and ${timeout}
    Then On ${phone1} Wait for 6 seconds
    Then verify the led state of ${line1} as ${blink} on ${phone3}
    Then verify the led state of ${line2} as ${blink} on ${phone3}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then On ${phone1} Wait for 2 seconds
    Then on ${phone1} verify display message ${unpark}
    Then press hardkey as ${scrollDown} on ${phone1}
    Then on ${phone1} press ${softkey} ${bottomKey1} for 1 times
    Then verify extension ${number} of ${phone2} on ${phone1}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone4}

186396:TC002 Create a Programmed button called whisper page WITHOUT target EXTENSION
    [Tags]      Owner:Anuj     Reviewer:Aman    whisper_page    ninth
    Given using ${bossPortal} I program ${whisperPage} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with noExtensionValue
    Then On ${phone1} verify display message ${whisperPage}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} verify display message >
    Then on ${phone1} enter number ${phone2}
    Then Verify audio path between ${phone1} and ${phone2}
    Then disconnect the call from ${phone1}

219019: TC004 Pressing Whisper page Mute key when whisper page call is active
    [Tags]      Owner:Anuj     Reviewer:Aman    whisper_page    ninth
    Given using ${bossPortal} I program ${whisperPageMute} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with noExtensionValue
    Then On ${phone1} verify display message ${whisperPage}
    Then I want to use fac Whisperpage on ${phone3} to ${phone1}
    Then Verify audio path between ${phone3} and ${phone1}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then Verify audio path between ${phone1} and ${phone3}
    Then disconnect the call from ${phone1}

219052:TC005 Pressing 'unmute' key after whisper page mute key is pressed
    [Tags]      Owner:Anuj     Reviewer:Aman    whisper_page    ninth
    Given using ${bossPortal} I program ${whisperPageMute} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with noExtensionValue
    Then On ${phone1} verify display message ${whisperPage}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then I want to use fac Whisperpage on ${phone3} to ${phone1}
    Then Verify audio path between ${phone3} and ${phone1}
    Then on ${phone1} wait for 6 seconds
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then verify no audio path from ${phone1} to ${phone2}
    Then on ${phone1} verify display message ${unmute}
    Then on ${phone1} press ${softKey} ${BottomKey3} for 1 times
    Then on ${phone1} verify display message ${mute}
    Then Verify audio path between ${phone1} and ${phone2}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}


219324:TC008 Press the'whisper page mute' key and hang up the calls
    [Tags]      Owner:Anuj     Reviewer:Aman    whisper_page    ninth
    Given using ${bossPortal} I program ${whisperPageMute} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with noExtensionValue
    Then On ${phone1} verify display message ${whisperPage}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then I want to use fac Whisperpage on ${phone3} to ${phone1}
    Then Verify audio path between ${phone3} and ${phone1}
    Then on ${phone1} wait for 6 seconds
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} verify display message ${unmute}
    Then verify no audio path from ${phone1} to ${phone2}
    Then press hardkey as ${goodBye} on ${phone2}
    Then press hardkey as ${goodBye} on ${phone1}
    Then on ${phone1} verify the softkeys in ${idle}
    Then verify the led state of ${line5} as ${off} on ${phone1}

219024:TC009 Pressing the 'whisper page mute' key while phone receiving an incoming call
    [Tags]      Owner:Anuj     Reviewer:    whisper_page    ninth
    Given using ${bossPortal} I program ${whisperPageMute} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with noExtensionValue
    Then On ${phone1} verify display message ${whisperPage}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then verify ringing state on ${phone2} and ${phone1}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then verify ringing state on ${phone2} and ${phone1}
    Then disconnect the call from ${phone2}

219025:TC010 Pressing 'whisper page mute' key in idle state
    [Tags]      Owner:Anuj     Reviewer:    whisper_page    ninth
    Given using ${bossPortal} I program ${whisperPageMute} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with noExtensionValue
    Then On ${phone1} verify display message ${whisperPage}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} verify the softkeys in ${idle}

220107:Whisper Target receives an incoming call while on a whisper paged and a regular call
    [Tags]      Owner:Anuj     Reviewer:    whisper_page    ninth
    Given using ${bossPortal} I program ${whisperPage} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${whisperPage}
    Then i want to make a two party call between ${phone3} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then Verify audio path between ${phone3} and ${phone2}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then Verify audio path between ${phone1} and ${phone2}
    Then verify no audio path from ${phone1} to ${phone3}
    Then i want to make a two party call between ${phone4} and ${phone2} using ${loudspeaker}
    Then verify the led state of ${line3} as ${blink} on ${phone2}
    Then answer the call on ${phone2} using ${programKey3}
    Then verify no audio path from ${phone3} to ${phone2}
    Then verify no audio path from ${phone2} to ${phone3}
    Then Verify audio path between ${phone2} and ${phone4}
    Then verify no audio path from ${phone1} to ${phone4}
    Then disconnect the call from ${phone4}
    Then disconnect the call from ${phone3}
    Then disconnect the call from ${phone2}

147399:Silent Coach Agent transition to Consult Silent Coach
    [Tags]      Owner:Anuj     Reviewer:    Silent_Coach    ninth
    Given using ${bossPortal} I program ${silentCoach} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 1 with extensionValue
    Then On ${phone1} verify display message ${silentCoach}
    Then I want to make a two party call between ${phone2} and ${phone3} using ${loudspeaker}
    Then answer the call on ${phone3} using ${loudspeaker}
    Then Verify audio path between ${phone2} and ${phone3}
    Then I want to press line key ${programKey2} on phone ${phone1}
    Then on ${phone1} wait for 2 seconds
    Then Verify audio path between ${phone1} and ${phone2}
    Then Verify one way audio from ${phone3} to ${phone1}
    Then verify no audio path from ${phone1} to ${phone3}
    Then On ${phone2} verify display message ${consult}
    Then On ${phone2} verify display message ${drop}
    Then On ${phone2} verify display message ${leave}
    Then on ${phone2} press ${softKey} ${bottomKey2} for 1 times
    Then Verify audio path between ${phone1} and ${phone2}
    Then verify no audio path from ${phone1} to ${phone3}
    Then verify no audio path from ${phone2} to ${phone3}
    Then Verify one way audio from ${phone3} to ${phone1}
    Then Verify one way audio from ${phone3} to ${phone2}
    Then On ${phone2} verify display message ${displayMessage['resume']}
    Then On ${phone2} verify display message ${drop}
    Then On ${phone2} verify display message ${leave}
    Then on ${phone2} press ${softKey} ${bottomKey2} for 1 times
    Then Verify audio path between ${phone3} and ${phone2}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Verify one way audio from ${phone3} to ${phone1}
    Then verify no audio path from ${phone1} to ${phone3}
    Then On ${phone2} verify display message ${consult}
    Then On ${phone2} verify display message ${drop}
    Then On ${phone2} verify display message ${leave}
    Then disconnect the call from ${phone2}

560400:TC015 Making a whisper page call while being in a whisper page call
    [Tags]      Owner:Anuj     Reviewer:    Whisper_Page    ninth
    Given using ${bossPortal} I program ${whisperPage} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Given using ${bossPortal} I program ${whisperPage} on ${phone2} using ${bossDetails} and extension of ${phone3} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${whisperPage}
    Then On ${phone2} verify display message ${whisperPage}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then Verify audio path between ${phone1} and ${phone2}
    Then I want to press line key ${programKey5} on phone ${phone2}
    Then Verify audio path between ${phone2} and ${phone3}
    Then on ${phone1} verify the softkeys in ${idle}
    Then disconnect the call from ${phone2}

560401:TC016 Making a transfer/conference call after sending a whisper page call
    [Tags]      Owner:Anuj     Reviewer:    Whisper_Page    ninth
    Given using ${bossPortal} I program ${whisperPage} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${whisperPage}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then Verify audio path between ${phone1} and ${phone2}
    Then i want to verify on ${phone1} negative display message ${transfer}
    Then disconnect the call from ${phone2}

560432:Whisper page with a held call on the phone - Mute behavior
    [Tags]      Owner:Anuj      Reviewer:      Whisper_Page    ninth
    Given using ${bossPortal} I program ${whisperPage} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${whisperPage}
    Then i want to make a two party call between ${phone2} and ${phone3} using ${loudspeaker}
    Then answer the call on ${phone3} using ${loudspeaker}
    Then Press hardkey as ${holdState} on ${phone2}
    Then verify no audio path from ${phone2} to ${phone3}
    Then verify no audio path from ${phone3} to ${phone2}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then Verify audio path between ${phone1} and ${phone2}
    Then verify the led state of ${line1} as ${blink} on ${phone2}
    Then i want to verify on ${phone2} negative display message ${mute}
    Then press hardkey as ${holdState} on ${phone2}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Verify audio path between ${phone2} and ${phone3}
    Then On ${phone2} verify display message ${mute}
    Then on ${phone2} press ${softKey} ${bottomKey3} for 1 times
    Then verify no audio path from ${phone2} to ${phone3}
    Then on ${phone2} verify display message ${unmute}
    Then on ${phone2} press ${softKey} ${bottomKey3} for 1 times
    Then Verify audio path between ${phone1} and ${phone2}
    Then Verify audio path between ${phone2} and ${phone3}
    Then On ${phone2} verify display message ${mute}
    Then disconnect the call from ${phone1}
    Then disconnect the call from ${phone3}

560430:Put a call on hold during whisper page - Mute behavior
    [Tags]      Owner:Anuj     Reviewer:      Whisper_Page    ninth
    Given using ${bossPortal} I program ${whisperPage} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${whisperPage}
    Then i want to make a two party call between ${phone2} and ${phone3} using ${loudspeaker}
    Then answer the call on ${phone3} using ${loudspeaker}
    Then Verify audio path between ${phone2} and ${phone3}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then Verify audio path between ${phone1} and ${phone2}
    Then On ${phone2} verify display message ${mute}
    Then Press hardkey as ${HoldState} on ${phone2}
    Then verify no audio path from ${phone2} to ${phone3}
    Then verify no audio path from ${phone3} to ${phone2}
    Then verify the led state of ${line1} as ${blink} on ${phone2}
    Then Press hardkey as ${HoldState} on ${phone2}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Verify audio path between ${phone3} and ${phone2}
    Then On ${phone2} verify display message ${mute}
    Then disconnect the call from ${phone3}
    Then disconnect the call from ${phone2}

560431:Put a whisper-muted call on hold
    [Tags]      Owner:Anuj     Reviewer:      Whisper_Page    ninth
    Given using ${bossPortal} I program ${whisperPage} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${whisperPage}
    Then i want to make a two party call between ${phone3} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then Verify audio path between ${phone3} and ${phone2}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then Verify audio path between ${phone2} and ${phone1}
    Then On ${phone2} verify display message ${mute}
    Then on ${phone2} press ${softKey} ${bottomKey3} for 1 times
    Then verify no audio path from ${phone2} to ${phone3}
    Then press hardkey as ${holdState} on ${phone2}
    Then verify no audio path from ${phone3} to ${phone2}
    Then verify no audio path from ${phone2} to ${phone3}
    Then verify the led state of ${line1} as ${blink} on ${phone2}
    Then Verify audio path between ${phone1} and ${phone2}
    Then i want to verify on ${phone2} negative display message ${unmute}
    Then press hardkey as ${holdState} on ${phone2}
    Then Verify audio path between ${phone3} and ${phone2}
    Then Verify audio path between ${phone1} and ${phone2}
    Then on ${phone2} verify display message ${mute}
    Then on ${phone2} press ${softKey} ${bottomKey3} for 1 times
    Then verify no audio path from ${phone2} to ${phone3}
    Then on ${phone2} verify display message ${unmute}
    Then disconnect the call from ${phone1}
    Then disconnect the call from ${phone3}

560415:TC009 whisper page keys on two phones having same target extension
    [Tags]      Owner:Anuj     Reviewer:      Whisper_Page    ninth
    Given using ${bossPortal} I program ${whisperPage} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with extensionValue
    Given using ${bossPortal} I program ${whisperPage} on ${phone2} using ${bossDetails} and extension of ${phone3} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${whisperPage}
    Then On ${phone2} verify display message ${whisperPage}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then Verify audio path between ${phone1} and ${phone3}
    Then verify the led state of ${line5} as ${on} on ${phone1}
    Then verify the led state of ${line5} as ${on} on ${phone2}
    Then disconnect the call from ${phone1}

560801:TC014 Two whisper page calls to same phone
    [Tags]      Owner:Anuj     Reviewer:      Whisper_Page    ninth
    Given using ${bossPortal} I program ${whisperPage} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Given using ${bossPortal} I program ${whisperPage} on ${phone3} using ${bossDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${whisperPage}
    Then On ${phone3} verify display message ${whisperPage}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then Verify audio path between ${phone1} and ${phone2}
    Then I want to press line key ${programKey5} on phone ${phone3}
    Then On ${phone3} verify display message ${actionNotPermitted}
    And disconnect the call from ${phone1}

559572:Hold Call and press Conference Consult key
    [Tags]      Owner:Anuj     Reviewer:      Conference    ninth
    Given using ${bossPortal} I program ${ConferenceConsultative} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['conferenceConsult']}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then i want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone3} wait for 2 seconds
    Then answer the call on ${phone3} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone3}
    Then press hardkey as ${holdState} on ${phone1}
    Then verify no audio path from ${phone1} to ${phone3}
    Then verify no audio path from ${phone3} to ${phone1}
    Then press hardkey as ${holdState} on ${phone1}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}

559568:Mute the Conference Consult call
    [Tags]      Owner:Anuj     Reviewer:      Conference    tenth
    Given using ${bossPortal} I program ${ConferenceConsultative} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['conferenceConsult']}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then Verify audio path between ${phone2} and ${phone1}
    Then i want to press line key ${programKey5} on phone ${phone1}
    Then verify ringing state on ${phone1} and ${phone3}
    Then answer the call on ${phone3} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone3}
    Then press hardkey as ${mute} on ${phone1}
    Then verify no audio path from ${phone1} to ${phone3}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}

557147: TC05: Offscreen call moves to idle call appearance when progbuttons enabled
    [Tags]      Owner:Anuj     Reviewer:      offscreen    tenth
    Given using ${bossPortal} I program 2 Call Appearance button on ${phone1}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then i want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${line2}
    Then Verify audio path between ${phone3} and ${phone1}
    Then i want to make a two party call between ${phone4} and ${phone1} using ${loudspeaker}
    Then on ${phone1} press ${softkey} ${bottomKey1} for 1 times
    Then press hardkey as ${scrollDown} on ${phone1}
    Then verify extension ${number} of ${phone4} on ${phone1}
    Then Verify audio path between ${phone1} and ${phone4}
    Then verify the led state of ${line2} as ${blink} on ${phone1}
    Then on ${phone3} press ${softkey} ${bottomKey1} for 1 times
    Then verify the led state of ${line2} as ${on} on ${phone1}
    Then on ${phone4} press ${softkey} ${bottomKey1} for 1 times
    Then on ${phone2} press ${softkey} ${bottomKey1} for 1 times

557149: TC07: Offscreen parked call moves to parked call
    [Tags]      Owner:Anuj     Reviewer:      offscreen    tenth
    Given using ${bossPortal} I program 2 Call Appearance button on ${phone1}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then i want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${line2}
    Then Verify audio path between ${phone3} and ${phone1}
    Then i want to make a two party call between ${phone5} and ${phone4} using ${loudspeaker}
    Then answer the call on ${phone4} using ${loudspeaker}
    Then Verify audio path between ${phone4} and ${phone5}
    Then on ${phone4} press the softkey ${Park} in AnswerState
    Then on ${phone4} wait for 2 seconds
    Then on ${phone4} enter number ${phone1}
    Then on ${phone4} wait for 3 seconds
    Then press hardkey as ${scrollDown} on ${phone1}
    Then verify extension ${number} of ${phone5} on ${phone1}
    Then on ${phone2} press the softkey ${drop} in AnswerState
    Then verify extension ${number} of ${phone5} on ${phone1}
    Then disconnect the call from ${phone3}
    Then disconnect the call from ${phone5}


558644: Press BargeIn during UCB Call
    [Tags]      Owner:Anuj     Reviewer:Aman      ucb    tenth
    Given using ${bossPortal} I program ${bargeIn} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then on ${phone1} verify display message ${bargeIn}
    Then on ${phone2} press ${softkey} ${bottomkey3} for 1 times
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} verify display message ${notPermittedOnThisCall}
    Then disconnect the call from ${phone2}
    Then on ${phone2} press ${softkey} ${bottomkey3} for 1 times
    Then on ${phone2} dial number ${wrongAccessCode}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} verify display message ${notPermittedOnThisCall}
    Then disconnect the call from ${phone2}
    Then on ${phone2} press ${softkey} ${bottomkey3} for 1 times
    Then on ${phone2} dial number ${accessCode}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} verify display message ${notPermittedOnThisCall}
    Then using ${bossPortal} I remove unused keys on ${phone1}
    And disconnect the call from ${phone2}

559207: TC015 Second BCA Incoming call while being on regular call
    [Tags]      Owner:Anuj     Reviewer:      BCA    tenth
    [SETUP]    BCA Custom Setup
    &{createBCAExtension} =  Create Dictionary    name=bca_anuj1   backupExtn=${phone4}    switch=2    callStackDepth=2    forwardAfter=2    callStackFull=${EMPTY}   noAnswer=${EMPTY}    outboundCallerID=${EMPTY}    allowBridgeConferencing=true   defaultPrivacySettings=0
    ${bcaExtn}=    using ${bossPortal} I want to create Bridge Call Appearance extension using ${createBCAExtension}
    &{BCAdetails} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=4    function=Bridge Call Appearance    label=BCA    target_extension=${bcaExtn}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${EMPTY}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=${EMPTY}
    Given using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails}
    Then on ${phone1} verify display message ${bca}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then on ${phone3} dial number ${bcaExtn}
    Then verify the led state of ${line5} as ${blink} on ${phone1}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}
   [Teardown]    BCA Custom Teardown

559211: Calling Party to BCA Hangs up During Consult Transfer
    [Tags]      Owner:Anuj     Reviewer:      BCA    tenth
    [SETUP]    BCA Custom Setup
    &{createBCAExtension} =  Create Dictionary    name=bca_anuj1   backupExtn=${phone4}    switch=2    callStackDepth=2    forwardAfter=2    callStackFull=${EMPTY}   noAnswer=${EMPTY}    outboundCallerID=${EMPTY}    allowBridgeConferencing=true   defaultPrivacySettings=0
    ${bcaExtn}=    using ${bossPortal} I want to create Bridge Call Appearance extension using ${createBCAExtension}
    &{BCAdetails} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=4    function=Bridge Call Appearance    label=BCA    target_extension=${bcaExtn}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${EMPTY}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=${EMPTY}
    Given using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails}
    Then on ${phone1} verify display message ${bca}
    Then verify the led state of ${line5} as ${off} on ${phone1}
    Then on ${phone2} dial number ${bcaExtn}
    Then on ${phone1} wait for 3 seconds
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then Verify audio path between ${phone1} and ${phone2}
    Then on ${phone1} press ${softkey} ${bottomkey3} for 1 times
    Then on ${phone1} enter number ${phone3}
    Then on ${phone1} wait for 3 seconds
    Then answer the call on ${phone3} using ${loudspeaker}
    Then disconnect the call from ${phone2}
    Then verify extension ${number} of ${phone1} on ${phone3}
    Then verify extension ${number} of ${phone3} on ${phone1}
    Then verify the led state of ${line5} as ${off} on ${phone1}
    Then on ${phone2} verify the softkeys in ${idle}
    Then disconnect the call from ${phone3}
    [Teardown]    BCA Custom Teardown

559214: Consult Transfer the BCA
    [Tags]      Owner:Anuj     Reviewer:      BCA    tenth
    [SETUP]    BCA Custom Setup
    &{createBCAExtension} =  Create Dictionary    name=bca_anuj1   backupExtn=${phone4}    switch=2    callStackDepth=2    forwardAfter=2    callStackFull=${EMPTY}   noAnswer=${EMPTY}    outboundCallerID=${EMPTY}    allowBridgeConferencing=true   defaultPrivacySettings=0
    ${bcaExtn}=    using ${bossPortal} I want to create Bridge Call Appearance extension using ${createBCAExtension}
    &{BCAdetails} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=4    function=Bridge Call Appearance    label=BCA    target_extension=${bcaExtn}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${EMPTY}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=${EMPTY}
    Given using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails}
    Then on ${phone1} verify display message ${bca}
    Then verify the led state of ${line5} as ${off} on ${phone1}
    Then on ${phone2} dial number ${bcaExtn}
    Then on ${phone1} wait for 3 seconds
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then Verify audio path between ${phone1} and ${phone2}
    Then on ${phone2} press ${softkey} ${bottomkey3} for 1 times
    Then on ${phone2} enter number ${phone3}
    Then on ${phone2} wait for 4 seconds
    Then answer the call on ${phone3} using ${loudspeaker}
    Then on ${phone2} wait for 2 seconds
    Then on ${phone2} press ${softkey} ${bottomkey3} for 1 times
    Then Verify audio path between ${phone1} and ${phone3}
    Then verify the led state of ${line5} as ${on} on ${phone1}
    And disconnect the call from ${phone3}
    [Teardown]    BCA Custom Teardown

559219: Transfers - BCA as a No Answer destination
    [Tags]      Owner:Anuj     Reviewer:      BCA    tenth
    [Setup]    BCA Custom Setup
    &{createBCAExtension} =  Create Dictionary    name=bca_anuj1   backupExtn=${phone4}    switch=2    callStackDepth=2    forwardAfter=2    callStackFull=${EMPTY}   noAnswer=${EMPTY}    outboundCallerID=${EMPTY}    allowBridgeConferencing=true   defaultPrivacySettings=0
    ${bcaExtn}=    using ${bossPortal} I want to create Bridge Call Appearance extension using ${createBCAExtension}
    &{BCAdetails1} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=4    function=Bridge Call Appearance    label=BCA    target_extension=${bcaExtn}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${EMPTY}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=${EMPTY}
    &{BCAdetails2} =  Create Dictionary    user_extension=${phone2}    button_box=0    soft_key=4    function=Bridge Call Appearance    label=BCA    target_extension=${bcaExtn}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${EMPTY}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=${EMPTY}
    Given using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails1}
    Then using ${bossPortal} I want to create bca on ${phone2} using ${BCAdetails2}
    Then on ${phone1} verify display message ${bca}
    Then on ${phone2} verify display message ${bca}
    Then on ${phone3} dial number ${bcaExtn}
    Then verify the led state of ${line5} as ${blink} on ${phone1}
    Then verify the led state of ${line5} as ${blink} on ${phone2}
    Then on ${phone3} wait for 10 seconds
    Then verify the led state of ${line5} as ${blink} on ${phone1}
    Then verify the led state of ${line5} as ${blink} on ${phone2}
    Then disconnect the call from ${phone3}
    Then verify the led state of ${line5} as ${off} on ${phone1}
    Then verify the led state of ${line5} as ${off} on ${phone2}
    [Teardown]    BCA Custom Teardown

559222: Transfers - BCA transfered to another BCA
    [Tags]      Owner:Anuj     Reviewer:      BCA    tenth
    [Setup]    BCA Custom Setup
    &{createBCAExtension} =  Create Dictionary    name=bca_anuj1   backupExtn=${phone4}    switch=2    callStackDepth=2    forwardAfter=2    callStackFull=${EMPTY}   noAnswer=${EMPTY}    outboundCallerID=${EMPTY}    allowBridgeConferencing=true   defaultPrivacySettings=0
    ${bcaExtn1}=    using ${bossPortal} I want to create Bridge Call Appearance extension using ${createBCAExtension}
    &{BCAdetails1} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=4    function=Bridge Call Appearance    label=BCA    target_extension=${bcaExtn1}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${EMPTY}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=${EMPTY}
    &{createBCAExtension2} =  Create Dictionary    name=bca_anuj2   backupExtn=${phone4}    switch=2    callStackDepth=2    forwardAfter=2    callStackFull=${EMPTY}   noAnswer=${EMPTY}    outboundCallerID=${EMPTY}    allowBridgeConferencing=true   defaultPrivacySettings=0
    ${bcaExtn2}=    using ${bossPortal} I want to create Bridge Call Appearance extension using ${createBCAExtension2}
    &{BCAdetails2} =  Create Dictionary    user_extension=${phone2}    button_box=0    soft_key=4    function=Bridge Call Appearance    label=BCA    target_extension=${bcaExtn2}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${EMPTY}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=${EMPTY}
    Given using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails1}
    Then using ${bossPortal} I want to create bca on ${phone2} using ${BCAdetails2}
    Then on ${phone1} verify display message ${bca}
    Then on ${phone2} verify display message ${bca}
    Then on ${phone3} enter number ${bcaExtn1}
    Then on ${phone3} dial number ${bcaExtn1}
    Then On ${phone1} Wait for 3 seconds
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then On ${phone1} Wait for 2 seconds
    Then Verify audio path between ${phone1} and ${phone3}
    Then verify the led state of ${line5} as ${on} on ${phone1}
    Then on ${phone1} press ${softkey} ${bottomkey3} for 1 times
    Then on ${phone1} dial number ${bcaExtn2}
    Then on ${phone1} press ${softKey} ${bottomKey3} for 1 times
    Then verify the led state of ${line5} as ${blink} on ${phone2}
    Then verify the led state of ${line5} as ${off} on ${phone1}
    Then I want to press line key ${programKey5} on phone ${phone2}
    Then Verify audio path between ${phone3} and ${phone2}
    Then verify the led state of ${line5} as ${on} on ${phone2}
    Then disconnect the call from ${phone2}
    [Teardown]    BCA Custom Teardown


566399: Agent login, logout ,wrap
    [Tags]      Owner:Anuj     Reviewer:      agent    tenth
    Given using ${bossPortal} I program ${agentLogin} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with noExtensionValue
    Then on ${phone1} verify display message ${agentLogin}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} verify the softkeys in ${idle}
    Then using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4
    Then using ${bossPortal} I program ${agentLogout} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with noExtensionValue
    Then on ${phone1} verify display message ${agentLogout}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} verify the softkeys in ${idle}
    Then using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4
    Then using ${bossPortal} I program ${agentWrapUp} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with noExtensionValue
    Then on ${phone1} verify display message ${agentWrapU}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} verify the softkeys in ${idle}

566401: Change Default Audio Path
    [Tags]      Owner:Anuj     Reviewer:      CHANGE_AUDIO    tenth
    &{audiopathdetails} =  Create Dictionary    changeDefaultAudioPath=speaker    account_name=Automation    button_box=0
    Given using ${bossPortal} I program ${changeDefaultAudioPath} on ${phone1} using ${audiopathdetails} and extension of ${phone2} and softkey position 4 with noExtensionValue
    Then on ${phone1} verify display message ${changeDefau}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} verify the softkeys in ${idle}

560300: Progbutton Transfer Consultative destination configured (call answered)
    [Tags]      Owner:Anuj     Reviewer:      Transfer    tenth
    Given using ${bossPortal} I program ${Transfer Consultative} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['transferConsult']}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then i want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone3} wait for 2 seconds
    Then answer the call on ${phone3} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone3}
    Then on ${phone1} press the softkey ${transfer} in TransferState
    Then Verify audio path between ${phone3} and ${phone2}
    Then on ${phone1} verify the softkeys in ${idle}
    Then disconnect the call from ${phone2}

557803: TC033 Mute the HG Call
    [Tags]      Owner:Anuj     Reviewer:      hunt_group    tenth
    [Setup]    Hunt Group Custom Setup
    @{members}   Create List      ${phone2}    ${phone3}
    &{huntGroupDetails} =  Create Dictionary    BackupExtension=${phone2}    GroupMembers=${members}   GroupName=HG_Anuj   IncludeInSystem=True    MakeExtnPrivate=False    HuntPattern=4    RingsPerMember=3    NoAnswerRings=4    CallMemberWhenForwarding=True    SkipMemberOnCall=True    CallStackFull=${EMPTY}    NoAnswer=${EMPTY}
    ${HGExtension} =     using ${bossPortal} I want to create hunt group user extension with ${huntGroupDetails}
    Given on ${phone1} dial number ${HGExtension}
    Then verify the led state of ${line1} as ${blink} on ${phone2}
    Then verify the led state of ${line1} as ${blink} on ${phone3}
    Then answer the call on ${phone3} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone3}
    Then press hardkey as ${mute} on ${phone1}
    Then verify no audio path from ${phone1} to ${phone3}
    Then disconnect the call from ${phone3}
    [Teardown]    Hunt Group Custom Teardown


557804: TC034 Confrence with HG Call
    [Tags]      Owner:Anuj     Reviewer:    Conference    tenth
    [Setup]    Hunt Group Custom Setup
    @{members}   Create List      ${phone4}    ${phone3}
    &{huntGroupDetails} =  Create Dictionary    BackupExtension=${phone2}    GroupMembers=${members}   GroupName=HG_Anuj   IncludeInSystem=True    MakeExtnPrivate=False    HuntPattern=4    RingsPerMember=3    NoAnswerRings=4    CallMemberWhenForwarding=True    SkipMemberOnCall=True    CallStackFull=${EMPTY}    NoAnswer=${EMPTY}
    ${HGExtension} =     using ${bossPortal} I want to create hunt group user extension with ${huntGroupDetails}
    Given on ${phone1} dial number ${HGExtension}
    Then verify the led state of ${line1} as ${blink} on ${phone3}
    Then verify the led state of ${line1} as ${blink} on ${phone4}
    Then answer the call on ${phone3} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone3}
    Then on ${phone1} press ${softkey} ${bottomKey2} for 1 times
    Then on ${phone1} enter number ${phone4}
    Then on ${phone1} wait for 3 seconds
    Then answer the call on ${phone4} using ${loudspeaker}
    Then on ${phone1} press ${softkey} ${bottomKey2} for 1 times
    Then conference call audio verify between ${phone1} ${phone4} and ${phone3}
    Then disconnect the call from ${phone3}
    Then disconnect the call from ${phone4}
    [Teardown]    Hunt Group Custom Teardown


560306: Hang up the transfer Consultative call
    [Tags]      Owner:Anuj     Reviewer:    Transfer    tenth
    Given using ${bossPortal} I program ${Transfer Consultative} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['transferConsult']}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone3}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then press hardkey as ${goodBye} on ${phone1}
    Then verify ringing state on ${phone2} and ${phone3}
    Then on ${phone1} wait for 2 seconds
    Then on ${phone1} verify the softkeys in ${idle}
    Then disconnect the call from ${phone2}



560308: Hang up the Answered transfer Consultative call
    [Tags]      Owner:Anuj     Reviewer:Aman    Transfer    tenth
    Given using ${bossPortal} I program ${Transfer Consultative} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['transferConsult']}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then verify ringing state on ${phone1} and ${phone3}
    Then answer the call on ${phone3} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone3}
    Then press hardkey as ${goodBye} on ${phone1}
    Then Verify audio path between ${phone2} and ${phone3}
    Then on ${phone1} verify the softkeys in ${idle}
    Then disconnect the call from ${phone2}

560436: Third party Conferences the call with Whisper paged extension
    [Tags]      Owner:Anuj     Reviewer:Aman    whisper_page    tenth
    Given using ${bossPortal} I program ${whisperPage} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${whisperPage}
    Then I want to make a two party call between ${phone3} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then Verify audio path between ${phone3} and ${phone2}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then Verify audio path between ${phone1} and ${phone2}
    Then verify no audio path from ${phone1} to ${phone3}
    Then on ${phone3} press the softkey ${conference} in AnswerState
    Then on ${phone3} enter number ${phone4}
    Then on ${phone3} wait for 3 seconds
    Then answer the call on ${phone4} using ${loudspeaker}
    Then on ${phone3} press the softkey ${conference} in AnswerState
    Then conference call audio verify between ${phone2} ${phone3} and ${phone4}
    Then i want to verify on ${phone1} negative display message ${leave}
    Then disconnect the call from ${phone4}
    Then disconnect the call from ${phone1}
    Then disconnect the call from ${phone2}

560438: Third party transfers call with Whisper paged extension
    [Tags]      Owner:Anuj     Reviewer:Aman    whisper_page    tenth
    Given using ${bossPortal} I program ${whisperPage} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${whisperPage}
    Then I want to make a two party call between ${phone2} and ${phone3} using ${loudspeaker}
    Then answer the call on ${phone3} using ${loudspeaker}
    Then Verify audio path between ${phone2} and ${phone3}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then Verify audio path between ${phone1} and ${phone2}
    Then verify no audio path from ${phone1} to ${phone3}
    Then on ${phone3} press the softkey ${transfer} in AnswerState
    Then on ${phone3} enter number ${phone4}
    Then on ${phone3} wait for 3 seconds
    Then answer the call on ${phone4} using ${loudspeaker}
    Then on ${phone3} press the softkey ${transfer} in AnswerState
    Then Verify audio path between ${phone2} and ${phone4}
    Then verify no audio path from ${phone1} to ${phone4}
    Then Verify audio path between ${phone1} and ${phone2}
    Then disconnect the call from ${phone4}
    Then disconnect the call from ${phone1}

558276: Unhold Call while Consult is being dialed
    [Tags]    Owner:Anuj    Reviewer:    Unhold     notApplicableFor6910    tenth    notApplicableForMiCloud
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then Verify audio path between ${phone2} and ${phone1}
    Then on ${phone1} press the softkey ${transfer} in AnswerState
    Then on ${phone1} verify display message >
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then using ${bossPortal} I want to change Delay after collecting digits value to 30000
    Then on ${phone1} verify display message ${transfer}
    Then on ${phone1} enter number 10
    Then on ${phone1} verify display message ${partialExtension}
    Then On ${phone1} verify the softkeys in ${transfer}
    Then using ${bossPortal} I want to change Delay after collecting digits value to 3000
    Then I want to press line key ${programKey1} on phone ${phone1}
    Then on ${phone1} verify display message ${drop}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    And disconnect the call from ${phone2}
    [Teardown]    Telephony Options Custom Teardown


558277: UnHold Call while Consult ringing
    [Tags]    Owner:Anuj    Reviewer:    Unhold    tenth    notApplicableForMiCloud
    Then i want to make a two party call between ${phone2} and ${phone1} using ${line1}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then Verify audio path between ${phone2} and ${phone1}
    Then on ${phone1} press the softkey ${transfer} in AnswerState
    Then on ${phone1} verify display message >
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then using ${bossPortal} I want to change Delay after collecting digits value to 25000
    Then on ${phone1} verify display message ${transfer}
    Then on ${phone1} enter number ${phone3}
    Then On ${phone1} verify the softkeys in ${transfer}
    Then using ${bossPortal} I want to change Delay after collecting digits value to 3000
    Then verify extension ${number} of ${phone3} on ${phone1}
    Then on ${phone1} press ${softkey} ${bottomKey1} for 1 times
    Then verify ringing state on ${phone1} and ${phone3}
    Then I want to press line key ${programKey1} on phone ${phone1}
    Then Verify audio path between ${phone1} and ${phone2}
    Then On ${phone3} verify the softkeys in ${idle}
    And disconnect the call from ${phone2}
    [TEARDOWN]    Telephony Options Custom Teardown

559381: Boss receives call on BCA button
    [Tags]    Owner:Anuj    Reviewer:    sca_bca    eleventh
    [Setup]    Telephony Feature Custom Setup
    &{telephonydetails} =  Create Dictionary    sca_enabled=True
    ${scaExtn} =  using ${bossPortal} on ${phone1} I want to enable SCA using ${telephonydetails}
    &{BCAdetails} =  Create Dictionary    user_extension=${phone2}    button_box=0    soft_key=4    function=Bridge Call Appearance    label=BCA    target_extension=${scaExtn}
    Given using ${bossPortal} I want to create bca on ${phone2} using ${BCAdetails}
    Then on ${phone2} verify display message ${bca}
    Then on ${phone2} dial number ${scaExtn}
    Then verify the led state of ${line5} as ${blink} on ${phone1}
    Then answer the call on ${phone1} using ${programKey5}
    Then Verify audio path between ${phone1} and ${phone2}
    Then disconnect the call from ${phone2}
    Then on ${phone1} verify the softkeys in ${idleState}
    And using ${bossPortal} remove the function key on ${phone1} using ${BCAdetails} and softkey position 4
    [Teardown]    Telephony Feature Custom Teardown


558090: Test Intercom *15, INITIATE CoS checked.
    [Tags]    Owner:Anuj    Reviewer:    CoS    eleventh
    &{COSDetails} =  Create Dictionary    Name=${fullyFeatured}    AllowIntercomInitiation=True
    Given using ${bossPortal} I want to change telephony features values using ${COSDetails}
    Then I want to use fac Intercom on ${phone1} to ${phone2}
    Then i want to verify on ${phone1} negative display message ${ringing}
    Then Verify audio path between ${phone1} and ${phone2}
    Then disconnect the call from ${phone2}
    &{COSDetails} =  Create Dictionary    Name=${fullyFeatured}
    And using ${bossPortal} I want to change telephony features values using ${COSDetails}
    [Teardown]    CoS Features Custom Teardown


557144: TC02: ignore off screen call
    [Tags]    Owner:Anuj    Reviewer:    offscreen    eleventh
    Given using ${bossPortal} I program 1 Call Appearance button on ${phone1}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then i want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then on ${phone1} verify display message ${answer}
    Then verify the led state of ${line2} as ${off} on ${phone1}
    Then disconnect the call from ${phone2}
    And using ${bossPortal} I remove unused keys on ${phone1}



557148: TC06: Offscreen call moves to idle call appearance call stack size set
    [Tags]    Owner:Anuj    Reviewer:    Offscreen    eleventh
    [Setup]    Telephony Feature Custom Setup
    Given using ${bossPortal} I program 2 Call Appearance button on ${phone1}
    &{telephonydetails} =  Create Dictionary    CallStackDepth=3
    Then using ${bossPortal} on ${phone1} I want to change call stack depth using ${telephonydetails}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then i want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${line2}
    Then verify the led state of ${line2} as ${on} on ${phone1}
    Then verify no audio path from ${phone1} to ${phone2}
    Then verify no audio path from ${phone2} to ${phone1}
    Then i want to make a two party call between ${phone4} and ${phone1} using ${loudspeaker}
    Then verify extension ${number} of ${phone4} on ${phone1}
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then press hardkey as ${scrollUp} on ${phone1}
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then on ${phone1} wait for 2 seconds
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then press hardkey as ${scrollDown} on ${phone1}
    Then verify extension ${number} of ${phone4} on ${phone1}
    Then press hardkey as ${scrollDown} on ${phone1}
    Then verify extension ${number} of ${phone4} on ${phone1}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone4}
    And using ${bossPortal} I remove unused keys on ${phone1}
    &{telephonydetails} =  Create Dictionary    CallStackDepth=10
    Then using ${bossPortal} on ${phone1} I want to change call stack depth using ${telephonydetails}
    [Teardown]    Telephony Feature Custom Teardown

561206: Regression - Assign-Unassign Phone, Password Change Checkbox=False
    [Tags]    Owner:Anuj    Reviewer:    assign_unassign    notApplicableForMiCloud    eleventh
    [Setup]    RUN KEYWORDS    Telephony Feature Custom Setup    Assign Extension Custom Setup
    &{telephonydetails} =  Create Dictionary    VM_pwd_change_on_next_login=False
    Given using ${bossPortal} on ${phone1} I want to uncheck voicemail password on next login using ${telephonydetails}
    Then on ${phone1} navigate to ${unassignUser} settings
    Then on ${phone1} wait for 10 seconds
    Then on ${phone1} verify display message ${assign}
    Then Go to reassign user on ${phone1} and ${phone1}
    Then on ${phone1} wait for 10 seconds
    Then Verify extension ${number} of ${phone1} on ${phone1}
    Then on ${phone1} navigate to ${unassignUser} settings
    Then on ${phone1} verify display message ${password}
    Then on ${phone1} enter number ${newExtn}
    Then on ${phone1} press ${hardKey} ${scrolldown} for 1 times
    Then on ${phone1} enter number ${voicemailPass}
    Then on ${phone1} press ${hardKey} ${Enter} for 1 times
    Then on ${phone1} verify display message ${vmpasschangewindow}
    Then on ${phone1} verify display message ${confirmnvm}
    Then on ${phone1} enter number ${newvmpass}
    Then on ${phone1} press ${hardKey} ${Enter} for 1 times
    Then on ${phone1} enter number ${newvmpass}
    Then on ${phone1} press ${hardKey} ${Enter} for 1 times
    Then on ${phone1} Wait for 16 seconds
    Then on ${phone1} verify display message ${newExtn}
    Then using ${bossPortal} I want to delete extension ${newExtn}
    Then on ${phone1} Wait for 10 seconds
    Then on ${phone1} verify display message ${available}
    Then on ${phone1} dial number #
    Then on ${phone1} Wait for 5 seconds
    Then on ${phone1} enter number ${phone1}
    Then on ${phone1} dial number ${loginVoicemail}
    Then on ${phone1} Wait for 3 seconds
    Then on ${phone1} dial number 7
    Then on ${phone1} Wait for 1 seconds
    Then on ${phone1} dial number 3
    Then on ${phone1} Wait for 1 seconds
    Then on ${phone1} dial number 1
    Then on ${phone1} Wait for 5 seconds
    Then Verify extension ${number} of ${phone1} on ${phone1}
    Then press hardkey as ${goodBye} on ${phone1}
    [Teardown]    RUN KEYWORDS    Assign Extension Custom Teardown    SET DEFAULT VOICEMAIL PASSWORD


561202: Regression - Access Directory, Password Change Checkbox=False
    [Tags]    Owner:Anuj    Reviewer:    directory    eleventh    notApplicableForMiCloud
    [Setup]    Telephony Feature Custom Setup
    &{telephonydetails} =  Create Dictionary    VM_pwd_change_on_next_login=False
    Given using ${bossPortal} on ${phone1} I want to uncheck voicemail password on next login using ${telephonydetails}
    Then press hardkey as ${directory} on ${phone1}
    Then on ${phone1} verify display message ${directory}
    Then press hardkey as ${goodbye} on ${phone1}
    [Teardown]    SET DEFAULT VOICEMAIL PASSWORD


559271: Hit BCA key of SCA user on Admin
    [Tags]    Owner:Anuj    Reviewer:    SCA    eleventh
    [Setup]    Telephony Feature Custom Setup
    &{telephonydetails} =  Create Dictionary    sca_enabled=True
    ${scaExtn} =  using ${bossPortal} on ${phone2} I want to enable SCA using ${telephonydetails}
    &{BCAdetails1} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=4    function=Bridge Call Appearance    label=BCA    target_extension=${scaExtn}    CallStackPosition=1
    Given using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails1}
    Then I want to press line key ${line1} on phone ${phone2}
    Then I want to press line key ${programKey5} on phone ${phone1}
    on ${phone1} verify display message ${lineInUse}
    &{telephonydetails} =  Create Dictionary    sca_enabled=False
    ${scaExtn} =  using ${bossPortal} on ${phone2} I want to disable SCA using ${telephonydetails}
    [Teardown]    Telephony Feature Custom Teardown


561204: Regression - Access History, Password Change Checkbox=False
    [Tags]    Owner:Anuj    Reviewer:    history    eleventh
    [Setup]    Telephony Feature Custom Setup
    &{telephonydetails} =  Create Dictionary    VM_pwd_change_on_next_login=False
    Then press hardkey as ${callersList} on ${phone1}
    And on ${phone1} verify display message ${callHistory}
    [Teardown]    SET DEFAULT VOICEMAIL PASSWORD


754445: XMON, CID Always - incoming call(s) + active picked-up call
    [Tags]    Owner:Anuj    Reviewer:    XMON    eleventh
    &{extensionDetails} =  Create Dictionary  ring_delay=none   show_caller_id=always    no_connected=dial_number    with_connected=dial_number    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['monitorExtn']}
    Then Set number of rings to 10 on ${phone2}
    Then I want to make a two party call between ${phone3} and ${phone2} using ${loudSpeaker}
    on ${phone1} press ${hardKey} ${programKey5} for 2 times
    Then verify the caller id on ${phone3} and ${phone1} display
    Then Verify the led state of ${line5} as ${on} on ${phone1}
    Then On ${phone1} verify ${line5} icon state as MONITOR_EXT_ACTIVE
    Then on ${phone2} verify the softkeys in ${idle}
    Then Set number of rings to 10 on ${phone4}
    Then i want to make a two party call between ${phone4} and ${phone2} using ${loudSpeaker}
    Then verify the caller id on ${phone4} and ${phone2} display
    Then Verify the led state of ${line5} as ${blink} on ${phone1}
    Then On ${phone1} verify ${line5} icon state as ${xmonRinging}
    Then verify the caller id on ${phone3} and ${phone1} display
    Then on ${phone1} press ${hardKey} ${programKey5} for 1 times
    Then verify extension ${number} of ${phone4} on ${phone1}
    Then On ${phone1} verify display message ${answer}
    Then On ${phone1} verify display message To Vm
    Then On ${phone1} verify display message ${cancel}
    Then I want to verify on ${phone1} negative display message ${phone3}
    Then on ${phone1} press ${softkey} ${bottomKey1} for 1 times
    Then verify the caller id on ${phone2} and ${phone3} display
    Then verify the caller id on ${phone4} and ${phone1} display
    Then Verify the led state of ${line5} as ${blink} on ${phone1}
    On ${phone1} verify ${line5} icon state as MONITOR_EXT_ACTIVE
    Then Set number of rings to 5 on ${phone4}
    Then Set number of rings to 5 on ${phone2}
    Then disconnect the call from ${phone1}
    Then disconnect the call from ${phone3}
    [Teardown]    RUN KEYWORDS    GENERIC TEST TEARDOWN    Default Number of Rings

754467: XMON, CID Only When Ringing - multiple incoming calls on target
    [Tags]    Owner:Anuj    Reviewer:    XMON    eleventh
    &{extensionDetails} =  Create Dictionary  ring_delay=none   show_caller_id=only_when_ringing    no_connected=dial_number    with_connected=dial_number    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['monitorExtn']}
    Then on ${phone2} navigate to ${availability} settings
    Then Modify call handler mode on ${phone2} to ${never} in ${available}
    Then on ${phone2} press ${softKey} ${bottomKey1} for 1 times
    Then i want to make a two party call between ${phone3} and ${phone2} using ${loudspeaker}
    Then i want to make a two party call between ${phone4} and ${phone2} using ${loudspeaker}
    Then i want to make a two party call between ${phone5} and ${phone2} using ${loudspeaker}
    Then verify the led state of ${line1} as ${blink} on ${phone2}
    Then verify the led state of ${line2} as ${blink} on ${phone2}
    Then verify the led state of ${line3} as ${blink} on ${phone2}
    Then verify the led state of ${line5} as ${blink} on ${phone1}
    Then On ${phone1} verify ${line5} icon state as ${xmonRinging}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then verify extension ${number} of ${phone3} on ${phone1}
    Then Press hardkey as ${scrollDown} on ${phone1}
    Then verify extension ${number} of ${phone4} on ${phone1}
    Then Press hardkey as ${scrollDown} on ${phone1}
    Then verify extension ${number} of ${phone5} on ${phone1}
    Then on ${phone1} verify display message ${answer}
    Then on ${phone1} verify display message To Vm
    Then on ${phone1} verify display message ${cancel}
    Then on ${phone1} press ${softKey} ${bottomKey4} for 3 times
    Then i want to verify on ${phone1} negative display message ${answer}
    Then on ${phone1} verify display message ${pickup}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then Press hardkey as ${scrollDown} on ${phone1}
    Then on ${phone1} press ${softKey} ${bottomKey2} for 1 times
    Then on ${phone4} verify display message ${displayVoiceMail}
    Then verify the led state of ${line2} as ${off} on ${phone2}
    Then Press hardkey as ${scrollDown} on ${phone1}
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then on ${phone1} verify display message ${drop}
    Then verify the led state of ${line5} as ${blink} on ${phone1}
    Then verify the caller id on ${phone1} and ${phone5} display
    Then On ${phone1} verify ${line5} icon state as ${xmonRinging}
    Then disconnect the call from ${phone5}
    And disconnect the call from ${phone3}
    [Teardown]    RUN KEYWORDS    Generic Test Teardown    Default Availability State


753692: Admin1 BCA calls A, admin2 picks up and BCA confs in, admin2 hangs up, no prompt
    [Tags]      Owner:Anuj     Reviewer:      BCA    eleventh
    [SETUP]    BCA Custom Setup
    &{createBCAExtension} =  Create Dictionary    name=bca_anuj1   backupExtn=${phone4}    switch=2    callStackDepth=1    forwardAfter=2    callStackFull=${EMPTY}   noAnswer=${EMPTY}    outboundCallerID=${EMPTY}    allowBridgeConferencing=true   defaultPrivacySettings=0
    ${bcaExtn}=    using ${bossPortal} I want to create Bridge Call Appearance extension using ${createBCAExtension}
    &{BCAdetails1} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=4    function=Bridge Call Appearance    label=BCA1    target_extension=${bcaExtn}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${EMPTY}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=${EMPTY}
    &{BCAdetails2} =  Create Dictionary    user_extension=${phone2}    button_box=0    soft_key=4    function=Bridge Call Appearance    label=BCA2    target_extension=${bcaExtn}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${EMPTY}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=${EMPTY}

    Given using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails1}
    Then on ${phone1} verify display message BCA1
    Then using ${bossPortal} I want to create bca on ${phone2} using ${BCAdetails2}
    Then on ${phone2} verify display message BCA2

    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} enter number ${phone3}
    Then on ${phone1} wait for 5 seconds
    Then answer the call on ${phone3} using ${loudspeaker}
    Then on ${phone3} press ${softKey} ${bottomKey2} for 1 times
    Then on ${phone3} enter number ${phone2}
    Then on ${phone3} press ${softKey} ${bottomKey2} for 1 times
    Then answer the call on ${phone2} using ${loudspeaker}
    Then press hardkey as ${goodbye} on ${phone2}
    Then on ${phone2} verify the softkeys in ${IdleState}
    Then press hardkey as ${goodbye} on ${phone1}
    And on ${phone2} verify the softkeys in ${IdleState}
    [Teardown]    BCA Custom Teardown

753460: Admin calls 2 parties and conf call. Hotline boss, Boss Joins, Admin drops, Boss locks& Unlocks, admin joins
    [Tags]      Owner:Anuj     Reviewer:      BCA    eleventh
    [Setup]    Telephony Feature Custom Setup
    &{telephonydetails} =  Create Dictionary    sca_enabled=True
    ${scaExtn} =  using ${bossPortal} on ${phone4} I want to enable SCA using ${telephonydetails}
    &{createBCAExtension} =  Create Dictionary    extension=${scaExtn}    backupExtn=${phone4}    allowBridgeConferencing=true   defaultPrivacySettings=0
    ${bcaExtn}=    using ${bossPortal} I want to modify Bridge Call Appearance extension using ${createBCAExtension}
    &{BCAdetails} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=4    function=Bridge Call Appearance    label=BCA    target_extension=${bcaExtn}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${EMPTY}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=${EMPTY}
    &{BCAdetails1} =  Create Dictionary    user_extension=${phone4}    button_box=0    soft_key=4    function=Bridge Call Appearance    label=BCA    target_extension=${bcaExtn}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${EMPTY}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=${EMPTY}
    Given using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails}
    Then on ${phone1} verify display message ${bca}
    Given using ${bossPortal} I want to create bca on ${phone4} using ${BCAdetails1}
    Then on ${phone4} verify display message ${bca}
    &{hotlineDetails}    CREATE DICTIONARY    ConnectedCallFunctionID=intercom    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${hotline} on ${phone1} using ${hotlineDetails} and extension of ${phone4} and softkey position 3 with extensionValue
    Then On ${phone1} verify display message ${hotline}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} enter number ${phone2}
    Then on ${phone1} wait for 5 seconds
    Then answer the call on ${phone2} using ${loudspeaker}
    Then on ${phone1} press the softkey ${conference} in answerstate
    Then on ${phone1} enter number ${phone3}
    Then on ${phone1} press ${softKey} ${bottomKey2} for 1 times
    Then answer the call on ${phone3} using ${loudspeaker}
    Then conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then I want to press line key ${programKey4} on phone ${phone1}
    Then verify the led state of ${line2} as ${blink} on ${phone4}
    Then answer the call on ${phone4} using ${line2}
    Then I want to press line key ${programKey5} on phone ${phone4}
    Then on ${phone1} wait for 6 seconds
    Then press hardkey as ${scrollUp} on ${phone1}
    Then on ${phone1} wait for 2 seconds
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} wait for 2 seconds
    Then press hardkey as ${goodbye} on ${phone1}
    Then on ${phone1} verify the softkeys in ${IdleState}
    Then on ${phone4} press the softkey ${lock} in ConferenceCallState
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then On ${phone1} verify display message ${actionNotPermitted}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone4}
    [Teardown]    Telephony Feature Custom Teardown


754284: TC026 Program a speed dial key on PKM
    [Tags]      Owner:Anuj     Reviewer:      pkm    eleventh
    Given using ${bossPortal} I program ${dialNumber} on ${phone1} using ${bossDetailsPKM} and extension of ${phone2} and softkey position 4 with extensionValue
    Then verify display message ${displayMessage['dialNumber']} on PKM for ${phone1}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetailsPKM} and softkey position 4


753812: BCA1 on phone calls A, BCA2 on BB calls B, uses conf to join to BCA1
    [Tags]      Owner:Anuj     Reviewer:      pkm    753812    eleventh
    [Setup]    BCA Custom Setup
    &{createBCAExtension1} =  Create Dictionary    name=anuj1   backupExtn=${phone3}    switch=2    callStackDepth=2    forwardAfter=2    callStackFull=${EMPTY}   noAnswer=${EMPTY}    outboundCallerID=${EMPTY}    allowBridgeConferencing=true   defaultPrivacySettings=0
    &{createBCAExtension2} =  Create Dictionary    name=anuj2   backupExtn=${phone3}    switch=2    callStackDepth=2    forwardAfter=2    callStackFull=${EMPTY}   noAnswer=${EMPTY}    outboundCallerID=${EMPTY}    allowBridgeConferencing=true   defaultPrivacySettings=0
    ${bcaExtn1}=    using ${bossPortal} I want to create Bridge Call Appearance extension using ${createBCAExtension1}
    ${bcaExtn2}=    using ${bossPortal} I want to create Bridge Call Appearance extension using ${createBCAExtension2}
    &{BCAdetails1} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=3    function=Bridge Call Appearance    label=BCA1    target_extension=${bcaExtn1}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${phone3}     show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=${EMPTY}
    &{BCAdetails2} =  Create Dictionary    user_extension=${phone1}    button_box=1    soft_key=4    function=Bridge Call Appearance    label=BCA2    target_extension=${bcaExtn2}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${phone3}     show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=${EMPTY}
    Given using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails1}
    Then using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails2}
    Then on ${phone1} verify display message BCA1
    Then verify display message BCA2 on PKM for ${phone1}
    Then I want to press line key ${programKey4} on phone ${phone1}
    Then on ${phone1} enter number ${phone2}
    Then on ${phone1} wait for 4 seconds
    Then Answer the call on ${phone2} using ${loudspeaker}
    Then I want to press PKM line key ${programKey5} on ${phone1}
    Then on ${phone1} enter number ${phone4}
    Then on ${phone1} wait for 4 seconds
    Then Answer the call on ${phone4} using ${loudspeaker}
    Then on ${phone1} press ${softKey} ${bottomKey2} for 1 times
    Then I want to press line key ${programKey4} on phone ${phone1}
    Then on ${phone1} wait for 4 seconds
    Then Verify the PKM led state of ${line5} as ${off} on ${phone1}
    Then conference call audio verify between ${phone1} ${phone2} and ${phone4}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone4}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetailsPKM} and softkey position 4
    [Teardown]     BCA Custom Teardown

753810: BCA1 on BB calls A, BCA2 on phone calls B, uses conf to join to BCA1
    [Tags]      Owner:Anuj     Reviewer:      pkm    753810    eleventh
    [Setup]    BCA Custom Setup
    &{createBCAExtension1} =  Create Dictionary    name=anuj1   backupExtn=${phone4}    switch=2    callStackDepth=2    forwardAfter=2    callStackFull=${EMPTY}   noAnswer=${EMPTY}    outboundCallerID=${EMPTY}    allowBridgeConferencing=true   defaultPrivacySettings=0
    &{createBCAExtension2} =  Create Dictionary    name=anuj2   backupExtn=${phone4}    switch=2    callStackDepth=2    forwardAfter=2    callStackFull=${EMPTY}   noAnswer=${EMPTY}    outboundCallerID=${EMPTY}    allowBridgeConferencing=true   defaultPrivacySettings=0
    ${bcaExtn1}=    using ${bossPortal} I want to create Bridge Call Appearance extension using ${createBCAExtension1}
    ${bcaExtn2}=    using ${bossPortal} I want to create Bridge Call Appearance extension using ${createBCAExtension2}
    &{BCAdetails1} =  Create Dictionary    user_extension=${phone1}    button_box=1    soft_key=3    function=Bridge Call Appearance    label=BCA1    target_extension=${bcaExtn1}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${phone3}     show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=${EMPTY}
    &{BCAdetails2} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=4    function=Bridge Call Appearance    label=BCA2    target_extension=${bcaExtn2}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${phone3}     show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=${EMPTY}
    Given using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails1}
    Then using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails2}
    Then verify display message BCA1 on PKM for ${phone1}
    Then on ${phone1} verify display message BCA2
    Then I want to press PKM line key ${programKey4} on ${phone1}
    Then on ${phone1} enter number ${phone2}
    Then on ${phone1} wait for 4 seconds
    Then Answer the call on ${phone2} using ${loudspeaker}

    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} enter number ${phone3}
    Then on ${phone1} wait for 4 seconds
    Then Answer the call on ${phone3} using ${loudspeaker}
    Then on ${phone1} press ${softKey} ${bottomKey2} for 1 times
    Then I want to press PKM line key ${programKey4} on ${phone1}

    Then on ${phone1} wait for 6 seconds
    Then verify the led state of ${line5} as ${off} on ${phone1}
    Then conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetailsPKM} and softkey position 3
    [Teardown]     BCA Custom Teardown

759616: Monitoring the Intercom extension "Active or Held Call"
# this is pkm version test case
    [Tags]      Owner:Anuj     Reviewer:      pkm21    eleventh
    Given verify ${available} state icon on ${phone1}
    &{extensionDetails} =  Create Dictionary    ring_delay=1    show_caller_id=only_when_ringing    no_connected=unused    with_connected=transfer_blind    account_name=Automation    part_name=SC1    button_box=1
    Then using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then Verify the PKM led state of ${line5} as ${off} on ${phone1}
    Then i want to make a two party call between ${phone3} and ${phone2} using ${loudspeaker}
    Then Verify the PKM led state of ${line5} as ${blink} on ${phone1}
    Then disconnect the call from ${phone3}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetailsPKM} and softkey position 4

753628: A calls BCA, B Calls BCA, RA and B both put BCA on hold, Admin joins, Admin drops no park, Call leaves BCA
    [Tags]      Owner:Anuj     Reviewer:      BCA    eleventh    753628
    [Setup]    BCA Custom Setup
    &{createBCAExtension1} =  Create Dictionary    name=bca_anuj1   backupExtn=${phone4}    switch=2    callStackDepth=2    forwardAfter=2    callStackFull=${EMPTY}   noAnswer=${EMPTY}    outboundCallerID=${EMPTY}    allowBridgeConferencing=true   defaultPrivacySettings=0
    ${bcaExtn1}=    using ${bossPortal} I want to create Bridge Call Appearance extension using ${createBCAExtension1}
    &{BCAdetails1} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=3    function=Bridge Call Appearance    label=BCA1    target_extension=${bcaExtn1}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${EMPTY}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=${EMPTY}
    &{createBCAExtension2} =  Create Dictionary    name=bca_anuj2   backupExtn=${phone4}    switch=2    callStackDepth=2    forwardAfter=2    callStackFull=${EMPTY}   noAnswer=${EMPTY}    outboundCallerID=${EMPTY}    allowBridgeConferencing=true   defaultPrivacySettings=0
    ${bcaExtn2}=    using ${bossPortal} I want to create Bridge Call Appearance extension using ${createBCAExtension2}
    &{BCAdetails2} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=4    function=Bridge Call Appearance    label=BCA2    target_extension=${bcaExtn2}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${EMPTY}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=${EMPTY}
    Given using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails1}
    Then using ${bossPortal} I want to create bca on ${phone2} using ${BCAdetails2}
    Then on ${phone1} verify display message BCA1
    Then on ${phone1} verify display message BCA2
    Then on ${phone2} dial number ${bcaExtn1}
    Then On ${phone1} Wait for 3 seconds
    Then I want to press line key ${programKey4} on phone ${phone1}
    Then Verify audio path between ${phone1} and ${phone2}
    Then on ${phone3} dial number ${bcaExtn2}
    Then On ${phone1} Wait for 3 seconds
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then Verify audio path between ${phone1} and ${phone3}
    Then press hardkey as ${holdstate} on ${phone3}
    Then on ${phone1} press ${softkey} ${bottomKey2} for 1 times
    Then I want to press line key ${programKey4} on phone ${phone1}
    Then on ${phone1} wait for 2 seconds
    Then verify the led state of ${line5} as ${off} on ${phone1}
    Then on ${phone1} verify display message ${leave}
    Then on ${phone2} verify display message ${leave}
    Then on ${phone3} verify display message ${leave}
    Then press hardkey as ${goodBye} on ${phone1}
    Then press hardkey as ${holdstate} on ${phone3}
    Then verify the caller id on ${phone3} and ${phone2} display
    Then Verify audio path between ${phone3} and ${phone2}
    Then disconnect the call from ${phone2}
    [Teardown]     BCA Custom Teardown

753676: BCA1 conf A, B, C;BCA2 conf D, use conf button to join to BCA2
    [Tags]    Owner:Anuj    Reviewer:    sca    eleventh
    [Setup]    Telephony Feature Custom Setup
    &{telephonydetails} =  Create Dictionary    sca_enabled=True
    ${scaExtn} =  using ${bossPortal} on ${phone2} I want to enable SCA using ${telephonydetails}
    &{BCAdetails1} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=3    function=Bridge Call Appearance    label=BCA1    target_extension=${scaExtn}
    &{BCAdetails2} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=4    function=Bridge Call Appearance    label=BCA2    target_extension=${scaExtn}
    Given using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails1}
    Then using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails2}
    Then on ${phone1} verify display message BCA1
    Then on ${phone1} verify display message BCA2
    Then I want to press line key ${programKey4} on phone ${phone1}
    Then on ${phone1} enter number ${phone6}
    Then on ${phone6} wait for 4 seconds
    Then answer the call on ${phone6} using ${loudspeaker}
    Then on ${phone1} press ${softkey} ${bottomkey2} for 1 times
    Then on ${phone1} enter number ${phone3}
    Then on ${phone1} press ${softkey} ${bottomkey2} for 1 times
    Then answer the call on ${phone3} using ${loudspeaker}
    Then on ${phone1} press ${softkey} ${bottomkey2} for 1 times
    Then on ${phone1} enter number ${phone4}
    Then on ${phone1} press ${softkey} ${bottomkey2} for 1 times
    Then answer the call on ${phone4} using ${loudspeaker}
    Then four party conference call audio verification between ${phone1} ${phone6} ${phone3} and ${phone4}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} enter number ${phone5}
    Then on ${phone5} wait for 4 seconds
    Then answer the call on ${phone5} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone5}
    Then on ${phone1} press ${softkey} ${bottomkey2} for 1 times
    Then I want to press line key ${programKey4} on phone ${phone1}
    Then verify the led state of ${line5} as ${off} on ${phone1}
    Then verify the led state of ${line4} as ${on} on ${phone1}
    Then disconnect the call from ${phone3}
    Then disconnect the call from ${phone4}
    Then disconnect the call from ${phone5}
    And disconnect the call from ${phone6}

754270: TC012 Program two speed dial keys with same label name
    [Tags]    Owner:Anuj    Reviewer:    speed_dial    eleventh
    Given using ${bossPortal} I program ${dialNumber} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 3 with extensionValue
    Then using ${bossPortal} I program ${dialNumber} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['dialNumber']}

753628: A calls BCA, B Calls BCA, RA and B both put BCA on hold, Admin joins, Admin drops no park, Call leaves BCA
    [Tags]      Owner:Anuj     Reviewer:      BCA    eleventh
    [Setup]    BCA Custom Setup
    &{createBCAExtension1} =  Create Dictionary    name=bca_anuj1   backupExtn=${phone4}    switch=2    callStackDepth=2    forwardAfter=2    callStackFull=${EMPTY}   noAnswer=${EMPTY}    outboundCallerID=${EMPTY}    allowBridgeConferencing=true   defaultPrivacySettings=0
    ${bcaExtn1}=    using ${bossPortal} I want to create Bridge Call Appearance extension using ${createBCAExtension1}
    &{BCAdetails1} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=3    function=Bridge Call Appearance    label=BCA1    target_extension=${bcaExtn1}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${EMPTY}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=${EMPTY}
    &{createBCAExtension2} =  Create Dictionary    name=bca_anuj2   backupExtn=${phone4}    switch=2    callStackDepth=2    forwardAfter=2    callStackFull=${EMPTY}   noAnswer=${EMPTY}    outboundCallerID=${EMPTY}    allowBridgeConferencing=true   defaultPrivacySettings=0
    ${bcaExtn2}=    using ${bossPortal} I want to create Bridge Call Appearance extension using ${createBCAExtension2}
    &{BCAdetails2} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=4    function=Bridge Call Appearance    label=BCA2    target_extension=${bcaExtn2}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${EMPTY}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=${EMPTY}
    Given using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails1}
    Then using ${bossPortal} I want to create bca on ${phone2} using ${BCAdetails2}
    Then on ${phone1} verify display message BCA1
    Then on ${phone1} verify display message BCA2
    Then on ${phone2} dial number ${bcaExtn1}
    Then On ${phone1} Wait for 3 seconds
    Then I want to press line key ${programKey4} on phone ${phone1}
    Then verify audio path between ${phone1} and ${phone2}
    Then on ${phone3} dial number ${bcaExtn2}
    Then On ${phone1} Wait for 3 seconds
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then verify audio path between ${phone1} and ${phone3}
    Then press hardkey as ${holdstate} on ${phone3}
    Then on ${phone1} press ${softkey} ${bottomKey2} for 1 times
    Then I want to press line key ${programKey4} on phone ${phone1}
    Then on ${phone1} wait for 2 seconds
    Then verify the led state of ${line5} as ${off} on ${phone1}
    Then on ${phone1} verify display message ${leave}
    Then on ${phone2} verify display message ${leave}
    Then on ${phone3} verify display message ${leave}
    Then press hardkey as ${goodBye} on ${phone1}
    Then press hardkey as ${holdstate} on ${phone3}
    Then verify the caller id on ${phone3} and ${phone2} display
    Then verify audio path between ${phone3} and ${phone2}
    Then disconnect the call from ${phone2}
    [Teardown]     BCA Custom Teardown


564948:Speed dial keys
    [Tags]     Owner:Abhishekkhanchi      Reviewer:AvishekRanjan       speed_dial_6910    Onlyfor6910
    Given using ${bossPortal} I program ${dialNumber} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then verify ringing state on ${phone1} and ${phone2}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify the led state of ${line5} as ${on} on ${phone1}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 5
    Then disconnect the call from ${phone2}

564950: Other than Speeddial keys
    [Tags]     Owner:Abhishekkhanchi      Reviewer:AvishekRanjan       speed_dial_6910     Onlyfor6910
    Given using ${bossPortal} I program ${whisperPage} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then On ${phone1} verify display message ${dial}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 5


558726: Conf allowed : phone displayed unlock
    [Tags]    Owner:Abhishekkhanchi    Reviewer:    bca    twelfth
    [Setup]    BCA Custom Setup
    &{createBCAExtension} =  Create Dictionary    name=BCA_AbhishekK   backupExtn=${phone3}    switch=2    callStackDepth=1    forwardAfter=2    callStackFull=${EMPTY}   noAnswer=${EMPTY}    outboundCallerID=${EMPTY}    allowBridgeConferencing=true   defaultPrivacySettings=1
    ${bcaExtn}=    using ${bossPortal} I want to create Bridge Call Appearance extension using ${createBCAExtension}
    &{BCAdetails} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=4    function=Bridge Call Appearance    label=${bca}    target_extension=${bcaExtn}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${phone3}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=Dial Extension
    &{BCAdetails_two} =  Create Dictionary    user_extension=${phone2}    button_box=0    soft_key=4    function=Bridge Call Appearance    label=${bca}    target_extension=${bcaExtn}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${EMPTY}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=${EMPTY}
    Given using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails}
    Given using ${bossPortal} I want to create bca on ${phone2} using ${BCAdetails_two}
    Then On ${phone1} verify display message ${bca}
    Then On ${phone2} verify display message ${bca}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then answer the call on ${phone3} using ${loudSpeaker}
    Then Verify audio path between ${phone1} and ${phone3}
    Then On ${phone1} verify the softkeys in ${bca}
    [Teardown]    BCA Custom Teardown

558741: Regular Make me conf on DUT1 - DUT1 holds - DUT2 barges - Stays make me
    [Tags]    Owner:Abhishekkhanchi    Reviewer:    bca    0014
    &{createBCAExtension} =  Create Dictionary    name=BCA_AbhishekK   backupExtn=${phone3}    switch=2    callStackDepth=1    forwardAfter=2    callStackFull=${EMPTY}   noAnswer=${EMPTY}    outboundCallerID=${EMPTY}    allowBridgeConferencing=true   defaultPrivacySettings=0
    ${bcaExtn}=    using ${bossPortal} I want to create Bridge Call Appearance extension using ${createBCAExtension}
    &{BCAdetails} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=4    function=Bridge Call Appearance    label=${bca}    target_extension=${bcaExtn}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${phone3}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=${EMPTY}
    &{BCAdetails_two} =  Create Dictionary    user_extension=${phone2}    button_box=0    soft_key=4    function=Bridge Call Appearance    label=${bca}    target_extension=${bcaExtn}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${EMPTY}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=${EMPTY}
    &{BCAdetails_three} =  Create Dictionary    user_extension=${phone3}    button_box=0    soft_key=4    function=Bridge Call Appearance    label=${bca}    target_extension=${bcaExtn}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${EMPTY}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=${EMPTY}
    Given using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails}
    Given using ${bossPortal} I want to create bca on ${phone2} using ${BCAdetails_two}
    Given using ${bossPortal} I want to create bca on ${phone3} using ${BCAdetails_three}
    Then verify display message ${bca} on ${phone1}
    Then verify display message ${bca} on ${phone2}
    Then verify display message ${bca} on ${phone3}
    Then on ${phone4} dial number ${bcaExtn}
    Then on ${phone1} wait for 4 seconds
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then Verify audio path between ${phone1} and ${phone4}
    Then on ${phone1} press the softkey ${conference} in ConferenceCallState
    Then I want to make a two party call between ${phone1} and ${phone5} using ${loudSpeaker}
    Then answer the call on ${phone5} using ${loudSpeaker}
    Then on ${phone1} wait for 4 seconds
    Then on ${phone1} press the softkey ${conference} in ConferenceCallState
    Then on ${phone1} wait for 4 seconds
    Then on ${phone1} press the softkey ${conference} in ConferenceCallState
    Then on ${phone1} enter number ${phone6}
    Then on ${phone1} press the softkey ${conference} in ConferenceCallState
    Then answer the call on ${phone6} using ${loudSpeaker}
    Then on ${phone1} wait for 3 seconds
    Then on ${phone1} press ${hardKey} ${holdState} for 1 times
    Then Verify audio path between ${phone4} and ${phone5}
    Then Verify audio path between ${phone4} and ${phone6}
    Then Verify audio path between ${phone5} and ${phone6}
    Then I want to press line key ${programKey5} on phone ${phone2}
    Then Verify audio path between ${phone2} and ${phone4}
    Then Verify audio path between ${phone2} and ${phone5}
    Then Verify audio path between ${phone2} and ${phone6}
    Then Verify audio path between ${phone4} and ${phone5}
    Then Verify audio path between ${phone4} and ${phone6}
    Then Verify audio path between ${phone5} and ${phone6}
    Then verify no audio path from ${phone1} to ${phone4}
    Then verify no audio path from ${phone1} to ${phone5}
    Then verify no audio path from ${phone1} to ${phone6}
    Then verify no audio path from ${phone1} to ${phone2}
    Then on ${phone1} press ${hardKey} ${holdState} for 1 times
    Then Verify audio path between ${phone1} and ${phone2}
    Then Verify audio path between ${phone1} and ${phone4}
    Then Verify audio path between ${phone1} and ${phone5}
    Then Verify audio path between ${phone1} and ${phone6}
    Then Verify audio path between ${phone2} and ${phone4}
    Then Verify audio path between ${phone2} and ${phone5}
    Then Verify audio path between ${phone2} and ${phone6}
    Then Verify audio path between ${phone4} and ${phone5}
    Then Verify audio path between ${phone4} and ${phone6}
    Then Verify audio path between ${phone5} and ${phone6}

560113: Park call doesnt answer or Pickup
     [Tags]    Owner:Abhishekkhanchi    Reviewer:    park    twelfth
    Given using ${bossPortal} I program ${park} on ${phone1} using ${bossDetails} and extension of ${phone1} and softkey position 4 with noExtensionValue
    Then On ${phone1} verify display message ${park}
    Then I want to make a two party call between ${phone1} and ${phone2} using ${loudSpeaker}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} enter number ${phone3}
    Then on ${phone1} wait for 4 seconds
    Then Verify the led state of ${line1} as ${blink} on ${phone3}
    Then on ${phone3} wait for 60 seconds
    Then Verify the led state of ${line1} as ${blink} on ${phone1}
    Then And On ${phone3} verify the softkeys in ${idle}
    Then disconnect the call from ${phone1}



560114: Park call is answered or Pickedup
    [Tags]    Owner:Abhishekkhanchi    Reviewer:    park    twelfth
    Given using ${bossPortal} I program ${park} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${park}
    Then I want to make a two party call between ${phone1} and ${phone2} using ${loudSpeaker}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then Verify the led state of ${line1} as ${blink} on ${phone3}
    Then On ${phone1} verify the softkeys in ${idle}
    Then I want to press line key ${programKey1} on phone ${phone3}
    Then Verify audio path between ${phone2} and ${phone3}
    Then disconnect the call from ${phone3}


558305: No Answer on Agents while call Blind transfers through HG extension
     [Tags]    Owner:Abhishekkhanchi    Reviewer:    HG Blind    twelfth
     [Setup]    Hunt Group Custom Setup
     Given I want to make a two party call between ${phone1} and ${phone2} using ${loudSpeaker}
     Then on ${phone2} press the softkey ${transfer} in RingingState
     Then on ${phone2} dial number ${HGExtension}
     Then on ${phone2} wait for 2 seconds
     Then Verify the led state of ${line1} as ${blink} on ${phone2}
     Then And Verify extension ${number} of ${phone1} on ${phone2}
     Then on ${phone2} wait for 2 seconds
     Then Verify the led state of ${line1} as ${blink} on ${phone3}
     Then And Verify extension ${number} of ${phone1} on ${phone3}
     Then And On ${phone2} verify the softkeys in ${IdleState}
     Then on ${phone2} wait for 2 seconds
     Then Verify the led state of ${line1} as ${blink} on ${phone4}
     Then And Verify extension ${number} of ${phone1} on ${phone4}
     Then on ${phone2} wait for 2 seconds
     Then Verify the led state of ${line1} as ${blink} on ${phone2}
     Then And Verify extension ${number} of ${phone1} on ${phone2}
     Then on ${phone2} wait for 2 seconds
     Then Verify the led state of ${line1} as ${blink} on ${phone3}
     Then And Verify extension ${number} of ${phone1} on ${phone3}
     Then And On ${phone2} verify the softkeys in ${IdleState}
     Then on ${phone2} wait for 2 seconds
     Then Verify the led state of ${line1} as ${blink} on ${phone4}
     Then And Verify extension ${number} of ${phone1} on ${phone4}
     Then on ${phone2} wait for 2 seconds
     Then Verify the led state of ${line1} as ${blink} on ${phone2}
     Then And Verify extension ${number} of ${phone1} on ${phone2}
     Then on ${phone2} wait for 2 seconds
     Then Verify the led state of ${line1} as ${blink} on ${phone3}
     Then And Verify extension ${number} of ${phone1} on ${phone3}
     Then And On ${phone2} verify the softkeys in ${IdleState}
     Then on ${phone2} wait for 2 seconds
     Then Verify the led state of ${line1} as ${blink} on ${phone4}
     Then And Verify extension ${number} of ${phone1} on ${phone4}
     Then And On ${phone3} verify the softkeys in ${IdleState}
     Then on ${phone2} wait for 4 seconds
     Then Verify the led state of ${line1} as ${blink} on ${phone2}
     Then And Verify extension ${number} of ${phone1} on ${phone2}
     Then And On ${phone4} verify the softkeys in ${IdleState}
     Then using ${bossPortal} I want to remove hunt group user extension ${HGExtension}
     [Teardown]    Hunt Group Custom Teardown

558303: Consult Transfer incoming call to multiple Agents via Huntgroup Extension
    [Tags]    Owner:Abhishekkhanchi    Reviewer:    HGConsult      notApplicableForMiCloud    twelfth
    [Setup]    Hunt Group Custom Setup
    @{members}   Create List      ${phone2}    ${phone3}    ${phone4}
    &{huntGroupDetails} =  Create Dictionary    BackupExtension=${phone1}    GroupMembers=${members}   GroupName=HG_AbhishekK_two   IncludeInSystem=True    MakeExtnPrivate=False    HuntPattern=1    RingsPerMember=3    NoAnswerRings=9    CallMemberWhenForwarding=True    SkipMemberOnCall=True    CallStackFull=${EMPTY}    NoAnswer=${EMPTY}
    ${HGExtension} =     using ${bossPortal} I want to create hunt group user extension with ${huntGroupDetails}
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudSpeaker}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then on ${phone2} press the softkey ${transfer} in RingingState
    Then on ${phone2} dial number ${HGExtension}
    Then on ${phone2} wait for 5 seconds
    Then Verify the led state of ${line2} as ${blink} on ${phone2}
    Then Verify extension ${number} of ${phone2} on ${phone2}
    Then on ${phone2} wait for 2 seconds
    Then Verify the led state of ${line1} as ${blink} on ${phone3}
    Then Verify extension ${number} of ${phone2} on ${phone3}
    Then on ${phone3} wait for 8 seconds
    Then Verify the led state of ${line1} as ${blink} on ${phone4}
    Then Verify extension ${number} of ${phone2} on ${phone4}
    Then answer the call on ${phone4} using ${loudSpeaker}
    Then On ${phone4} verify display message ${drop}
    Then On ${phone4} verify display message ${transfer}
    Then on ${phone2} press the softkey ${transfer} in RingingState
    Then Verify audio path between ${phone1} and ${phone4}
    Then disconnect the call from ${phone4}
    Then using ${bossPortal} I want to remove hunt group user extension ${HGExtension}
    [Teardown]    Hunt Group Custom Teardown

560469: Whisper Page (outgoing) during UCB Call
    [Tags]      Owner:Abhishekkhanchi     Reviewer:Surendersingh    whisper_page    twelfth
    Given using ${bossPortal} I program ${whisperPage} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${whisperPage}
    Then on ${phone1} press the key ${conference} in state ${idle}
    Then On ${phone1} Wait for 4 seconds
    Then On ${phone1} verify display message ${conference}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then Verify audio path between ${phone1} and ${phone2}
    Then On ${phone1} Wait for 4 seconds
    Then on ${phone1} press the softkey ${drop} in AnswerState
    Then on ${phone1} press the key ${conference} in state ${idle}
    Then On ${phone1} Wait for 4 seconds
    Then on ${phone1} dial number ${wrongAccessCode}
    Then On ${phone1} Wait for 4 seconds
    Then i want to verify on ${phone1} negative display message ${park}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then Verify audio path between ${phone1} and ${phone2}
    Then On ${phone1} Wait for 4 seconds
    Then on ${phone1} press the softkey ${drop} in AnswerState
    Then on ${phone1} press the key ${conference} in state ${idle}
    Then On ${phone1} Wait for 4 seconds
    Then on ${phone1} dial number ${accessCode}
    Then On ${phone1} Wait for 4 seconds
    Then On ${phone1} verify the softkeys in Talk
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then Verify the led state of ${line1} as ${blink} on ${phone1}
    Then Verify audio path between ${phone1} and ${phone2}
    Then On ${phone1} verify display message ${drop}
    Then on ${phone1} press the softkey ${drop} in AnswerState
    Then On ${phone1} verify display message ${pickup}
    Then on ${phone1} Press ${softKey} ${bottomKey1} for 1 times
    Then On ${phone1} verify display message ${drop}
    Then on ${phone1} press the softkey ${drop} in AnswerState
    Then And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4

560250:Silent Coach Agent transition to Consult Silent Coach with no Silent coach Permissions on Agent
    [Tags]    Owner:Abhishekkhanchi    Reviewer:AvishekRanjan    cos    twelfth
    &{COSDetails} =  Create Dictionary    Name=Fully Featured     AllowSilentMonitorInitiation=False
    Given using ${bossPortal} I program ${silentCoach} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 0 with extensionValue
    Given using ${bossPortal} I want to change telephony features values using ${COSDetails}
    Then i want to make a two party call between ${phone3} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then Verify audio path between ${phone3} and ${phone2}
    Then I want to press line key ${programKey1} on phone ${phone1}
    Then On ${phone1} verify display message ${displayMessage['notPermit']}
    Then on ${phone1} verify display message ${silentCoach}
    Then disconnect the call from ${phone3}
    &{COSDetails} =  Create Dictionary    Name=Fully Featured
    And using ${bossPortal} I want to change telephony features values using ${COSDetails}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 0
    [Teardown]    CoS Features custom teardown

560155:Un-park progbutton target not set (Directory or Call History)
    [Tags]    Owner:Abhishekkhanchi    Reviewer:AvishekRanjan    twelfth
     Given using ${bossPortal} I program ${unPark} on ${phone1} using ${bossDetails} and extension of ${phone1} and softkey position 4 with noExtensionValue
     Then I want to make a two party call between ${phone2} and ${phone3} using ${loudSpeaker}
     Then answer the call on ${phone3} using ${loudSpeaker}
     Then Verify audio path between ${phone3} and ${phone2}
     Then Put the linekey ${line1} of ${phone3} on ${hold}
     Then I want to press line key ${programKey5} on phone ${phone1}
     Then on ${phone1} verify the softkeys in ${unPark}
     Then On ${phone1} verify directory with ${directoryAction['selectOnly']} of ${phone3}
     Then Verify audio path between ${phone1} and ${phone2}
     Then disconnect the call from ${phone1}
     And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4

560487:Caller ID displays when call is auto-answered
    [Tags]    Owner:Abhishekkhanchi    Reviewer:AvishekRanjan    twelfth
     Given using ${bossPortal} I program ${intercom} on ${phone3} using ${bossDetails} and extension of ${phone1} and softkey position 4 with extensionValue
     Then I want to make a two party call between ${phone2} and ${phone1} using ${loudSpeaker}
     Then answer the call on ${phone1} using ${loudSpeaker}
     Then Verify audio path between ${phone2} and ${phone1}
     Then I want to press line key ${programKey5} on phone ${phone3}
     Then Verify audio path between ${phone1} and ${phone3}
     Then Verify the Caller id on ${phone1} and ${phone3} display
     Then disconnect the call from ${phone3}
     Then disconnect the call from ${phone2}
     Then And using ${bossPortal} remove the function key on ${phone3} using ${bossDetails} and softkey position 4

558348:Partial digits removed when Directory selected
    [Tags]    Owner:Abhishekkhanchi    Reviewer:AvishekRanjan    PD    twelfth    notApplicableForMiCloud
    Given using ${bossPortal} I want to change Delay after collecting digits value to 12000
    Given I want to make a two party call between ${phone2} and ${phone1} using ${loudSpeaker}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then answer the call on ${phone1} using ${loudSpeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then on ${phone1} press the softkey ${transfer} in AnswerState
    Then on ${phone1} enter number 69
    Then on ${phone1} verify the softkeys in ${transfer}
    Then on ${phone1} ${semiAttendedTransfer} call to ${phone3} using directory
    Then answer the call on ${phone3} using ${loudspeaker}
    Then On ${phone1} verify the softkeys in ${IdleState}
    Then Verify audio path between ${phone3} and ${phone2}
    Then using ${bossPortal} I want to change Delay after collecting digits value to 3000
    Then disconnect the call from ${phone3}
    [Teardown]    Telephony Options Custom Teardown

560467:Whisper Target receives an INTERCOM call while on a paged and a regular call
    [Tags]    Owner:Abhishekkhanchi    Reviewer:    twelfth
     Given using ${bossPortal} I program ${whisperPage} on ${phone2} using ${bossDetails} and extension of ${phone1} and softkey position 4 with extensionValue
     Then I want to make a two party call between ${phone4} and ${phone1} using ${loudSpeaker}
     Then On ${phone1} Wait for 4 seconds
     Then answer the call on ${phone1} using ${loudSpeaker}
     Then Verify audio path between ${phone4} and ${phone1}
     Then I want to press line key ${programKey5} on phone ${phone2}
     Then Verify audio path between ${phone2} and ${phone1}
     Then Verify no audio path from ${phone2} to ${phone4}
     Then i want to use fac ${intercom} on ${phone3} to ${phone1}
     Then On ${phone3} Wait for 4 seconds
     Then verify ringing state on ${phone3} and ${phone1}
     Then Verify the led state of ${line3} as ${blink} on ${phone1}
     Then answer the call on ${phone1} using Softkey
     Then Verify the led state of ${line3} as ${on} on ${phone1}
     Then Verify audio path between ${phone3} and ${phone1}
     Then Verify no audio path from ${phone2} to ${phone3}
     Then Verify the led state of ${line1} as ${blink} on ${phone1}
     Then disconnect the call from ${phone3}
     Then disconnect the call from ${phone2}
     Then disconnect the call from ${phone4}
     Then And using ${bossPortal} remove the function key on ${phone2} using ${bossDetails} and softkey position 4

559011: A calls Admin, Admin answers, B calls Boss, Admin answers. Admin attempts to join into A
    [Tags]    Owner:Abhishekkhanchi    Reviewer:RAM    bca      notApplicableForMiCloud    twelfth
    [Setup]    Telephony Feature Custom Setup
    &{telephonydetails} =  Create Dictionary    sca_enabled=True
    ${scaExtn} =  using ${bossPortal} on ${phone2} I want to enable SCA using ${telephonydetails}
    &{BCAdetails} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=4    function=Bridge Call Appearance    label=BCA    target_extension=${scaExtn}
    Given using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails}
    Then On ${phone1} verify display message ${bca}
    Then I want to make a two party call between ${phone4} and ${phone1} using ${loudSpeaker}
    Then on ${phone1} wait for 3 seconds
    Then answer the call on ${phone1} using ${loudSpeaker}
    Then Verify audio path between ${phone4} and ${phone1}
    Then on ${phone3} dial number ${scaExtn}
    Then on ${phone1} wait for 3 seconds
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} press the softkey ${conference} in AnswerState
    Then I want to press line key ${programKey1} on phone ${phone1}
    Then on ${phone1} wait for 3 seconds
    Then conference call audio verify between ${phone1} ${phone3} and ${phone4}
    Then Disconnect the call from ${phone1}
    Then Disconnect the call from ${phone3}
    Then Disconnect the call from ${phone4}
    Then on ${phone1} wait for 4 seconds
    Then I want to make a two party call between ${phone4} and ${phone1} using ${loudSpeaker}
    Then on ${phone1} wait for 3 seconds
    Then answer the call on ${phone1} using ${loudSpeaker}
    Then Verify audio path between ${phone4} and ${phone1}
    Then on ${phone3} dial number ${scaExtn}
    Then on ${phone1} wait for 3 seconds
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} press the softkey ${conference} in AnswerState
    Then On ${phone1} verify display message ${cancel}
    Then on ${phone1} press the softkey ${cancel} in DialingState
    Then Verify the Caller id on ${phone1} and ${phone3} display
    Then Disconnect the call from ${phone3}
    Then Disconnect the call from ${phone4}
    &{telephonydetails} =  Create Dictionary    sca_enabled=False
    Then using ${bossPortal} on ${phone2} I want to disable SCA using ${telephonydetails}
    [Teardown]    Telephony Feature Custom Teardown


559320:Call to user with hotline button (Hotline not configured on caller)
    [Tags]      Owner:Abhishekkhanchi     Reviewer:Ram    HT    twelfth
    Given using ${bossPortal} I remove unused keys on ${phone1}
    Then using ${bossPortal} I remove unused keys on ${phone2}
    Then using ${bossPortal} I program ${hotline} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message Hotline
    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then Verify the led state of ${line1} as ${blink} on ${phone1}
    Then Verify the led state of ${line5} as ${off} on ${phone1}
    Then Verify the Caller id on ${phone2} and ${phone1} display
    Then disconnect the call from ${phone2}
    Then using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4

559845:XMON, CID Never - shouldnt be able to unpark a conference call (with multiple held calls)
    [Tags]      Owner:Abhishekkhanchi     Reviewer:Ram    HT    twelfth
    &{extensionDetails} =  Create Dictionary  ring_delay=1   show_caller_id=Never    no_connected=unused    with_connected=unused    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 4 with ExtensionValue
    Then On ${phone1} verify display message ${displayMessage['monitorExtn']}
    Then verify the led state of ${line5} as ${off} on ${phone1}
    Then I want to make a two party call between ${phone2} and ${phone3} using ${loudSpeaker}
    Then on ${phone3} wait for 4 seconds
    Then answer the call on ${phone3} using ${loudSpeaker}
    Then Verify audio path between ${phone2} and ${phone3}
    Then on ${phone2} press ${hardKey} ${holdState} for 1 times
    Then verify the led state of ${line1} as ${blink} on ${phone2}
    Then verify the led state of ${line5} as ${blink} on ${phone1}
    Then I want to make a two party call between ${phone4} and ${phone2} using ${loudSpeaker}
    Then on ${phone2} wait for 4 seconds
    Then answer the call on ${phone2} using ${line2}
    Then on ${phone2} press the softkey ${conference} in AnswerState
    Then on ${phone2} enter number ${phone5}
    Then on ${phone5} wait for 5 seconds
    Then answer the call on ${phone5} using ${loudSpeaker}
    Then on ${phone5} wait for 3 seconds
    Then on ${phone2} press the softkey ${conference} in AnswerState
    Then conference call audio verify between ${phone2} ${phone4} and ${phone5}
    Then on ${phone5} wait for 3 seconds
    Then on ${phone2} press ${hardKey} ${holdState} for 1 times
    Then verify the led state of ${line2} as ${blink} on ${phone2}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then On ${phone1} verify display message Call
    Then On ${phone1} verify display message ${unPark}
    Then Verify extension ${number} of ${phone2} on ${phone1}
    Then press hardkey as ${scrollDown} on ${phone1}
    Then On ${phone1} verify display message ${conference}
    Then i want to verify on ${phone1} negative display message ${unPark}
    Then on ${phone1} wait for 3 seconds
    Then press hardkey as ${scrollUp} on ${phone1}
    Then On ${phone1} verify display message ${unPark}
    Then on ${phone1} Press ${softKey} ${bottomKey1} for 1 times
    Then verify the led state of ${line5} as ${on} on ${phone1}
    Then Verify audio path between ${phone1} and ${phone3}
    Then disconnect the call from ${phone4}
    Then disconnect the call from ${phone3}
    Then disconnect the call from ${phone5}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4


559030:Admin SCA calls A, Admin SCA calls B, Boss picks up A call, Admin joins
    [Tags]      Owner:Abhishekkhanchi     Reviewer:Ram    HT    twelfth
    [Setup]    Telephony Feature Custom Setup
    &{telephonydetails} =  Create Dictionary    sca_enabled=True
    ${scaExtn} =  using ${bossPortal} on ${phone2} I want to enable SCA using ${telephonydetails}
    &{createBCAExtension1} =  Create Dictionary    extension=${scaExtn}    backupExtn=${phone1}    allowBridgeConferencing=true   defaultPrivacySettings=0
    ${bcaExtn}=    using ${bossPortal} I want to modify Bridge Call Appearance extension using ${createBCAExtension1}
    ${scaExtntwo} =  using ${bossPortal} on ${phone5} I want to enable SCA using ${telephonydetails}
    &{createBCAExtension2} =  Create Dictionary    extension=${scaExtntwo}    backupExtn=${phone1}    allowBridgeConferencing=true   defaultPrivacySettings=0
    ${bcaExtntwo}=    using ${bossPortal} I want to modify Bridge Call Appearance extension using ${createBCAExtension2}
    &{BCAdetails_one} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=3    function=Bridge Call Appearance    label=BCA    target_extension=${bcaExtn}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${EMPTY}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=${EMPTY}
    &{BCAdetails_two} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=4    function=Bridge Call Appearance    label=BCAT    target_extension=${bcaExtntwo}    RingDelayBeforeAlert=0      CallStackPosition=2    DialExtension=${EMPTY}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=${EMPTY}
    Given using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails_one}
    Given using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails_two}
    Then I want to press line key ${programKey4} on phone ${phone1}
    Then on ${phone1} enter number ${phone3}
    Then on ${phone1} wait for 4 seconds
    Then answer the call on ${phone3} using ${loudSpeaker}
    Then Verify audio path between ${phone1} and ${phone3}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} enter number ${phone4}
    Then on ${phone2} wait for 4 seconds
    Then answer the call on ${phone4} using ${loudSpeaker}
    Then Verify audio path between ${phone1} and ${phone4}
    Then verify the led state of ${line1} as ${blink} on ${phone2}
    Then on ${phone2} Press ${softKey} ${bottomKey1} for 1 times
    Then verify the led state of ${line1} as ${on} on ${phone2}
    Then on ${phone1} press the softkey ${conference} in AnswerState
    Then I want to press line key ${programKey4} on phone ${phone1}
    Then on ${phone2} wait for 4 seconds
    Then conference call audio verify between ${phone2} ${phone3} and ${phone4}
    Then verify no audio path from ${phone1} to ${phone3}
    Then verify no audio path from ${phone1} to ${phone4}
    And press hardkey as ${goodBye} on ${phone3}
    And press hardkey as ${goodBye} on ${phone4}
    &{telephonydetails} =  Create Dictionary    sca_enabled=False
    And using ${bossPortal} on ${phone2} I want to disable SCA using ${telephonydetails}
    And using ${bossPortal} on ${phone5} I want to disable SCA using ${telephonydetails}
    [Teardown]    Telephony Feature Custom Teardown

127498:Directory blind transfer extension
    [Tags]    Owner:Abhishekkhanchi    Reviewer:    PD  seprateExecution    twelfth
    Given using ${bossPortal} I want to change Delay after collecting digits value to 12000
    Given I want to make a two party call between ${phone2} and ${phone1} using ${loudSpeaker}
    Then on ${phone1} wait for 8 seconds
    Then answer the call on ${phone1} using ${loudSpeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then on ${phone1} press the softkey ${transfer} in AnswerState
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then on ${phone1} ${SemiAttendedTransferVSK} call to ${phone3} using directory
    Then answer the call on ${phone3} using ${loudspeaker}
    Then On ${phone1} verify the softkeys in ${IdleState}
    Then Verify audio path between ${phone3} and ${phone2}
    Then using ${bossPortal} I want to change Delay after collecting digits value to 3000
    Then disconnect the call from ${phone3}

559051:SCA Boss using BCA programmed buttons calls A, Boss Calls B, joins
    [Tags]    Owner:Abhishekkhanchi    Reviewer:    twelfth
    &{telephonydetails} =  Create Dictionary    sca_enabled=True
    ${scaExtn} =  using ${bossPortal} on ${phone1} I want to enable SCA using ${telephonydetails}
    &{createBCAExtension} =  Create Dictionary    extension=${scaExtn}    backupExtn=${phone1}    allowBridgeConferencing=true   defaultPrivacySettings=0
    Given using ${bossPortal} I want to modify Bridge Call Appearance extension using ${createBCAExtension}
    Then I want to press line key ${programKey2} on phone ${phone1}
    Then on ${phone1} enter number ${phone2}
    Then on ${phone1} wait for 4 seconds
    Then Answer the call on ${phone2} using ${OffHook}
    Then Verify audio path between ${phone1} and ${phone2}
    Then I want to press line key ${programKey3} on phone ${phone1}
    Then on ${phone1} enter number ${phone3}
    Then on ${phone1} wait for 4 seconds
    Then Answer the call on ${phone3} using ${OffHook}
    Then Verify audio path between ${phone1} and ${phone3}
    Then on ${phone1} press the softkey ${conference} in AnswerState
    Then on ${phone1} wait for 3 seconds
    Then I want to press line key ${programKey2} on phone ${phone1}
    Then on ${phone1} wait for 8 seconds
    Then conference call audio verify between ${phone1} ${phone2} and ${phone3}
    And press hardkey as ${goodBye} on ${phone2}
    And press hardkey as ${goodBye} on ${phone3}
    &{telephonydetails} =  Create Dictionary    sca_enabled=False
    Then using ${bossPortal} on ${phone1} I want to disable SCA using ${telephonydetails}


561215:User Options, Password Change Checkbox=True
    [Tags]    Owner:Abhishekkhanchi    Reviewer:  notApplicableFor6910    twelfth    notApplicableForMiCloud
    &{telephonydetails} =  Create Dictionary    VM_pwd_change_on_next_login=False
    Given using ${bossPortal} on ${phone1} I want to uncheck voicemail password on next login using ${telephonydetails}
    Then on ${phone1} dial number #
    Then on ${phone1} Wait for 8 seconds
    Then on ${phone1} dial number ${loginVoicemail}
    Then on ${phone1} Wait for 3 seconds
    Then on ${phone1} dial number 7
    Then on ${phone1} Wait for 1 seconds
    Then on ${phone1} dial number 3
    Then on ${phone1} Wait for 1 seconds
    Then on ${phone1} dial number 2
    Then on ${phone1} Wait for 15 seconds
    Then on ${phone1} verify display message ${available}
    Then On ${phone1} Wait for 2 seconds
    Then on ${phone1} dial number #
    Then on ${phone1} Wait for 5 seconds
    Then on ${phone1} enter number ${phone1}
    Then on ${phone1} dial number ${loginVoicemail}
    Then on ${phone1} Wait for 3 seconds
    Then on ${phone1} dial number 7
    Then on ${phone1} Wait for 1 seconds
    Then on ${phone1} dial number 3
    Then on ${phone1} Wait for 1 seconds
    Then on ${phone1} dial number 1
    Then on ${phone1} Wait for 15 seconds
    Then Verify extension ${number} of ${phone1} on ${phone1}
    &{telephonydetails} =  Create Dictionary    VM_pwd_change_on_next_login=True
    Then using ${bossPortal} on ${phone1} I want to check voicemail password on next login using ${telephonydetails}
    Then Press hardkey as ${menu} on ${phone1}
    Then on ${phone1} enter number ${voicemailPassword}
    Then on ${phone1} press ${hardKey} ${Enter} for 1 times
    Then on ${phone1} verify display message ${vmpasschangewindow}
    Then on ${phone1} verify display message ${confirmnvm}
    Then on ${phone1} enter number ${newvmpass}
    Then on ${phone1} press ${hardKey} ${Enter} for 1 times
    Then on ${phone1} enter number ${newvmpass}
     Then on ${phone1} press ${hardKey} ${Enter} for 1 times
    Then on ${phone1} Wait for 10 seconds
    Then on ${phone1} verify display message User Settings
    Then press hardkey as ${goodBye} on ${phone1}
    &{telephonydetails} =  Create Dictionary    VM_pwd_change_on_next_login=True
    Then using ${bossPortal} on ${phone1} I want to uncheck voicemail password on next login using ${telephonydetails}
    Then Press hardkey as ${menu} on ${phone1}
    Then on ${phone1} enter number ${newvmpass}
    Then on ${phone1} press ${hardKey} ${Enter} for 1 times
    Then on ${phone1} verify display message ${vmpasschangewindow}
    Then on ${phone1} verify display message ${confirmnvm}
    Then on ${phone1} enter number ${voicemailPassword}
    Then on ${phone1} press ${hardKey} ${Enter} for 1 times
    Then on ${phone1} enter number ${voicemailPassword}
    Then on ${phone1} press ${hardKey} ${Enter} for 1 times
    Then on ${phone1} Wait for 10 seconds
    &{telephonydetails} =  Create Dictionary    VM_pwd_change_on_next_login=False
    Then using ${bossPortal} on ${phone1} I want to uncheck voicemail password on next login using ${telephonydetails}
    And press hardkey as ${goodBye} on ${phone1}

562816: Change user's Voicemail password
    [Tags]    Owner:Abhishekkhanchi    Reviewer:  notApplicableFor6910    twelfth    notApplicableForMiCloud
    &{telephonydetails} =  Create Dictionary    VM_pwd_change_on_next_login=True
    Then using ${bossPortal} on ${phone1} I want to uncheck voicemail password on next login using ${telephonydetails}
    Then Press hardkey as ${menu} on ${phone1}
    Then on ${phone1} enter number ${voicemailPassword}
    Then on ${phone1} press ${hardKey} ${Enter} for 1 times
    Then on ${phone1} verify display message ${vmpasschangewindow}
    Then on ${phone1} verify display message ${confirmnvm}
    Then on ${phone1} enter number ${newvmpass}
    Then on ${phone1} press ${hardKey} ${Enter} for 1 times
    Then on ${phone1} enter number ${newvmpass}
     Then on ${phone1} press ${hardKey} ${Enter} for 1 times
    Then on ${phone1} Wait for 5 seconds
    Then on ${phone1} verify display message User Settings
    Then press hardkey as ${goodBye} on ${phone1}
    &{telephonydetails} =  Create Dictionary    VM_pwd_change_on_next_login=True
    Then using ${bossPortal} on ${phone1} I want to uncheck voicemail password on next login using ${telephonydetails}
    Then Press hardkey as ${menu} on ${phone1}
    Then on ${phone1} enter number ${newvmpass}
    Then on ${phone1} press ${hardKey} ${Enter} for 1 times
    Then on ${phone1} verify display message ${vmpasschangewindow}
    Then on ${phone1} verify display message ${confirmnvm}
    Then on ${phone1} enter number ${voicemailPass}
    Then on ${phone1} press ${hardKey} ${Enter} for 1 times
    Then on ${phone1} enter number ${voicemailPass}
    Then on ${phone1} press ${hardKey} ${Enter} for 1 times
    Then on ${phone1} Wait for 5 seconds
    &{telephonydetails} =  Create Dictionary    VM_pwd_change_on_next_login=False
    Then using ${bossPortal} on ${phone1} I want to uncheck voicemail password on next login using ${telephonydetails}
    And press hardkey as ${goodBye} on ${phone1}

560153:Un-park call with 2 or more Held Calls on target extension (active call)
   [Tags]    Owner:Abhishekkhanchi    Reviewer:  notApplicableFor6910    twelfth
   Given using ${bossPortal} I program ${unPark} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 2 with ExtensionValue
   Then I want to make a two party call between ${phone3} and ${phone2} using ${loudSpeaker}
   Then answer the call on ${phone2} using ${loudSpeaker}
   Then Verify audio path between ${phone3} and ${phone2}
   Then I want to make a two party call between ${phone4} and ${phone2} using ${loudSpeaker}
   Then I want to press line key ${programKey2} on phone ${phone2}
   Then Verify audio path between ${phone4} and ${phone2}
   Then I want to press line key ${programKey3} on phone ${phone2}
   Then I want to make a two party call between ${phone2} and ${phone5} using ${programKey3}
   Then answer the call on ${phone5} using ${loudSpeaker}
   Then Verify audio path between ${phone2} and ${phone5}
   Then I want to press line key ${programKey3} on phone ${phone1}
   Then On ${phone1} verify display message Select
   Then Verify extension ${number} of ${phone3} on ${phone1}
   Then Verify extension ${number} of ${phone4} on ${phone1}
   Then press hardkey as ${scrollDown} on ${phone1}
   Then on ${phone1} Press ${softKey} ${bottomKey1} for 1 times
   Then Verify audio path between ${phone1} and ${phone3}
   Then I want to verify on ${phone2} negative display message ${phone3}
   Then press hardkey as ${goodBye} on ${phone1}
   Then press hardkey as ${goodBye} on ${phone2}
   Then press hardkey as ${goodBye} on ${phone3}
   And press hardkey as ${goodBye} on ${phone4}
   Then And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 2

561688:DUT prompts user to enter new password for after creating New User
    [Tags]    Owner:Abhishekkhanchi    Reviewer:AvishekRanjan    notApplicableFor6910    thirteenth    notApplicableForMiCloud
    &{telephonydetails} =  Create Dictionary    AllowTelephonyPresence=True
    ${newExtn}=  using ${bossPortal} I want to create user using ${telephonydetails}
    Then on ${phone1} dial number #
    Then on ${phone1} Wait for 5 seconds
    Then on ${phone1} dial number ${loginVoicemail}
    Then on ${phone1} Wait for 3 seconds
    Then on ${phone1} dial number 7
    Then on ${phone1} Wait for 1 seconds
    Then on ${phone1} dial number 3
    Then on ${phone1} Wait for 1 seconds
    Then on ${phone1} dial number 2
    Then on ${phone1} Wait for 5 seconds
    Then on ${phone1} verify display message ${available}
    Then on ${phone1} verify display message ${assign}
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then on ${phone1} verify display message ${assignUser}
    Then on ${phone1} verify display message ${extension}
    Then on ${phone1} verify display message ${password}
    Then on ${phone1} enter number ${newExtn}
    Then on ${phone1} press ${hardKey} ${scrolldown} for 1 times
    Then on ${phone1} enter number ${voicemailPassword}
    Then on ${phone1} press ${hardKey} ${Enter} for 1 times
    Then on ${phone1} verify display message ${vmpasschangewindow}
    Then on ${phone1} verify display message ${confirmnvm}
    Then on ${phone1} enter number ${newvmpass}
    Then on ${phone1} press ${hardKey} ${Enter} for 1 times
    Then on ${phone1} enter number ${newvmpass}
    Then on ${phone1} press ${hardKey} ${Enter} for 1 times
    Then on ${phone1} Wait for 16 seconds
    Then on ${phone1} verify display message ${newExtn}
    Then using ${bossPortal} I want to delete extension ${newExtn}
    Then on ${phone1} Wait for 10 seconds
    Then on ${phone1} verify display message ${available}
    Then on ${phone1} dial number #
    Then on ${phone1} Wait for 5 seconds
    Then on ${phone1} enter number ${phone1}
    Then on ${phone1} dial number ${loginVoicemail}
    Then on ${phone1} Wait for 3 seconds
    Then on ${phone1} dial number 7
    Then on ${phone1} Wait for 1 seconds
    Then on ${phone1} dial number 3
    Then on ${phone1} Wait for 1 seconds
    Then on ${phone1} dial number 1
    Then on ${phone1} Wait for 5 seconds
    Then Verify extension ${number} of ${phone1} on ${phone1}
    Then press hardkey as ${goodBye} on ${phone1}

759632:XMON, CID Only When Ringing - 1 active call on target
   [Tags]    Owner:AbhishekKhanchi    Reviewer:    thirteenth
    &{extensionDetails} =  Create Dictionary  ring_delay=1   show_caller_id=only_when_ringing    no_connected=dial_number    with_connected=dial_number    account_name=Automation    part_name=SC1    button_box=1
    Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 2 with ExtensionValue
    Then verify display message ${displayMessage['monitorExtn']} on PKM for ${phone1}
    Then I want to make a two party call between ${phone3} and ${phone2} using ${offHook}
    Then answer the call on ${phone2} using ${offHook}
    Then verify audio path between ${phone3} and ${phone2}
    Then Verify the PKM led state of ${line2} as ${on} on ${phone1}
    Then On ${phone1} verify the softkeys in ${idle}
    Then I want to press pkm line key ${programKey3} on ${phone1}
    Then I want to press pkm line key ${programKey3} on ${phone1}
    Then verify the led state of ${line2} as ${blink} on ${phone2}
    Then Verify the Caller id on ${phone2} and ${phone1} display
    And disconnect the call from ${phone1}
    And disconnect the call from ${phone3}
    And using ${bossPortal} remove the function key on ${phone1} using ${extensionDetails} and softkey position 2

759638:XMON, CID Only When Ringing - incoming call(s) + active picked-up call
    [Tags]    Owner:Abhishekkhanchi    Reviewer:AvishekRanjan    XMON    thirteenth
    &{extensionDetails} =  Create Dictionary  ring_delay=1   show_caller_id=only_when_ringing    no_connected=dial_number    with_connected=dial_number    account_name=Automation    part_name=SC1    button_box=1
    Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 2 with ExtensionValue
    Then verify display message ${displayMessage['monitorExtn']} on PKM for ${phone1}
    Then I want to make a two party call between ${phone3} and ${phone2} using ${offHook}
    Then I want to press pkm line key ${programKey3} on ${phone1}
    Then I want to press pkm line key ${programKey3} on ${phone1}
    Then verify audio path between ${phone1} and ${phone3}
    Then Verify the PKM led state of ${line3} as ${on} on ${phone1}
    Then Verify the Caller id on ${phone3} and ${phone1} display
    Then On ${phone1} verify ${line1} icon state as ${callAppearanceIdle}
    Then I want to make a two party call between ${phone4} and ${phone2} using ${offHook}
    Then Verify extension ${number} of ${phone4} on ${phone2}
    Then Verify the PKM led state of ${line3} as ${blink} on ${phone1}
    Then I want to press pkm line key ${programKey3} on ${phone1}
    Then Verify extension ${number} of ${phone4} on ${phone1}
    Then On ${phone1} verify the softkeys in ${xmon}
    Then press hardkey as ScrollDown on ${phone1}
    Then i want to verify on ${phone1} negative display message ${phone3}
    And disconnect the call from ${phone1}
    And disconnect the call from ${phone3}
    And disconnect the call from ${phone4}
    And using ${bossPortal} remove the function key on ${phone1} using ${extensionDetails} and softkey position 2

753809:BCA1 on BB calls A, BCA2 on BB calls B, uses conf to join to BCA1
    [Tags]    Owner:Abhishekkhanchi    Reviewer:    thirteenth
    [Setup]    BCA Custom Setup
    &{createBCAExtension1} =  Create Dictionary    name=abhishekkhanchi1   backupExtn=${phone3}    switch=2    callStackDepth=2    forwardAfter=2    callStackFull=${EMPTY}   noAnswer=${EMPTY}    outboundCallerID=${EMPTY}    allowBridgeConferencing=true   defaultPrivacySettings=0
    &{createBCAExtension2} =  Create Dictionary    name=abhishekkhanchi2   backupExtn=${phone3}    switch=2    callStackDepth=2    forwardAfter=2    callStackFull=${EMPTY}   noAnswer=${EMPTY}    outboundCallerID=${EMPTY}    allowBridgeConferencing=true   defaultPrivacySettings=0
    ${bcaExtn1}=    using ${bossPortal} I want to create Bridge Call Appearance extension using ${createBCAExtension1}
    ${bcaExtn2}=    using ${bossPortal} I want to create Bridge Call Appearance extension using ${createBCAExtension2}
    &{BCAdetails1} =  Create Dictionary    user_extension=${phone1}    button_box=1    soft_key=3    function=Bridge Call Appearance    label=BCA1    target_extension=${bcaExtn1}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${phone4}     show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=${EMPTY}
    &{BCAdetails2} =  Create Dictionary    user_extension=${phone1}    button_box=1    soft_key=4    function=Bridge Call Appearance    label=BCA2    target_extension=${bcaExtn2}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${phone4}     show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=${EMPTY}
    Given using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails1}
    Then using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails2}
    Then verify display message BCA1 on PKM for ${phone1}
    Then verify display message BCA2 on PKM for ${phone1}
    Then I want to press PKM line key ${programKey3} on ${phone1}
    Then on ${phone1} enter number ${phone2}
    Then on ${phone1} wait for 4 seconds
    Then Answer the call on ${phone2} using ${loudspeaker}
    Then I want to press PKM line key ${programKey4} on ${phone1}
    Then on ${phone1} enter number ${phone3}
    Then on ${phone1} wait for 4 seconds
    Then Answer the call on ${phone3} using ${loudspeaker}
    Then on ${phone1} press ${softkey} ${bottomkey2} for 1 times
    Then I want to press PKM line key ${programKey3} on ${phone1}
    Then on ${phone1} wait for 4 seconds
    Then Verify the PKM led state of ${line3} as ${on} on ${phone1}
    Then Verify the PKM led state of ${line4} as ${off} on ${phone1}
    Then Disconnect the call from ${phone2}
    Then Disconnect the call from ${phone3}
    And using ${bossPortal} I want to delete Bridge Call Appearance extension using ${bcaExtn1}
    And using ${bossPortal} I want to delete Bridge Call Appearance extension using ${bcaExtn2}
    [Teardown]     BCA Custom Teardown

759549:Implicit monitoring (Pickup)
  [Tags]    Owner:Abhishekkhanchi    Reviewer:AvishekRanjan    XMON    thirteenth
  &{extensionDetails} =  Create Dictionary  button_box=1
  Given using ${bossPortal} I program ${pickup} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 2 with ExtensionValue
  Then verify display message ${pickup} on PKM for ${phone1}
  Then On ${phone2} verify ${line1} icon state as ${callAppearanceIdle}
  Then Verify the PKM led state of ${line3} as ${off} on ${phone1}
  Then I want to make a two party call between ${phone3} and ${phone2} using ${offHook}
  Then Verify the PKM led state of ${line3} as ${blink} on ${phone1}
  Then On PKM verify ${line3} icon state as idle for ${phone1}
  Then Answer the call on ${phone2} using ${offHook}
  Then verify audio path between ${phone3} and ${phone2}
  Then Verify the PKM led state of ${line3} as ${on} on ${phone1}
  Then Verify the PKM led color of ${line3} as Red on ${phone1}
  Then On PKM verify ${line3} icon state as active for ${phone1}
  Then disconnect the call from ${phone3}
  Then on ${phone2} navigate to ${availability} settings
  Then Modify call handler mode on ${phone2} to ${always} in ${doNotDisturb}
  Then Verify the PKM led state of ${line3} as ${on} on ${phone1}
  Then Verify the PKM led color of ${line3} as Red on ${phone1}
  Then On PKM verify ${line3} icon state as active for ${phone1}
  And Change the phone state to default state on ${phone2}
  And using ${bossPortal} remove the function key on ${phone1} using ${extensionDetails} and softkey position 2
  [Teardown]    RUN KEYWORDS    Generic Test Teardown    Default Availability State

752466:Barge In
    [Tags]    Owner:Abhishekkhanchi    Reviewer:    MOh    thirteenth    notApplicableForMiCloud
    &{MOHFeatures}    CREATE DICTIONARY    option=1    fileName=MOH_50
    Given using ${bossPortal} I want to enable MOH features using ${MOHFeatures}
    Given using ${bossPortal} I want to modify usergroups MOH for ${executives} with filename MOH_200
    Then I want to make a two party call between ${phone1} and ${phone2} using ${offHook}
    Then Answer the call on ${phone2} using ${offHook}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Put the linekey ${line1} of ${phone1} on ${hold}
    Then verify MOH audio on ${phone2} for 200 frequency
    Then Put the linekey ${line1} of ${phone1} on ${unhold}
    Then I WANT TO USE FAC ${bargeInFAC} ON ${PHONE3} TO ${PHONE2}
    Then On ${phone3} verify display message ${conference}
    Then conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then Put the linekey ${line1} of ${phone2} on ${hold}
    Then Put the linekey ${line1} of ${phone2} on ${unhold}
    Then Verify no MOH audio on ${phone1}
    Then Verify no MOH audio on ${phone2}
    Then Verify no MOH audio on ${phone3}
    Then Disconnect the call from ${phone2}
    Then Disconnect the call from ${phone3}
    &{MOHFeatures}    CREATE DICTIONARY    option=0    fileName=MOH_50
    And using ${bossPortal} I want to disable MOH features using ${MOHFeatures}


753764:Boss Calls UCB Gets Incoming call joins Boss hangs up No Dropped conf Prompt
    [Tags]    Owner:Abhishekkhanchi    Reviewer:    thirteenth
    [Setup]    Telephony Feature Custom Setup
    &{telephonydetails} =  Create Dictionary    sca_enabled=True
    ${scaExtn} =  using ${bossPortal} on ${phone1} I want to enable SCA using ${telephonydetails}
    Given on ${phone1} press the key ${conference} in state ${idle}
    Then on ${phone1} enter number ${accessCode}
    Then on ${phone2} enter number ${scaExtn}
    Then on ${phone1} wait for 4 seconds
    Then Answer the call on ${phone1} using ${programKey2}
    Then Verify audio path between ${phone1} and ${phone2}
    Then on ${phone1} press the softkey ${conference} in AnswerState
    Then on ${phone1} wait for 5 seconds
    Then I want to press line key ${programKey1} on phone ${phone1}
    Then On ${phone1} verify display message ${conferenceExt}
    Then On ${phone2} verify display message ${conferenceExt}
    And press hardkey as ${goodBye} on ${phone1}
    Then On ${phone2} verify display message ${conferenceExt}
    And press hardkey as ${goodBye} on ${phone2}
    [Teardown]    Telephony Feature Custom Teardown

753691:Admin1 BCA calls A, admin2 picks up and BCA confs in, admin1 hangs up, no prompt
    [Tags]    Owner:Abhishekkhanchi    Reviewer:AvishekRanjan    thirteenth
    [Setup]    BCA Custom Setup
    &{createBCAExtension} =  Create Dictionary    name=BCA_AK   backupExtn=${phone3}    switch=2    callStackDepth=1    forwardAfter=2    callStackFull=${EMPTY}   noAnswer=${EMPTY}    outboundCallerID=${EMPTY}    allowBridgeConferencing=true   defaultPrivacySettings=0
    ${bcaExtn}=    using ${bossPortal} I want to create Bridge Call Appearance extension using ${createBCAExtension}
    &{BCAdetailsone} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=4    function=Bridge Call Appearance    label=${bca}    target_extension=${bcaExtn}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${EMPTY}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=${EMPTY}
    &{BCAdetailstwo} =  Create Dictionary    user_extension=${phone2}    button_box=0    soft_key=4    function=Bridge Call Appearance    label=${bca}    target_extension=${bcaExtn}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${EMPTY}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=${EMPTY}
    Given using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetailsone}
    Given using ${bossPortal} I want to create bca on ${phone2} using ${BCAdetailstwo}
    Then On ${phone1} verify display message ${bca}
    Then On ${phone2} verify display message ${bca}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} enter number ${phone3}
    Then On ${phone3} Wait for 3 seconds
    Then answer the call on ${phone3} using ${loudSpeaker}
    Then Verify audio path between ${phone1} and ${phone3}
    Then I want to press line key ${programKey5} on phone ${phone2}
    Then on ${phone1} wait for 4 seconds
    Then Conference call audio verify between ${phone1} ${phone2} and ${phone3}
    And Disconnect the call from ${phone3}
    And Disconnect the call from ${phone2}
    And Disconnect the call from ${phone1}
    [Teardown]    BCA Custom Teardown


753939:Multiple Hotline buttons
   [Tags]    Owner:Abhishekkhanchi    Reviewer    hotline_multiple    thirteenth
    &{hotlineA}    CREATE DICTIONARY    ConnectedCallFunctionID=dial number    label=A    account_name=Automation    part_name=SC1    button_box=0
    &{hotlineB}    CREATE DICTIONARY    ConnectedCallFunctionID=dial number    label=B    account_name=Automation    part_name=SC1    button_box=0
    &{hotlineC}    CREATE DICTIONARY    ConnectedCallFunctionID=dial number    label=C    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${hotline} on ${phone2} using ${hotlineB} and extension of ${phone1} and softkey position 2 with extensionValue
    Then using ${bossPortal} I program ${hotline} on ${phone2} using ${hotlineC} and extension of ${phone3} and softkey position 3 with extensionValue
    Then using ${bossPortal} I program ${hotline} on ${phone2} using ${hotlineB} and extension of ${phone1} and softkey position 4 with extensionValue
    Then using ${bossPortal} I program ${hotline} on ${phone1} using ${hotlineA} and extension of ${phone2} and softkey position 2 with extensionValue
    Then using ${bossPortal} I program ${hotline} on ${phone1} using ${hotlineC} and extension of ${phone3} and softkey position 3 with extensionValue
    Then using ${bossPortal} I program ${hotline} on ${phone1} using ${hotlineA} and extension of ${phone2} and softkey position 4 with extensionValue
    Then using ${bossPortal} I program ${hotline} on ${phone1} using ${hotlineA} and extension of ${phone2} and softkey position 5 with extensionValue
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then On ${phone1} Wait for 2 seconds
    Then verify the led state of ${line3} as ${blink} on ${phone2}
    Then answer the call on ${phone2} using ${programKey3}
    Then I want to press line key ${programKey6} on phone ${phone1}
    Then On ${phone1} Wait for 2 seconds
    Then verify the led state of ${line5} as ${blink} on ${phone2}
    Then answer the call on ${phone2} using ${programKey5}
    Then I want to press line key ${programKey3} on phone ${phone1}
    Then On ${phone1} Wait for 2 seconds
    Then verify the led state of ${line1} as ${blink} on ${phone2}
    Then verify the led state of ${line4} as ${off} on ${phone2}
    Then Disconnect the call from ${phone2}
    Then Disconnect the call from ${phone2}
    Then press hardkey as ${holdState} on ${phone2}
    Then Disconnect the call from ${phone2}
    Then I want to press line key ${programKey3} on phone ${phone1}
    Then On ${phone1} Wait for 2 seconds
    Then verify the led state of ${line3} as ${blink} on ${phone2}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then On ${phone1} Wait for 2 seconds
    Then verify the led state of ${line5} as ${blink} on ${phone2}
    Then answer the call on ${phone2} using ${programKey5}
    Then I want to press line key ${programKey6} on phone ${phone1}
    Then On ${phone1} Wait for 2 seconds
    Then verify the led state of ${line1} as ${blink} on ${phone2}
    Then verify the led state of ${line4} as ${off} on ${phone2}
    Then Disconnect the call from ${phone2}
    Then Disconnect the call from ${phone2}
    Then press hardkey as ${holdState} on ${phone2}
    Then Disconnect the call from ${phone2}


753690:Admin1 BCA calls A, admin2 is added to conference by blind conf own ext, admin1 hangs up, sees prompt
    [Tags]    Owner:Abhishekkhanchi    Reviewer:AvishekRanjan    thirteenth
    [Setup]    BCA Custom Setup
    &{createBCAExtensionone} =  Create Dictionary    name=BCA_AKONE   backupExtn=${phone3}    switch=2    callStackDepth=1    forwardAfter=2    callStackFull=${EMPTY}   noAnswer=${EMPTY}    outboundCallerID=${EMPTY}
    ${bcaExtnone}=    using ${bossPortal} I want to create Bridge Call Appearance extension using ${createBCAExtensionone}
    &{createBCAExtensiontwo} =  Create Dictionary    name=BCA_AKTWO   backupExtn=${phone3}    switch=2    callStackDepth=1    forwardAfter=2    callStackFull=${EMPTY}   noAnswer=${EMPTY}    outboundCallerID=${EMPTY}
    ${bcaExtntwo}=    using ${bossPortal} I want to create Bridge Call Appearance extension using ${createBCAExtensiontwo}
    &{BCAdetailsone} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=4    function=Bridge Call Appearance    label=${bca}    target_extension=${bcaExtnone}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${EMPTY}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=${EMPTY}
    &{BCAdetailstwo} =  Create Dictionary    user_extension=${phone2}    button_box=0    soft_key=4    function=Bridge Call Appearance    label=${bca}    target_extension=${bcaExtntwo}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${EMPTY}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=${EMPTY}
    Given using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetailsone}
    Given using ${bossPortal} I want to create bca on ${phone2} using ${BCAdetailstwo}
    Then On ${phone1} verify display message ${bca}
    Then On ${phone2} verify display message ${bca}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} enter number ${phone3}
    Then On ${phone3} Wait for 3 seconds
    Then answer the call on ${phone3} using ${loudSpeaker}
    Then Verify audio path between ${phone1} and ${phone3}
    Then on ${phone1} press the softkey ${conference} in AnswerState
    Then on ${phone1} enter number ${bcaExtntwo}
    Then on ${phone1} press the softkey ${conference} in AnswerState
    Then on ${phone1} wait for 4 seconds
    Then answer the call on ${phone2} using ${programKey5}
    Then Conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then Disconnect the call from ${phone1}
    Then On ${phone1} verify the softkeys in ${idleState}
    Then verify the led state of ${line5} as ${on} on ${phone2}
    Then Verify audio path between ${phone2} and ${phone3}
    And Disconnect the call from ${phone3}
    And Disconnect the call from ${phone2}
    [Teardown]    BCA Custom Teardown

754335:Initiate "Intercom" for already configured extension.
    [Tags]    Owner:Abhishekkhanchi    Reviewer:AvishekRanjan    thirteenth
    Given using ${bossPortal} I program ${intercom} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with ExtensionValue
    Then On ${phone1} verify display message ${intercom}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then verify the led state of ${line5} as ${on} on ${phone1}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then Verify the led state of mute as ${off} on ${phone2}
    Then Verify audio path between ${phone2} and ${phone1}
    And Disconnect the call from ${phone2}

759612:Initiate "Intercom" with Speed Dial
    [Tags]    Owner:Abhishekkhanchi    Reviewer:AvishekRanjan    thirteenth
    Given using ${bossPortal} I program ${intercom} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 3 with noExtensionValue
    Then using ${bossPortal} I program ${dialNumber} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['dialNumber']}
    Then On ${phone1} verify display message ${intercom}
    Then I want to press line key ${programKey4} on phone ${phone1}
    Then On ${phone1} verify display message ${intercom}
    Then On ${phone1} verify display message >
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then verify the led state of ${line5} as ${on} on ${phone1}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then Verify the led state of mute as ${off} on ${phone2}
    Then Verify audio path between ${phone2} and ${phone1}
    And Disconnect the call from ${phone2}

752144:Make me Conference call when insufficient switch ports available
    [Tags]    Owner:Abhishekkhanchi    Reviewer:    thirteenth
    &{COSDetails} =  Create Dictionary    Name=${fullyFeatured}    MaxPartiesMakeMeConference=5
    &{pmargst} =  Create Dictionary  softKey=${conference}
    &{pressSoftkeyInConferenceCall} =  Create Dictionary  action_name=pressSoftkeyInConferenceCall   pmargs=&{pmargst}
    Given using ${bossPortal} I want to change telephony features values using ${COSDetails}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${line1}
    Then answer the call on ${phone1} using ${loudSpeaker}
    Then I want to make a conference call between ${phone1},${phone2} and ${phone3} using ${directConference}
    Then Conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then Add the ${phone4} in 3 parties conference call on ${phone1}
    Then Verify audio path between ${phone4} and ${phone2}
    Then on ${phone2} press the softkey ${conference} in ConferenceCallState
    Then verify the led state of ${line1} as ${blink} on ${phone2}
    Then on ${phone2} enter number ${phone5}
    Then on ${phone1} wait for 4 seconds
    Then answer the call on ${phone5} using ${loudSpeaker}
    Then Verify audio path between ${phone5} and ${phone2}
    Then On ${phone2} verify display message Conference
    Then On ${phone2} verify display message Drop
    Then I want to verify on ${phone2} negative display message Show
    Then on ${phone1} verify display message Conferenced 3 calls
    Then on ${phone3} verify display message Conferenced 3 calls
    Then on ${phone4} verify display message Conferenced 3 calls
    Then on ${phone2} press the softkey ${conference} in ConferenceCallState
    Then on ${phone1} verify display message Conferenced 4 calls
    Then on ${phone2} verify display message Conferenced 4 calls
    Then on ${phone3} verify display message Conferenced 4 calls
    Then on ${phone4} verify display message Conferenced 4 calls
    Then on ${phone2} due to action ${pressSoftkeyInConferenceCall} popup raised verify message Conference not permitted on this with wait of 0
    Then Verify audio path between ${phone2} and ${phone5}
    Then disconnect the call from ${phone1}
    Then disconnect the call from ${phone3}
    Then disconnect the call from ${phone4}
    Then disconnect the call from ${phone5}
    [Teardown]    CoS Features Custom Teardown

754724:Pickup call from user that is not in the Pickup Group
    [Tags]    Owner:Abhishekkhanchi    Reviewer:    thirteenth
    [Setup]     Paging Group Custom Setup
    @{members}   Create List    ${phone4}    ${phone5}
    &{pickupGroupDetails}    CREATE DICTIONARY    user_extension=${phone1}    PickupGroupName=pickAk    pickupListName=mylist    switch=2    GroupMembers=${members}
    ${pickupExtension}=     using ${bossPortal} I want to create pickup groups using ${pickupGroupDetails}
    Given I want to make a two party call between ${phone2} and ${phone3} using ${line1}
    Then Verify ringing state on ${phone2} and ${phone3}
    Then I want to use fac Pickup on ${phone1} to ${pickupExtension}
    Then On ${phone1} verify display message No calls to pickup
    Then disconnect the call from ${phone1}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}
    And Using ${bossPortal} I want to delete pickup groups ${pickupExtension} and pickup extension list ${pickupGroupDetails['pickupListName']}
    [Teardown]    Pickup Group Custom Teardown

756244:Assigned phone and usermailboxPresent value to OFF
    [Tags]    Owner:Abhishekkhanchi    Reviewer:    thirteenth
    [Setup]    TELEPHONY FEATURE CUSTOM SETUP
    &{telephonydetails} =  Create Dictionary    extension=${phone1}    LicenseTypeID=2
    Given using ${bossPortal} on ${phone1} I want to change usermailboxsettings using ${telephonydetails}
    Then press hardkey as ${voicemail} on ${phone1}
    Then i want to verify on ${phone1} negative display message ${voiceMailLoginScreenDisplay}
    Then on ${phone1} enter number ${phone2}
    Then on ${phone1} Wait for 3 seconds
    Then on ${phone1} enter number ${loginVoicemail}
    Then on ${phone1} Wait for 3 seconds
    Then on ${phone1} dial number 7
    Then on ${phone1} Wait for 1 seconds
    Then on ${phone1} dial number 3
    Then on ${phone1} Wait for 1 seconds
    Then on ${phone1} dial number 2
    Then on ${phone1} Wait for 5 seconds
    Then on ${phone2} verify display message ${available}
    Then on ${phone2} dial number #
    Then on ${phone2} Wait for 5 seconds
    Then on ${phone2} enter number ${phone2}
    Then on ${phone2} dial number ${loginVoicemail}
    Then on ${phone2} Wait for 3 seconds
    Then on ${phone2} dial number 7
    Then on ${phone2} Wait for 1 seconds
    Then on ${phone2} dial number 3
    Then on ${phone2} Wait for 1 seconds
    Then on ${phone2} dial number 1
    Then on ${phone2} Wait for 5 seconds
    Then Verify extension ${number} of ${phone2} on ${phone2}
    Then press hardkey as ${goodBye} on ${phone1}
    Then on ${phone1} dial number #
    Then i want to verify on ${phone1} negative display message ${voiceMailLoginScreenDisplay}
    Then on ${phone1} enter number ${phone2}
    Then on ${phone1} Wait for 3 seconds
    Then on ${phone1} dial number 7
    Then on ${phone1} Wait for 1 seconds
    Then on ${phone1} dial number 3
    Then on ${phone1} Wait for 1 seconds
    Then on ${phone1} dial number 2
    Then on ${phone1} Wait for 5 seconds
    Then on ${phone1} verify display message ${available}
    Then on ${phone2} dial number #
    Then on ${phone2} Wait for 5 seconds
    Then on ${phone2} enter number ${phone2}
    Then on ${phone2} dial number ${loginVoicemail}
    Then on ${phone2} Wait for 3 seconds
    Then on ${phone2} dial number 7
    Then on ${phone2} Wait for 1 seconds
    Then on ${phone2} dial number 3
    Then on ${phone2} Wait for 1 seconds
    Then on ${phone2} dial number 1
    Then on ${phone2} Wait for 15 seconds
    Then Verify extension ${number} of ${phone2} on ${phone2}
    Then press hardkey as ${goodBye} on ${phone1}
    Then on ${phone1} dial number #
    Then i want to verify on ${phone1} negative display message ${voiceMailLoginScreenDisplay}
    Then on ${phone1} verify display message ${voiceMailLogin}
    Then on ${phone1} enter number ${phone2}
    Then on ${phone1} Wait for 3 seconds
    Then on ${phone1} dial number 7
    Then on ${phone1} Wait for 1 seconds
    Then on ${phone1} dial number 3
    Then on ${phone1} Wait for 1 seconds
    Then on ${phone1} dial number 2
    Then on ${phone1} Wait for 5 seconds
    Then on ${phone1} verify display message ${available}
    Then on ${phone2} dial number #
    Then on ${phone2} Wait for 5 seconds
    Then on ${phone2} enter number ${phone2}
    Then on ${phone2} dial number ${loginVoicemail}
    Then on ${phone2} Wait for 3 seconds
    Then on ${phone2} dial number 7
    Then on ${phone2} Wait for 1 seconds
    Then on ${phone2} dial number 3
    Then on ${phone2} Wait for 1 seconds
    Then on ${phone2} dial number 1
    Then on ${phone2} Wait for 15 seconds
    Then Verify extension ${number} of ${phone2} on ${phone2}
    Then press hardkey as ${goodBye} on ${phone1}
    Then on ${phone1} dial number #
    Then press hardkey as ${goodBye} on ${phone1}
    &{telephonydetails} =  Create Dictionary    extension=${phone1}    LicenseTypeID=1
    And using ${bossPortal} on ${phone1} I want to change usermailboxsettings using ${telephonydetails}
    [Teardown]    Telephony Feature Custom Teardown

753713:A calls boss, B Calls boss, admin answers both calls and joins
    [Tags]    Owner:Abhishekkhanchi    Reviewer:    thirteenth
    [Setup]    BCA Custom Setup
    &{telephonydetails} =  Create Dictionary    sca_enabled=True
    ${scaExtn} =  using ${bossPortal} on ${phone2} I want to enable SCA using ${telephonydetails}
    &{createBCAExtension} =  Create Dictionary    extension=${scaExtn}    backupExtn=${phone4}    allowBridgeConferencing=true   defaultPrivacySettings=0
    ${bcaExtn}=    using ${bossPortal} I want to modify Bridge Call Appearance extension using ${createBCAExtension}
    &{BCAdetails1} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=3    function=Bridge Call Appearance    label=BCA1    target_extension=${bcaExtn}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${EMPTY}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=${EMPTY}
    &{BCAdetails2} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=4    function=Bridge Call Appearance   label=BCA2    target_extension=${bcaExtn}    RingDelayBeforeAlert=0      CallStackPosition=2    DialExtension=${EMPTY}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=${EMPTY}
    &{telephonydetails} =  Create Dictionary    extension=${phone2}    Label=call_move    NumberOfRings=3    PhoneNumber=${phone5}    Activation=1
    Given using ${bossPortal} on ${phone2} I want to enable simulring using ${telephonydetails}
    Then using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails1}
    Then using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails2}
    Then on ${phone1} verify display message BCA1
    Then on ${phone2} verify display message BCA2
    Then on ${phone3} dial number ${scaExtn}
    Then on ${phone1} wait for 4 seconds
    Then i want to press line key ${programkey4} on phone ${phone1}
    Then verify the led state of ${programkey4} as ${on} on ${phone1}
    Then verify audio path between ${phone3} and ${phone1}
    Then on ${phone4} dial number ${scaExtn}
    Then on ${phone1} wait for 4 seconds
    Then i want to press line key ${programkey5} on phone ${phone1}
    Then verify the led state of ${programkey5} as ${on} on ${phone1}
    Then verify audio path between ${phone4} and ${phone1}
    Then on ${phone1} press the softkey ${conference} in ConferenceCallState
    Then i want to press line key ${programkey4} on phone ${phone1}
    Then on ${phone1} wait for 4 seconds
    Then On ${phone1} verify display message Conference
    Then On ${phone3} verify display message Conference
    Then On ${phone4} verify display message Conference
    Then Conference call audio verify between ${phone1} ${phone3} and ${phone4}
    [Teardown]    bca custom teardown


753768:Boss tries to join a meetme and a normal conference
    [Tags]    Owner:Abhishekkhanchi    Reviewer:    thirteenth
    [Setup]    BCA Custom Setup
    &{telephonydetails} =  Create Dictionary    sca_enabled=True
    ${scaExtn} =  using ${bossPortal} on ${phone1} I want to enable SCA using ${telephonydetails}
    &{createBCAExtension} =  Create Dictionary    extension=${scaExtn}    backupExtn=${phone4}    allowBridgeConferencing=true   defaultPrivacySettings=0
    &{pmargst} =  Create Dictionary  softKey=${conference}
    &{pressSoftkeyInConferenceCall} =  Create Dictionary  action_name=pressSoftkeyInConferenceCall   pmargs=&{pmargst}
    Given using ${bossPortal} I want to modify Bridge Call Appearance extension using ${createBCAExtension}
    Then on ${phone1} press the key ${conference} in state ${idle}
    Then on ${phone1} enter number ${accessCode}
    Then on ${phone2} press the key ${conference} in state ${idle}
    Then on ${phone2} enter number ${accessCode}
    Then on ${phone3} press the key ${conference} in state ${idle}
    Then on ${phone3} enter number ${accessCode}
    Then on ${phone4} press the key ${conference} in state ${idle}
    Then on ${phone4} enter number ${accessCode}
    Then on ${phone5} press the key ${conference} in state ${idle}
    Then on ${phone5} enter number ${accessCode}
    Then Five party Conference call audio verification between ${phone1} ${phone2} ${phone3} ${phone4} and ${phone5}
    Then I want to press line key ${programKey2} on phone ${phone1}
    Then i want to make a two party call between ${phone1} and ${phone6} using ${offhook}
    Then answer the call on ${phone6} using ${offhook}
    Then on ${phone1} press the softkey ${conference} in AnswerState
    Then on ${phone1} enter number ${phone7}
    Then on ${phone1} wait for 4 seconds
    Then Answer the call on ${phone7} using ${offhook}
    Then on ${phone1} press the softkey ${conference} in AnswerState
    Then on ${phone1} enter number ${phone8}
    Then on ${phone1} wait for 4 seconds
    Then Answer the call on ${phone8} using ${offhook}
    Then on ${phone1} press the softkey ${conference} in AnswerState
    Then four party conference call audio verification between ${phone1} ${phone6} ${phone7} and ${phone8}
    Then on ${phone1} press the softkey ${conference} in AnswerState
    Then I want to press line key ${programKey2} on phone ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then verify the led state of ${line2} as ${blink} on ${phone1}
    Then On ${phone1} verify display message >

    Then on ${phone1} press the softkey ${conference} in AnswerState
    Then I want to press line key ${programKey1} on phone ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then verify the led state of ${line2} as ${blink} on ${phone1}
    Then On ${phone1} verify display message >
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}
    Then disconnect the call from ${phone4}
    Then disconnect the call from ${phone5}
    Then disconnect the call from ${phone6}
    Then disconnect the call from ${phone7}
    Then disconnect the call from ${phone7}
    [Teardown]    bca custom teardown

754723:phone presses Pickup Group prog button
    [Tags]    Owner:Abhishekkhanchi    Reviewer:    thirteenth
    [Setup]     Paging Group Custom Setup
    @{members}   Create List    ${phone1}    ${phone2}    ${phone3}
    &{pickupGroupDetails}    CREATE DICTIONARY    user_extension=${phone1}    PickupGroupName=pickAk    pickupListName=mylist    switch=2    GroupMembers=${members}
    ${pickupExtension}=     using ${bossPortal} I want to create pickup groups using ${pickupGroupDetails}
    Given using ${bossPortal} I program ${groupPickup} on ${phone1} using ${bossDetails} and extension of ${pickupExtension} and softkey position 4 with ExtensionValue
    Then I want to make a two party call between ${phone2} and ${phone3} using ${line1}
    Then Verify ringing state on ${phone2} and ${phone3}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then verify audio path between ${phone1} and ${phone2}
    Then Verify the Caller id on ${phone1} and ${phone2} display
    Then disconnect the call from ${phone1}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}
    And Using ${bossPortal} I want to delete pickup groups ${pickupExtension} and pickup extension list ${pickupGroupDetails['pickupListName']}
    [Teardown]    Pickup Group Custom Teardown

147127: Implicit monitoring (PickupUnpark)
    [Tags]    Owner:AbhishekPathak    Reviewer    target_extension_pickup_unpark    thirteenth
    Given using ${bossPortal} I program ${PickupUnpark} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with ExtensionValue
    Then on ${phone1} wait for 2 seconds
    Then on ${phone1} verify display message ${pickAndUnpar}
    Then Verify the led state of Line5 as ${off} on ${phone1}
    Then I want to make a two party call between ${phone3} and ${phone2} using ${loudspeaker}
    Then Verify the led state of Line5 as ${blink} on ${phone1}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} wait for 2 seconds
    Then Verify the led state of Line1 as ${on} on ${phone1}
    Then Verify the led state of Line5 as ${off} on ${phone1}
    Then Verify audio path between ${phone1} and ${phone3}
    Then disconnect the call from ${phone3}

147151: Unpark 1 or more held calls on XMON target phone
    [Tags]    Owner:AbhishekPathak    Reviewer:Aman    unpark_held_xmontarget    thirteenth
    &{extensionDetails} =    Create Dictionary    ring_delay=dont_ring    show_caller_id=never    no_connected=dial_number    with_connected=dial_number    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 4 with ExtensionValue
    Then on ${phone1} wait for 2 seconds
    Then on ${phone1} verify display message ${displayMessage['monitorExtn']}
    Then I want to make a two party call between ${phone3} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then Verify audio path between ${phone3} and ${phone2}
    Then press hardkey as ${holdState} on ${phone2}
    Then verify the led state of ${line1} as ${blink} on ${phone2}
    Then I want to make a two party call between ${phone4} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${line2}
    Then Verify audio path between ${phone4} and ${phone2}
    Then press hardkey as ${holdState} on ${phone2}
    Then verify the led state of ${line2} as ${blink} on ${phone2}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} wait for 2 seconds
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then verify the led state of ${line1} as ${off} on ${phone2}
    Then Verify audio path between ${phone1} and ${phone3}
    Then verify the led state of ${line2} as ${blink} on ${phone2}
    Then disconnect the call from ${phone3}
    Then disconnect the call from ${phone4}

147178: monitor extension and Park call ONLY WHEN RINGING
    [Tags]    Owner:AbhishekPathak    Reviewer:Aman    monitor_extension_callpark_ringingstate    fourteenth
    &{extensionDetails} =    Create Dictionary    ring_delay=dont_ring    show_caller_id=only_when_ringing    no_connected=dial_number    with_connected=dial_number    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then on ${phone1} wait for 2 seconds
    Then on ${phone1} verify display message ${displayMessage['monitorExtn']}
    Then I want to make a two party call between ${phone3} and ${phone2} using ${loudspeaker}
    Then verify the led state of ${line5} as ${blink} on ${phone1}
    Then Verify ringing state on ${phone3} and ${phone2}
    Then on ${phone2} wait for 2 seconds
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then Verify audio path between ${phone3} and ${phone2}
    Then verify the led state of ${line5} as ${on} on ${phone1}
    Then I want to Park the call from ${phone2} on ${phone4} using ${default} and ${Park}
    Then verify the led state of ${line5} as ${off} on ${phone1}
    Then disconnect the call from ${phone3}

146275: barge in button with extension target -onhook
    [Tags]    Owner:AbhishekPathak   Reviewer:Ram    bargein_onhook    fourteenth
    Given using ${bossPortal} I program ${bargeIn} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with ExtensionValue
    Then on ${phone1} wait for 2 seconds
    Then on ${phone1} verify display message ${bargeIn}
    Then I want to make a two party call between ${phone2} and ${phone3} using ${loudspeaker}
    Then Answer the call on ${phone3} using ${loudSpeaker}
    Then Verify audio path between ${phone2} and ${phone3}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}



146276: barge in button with no extension target -offhook
    [Tags]    Owner:AbhishekPathak    Reviewer:Ram    bargein_offhook    fourteenth
    Given using ${bossPortal} I program ${bargeIn} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with noExtensionValue
    Then on ${phone1} wait for 2 seconds
    Then on ${phone1} verify display message ${bargeIn}
    Then I want to make a two party call between ${phone3} and ${phone2} using ${loudspeaker}
    Then Answer the call on ${phone2} using ${loudSpeaker}
    Then Verify audio path between ${phone2} and ${phone3}
    Then Press hookMode ${offHook} on phone ${phone1}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} enter number ${phone2}
    Then on ${phone1} verify display message ${bargeIn}
    Then conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then disconnect the call from ${phone1}
    Then disconnect the call from ${phone3}

146278: finish barge in directory SELECT
    [Tags]    Owner:AbhishekPathak    Reviewer:Ram    bargein_directory_select    fourteenth
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then disconnect the call from ${phone1}
    Then using ${bossPortal} I program ${bargeIn} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with noExtensionValue
    Then on ${phone1} wait for 2 seconds
    Then on ${phone1} verify display message ${bargeIn}
    Then I want to make a two party call between ${phone2} and ${phone3} using ${loudspeaker}
    Then Answer the call on ${phone3} using ${loudSpeaker}
    Then Verify audio path between ${phone2} and ${phone3}
    Then on ${phone3} wait for 2 seconds
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} verify display message ${bargeIn}
    Then I want to bargein ${phone1} into ${phone2} using ${callHistory} and ${Select}
    Then on ${phone1} wait for 5 seconds
    Then conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then disconnect the call from ${phone1}
    Then disconnect the call from ${phone3}

147126: Implicit monitoring (Pickup)
    [Tags]    Owner:AbhishekPathak    Reviewer:    target_extension_pickup    fourteenth
    Given using ${bossPortal} I program ${pickup} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with ExtensionValue
    Then on ${phone1} wait for 2 seconds
    Then on ${phone1} verify display message ${pickup}
    Then Verify the led state of Line5 as ${off} on ${phone1}
    Then I want to make a two party call between ${phone3} and ${phone2} using ${loudspeaker}
    Then Verify the led state of Line5 as ${blink} on ${phone1}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then Verify audio path between ${phone1} and ${phone3}
    Then on ${phone3} wait for 2 seconds
    Then Verify the led state of Line5 as ${off} on ${phone1}
    Then disconnect the call from ${phone3}
    Then on ${phone2} navigate to ${availability} settings
    Then Modify call handler mode on ${phone2} to ${always} in ${doNotDisturb}
    Then Press softkey ${Save} on ${phone2}
    Then Press softkey ${Quit} on ${phone2}
    Then on ${phone2} wait for 5 seconds
    Then Verify the led state of Line5 as ${on} on ${phone1}
    Then Change the phone state to default state on ${phone2}
    Then Verify the led state of Line5 as ${off} on ${phone1}
    [Teardown]    RUN KEYWORDS    Generic Test Teardown    Default Availability State

147127: Implicit monitoring (PickupUnpark)
    [Tags]    Owner:AbhishekPathak    Reviewer    target_extension_pickup_unpark    fourteenth
    Given using ${bossPortal} I program ${PickupUnpark} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with ExtensionValue
    Then on ${phone1} wait for 2 seconds
    Then on ${phone1} verify display message ${pickAndUnpar}
    Then Verify the led state of Line5 as ${off} on ${phone1}
    Then I want to make a two party call between ${phone3} and ${phone2} using ${loudspeaker}
    Then Verify the led state of Line5 as ${blink} on ${phone1}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} wait for 2 seconds
    Then Verify the led state of Line1 as ${on} on ${phone1}
    Then Verify the led state of Line5 as ${off} on ${phone1}
    Then Verify audio path between ${phone1} and ${phone3}
    Then disconnect the call from ${phone3}

147128: Implicit monitoring (Unpark)
    [Tags]    Owner:AbhishekPathak    Reviewer    target_extension_unpark    fourteenth
    Given using ${bossPortal} I program ${unpark} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with ExtensionValue
    Then on ${phone1} wait for 2 seconds
    Then on ${phone1} verify display message ${unpark}
    Then Verify the led state of Line5 as ${off} on ${phone1}
    Then I want to make a two party call between ${phone3} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then Verify the led state of Line5 as ${on} on ${phone1}
    Then disconnect the call from ${phone3}
    Then Verify the led state of Line5 as ${off} on ${phone1}
    Then on ${phone2} navigate to ${availability} settings
    Then Modify call handler mode on ${phone2} to ${always} in ${doNotDisturb}
    Then Press softkey ${Save} on ${phone2}
    Then Press softkey ${Quit} on ${phone2}
    Then on ${phone2} wait for 2 seconds
    Then Verify the led state of Line5 as ${on} on ${phone1}
    Then Change the phone state to default state on ${phone2}
    Then Verify the led state of Line5 as ${off} on ${phone1}
    [Teardown]    RUN KEYWORDS    Generic Test Teardown    Default Availability State

558009: pickup - call history
    [Tags]    Owner:AbhishekPathak    Reviewer    pickup_callhistory    fourteenth
    Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then disconnect the call from ${phone2}
    Then on ${phone2} wait for 2 seconds
    Then using ${bossPortal} I program ${pickup} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with noExtensionValue
    Then on ${phone1} wait for 2 seconds
    Then on ${phone1} verify display message ${pickup}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then On ${phone1} verify display message PickUp
    Then On ${phone1} verify display message Backspace
    Then On ${phone1} verify display message Cancel
    Then disconnect the call from ${phone1}
    Then I want to make a two party call between ${phone3} and ${phone2} using ${loudspeaker}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then I want to pickup call from ${phone1} of ${phone2} using ${CallHistory} and ${Select}
    Then disconnect the call from ${phone3}

559961: Xmon - Multiple incoming calls
    [Tags]    Owner:AbhishekPathak    Reviewer:Aman    monitor_extension_multiple_calls    fourteenth
    &{extensionDetails} =    Create Dictionary    ring_delay=dont_ring    show_caller_id=only_when_ringing    no_connected=dial_number    with_connected=dial_number    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then on ${phone1} wait for 2 seconds
    Then on ${phone1} verify display message ${displayMessage['monitorExtn']}
    Then I want to make a two party call between ${phone3} and ${phone2} using ${loudspeaker}
    Then I want to make a two party call between ${phone4} and ${phone2} using ${loudspeaker}
    Then verify the led state of ${line5} as ${blink} on ${phone1}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} wait for 2 seconds
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then Verify audio path between ${phone1} and ${phone3}
    Then Verify extension ${number} of ${phone3} on ${phone1}
    Then disconnect the call from ${phone3}
    Then disconnect the call from ${phone4}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4

    &{extensionDetails} =    Create Dictionary    ring_delay=dont_ring    show_caller_id=never    no_connected=dial_number    with_connected=dial_number    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then on ${phone1} wait for 2 seconds
    Then on ${phone1} verify display message ${displayMessage['monitorExtn']}
    Then I want to make a two party call between ${phone3} and ${phone2} using ${loudspeaker}
    Then I want to make a two party call between ${phone4} and ${phone2} using ${loudspeaker}
    Then verify the led state of ${line5} as ${blink} on ${phone1}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} wait for 2 seconds
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then Verify audio path between ${phone1} and ${phone3}
    Then Verify extension ${number} of ${phone3} on ${phone1}
    Then disconnect the call from ${phone3}
    Then disconnect the call from ${phone4}

558011: pickup - xmon
    [Tags]    Owner:AbhishekPathak    Reviewer    pickup_xmon    fourteenth
    &{extensionDetails} =    Create Dictionary    ring_delay=dont_ring    show_caller_id=never    no_connected=dial_number    with_connected=dial_number    account_name=Automation    part_name=SC1    button_box=0
    Given on ${phone1} Press ${softKey} ${bottomKey1} for 1 times
    Then on ${phone1} verify display message ${pick}
    Then on ${phone1} press the softkey ${cancel} in DialingState
    Then using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then on ${phone1} wait for 2 seconds
    Then on ${phone1} verify display message ${displayMessage['monitorExtn']}
    Then I want to make a two party call between ${phone3} and ${phone2} using ${loudspeaker}
    Then on ${phone1} Press ${softKey} ${bottomKey1} for 1 times
    Then on ${phone1} verify display message ${pickup}
    Then on ${phone1} verify display message ${backspace}
    Then on ${phone1} verify display message ${cancel}
    Then i want to press line key ${programKey5} on phone ${phone1}
    Then Verify audio path between ${phone3} and ${phone1}
    Then disconnect the call from ${phone3}

559827: XMON, CID Always - 1 held call on target
    [Tags]    Owner:AbhishekPathak    Reviewer:Aman    xmon_unpark_pickup    fourteenth
    &{extensionDetails} =    Create Dictionary    ring_delay=dont_ring    show_caller_id=always    no_connected=dial_number    with_connected=dial_number    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then on ${phone1} wait for 2 seconds
    Then on ${phone1} verify display message ${displayMessage['monitorExtn']}
    Then i want to make a two party call between ${phone3} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then Verify audio path between ${phone3} and ${phone2}
    Then press hardkey as ${holdState} on ${phone2}
    Then Verify extension ${number} of ${phone3} on ${phone2}
    Then on ${phone2} verify display message ${pickup}
    Then Verify the led state of ${line5} as ${blink} on ${phone1}
    Then i want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} wait for 2 seconds
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then Verify extension ${number} of ${phone3} on ${phone1}
    Then Verify audio path between ${phone3} and ${phone1}
    Then Verify the led state of ${line5} as ${on} on ${phone1}
    Then On ${phone2} verify the softkeys in ${idle}
    Then disconnect the call from ${phone3}

559908: Put picked-up XMON call on hold
    [Tags]    Owner:AbhishekPathak    Reviewer    xmon_picked_hold    fourteenth
    &{extensionDetails} =    Create Dictionary    ring_delay=dont_ring    show_caller_id=never    no_connected=dial_number    with_connected=dial_number    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 4 with ExtensionValue
    Then on ${phone1} wait for 2 seconds
    Then on ${phone1} verify display message ${displayMessage['monitorExtn']}
    Then i want to make a two party call between ${phone3} and ${phone2} using ${loudspeaker}
    Then i want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} wait for 2 seconds
    Then i want to press line key ${programKey5} on phone ${phone1}
    Then verify the led state of ${line5} as ${on} on ${phone1}
    Then Verify audio path between ${phone3} and ${phone1}
    Then Press hardkey as ${HoldState} on ${phone1}
    Then verify the led state of ${line5} as ${blink} on ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone2}
    Then Verify extension ${number} of ${phone3} on ${phone2}
    Then disconnect the call from ${phone3}
    Then on ${phone1} wait for 5 seconds

    Then i want to make a two party call between ${phone3} and ${phone2} using ${loudspeaker}
    Then i want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} wait for 2 seconds
    Then i want to press line key ${programKey5} on phone ${phone1}
    Then verify the led state of ${line5} as ${on} on ${phone1}
    Then Verify audio path between ${phone3} and ${phone1}
    Then i want to press line key ${programKey5} on phone ${phone1}
    Then verify the led state of ${line5} as ${blink} on ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone2}
    Then Verify extension ${number} of ${phone3} on ${phone2}
    Then disconnect the call from ${phone3}

559982: monitor extension and Park call - ALWAYS
    [Tags]    Owner:AbhishekPathak    Reviewer    xmon_park_always    fourteenth
    &{extensionDetails} =    Create Dictionary    ring_delay=dont_ring    show_caller_id=always    no_connected=dial_number    with_connected=dial_number    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 4 with ExtensionValue
    Then on ${phone1} wait for 2 seconds
    Then on ${phone1} verify display message ${displayMessage['monitorExtn']}
    Then i want to make a two party call between ${phone3} and ${phone2} using ${loudspeaker}
    Then on ${phone2} wait for 4 seconds
    Then verify the led state of ${line5} as ${blink} on ${phone1}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then Verify audio path between ${phone3} and ${phone2}
    Then verify the led state of ${line5} as ${on} on ${phone1}
    Then I want to Park the call from ${phone2} on ${phone4} using ${default} and ${Park}
    Then on ${phone2} wait for 5 seconds
    Then verify the led state of ${line5} as ${off} on ${phone1}
    Then disconnect the call from ${phone3}


559986: set Show Caller ID to NEVER for extension monitor then park
    [Tags]    Owner:AbhishekPathak    Reviewer    xmon_park_never    fourteenth
    &{extensionDetails} =    Create Dictionary    ring_delay=dont_ring    show_caller_id=never    no_connected=dial_number    with_connected=dial_number    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 4 with ExtensionValue
    Then on ${phone1} wait for 2 seconds
    Then on ${phone1} verify display message ${displayMessage['monitorExtn']}
    Then i want to make a two party call between ${phone3} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then Verify audio path between ${phone3} and ${phone2}
    Then I want to Park the call from ${phone2} on ${phone4} using ${default} and ${Park}
    Then on ${phone2} wait for 5 seconds
    Then On ${phone2} verify the softkeys in ${idle}
    Then disconnect the call from ${phone3}

560149: Pickup XMON call, hold, unpark, hold
    [Tags]    Owner:AbhishekPathak    Reviewer    xmon_hold_unpark_hold    fourteenth
    &{extensionDetails} =    Create Dictionary    ring_delay=dont_ring    show_caller_id=never    no_connected=dial_number    with_connected=dial_number    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 4 with ExtensionValue
    Then on ${phone1} wait for 2 seconds
    Then on ${phone1} verify display message ${displayMessage['monitorExtn']}
    Then i want to make a two party call between ${phone3} and ${phone2} using ${loudspeaker}
    Then i want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} wait for 2 seconds
    Then i want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} wait for 2 seconds
    Then verify the led state of ${line5} as ${on} on ${phone1}
    Then Verify audio path between ${phone3} and ${phone1}
    Then i want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} wait for 2 seconds
    Then verify the led state of ${line5} as ${blink} on ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone2}
    Then i want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} wait for 2 seconds
    Then i want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} wait for 5 seconds
    Then on ${phone2} verify the softkeys in ${idle}
    Then Verify audio path between ${phone3} and ${phone1}
    Then verify the led state of ${line5} as ${on} on ${phone1}
    Then disconnect the call from ${phone3}

561980: Two incoming calls ringing; press Pickup or XMON
    [Tags]    Owner:AbhishekPathak    Reviewer    xmon_verify_extension_number    fourteenth
    &{extensionDetails} =    Create Dictionary    ring_delay=dont_ring    show_caller_id=never    no_connected=dial_number    with_connected=dial_number    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 4 with ExtensionValue
    Then on ${phone1} wait for 2 seconds
    Then on ${phone1} verify display message ${displayMessage['monitorExtn']}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then i want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then i want to press line key ${programKey5} on phone ${phone1}
    Then Verify extension ${number} of ${phone2} on ${phone1}
    Then disconnect the call from ${phone3}
    Then disconnect the call from ${phone2}

560437: Third party Holds the call with Whisper paged extension
    [Tags]    Owner:AbhishekPathak    Reviewer    whisperpage_ext_with_hold    fourteenth
    Given using ${bossPortal} I program ${whisperPage} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with ExtensionValue
    Then On ${phone1} verify display message ${whisperPage}
    Then i want to make a two party call between ${phone2} and ${phone3} using ${loudspeaker}
    Then answer the call on ${phone3} using ${loudspeaker}
    Then Verify audio path between ${phone2} and ${phone3}
    Then i want to press line key ${programKey5} on phone ${phone1}
    Then Verify audio path between ${phone1} and ${phone2}
    Then verify no audio path from ${phone1} to ${phone3}
    Then Press hardkey as ${HoldState} on ${phone3}
    Then i want to press line key ${programKey2} on phone ${phone3}
    Then i want to make a two party call between ${phone3} and ${phone4} using ${loudspeaker}
    Then answer the call on ${phone4} using ${loudspeaker}
    Then Verify the led state of ${line1} as ${blink} on ${phone3}
    Then Verify audio path between ${phone4} and ${phone3}
    Then Verify audio path between ${phone1} and ${phone2}
    Then verify no audio path from ${phone1} to ${phone3}
    Then verify no audio path from ${phone1} to ${phone4}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone4}
    Then disconnect the call from ${phone1}

560002: (connected call : Whisper page)when monitoring phone is in held state and target extension is ringing back
    [Tags]    Owner:AbhishekPathak    Reviewer    xmon_connectedcall_whisperpage    fourteenth
    &{extensionDetails} =    Create Dictionary    ring_delay=dont_ring    show_caller_id=never    no_connected=dial_number    with_connected=whisper_page    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then on ${phone1} wait for 2 seconds
    Then on ${phone1} verify display message ${displayMessage['monitorExtn']}
    Then i want to make a two party call between ${phone2} and ${phone3} using ${loudspeaker}
    Then verify the led state of ${line5} as ${on} on ${phone1}
    Then disconnect the call from ${phone2}
    Then i want to make a two party call between ${phone4} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then Verify audio path between ${phone4} and ${phone1}
    Then Press hardkey as ${HoldState} on ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} wait for 2 seconds
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then Verify audio path between ${phone1} and ${phone2}
    Then verify the led state of ${line5} as ${on} on ${phone1}
    Then disconnect the call from ${phone4}
    Then disconnect the call from ${phone1}

559595: Cancelling a Conference Blind call
    [Tags]    Owner:AbhishekPathak    Reviewer    conferenceblind_cancel    fourteenth
    Given using ${bossPortal} I program ${conferenceBlind} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with noExtensionValue
    Then on ${phone1} verify display message ${displayMessage['conferenceBlind']}
    Then i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} enter number ${phone3}
    Then Verify extension ${number} of ${phone3} on ${phone1}
    Then on ${phone1} verify display message ${conference}
    Then on ${phone1} verify display message ${backspace}
    Then on ${phone1} verify display message ${cancel}
    Then press softkey cancel on ${phone1}
    Then verify no audio path from ${phone1} to ${phone2}
    Then verify no audio path from ${phone2} to ${phone1}
    Then disconnect the call from ${phone2}

559606: Conference Blind Call from directory
    [Tags]    Owner:AbhishekPathak    Reviewer    conferenceblind_directory    fourteenth
    Given using ${bossPortal} I program ${conferenceBlind} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with noExtensionValue
    Then on ${phone1} verify display message ${displayMessage['conferenceBlind']}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} verify directory with ${directoryAction['selectOnly']} of ${phone3}
    Then on ${phone3} wait for 8 seconds
    Then answer the call on ${phone3} using ${loudspeaker}
    Then conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone1}

559668: TC023 Press speed dial key twice while being in active call
    [Tags]    Owner:AbhishekPathak    Reviewer    speeddial_repeat    fifteenth
    Given using ${bossPortal} I program ${dialNumber} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then on ${phone1} verify display message ${displayMessage['dialNumber']}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then verify ringing state on ${phone1} and ${phone2}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify the led state of ${line5} as ${on} on ${phone1}
    Then Verify audio path between ${phone1} and ${phone2}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then verify the led state of ${line2} as ${blink} on ${phone2}
    Then verify ringing state on ${phone1} and ${phone2}
    Then press hardkey as ${goodBye} on ${phone1}
    Then disconnect the call from ${phone2}

559604: Hold the 'Conference Blind' call
    [Tags]    Owner:AbhishekPathak    Reviewer    conferenceblind_hold    fifteenth
    Given using ${bossPortal} I program ${conferenceBlind} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with extensionValue
    Then on ${phone1} verify display message ${displayMessage['conferenceBlind']}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} wait for 5 seconds
    Then verify ringing state on ${phone1} and ${phone3}
    Then answer the call on ${phone3} using ${loudspeaker}
    Then conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then Press hardkey as ${HoldState} on ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then Verify audio path between ${phone2} and ${phone3}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}

559569: Hold the 'Conference consult' call
    [Tags]    Owner:AbhishekPathak    Reviewer    conferenceconsult_hold    fifteenth
    Given using ${bossPortal} I program ${conferenceConsultative} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then on ${phone1} verify display message ${displayMessage['conferenceConsult']}
    Then i want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then Verify audio path between ${phone3} and ${phone1}
    Then i want to press line key ${programkey5} on phone ${phone1}
    Then on ${phone1} wait for 2 seconds
    Then verify ringing state on ${phone1} and ${phone2}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Press hardkey as ${HoldState} on ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then verify no audio path from ${phone1} to ${phone2}
    Then verify no audio path from ${phone2} to ${phone1}
    Then disconnect the call from ${phone3}
    Then disconnect the call from ${phone2}

559571: Conference Consult Call from directory
    [Tags]    Owner:AbhishekPathak    Reviewer    conferenceconsult_directory    fifteenth
    Given using ${bossPortal} I program ${conferenceConsultative} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with noExtensionValue
    Then on ${phone1} verify display message ${displayMessage['conferenceConsult']}
    Then i want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then Verify audio path between ${phone3} and ${phone1}
    Then i want to press line key ${programkey5} on phone ${phone1}
    Then on ${phone1} wait for 2 seconds
    Then On ${phone1} verify directory with ${directoryAction['selectOnly']} of ${phone2}
    Then on ${phone2} wait for 5 seconds
    Then verify ringing state on ${phone1} and ${phone2}
    Then verify extension ${number} of ${phone1} on ${phone2}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}

560118: Park call to user on active call
    [Tags]    Owner:AbhishekPathak    Reviewer    callcontrol_park    fifteenth
    Given using ${bossPortal} I program ${park} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with ExtensionValue
    Then on ${phone1} verify display message Park
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then Verify audio path between ${phone2} and ${phone1}
    Then on ${phone3} verify the softkeys in ${idle}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then Verify the led state of ${line5} as ${on} on ${phone1}
    Then on ${phone3} wait for 2 seconds
    Then on ${phone3} press ${softKey} ${BottomKey1} for 1 times
    Then Verify audio path between ${phone2} and ${phone3}
    Then disconnect the call from ${phone2}

565115: Silent Monitor button with extension target programmed- On Hook
    [Tags]    Owner:AbhishekPathak    Reviewer    callcontrol_silentcoach_onhook    fifteenth
    Given using ${bossPortal} I program ${silentmonitor} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then on ${phone1} verify display message ${displayMessage['silentMonitor']}
    Then i want to make a two party call between ${phone2} and ${phone3} using ${loudspeaker}
    Then answer the call on ${phone3} using ${loudspeaker}
    Then Verify audio path between ${phone2} and ${phone3}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} wait for 2 seconds
    Then verify no audio path from ${phone1} to ${phone2}
    Then verify no audio path from ${phone1} to ${phone3}
    Then Verify one way audio from ${phone2} to ${phone1}
    Then Verify one way audio from ${phone3} to ${phone1}
    Then on ${phone1} press the softkey ${drop} in AnswerState
    Then Verify audio path between ${phone2} and ${phone3}
    Then disconnect the call from ${phone2}

557146: TC04: Offscreen call moves to idle call appearance
    [Tags]    Owner:AbhishekPathak    Reviewer:    move_ca    fifteenth
    Given using ${bossPortal} I program 1 Call Appearance button on ${phone1}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then i want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then on ${phone1} press ${softkey} ${bottomkey1} for 1 times
    Then disconnect the call from ${phone2}
    Then on ${phone2} verify the softkeys in ${idle}
    Then Verify audio path between ${phone1} and ${phone3}
    Then disconnect the call from ${phone3}

565181: Record extension
    [Tags]    Owner:AbhishekPathak    Reviewer:    record_ext    fifteenth
    Given using ${bossPortal} I program ${recordExtension} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then on ${phone1} verify display message Record Exten
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} verify the softkeys in ${idle}

565186: Page, ParknPage
    [Tags]    Owner:AbhishekPathak    Reviewer:    page_parkpage    fifteenth
    Given using ${bossPortal} I program ${page} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with noextensionValue
    Then on ${phone1} verify display message Page
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} verify the softkeys in ${idle}
    Then using ${bossPortal} I program ${parknpage} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 5 with extensionValue
    Then on ${phone1} verify display message Park and Pag
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} verify the softkeys in ${idle}

559232: Hang up displays when BCA progbutton is pressed
    [Tags]    Owner:AbhishekPathak    Reviewer    press_bca    fifteenth
    [Setup]    BCA Custom Setup
    &{createBCAExtension} =  Create Dictionary    name=bca_pathak   backupExtn=${phone3}    switch=2    callStackDepth=2    forwardAfter=2    callStackFull=${EMPTY}   noAnswer=${EMPTY}    outboundCallerID=${EMPTY}    allowBridgeConferencing=true   defaultPrivacySettings=0
    ${bcaExtn}=    using ${bossPortal} I want to create Bridge Call Appearance extension using ${createBCAExtension}
    &{BCAdetails} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=4    function=Bridge Call Appearance    label=BCA    target_extension=${bcaExtn}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${phone2}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=Dial extension
    Given using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails}
    Then on ${phone1} verify display message BCA
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then verify extension ${number} of ${phone2} on ${phone1}
    Then on ${phone1} verify display message ${cancel}
    Then Press hardkey as ${goodBye} on ${phone1}
    [Teardown]    BCA Custom Teardown

559244: set Show Caller ID to ALWAYS for BCA then park
    [Tags]    Owner:AbhishekPathak    Reviewer    park_bca    fifteenth
    [Setup]    BCA Custom Setup
    &{createBCAExtension} =  Create Dictionary    name=bca_pathak   backupExtn=${phone3}    switch=2    callStackDepth=2    forwardAfter=2    callStackFull=${EMPTY}   noAnswer=${EMPTY}    outboundCallerID=${EMPTY}    allowBridgeConferencing=true   defaultPrivacySettings=0
    ${bcaExtn}=    using ${bossPortal} I want to create Bridge Call Appearance extension using ${createBCAExtension}
    &{BCAdetails} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=4    function=Bridge Call Appearance    label=BCA    target_extension=${bcaExtn}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${phone4}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=Dial extension
    Given using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails}
    Then on ${phone1} verify display message BCA
    Then on ${phone2} dial number ${bcaExtn}
    Then verify the led state of ${line5} as ${blink} on ${phone1}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then verify extension ${number} of ${phone2} on ${phone1}
    Then Verify audio path between ${phone1} and ${phone2}
    Then I want to Park the call from ${phone1} on ${phone3} using ${default} and ${Park}
    Then verify extension ${number} of ${phone2} on ${phone3}
    Then disconnect the call from ${phone2}
    [Teardown]    BCA Custom Teardown

559749:Press Hotline speed dial button to initiate a call
    [Tags]    Owner:AbhishekPathak    Reviewer    hotline_speeddial    fifteenth
    &{hotlines}    CREATE DICTIONARY    ConnectedCallFunctionID=dial number    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program Hotline on ${phone1} using ${hotlines} and extension of ${phone2} and softkey position 4 with extensionValue
    Then on ${phone1} verify display message ${hotline}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then answer the call on ${phone2} using ${programKey1}
    Then Verify audio path between ${phone1} and ${phone2}
    Then Verify the led state of ${line5} as ${on} on ${phone1}
    Then disconnect the call from ${phone2}


559755: BLIND-Transfer a call by pressing Hotline speed dial button
    [Tags]    Owner:AbhishekPathak    Reviewer    hotline_blindtransfer    fifteenth
    &{hotlines}    CREATE DICTIONARY    ConnectedCallFunctionID=dial number    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${hotline} on ${phone1} using ${hotlines} and extension of ${phone2} and softkey position 4 with extensionValue
    Then on ${phone1} verify display message ${hotline}
    Then i want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then on ${phone3} wait for 2 seconds
    Then Verify the led state of ${line1} as ${on} on ${phone3}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then Verify audio path between ${phone3} and ${phone1}
    Then on ${phone1} press the softkey ${Transfer} in AnswerState
    Then Verify the led state of ${line1} as ${blink} on ${phone1}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} wait for 5 seconds
    Then on ${phone1} press the softkey ${transfer} in DialingState
    Then on ${phone3} wait for 3 seconds
    Then Verify the led state of ${line1} as ${blink} on ${phone2}
    Then disconnect the call from ${phone3}
    Then Press hardkey as ${goodBye} on ${phone1}

558253: TC009 Making HG extension private
    [Tags]    Owner:AbhishekPathak    Reviewer:    huntgroup    fifteenth
    [Setup]    Hunt Group Custom Setup
    @{members}   Create List    ${phone3}
    &{huntGroupDetails} =  Create Dictionary    BackupExtension=${phone3}    GroupMembers=${members}   GroupName=HG_AP   IncludeInSystem=True    MakeExtnPrivate=False    HuntPattern=4    RingsPerMember=2    NoAnswerRings=4    CallMemberWhenForwarding=True    SkipMemberOnCall=True    CallStackFull=${EMPTY}    NoAnswer=${EMPTY}
    ${HGExtension} =     using ${bossPortal} I want to create hunt group user extension with ${huntGroupDetails}
    Given i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then on ${phone2} press the softkey ${transfer} in answerstate
    Then On ${phone2} verify directory with ${directoryAction['selectOnly']} of ${HGExtension}
    Then on ${phone2} wait for 5 seconds
    Then on ${phone2} press the softkey ${Transfer} in TransferState
    Then On ${phone1} verify display message ${HGExtension}
    Then answer the call on ${phone3} using ${loudspeaker}
    Then verify extension ${number} of ${phone3} on ${phone1}
    Then disconnect the call from ${phone1}
    Then using ${bossPortal} I want to remove hunt group user extension ${HGExtension}
    [Teardown]    Hunt Group Custom Teardown

558254: Blind Transfer Hunt Group while ringing
    [Tags]    Owner:AbhishekPathak    Reviewer:    huntgroup    fifteenth
    [Setup]    Hunt Group Custom Setup
    @{members}   Create List    ${phone3}
    &{huntGroupDetails} =  Create Dictionary    BackupExtension=${phone3}    GroupMembers=${members}   GroupName=HG_AP   IncludeInSystem=True    MakeExtnPrivate=False    HuntPattern=4    RingsPerMember=2    NoAnswerRings=4    CallMemberWhenForwarding=True    SkipMemberOnCall=True    CallStackFull=${EMPTY}    NoAnswer=${EMPTY}
    ${HGExtension} =     using ${bossPortal} I want to create hunt group user extension with ${huntGroupDetails}
    Then i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then verify extension ${number} of ${phone2} on ${phone1}
    Then on ${phone2} press the softkey ${transfer} in ringingstate
    Then on ${phone2} enter number ${HGExtension}
    Then On ${phone1} verify display message ${huntGroupDetails['GroupName']}
    Then On ${phone1} verify display message ${HGExtension}
    Then on ${phone1} wait for 5 seconds
    Then answer the call on ${phone3} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone3}
    Then verify extension ${number} of ${phone3} on ${phone1}
    Then disconnect the call from ${phone1}
    Then using ${bossPortal} I want to remove hunt group user extension ${HGExtension}
    [Teardown]    Hunt Group Custom Teardown

558260: Cancel incoming call Transfer to Agents via Huntgroup Extension
    [Tags]    Owner:AbhishekPathak    Reviewer:    hgt    fifteenth
    [Setup]    Hunt Group Custom Setup
    @{members}   Create List      ${phone2}    ${phone3}    ${phone4}
    &{huntGroupDetails} =  Create Dictionary    BackupExtension=${phone4}    GroupMembers=${members}   GroupName=HG_AP   IncludeInSystem=True    MakeExtnPrivate=True    HuntPattern=1    RingsPerMember=3    NoAnswerRings=4    CallMemberWhenForwarding=True    SkipMemberOnCall=True    CallStackFull=${EMPTY}    NoAnswer=${EMPTY}
    ${HGExtension} =     using ${bossPortal} I want to create hunt group user extension with ${huntGroupDetails}
    Given i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then on ${phone2} press the softkey ${transfer} in answerstate
    Then on ${phone2} dial number ${HGExtension}
    Then On ${phone2} verify display message ${HGExtension}
    Then verify extension ${number} of ${phone2} on ${phone3}
    Then on ${phone2} wait for 4 seconds
    Then On ${phone2} verify display message ${HGExtension}
    Then on ${phone4} wait for 10 seconds
    Then answer the call on ${phone4} using ${loudspeaker}
    Then Verify audio path between ${phone2} and ${phone4}
    Then verify extension ${number} of ${phone4} on ${phone2}
    Then on ${phone2} press ${softkey} ${bottomkey1} for 1 times
    Then verify extension ${number} of ${phone2} on ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone2}
    Then disconnect the call from ${phone1}
    Then using ${bossPortal} I want to remove hunt group user extension ${HGExtension}
    [Teardown]    Hunt Group Custom Teardown

560247 : Press Silent Coach during UCB Call
    [Tags]      Owner:AbhishekPathak    Reviewer:    silentcoach_ucb_call    fifteenth
    Given using ${bossPortal} I program ${silentcoach} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then on ${phone1} verify display message ${displaysilentcoach}
    Then on ${phone2} press ${softkey} ${bottomkey3} for 1 times
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} verify display message ${notPermittedOnThisCall}
    Then disconnect the call from ${phone2}
    Then Press hardkey as ${goodBye} on ${phone1}
    Then on ${phone2} press ${softkey} ${bottomkey3} for 1 times
    Then on ${phone2} dial number ${wrongAccessCode}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} verify display message ${notPermittedOnThisCall}
    Then disconnect the call from ${phone2}
    Then Press hardkey as ${goodBye} on ${phone1}
    Then on ${phone2} press ${softkey} ${bottomkey3} for 1 times
    Then on ${phone2} dial number ${accessCode}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} verify display message ${notPermittedOnThisCall}
    Then disconnect the call from ${phone2}
    Then Press hardkey as ${goodBye} on ${phone1}

559903: TC07: Monitoring ph gets incoming call while Monitored phone has active call
   [Tags]    Owner:AbhishekPathak    Reviewer    xmon    fifteenth
    &{extensionDetails} =    Create Dictionary    ring_delay=none    show_caller_id=always    no_connected=dial_number    with_connected=dial_number    account_name=Automation    part_name=SC1    button_box=0
    Then using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then on ${phone1} verify display message ${displayMessage['monitorExtn']}
    Then i want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then Verify audio path between ${phone3} and ${phone1}
    Then i want to make a two party call between ${phone2} and ${phone4} using ${loudspeaker}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then verify extension ${number} of ${phone4} on ${phone1}
    Then disconnect the call from ${phone3}
    Then on ${phone2} verify display message ${ringing}
    Then disconnect the call from ${phone2}

559905: TC09: DUT monitors 2 users - Ring delay set to DonΓÇÖt Ring for X and None for Y
   [Tags]    Owner:AbhishekPathak    Reviewer:Ram    xmon2    fifteenth
    &{extensionDetails} =    Create Dictionary    ring_delay= -1    show_caller_id=always    no_connected=dial_number    with_connected=dial_number    account_name=Automation    part_name=SC1    button_box=0
    Then using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 3 with extensionValue
    &{extensionDetails2} =    Create Dictionary    ring_delay= 0    show_caller_id=always    no_connected=dial_number    with_connected=dial_number    account_name=Automation    part_name=SC1    button_box=0
    Then using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails2} and extension of ${phone3} and softkey position 4 with extensionValue
    Then on ${phone1} verify display message ${displayMessage['monitorExtn']}
    Then i want to make a two party call between ${phone4} and ${phone2} using ${loudspeaker}
    Then I want to press line key ${programKey4} on phone ${phone1}
    Then on ${phone4} verify display message ${ringing}
    Then verify extension ${number} of ${phone4} on ${phone1}
    Then i want to make a two party call between ${phone5} and ${phone3} using ${loudspeaker}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then verify extension ${number} of ${phone5} on ${phone1}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then Verify audio path between ${phone2} and ${phone4}
    Then verify extension ${number} of ${phone5} on ${phone1}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}
    Then disconnect the call from ${phone5}


560314: Hold and hang up the transfer consult call
    [Tags]    Owner:AbhishekPathak    Reviewer:    transfer    fifteenth
    Given using ${bossPortal} I program ${transferConsultative} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['transferConsult']}
    Then i want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then Verify audio path between ${phone3} and ${phone1}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone2}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then press hardkey as ${holdState} on ${phone1}
    Then verify no audio path from ${phone1} to ${phone2}
    Then Press hardkey as ${goodBye} on ${phone1}
    Then verify extension ${number} of ${phone3} on ${phone2}
    Then verify extension ${number} of ${phone2} on ${phone3}
    Then Verify audio path between ${phone2} and ${phone3}
    Then disconnect the call from ${phone3}

560329: TC009 - Blind transfer the answered outgoing call
    [Tags]      Owner:AbhishekPathak      Reviewer:    transfer    sixteenth
    Given using ${bossPortal} I program ${transferBlind} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['transferBlind']}
    Then i want to make a two party call between ${phone1} and ${phone3} using ${loudspeaker}
    Then answer the call on ${phone3} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone3}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone2} wait for 2 seconds
    Then verify extension ${number} of ${phone3} on ${phone2}
    Then disconnect the call from ${phone3}


560828: for intercom, intercom should work when permission is allowed, and not show when no permission
    [Tags]    Owner:AbhishekPathak    Reviewer:    cos    sixteenth
    &{COSDetails} =  Create Dictionary    Name=${fullyFeatured}    AllowIntercomInitiation=True
    using ${bossPortal} I want to change telephony features values using ${COSDetails}
    Then On ${phone1} press directory and ${Intercom} of ${phone2}
    Then verify extension ${number} of ${phone2} on ${phone1}
    Then Verify audio path between ${phone1} and ${phone2}
    Then disconnect the call from ${phone1}
    Then on ${phone1} wait for 5 seconds
    &{COSDetails} =  Create Dictionary    Name=${fullyFeatured}    AllowIntercomInitiation=False
    using ${bossPortal} I want to change telephony features values using ${COSDetails}
    Then On ${phone1} press directory and ${Intercom} of ${phone2}
    Then i want to verify on ${phone1} negative display message ${Intercom}
    Then on ${phone1} wait for 2 seconds
    Then press hardkey as ${goodBye} on ${phone1}
    [Teardown]    CoS Features Custom Teardown

560802: TC015 Making a whisper page call while being in a whisper page call
    [Tags]    Owner:AbhishekPathak    Reviewer:    whisper    sixteenth
    Given using ${bossPortal} I program ${whisperpage} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with ExtensionValue
    Then On ${phone1} verify display message ${whisperpage}
    Then using ${bossPortal} I program ${whisperPage} on ${phone2} using ${bossDetails} and extension of ${phone3} and softkey position 4 with ExtensionValue
    Then On ${phone2} verify display message ${whisperPage}
    Then i want to press line key ${programKey5} on phone ${phone1}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
    Then verify extension ${number} of ${phone2} on ${phone1}
    Then Verify audio path between ${phone1} and ${phone2}
    Then i want to press line key ${programKey5} on phone ${phone2}
    Then Verify the led state of ${line5} as ${on} on ${phone2}
    Then Verify audio path between ${phone2} and ${phone3}
    Then I want to verify on ${phone1} negative display message ${phone2}
    Then on ${phone1} verify the softkeys in ${idle}
    Then press hardkey as ${goodBye} on ${phone2}

558363: TC014 Hold the 'Transfer Whipser' call
    [Tags]    Owner:AbhishekPathak    Reviewer    wp    sixteenth
    &{pmargst} =  Create Dictionary  key=${holdState}
    &{pressHardkey} =  Create Dictionary  action_name=pressHardkey   pmargs=&{pmargst}
    Given using ${bossPortal} I program ${transferWhisper} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['transferToWhisper']}
    Then i want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone3}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then Verify audio path between ${phone1} and ${phone2}
    Then On ${phone3} verify display message ${drop}
    Then On ${phone1} verify display message ${transfer}
    Then on ${phone1} due to action ${pressHardkey} popup raised verify message Hold not permitted with wait of 0
    Then disconnect the call from ${phone3}
    Then disconnect the call from ${phone1}

541280:phone presses Pickup progbutton enter extension
    [Tags]    Owner:AbhishekPathak    Reviewer:    grouppickup    easywin_migration    sixteenth
    Then using ${bossPortal} I program ${pickup} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with noExtensionValue
    Given i want to make a two party call between ${phone3} and ${phone2} using ${loudspeaker}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} dial number ${grouppickup}
    Then Verify audio path between ${phone1} and ${phone3}
    Then disconnect the call from ${phone3}

754343: Monitoring the Intercom extension "Active or Held Call"
    [Tags]    Owner:AbhishekPathak    Reviewer:    xmon    sixteenth
    Given on ${phone1} navigate to ${availability} settings
    Then Modify call handler mode on ${phone1} to ${noMode} in ${available}
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then Press softkey ${Quit} on ${phone1}
    &{extensionDetails} =    Create Dictionary    ring_delay=dont_ring    show_caller_id=always    no_connected=dial_number    with_connected=Intercom    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 4 with ExtensionValue
    Then on ${phone1} verify display message ${displayMessage['monitorExtn']}
    Then i want to make a two party call between ${phone3} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then Verify audio path between ${phone3} and ${phone2}
    Then verify the led state of ${line5} as ${on} on ${phone1}
    Then on ${phone1} verify ${line5} icon state as ${xmonBusy}
    Then disconnect the call from ${phone3}
    [Teardown]    RUN KEYWORDS    Generic Test Teardown    Default Availability State

754342:Monitoring the Intercom extension "Idle or Offering Call"
    [Tags]    Owner:AbhishekPathak    Reviewer:    xmon    sixteenth
    Given on ${phone1} navigate to ${availability} settings
    Then Modify call handler mode on ${phone1} to ${noMode} in ${available}
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then Press softkey ${Quit} on ${phone1}
    &{extensionDetails} =    Create Dictionary    ring_delay=dont_ring    show_caller_id=always    no_connected=dial_number    with_connected=Intercom    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 3 with ExtensionValue
    Then on ${phone1} verify display message ${displayMessage['monitorExtn']}
    Then on ${phone1} wait for 2 seconds
    Then verify the led state of ${line4} as ${off} on ${phone1}
    Then on ${phone1} verify ${line4} icon state as ${xmonIdle}
    [Teardown]    RUN KEYWORDS    Generic Test Teardown    Default Availability State

754446: XMON, CID Always - multiple held calls on target, no incoming calls
    [Tags]    Owner:AbhishekPathak    Reviewer:    xmon    sixteenth
    &{extensionDetails} =    Create Dictionary    ring_delay=dont_ring    show_caller_id=always    no_connected=dial_number    with_connected=dial_number    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 4 with ExtensionValue
    Then i want to make a two party call between ${phone3} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${line1}
    Then Verify audio path between ${phone3} and ${phone2}
    Then i want to make a two party call between ${phone4} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${line2}
    Then Verify audio path between ${phone4} and ${phone2}
    Then press hardkey as ${holdState} on ${phone2}
    Then verify the led state of ${line5} as ${blink} on ${phone1}
    Then on ${phone1} verify ${line5} icon state as MONITOR_EXT_HOLD
    Then on ${phone1} verify display message ${pickup}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then Verify extension ${number} of ${phone3} on ${phone1}
    Then Press hardkey as ${scrolldown} on ${phone1}
    Then Verify extension ${number} of ${phone4} on ${phone1}
    Then on ${phone1} verify display message ${unpark}
    Then on ${phone1} verify display message ${cancel}
    Then on ${phone1} press ${softKey} ${BottomKey4} for 2 times
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then Press hardkey as ${scrolldown} on ${phone1}
    Then on ${phone1} press ${softKey} ${BottomKey1} for 1 times
    Then Verify extension ${number} of ${phone4} on ${phone1}
    Then verify the led state of ${line5} as ${blink} on ${phone1}
    Then on ${phone1} verify ${line5} icon state as MONITOR_EXT_RINGING
    Then disconnect the call from ${phone3}
    Then disconnect the call from ${phone4}

753637:Admin makes 2 way conf on SCA line1, Admin leaves, gets dialog, parks call, Admin unholds has audio to A and B
    [Tags]    Owner:AbhishekPathak    Reviewer:    bca
    [Setup]    Telephony Feature Custom Setup
    &{telephonydetails} =  Create Dictionary    sca_enabled=True
    ${scaExtn} =  using ${bossPortal} on ${phone4} I want to enable SCA using ${telephonydetails}
    &{BCAdetails} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=4    function=Bridge Call Appearance    label=BCA    target_extension=${scaExtn}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${phone2}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=Dial tone
    Given using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails}
    Then on ${phone1} verify display message BCA
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} enter number ${phone2}
    Then on ${phone2} wait for 5 seconds
    Then answer the call on ${phone2} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then i want to make a conference call between ${phone1},${phone2} and ${phone3} using ${directConference}
    Then conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then press hardkey as ${goodbye} on ${phone1}
    Then on ${phone1} verify display message Keep managing conference call?
    Then press softkey ${yes} on ${phone1}
    Then on ${phone1} verify ${line5} icon state as BCA_HOLD_OR_PARKED
    Then Verify audio path between ${phone3} and ${phone2}
    Then press hardkey as ${holdState} on ${phone1}
    Then conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then press hardkey as ${goodbye} on ${phone1}
    Then press softkey ${no} on ${phone1}
    Then verify extension ${number} of ${phone2} on ${phone3}
    Then on ${phone1} verify the softkeys in ${idle}
    Then disconnect the call from ${phone2}
    [Teardown]    Telephony Feature Custom Teardown

752461:Blind Transfer
    [Tags]    Owner:AbhishekPathak    Reviewer:    moh    sixteenth    notApplicableForMiCloud
    #MOH
    &{MOHFeatures} =  Create Dictionary   option=1    fileName=MOH_50
    using ${bossPortal} I want to enable MOH features using ${MOHFeatures}
    using ${bossPortal} I want to modify usergroups MOH for ${executives} with filename MOH_150
    Then i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then on ${phone1} press ${softKey} ${BottomKey3} for 1 times
    Then on ${phone1} enter number ${phone3}
    Then on ${phone2} wait for 5 seconds
    Then verify MOH audio on ${phone2} for 50 frequency
    Then on ${phone3} wait for 5 seconds
    Then answer the call on ${phone3} using ${loudspeaker}
    Then on ${phone1} press ${softKey} ${BottomKey3} for 1 times
    Then Verify no MOH audio on ${phone3}
    Then press hardkey as ${holdState} on ${phone3}
    Then verify MOH audio on ${phone2} for 50 frequency
    Then press hardkey as ${holdState} on ${phone3}
    Then disconnect the call from ${phone3}
    &{MOHFeatures} =  Create Dictionary   option=0    fileName=MOH_50
    using ${bossPortal} I want to disable MOH features using ${MOHFeatures}


565060:Press programmed Dial Number button while a call is on Hold
    [Tags]    Owner:AbhishekPathak    Reviewer:    pkm    sixteenth
    Given using ${bossPortal} I program ${dialNumber} on ${phone1} using ${bossDetailsPKM} and extension of ${phone2} and softkey position 1 with extensionValue
    Given using ${bossPortal} I program ${dialNumber} on ${phone1} using ${bossDetailsPKM} and extension of ${phone2} and softkey position 3 with extensionValue
    Given using ${bossPortal} I program ${dialNumber} on ${phone1} using ${bossDetailsPKM} and extension of ${phone2} and softkey position 7 with extensionValue
    Then on ${phone1} verify display message ${displayMessage['dialNumber']}
    Then i want to make a two party call between ${phone1} and ${phone3} using ${loudspeaker}
    Then On ${phone1} verify ${line1} icon state as ${callAppearanceActive}
    Then answer the call on ${phone3} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone3}
    Then press hardkey as ${holdstate} on ${phone3}
    Then I want to press PKM line key ${programkey2} on ${phone1}
    Then on ${phone1} wait for 5 seconds
    Then On ${phone1} verify ${line2} icon state as ${callAppearanceActive}
    Then press hardkey as ${goodbye} on ${phone1}
    Then press hardkey as ${holdstate} on ${phone3}
    Then disconnect the call from ${phone3}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetailsPKM} and softkey position 1
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetailsPKM} and softkey position 3
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetailsPKM} and softkey position 7

753811:BCA1 on BB calls A, own line on phone calls B, uses conf to join to BCA1
    [Tags]    Owner:AbhishekPathak    Reviewer:    bca    sixteenth
    [Setup]    Telephony Feature Custom Setup
    &{createBCAExtension1} =  Create Dictionary    name=pathak_bca1   backupExtn=${phone3}    switch=2    callStackDepth=2    forwardAfter=2    callStackFull=${EMPTY}   noAnswer=${EMPTY}    outboundCallerID=${EMPTY}    allowBridgeConferencing=true   defaultPrivacySettings=0
    &{createBCAExtension2} =  Create Dictionary    name=pathak_bca2   backupExtn=${phone3}    switch=2    callStackDepth=2    forwardAfter=2    callStackFull=${EMPTY}   noAnswer=${EMPTY}    outboundCallerID=${EMPTY}    allowBridgeConferencing=true   defaultPrivacySettings=0
    ${bcaExtn1}=    using ${bossPortal} I want to create Bridge Call Appearance extension using ${createBCAExtension1}
    ${bcaExtn2}=    using ${bossPortal} I want to create Bridge Call Appearance extension using ${createBCAExtension2}
    &{BCAdetails1} =  Create Dictionary    user_extension=${phone1}    button_box=1    soft_key=3    function=Bridge Call Appearance    label=BCA1    target_extension=${bcaExtn1}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${phone3}     show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=${EMPTY}
    &{BCAdetails2} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=4    function=Bridge Call Appearance    label=BCA2    target_extension=${bcaExtn2}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${phone3}     show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=${EMPTY}
    Given using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails1}
    Then using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails2}
    Then I want to press PKM line key ${programKey4} on ${phone1}
    Then on ${phone1} enter number ${phone2}
    Then on ${phone2} wait for 5 seconds
    Then answer the call on ${phone2} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then i want to make a two party call between ${phone1} and ${phone3} using ${line1}
    Then answer the call on ${phone3} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone3}
    Then on ${phone1} press the softkey ${conference} in ConferenceCallState
    Then I want to press PKM line key ${programKey4} on ${phone1}
    Then conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then disconnect the call from ${phone1}
    Then disconnect the call from ${phone3}
    Then on ${phone1} wait for 5 seconds

    Then I want to press PKM line key ${programKey4} on ${phone1}
    Then on ${phone1} enter number ${phone2}
    Then on ${phone2} wait for 5 seconds
    Then answer the call on ${phone2} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} enter number ${phone3}
    Then on ${phone3} wait for 5 seconds
    Then answer the call on ${phone3} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone3}
    Then on ${phone1} press the softkey ${conference} in ConferenceCallState
    Then I want to press PKM line key ${programKey4} on ${phone1}
    Then conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then disconnect the call from ${phone1}
    Then disconnect the call from ${phone3}
    Then on ${phone1} wait for 5 seconds
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetailsPKM} and softkey position 3
    [Teardown]    BCA Custom Teardown

759730: Page, ParknPage_PKM
    [Tags]    Owner: Abhishek Pathak    Reviewer:    pkm_page_parkpage    sixteenth
    Given using ${bossPortal} I program ${page} on ${phone1} using ${bossDetailsPKM} and extension of ${phone2} and softkey position 3 with noextensionValue
    Then verify display message Page on PKM for ${phone1}
    Then I want to press PKM line key ${programKey4} on ${phone1}
    Then on ${phone1} verify the softkeys in ${IdleState}
    Then on ${phone1} wait for 5 seconds
    Then using ${bossPortal} I program ${parknpage} on ${phone1} using ${bossDetailsPKM} and extension of ${phone2} and softkey position 4 with extensionValue
    Then verify display message Park and Pag on PKM for ${phone1}
    Then I want to press PKM line key ${programKey5} on ${phone1}
    Then on ${phone1} verify the softkeys in ${IdleState}
    Then using ${bossPortal} remove the function key on ${phone1} using ${bossDetailsPKM} and softkey position 3
    Then using ${bossPortal} remove the function key on ${phone1} using ${bossDetailsPKM} and softkey position 4

753328: Conf allowed - hold on remote phone - barge in
    [Tags]    Owner:AbhishekPathak    Reviewer:    bca    sixteenth
    [Setup]    Telephony Feature Custom Setup
    &{createBCAExtension1} =  Create Dictionary    name=bca_ap   backupExtn=${phone3}    switch=2    callStackDepth=4    allowBridgeConferencing=true   defaultPrivacySettings=0
    ${bcaExtn}=    using ${bossPortal} I want to create Bridge Call Appearance extension using ${createBCAExtension1}
    &{BCAdetails1} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=4    function=Bridge Call Appearance    label=BCA    target_extension=${bcaExtn}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${EMPTY}     show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=${EMPTY}
    &{BCAdetails2} =  Create Dictionary    user_extension=${phone2}    button_box=0    soft_key=4    function=Bridge Call Appearance    label=BCA    target_extension=${bcaExtn}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${EMPTY}     show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=${EMPTY}
    Given using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails1}
    Given using ${bossPortal} I want to create bca on ${phone2} using ${BCAdetails2}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} enter number ${phone3}
    Then on ${phone3} wait for 5 seconds
    Then answer the call on ${phone3} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone3}
    Then On ${phone1} verify the led state of ${line5} as ${on} and led color as ${blue}
    Then On ${phone2} verify the led state of ${line5} as ${on} and led color as ${orange}
    Then press hardkey as ${holdstate} on ${phone3}
    Then On ${phone2} verify the led state of ${line5} as ${on} and led color as ${orange}
    Then on ${phone1} verify ${line5} icon state as ${bcaRemoteHold}
    Then I want to use fac ${barge} on ${phone2} to ${phone3}
    Then on ${phone2} verify display message ${notPermittedOnThisCall}
    Then press softkey ${cancel} on ${phone1}
    Then on ${phone3} wait for 2 seconds
    Then press hardkey as ${holdstate} on ${phone3}
    Then on ${phone2} wait for 2 seconds
    Then I want to press line key ${programKey5} on phone ${phone2}
    Then conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then disconnect the call from ${phone3}
    Then disconnect the call from ${phone1}
    [Teardown]    BCA Custom Teardown

753590: A calls boss, Admin answers, B calls boss, admin answers, Admin joins, Admin attempts transfer to C.
    [Tags]    Owner:AbhishekPathak    Reviewer:    bca    sixteenth
    [Setup]    Telephony Feature Custom Setup
    &{telephonydetails} =  Create Dictionary    sca_enabled=True
    ${scaExtn} =  using ${bossPortal} on ${phone2} I want to enable SCA using ${telephonydetails}
    &{createBCAExtension} =  Create Dictionary    extension=${scaExtn}    backupExtn=${phone4}    allowBridgeConferencing=true   defaultPrivacySettings=0
    ${bcaExtn}=    using ${bossPortal} I want to modify Bridge Call Appearance extension using ${createBCAExtension}
    &{BCAdetails1} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=3    function=Bridge Call Appearance    label=BCA1    target_extension=${bcaExtn}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${EMPTY}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=${EMPTY}
    &{BCAdetails2} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=4    function=Bridge Call Appearance    label=BCA2    target_extension=${bcaExtn}    RingDelayBeforeAlert=0      CallStackPosition=2    DialExtension=${EMPTY}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=${EMPTY}
    Given using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails1}
    Given using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails2}
    Then i want to make a two party call between ${phone3} and ${phone2} using ${loudspeaker}
    Then on ${phone1} wait for 5 seconds
    Then I want to press line key ${programKey4} on phone ${phone1}
    Then Verify audio path between ${phone1} and ${phone3}
    Then Press hardkey as ${HoldState} on ${phone1}
    Then i want to make a two party call between ${phone4} and ${phone2} using ${loudspeaker}
    Then on ${phone1} wait for 5 seconds
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then Verify audio path between ${phone1} and ${phone4}
    Then on ${phone1} press the softkey ${conference} in ConferenceCallState
    Then on ${phone1} wait for 2 seconds
    Then I want to press line key ${programKey4} on phone ${phone1}
    Then conference call audio verify between ${phone1} ${phone3} and ${phone4}
    Then disconnect the call from ${phone3}
    Then disconnect the call from ${phone4}
    [Teardown]    Telephony Feature Custom Teardown

754759:Answer BCA-SCA call, hold, unhold
    [Tags]    Owner:AbhishekPathak    Reviewer:    bca    sixteenth
    [Setup]    BCA Custom Setup
    &{createBCAExtension} =  Create Dictionary    name=bca_ap   backupExtn=${phone3}    switch=2    callStackDepth=4    allowBridgeConferencing=true   defaultPrivacySettings=0
    ${bcaExtn}=    using ${bossPortal} I want to create Bridge Call Appearance extension using ${createBCAExtension}
    &{BCAdetails1} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=4    function=Bridge Call Appearance    label=BCA    target_extension=${bcaExtn}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${EMPTY}     show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=${EMPTY}
    &{BCAdetails2} =  Create Dictionary    user_extension=${phone2}    button_box=0    soft_key=4    function=Bridge Call Appearance    label=BCA    target_extension=${bcaExtn}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${EMPTY}     show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=${EMPTY}
    Given using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails1}
    Given using ${bossPortal} I want to create bca on ${phone2} using ${BCAdetails2}
    Then on ${phone3} enter number ${bcaExtn}
    Then on ${phone1} wait for 5 seconds
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then Verify audio path between ${phone1} and ${phone3}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} wait for 2 seconds
    Then verify the led state of ${line5} as ${blink} on ${phone1}
    Then verify the led state of ${line5} as ${blink} on ${phone2}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then Verify audio path between ${phone1} and ${phone3}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then verify the led state of ${line5} as ${blink} on ${phone1}
    Then verify the led state of ${line5} as ${blink} on ${phone2}
    Then disconnect the call from ${phone3}
    Then on ${phone1} verify the softkeys in ${idle}
    Then on ${phone2} verify the softkeys in ${idle}
    [Teardown]    BCA Custom Teardown

753527:Admin on call for boss, 2nd incoming to Boss to VM
    [Tags]    Owner:AbhishekPathak    Reviewer:    bca    sixteenth
    [Setup]    Telephony Feature Custom Setup
    Given Delete voicemail message on ${inbox} for ${phone2} using ${voicemailPassword}
    &{telephonydetails} =  Create Dictionary    sca_enabled=True
    ${scaExtn} =  using ${bossPortal} on ${phone2} I want to enable SCA using ${telephonydetails}
    &{createBCAExtension} =  Create Dictionary    extension=${scaExtn}    backupExtn=${phone4}    allowBridgeConferencing=true   defaultPrivacySettings=0
    ${bcaExtn}=    using ${bossPortal} I want to modify Bridge Call Appearance extension using ${createBCAExtension}
    &{BCAdetails} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=3    function=Bridge Call Appearance    label=BCA1    target_extension=${bcaExtn}    RingDelayBeforeAlert=0      CallStackPosition=2    DialExtension=${EMPTY}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=${EMPTY}
    Then using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails}
    Then i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then i want to make a two party call between ${phone3} and ${phone2} using ${loudspeaker}
    Then verify the led state of ${line4} as ${blink} on ${phone1}
    Then on ${phone2} press ${softKey} ${BottomKey2} for 1 times
    Then on ${phone3} wait for 20 seconds
    Then disconnect the call from ${phone3}
    Then disconnect the call from ${phone1}
    Then Login into voicemailBox for ${phone2} using ${voicemailPassword}
    Then Press hardkey as ${scrollRight} on ${phone2}
    Then Verify extension ${number} of ${phone3} on ${phone2}
    Then press hardkey as ${goodbye} on ${phone2}
    [Teardown]    Telephony Feature Custom Teardown

752467:Make Me Conference
    [Tags]    Owner:AbhishekPathak    Reviewer:    moh    sixteenth    notApplicableForMiCloud
    &{MOHFeatures}    CREATE DICTIONARY    option=1    fileName=MOH_50
    Given using ${bossPortal} I want to enable MOH features using ${MOHFeatures}
    Given using ${bossPortal} I want to modify usergroups MOH for ${executives_ap} with filename MOH_200
    Then i want to make a two party call between ${phone1} and ${phone2} using ${line1}
    Then answer the call on ${phone2} using ${offhook}
    Then Verify audio path between ${phone1} and ${phone2}
    Then on ${phone1} press the softkey ${conference} in answerstate
    Then on ${phone1} enter number ${phone3}
    Then verify MOH audio on ${phone2} for 50 frequency
    Then on ${phone1} press ${softKey} ${BottomKey2} for 1 times
    Then answer the call on ${phone3} using ${offhook}
    Then Verify no MOH audio on ${phone3}
    Then conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then on ${phone2} wait for 5 seconds
    Then on ${phone2} press the softkey ${conference} in answerstate
    Then on ${phone2} enter number ${phone4}
    Then on ${phone2} press ${softKey} ${BottomKey1} for 1 times
    Then answer the call on ${phone4} using ${offhook}
    Then Verify no MOH audio on ${phone3}
    Then on ${phone2} press ${softKey} ${BottomKey2} for 1 times
    Then four party conference call audio verification between ${phone1} ${phone2} ${phone3} and ${phone4}
    Then Press hardkey as ${HoldState} on ${phone1}
    Then Verify no MOH audio on ${phone2}
    Then Press hardkey as ${HoldState} on ${phone1}
    Then Verify no MOH audio on ${phone2}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}
    Then disconnect the call from ${phone4}
    &{MOHFeatures} =  Create Dictionary   option=0    fileName=MOH_50
    using ${bossPortal} I want to disable MOH features using ${MOHFeatures}

752870:Blind Transfer loops back to original extension during a Huntgroup transfer
    [Tags]    Owner:AbhishekPathak    Reviewer:    huntgroup    sixteenth
    [Setup]    Hunt Group Custom Setup
    @{members}   Create List    ${phone3}    ${phone4}    ${phone2}
    &{huntGroupDetails} =  Create Dictionary    BackupExtension=${phone5}    GroupMembers=${members}   GroupName=HG_AP   IncludeInSystem=True    MakeExtnPrivate=False    HuntPattern=1    RingsPerMember=2    NoAnswerRings=9    CallMemberWhenForwarding=True    SkipMemberOnCall=True    CallStackFull=${EMPTY}    NoAnswer=${EMPTY}
    ${HGExtension} =     using ${bossPortal} I want to create hunt group user extension with ${huntGroupDetails}
    Given i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then on ${phone2} press ${softKey} ${BottomKey3} for 1 times
    Then on ${phone2} dial number ${HGExtension}
    Then on ${phone2} press ${softKey} ${BottomKey1} for 1 times
    Then On ${phone1} verify display message ${HGExtension}
    Then Verify extension ${number} of ${phone1} on ${phone3}
    Then on ${phone4} wait for 10 seconds
    Then Verify extension ${number} of ${phone1} on ${phone4}
    Then on ${phone2} wait for 10 seconds
    Then Verify extension ${number} of ${phone1} on ${phone2}
    Then on ${phone3} wait for 15 seconds
    Then answer the call on ${phone3} using ${loudspeaker}
    Then Verify extension ${number} of ${phone1} on ${phone3}
    Then Verify extension ${number} of ${phone3} on ${phone1}
    Then Verify audio path between ${phone1} and ${phone3}
    Then disconnect the call from ${phone1}
    Then using ${bossPortal} I want to remove hunt group user extension ${HGExtension}
    [Teardown]    Hunt Group Custom Teardown

753699:SCA - Admin1 BCA Calls A, Admin2 Calls B, Admin2 joins.
    [Tags]    Owner:AbhishekPathak    Reviewer:    bca    sixteenth
    [Setup]    Telephony Feature Custom Setup
    &{telephonydetails} =  Create Dictionary    sca_enabled=True
    ${scaExtn} =  using ${bossPortal} on ${phone2} I want to enable SCA using ${telephonydetails}
    &{createBCAExtension} =  Create Dictionary    extension=${scaExtn}    backupExtn=${phone4}    allowBridgeConferencing=true   defaultPrivacySettings=0
    ${bcaExtn}=    using ${bossPortal} I want to modify Bridge Call Appearance extension using ${createBCAExtension}
    &{BCAdetails1} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=4    function=Bridge Call Appearance    label=BCA    target_extension=${bcaExtn}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${EMPTY}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=${EMPTY}
    &{BCAdetails2} =  Create Dictionary    user_extension=${phone3}    button_box=0    soft_key=4    function=Bridge Call Appearance    label=BCA    target_extension=${bcaExtn}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${EMPTY}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=${EMPTY}
    Given using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails1}
    Given using ${bossPortal} I want to create bca on ${phone3} using ${BCAdetails2}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} enter number ${phone4}
    Then on ${phone3} wait for 5 seconds
    Then answer the call on ${phone4} using ${loudspeaker}
    Then Verify audio path between ${phone1} and ${phone4}
    Then i want to make a two party call between ${phone3} and ${phone5} using ${line1}
    Then answer the call on ${phone5} using ${loudspeaker}
    Then Verify audio path between ${phone3} and ${phone5}
    Then on ${phone3} press ${softKey} ${BottomKey2} for 1 times
    Then I want to press line key ${programKey5} on phone ${phone3}
    Then conference call audio verify between ${phone1} ${phone4} and ${phone5}
    Then disconnect the call from ${phone4}
    Then disconnect the call from ${phone5}
    [Teardown]    Telephony Feature Custom Teardown


754447:XMON, CID Always - multiple incoming calls on target
    [Tags]    Owner:AbhishekPathak    Reviewer:    xmom    sixteenth
    &{extensionDetails} =    Create Dictionary    ring_delay=dont_ring    show_caller_id=always    no_connected=dial_number    with_connected=dial_number    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${monitorExtension} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 4 with ExtensionValue
    Then Delete voicemail message on ${inbox} for ${phone2} using ${voicemailPassword}
    Then on ${phone3} wait for 5 seconds
    Then Set number of rings to ${increasering} on ${phone2}
    Then Set number of rings to ${increasering} on ${phone3}
    Then Set number of rings to ${increasering} on ${phone4}
    Then Set number of rings to ${increasering} on ${phone5}
    Then i want to make a two party call between ${phone3} and ${phone2} using ${line1}
    Then i want to make a two party call between ${phone4} and ${phone2} using ${line1}
    Then i want to make a two party call between ${phone5} and ${phone2} using ${line1}
    Then verify the led state of ${line5} as ${blink} on ${phone1}
    Then on ${phone1} verify ${line5} icon state as ${xmonRinging}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then Verify extension ${number} of ${phone3} on ${phone1}
    Then on ${phone1} verify display message ${answer}
    Then on ${phone1} verify display message To Vm
    Then on ${phone1} verify display message ${cancel}
    Then on ${phone1} press ${softKey} ${BottomKey4} for 3 times
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then Press hardkey as ${scrolldown} on ${phone1}
    Then Verify extension ${number} of ${phone4} on ${phone1}
    Then on ${phone1} press ${softKey} ${BottomKey2} for 1 times
    Then I want to verify on ${phone2} negative display message ${phone4}
    Then Press hardkey as ${scrolldown} on ${phone1}
    Then on ${phone1} press ${softKey} ${BottomKey1} for 1 times
    Then Verify extension ${number} of ${phone5} on ${phone1}
    Then verify the led state of ${line5} as ${blink} on ${phone1}
    Then on ${phone1} verify ${line5} icon state as ${xmonBusy}
    Then I want to verify on ${phone2} negative display message ${answer}
    Then I want to verify on ${phone2} negative display message To Vm
    Then disconnect the call from ${phone3}
    Then disconnect the call from ${phone5}
    Then disconnect the call from ${phone4}
    Then Login into voicemailBox for ${phone2} using ${voicemailPassword}
    Then Press hardkey as ${scrollRight} on ${phone2}
    Then Verify extension ${number} of ${phone4} on ${phone2}
    Then press hardkey as ${goodbye} on ${phone2}
    Then Set number of rings to ${decreasering} on ${phone2}
    Then Set number of rings to ${decreasering} on ${phone3}
    Then Set number of rings to ${decreasering} on ${phone4}
    Then Set number of rings to ${decreasering} on ${phone5}

754753:TC03: PickupUnpark prog button to pick up a Hunt Group or Work Group
    [Tags]    Owner:AbhishekPathak    Reviewer:    huntgroup    seventeenth
    [Setup]    Hunt Group Custom Setup
    @{members}   Create List    ${phone3}
    &{huntGroupDetails} =  Create Dictionary    BackupExtension=${phone3}    GroupMembers=${members}   GroupName=HG_AP   IncludeInSystem=True    MakeExtnPrivate=False    HuntPattern=4    RingsPerMember=2    NoAnswerRings=4    CallMemberWhenForwarding=True    SkipMemberOnCall=True    CallStackFull=${EMPTY}    NoAnswer=${EMPTY}
    ${HGExtension} =     using ${bossPortal} I want to create hunt group user extension with ${huntGroupDetails}
    Given using ${bossPortal} I program ${pickupUnpark} on ${phone1} using ${bossDetails} and extension of ${HGExtension} and softkey position 4 with extensionValue
    Then on ${phone1} verify display message ${pickAndUnpar}
    Then on ${phone2} dial number ${HGExtension}
    Then on ${phone2} verify display message ${huntGroupDetails['GroupName']}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then Verify audio path between ${phone1} and ${phone2}
    Then disconnect the call from ${phone2}
    Then using ${bossPortal} I want to remove hunt group user extension ${HGExtension}
    [Teardown]    Hunt Group Custom Teardown

754240:TC01: Press Dial Mailbox button, destination not configured
    [Tags]    Owner:AbhishekPathak    Reviewer:    dialmailbox    seventeenth
    Given using ${bossPortal} I program ${dialmailbox} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with noExtensionValue
    Then on ${phone1} verify display message ${dialmailbox}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} verify display message >
    Then on ${phone1} enter number ${phone2}
    Then on ${phone1} wait for 2 seconds
    Then on ${phone1} verify display message ${displayVoiceMail}
    Then On ${phone1} verify ${line1} icon state as ${callAppearanceActive}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then on ${phone1} wait for 15 seconds
    Then disconnect the call from ${phone1}
    Then Login into voicemailBox for ${phone2} using ${voicemailPassword}
    Then Press hardkey as ${scrollRight} on ${phone2}
    Then Verify extension ${number} of ${phone1} on ${phone2}
    Then press hardkey as ${goodbye} on ${phone2}

755402:From Directory, select a user with multiple numbers press Dial
    [Tags]    Owner:AbhishekPathak    Reviewer:    directory    seventeenth
    Given On ${phone1} press directory and ${details} of ${phone2}
    Then press hardkey as ${scrolldown} on ${phone1}
    Then Verify extension ${number} of ${phone2} on ${phone1}
    Then on ${phone1} press the softkey ${dial} in DialingState
    Then Verify extension ${number} of ${phone1} on ${phone3}
    Then disconnect the call from ${phone1}
    Then on ${phone1} wait for 2 seconds
    Then On ${phone1} verify the softkeys in ${idle}

754922:TC002 Transfer Intercom - phone presses Cancel on Intercom
    [Tags]    Owner:AbhishekPathak    Reviewer:    transferintercom    seventeenth
    Given using ${bossPortal} I program ${transferintercom} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with noExtensionValue
    Then On ${phone1} verify display message ${displayMessage['transferIntercom']}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then i want to press line key ${programkey5} on phone ${phone1}
    Then on ${phone1} enter number ${phone3}
    Then on ${phone1} Press ${softKey} ${bottomKey1} for 1 times
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then Verify the led state of speaker as ${on} on ${phone3}
    Then verify audio path between ${phone1} and ${phone3}
    Then on ${phone1} press the softkey ${drop} in AnswerState
    Then using ${phone1} pickup call of ${phone2} using ${pickup} and ${timeout}
    Then verify audio path between ${phone1} and ${phone2}
    Then disconnect the call from ${phone2}

754286:TC028 Press speed dial keys on PKM to make a call
    [Tags]    Owner:GAURAV    Reviewer:    PKM    754286    seventeenth
    Given using ${bossPortal} I program ${dialNumber} on ${phone1} using ${bossDetailsPKM} and extension of ${phone2} and softkey position 1 with extensionValue
    Then verify display message ${displayMessage['dialNumber']} on PKM for ${phone1}
    Then I want to press PKM line key ${programkey2} on ${phone1}
    Then verify extension ${number} of ${phone1} on ${phone2}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetailsPKM} and softkey position 1


755791: Regression - Reboot Phone, Password Change Checkbox=False
    [Tags]    Owner:GAURAV    Reviewer:    seventeenth    notApplicableForMiCloud
    [Setup]    Telephony Feature Custom Setup
    &{telephonydetails} =  Create Dictionary    VM_pwd_change_on_next_login=False
    Given using ${bossPortal} on ${phone1} I want to uncheck voicemail password on next login using ${telephonydetails}
    Then Reboot ${phone1}
    Then I want to verify on ${phone1} negative display message ${newVoiceMailPasswordDisplay}
    [Teardown]    Set Default Voicemail Password


755792: Regression - Reboot Phone, Password Change Checkbox=True
    [Tags]    Owner:GAURAV    Reviewer:    755792    seventeenth    notApplicableForMiCloud
    [Setup]    Telephony Feature Custom Setup
    &{telephonydetails} =  Create Dictionary    VM_pwd_change_on_next_login=True
    Given using ${bossPortal} on ${phone1} I want to check voicemail password on next login using ${telephonydetails}
    Then Reboot ${phone1}
    Then I want to verify on ${phone1} negative display message ${voiceMailLoginScreenDisplay}
    [Teardown]    Set Default Voicemail Password


753760: Admin has meetme on BCA line, Calls boss on boss2 line, joins.
    [Tags]    Owner:GAURAV    Reviewer:    753761    seventeenth
    [Setup]    Telephony Feature Custom Setup
    &{telephonydetails} =  Create Dictionary    sca_enabled=True
    ${scaExtn1} =  using ${bossPortal} on ${phone2} I want to enable SCA using ${telephonydetails}
    &{telephonydetails} =  Create Dictionary    sca_enabled=True
    ${scaExtn2} =  using ${bossPortal} on ${phone3} I want to enable SCA using ${telephonydetails}
    &{BCAdetails} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=4    function=Bridge Call Appearance    label=BCA1    target_extension=${scaExtn1}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${phone2}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=Dial tone
    Given using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails}
    &{BCAdetails} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=5    function=Bridge Call Appearance    label=BCA2    target_extension=${scaExtn2}    RingDelayBeforeAlert=0      CallStackPosition=2    DialExtension=${phone2}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=Dial tone
    Given using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails}
    Then on ${phone1} verify display message BCA1
    Then on ${phone1} verify display message BCA2
    Then I want to press line key ${line4} on phone ${phone1}
    Then on ${phone1} Press ${softKey} ${bottomKey3} for 1 times
    Then on ${phone1} enter number ${accessCode}
    Then on ${phone4} Press ${softKey} ${bottomKey3} for 1 times
    Then on ${phone4} enter number ${accessCode}
    Then on ${phone5} Press ${softKey} ${bottomKey3} for 1 times
    Then on ${phone5} enter number ${accessCode}
    Then on ${phone6} Press ${softKey} ${bottomKey3} for 1 times
    Then on ${phone6} enter number ${accessCode}
    Then on ${phone7} Press ${softKey} ${bottomKey3} for 1 times
    Then on ${phone7} enter number ${accessCode}
    Then I want to press line key ${line5} on phone ${phone1}
    Then on ${phone1} dial number ${scaExtn2}
    Then on ${phone3} Press ${softKey} ${bottomKey1} for 1 times
    Then on ${phone1} Press ${softKey} ${bottomKey3} for 1 times
    Then I want to press line key ${line4} on phone ${phone1}
    Then On ${phone3} verify display message ${conferenceExt}
    Then disconnect the call from ${phone1}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}
    Then disconnect the call from ${phone4}
    Then disconnect the call from ${phone5}
    Then disconnect the call from ${phone6}
    [Teardown]    Telephony Feature Custom Teardown


753761: Admin has meetme on BCA line, Calls boss on own line, joins.
    [Tags]    Owner:GAURAV    Reviewer:    seventeenth
    [Setup]    TELEPHONY FEATURE CUSTOM SETUP
    &{telephonydetails} =  Create Dictionary    sca_enabled=True
    ${scaExtn} =  using ${bossPortal} on ${phone2} I want to enable SCA using ${telephonydetails}
    &{BCAdetails} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=3    function=Bridge Call Appearance    label=BCA    target_extension=${scaExtn}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${phone2}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=Dial tone
    Given using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails}
    Then on ${phone1} verify display message BCA
    Then I want to press line key ${line4} on phone ${phone1}
    Then on ${phone1} Press ${softKey} ${bottomKey3} for 1 times
    Then on ${phone1} enter number ${accessCode}
    Then on ${phone3} Press ${softKey} ${bottomKey3} for 1 times
    Then on ${phone3} enter number ${accessCode}
    Then on ${phone4} Press ${softKey} ${bottomKey3} for 1 times
    Then on ${phone4} enter number ${accessCode}
    Then on ${phone5} Press ${softKey} ${bottomKey3} for 1 times
    Then on ${phone5} enter number ${accessCode}
    Then on ${phone6} Press ${softKey} ${bottomKey3} for 1 times
    Then on ${phone6} enter number ${accessCode}
    Then i want to press line key ${line1} on phone ${phone1}
    Then on ${phone1} dial number ${scaExtn}
    tHEN On ${phone1} Wait for 3 seconds
    Then on ${phone2} Press ${softKey} ${bottomKey1} for 1 times
    Then on ${phone1} Press ${softKey} ${bottomKey3} for 1 times
    Then I want to press line key ${line4} on phone ${phone1}
    Then On ${phone2} verify display message ${conferenceExt}
    Then disconnect the call from ${phone1}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}
    Then disconnect the call from ${phone4}
    Then disconnect the call from ${phone5}
    [Teardown]    Telephony Feature Custom Teardown

753830:Transfers - Consultative transfer from BCA w Phone
    [Tags]    Owner:GAURAV    Reviewer:    753830    seventeenth
    [Setup]    BCA Custom Setup
    &{createBCAExtension1} =  Create Dictionary    name=bca_gaurav   backupExtn=${phone4}    switch=2    callStackDepth=1    forwardAfter=2    callStackFull=${EMPTY}   noAnswer=${EMPTY}    outboundCallerID=${EMPTY}    allowBridgeConferencing=true   defaultPrivacySettings=0
    ${bcaExtn1}=    using ${bossPortal} I want to create Bridge Call Appearance extension using ${createBCAExtension1}
    &{createBCAExtension2} =  Create Dictionary    name=bca_gaurav1   backupExtn=${phone4}    switch=2    callStackDepth=1    forwardAfter=2    callStackFull=${EMPTY}   noAnswer=${EMPTY}    outboundCallerID=${EMPTY}    allowBridgeConferencing=true   defaultPrivacySettings=0
    ${bcaExtn2}=    using ${bossPortal} I want to create Bridge Call Appearance extension using ${createBCAExtension2}
    &{BCAdetails1} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=4    function=Bridge Call Appearance    label=BCA1    target_extension=${bcaExtn1}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${EMPTY}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=${EMPTY}
    &{BCAdetails2} =  Create Dictionary    user_extension=${phone2}    button_box=0    soft_key=4    function=Bridge Call Appearance    label=BCA2    target_extension=${bcaExtn2}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${EMPTY}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=${EMPTY}
    Given using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails1}
    Then on ${phone1} verify display message BCA1
    Then using ${bossPortal} I want to create bca on ${phone2} using ${BCAdetails2}
    Then on ${phone2} verify display message BCA2
    Then on ${phone3} dial number ${bcaExtn1}
    Then i want to press line key ${programkey5} on phone ${phone1}
    Then verify the led state of ${programkey5} as ${on} on ${phone1}
    Then Verify audio path between ${phone3} and ${phone1}
    Then on ${phone1} Press ${softKey} ${bottomKey2} for 1 times
    Then on ${phone1} enter number ${phone2}
    Then on ${phone1} Press ${softKey} ${bottomKey1} for 1 times
    Then verify ringing state on ${phone1} and ${phone2}
    Then verify the led state of ${programkey5} as ${blink} on ${phone1}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then on ${phone1} Press ${softKey} ${bottomKey2} for 1 times
    Then Verify audio path between ${phone3} and ${phone2}
    Then verify the led state of ${programkey5} as ${off} on ${phone2}
    [Teardown]    BCA Custom Teardown

759709:Press Hotline speed dial button while on active call
    [Tags]    Owner:GAURAV    Reviewer:    759709    seventeenth
    &{hotlines}    CREATE DICTIONARY    ConnectedCallFunctionID=dial number    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program Hotline on ${phone1} using ${hotlines} and extension of ${phone2} and softkey position 4 with extensionValue
    Then on ${phone1} verify display message ${hotline}
    Then i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then on ${phone1} verify display message 00
    Then Verify audio path between ${phone1} and ${phone2}
    Then i want to press line key ${praogramkey5} on phone ${phone1}
    Then On ${phone1} verify ${line1} icon state as ${callAppearanceLocalHold}
    Then On ${phone1} verify ${line1} icon state as ${callAppearanceRemoteHold}
    Then disconnect the call from ${phone1}
    Then disconnect the call from ${phone2}

753550:Boss stack 1 on call and another comes in Phone
    [Tags]    Owner:GAURAV    Reviewer:    753550    seventeenth
    [Setup]    TELEPHONY FEATURE CUSTOM SETUP
    &{telephonydetails} =  Create Dictionary    sca_enabled=True        CallStackDepth=1
    ${scaExtn} =  using ${bossPortal} on ${phone1} I want to enable SCA using ${telephonydetails}
    &{createBCAExtension} =  Create Dictionary    extension=${scaExtn}    backupExtn=${phone2}    allowBridgeConferencing=true   defaultPrivacySettings=0
    ${bcaExtn}=    using ${bossPortal} I want to modify Bridge Call Appearance extension using ${createBCAExtension}
    Given i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then on ${phone3} dial number ${scaExtn}
    Then on ${phone3} wait for 5 seconds
    Then on ${phone3} verify display message ${displayVoiceMail}
    Then disconnect the call from ${phone2}
    And disconnect the call from ${phone3}
    [Teardown]    Telephony Feature Custom Teardown


759577: Prog Button Intercom Conference (Destination NOT configured)
    [Tags]    Owner:GAURAV    Reviewer:        759577    seventeenth
    &{extensionDetails} =  Create Dictionary   account_name=Automation    part_name=SC1    button_box=1
    Given using ${bossPortal} I program ${intercom} on ${phone1} using ${extensionDetails} and extension of ${phone2} and softkey position 4 with noExtensionValue
    Then i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then I want to press PKM line key ${programkey5} on ${phone1}
    Then on ${phone1} dial number ${phone3}
    Then on ${phone1} Press ${softKey} ${bottomKey1} for 1 times
    Then on ${phone1} verify display message ${conference}
    Then on ${phone1} verify display message ${cancel}
    Then on ${phone1} Press ${softKey} ${bottomKey2} for 1 times
    Then conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then disconnect the call from ${phone1}
    And disconnect the call from ${phone2}

754402: Implicit monitoring (with VM)
    [Tags]    Owner:GAURAV    Reviewer:        754402    seventeenth
    Given using ${bossPortal} I program ${dialMailbox} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['dialMailbox']}
    Then On ${phone2} verify the softkeys in ${idle}
    Then verify the led state of ${line5} as ${off} on ${phone1}
    Then on ${phone2} navigate to ${availability} settings
    Then Modify call handler mode on ${phone2} to ${always} in ${doNotDisturb}
    Then on ${phone2} Press ${softKey} ${bottomKey1} for 1 times
    Then press hardkey as ${goodBye} on ${phone2}
    Then On ${phone1} verify the led state of ${line5} as ${on} and led color as ${red}
    Then on ${phone1} wait for 5 seconds
    Then Change the phone state to default state on ${phone2}
    Then verify the led state of ${line5} as ${off} on ${phone1}
    Then On ${phone1} verify the softkeys in ${idle}
    Then On ${phone2} verify the softkeys in ${idle}
    Then i want to make a two party call between ${phone3} and ${phone2} using ${loudSpeaker}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then On ${phone1} verify the led state of ${line5} as ${on} and led color as ${red}
    Then press hardkey as ${holdstate} on ${phone2}
    Then On ${phone1} verify the led state of ${line5} as ${on} and led color as ${red}
    Then put the linekey ${line1} of ${phone2} on ${unhold}
    Then disconnect the call from ${phone2}
    Then leave voicemail message from ${phone3} on ${phone2}
    Then On ${phone1} verify the led state of ${line5} as ${on} and led color as ${red}
    Then delete voicemail message on ${inbox} for ${phone2} using ${voicemailpassword}
    Then press hardkey as ${goodbye} on ${phone2}
    Given using ${bossPortal} I program ${transferToMailbox} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['transferToMailbox']}
    Then On ${phone2} verify the softkeys in ${idle}
    Then verify the led state of ${line5} as ${off} on ${phone1}
    Then on ${phone2} navigate to ${availability} settings
    Then Modify call handler mode on ${phone2} to ${always} in ${doNotDisturb}
    Then on ${phone2} Press ${softKey} ${bottomKey1} for 1 times
    Then press hardkey as ${goodBye} on ${phone2}
    Then On ${phone1} verify the led state of ${line5} as ${on} and led color as ${red}
    Then on ${phone1} wait for 5 seconds
    Then Change the phone state to default state on ${phone2}
    Then verify the led state of ${line5} as ${off} on ${phone1}
    Then On ${phone1} verify the softkeys in ${idle}
    Then On ${phone2} verify the softkeys in ${idle}
    Then i want to make a two party call between ${phone3} and ${phone2} using ${loudSpeaker}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then On ${phone1} verify the led state of ${line5} as ${on} and led color as ${red}
    Then press hardkey as ${holdstate} on ${phone2}
    Then On ${phone1} verify the led state of ${line5} as ${on} and led color as ${red}
    Then put the linekey ${line1} of ${phone2} on ${unhold}
    Then disconnect the call from ${phone2}
    Then leave voicemail message from ${phone3} on ${phone2}
    Then On ${phone1} verify the led state of ${line5} as ${on} and led color as ${red}
    Then delete voicemail message on ${inbox} for ${phone2} using ${voicemailpassword}
    Then press hardkey as ${goodbye} on ${phone2}
    [Teardown]    RUN KEYWORDS    Generic Test Teardown    Default Availability State


755818:Intercom does not display when set to Off in the cli
    [Tags]    Owner:GAURAV    Reviewer:    seventeenth
    Then i want to make a two party call between ${phone1} and ${phone2} using ${loudSpeaker}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then disconnect the call from ${phone2}
    Then Press the call history button on ${phone1} and folder ${All} and ${details}
    Then On ${phone1} verify display message ${dial}
    Then On ${phone1} verify display message ${intercom}
    Then On ${phone1} verify display message ${close}
    Then On ${phone1} verify display message ${dialVM}
    &{COSDetails} =  Create Dictionary    Name=${fullyFeatured}    AllowIntercomInitiation=False
    Then using ${bossPortal} I want to change telephony features values using ${COSDetails}
    Then on ${phone} wait for 3 seconds
    Then Press the call history button on ${phone1} and folder ${All} and ${details}
    Then On ${phone1} verify display message ${dial}
    Then On ${phone1} verify display message ${close}
    Then On ${phone1} verify display message ${dial}
    Then press hardkey as ${goodbye} on ${phone1}
    [Teardown]    CoS Features Custom Teardown


810825:Implicit monitoring (conferenceBlind)
    [Tags]    Owner:GAURAV    Reviewer:         conferenceBlind         810823    seventeenth
    Then using ${bossPortal} I program ${conferenceBlind} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 2 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['conferenceBlind']}
    Then On ${phone2} verify the softkeys in ${idle}
    Then verify the led state of ${line3} as ${off} on ${phone1}
    Then on ${phone2} navigate to ${availability} settings
    Then Modify call handler mode on ${phone2} to ${always} in ${doNotDisturb}
    Then on ${phone2} Press ${softKey} ${bottomKey1} for 1 times
    Then press hardkey as ${goodbye} on ${phone2}
    Then On ${phone1} verify the led state of ${line3} as ${on} and led color as ${red}
    Then on ${phone1} wait for 5 seconds
    Then Change the phone state to default state on ${phone2}
    Then verify the led state of ${line3} as ${off} on ${phone1}
    Then On ${phone1} verify the softkeys in ${idle}
    Then On ${phone2} verify the softkeys in ${idle}
    Then i want to make a two party call between ${phone3} and ${phone2} using ${loudSpeaker}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then On ${phone1} verify the led state of ${line3} as ${on} and led color as ${red}
    Then press hardkey as ${holdstate} on ${phone2}
    Then On ${phone1} verify the led state of ${line3} as ${on} and led color as ${red}
    Then put the linekey ${line1} of ${phone2} on ${unhold}
    Then disconnect the call from ${phone2}
    [Teardown]    RUN KEYWORDS    Generic Test Teardown    Default Availability State

810826:Implicit monitoring (ConferenceConsultative)
    [Tags]    Owner:GAURAV    Reviewer:         ConferenceConsultative             810823    seventeenth
    Then using ${bossPortal} I program ${ConferenceConsultative} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 2 with noExtensionValue
    Then On ${phone1} verify display message ${displayMessage["conferenceConsult"]}
    Then On ${phone2} verify the softkeys in ${idle}
    Then verify the led state of ${line3} as ${off} on ${phone1}
    Then on ${phone2} navigate to ${availability} settings
    Then Modify call handler mode on ${phone2} to ${always} in ${doNotDisturb}
    Then on ${phone2} Press ${softKey} ${bottomKey1} for 1 times
    Then press hardkey as ${goodbye} on ${phone2}
    Then On ${phone1} verify the led state of ${line3} as ${on} and led color as ${red}
    Then on ${phone1} wait for 5 seconds
    Then Change the phone state to default state on ${phone2}
    Then verify the led state of ${line3} as ${off} on ${phone1}
    Then On ${phone1} verify the softkeys in ${idle}
    Then On ${phone2} verify the softkeys in ${idle}
    Then i want to make a two party call between ${phone3} and ${phone2} using ${loudSpeaker}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then On ${phone1} verify the led state of ${line3} as ${on} and led color as ${red}
    Then press hardkey as ${holdstate} on ${phone2}
    Then On ${phone1} verify the led state of ${line3} as ${on} and led color as ${red}
    Then put the linekey ${line1} of ${phone2} on ${unhold}
    Then disconnect the call from ${phone2}
    [Teardown]    RUN KEYWORDS    Generic Test Teardown    Default Availability State

810827:Implicit monitoring (ConferenceIntercom)
    [Tags]    Owner:GAURAV    Reviewer:                 ConferenceIntercom              810823    seventeenth
    Then using ${bossPortal} I program ${ConferenceIntercom} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 2 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['conferenceIntercom']}
   Then On ${phone2} verify the softkeys in ${idle}
    Then verify the led state of ${line3} as ${off} on ${phone1}
    Then on ${phone2} navigate to ${availability} settings
    Then Modify call handler mode on ${phone2} to ${always} in ${doNotDisturb}
    Then on ${phone2} Press ${softKey} ${bottomKey1} for 1 times
    Then press hardkey as ${goodbye} on ${phone2}
    Then On ${phone1} verify the led state of ${line3} as ${on} and led color as ${red}
    Then on ${phone1} wait for 5 seconds
    Then Change the phone state to default state on ${phone2}
    Then verify the led state of ${line3} as ${off} on ${phone1}
    Then On ${phone1} verify the softkeys in ${idle}
    Then On ${phone2} verify the softkeys in ${idle}
    Then i want to make a two party call between ${phone3} and ${phone2} using ${loudSpeaker}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then On ${phone1} verify the led state of ${line3} as ${on} and led color as ${red}
    Then press hardkey as ${holdstate} on ${phone2}
    Then On ${phone1} verify the led state of ${line3} as ${on} and led color as ${red}
    Then put the linekey ${line1} of ${phone2} on ${unhold}
    Then disconnect the call from ${phone2}
    [Teardown]    RUN KEYWORDS    Generic Test Teardown    Default Availability State

810828: Implicit monitoring (intercom)
    [Tags]    Owner:GAURAV    Reviewer:             intercom                810823    seventeenth
    Then using ${bossPortal} I program ${intercom} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 2 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['intercom']}
   Then On ${phone2} verify the softkeys in ${idle}
    Then verify the led state of ${line3} as ${off} on ${phone1}
    Then on ${phone2} navigate to ${availability} settings
    Then Modify call handler mode on ${phone2} to ${always} in ${doNotDisturb}
    Then on ${phone2} Press ${softKey} ${bottomKey1} for 1 times
    Then press hardkey as ${goodbye} on ${phone2}
    Then On ${phone1} verify the led state of ${line3} as ${on} and led color as ${red}
    Then on ${phone1} wait for 5 seconds
    Then Change the phone state to default state on ${phone2}
    Then verify the led state of ${line3} as ${off} on ${phone1}
    Then On ${phone1} verify the softkeys in ${idle}
    Then On ${phone2} verify the softkeys in ${idle}
    Then i want to make a two party call between ${phone3} and ${phone2} using ${loudSpeaker}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then On ${phone1} verify the led state of ${line3} as ${on} and led color as ${red}
    Then press hardkey as ${holdstate} on ${phone2}
    Then On ${phone1} verify the led state of ${line3} as ${on} and led color as ${red}
    Then put the linekey ${line1} of ${phone2} on ${unhold}
    Then disconnect the call from ${phone2}
    [Teardown]    RUN KEYWORDS    Generic Test Teardown    Default Availability State

810829:Implicit monitoring (park)
    [Tags]    Owner:GAURAV    Reviewer:            park         810823    seventeenth
    Then using ${bossPortal} I program ${park} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 2 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['park']}
    Then On ${phone2} verify the softkeys in ${idle}
    Then verify the led state of ${line3} as ${off} on ${phone1}
    Then on ${phone2} navigate to ${availability} settings
    Then Modify call handler mode on ${phone2} to ${always} in ${doNotDisturb}
    Then on ${phone2} Press ${softKey} ${bottomKey1} for 1 times
    Then press hardkey as ${goodbye} on ${phone2}
    Then On ${phone1} verify the led state of ${line3} as ${on} and led color as ${red}
    Then on ${phone1} wait for 5 seconds
    Then Change the phone state to default state on ${phone2}
    Then verify the led state of ${line3} as ${off} on ${phone1}
    Then On ${phone1} verify the softkeys in ${idle}
    Then On ${phone2} verify the softkeys in ${idle}
    Then i want to make a two party call between ${phone3} and ${phone2} using ${loudSpeaker}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then On ${phone1} verify the led state of ${line3} as ${on} and led color as ${red}
    Then press hardkey as ${holdstate} on ${phone2}
    Then On ${phone1} verify the led state of ${line3} as ${on} and led color as ${red}
    Then put the linekey ${line1} of ${phone2} on ${unhold}
    Then disconnect the call from ${phone2}
    [Teardown]    RUN KEYWORDS    Generic Test Teardown    Default Availability State

810830:Implicit monitoring (parknPage)
    [Tags]    Owner:GAURAV    Reviewer:             parknPage              810823    eigteenth
    Then using ${bossPortal} I program ${parknPage} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 2 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['parknPage']}
    Then On ${phone2} verify the softkeys in ${idle}
    Then verify the led state of ${line3} as ${off} on ${phone1}
    Then on ${phone2} navigate to ${availability} settings
    Then Modify call handler mode on ${phone2} to ${always} in ${doNotDisturb}
    Then on ${phone2} Press ${softKey} ${bottomKey1} for 1 times
    Then press hardkey as ${goodbye} on ${phone2}
    Then On ${phone1} verify the led state of ${line3} as ${on} and led color as ${red}
    Then on ${phone1} wait for 5 seconds
    Then Change the phone state to default state on ${phone2}
    Then verify the led state of ${line3} as ${off} on ${phone1}
    Then On ${phone1} verify the softkeys in ${idle}
    Then On ${phone2} verify the softkeys in ${idle}
    Then i want to make a two party call between ${phone3} and ${phone2} using ${loudSpeaker}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then On ${phone1} verify the led state of ${line3} as ${on} and led color as ${red}
    Then press hardkey as ${holdstate} on ${phone2}
    Then On ${phone1} verify the led state of ${line3} as ${on} and led color as ${red}
    Then put the linekey ${line1} of ${phone2} on ${unhold}
    Then disconnect the call from ${phone2}
    [Teardown]    RUN KEYWORDS    Generic Test Teardown    Default Availability State

810831:Implicit monitoring (silentCoach)
    [Tags]    Owner:GAURAV    Reviewer:                     silentCoachFAC              810823    eigteenth
    Then using ${bossPortal} I program ${silentCoachFAC} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 2 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['silentcoach']}
    Then On ${phone2} verify the softkeys in ${idle}
    Then verify the led state of ${line3} as ${off} on ${phone1}
    Then on ${phone2} navigate to ${availability} settings
    Then Modify call handler mode on ${phone2} to ${always} in ${doNotDisturb}
    Then on ${phone2} Press ${softKey} ${bottomKey1} for 1 times
    Then press hardkey as ${goodbye} on ${phone2}
    Then On ${phone1} verify the led state of ${line3} as ${on} and led color as ${red}
    Then on ${phone1} wait for 5 seconds
    Then Change the phone state to default state on ${phone2}
    Then verify the led state of ${line3} as ${off} on ${phone1}
    Then On ${phone1} verify the softkeys in ${idle}
    Then On ${phone2} verify the softkeys in ${idle}
    Then i want to make a two party call between ${phone3} and ${phone2} using ${loudSpeaker}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then On ${phone1} verify the led state of ${line3} as ${on} and led color as ${red}
    Then press hardkey as ${holdstate} on ${phone2}
    Then On ${phone1} verify the led state of ${line3} as ${on} and led color as ${red}
    Then put the linekey ${line1} of ${phone2} on ${unhold}
    Then disconnect the call from ${phone2}
    [Teardown]    RUN KEYWORDS    Generic Test Teardown    Default Availability State

810832:Implicit monitoring (silentMonitor)
    [Tags]    Owner:GAURAV    Reviewer:    silentMonitorFAC    810823    eigteenth
    Then using ${bossPortal} I program ${silentMonitorFAC} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 2 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['Silentmonitor']}
    Then On ${phone2} verify the softkeys in ${idle}
    Then verify the led state of ${line3} as ${off} on ${phone1}
    Then on ${phone2} navigate to ${availability} settings
    Then Modify call handler mode on ${phone2} to ${always} in ${doNotDisturb}
    Then on ${phone2} Press ${softKey} ${bottomKey1} for 1 times
    Then press hardkey as ${goodbye} on ${phone2}
    Then On ${phone1} verify the led state of ${line3} as ${on} and led color as ${red}
    Then on ${phone1} wait for 5 seconds
    Then Change the phone state to default state on ${phone2}
    Then verify the led state of ${line3} as ${off} on ${phone1}
    Then On ${phone1} verify the softkeys in ${idle}
    Then On ${phone2} verify the softkeys in ${idle}
    Then i want to make a two party call between ${phone3} and ${phone2} using ${loudSpeaker}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then On ${phone1} verify the led state of ${line3} as ${on} and led color as ${red}
    Then press hardkey as ${holdstate} on ${phone2}
    Then On ${phone1} verify the led state of ${line3} as ${on} and led color as ${red}
    Then put the linekey ${line1} of ${phone2} on ${unhold}
    Then disconnect the call from ${phone2}
    [Teardown]    RUN KEYWORDS    Generic Test Teardown    Default Availability State

810833:Implicit monitoring (transferBlind)
    [Tags]    Owner:GAURAV    Reviewer:    transferBlind    810833    eigteenth
    Then using ${bossPortal} I program ${transferBlind} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 2 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['transferBlind']}
    Then On ${phone2} verify the softkeys in ${idle}
    Then verify the led state of ${line3} as ${off} on ${phone1}
    Then on ${phone2} navigate to ${availability} settings
    Then Modify call handler mode on ${phone2} to ${always} in ${doNotDisturb}
    Then on ${phone2} Press ${softKey} ${bottomKey1} for 1 times
    Then press hardkey as ${goodbye} on ${phone2}
    Then On ${phone1} verify the led state of ${line3} as ${on} and led color as ${red}
    Then on ${phone1} wait for 5 seconds
    Then Change the phone state to default state on ${phone2}
    Then verify the led state of ${line3} as ${off} on ${phone1}
    Then On ${phone1} verify the softkeys in ${idle}
    Then On ${phone2} verify the softkeys in ${idle}
    Then i want to make a two party call between ${phone3} and ${phone2} using ${loudSpeaker}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then On ${phone1} verify the led state of ${line3} as ${on} and led color as ${red}
    Then press hardkey as ${holdstate} on ${phone2}
    Then On ${phone1} verify the led state of ${line3} as ${on} and led color as ${red}
    Then put the linekey ${line1} of ${phone2} on ${unhold}
    Then disconnect the call from ${phone2}
    [Teardown]    RUN KEYWORDS    Generic Test Teardown    Default Availability State

810834:Implicit monitoring (Transfer Consultative)
    [Tags]    Owner:GAURAV    Reviewer:    Transfer Consultative    810834    eigteenth
    Then using ${bossPortal} I program ${Transfer Consultative} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 2 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['transferConsult']}
    Then On ${phone2} verify the softkeys in ${idle}
    Then verify the led state of ${line3} as ${off} on ${phone1}
    Then on ${phone2} navigate to ${availability} settings
    Then Modify call handler mode on ${phone2} to ${always} in ${doNotDisturb}
    Then on ${phone2} Press ${softKey} ${bottomKey1} for 1 times
    Then press hardkey as ${goodbye} on ${phone2}
    Then On ${phone1} verify the led state of ${line3} as ${on} and led color as ${red}
    Then on ${phone1} wait for 5 seconds
    Then Change the phone state to default state on ${phone2}
    Then verify the led state of ${line3} as ${off} on ${phone1}
    Then On ${phone1} verify the softkeys in ${idle}
    Then On ${phone2} verify the softkeys in ${idle}
    Then i want to make a two party call between ${phone3} and ${phone2} using ${loudSpeaker}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then On ${phone1} verify the led state of ${line3} as ${on} and led color as ${red}
    Then press hardkey as ${holdstate} on ${phone2}
    Then On ${phone1} verify the led state of ${line3} as ${on} and led color as ${red}
    Then put the linekey ${line1} of ${phone2} on ${unhold}
    Then disconnect the call from ${phone2}
    [Teardown]    RUN KEYWORDS    Generic Test Teardown    Default Availability State

810835:Implicit monitoring (transferIntercom)
    [Tags]    Owner:GAURAV    Reviewer:    transferIntercom    810835    eigteenth
    Then using ${bossPortal} I program ${transferIntercom} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 2 with noExtensionValue
    Then On ${phone1} verify display message ${displayMessage['transferIntercom']}
    Then On ${phone2} verify the softkeys in ${idle}
    Then verify the led state of ${line3} as ${off} on ${phone1}
    Then on ${phone2} navigate to ${availability} settings
    Then Modify call handler mode on ${phone2} to ${always} in ${doNotDisturb}
    Then on ${phone2} Press ${softKey} ${bottomKey1} for 1 times
    Then press hardkey as ${goodbye} on ${phone2}
    Then On ${phone1} verify the led state of ${line3} as ${on} and led color as ${red}
    Then on ${phone1} wait for 5 seconds
    Then Change the phone state to default state on ${phone2}
    Then verify the led state of ${line3} as ${off} on ${phone1}
    Then On ${phone1} verify the softkeys in ${idle}
    Then On ${phone2} verify the softkeys in ${idle}
    Then i want to make a two party call between ${phone3} and ${phone2} using ${loudSpeaker}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then On ${phone1} verify the led state of ${line3} as ${on} and led color as ${red}
    Then press hardkey as ${holdstate} on ${phone2}
    Then On ${phone1} verify the led state of ${line3} as ${on} and led color as ${red}
    Then put the linekey ${line1} of ${phone2} on ${unhold}
    Then disconnect the call from ${phone2}
    [Teardown]    RUN KEYWORDS    Generic Test Teardown    Default Availability State

810836:Implicit monitoring (transferWhisper)
    [Tags]    Owner:GAURAV    Reviewer:    transferWhisper    810836    eigteenth
    Then using ${bossPortal} I program ${transferWhisper} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 2 with noExtensionValue
    Then On ${phone1} verify display message ${displayMessage['transferToWhisper']}
    Then On ${phone2} verify the softkeys in ${idle}
    Then verify the led state of ${line3} as ${off} on ${phone1}
    Then on ${phone2} navigate to ${availability} settings
    Then Modify call handler mode on ${phone2} to ${always} in ${doNotDisturb}
    Then on ${phone2} Press ${softKey} ${bottomKey1} for 1 times
    Then press hardkey as ${goodbye} on ${phone2}
    Then On ${phone1} verify the led state of ${line3} as ${on} and led color as ${red}
    Then on ${phone1} wait for 5 seconds
    Then Change the phone state to default state on ${phone2}
    Then verify the led state of ${line3} as ${off} on ${phone1}
    Then On ${phone1} verify the softkeys in ${idle}
    Then On ${phone2} verify the softkeys in ${idle}
    Then i want to make a two party call between ${phone3} and ${phone2} using ${loudSpeaker}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then On ${phone1} verify the led state of ${line3} as ${on} and led color as ${red}
    Then press hardkey as ${holdstate} on ${phone2}
    Then On ${phone1} verify the led state of ${line3} as ${on} and led color as ${red}
    Then put the linekey ${line1} of ${phone2} on ${unhold}
    Then disconnect the call from ${phone2}
    [Teardown]    RUN KEYWORDS    Generic Test Teardown    Default Availability State

810837:Implicit monitoring (whisperPage)
    [Tags]    Owner:GAURAV    Reviewer:    whisperPage    810837    eigteenth
    Then using ${bossPortal} I program ${whisperPage} on ${phone1} using ${bossDetails} and extension of ${phone3} and softkey position 2 with noExtensionValue
    Then On ${phone1} verify display message ${displayMessage['whisperPage']}
    Then On ${phone2} verify the softkeys in ${idle}
    Then verify the led state of ${line3} as ${off} on ${phone1}
    Then on ${phone2} navigate to ${availability} settings
    Then Modify call handler mode on ${phone2} to ${always} in ${doNotDisturb}
    Then on ${phone2} Press ${softKey} ${bottomKey1} for 1 times
    Then press hardkey as ${goodbye} on ${phone2}
    Then On ${phone1} verify the led state of ${line3} as ${on} and led color as ${red}
    Then on ${phone1} wait for 5 seconds
    Then Change the phone state to default state on ${phone2}
    Then verify the led state of ${line3} as ${off} on ${phone1}
    Then On ${phone1} verify the softkeys in ${idle}
    Then On ${phone2} verify the softkeys in ${idle}
    Then i want to make a two party call between ${phone3} and ${phone2} using ${loudSpeaker}
    Then answer the call on ${phone2} using ${loudSpeaker}
    Then On ${phone1} verify the led state of ${line3} as ${on} and led color as ${red}
    Then press hardkey as ${holdstate} on ${phone2}
    Then On ${phone1} verify the led state of ${line3} as ${on} and led color as ${red}
    Then put the linekey ${line1} of ${phone2} on ${unhold}
    Then disconnect the call from ${phone2}
    [Teardown]    RUN KEYWORDS    Generic Test Teardown    Default Availability State

186380: TC004 Whisper Page/ Whisper Mute
    [Tags]    eigteenth
    Given using ${bossPortal} I program ${whisperPage} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${whisperPage}
    And using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4

254673:TC10-Progbutton Transfer Blind destination configured (call not answered)
    [Tags]    eigteenth
    Given using ${bossPortal} I program ${transferBlind} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['transferBlind']}
    Then On ${phone1} verify display message Pickup
    Then I want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then On ${phone1} verify display message Call Transferred
    Then Verify the Caller id on ${phone2} and ${phone3} display
    Then using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4
    Then Check Connection and disconnect the ${phone2}

254674:TC11-Progbutton Transfer Blind destination not configured (call not answered)
    [Tags]    eigteenth
    Given using ${bossPortal} I program Transfer Blind on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with noExtensionValue
    Then On ${phone1} verify display message Transfer Bli
    Then I want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then On ${phone1} verify display message Deflect
    Then On ${phone1} verify display message Backspace
    Then On ${phone1} verify display message Cancel
    Then Verify the Caller id on ${phone2} and ${phone3} display
    Then using ${bossPortal} remove the function key on ${phone1} using ${bossDetails} and softkey position 4
    Then Check Connection and disconnect the ${phone2}

247371:TC001 Prog Button Transfer Whisper (with extension)
    [Tags]    eigteenth
    Given using ${bossPortal} I program ${transferWhisper} on ${phone1} using ${bossDetails} and extension of ${phone2} and softkey position 4 with extensionValue
    Then On ${phone1} verify display message ${displayMessage['transferToWhisper']}
    Then I want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then Answer the call on ${phone1} using ${loudspeaker}
    Then I want to press line key ${programKey5} on phone ${phone1}
    Then on ${phone1} wait for 2 seconds
    Then on ${phone1} press ${softKey} ${bottomKey3} for 1 times
    Then verify the led state of ${line1} as ${blink} on ${phone2}


753460: Admin calls 2 parties and conf call. Hotline boss, Boss Joins, Admin drops, Boss locks& Unlocks, admin joins
    [Tags]    Owner:Milind    Reviewer:Vikhyat
    [Setup]    Telephony Feature Custom Setup
    &{telephonydetails}=  Create Dictionary    sca_enabled=True
    ${scaExtn} =  using ${bossPortal} on ${phone2} I want to enable SCA using ${telephonydetails}
    &{modifySCAExtension}=    CREATE DICTIONARY    extension=${scaExtn}   backupExtn=${phone3}    allowBridgeConferencing=true
    Given Using ${bossPortal} I want to modify Bridge Call Appearance extension using ${modifySCAExtension}

    &{BCAdetails}=    Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=2    function=Bridge Call Appearance    label=BCA    target_extension=${scaExtn}       CallStackPosition=1     allowBridgeConferencing=true
    Given using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails}
    Then On ${phone1} verify display message ${bca}

    &{hotlines}=    create dictionary    ConnectedCallFunctionID=intercom    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${hotline} on ${phone1} using ${hotlines} and extension of ${phone2} and softkey position 3 with ExtensionValue

    Then I want to make a two party call between ${phone1} and ${phone3} using ${programKey3}
    Then Answer the call on ${phone3} using ${offHook}
    Then I want to make a conference call between ${phone1},${phone3} and ${phone4} using ${consultiveConference}
    Then Conference call audio verify between ${phone1} ${phone3} and ${phone4}
    Then I want to press line key ${programKey4} on phone ${phone1}
    Then on ${phone1} wait for 10 seconds
    Then Verify extension ${number} of ${phone1} on ${phone2}
    Then Verify extension ${number} of ${phone2} on ${phone1}
    Then answer the call on ${phone1} using ${line2}
    Then On ${phone1} verify ${line3} icon state as ${callAppearanceActive}
    Then On ${phone2} verify ${line2} icon state as ${callAppearanceActive}
    Then I want to press line key ${programKey1} on phone ${phone2}
    Then on ${phone1} wait for 10 seconds
    Then On ${phone2} verify display message Conferenced 3 calls
    Then On ${phone3} verify display message Conferenced 3 calls
    Then On ${phone4} verify display message Conferenced 3 calls
    Then Conference call audio verify between ${phone2} ${phone3} and ${phone4}
    Then I want to press line key ${programKey4} on phone ${phone1}
    Then on ${phone1} wait for 2 seconds
    Then on ${phone1} press ${softkey} ${bottomKey1} for 1 times
    Then on ${phone1} wait for 2 seconds
    Then on ${phone1} press ${softkey} ${bottomKey1} for 1 times
    Then Disconnect the call from ${phone1}
    Then On ${phone2} press the softkey ${lock} in ConferenceCallState
    Then I want to press line key ${programKey3} on phone ${phone1}
    Then On ${phone1} verify display message Action not permitted
    Then Disconnect the call from ${phone2}
    Then Disconnect the call from ${phone3}
    Then Disconnect the call from ${phone4}
    [Teardown]    Telephony Feature Custom Teardown

753639: Admin makes 2 way conf on SCA line1, Admin SCA calls C, Boss picks up conf call, Admin joins
    [Tags]    Owner:Milind    Reviewer:Vikhyat
    [Setup]    Telephony Feature Custom Setup
    &{telephonydetails}=  Create Dictionary    sca_enabled=True
    ${scaExtn} =  using ${bossPortal} on ${phone2} I want to enable SCA using ${telephonydetails}
    &{modifySCAExtension}=    CREATE DICTIONARY    extension=${scaExtn}   backupExtn=${phone3}    allowBridgeConferencing=true
    Given Using ${bossPortal} I want to modify Bridge Call Appearance extension using ${modifySCAExtension}

    &{bcaDetails1}=  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=2    function=Bridge Call Appearance    label=${bca}1    target_extension=${scaExtn}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${EMPTY}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=${EMPTY}
    Given using ${bossPortal} I want to create bca on ${phone1} using ${bcaDetails1}
    Then On ${phone1} verify display message ${bca}1

    &{bcaDetails2}=  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=3    function=Bridge Call Appearance    label=${bca}2    target_extension=${scaExtn}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${EMPTY}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=${EMPTY}
    Given using ${bossPortal} I want to create bca on ${phone1} using ${bcaDetails2}
    Then On ${phone1} verify display message ${bca}2

    Then I want to make a two party call between ${phone1} and ${phone3} using ${programKey3}
    Then Answer the call on ${phone3} using ${offHook}
    Then I want to make a conference call between ${phone1},${phone3} and ${phone4} using ${consultiveConference}
    Then On ${phone1} verify ${line3} icon state as ${bcaLocalHold}
    Then Conference call audio verify between ${phone1} ${phone3} and ${phone4}
    Then Put the linekey ${line3} of ${phone1} on ${hold}
    Then On ${phone1} verify ${line3} icon state as ${bcaLocalHold}
    Then I want to press line key ${programKey1} on phone ${phone2}
    Then on ${phone1} wait for 5 seconds
    Then On ${phone1} verify ${line1} icon state as ${callAppearanceLocalHold}
    Then I want to make a two party call between ${phone1} and ${phone5} using ${programKey4}
    Then On ${phone1} press the softkey ${conference} in AnswerState
    Then I want to press line key ${programKey3} on phone ${phone1}
    Then on ${phone1} wait for 5 seconds
    Then on ${phone1} verify display message Conferenced 4 calls
    Then on ${phone2} verify display message Conferenced 4 calls
    Then on ${phone3} verify display message Conferenced 4 calls
    Then on ${phone4} verify display message Conferenced 4 calls
    Then Four party Conference call audio verification between ${phone1} ${phone2} ${phone3} and ${phone4}
    Then Disconnect the call from ${phone5}
    Then Disconnect the call from ${phone4}
    Then Disconnect the call from ${phone3}
    Then Disconnect the call from ${phone2}

    [Teardown]    Telephony Feature Custom Teardown

753642: Admin on 1 way makeme hangs up, no prompt
    [Tags]    Owner:Milind    Reviewer:Vikhyat
    [Setup]    Telephony Feature Custom Setup
    &{createBCAExtension} =  Create Dictionary    name=Milind1   backupExtn=${phone3}    switch=2    callStackDepth=2    forwardAfter=2    callStackFull=${EMPTY}   noAnswer=${EMPTY}    outboundCallerID=${EMPTY}    allowBridgeConferencing=true   defaultPrivacySettings=0
    ${bcaExtn}=    using ${bossPortal} I want to create Bridge Call Appearance extension using ${createBCAExtension}

    &{BCAdetails} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=3    function=Bridge Call Appearance    label=BCA    target_extension=${bcaExtn}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${phone2}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=Dial tone
    Given using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails}
    Then on ${phone1} verify display message BCA

    Then I want to make a two party call between ${phone1} and ${phone2} using ${programKey4}
    Then Answer the call on ${phone2} using ${loudspeaker}
    Then I want to make a conference call between ${phone1},${phone2} and ${phone3} using ${directConference}
    Then Add the ${phone4} in 3 parties conference call on ${phone1}
    Then on ${phone1} verify display message Conferenced 3 calls
    Then on ${phone2} verify display message Conferenced 3 calls
    Then on ${phone3} verify display message Conferenced 3 calls
    Then on ${phone4} verify display message Conferenced 3 calls
    Then Four party Conference call audio verification between ${phone1} ${phone2} ${phone3} and ${phone4}
    Then on ${phone1} press the softkey ${show} in ConferenceCallState
    Then verify extension ${number} of ${phone2} on ${phone1}
    Then verify extension ${number} of ${phone3} on ${phone1}
    Then verify extension ${number} of ${phone4} on ${phone1}
    Then Disconnect the call from ${phone1}
    #To Do -- need to add validation to verify "DO you want to keep managing this call once feature is available"
    Then Disconnect the call from ${phone2}
    Then Disconnect the call from ${phone3}
    Then Disconnect the call from ${phone4}

    Then I want to make a two party call between ${phone1} and ${phone2} using ${programKey1}
    Then Answer the call on ${phone4} using ${offHook}
    #Then On ${phone1} verify ${line1} icon state as ${callAppearanceLocalHold}
    Then I want to make a conference call between ${phone1},${phone2} and ${phone3} using ${directConference}
    Then Add the ${phone4} in 3 parties conference call on ${phone1}
    Then on ${phone1} verify display message Conferenced 3 calls
    Then on ${phone2} verify display message Conferenced 3 calls
    Then on ${phone3} verify display message Conferenced 3 calls
    Then on ${phone4} verify display message Conferenced 3 calls
    Then on ${phone1} press the softkey ${show} in ConferenceCallState
    Then verify extension ${number} of ${phone2} on ${phone1}
    Then verify extension ${number} of ${phone3} on ${phone1}
    Then verify extension ${number} of ${phone4} on ${phone1}
    Then Disconnect the call from ${phone1}
    #To Do -- need to add validation to verify "DO you want to keep managing this call"
    Then Disconnect the call from ${phone2}
    Then Disconnect the call from ${phone3}
    Then Disconnect the call from ${phone4}
    [Teardown]    Telephony Feature Custom Teardown

798946: Answer BCA-SCA call, hold, unhold
    [Tags]    Owner:Milind    Reviewer:Vikhyat
    [Setup]    Telephony Feature Custom Setup
    &{createBCAExtension} =  Create Dictionary    name=Milind1   backupExtn=${phone3}    switch=2    callStackDepth=2    forwardAfter=2    callStackFull=${EMPTY}   noAnswer=${EMPTY}    outboundCallerID=${EMPTY}    allowBridgeConferencing=true   defaultPrivacySettings=0
    ${bcaExtn}=    using ${bossPortal} I want to create Bridge Call Appearance extension using ${createBCAExtension}

    &{BCAdetails} =  Create Dictionary    user_extension=${phone1}    button_box=0    soft_key=3    function=Bridge Call Appearance    label=BCA    target_extension=${bcaExtn}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${EMPTY}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=Dial tone
    Given using ${bossPortal} I want to create bca on ${phone1} using ${BCAdetails}
    Then on ${phone1} verify display message BCA

    &{BCAdetails} =  Create Dictionary    user_extension=${phone2}    button_box=0    soft_key=3    function=Bridge Call Appearance    label=BCA    target_extension=${bcaExtn}    RingDelayBeforeAlert=0      CallStackPosition=1    DialExtension=${EMPTY}    show_caller_id_option=always    EnableAutoAnswerWhenRinging=True    SecondaryType=Dial tone
    Given using ${bossPortal} I want to create bca on ${phone2} using ${BCAdetails}
    Then on ${phone1} verify display message BCA

    Then on ${phone3} dial number ${bcaExtn}
    Then on ${phone3} wait for 5 seconds
    Then On ${phone1} verify ${line4} icon state as ${bcaIncomingCall}
    Then I want to press line key ${programKey4} on phone ${phone1}
    Then On ${phone1} verify ${line4} icon state as ${bcaActive}
    Then On ${phone2} verify ${line4} icon state as ${bcaActive}
    Then Verify the Caller id on ${phone1} and ${phone3} display
    Then Put the linekey ${line4} of ${phone1} on ${hold}
    Then on ${phone1} wait for 3 seconds
    Then On ${phone1} verify ${line4} icon state as ${bcaLocalHold}
    Then On ${phone2} verify ${line4} icon state as ${bcaLocalHold}
    Then put the linekey ${line4} of ${phone1} on ${unhold}
    Then on ${phone1} wait for 3 seconds
    Then On ${phone1} verify ${line4} icon state as ${bcaActive}
    Then On ${phone2} verify ${line4} icon state as ${bcaActive}
    Then Verify the Caller id on ${phone1} and ${phone3} display
    Then Put the linekey ${line4} of ${phone1} on ${hold}
    Then on ${phone1} wait for 3 seconds
    Then On ${phone1} verify ${line4} icon state as ${bcaLocalHold}
    Then On ${phone2} verify ${line4} icon state as ${bcaLocalHold}
    Then Disconnect the call from ${phone3}

    [Teardown]    Telephony Feature Custom Teardown

807245: Answer incoming calls via audio path buttons while there is existing held call
    [Tags]    Owner:Milind    Reviewer:Vikhyat
    [Setup]    Telephony Feature Custom Setup
    Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then verify ringing state on ${phone2} and ${phone1}
    Then On ${phone1} verify ${line1} icon state as ${callAppearanceIncoming}
    Then Answer the call on ${phone1} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then put the linekey ${line1} of ${phone1} on ${hold}
    Then On ${phone1} verify ${line1} icon state as ${callAppearanceLocalHold}
    Then verify no audio path from ${phone1} to ${phone2}
    Then verify no audio path from ${phone2} to ${phone1}
    Then I want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then I want to make a two party call between ${phone4} and ${phone1} using ${loudspeaker}
    Then On ${phone1} verify ${line2} icon state as ${callAppearanceIncoming}
    Then On ${phone1} verify ${line3} icon state as ${callAppearanceIncoming}
    Then Answer the call on ${phone1} using ${loudspeaker}
    Then On ${phone1} verify ${line2} icon state as ${callAppearanceActive}
    Then press hardkey as ${handsFree} on ${phone1}
    Then verify the led state of ${line2} as ${off} on ${phone1}
    Then press hardkey as ${handsFree} on ${phone1}
    Then press hardkey as ${handsFree} on ${phone1}
    Then verify the led state of ${line3} as ${off} on ${phone1}
    Then On ${phone3} verify the softkeys in ${idleState}
    And On ${phone4} verify the softkeys in ${idleState}
    Then Disconnect the call from ${phone2}
    [Teardown]    Telephony Feature Custom Teardow


754150: Program selected Button to CHM Extended Absence
    [Tags]    Owner:Milind    Reviewer:    Vikhyat    CHM
    &{extensionDetails} =    Create Dictionary    availability=Vacation
    Given Using ${bossPortal} I program ${changeAvailability} on ${phone1} using &{extensionDetails} and extension of ${phone2} and softkey position 3 with noExtensionValue
    Then On ${phone1} verify display message ${displayMessage['availabilityVacation']}
    Then I want to press line key ${programKey4} on phone ${phone1}
    Then on ${phone1} wait for 5 seconds
    Given On ${phone1} navigate to ${availability} settings
    Then On ${phone1} verify display message Vacation
    Then press hardkey as ${goodBye} on ${phone1}
    Then Verify ${availabilityVacation} state icon on ${phone1}
    And using ${bossPortal} I remove unused keys on ${phone1}
    [Teardown]   Default Availability State

799594: Phone sends digits over VM
    [Tags]      Owner:Vikhyat    Reviewer:    notApplicableFor6910
    &{sendDigits}=    Create Dictionary   digits=1234#    account_name=Automation    part_name=SC1    button_box=0
    Given using ${bossPortal} I program ${sendDigitsOverCall} on ${phone1} using ${sendDigits} and extension of ${phone2} and softkey position 3 with ExtensionValue
    Then Leave voicemail message from ${phone2} on ${phone1}
    Then Verify the led state of ${messageWaitingIndicator} as ${blink} on ${phone1}
    Then On ${phone1} dial number ##
    Then On ${phone1} Wait for 3 seconds
    Then on ${phone1} press ${softkey} ${programKey4} for 1 times
    Then On ${phone1} dial number 1
    Then On ${phone1} Wait for 2 seconds
    Then On ${phone1} dial number 3
    Then Press hardkey as ${goodBye} on ${phone1}
    And Verify the led state of ${messageWaitingIndicator} as ${off} on ${phone1}

759573: Prog Button Consult Conference (Destination not configured)
    [Tags]    Owner:Vikhyat    Reviewer:    consultConference
    Given using ${bossPortal} I program ${ConferenceConsultative} on ${phone1} using ${bossDetailsPKM} and extension of ${phone3} and softkey position 3 with noExtensionValue
    Then On ${phone1} verify display message ${displayMessage['conferenceConsult']}
    Then I want to make a two party call between ${phone1} and ${phone2} using ${loudSpeaker}
    Then Answer the call on ${phone2} using ${loudSpeaker}
    Then Verify audio path between ${phone1} and ${phone2}
    Then On ${phone1} press ${softkey} ${programKey4} for 1 times
    Then On ${phone1} enter number ${phone3}
    Then On ${phone1} press the softkey ${consult} in DialingState
    Then Verify ringing state on ${phone1} and ${phone3}
    Then Answer the call on ${phone3} using ${loudSpeaker}
    Then Conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then Disconnect the call from ${phone2}
    And Disconnect the call from ${phone1}

759616: Monitoring the Intercom extension "Active or Held Call"
    [Tags]    Owner:Vikhyat    Reviewer:    PKM    Intercom    Icon
    Given Using ${bossPortal} I program ${intercom} on ${phone1} using ${bossDetailsPKM} and extension of ${phone2} and softkey position 3 with extensionValue
    Then verify display message ${intercom} on PKM for ${phone1}
    Then I want to make a two party call between ${phone2} and ${phone3} using ${offHook}
    Then Answer the call on ${phone3} using ${offHook}
    Then Verify the Caller id on ${phone3} and ${phone2} display
    Then Verify ${line4} icon state as ${intercomActive} on PKM for ${phone1}
    And Disconnect the call from ${phone3}

