
% r = length in pixels
% X = real length [m]
% Z = Distance to object [m]
% k = f/sx (focal length/pixel size)

% Calculate k constant
% k = (r*Z)/X;

% Assume a value for the camera's k-constant
	% Comment out and replace with calculation above, if we get access to
	% the webcam before handin.
k = 500;

% Distance from camera to work area [m]
Z = 0.65;

% Find real length to travel from pixel length
dist = @(r) ((r*Z)/k);
p2m_constant = Z/k;

% Example: if the distance to move on the camera is 45 pixels, then we can
% find the real distance in meters.
moveDist = dist(45)
unitDist = dist(1)