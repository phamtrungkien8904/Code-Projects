data = readtable('data.csv','ReadVariableNames',true);

% Metadata is stored in the first data row of columns n, N, p
n = data{1,3};
N = data{1,4};
p = data{1,5};

% Frequencies start from row 2 (coin count 0 to n)
x = data{2:end,1}';
m = data{2:end,2}' / N * 100;

P = 100 * binopdf(x, n, p);
plot(x, P, 'LineWidth', 2, 'Color', 'r')
hold on
stem(x, P, 'LineWidth', 2, 'LineStyle', 'none', 'Color', 'r')
hold on
plot(x, m, 'LineWidth', 2, 'Color', 'b')
hold on
stem(x, m, 'LineWidth', 2, 'LineStyle', '--', 'Color', 'b')
xlabel('Erfolge')
ylabel('Wahrscheinlichkeit(%)')
xlim([0 n])
ylim([0 100])
title(sprintf('Data-generate vs. Theorie (N = %d)', N))
legend('Binomialverteilung', '', 'Daten', '')