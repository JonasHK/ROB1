
% theta, alpha, a, d
A1_2 = transMatrixA(deg2rad(180), deg2rad(90), 0, 0)
A2_3 = transMatrixA(deg2rad(-90), deg2rad(180), 62, 18)
A3_4 = transMatrixA(deg2rad(90), deg2rad(180), 58, 13)
A4_5 = transMatrixA(deg2rad(180), deg2rad(-90), 0, 13)
A5_6 = transMatrixA(deg2rad(-90), deg2rad(-90), 0, 12)
A6_7 = transMatrixA(deg2rad(0), deg2rad(0), 0, 6)

% Full transformation matrix
Acomb = A1_2 * A2_3 * A3_4 * A4_5 * A5_6 * A6_7
