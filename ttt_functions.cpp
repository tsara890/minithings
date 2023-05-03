#include <iostream>
#include <vector>
#include <cstdlib>
#include <algorithm>
#include <string>

std::string board[9] = {"", "", "", "", "", "", "", "", ""};

void introduction();
void print_board();
void player_move();
void computer_move();
bool is_winner(std::string let, std::string board[]);

int main() {

  introduction();
  bool run = true;
  while (run) {
    player_move();
    print_board();
    computer_move();
    print_board();
    std::cout << "Computer played its move!\n";

    if (is_winner("X", board) || is_winner("O", board)) {
      run = false;
      std::cout << "Who won??\n";
    }
    }
  }

void print_board() {
  std::cout << "\n\n";
  std::cout <<  board[0] << " | " << board[1] << " | " << board[2] << "\n";
  std::cout << "---------\n";
  std::cout <<  board[3] << " | " << board[4] << " | " << board[5] << "\n";
  std::cout << "---------\n";
  std::cout <<  board[6] << " | " << board[7] << " | " << board[8] << "\n";
  std::cout << "\n\n\n";
  
}

void introduction() {
  char answer;
  std::cout << "----Hello! Welcome to----\n";
  std::cout << "-------TIC-TAC-TOE-------\n";
  std::cout << "       featuring:        \n";
  std::cout << "This is your board:\n";
  std::cout << " 0 | 1 | 2 \n";
  std::cout << "-----------\n";
  std::cout << " 3 | 4 | 5 \n";
  std::cout << "-----------\n";
  std::cout << " 6 | 7 | 8 \n";
  std::cout << "Press 'a' to begin!\n\n";
  std::cin >> answer;
  if (answer == 'a') {
    print_board();
  }
}

bool is_winner(std::string let, std::string board[]) {
  if (board[0] == let && board[1] == let && board[2] == let) {
    return true;
  } else if (board[3] == let && board[4] == let && board[5] == let) {
    return true;
  } else if (board[6] == let && board[7] == let && board[8] == let) {
    return true;
  } else if (board[0] == let && board[3] == let && board[6] == let) {
    return true;
  } else if (board[1] == let && board[4] == let && board[7] == let) {
    return true;
  } else if (board[2] == let && board[5] == let && board[8] == let) {
    return true;
  } else if (board[0] == let && board[4] == let && board[8] == let) {
    return true;
  } else if (board[2] == let && board[4] == let && board[6] == let) {
    return true;
  }
  else {
    return false;
  }
}

void player_move() {
  int answer;
  std::cout << "Pick a position to draw the X! (0-8)\n";
  std::cin >> answer;
  while (!(board[answer] == "")) {
    std::cout << "This spot is taken! Pick another:\n";
    std::cin >> answer; 
  }
  while (answer != 0 && answer != 1 && answer != 2 && answer != 3 && answer != 4 && answer != 5 && answer != 6 && answer != 7 && answer != 8) {
    std::cout << "Pick a valid position please!\n";
    std::cin >> answer;
    }
  board[answer] = "X";
}

void computer_move() {
  srand(time(NULL));
  int random_pos;
  std::string boardcopy[9];

  for (int i=0; i<=9; i++) {

    if (i<9) {
      std::copy(std::begin(board), std::end(board), std::begin(boardcopy));
      boardcopy[i] = "X";
      if (is_winner("X", boardcopy) && board[i] == "") {
        board[i] = "O";
        break;
      }
      else {
        std::copy(std::begin(board), std::end(board), std::begin(boardcopy));
        boardcopy[i] = "O";
        if (is_winner("O", boardcopy) && board[i] == "") {
          board[i] = "O";
          break;
        }
      }
    }
    else if (i==9) {
      do {
        random_pos = rand() % 9;
      } while (board[random_pos] != "");
        board[random_pos] = "O";
        break;
    }
  }
}


