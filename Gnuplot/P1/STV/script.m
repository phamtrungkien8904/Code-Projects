n = 12; % number of coins to pick
p = 0.22; % probability of a certain coin type
N = 50; % number of repetitions


data = readmatrix('data.csv');
m = data(:,2).' / N * 100;

x = linspace(0, n, n + 1);
P = 100 * binopdf(x, n, p);
plot(x, P, 'LineWidth', 2, 'Color', 'r')
hold on
stem(x, P, 'LineWidth', 2, 'LineStyle', 'none', 'Color', 'r')
hold on
plot(x, m, 'LineWidth', 2, 'Color', 'b')
hold on
stem(x, m, 'LineWidth', 2, 'LineStyle', '--', 'Color', 'b')
xlabel('Erfolge')
ylabel('Wahrscheinlichkeit (%)')
xlim([0 n])
ylim([0 40])
title(sprintf('Data-generate vs. Theorie (N = %d)', N))
legend('Binomialverteilung', '', 'Daten', '')