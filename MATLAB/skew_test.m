clear all

% Example usage
rot = randomRotationMatrix();
skew = randomSkewSymmetricMatrix();
vectorForm = skewSymmetricToVector(skew);

R_skew = skewSymmetricToVector(rot*skew);

% disp('Random Rotation Matrix:');
% disp(rotationMatrix);
% 
% disp('Random Skew-Symmetric Matrix:');
% disp(skewSymmetricMatrix);
% 
% disp('Vector Form of Skew-Symmetric Matrix:');
% disp(vectorForm);% Generate a random rotation matrix

function R = randomRotationMatrix()
    % Generate a random rotation matrix using the QR decomposition method
    A = randomSkewSymmetricMatrix;
    % [Q, ~] = qr(A);
    R = expm(A);
end

% Generate a random skew-symmetric matrix
function S = randomSkewSymmetricMatrix()
    % Generate a random skew symmetric matrix by creating a random vector
    % and forming its skew symmetric matrix
    v = randn(3,1);
    S = [0 -v(3) v(2);
         v(3) 0 -v(1);
         -v(2) v(1) 0];
end

% Function to transform skew symmetric matrix to its vector form
function v = skewSymmetricToVector(S)
    % Extract the vector form from the upper triangular part of the matrix
    v = [S(3,2); S(1,3); S(2,1)];
end