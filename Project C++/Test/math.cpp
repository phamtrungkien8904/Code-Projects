#include "mymath.h"
using namespace std;

// Basic Calculator
int calculate(string s){
    stack<int> nums;
    stack<char> ops;
    int num = 0;
    char sign = '+';
    for(int i = 0; i < s.size(); i++){
        if(isdigit(s[i])){
            num = num * 10 + s[i] - '0';
        }
        if((!isdigit(s[i]) && s[i] != ' ') || i == s.size() - 1){
            if(sign == '+'){
                nums.push(num);
            }
            else if(sign == '-'){
                nums.push(-num);
            }
            else if(sign == '*'){
                int temp = nums.top();
                nums.pop();
                nums.push(temp * num);
            }
            else if(sign == '/'){
                int temp = nums.top();
                nums.pop();
                nums.push(temp / num);
            }
            sign = s[i];
            num = 0;
        }
    }
    int res = 0;
    while(!nums.empty()){
        res += nums.top();
        nums.pop();
    }
    return res;
}