#include <iostream>
#include <string>
#include <vector>

using std::cin;
using std::cout;
using std::vector;
using std::string;
typedef vector<int> list;

class A {
public:
	int price = 0;
	int & abc;
	string name{"121212"};
	list taste;
	A(string n, list t, int & sth) : name(n), taste(t),abc(sth) {}
	int trade() {
		for (int &i :taste) {
			cost += i;
		}
		profit = cost * 2;
		price = cost * 3;
		return price;
	}
private:
	int cost = 0;
	int profit = 0;
};

auto func1() {
	int ak = 1;
	auto a = A("ice cream", {12,3,4},ak);
	return a.trade();


}
int main() {
	auto result = func1();
	cout << result << std::endl;
	return 0;
}