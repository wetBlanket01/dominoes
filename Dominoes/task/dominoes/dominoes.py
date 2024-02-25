import copy
from random import shuffle, choice


def is_num(num: str):
    try:
        int(num)
        return 1
    except ValueError:
        return 0


def is_legal_move(domino, snake_domino) -> bool:
    return snake_domino in domino


def is_valid_cmd(stack_list, cmd) -> bool:
    if not cmd and not is_num(cmd) or not stack_list:
        return False
    return False if abs(int(cmd)) - 1 > len(stack_list) else True


class Dominoes:
    def __init__(self):
        self.dominoes = [[i, j] for i in range(7) for j in range(i, 7)]
        self.domino_snake = []
        self.player_move_mess = "It's your turn to make a move. Enter your command."
        self.computer_move_mess = "Computer is about to make a move. Press Enter to continue..."
        self.status_list = [self.player_move_mess, self.computer_move_mess]
        self.game_end_mess_list = {
            'player': 'The game is over. You won!',
            'computer': 'The game is over. The computer won!',
            'draw': "The game is over. It's a draw!"
        }

        while True:
            shuffle(self.dominoes)
            self.stock = self.dominoes[:14]
            self.computer_stack = self.dominoes[14:21]
            self.player_stack = self.dominoes[21:28]

            max_double = max(max(self.player_stack), max(self.computer_stack))
            if max_double[0] == max_double[1]:
                break

        if max_double in self.player_stack:
            self.status_mess = self.computer_move_mess
            self.player_stack.remove(max_double)
        else:
            self.status_mess = self.player_move_mess
            self.computer_stack.remove(max_double)

        self.domino_snake.append(max_double)
        self.game_status()

    def game_status(self):
        border = '=' * 70
        print(border, f"Stock size: {len(self.stock)}", f"Computer pieces: {len(self.computer_stack)}", '', sep='\n')

        if len(self.domino_snake) <= 6:
            print(*self.domino_snake, sep='')
        else:
            print(*self.domino_snake[:3], '...', *self.domino_snake[-3:], sep='')

        print('\nYour pieces:')
        for i, domino in zip(range(1, len(self.player_stack) + 1), self.player_stack):
            print("{}:{}".format(i, domino))
        print()

        print(f"Status: {self.status_mess}")
        if self.status_mess not in self.game_end_mess_list.values():
            self.get_cmd(input())

    def get_cmd(self, cmd: str):
        stack_list = []
        if self.status_mess == self.player_move_mess and is_num(cmd):
            stack_list = self.player_stack
        elif self.status_mess == self.computer_move_mess and not cmd:
            cmd = self.comp_valid_moves(self.sort_domino_score(self.comp_moves_score())) + [0]
            cmd = cmd[0]
            stack_list = self.computer_stack
        if is_valid_cmd(stack_list, cmd):
            self.execute_cmd(stack_list, int(cmd))
        else:
            return self.get_cmd(input('Invalid input. Please try again.\n'))

    def execute_cmd(self, stack_list, cmd: int):
        if cmd == 0:
            stack_list.append(self.stock.pop(choice(range(len(self.stock))))) if len(self.stock) > 0 else None
        else:
            if is_legal_move(stack_list[abs(cmd) - 1],
                             self.domino_snake[0][0] if cmd < 0 else self.domino_snake[-1][-1]):
                self.add_domino(stack_list, stack_list[abs(cmd) - 1], cmd)
            else:
                return self.get_cmd(
                    input('Illegal move. Please try again.\n') if stack_list == self.player_stack else '')
        self.status_mess = self.status_list[self.status_list.index(self.status_mess) + 1 * -1]
        self.check_on_end(stack_list)
        return self.game_status()

    def add_domino(self, stack_list, domino, cmd) -> None:
        if cmd > 0:
            self.domino_snake.append(domino if self.domino_snake[-1][-1] == domino[0] else domino[::-1])
        else:
            self.domino_snake.insert(0, domino if self.domino_snake[0][0] == domino[-1] else domino[::-1])
        stack_list.remove(domino)

    def check_on_end(self, stack_list) -> bool:
        if len(stack_list) == 0:
            self.status_mess = self.game_end_mess_list.get('player' if stack_list == self.player_stack else 'computer')
            return True
        elif self.domino_snake[0][0] == self.domino_snake[-1][-1]:
            if sum(self.domino_snake[0][0] in dom for dom in stack_list) == 7:
                self.status_mess = self.game_end_mess_list.get('draw')
                return True
        return False

    def comp_moves_score(self) -> list:
        domino_score = copy.deepcopy(self.computer_stack)
        for num in range(7):
            count = 0
            for dom in self.domino_snake + self.computer_stack:
                if num == dom[0]:
                    count += 1
                if num == dom[1]:
                    count += 1
            for cs_index in range(len(self.computer_stack)):
                if self.computer_stack[cs_index][0] == num:
                    domino_score[cs_index][0] = count
                if self.computer_stack[cs_index][1] == num:
                    domino_score[cs_index][1] = count
        return domino_score

    def sort_domino_score(self, domino_score: list) -> list:
        sum_score = [sum(domino_score[i]) for i in range(len(self.computer_stack))]
        score_list = [(sum_score[i], self.computer_stack[i]) for i in range(len(self.computer_stack))]
        sorted_list = sorted(score_list, key=lambda x: x[0], reverse=True)
        return [sorted_list[i][1] for i in range(len(sorted_list))]

    def comp_valid_moves(self, stack_list) -> list:
        valid_moves = []
        for domino in stack_list:
            if self.domino_snake[-1][-1] in domino:
                valid_moves.append(self.computer_stack.index(domino) + 1)
            if self.domino_snake[0][0] in domino:
                valid_moves.append((self.computer_stack.index(domino) + 1) * -1)
        return valid_moves


game = Dominoes()
