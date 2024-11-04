#include <iostream>
#include <string>
using namespace std;

class Employee {
    private:
        string name;
        int salary;
    public:
        void getSalary(int s){
            salary = s;
        }
        int getSalary(){
            return salary;
        }
        void getName(string n){
            name = n;
        }
        string getName(){
            return name;
        }
};

int main() {
    Employee emp1;
    emp1.getName("John Doe");
    emp1.getSalary(100000);
    cout << emp1.getName() << " earns " << emp1.getSalary() << " per year." << endl;
//    cout << "The salary of " << emp1.getName() << " is " << emp1.salary << " per year." << endl;
    return 0;
}