%% Own measured parameters
% Purpose:
%	Calculating the transformation matrices, between each of the frames and
%	calculating the combines transformation matrix for the whole robot.

% Input order of the function "transMatrixA": theta, alpha, a, d
A1_2 = transMatrixA(deg2rad(0), deg2rad(90), 0, 0)
A2_3 = transMatrixA(deg2rad(0), deg2rad(180), 62, 18)
A3_4 = transMatrixA(deg2rad(0), deg2rad(180), 58, 13)
A4_5 = transMatrixA(deg2rad(0), deg2rad(-90), 0, 13)
A5_6 = transMatrixA(deg2rad(0), deg2rad(-90), 0, 12)
A6_7 = transMatrixA(deg2rad(0), deg2rad(0), 0, 6)

% Combined transformation matrix for the entire robot
Acomb = A1_2 * A2_3 * A3_4 * A4_5 * A5_6 * A6_7

%% Parameters found for the UR10 on the internet
% Purpose:
%	Calculating the transformation matrices, between each of the frames and
%	calculating the combines transformation matrix for the whole robot.

% Input order of the function "transMatrixA": theta, alpha, a, d
A1_2 = transMatrixA(deg2rad(0), deg2rad(90), 0, 0.12)
A2_3 = transMatrixA(deg2rad(0), deg2rad(180), -0.612, 0)
A3_4 = transMatrixA(deg2rad(0), deg2rad(180), -0.5723,0)
A4_5 = transMatrixA(deg2rad(0), deg2rad(-90), 0, 0.163941)
A5_6 = transMatrixA(deg2rad(0), deg2rad(-90), 0, 0.1157)
A6_7 = transMatrixA(deg2rad(0), deg2rad(0), 0, 0.0922)

% Combined transformation matrix for the entire robot
Acomb = A1_2 * A2_3 * A3_4 * A4_5 * A5_6 * A6_7