%% Init model
clear
close all

% Load our own model
load UR10_lim


%% Forward Kin with UR10
qn = [0 0.3 0];
T1 = urLim.fkine(qn)
urLim.plot(qn); %, 'workspace', [-10 10 -10 10 -10 10])
% urLim.teach()


%% Test inverse kinetics
o = T1.t'
o = [114, -5, 35]
qn2 = UR10_inv(o)








%%
o = [-15 15 9];
tic
for i=1:100000,
    qn = CrustInvKin(o);
end
toc
crawl.plot(qn); %, 'workspace', [-10 10 -10 10 -10 10])
crawl.teach()

% Compare with built-in func
T1 = crawl.fkine(qn)
tic
for i=1:100
    qn2 = crawl.ikine(T1, 'q0', [0 0 0 0], 'mask', [1 1 1 0 0 0]);
end
toc
crawl.plot(qn2); %, 'workspace', [-10 10 -10 10 -10 10])
crawl.teach()

