class SnakeGame:

    def __init__(self, width=20, height=20):

        self.width = width
        self.height = height

        self.reset()


    def reset(self):

        self.snake = [
            (10, 10),
            (9, 10),
            (8, 10)
        ]

        self.direction = (1, 0)

        self.score = 0

        self.game_over = False


    def change_direction(self, direction):

        dx, dy = direction

        current_dx, current_dy = self.direction

        # 반대 방향 금지
        if (
            dx == -current_dx and
            dy == -current_dy
        ):
            return

        self.direction = direction


    def move(self):

        if self.game_over:
            return

        head_x, head_y = self.snake[0]

        dx, dy = self.direction

        new_head = (
            head_x + dx,
            head_y + dy
        )

        # 벽 충돌
        if (
            new_head[0] < 0 or
            new_head[0] >= self.width or
            new_head[1] < 0 or
            new_head[1] >= self.height
        ):

            self.game_over = True

            return

        # 몸 충돌
        if new_head in self.snake:

            self.game_over = True

            return

        self.snake.insert(
            0,
            new_head
        )


    def get_score(self):

        return self.score
