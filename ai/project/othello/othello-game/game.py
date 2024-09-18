import pygame
import sys
import time

import othello as oth

pygame.init()
size = width, height = 700, 700

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
green = (1, 50, 32)
gray = (150.2, 150.2, 150.2)
light_green = (140, 240, 140)

screen = pygame.display.set_mode(size)

mediumFont = pygame.font.Font("OpenSans-Regular.ttf", 28)
largeFont = pygame.font.Font("OpenSans-Regular.ttf", 40)
moveFont = pygame.font.Font("OpenSans-Regular.ttf", 60)

user = None
ai = None
board = oth.initial_state()
screen.fill(green)
player = None

def main():
    global player, user, ai

    # Draw title
    title = largeFont.render("Othello", True, white)
    author = mediumFont.render("By Luka M.S. and Pedro M.", True, white)
    titleRect = title.get_rect()
    authorRect = title.get_rect()
    titleRect.center = ((width / 2.05), 50)
    authorRect.center = ((width / 3), height - 100)
    screen.blit(title, titleRect)
    screen.blit(author, authorRect)

    # Draw buttons
    play_b_button = pygame.Rect((width / 2.75), (height / 3), width / 4, 50)
    play_b = mediumFont.render("Play as Black", True, white)
    play_b_rect = play_b.get_rect()
    play_b_rect.center = play_b_button.center
    pygame.draw.rect(screen, black, play_b_button)
    screen.blit(play_b, play_b_rect)

    play_w_button = pygame.Rect((width / 2.75), (height / 2), width / 4, 50)
    play_w = mediumFont.render("Play as White", True, black)
    play_w_rect = play_w.get_rect()
    play_w_rect.center = play_w_button.center
    pygame.draw.rect(screen, white, play_w_button)
    screen.blit(play_w, play_w_rect)

    selected = False
    while not selected:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        # Check if button is clicked
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if play_b_button.collidepoint(mouse):
                time.sleep(0.2)
                user = oth.B
                ai = oth.W
                player = oth.B
                selected = True
            elif play_w_button.collidepoint(mouse):
                time.sleep(0.2)
                user = oth.W
                ai = oth.B
                player = oth.B
                selected = True

        pygame.display.flip()
    game()


tile_size = 60
tile_origin = (width / 3.5 - (1.5 * tile_size),
                height / 3.5 - (1.5 * tile_size))

def game():
    global board, user, ai, player, tile_size, tile_origin

    # Draw the initial screen
    screen.fill(green)
    title = f"Player's Turns"
    title = largeFont.render(title, True, white)
    titleRect = title.get_rect()
    titleRect.center = ((width / 2), 30)
    screen.blit(title, titleRect)
    tiles = draw_board(board)
    pygame.display.flip()

    blacks = 2
    whites = 2
    game_done = False
    game_over = False
    possible_actions = None
    while not game_done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill(green)

        # Show title
        if game_over:
            time.sleep(0.6)
            winner = oth.winner(board, blacks, whites)
            if winner is None:
                title = f"Game Over: Tie."
            else:
                title = f"Game Over: {winner} wins."
        elif user == player:
            possible_actions = oth.actions(board, player)

            if len(possible_actions) == 0:
                if len(oth.actions(board, ai)) == 0 or whites == 0 or blacks == 0:
                    game_over = True
                    continue
                else:
                    time.sleep(0.3)
                    player = ai
                    continue
            title = f"Player's Turns"

            for action in possible_actions:

                rectTest = pygame.Rect(
                        tile_origin[1] + action[1] * tile_size,
                        tile_origin[0] + action[0] * tile_size,
                        tile_size, tile_size
                        )
                pygame.draw.circle(screen, light_green, rectTest.center, 20, 1)

            tiles = draw_board(board)
        else:
            possible_actions = oth.actions(board, player)
            if len(possible_actions) == 0:
                if len(oth.actions(board, user)) == 0 or whites == 0 or blacks == 0:
                    game_over = True
                    continue
                else:
                    player = user
                    continue
            else:
                title = f"Computer thinking..."

                tiles = draw_board(board)

        title = largeFont.render(title, True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 30)
        screen.blit(title, titleRect)

        # Check for AI move
        if not game_over:
            if player == ai:
                pygame.display.flip()
                move = oth.minimax(board, ai, possible_actions, whites, blacks)
                board, blacks, whites = oth.result(board, move, ai, blacks, whites)
                tiles = draw_board(board)

                player = user
            else:
                # Check for a user move
                click, _, _ = pygame.mouse.get_pressed()
                if click == 1:
                    mouse = pygame.mouse.get_pos()
                    for action in possible_actions:
                        if tiles[action[0]][action[1]].collidepoint(mouse):
                            board, blacks, whites = oth.result(board, action, player, blacks, whites)
                            tiles = draw_board(board)
                            player = ai

                tiles = draw_board(board)
        else:
            againButton = pygame.Rect(width / 3, height - 65, width / 3, 50)
            again = mediumFont.render("Play Again", True, black)
            againRect = again.get_rect()
            againRect.center = againButton.center
            pygame.draw.rect(screen, white, againButton)
            screen.blit(again, againRect)
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if againButton.collidepoint(mouse):
                    user = None
                    ai = None
                    board = oth.initial_state()
                    screen.fill(green)
                    player = None
                    main()

        pygame.display.flip()


def draw_board(board):
    global tile_origin, tile_size
    # Draw game board
    tiles = []
    for i in range(8):
        row = []
        for j in range(8):
            rect = pygame.Rect(
                tile_origin[0] + j * tile_size,
                tile_origin[1] + i * tile_size,
                tile_size, tile_size
            )
            pygame.draw.rect(screen, white, rect, 1)

            if board[i][j] != oth.EMPTY:
                if board[i][j] == oth.B:
                    pygame.draw.circle(screen, black, rect.center, 20)
                else:
                    pygame.draw.circle(screen, white, rect.center, 20)

            row.append(rect)
        tiles.append(row)
    return tiles


main()
