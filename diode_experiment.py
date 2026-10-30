import pyvisa
import time
import matplotlib.pyplot as plt

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


L_U_LED = []
L_I_LED = []
for index in range(0, 1024, 10):
    device.query(f'OUT:CH0 {index}')
    time.sleep(0.01)
    
    U_totaal = index * (3.3/1023)
    CH1 = int(device.query('MEAS:CH1?'))
    CH2 = int(device.query('MEAS:CH2?'))
    U_1 = CH1 * (3.3/1023)
    U_2 = CH2 * (3.3/1023)
    U_LED = U_1 - U_2
    I_LED = U_2 / 220
    
    print(f'Index: {index}')
    print(f'U totaal: {U_totaal:.2f} V')
    print(f'U LED: {U_LED:.2f} V')
    print(f'I LED: {I_LED:.2f} A')
    
    L_U_LED.append(U_LED)
    L_I_LED.append(I_LED)

device.query('OUT:CH0 0')

plt.scatter(L_U_LED, L_I_LED, marker='.')
plt.xlabel('Spanning U (V)')
plt.ylabel('Stroomsterkte I (A)')
plt.title('UI-grafiek')
plt.grid(True)
plt.legend()
plt.show()







    
