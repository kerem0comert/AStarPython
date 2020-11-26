from Candidate import Candidate

a = Candidate(5,3,2,1)
b = Candidate(2,4,2,2)
c = Candidate(5,3,2,4)

l1 = [a,b]

print(any(p.__eq__(d) for p in l1))