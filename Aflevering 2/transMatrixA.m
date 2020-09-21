function [Aj0_j1] = transMatrixA(qj, alj, aj, dj)
% qj = theta to j
% alj = alpha to j
% aj = a to j
% dj = d to j
Aj0_j1 = [cos(qj),	-sin(qj)*cos(alj),	sin(qj)*sin(alj),	aj*cos(qj);
		  sin(qj),	cos(qj)*cos(alj),	-cos(qj)*sin(alj),	alj*sin(qj);
		  0,		sin(alj),			cos(alj),			dj;
		  0,		0,					0,					1];

end