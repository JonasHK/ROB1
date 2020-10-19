

L1 = Revolute('d', 0, 'a', 0, 'alpha', pi/2)
L2 = Revolute('d', 18, 'a', 62, 'alpha', pi)
L3 = Revolute('d', 13, 'a', 58, 'alpha', pi)
L4 = Revolute('d', 13, 'a', 0, 'alpha', -pi/2)
urLim = SerialLink([L1, L2, L3, L4])


save('UR10_lim.mat', 'urLim')