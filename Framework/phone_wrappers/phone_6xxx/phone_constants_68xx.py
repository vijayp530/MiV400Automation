# values are in hex
led_type = {"indicator_line_1":4,"indicator_line_2":5, "ringer":38,"message_waiting":39,"mute":"3A","speaker":'3F',"Function1":18}
# values are in hex
# led_mode = {"on":1, "off":0, "blink":[hex(x)[2:].upper() for x in range(2,17)]}
led_mode = {"on":'1', "off":'0', "blink":[str(x) for x in range(2,18)]}
# led_mode = {"on":1, "off":0, "blink":"F"}
# values are in decimal
line_state = {"idle":0,"dialing":1,"calling":2,"outgoing":3,"incoming":4,"connected":5,"clearing":6,"seizing":7,"hold":8,
              "busy":9,"enquiry_dialing":"17","enquiry_calling":"18","enquiry_outgoing":"19","enquiry_connected":"21","enquiry_clearing":"22",
              "enquiry_busy": "25"}

line_key_start_index = 23