function [Aj0_j1] = transMatrixA(qj, alj, aj, dj)
% Transformation matrix from frame j to j+1.
%	Based on transformation matrix, from eq. 2.23, p. 46 in Corke 2nd
%	Edition
%	Inputs:
%		qj = theta to frame j
%		alj = alpha to frame j
% 		aj = a to frame j
% 		dj = d to frame j

Aj0_j1 = [cos(qj),	-sin(qj)*cos(alj),	sin(qj)*sin(alj),	aj*cos(qj);
		  sin(qj),	cos(qj)*cos(alj),	-cos(qj)*sin(alj),	alj*sin(qj);
		  0,		sin(alj),			cos(alj),			dj;
		  0,		0,					0,					1];

end