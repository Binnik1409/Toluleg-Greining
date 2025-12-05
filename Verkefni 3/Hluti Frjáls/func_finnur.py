def f3(start, m1=1, m2=1, m3=1, l1=2, l2=2, l3=2, g=9.81):

    theta_1, theta_2, theta_3, omega_1, omega_2, omega_3 = start

    a1 = (m2 + m3)*l1*m.sin(theta_1)*m.sin(theta_2-theta_1) - m1*l1*m.cos(theta_2)
    a2 = (m2 + m3)*l2*m.sin(theta_2)*m.sin(theta_2 - theta_1)
    a3 = m3*l3*m.sin(theta_3)*m.sin(theta_2 - theta_1)
    a4 = (m2 + m3)*l1*m.cos(theta_1)*m.sin(theta_2 - theta_1)
    a5 = (m2 + m3)*l2*m.cos(theta_2)*m.sin(theta_2 - theta_1)
    a6 = m3*l3*m.cos(theta_3)*m.sin(theta_2 - theta_1)
    a7 = (m2 + m3)*g*m.sin(theta_2 - theta_1) - m1*g*m.sin(theta_1)*m.cos(theta_2)

    b1 = m3*l1*m.sin(theta_1)*m.sin(theta_3 - theta_2) - m2*l1*m.cos(theta_3)*m.cos(theta_1 - theta_2)
    b2 = m3*l2*m.sin(theta_2)*m.sin(theta_3 - theta_2) - m2*l2*m.cos(theta_3)
    b3 = m3*l3*m.sin(theta_3)*m.sin(theta_3 - theta_2)
    b4 = m3*l1*m.cos(theta_1)*m.sin(theta_3 - theta_2) + m2*l1*m.cos(theta_3)*m.sin(theta_1 - theta_2)
    b5 = m3*l2*m.cos(theta_2)*m.sin(theta_3 - theta_2)
    b6 = m3*l3*m.cos(theta_3)*m.sin(theta_3 - theta_2)
    b7 = -(m2 + m3)*g*m.sin(theta_2)*m.cos(theta_3) + m3*g*m.cos(theta_2)*m.sin(theta_3)

    c1 = l1*m.cos(theta_1 - theta_3)
    c2 = l2*m.cos(theta_2 - theta_3)
    c3 = l3
    c4 = l1*m.sin(theta_3 - theta_1)
    c5 = l2*m.sin(theta_3 - theta_2)
    c6 = g*m.sin(theta_3)

    M = np.array([[a1, a2, a3],[b1, b2, b3],[c1, c2, c3]], dtype=float)
    F = np.array([a4*omega_1**2 + a5*omega_2**2 + a6*omega_3**2 + a7,
                  b4*omega_1**2 + b5*omega_2**2 + b6*omega_3**2 + b7,
                  c4*omega_1**2 + c5*omega_2**2 + c6], dtype=float)

    alpha = np.linalg.solve(M, F)
    alpha_1, alpha_2, alpha_3 = alpha

    return np.array([omega_1,omega_2,omega_3,alpha_1,alpha_2,alpha_3])