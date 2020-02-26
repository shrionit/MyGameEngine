class A:
	pass

def add(a, b):
	return a+b
A.add = add
add.__set_name__(A, 'ad')
print(A.add(10, 20))