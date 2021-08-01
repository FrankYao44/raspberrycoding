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
	string name;
	list taste;
	A(string n, list t) : name(n), taste(t) {}
	int trade() {
		for (int &i in taste) {
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
	auto a = A();
	return a.trade();


}
int main() {
	auto result = func1();
	cout << result << std::endl;
	return 0;
}