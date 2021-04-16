#include <iostream>

using namespace std;

int main( int argc, char *argv[] )
  {
  std::string s;
  getline( cin, s );
  cout << argv[1] << ": " << s << endl;
  return 0;
  }