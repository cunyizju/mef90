Point(1) = {0, 0, 0, 0.01};
Point(2) = {1, 0, 0, 0.01};
Point(3) = {1, 0.1, 0, 0.01};
Point(4) = {0, 0.1, 0, 0.01};
Line(1) = {1, 2};
Line(2) = {2, 3};
Line(3) = {3, 4};
Line(4) = {4, 1};
Line Loop(6) = {3, 4, 1, 2};
Plane Surface(6) = {6};
Physical Line(20) = {4};
Physical Line(30) = {2};
Physical Surface(1) = {6};