%% UR10 - UR10 fra nettet DH-parametre inkl. tool_length
clear, close all;
tool_length = 0.15; % m
L1 = Revolute('d', 0.12, 'a', 0, 'alpha', pi/2);
L2 = Revolute('d', 0, 'a', -0.612, 'alpha', 0);
L3 = Revolute('d', 0, 'a', -0.5723, 'alpha', 0);
L4 = Revolute('d', 0.163941, 'a', 0, 'alpha', pi/2);
L5 = Revolute('d', 0.1157, 'a', 0, 'alpha', -pi/2);
L6 = Revolute('d', 0.0922+tool_length, 'a', 0, 'alpha', 0);
ur = SerialLink([L1, L2, L3, L4, L5, L6]);

qn = [pi -0.35 1.2 pi/2 pi/4 0];
T = ur.fkine(qn)