if op[i] < op_lo:  # check lower limit
    op[i] = op_lo
    ie[i] = ie[i] - e[i] * delta_t # anti-reset windup