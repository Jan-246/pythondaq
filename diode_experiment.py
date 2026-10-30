import pyvisa
import time
import matplotlib.pyplot as plt
import numpy as np

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
L_gem_U = []
L_gem_I = []
N = 3
for N in range(0, N):
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
        
        # print(f'Index: {index}')
        # print(f'U totaal: {U_totaal:.2f} V')
        # print(f'U LED: {U_LED:.2f} V')
        # print(f'I LED: {I_LED:.2f} A')
        
        L_U_LED.append(U_LED)
        L_I_LED.append(I_LED)
        
        U_gem = np.mean(L_U_LED)
        I_gem = np.mean(L_I_LED)
        std_U = np.std(L_U_LED, ddof=1)
        std_I = np.std(L_I_LED, ddof=1)
        L_gem_U.append(U_gem)
        L_gem_I.append(I_gem)
        onzekerheid_gem_U = std_U / np.sqrt(1024)


    print(f'gem U = {U_gem:.2f} +- {std_U:.2f}V, gem I = {I_gem:.2f} +- {std_I:.2f}A')

device.query('OUT:CH0 0')



plt.scatter(L_U_LED, L_I_LED, marker='.')
plt.xlabel('Spanning U (V)')
plt.ylabel('Stroomsterkte I (A)')
plt.title('UI-grafiek')
plt.grid(True)
plt.legend()
# plt.show()







    
