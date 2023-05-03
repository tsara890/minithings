#include <iostream>
#include <vector>
#include <string>
#include <algorithm>

int main() {
  std::string input = "Hi Human!";

  std::transform(input.begin(), input.end(), input.begin(), ::tolower);
  std::vector<char> vowels = {'a', 'e', 'i', 'o', 'u', ',', '.', '!', '?'};
  std::vector<char> result;

  for (int i = 0; i < input.size(); i++) {
    for (int j = 0; j < vowels.size(); j++) {
      if (input[i] == vowels[j]) {
        result.push_back(vowels[j]);
      }
    }
    if (input[i] == 'e' || input[i] == 'u') {
      result.push_back(input[i]);
      }
    }
  /*char last_letter = (char)input.back();
  char exclamation_point = '!';
  if (last_letter == exclamation_point) {
    result.push_back(result[result.size()-2]);
    std::swap(result[result.size()-2], result[result.size()-1]);
  }*/
  for (int a = 0; a < input.length(); a++) {
    if (input[a] == '!') {
      int n = 1;

      while ((result[result.size()-n] == '.' || result[result.size()-n] == ',' || result[result.size()-n] == '?' || result[result.size()-n] == '!') && n < result.size()) {
        n++;
      }
      result.push_back(result[result.size()-n]);
      std::swap(result[result.size()-n], result[result.size()-n+1]);
    }
  }

  /*New and improved ^
    if there is any punctuation at the end of input, counter n will keep increasing
    untill it has reached a letter in result that is not punctuation, it will double it
    And for finishing, we swap the punctuation and letter so punctuation is still at the end of result
    !!Only works for one punctuation character, not many!!*/
  
  for (int k = 0; k <= result.size(); k++) {
    std::cout << result[k];
  }
}