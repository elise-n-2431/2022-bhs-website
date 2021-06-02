i=42
t=1e-10
a=10
c=0
maxc=20
done=False
while not done:
    anew=0.5*(i/a+a)
    change=abs(a-anew)
    a=anew
    done=change<t or c>=maxc
    c=c+1
    print(a)
