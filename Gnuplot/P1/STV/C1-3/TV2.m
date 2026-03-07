data1 = dlmread('TV2_50Messungen.stat','',15,0)
x1 = data1(:,1);
y1 = data1(:,2);
E1 = dot(x1,y1)/sum(y1) % Mittelwert
sigma1 = sqrt(dot(y1,(x1-E1).^2)/sum(y1))

data2 = dlmread('TV2_100Messungen.stat','',15,0)
x2 = data2(:,1);
y2 = data2(:,2);
E2 = dot(x2,y2)/sum(y2) % Mittelwert
sigma2 = sqrt(dot(y2,(x2-E2).^2)/sum(y2))

[ax,h1,h2]=plotyy(x1,y1,x2,y2,'bar','bar')
set(h2,'FaceColor',[0 0.447 0.741], 'FaceAlpha', 0.8, 'BarWidth', 0.7);
set(h1,'FaceColor',[0.85 0.325 0.098], 'FaceAlpha', 1.0, 'BarWidth', 0.9);
xlabel('Anzahl der Zerfälle pro 2s');
ylabel(ax(1),'Häufigkeit (50 Messungen)');
ylabel(ax(2),'Häufigkeit (100 Messungen)');
title('Poissonverteilung der Radioaktivität');
legend('50 Messungen', '100 Messungen');

hold on

stem(E2, 12)