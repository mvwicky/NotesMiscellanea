nu = 5;
p = @(t) (t.^(-nu/2-1)).*(exp(-1./(2*t)));
proposal_PDF= @(mu) unifrnd(0, 3);

N = 1000;
nn = 0.1*(N);
theta = zeros(1, N);
theta(1) = 0.3;

for i = 1:N
	theta_ast = proposal_PDF