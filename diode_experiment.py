import pyvisa
import time


rm = pyvisa.ResourceManager("@py")
ports = rm.list_resources()
print(ports)

device = rm.open_resource(
    "ASRL13::INSTR",
    read_termination="\r\n",
    write_termination="\n"
)
identification = device.query("*IDN?")
print(identification)


index = 0
L_U_LED = []
L_I_LED = []
while index < 1024:
    index += 10
    device.query(f'OUT:CH0 {index}')
    time.sleep(0.01)
    print(index)
    U_totaal = index * (3.3/1023)
    U_LED = int(device.query('MEAS:CH1?'))*(3.3/1023) - int(device.query('MEAS:CH2?'))*(3.3/1023)
    I_LED = int(device.query('MEAS:CH2?')) / 220
    print(f'U totaal: {U_totaal:.2f} V')
    print(f'U LED: {U_lampje:.2f} V')
    print(f'I LED: {I_lampje:.2f} A')
    L_U_LED.append(U_LED)
    L_I_LED.append(I_LED)





    
