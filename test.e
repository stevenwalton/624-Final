y = 0; 
n = 100000; 
function (float) foo(int n) {epsilon = 0.001; x = 1; r = sqrt(n); while (abs(x - r) > epsilon) x = 0.5 * (x + n/x); return x;} 
y = foo(25);
