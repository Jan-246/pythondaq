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

L_gem_U = []
L_gem_I = []
L_gem_U_err = []
L_gem_I_err = []

for index in range(0, 1024, 1):
    device.query(f'OUT:CH0 {index}')
    time.sleep(0.01)
    L_U_LED = []
    L_I_LED = []

    U_totaal = index * (3.3/1023)
    N = 3
    for i in range(N):
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
    gem_U_err = std_U / np.sqrt(N)
    gem_I_err = std_I / np.sqrt(N)
    L_gem_U_err.append(gem_U_err)
    L_gem_I_err.append(gem_I_err)

    
    print(f'gem U = {U_gem:.2f} +- {gem_U_err:.2f}V, gem I = {I_gem:.2g} +- {gem_I_err:.2g}A')

device.query('OUT:CH0 0')

plt.errorbar(L_gem_U, L_gem_I, xerr=L_gem_U_err, yerr=L_gem_I_err, ecolor='red')
plt.xlabel('Spanning U (V)')
plt.ylabel('Stroomsterkte I (A)')
plt.title('UI-grafiek met onzekerheden')
plt.grid(True)
plt.legend()
plt.show()

# plt.scatter(L_U_LED, L_I_LED, marker='.')
# plt.xlabel('Spanning U (V)')
# plt.ylabel('Stroomsterkte I (A)')
# plt.title('UI-grafiek')
# plt.grid(True)
# plt.legend()
# plt.show()







    
