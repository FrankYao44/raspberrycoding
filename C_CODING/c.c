# include <iostream>
# include <string>
# include <vector>

using std::string;
using std::cout;
using std::cin;
using std::vector;
typedef vector<int>::const_iterator clist;

int test1(){
	string a = "a string";
	string b;
	clist pp;
	vector<int> d(10,10);
	for (auto c:d){
		cout << c << "\n" << std::endl;
	}
	getline(cin, b);
	if (b == a){
		cout << "yes" << std::endl;
		return 0;
	} 
	else{
		cout << "fuck" << std::endl;
		return -1;
	}


}

int test2(){
	double a = 7.0 ;
	int c = 7;
	int b = 3;
	cout << b/a << b/c ;
	return 0;
}

int test3(){
	long a = -11;
	unsigned long b = 10;
	long *i = &a;
	i += 2;
	if (1){
	cout << a+b;
	}
	return 0;
}
int &test4(vector<int> & i){
	i.push_back(4);
	int p = 1;
	const int *a = &p;
	p =2;

	return i[3];


}
struct AClass {
	AClass() = default;
	AClass(int a, int b) : mem1(a*b){}
	AClass(int * const a) : mem1(*a){}
	AClass(const int * a) :mem1(*a){}
	int mem1 = 1;

};

int main(){
	int i = 1111;
	const int * a = &i;
	int * const  b = &i;
	AClass S ;
	cout <<AClass(1,2).mem1 <<"\n" << AClass(a).mem1 <<"\n"<< AClass(b).mem1<< "\n"<<S.mem1std::endl;
//	vector<int> i = {1,2,3};
//
//	int &a = test4(i);
//	a+=1;
//	cout << a<<i[3] << std::endl;
	return 0;
}
