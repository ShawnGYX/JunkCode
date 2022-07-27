clear all
clc


dt = 0.5;

omega = rand(1,3);
a = rand(1,3);
U = zeros(5);

G = zeros(5);
G(3,5) = -9.81;

ox = skew(omega);
oxt = ox*dt;
U(1:3,1:3) = ox;
U(1:3,5) = a;
D = zeros(5);
D(5,4) = 1;


f1 = expm(dt*(U+D));

f2 = eye(5);
f2(5,4)=dt;
f2(1:3,1:3) = expm(dt*skew(omega));
theta = norm(dt*omega);
J = eye(3)+((1-cos(theta))/(theta^2))*oxt + ((theta-sin(theta))/(theta^3))*(oxt*oxt);

S = 0.5*eye(3)+((theta-sin(theta))/(theta^3))*oxt - ((1-0.5*theta^2-cos(theta))/(theta^4))*(oxt*oxt);
f2(1:3,5) = J*a'*dt;
f2(1:3,4) = S*a'*dt*dt;

disp(f1);
disp(f2);

function x_skew = skew(x)
    x_skew = [0,-x(3),x(2);...
        x(3),0,-x(1);...
        -x(2),x(1),0];
 end
