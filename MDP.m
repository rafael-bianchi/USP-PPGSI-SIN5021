% | 1 | 2 | 3 | 4 | 5|
% | 6 | 7 | 8 | 9 |10|

S = 10;
A = 4;


R = ones(S,A);

R(1:S,1:A) = -1;
R(S,1:A) = 0;

%% Versao Explicita - Extensa

%UP

T = zeros(S,S,A);

T(:,:,1) = [  1   0   0   0   0   0   0   0   0   0;
              0   1   0   0   0   0   0   0   0   0;
              0   0   1   0   0   0   0   0   0   0;
              0   0   0   1   0   0   0   0   0   0;
              0   0   0   0   1   0   0   0   0   0;
              1   0   0   0   0   0   0   0   0   0;
              0 0.5   0   0   0 0.5   0   0   0   0;
              0   0 0.5   0   0 0.5   0   0   0   0;
              0   0   0 0.5   0 0.5   0   0   0   0;
              0   0   0   0   0   0   0   0   0   1];

%DOWN

T(:,:,2) = [  0   0   0   0   0   1   0   0   0   0;
              0   0   0   0   0   0   1   0   0   0;
              0   0   0   0   0   0   0   1   0   0;
              0   0   0   0   0   0   0   0   1   0;
              0   0   0   0   0   0   0   0   0   1;
              0   0   0   0   0   1   0   0   0   0;
              0   0   0   0   0 0.5 0.5   0   0   0;
              0   0   0   0   0 0.5   0 0.5   0   0;
              0   0   0   0   0 0.5   0   0 0.5   0;
              0   0   0   0   0   0   0   0   0   1];
        
%RIGHT

T(:,:,3) = [  0   1   0   0   0   0   0   0   0   0;
              0   0   1   0   0   0   0   0   0   0;
              0   0   0   1   0   0   0   0   0   0;
              0   0   0   0   1   0   0   0   0   0;
              0   0   0   0   1   0   0   0   0   0;
              0   0   0   0   0   0   1   0   0   0;
              0   0   0   0   0 0.5   0 0.5   0   0;
              0   0   0   0   0 0.5   0   0 0.5   0;
              0   0   0   0   0 0.5   0   0   0 0.5;
              0   0   0   0   0   0   0   0   0   1];

%LEFT

T(:,:,4) = [  1   0   0   0   0   0   0   0   0   0;
              1   0   0   0   0   0   0   0   0   0;
              0   1   0   0   0   0   0   0   0   0;
              0   0   1   0   0   0   0   0   0   0;
              0   0   0   1   0   0   0   0   0   0;
              0   0   0   0   0   1   0   0   0   0;
              0   0   0   0   0   1   0   0   0   0;
              0   0   0   0   0 0.5 0.5   0   0   0;
              0   0   0   0   0 0.5   0 0.5   0   0;
              0   0   0   0   0   0   0   0   0   1];
          
%% Versao Explicita - Reduzida

T = zeros(S,S,A);

%UP
T(1,[1],1) = [1];
T(2,[2],1) = [1];
T(3,[3],1) = [1];
T(4,[4],1) = [1];
T(5,[5],1) = [1];
T(6,[1],1) = [1];
T(7,[2 6],1) = [0.5 0.5];
T(8,[3 6],1) = [0.5 0.5];
T(9,[4 6],1) = [0.5 0.5];
T(10,[10],1) = [1];

%DOWN
T(1,[6],2) = [1];
T(2,[7],2) = [1];
T(3,[8],2) = [1];
T(4,[9],2) = [1];
T(5,[10],2) = [1];
T(6,[6],2) = [1];
T(7,[7 6],2) = [0.5 0.5];
T(8,[8 6],2) = [0.5 0.5];
T(9,[9 6],2) = [0.5 0.5];
T(10,[10],2) = [1];
          
%RIGHT
T(1,[2],3) = [1];
T(2,[3],3) = [1];
T(3,[4],3) = [1];
T(4,[5],3) = [1];
T(5,[5],3) = [1];
T(6,[7],3) = [1];
T(7,[8 6],3) = [0.5 0.5];
T(8,[9 6],3) = [0.5 0.5];
T(9,[10 6],3) = [0.5 0.5];
T(10,[10],3) = [1];

%LEFT
T(1,[1],4) = [1];
T(2,[1],4) = [1];
T(3,[2],4) = [1];
T(4,[3],4) = [1];
T(5,[4],4) = [1];
T(6,[6],4) = [1];
T(7,[6],4) = [1];
T(8,[7 6],4) = [0.5 0.5];
T(9,[8 6],4) = [0.5 0.5];
T(10,[10],4) = [1];


%% Versao Implicita


X = 5; Y = 2;

S = X*Y;
T = zeros(S,S,A);

prob = 0.5;

%UP
a = 1;
for y=1:Y
    for x=1:X
        s = (y-1)*X + x;
        
        probAux = prob;
        
        if (x == 1 || x == X || y == 1)
            nextx = x;
            nexty = max(y-1,1);
            nexts = (nexty-1)*X + nextx;
            
            T(s,nexts,a) = T(s,nexts,a) + 1;
        else
            nextx = x;
            nexty = max(y-1,1);
            nexts = (nexty-1)*X + nextx;
            
            T(s,nexts,a) = T(s,nexts,a) + (1-probAux);

            nextx = 1;
            nexty = Y;
            nexts = (nexty-1)*X + nextx;
            T(s,nexts,a) = T(s,nexts,a) + probAux;
        end
    end
end

% Meta
T(S,:,a) = 0; T(S,S,a) = 1;

%DOWN
a = 2;
for y=1:Y
    for x=1:X
        s = (y-1)*X + x;
        
        probAux = prob;
        
        if (x == 1 || x == X || y == 1)
            nextx = x;
            nexty = min(y+1,Y);
            nexts = (nexty-1)*X + nextx;
            
            T(s,nexts,a) = T(s,nexts,a) + 1;
        else
            nextx = x;
            nexty = min(y+1,Y);
            nexts = (nexty-1)*X + nextx;
            
            T(s,nexts,a) = T(s,nexts,a) + (1-probAux);

            nextx = 1;
            nexty = Y;
            nexts = (nexty-1)*X + nextx;
            T(s,nexts,a) = T(s,nexts,a) + probAux;
        end
    end
end

% Meta
T(S,:,a) = 0; T(S,S,a) = 1;

%LEFT
a = 4;
for y=1:Y
    for x=1:X
        s = (y-1)*X + x;

        probAux = prob;
        
        if (x == 1 || x == X || y == 1)
            nextx = max(x-1,1);
            nexty = y;
            nexts = (nexty-1)*X + nextx;
            
            T(s,nexts,a) = T(s,nexts,a) + 1;
        else
            nextx = max(x-1,1);
            nexty = y;
            nexts = (nexty-1)*X + nextx;
            
            T(s,nexts,a) = T(s,nexts,a) + (1-probAux);

            nextx = 1;
            nexty = Y;
            nexts = (nexty-1)*X + nextx;
            T(s,nexts,a) = T(s,nexts,a) + probAux;
        end
    end
end

% Meta
T(S,:,a) = 0; T(S,S,a) = 1;

%RIGHT
a = 3;
for y=1:Y
    for x=1:X
        s = (y-1)*X + x;

        probAux = prob;
        
        if (x == 1 || x == X || y == 1)
            nextx = min(x+1,X);
            nexty = y;
            nexts = (nexty-1)*X + nextx;
            
            T(s,nexts,a) = T(s,nexts,a) + 1;
        else
            nextx = min(x+1,X);
            nexty = y;
            nexts = (nexty-1)*X + nextx;
            
            T(s,nexts,a) = T(s,nexts,a) + (1-probAux);

            nextx = 1;
            nexty = Y;
            nexts = (nexty-1)*X + nextx;
            T(s,nexts,a) = T(s,nexts,a) + probAux;
        end
    end
end

% Meta
T(S,:,a) = 0; T(S,S,a) = 1;

