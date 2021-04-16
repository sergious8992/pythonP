#include <iostream>
#include <stdlib.h>
#include <fstream>
#include <thread> 
#include <atomic>
#include <chrono>
#include <string>

using namespace std;

atomic<bool> server_turn (false);

void reset_log(){
    ofstream txtlog ("log.txt", ios::out | ios::trunc);
    txtlog.close();
}

int count_lines(){
    string temp;
    int lines = 0;
    ifstream txtlog ("log.txt");
    if(txtlog.is_open()){
        while(getline(txtlog, temp)) lines++;
        txtlog.close();
    }
    return lines;
}

void read_log(){
    string actual_line;
    int lines = 0;
    static int last_read_line = 0;
    bool reading = true;
    while(reading){
        while(last_read_line == lines){
            lines = count_lines();
        } 
        ifstream txtlog ("log.txt");
        for(int i = 1; i <= lines; i++){
            getline(txtlog, actual_line, '\n');
            if(i > last_read_line){
                cout << actual_line << endl;
            }
        }
        last_read_line = lines;
    }
}

void bat(){
    this_thread::sleep_for(chrono::seconds(1));
    system("start.bat -l >log.txt");
}

void program(){
    string command;
    bool program_is_running = true;
    do{
        cout << "This is the program, write a command: ";
        getline(cin, command, '\n');
        cout << "\nThis is your command -> " << command << endl;
        if(command == "exit"){
            program_is_running = false;
        }
    }while(program_is_running);
}

int main(){

    cout << "Inicializating... \n\n";
    reset_log();
    thread programa(program), bato(bat), reading(read_log);
    programa.join();
    bato.join();

    return 0;
}