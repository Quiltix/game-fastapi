from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.core.exceptions import NotFoundException, ConflictException
from src.db.models.game import PlayerSymbol, Game, GamePlayer, GameStatus, GameResult


def check_winner(board: str) -> PlayerSymbol | None:
    """Проверяет, есть ли победитель."""
    winning_combinations = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6),
    ]

    for combo in winning_combinations:

        cell1 = board[combo[0]]
        cell2 = board[combo[1]]
        cell3 = board[combo[2]]
        if cell1 == cell2 == cell3 and cell1 != '_':
            return PlayerSymbol(cell1)

    return None


async def create_new_game(db: AsyncSession, user_id: int) -> Game:
    """Создает новую игру для пользователя."""
    new_game = Game(status=GameStatus.PENDING)

    first_player = GamePlayer(
        user_id=user_id,
        game=new_game,
        symbol=PlayerSymbol.X
    )

    db.add(new_game)
    db.add(first_player)

    await db.flush()
    await db.refresh(new_game)

    created_game_id = new_game.id
    return await get_game_by_id(db, created_game_id)


async def process_player_move(db: AsyncSession, game_id: int, user_id: int, position: int) -> Game:
    """Обрабатывает ход игрока, обновляет состояние игры и возвращает обновленный объект игры."""
    game = await get_game_by_id(db, game_id)

    if game.status != GameStatus.IN_PROGRESS:
        raise ConflictException(detail="Игра не активна.")

    if not (0 <= position < 9):
        raise ConflictException(detail="Некорректная позиция для хода.")

    player_entry = next((p for p in game.player_associations if p.user_id == user_id), None)
    if not player_entry:
        raise ConflictException( detail="Вы не являетесь участником этой игры.")

    player_symbol = player_entry.symbol
    turn = PlayerSymbol.X if game.board_state.count('X') == game.board_state.count('O') else PlayerSymbol.O

    if player_symbol != turn:
        raise ConflictException(detail="Сейчас не ваш ход.")

    board_list = list(game.board_state)
    if board_list[position] != '_':
        raise ConflictException(detail="Эта клетка уже занята.")

    board_list[position] = player_symbol.value
    game.board_state = "".join(board_list)

    winner_symbol = check_winner(game.board_state)
    is_draw = '_' not in game.board_state

    if winner_symbol:
        game.status = GameStatus.COMPLETED
        game.result = GameResult.X_WINS if winner_symbol == PlayerSymbol.X else GameResult.O_WINS
        winner_entry = next(p for p in game.player_associations if p.symbol == winner_symbol)
        game.winner_id = winner_entry.user_id
        game.finished_at = func.now()
    elif is_draw:
        game.status = GameStatus.COMPLETED
        game.result = GameResult.DRAW
        game.finished_at = func.now()

    await db.flush()
    return await get_game_by_id(db, game_id)


async def get_game_by_id(db: AsyncSession, game_id: int) -> Game:
    """Функция для получения игры"""
    query = (
        select(Game)
        .where(Game.id == game_id)
        .options(
    selectinload(Game.player_associations).selectinload(GamePlayer.user),
            selectinload(Game.winner)
        )
    )
    result = await db.execute(query)
    game = result.scalar_one_or_none()
    if not game:
        raise NotFoundException(detail="Игра не найдена.")
    return game


async def add_player_to_game(db: AsyncSession, game_id: int, user_id: int) -> Game:
    """Добавляет второго игрока в игру, меняет статус и возвращает обновленный объект игры."""
    game = await get_game_by_id(db, game_id)

    if game.status != GameStatus.PENDING:
        raise ConflictException(detail="Нельзя присоединиться к этой игре. Она уже началась или завершена.")

    if len(game.player_associations) >= 2:
        raise ConflictException(detail="В этой игре уже максимальное количество игроков.")

    is_already_player = any(p.user_id == user_id for p in game.player_associations)
    if is_already_player:
        raise ConflictException(detail="Вы уже являетесь участником этой игры.")

    new_game_player = GamePlayer(
        user_id=user_id,
        game_id=game_id,
        symbol=PlayerSymbol.O
    )
    db.add(new_game_player)

    game.status = GameStatus.IN_PROGRESS

    await db.flush()

    return await get_game_by_id(db, game_id)

async def get_available_games(db: AsyncSession) -> list[Game]:
    """Возвращает список игр, ожидающих второго игрока."""
    query = (
        select(Game)
        .where(Game.status == GameStatus.PENDING)
        .options(selectinload(Game.player_associations).selectinload(GamePlayer.user))
        .order_by(Game.created_at.desc())
    )
    result = await db.execute(query)
    return list(result.scalars().all())

async def get_user_game_history(db: AsyncSession, user_id: int) -> list[Game]:
    """Возвращает историю завершенных игр для конкретного пользователя."""
    query = (
        select(Game)
        .join(Game.player_associations)
        .where(GamePlayer.user_id == user_id, Game.status == GameStatus.COMPLETED)
        .options(selectinload(Game.player_associations).selectinload(GamePlayer.user))
        .order_by(Game.finished_at.desc())
    )
    result = await db.execute(query)
    return list(result.scalars().all())

async def get_all_completed_games(db: AsyncSession) -> list[Game]:
    """Возвращает список завершенных игр.
    Отсортированный по дате завершения."""
    query = (
        select(Game)
        .join(Game.player_associations)
        .where(Game.status == GameStatus.COMPLETED)
        .options(selectinload(Game.player_associations).selectinload(GamePlayer.user))
        .order_by(Game.finished_at.desc())
    )
    result = await db.execute(query)
    return list(result.scalars().all())

