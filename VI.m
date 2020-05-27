V = zeros(S,1);

V(S) = 0;

res = inf;

epsilon = 0.00001;
gamma = 1;

Q = zeros(S,A);

%% Versao com lacos


while res > epsilon
%     imshow(reshape(V,X,Y)',[-(2*Y+X) 0],'InitialMagnification','fit')
%     pause

    V_old = V;
    for s=1:S
        for a=1:A
            Q(s,a) = R(s,a);
            for sNext=1:S
               Q(s,a) =  Q(s,a) +  gamma*T(s,sNext,a)*V_old(sNext);
            end
        end
        [V(s) pi(s)] = max(Q(s,:));
    end
    
    res = 0;
    for s = 1:S
        dif = abs(V_old(s)-V(s));
        if dif > res
            res = dif;
        end
    end
    
end




%% Versao vetorial

residuos = [];

while res > epsilon
    for a=1:A
       Q(:,a) = R(:,a) +  gamma*T(:,:,a)*V;
    end
    V_old = V;
    [V pi] = max(Q,[],2);
    res = max(abs(V_old-V));
end

%%

reshape(V,X,Y)'

ind  = find( pi(:) == 1);
pi(ind) = '^';
ind  = find( pi(:) == 2);
pi(ind) = 'V';
ind  = find( pi(:) == 3);
pi(ind) = '>';
ind  = find( pi(:) == 4);
pi(ind) = '<';


disp(char(reshape(pi,X,Y)'))

imshow(reshape(V,X,Y)',[min(V) max(V)],'InitialMagnification','fit')