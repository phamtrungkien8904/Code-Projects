n = 12; % number of coins to pick
p = 0.22; % probability of a certain coin type
N = 50; % number of repetitions


data = readmatrix('data.csv');
m = data(:,2).' / N * 100;

x = linspace(0, n, n + 1);
P_bi = 100 * binopdf(x, n, p);
P_poi = 100 * poisspdf(x, n * p);
plot(x, P_bi, 'LineWidth', 2, 'Color', 'r')
hold on
stem(x, P_bi, 'LineWidth', 2, 'LineStyle', 'none', 'Color', 'r')
hold on
plot(x, P_poi, 'LineWidth', 2, 'Color', 'g')
hold on
stem(x, P_poi, 'LineWidth', 2, 'LineStyle', 'none', 'Color', 'g')
hold on
plot(x, m, 'LineWidth', 2, 'Color', 'b')
hold on
stem(x, m, 'LineWidth', 2, 'LineStyle', '--', 'Color', 'b')
xlabel('Erfolge')
ylabel('Wahrscheinlichkeit (%)')
xlim([0 n])
ylim([0 40])
title(sprintf('Data-generate vs. Theorie (N = %d)', N))
legend('Binomialverteilung', '','Poissonverteilung','', 'Daten', '')


exportgraphics(gcf, 'code-1.eps', 'ContentType', 'vector');