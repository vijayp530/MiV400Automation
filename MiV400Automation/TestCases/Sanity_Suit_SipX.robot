*** Settings ***
Resource   ../RobotKeywords/Setup_And_Teardown.robot
Resource    ../RobotKeywords/PhoneKeywords.robot
Resource    ../Variables/SipX_Initialization.robot
Library    ../lib/MyListner.py


Test Timeout  5 minutes
Suite Setup  Run Keywords    Phones Initialization     Register Phone
Test Setup   Check Phone Connection
Test Teardown  Generic Test Teardown
Suite Teardown    Run Keywords   Check Phone Connection    Generic Test Teardown

*** Test Cases ***


750130: TC001 Phone Registration
    [Tags]   Owner: Ram    Reviewer:     RegisterPhone    1
    on ${phone1} wait for 5 seconds

############# SIPX Test Cases By Aman #############

750228: TC046 Blind Xfer
    [Tags]    Owner:Aman        Reviewer:       transfer    Generic_SIP_Sanity_Test_Plan_Version_1.0
    Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then Transfer call from ${phone1} to ${phone3} using ${blindTransfer}
    Then Verify audio path between ${phone2} and ${phone3}
    And disconnect the call from ${phone2}

750229: TC047 Blind Xfer - When Ringing (Semi-Attended Xfer)
    [Tags]    Owner:Aman        Reviewer:       transfer    Generic_SIP_Sanity_Test_Plan_Version_1.0
    Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then Transfer call from ${phone1} to ${phone3} using ${semiAttendedTransfer}
    Then answer the call on ${phone3} using ${loudspeaker}
    Then Verify audio path between ${phone2} and ${phone3}
    And disconnect the call from ${phone2}

750230: TC048 Consultative Xfer (Attended Xfer)
    [Tags]    Owner:Aman        Reviewer:       transfer    Generic_SIP_Sanity_Test_Plan_Version_1.0
    Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then Transfer call from ${phone1} to ${phone3} using ${consultiveTransfer}
    Then Verify audio path between ${phone2} and ${phone3}
    And disconnect the call from ${phone2}

750231: TC049 Local Conference and Leave Conference
    [Tags]    Owner:Aman        Reviewer:       conference    Generic_SIP_Sanity_Test_Plan_Version_1.0
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then i want to make a conference call between ${phone1},${phone2} and ${phone3} using ${directConference}
    Then conference call audio verify between ${phone1} ${phone2} and ${phone3}
	Then press hardkey as ${goodBye} on ${phone1}
    # Check for verify call transfer on display
    Then Verify audio path between ${phone2} and ${phone3}
	And Verify extension ${number} of ${phone1} on ${phone1}

750232: TC050 DND
    [Tags]    Owner:Aman        Reviewer:       dnd    Generic_SIP_Sanity_Test_Plan_Version_1.0
    Given I want to program ${doNotDisturb} key on position 4 on ${phone1}
    Then I want to press line key ${programKey4} on phone ${phone1}
    Then verify the led state of ${message_waiting} as ${on} on ${phone1}
    Then verify the led state of ${line4} as ${on} on ${phone1}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    # Verify phone busy
    Then I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
	Then Verify the Caller id on ${phone1} and ${phone2} display
	Then press hardkey as ${goodBye} on ${phone1}
    Then I want to press line key ${programKey4} on phone ${phone1}
    Then verify the led state of ${message_waiting} as ${off} on ${phone1}
    Then verify the led state of ${line4} as ${off} on ${phone1}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
	Then Verify the Caller id on ${phone1} and ${phone2} display
	Then press hardkey as ${goodBye} on ${phone2}
    Then I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
	Then Verify the Caller id on ${phone1} and ${phone2} display
	Then press hardkey as ${goodBye} on ${phone1}
	And I want to program ${none} key on position 4 on ${phone1}

750233: TC051 Line Stacking- outgoing call made and then incoming call appears - ringback/ringing state
    [Tags]    Owner:Aman        Reviewer:       call    Generic_SIP_Sanity_Test_Plan_Version_1.0        notApplicableFor6910        notApplicableFor6865
    Given I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then Verify ringing state on ${phone1} and ${phone2}
    Then Verify extension ${number} of ${phone2} on ${phone1}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then I want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then Verify ringing state on ${phone3} and ${phone1}
    Then Verify extension ${number} of ${phone3} on ${phone1}
    Then answer the call on ${phone1} using ${line2}
    Then on ${phone1} press ${hardKey} ${scrollUp} for 1 times
    Then Verify extension ${number} of ${phone2} on ${phone1}
    Then on ${phone1} press ${hardKey} ${scrollDown} for 1 times
    Then Verify extension ${number} of ${phone3} on ${phone1}
    Then on ${phone1} press ${hardKey} ${scrollLeft} for 1 times
    Then on ${phone1} press ${hardKey} ${scrollUp} for 1 times
    Then on ${phone1} press ${hardKey} ${scrollRight} for 1 times
    Then Verify extension ${number} of ${phone2} on ${phone1}
    Then on ${phone1} press ${hardKey} ${scrollLeft} for 1 times
    Then on ${phone1} press ${hardKey} ${scrollUp} for 1 times
    Then press hardkey as ${enter} on ${phone1}
    Then Verify extension ${number} of ${phone2} on ${phone1}
    Then on ${phone1} press ${hardKey} ${scrollLeft} for 1 times
    Then on ${phone1} press ${hardKey} ${scrollDown} for 1 times
    Then press hardkey as ${enter} on ${phone1}
    Then Verify extension ${number} of ${phone3} on ${phone1}
    Then disconnect the call from ${phone3}
    And disconnect the call from ${phone2}

750672: TC018 Intercom -Phone Side
    [Tags]    Owner:Aman        Reviewer:       Intercom    Generic_SIP_Sanity_Test_Plan_Version_1.0
    Given I want to program ${intercom} key on position 4 on ${phone1}
    Then Verify extension ${number} of ${phone1} on ${phone1}
    Then I want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then I want to press line key ${programKey4} on phone ${phone1}
    Then Verify the led state of ${mute} as ${blink} on ${phone1}
    Then Verify the led state of ${speaker} as ${on} on ${phone1}
    Then Verify one way audio from ${phone1} to ${phone2}
    Then Verify no audio path from ${phone2} to ${phone1}
    Then disconnect the call from ${phone1}
	And I want to program ${none} key on position 4 on ${phone1}

750673: TC031 Silent feature
    [Tags]    Owner:Aman        Reviewer:       Silence    Generic_SIP_Sanity_Test_Plan_Version_1.0    notApplicableFor6910        notApplicableFor6865
    Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then Verify ringing state on ${phone2} and ${phone1}
	Then verify the led state of ${line1} as ${blink} on ${phone1}
	Then on ${phone1} verify display message ${answer}
	Then on ${phone1} verify display message ${ignore}
	Then on ${phone1} verify display message ${silence}
    Then on ${phone1} press ${softkey} ${bottomKey4} for 1 times
	Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then on ${phone1} press ${softkey} ${bottomKey1} for 1 times
    Then Verify audio path between ${phone1} and ${phone2}
    Then disconnect the call from ${phone1}
    Given I want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then Verify ringing state on ${phone2} and ${phone1}
	Then verify the led state of ${line1} as ${blink} on ${phone1}
	Then on ${phone1} verify display message ${answer}
	Then on ${phone1} verify display message ${ignore}
	Then on ${phone1} verify display message ${silence}
	And press hardkey as ${goodBye} on ${phone2}


#########################  Anuj asterisk test cases #######################
750159: TC002 Redial list
    [Tags]    Owner:Anuj        Reviewer:       Asterisk    750159
    Given i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
#    Then verify audio path between ${phone1} and ${phone2}
    Then verify the caller id on ${phone1} and ${phone2} display
    Then disconnect the call from ${phone2}
    Then Press the call history button on ${phone1} and folder ${outgoing} and ${nothing}
    Then verify extension ${number} of ${phone2} on ${phone1}
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then on ${phone2} verify display message ${isCalling}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify the caller id on ${phone1} and ${phone2} display
#    Then verify audio path between ${phone1} and ${phone2}
    Then disconnect the call from ${phone2}
    Then Press the call history button on ${phone1} and folder ${outgoing} and ${delete}
    Then disconnect the call from ${phone2}
    Then Press the call history button on ${phone1} and folder ${outgoing} and ${nothing}
    Then i want to verify on ${phone1} negative display message ${phone2}
    Then disconnect the call from ${phone1}
    Then i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then disconnect the call from ${phone2}
    Then Press the call history button on ${phone1} and folder ${outgoing} and ${nothing}
    Then on ${phone1} press ${softkey} ${bottomkey3} for 1 times
    Then disconnect the call from ${phone1}
    Then press hardkey as ${directory} on ${phone1}
    Then in directory search ${phone2} on ${phone1}



750160: TC003 Caller list
    [Tags]    Owner:Anuj        Reviewer:       Asterisk    750160
    Given i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then disconnect the call from ${phone1}
    Then Press the call history button on ${phone1} and folder ${received} and ${offHook}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify the caller id on ${phone1} and ${phone2} display
#    Then verify audio path between ${phone1} and ${phone2}
    Then disconnect the call from ${phone2}
    Then Press the call history button on ${phone1} and folder ${received} and ${delete}
    Then disconnect the call from ${phone2}
    Then Press the call history button on ${phone1} and folder ${outgoing} and ${nothing}
    Then i want to verify on ${phone1} negative display message ${phone2}
    Then disconnect the call from ${phone1}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then disconnect the call from ${phone2}
    Then Press the call history button on ${phone1} and folder ${received} and ${nothing}
    Then on ${phone1} press ${softkey} ${bottomkey3} for 1 times
    Then disconnect the call from ${phone1}
    Then press hardkey as ${directory} on ${phone1}
    Then in directory search ${phone2} on ${phone1}
    And disconnect the call from ${phone1}

750161: TC004 Phone Lock
    [Tags]    Owner:Anuj        Reviewer:       Asterisk    750161
    Given press hardkey as ${menu} on ${phone1}
    Then press hardkey as ${scrollLeft} on ${phone1}
    Then on ${phone1} verify display message ${lock}
    Then press hardkey as ${scrollDown} on ${phone1}
    Then press hardkey as ${scrollDown} on ${phone1}
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then press hardkey as ${scrollRight} on ${phone1}
    Then press hardkey as ${enter} on ${phone1}
    Then on ${phone1} verify display message Phone is locked
    Then i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then i want to verify on ${phone2} negative display message ${isCalling}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then verify the caller id on ${phone1} and ${phone2} display
    Then disconnect the call from ${phone1}
    Then press hardkey as ${directory} on ${phone1}
    Then i want to verify on ${phone1} negative display message ${directory}
    Then Press the call history button on ${phone1} and folder ${All} and ${nothing}
    Then i want to verify on ${phone1} negative display message ${callHistory}
    Then press hardkey as ${callersList} on ${phone1}
    Then i want to verify on ${phone1} negative display message ${callHistory}
    Then press hardkey as ${menu} on ${phone1}
    Then on ${phone1} dial number 22222
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then press hardkey as ${scrollRight} on ${phone1}
    Then press hardkey as ${enter} on ${phone1}
    Then i want to make a two party call between ${phone1} and ${phone2} using ${loudspeaker}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then press hardkey as ${directory} on ${phone1}
    Then verify the caller id on ${phone1} and ${phone2} display
    Then disconnect the call from ${phone1}
    Then on ${phone1} verify display message ${directory}
    Then Press the call history button on ${phone1} and folder ${All} and ${nothing}
    Then on ${phone1} verify display message ${callHistory}
    Then disconnect the call from ${phone1}
    Then press hardkey as ${callersList} on ${phone1}
    Then on ${phone1} verify display message ${callHistory}
    And disconnect the call from ${phone1}

750162: TC006 Time display
    [Tags]    Owner:Anuj        Reviewer:       Asterisk    750162
    Given press hardkey as ${menu} on ${phone1}
    Then on ${phone1} press ${hardKey} ${scrollLeft} for 5 times
    Then on ${phone1} verify display message ${timedate}
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then on ${phone1} press ${hardKey} ${scrollDown} for 2 times
    Then on ${phone1} press ${hardKey} ${scrollRight} for 1 times
    Then on ${phone1} press ${hardKey} ${scrollUp} for 13 times
    Then on ${phone1} verify display message WWW MMM DD
    Then on ${phone1} press ${hardKey} ${scrollDown} for 13 times
    Then on ${phone1} verify display message DD.MM.YYYY
    And disconnect the call from ${phone1}

750163: TC011 Call Forward All (Unconditional)
    [Tags]    Owner:Anuj        Reviewer:       Asterisk    750163
    Given press hardkey as ${menu} on ${phone1}
    Then on ${phone1} press ${hardkey} ${scrollLeft} for 2 times
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then on ${phone1} enter number ${phone3}
    Then on ${phone1} press ${hardkey} ${enter} for 2 times
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then disconnect the call from ${phone1}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then on ${phone3} verify display message ${isCalling}
    Then answer the call on ${phone3} using ${loudspeaker}
#    Then verify audio path between ${phone2} and ${phone3}
    Then press hardkey as ${menu} on ${phone1}
    Then on ${phone1} press ${hardkey} ${scrollLeft} for 2 times
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then on ${phone1} press ${softKey} ${bottomKey2} for 10 times
    Then on ${phone1} press ${hardkey} ${enter} for 2 times
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times

    Then On ${phone1} program ${callForward} key on position 3 with ${phone3} value
    Then on ${phone1} press ${softKey} ${bottomKey2} for 1 times
    Then on ${phone1} enter number ${phone3}
    Then on ${phone1} press ${hardkey} ${enter} for 2 times
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then disconnect the call from ${phone1}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then on ${phone3} verify display message ${isCalling}
    Then answer the call on ${phone3} using ${loudspeaker}
    Then verify audio path between ${phone3} and ${phone2}
    Then disconnect the call from ${phone3}
    Then on ${phone1} press ${softKey} ${bottomKey2} for 1 times
    Then on ${phone1} press ${softKey} ${bottomKey2} for 10 times
    Then on ${phone1} press ${hardkey} ${enter} for 2 times
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times

    &{Details} =  Create Dictionary    ForwardNumberAll=${phone3}      ForwardNumberBusy=${phone3}       ForwardNumberNoAnswer=${phone3}     RingNumber=0    dnd=0
    Then I want to configure AccountConfiguration parameters using ${Details} for ${phone1}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then on ${phone3} verify display message ${isCalling}
    Then answer the call on ${phone3} using ${loudspeaker}
#    Then verify audio path between ${phone3} and ${phone2}
    &{Details} =  Create Dictionary    RingNumber=3    dnd=0
    Then I want to configure AccountConfiguration parameters using ${Details} for ${phone1}
    And disconnect the call from ${phone3}

750164: TC012 Call Foward Busy
    [Tags]    Owner:Anuj        Reviewer:       Asterisk    750164
    Given press hardkey as ${menu} on ${phone1}
    Then on ${phone1} press ${hardkey} ${scrollLeft} for 2 times
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then on ${phone1} press ${hardkey} ${scrollDown} for 2 times
    Then on ${phone1} enter number ${phone3}
    Then on ${phone1} press ${hardkey} ${enter} for 2 times
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then disconnect the call from ${phone1}

    Then i want to press line key ${programKey1} on phone ${phone1}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${line2}
#    Then verify audio path between ${phone1} and ${phone2}
    Then i want to make a two party call between ${phone4} and ${phone1} using ${loudspeaker}
    Then on ${phone3} verify display message ${isCalling}
    Then answer the call on ${phone3} using ${loudspeaker}
#    Then verify audio path between ${phone3} and ${phone4}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone4}
    Then press hardkey as ${menu} on ${phone1}
    Then on ${phone1} press ${hardkey} ${scrollLeft} for 2 times
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then on ${phone1} press ${hardkey} ${scrolldown} for 2 times
    Then on ${phone1} press ${softKey} ${bottomKey2} for 10 times
    Then on ${phone1} press ${hardkey} ${enter} for 2 times
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times

    Then On ${phone1} program ${callForward} key on position 3 with ${phone3} value
    Then on ${phone1} press ${softKey} ${bottomKey2} for 1 times
    Then on ${phone1} press ${hardkey} ${scrollDown} for 2 times
    Then on ${phone1} enter number ${phone3}
    Then on ${phone1} press ${hardkey} ${enter} for 2 times
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then disconnect the call from ${phone1}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone2}
    Then i want to make a two party call between ${phone4} and ${phone1} using ${loudspeaker}
    Then on ${phone3} verify display message ${isCalling}
    Then answer the call on ${phone3} using ${loudspeaker}
    Then verify audio path between ${phone3} and ${phone4}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone4}
    Then on ${phone1} press ${softKey} ${bottomKey2} for 1 times
    Then on ${phone1} press ${hardkey} ${scrollDown} for 2 times
    Then on ${phone1} press ${softKey} ${bottomKey2} for 10 times
    Then on ${phone1} press ${hardkey} ${enter} for 2 times
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times

    &{Details} =  Create Dictionary      ForwardNumberBusy=${phone3}     RingNumber=3    dnd=0
    Then I want to configure AccountConfiguration parameters using ${Details} for ${phone1}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then i want to make a two party call between ${phone4} and ${phone1} using ${loudspeaker}
    Then on ${phone3} verify display message ${isCalling}
    Then answer the call on ${phone3} using ${loudspeaker}
    Then verify audio path between ${phone3} and ${phone4}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone4}
    &{Details} =  Create Dictionary    RingNumber=3    dnd=0
    And I want to configure AccountConfiguration parameters using ${Details} for ${phone1}

750166: TC013 Call Forward No Answer
    [Tags]    Owner:Anuj        Reviewer:       Asterisk    750166
    Given press hardkey as ${menu} on ${phone1}
    Then on ${phone1} press ${hardkey} ${scrollLeft} for 2 times
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then on ${phone1} press ${hardkey} ${scrollDown} for 4 times
    Then on ${phone1} enter number ${phone3}
    Then on ${phone1} press ${hardkey} ${enter} for 3 times
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then disconnect the call from ${phone1}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then on ${phone1} wait for 8 seconds
    Then on ${phone3} verify display message ${isCalling}
    Then answer the call on ${phone3} using ${loudspeaker}
    Then verify audio path between ${phone2} and ${phone3}
    Then disconnect the call from ${phone2}
    Then press hardkey as ${menu} on ${phone1}
    Then on ${phone1} press ${hardkey} ${scrollLeft} for 2 times
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then on ${phone1} press ${hardkey} ${scrollDown} for 4 times
    Then on ${phone1} press ${softKey} ${bottomKey2} for 10 times
    Then on ${phone1} press ${hardkey} ${enter} for 3 times
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times

    Then On ${phone1} program ${callForward} key on position 3 with ${phone3} value
    Then on ${phone1} press ${softKey} ${bottomKey2} for 1 times
    Then on ${phone1} press ${hardkey} ${scrollDown} for 4 times
    Then on ${phone1} enter number ${phone3}
    Then on ${phone1} press ${hardkey} ${enter} for 3 times
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times
    Then disconnect the call from ${phone1}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then on ${phone1} wait for 8 seconds
    Then on ${phone3} verify display message ${isCalling}
    Then answer the call on ${phone3} using ${loudspeaker}
    Then verify audio path between ${phone2} and ${phone3}
    Then disconnect the call from ${phone2}
    Then on ${phone1} press ${softKey} ${bottomKey2} for 1 times
    Then on ${phone1} press ${hardkey} ${scrollDown} for 4 times
    Then on ${phone1} press ${softKey} ${bottomKey2} for 10 times
    Then on ${phone1} press ${hardkey} ${enter} for 3 times
    Then on ${phone1} press ${softKey} ${bottomKey1} for 1 times

    &{Details} =  Create Dictionary      ForwardNumberNoAnswer=${phone3}     RingNumber=3    dnd=0
    Then I want to configure AccountConfiguration parameters using ${Details} for ${phone1}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${loudspeaker}
    Then on ${phone1} wait for 8 seconds
    Then on ${phone3} verify display message ${isCalling}
    Then answer the call on ${phone3} using ${loudspeaker}
    Then verify audio path between ${phone2} and ${phone3}
    Then disconnect the call from ${phone2}
    &{Details} =  Create Dictionary    RingNumber=3    dnd=0
    And I want to configure AccountConfiguration parameters using ${Details} for ${phone1}

750200: TC014 Speeddial
    [Tags]    Owner:Anuj        Reviewer:       speeddial    750200
    Given On ${phone1} program ${speedDial} key on position 3 with ${phone2} value
    Then on ${phone1} verify display message speeddial
    Then i want to press line key ${programKey3} on phone ${phone1}
    Then on ${phone2} verify display message ${isCalling}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify the caller id on ${phone1} and ${phone2} display
    Then verify audio path between ${phone1} and ${phone2}
    Then disconnect the call from ${phone2}
    Then i want to make a two party call between ${phone1} and ${phone3} using ${loudspeaker}
    Then answer the call on ${phone3} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone3}
    Then verify the caller id on ${phone1} and ${phone3} display
    Then on ${phone1} press ${softKey} ${bottomKey3} for 1 times
    Then i want to press line key ${programKey3} on phone ${phone1}
    Then on ${phone2} verify display message ${isCalling}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify audio path between ${phone2} and ${phone3}
    Then disconnect the call from ${phone3}
    Then disconnect the call from ${phone2}
    Then i want to make a two party call between ${phone1} and ${phone3} using ${loudspeaker}
    Then answer the call on ${phone3} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone3}
    Then verify the caller id on ${phone1} and ${phone3} display
    Then on ${phone1} press ${softKey} ${bottomKey2} for 1 times
    Then i want to press line key ${programKey3} on phone ${phone1}
    Then on ${phone2} verify display message ${isCalling}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then on ${phone1} press ${softKey} ${bottomKey2} for 1 times
    Then conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then disconnect the call from ${phone2}
    And disconnect the call from ${phone3}

750201: TC015 Speeddial Xfer
    [Tags]    Owner:Anuj        Reviewer:       speeddialXfer    750201
    Given On ${phone1} program ${speeddialxfer} key on position 2 with ${phone2} value
    Then on ${phone1} verify display message ${speeddialxfer}
    Then i want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
#    Then verify audio path between ${phone1} and ${phone3}
    Then i want to press line key ${programKey2} on phone ${phone1}
    Then on ${phone2} verify display message ${isCalling}
    Then answer the call on ${phone2} using ${loudspeaker}
#    Then verify audio path between ${phone3} and ${phone2}
    Then I want to program None key on position 2 on ${phone1}
    &{configurationDetails}=    create dictionary    topsoftkey2 type=speeddialxfer    topsoftkey2 label=speeddialxfer    topsoftkey2 value=4165142512    topsoftkey2 line=1        prgkey3 type=speeddialxfer        prgkey3 label=speeddialxfer        prgkey3 value=4165142512    prgkey3 line=1
    Given Configure parameters on ${phone1} using ${configurationDetails}
    Then on ${phone1} verify display message ${speeddialxfer}
    Then i want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then veriy audio path between ${phone1} and ${phone3}
    Then i want to press line key ${programKey2} on phone ${phone1}
    Then on ${phone2} verify display message ${isCalling}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then verify audio path between ${phone3} and ${phone2}
    Then I want to program None key on position 2 on ${phone1}
    And disconnect the call from ${phone2}

750202: TC016 Speeddial Conference
    [Tags]    Owner:Anuj        Reviewer:       speeddialconf    750202
    Given On ${phone1} program ${speeddialconf} key on position 2 with ${phone2} value
    Then on ${phone1} verify display message ${speeddialconf}
    Then i want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone3}
    Then i want to press line key ${programKey2} on phone ${phone1}
    Then on ${phone2} verify display message ${isCalling}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then I want to program None key on position 2 on ${phone1}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}
    &{configurationDetails}=    create dictionary    topsoftkey2 type=speeddialconf    topsoftkey2 label=speeddialconf    topsoftkey2 value=4165142512    topsoftkey2 line=1        prgkey3 type=speeddialconf        prgkey3 label=speeddialconf        prgkey3 value=4165142512    prgkey3 line=1
    Given Configure parameters on ${phone1} using ${configurationDetails}
    Then on ${phone1} verify display message ${speeddialconf}
    Then i want to make a two party call between ${phone3} and ${phone1} using ${loudspeaker}
    Then answer the call on ${phone1} using ${loudspeaker}
    Then verify audio path between ${phone1} and ${phone3}
    Then i want to press line key ${programKey2} on phone ${phone1}
    Then on ${phone2} verify display message ${isCalling}
    Then answer the call on ${phone2} using ${loudspeaker}
    Then conference call audio verify between ${phone1} ${phone2} and ${phone3}
    Then disconnect the call from ${phone2}
    And disconnect the call from ${phone3}
    Then I want to program None key on position 2 on ${phone1}

###################### end of anuj test cases ###########################

################Abhishekkhanchi##############################################
750217:TC032 Display DTMF digit
    [Tags]    Owner:Abhishekkhanchi    Reviewer:    xfer    01/04/2020    1
    &{Details} =  Create Dictionary      displayDtmfDigits=1
    Then I want to configure Preferences parameters using ${Details} for ${phone1}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${OffHook}
    Then on ${phone1} wait for 4 seconds
    Then Answer the call on ${phone1} using ${OffHook}
#    Then verify audio path between ${phone2} and ${phone1}
    Then on ${phone1} dial number 2
    Then On ${phone1} verify display message 2
    Then disconnect the call from ${phone1}
    &{Details} =  Create Dictionary      displayDtmfDigits=0
    Then I want to configure Preferences parameters using ${Details} for ${phone1}

750223:TC039 Switch UI Focus to ringing line - Disable
    [Tags]    Owner:Abhishekkhanchi    Reviewer:    xfer    01/04/2020    102     nr
#    Given Remove topsoftkey2 from ${phone1}
#    Then Remove topsoftkey3 from ${phone1}
    &{Details} =  Create Dictionary      switchFocusToRingingLine=${disable}
    Then I want to configure Preferences parameters using ${Details} for ${phone1}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${OffHook}
    Then on ${phone1} wait for 4 seconds
    Then Answer the call on ${phone1} using ${OffHook}
#    Then verify audio path between ${phone2} and ${phone1}
    Then i want to make a two party call between ${phone3} and ${phone1} using ${OffHook}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then Verify extension ${number} of ${phone2} on ${phone1}
    Then On ${phone1} verify the led state of ${message_waiting} as ${blink} and led color
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}
    &{Details} =  Create Dictionary      switchFocusToRingingLine=${disable}
    Then I want to configure Preferences parameters using ${Details} for ${phone1}


750224:TC040 Switch UI Focus to ringing line - Enable
    [Tags]    Owner:Abhishekkhanchi    Reviewer:    xfer    01/04/2020    1     nr
#    Given Remove topsoftkey2 from ${phone1}
#    Then Remove topsoftkey3 from ${phone1}
    &{Details} =  Create Dictionary      switchFocusToRingingLine=${enable}
    Then I want to configure Preferences parameters using ${Details} for ${phone1}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${OffHook}
    Then on ${phone1} wait for 4 seconds
    Then Answer the call on ${phone1} using ${OffHook}
#    Then verify audio path between ${phone2} and ${phone1}
    Then i want to make a two party call between ${phone3} and ${phone1} using ${OffHook}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then Verify extension ${number} of ${phone3} on ${phone1}
    Then On ${phone1} verify the led state of ${message_waiting} as ${blink} and led color
    Then disconnect the call from ${phone1}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone3}
    &{Details} =  Create Dictionary      switchFocusToRingingLine=${disable}
    Then I want to configure Preferences parameters using ${Details} for ${phone1}


750225:TC041 Preferred Line
    [Tags]    Owner:Abhishekkhanchi    Reviewer:    xfer    01/04/2020   12
    &{Details} =  Create Dictionary      preferedLine=${pflinetwo}
    Given I want to configure Preferences parameters using ${Details} for ${phone1}
    Then Press hardkey as ${OffHook} on ${phone1}
    Then verify the led state of ${line2} as ${on} on ${phone1}
    Then On ${phone1} verify display message >
    Then Press hardkey as ${OffHook} on ${phone1}
    Then disconnect the call from ${phone1}
    Then on ${phone1} wait for 4 seconds
    Then i want to make a two party call between ${phone2} and ${phone1} using ${OffHook}
    Then on ${phone1} wait for 8 seconds
    Then Answer the call on ${phone1} using ${OffHook}
#    Then verify audio path between ${phone2} and ${phone1}
    Then verify the led state of ${line2} as ${on} on ${phone1}
    Then disconnect the call from ${phone1}
    &{Details} =  Create Dictionary      preferedLine=${pflineone}
    Then I want to configure Preferences parameters using ${Details} for ${phone1}


750226:TC042 Preferred Line Timeout
    [Tags]    Owner:Abhishekkhanchi    Reviewer:    xfer    01/04/2020    123
    &{Details} =  Create Dictionary      preferedLine=${pflinetwo}  preferedLineTimeout=20
    Given I want to configure Preferences parameters using ${Details} for ${phone1}
    Then Press hardkey as ${OffHook} on ${phone1}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then on ${phone1} wait for 22 seconds
    Then verify the led state of ${line2} as ${on} on ${phone1}
    Then On ${phone1} verify display message >
    Then Press hardkey as ${OffHook} on ${phone1}
    Then i want to make a two party call between ${phone2} and ${phone1} using ${OffHook}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then on ${phone1} wait for 22 seconds
    Then verify the led state of ${line2} as ${blink} on ${phone1}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone1}
    &{Details} =  Create Dictionary      preferedLine=${pflineone}  preferedLineTimeout=0
    Then I want to configure Preferences parameters using ${Details} for ${phone1}


750227:TC043 GoodBye Key Cancels Incoming call - OFF
    [Tags]    Owner:Abhishekkhanchi    Reviewer:    xfer    01/04/2020    1
    &{Details} =  Create Dictionary      goodbyeCancelIncomingCall=${disable}
    Given I want to configure Preferences parameters using ${Details} for ${phone1}
    Then press hardkey as CallersList on ${phone1}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${offHook}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then Answer the call on ${phone1} using ${line1}
    Then i want to make a two party call between ${phone3} and ${phone1} using ${OffHook}
    Then Verify the led state of ${message_waiting} as ${blink} on ${phone1}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then verify the led state of ${line2} as ${blink} on ${phone1}
    Then Verify extension ${number} of ${phone2} on ${phone1}
    Then Press hardkey as ${goodBye} on ${phone1}
    Then Verify the led state of ${line1} as ${off} on ${phone1}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone1}
    &{Details} =  Create Dictionary      goodbyeCancelIncomingCall=${enable}
    And I want to configure Preferences parameters using ${Details} for ${phone1}

750234:TC044 Goodbye Cancels incoming call - ON
    [Tags]    Owner:Abhishekkhanchi    Reviewer:    xfer    01/04/2020    1
    &{Details} =  Create Dictionary      goodbyeCancelIncomingCall=${enable}
    Given I want to configure Preferences parameters using ${Details} for ${phone1}
    Then press hardkey as CallersList on ${phone1}
    Then I want to make a two party call between ${phone2} and ${phone1} using ${offHook}
    Then verify the led state of ${line1} as ${blink} on ${phone1}
    Then on ${phone1} wait for 4 seconds
    Then Answer the call on ${phone1} using ${line1}
    Then i want to make a two party call between ${phone3} and ${phone1} using ${OffHook}
    Then Verify the led state of ${message_waiting} as ${blink} on ${phone1}
    Then verify the led state of ${line1} as ${on} on ${phone1}
    Then verify the led state of ${line2} as ${blink} on ${phone1}
    Then Verify extension ${number} of ${phone2} on ${phone1}
    Then Press hardkey as ${goodBye} on ${phone1}
    Then Verify the led state of ${line1} as ${on} on ${phone1}
#    Then verify audio path between ${phone2} and ${phone1}
    Then disconnect the call from ${phone2}
    Then disconnect the call from ${phone1}
    &{Details} =  Create Dictionary      goodbyeCancelIncomingCall=${enable}
    Then I want to configure Preferences parameters using ${Details} for ${phone1}
