#### Highlighting the parts that need to be changed ####
# Controller tuning
Kff = -3.0

# simulate with ODEINT
for i in range(n-1):
    ##### add feedforward to controller
    valve = ubias + P[i] + I[i] + Kff * (Fin[i]-Fin[0])
    #####