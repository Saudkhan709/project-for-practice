#include <iostream>
#include <string>

int main() {
    // Variable to store user input
    std::string user_name;
    std::string user_age;

    // input to console
    std::cout << "Hello! I am your C++ System Agent." << std::endl;
    std::cout << "What is your name? ";
    std::cout << "what is your age? ";

    // Taking input
    std::getline(std::cin, user_name);
    // Taking output
    std::getline(std::cin, user_name);

    // Processing and Output
    std::cout << "Nice to meet you, " << user_name<< "! " 
              << "I am ready to process your commands." << std::endl;

    return 0;
}