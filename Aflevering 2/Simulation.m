%% UR10 - Egne DH-parametre
clear, close all;
L1 = Revolute('d', 0, 'a', 0, 'alpha', pi/2)
L2 = Revolute('d', 18, 'a', 62, 'alpha', pi)
L3 = Revolute('d', 12, 'a', 58, 'alpha', pi)
L4 = Revolute('d', 13, 'a', 0, 'alpha', -pi/2)
L5 = Revolute('d', 12, 'a', 0, 'alpha', -pi/2)
L6 = Revolute('d', 6, 'a', 0, 'alpha', 0)
ur = SerialLink([L1, L2, L3, L4, L5, L6])

figure()
ur.teach()
ur.fkine([0, 0.1, 0.2, pi/2, pi/4, 0])

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

qr = [pi -0.35 1.2 pi/2 pi/4 0];
figure(1)
T = ur.fkine(qr)
ur.plot(qr);
%ur.teach()
%ur.ikine(T)


%% Forward Kinematic
qn = [0 0.1 0.2 pi/2 pi/4 0];
T1 = ur.fkine(qn)
ur.plot(qn); %, 'workspace', [-10 10 -10 10 -10 10])
%ur.teach()


%% Testing Inverse Kinematics
% Compare with built-in func
qn2 = ur.ikine(T1)
ur.plot(qn2); %, 'workspace', [-10 10 -10 10 -10 10])
ur.teach()
qn
qn2
%% Generate path
xarr = -20:1:50; % y-values
yarr = -25*ones(size(xarr)); % x-values (constant)
zarr = 30*ones(size(xarr)); % z-values (constant)

Tinit = transl(xarr(1), yarr(1), zarr(1));
qseq = zeros(length(xarr), 6);
qseq(1,:)=ur.ikine(Tinit);
%  'ilimit',L     set the maximum iteration count (default 1000)
%   'tol',T        set the tolerance on error norm (default 1e-6)
%   'alpha',A      set step size gain (default 1)

for i= 2:length(xarr) % note: from i=2
    T = transl(xarr(i), yarr(i), zarr(i)); % homogeneous transform
    qseq(i,:) = ur.ikine(T, 'q0',qseq(i-1,:));
end

%% "Animating" path
disp('Start animating')
% pause;
ur.plot(qseq, 'trail', 'r')


%% Symbolic solution
syms q1 q2 q3 q4 q5 q6

ursym = ur.sym();

Tsym = ursym.fkine([q1 q2 q3 q4 q5 q6])
