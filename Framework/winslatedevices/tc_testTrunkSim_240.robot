*** Settings ***
Documentation   TC NAME: Active call shows up as an blue strip in the extension
...             COMMENTS:  
Default Tags    dev-mvilleda	tc-240
# Resource		../../lib/newcommon.robot
Library			stafenv.py

Variables	automationProject.py

# Library			AutomationConfig
#Library			PPhoneInterface       ${IS_RUNTYPE_MT}  	WITH NAME	IP4XX_01
Library			wintrunksim		WITH NAME	TRUNK_ACTOR_1

# Test Setup		pphone_get_popup	${user_01}	

*** Variables ***
${Implicit_Wait}   5 seconds

*** Test Cases ***
Trunk Sim 240299
	# TRUNK_ACTOR_1.Trunksim Inboundcall	${user01.sip_did}
	TRUNK_ACTOR_1.Trunksim Inboundcall	14082223001
	
	Log		PICKUP NOW	WARN
	Sleep	7
	# IP4XX_01.answer_via_headset		${user01} 
	
	TRUNK_ACTOR_1.Trunksim Complete Inboundcall
	TRUNK_ACTOR_1.Trunksim Hangup
	
	# IP4XX_01.verify_pphone_idle		${user01}
	
	# # IP4XX_01.pphone_make_call	94087771001
	# # TRUNK_ACTOR_1.trunksim_receive_call
	
