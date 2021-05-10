function_ids = {'SHARED_CALL_APPEARANCE': '86',
             'SILENT_COACH': '82',
             'TRANSFER_TO_WHISPER': '28',
             'TRANSFER_INTERCOM': '18',
             'MONITOR_EXTENSION': '3',
             'ASSIGN_TO_LAST_EXTERNAL': '43',
             'INTERCOM': '6',
             'TOGGLE_HANDSFREE': '60',
             'PARK': '22',
             'CENTREX_FLASH': '29',
             'RECORD_EXTENSION': '24',
             'AGENT_LOGOUT': '45',
             'WHISPER_PAGE_MUTE': '26',
             'CONFERENCE_BLIND': '19',
             'GROUP_PICKUP': '33',
             'TRANSFER_TO_MAILBOX': '17',
             'CALL_MOVE': '84',
             'INVOKE_URL': '37',
             'TO_VM': '39',
             'INVOKE_COMMAND_LINE': '36',
             'PARK_AND_PAGE': '23',
             'CONFERENCE': '41',
             'TOGGLE_LOCK_UNLOCK': '87',
             'WRAP_UP_CODE': '75',
             'CONTACT_CENTER': '4',
             'PAPI': '80',
             'WINDOWING': '2',
             'MALICIOUS_CALL_TRACE': '83',
             'CALL_APPEARANCE': '2',
             'RECORD_CALL': '25',
             'HANGUP': '34',
             'SILENT_MONITOR': '7',
             'RELEASE_WITH_CODE': '74',
             'CHANGE_CHM': '42',
             'ANSWER': '31',
             'BRIDGE_CALL_APPEARANCE': '30',
             'TRANSFER_CONSULTATIVE': '16',
             'AGENT_WRAP_UP': '46',
             'DIAL_MAILBOX': '5',
             'PICKUP_NIGHT_BELL': '13',
             'EXECUTE_DDE_COMMAND': '32',
             'RUN_CONTACT_CENTER_APP': '79',
             'SEND_DIGITS_OVER_CALL': '27',
             'CONFERENCE_INTERCOM': '21',
             'UNUSED': '1',
             'UNPARK': '11',
             'BARGE_IN': '8',
             'FUNCTION_CATEGORY': '{}',
             'HOLD': '35',
             'OPEN_HISTORY_VIEWER': '47',
             'TRANSFER_BLIND': '15',
             'WHISPER_PAGE': '9',
             'CONFERENCE_CONSULTATIVE': '20',
             'ALL': '0',
             'SUPERVISOR_HELP': '78',
             'CHANGE_DEFAULT_AUDIO_PATH': '62',
             'MOBILE': '88',
             'TRANSFER': '40',
             'DIAL_NUMBER_SPEED_DIAL': '4',
             'TO_AA': '38',
             'TELEPHONY': '1',
             'PICKUP': '10',
             'OTHER': '5',
             'HOTLINE': '81',
             'PICK_AND_PARK': '12',
             'CONFIG': '3',
             'PAGE': '14',
             'AGENT_LOGIN': '44'}

# for programming monitor extension
ring_delay_before_alert = {
                            "none": "0",
                            "1": "1",
                            "2": "2",
                            "3": "3",
                            "4": "4",
                            "dont_ring": "-1"
                            }

caller_id_alert = {
                            "always": "always",
                            "never": "never",
                            "only_when_ringing": "only_when_ringing",
                            }
no_connected_action = {
                            "unused": "1",
                            "dial_number": "4",
                            "intercom": "6",
                            "whisper_page": "9",
                            }
with_connected_action = {
                            "unused": "1",
                            "dial_number": "4",
                            "intercom": "6",
                            "whisper_page": "9",
                            "transfer_blind": "15",
                            "transfer_consultative": "16",
                            "transfer_intercom": "18",
                            "park": "22",
                            "transfer_whisper": "28",
                            }
hotline_call_actions = {
                            "dial number": "4",
                            "intercom": "6",
                       }

availability_options = {
                            "available": "1",
                            "in a meeting": "2",
                            "out of office": "3",
                            "do not disturb": "6",
                            "vacation": "4",
                            "custom": "5"
                       }