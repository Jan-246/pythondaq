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
while index < 1024:
    index += 10
    device.query(f'OUT:CH0 {index}')
    time.sleep(0.01)
    print(index)
    U_totaal = index * (3.3/1023)
    U_lampje = int(device.query('MEAS:CH1?'))*(3.3/1023) - int(device.query('MEAS:CH2?'))*(3.3/1023)
    I_lampje = int(device.query('MEAS:CH2?')) / 220
    print(f'spanning lampje: {U_lampje} V')
    print(f'spanning totaal: {U_totaal} V')
    print(f'stroom lampje: {I_lampje} A')

    
