def write():
	f = open('ex_result2.txt', 'a')
	f.write('11\n')
	f.close()
	return 

def main():
	for x in range(3):
		write()
if __name__ == '__main__':
	main()
