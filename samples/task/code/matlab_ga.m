options = gaoptimset;
options = gaoptimset(options, 'Display', 'iter');
options = gaoptimset(options, 'PopulationSize', 80);
options = gaoptimset(options, 'Generations', 15);
options = gaoptimset(options, 'PlotFcn', @gaplotbestf);

LB = [-5.12]; % Lower bound
UB = [+5.12]; % Upper bound
x = ga(@dejong, 2, [], [], [], [], LB, UB, [], [], options)

function y = dejong(x)
    r = abs(fix(x));
    y = sum(r, 2);
end