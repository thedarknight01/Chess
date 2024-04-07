import chess
import chess.pgn
import chess.engine 
engine_path= "stockfish\stockfish-windows-x86-64-avx2.exe"

def evaluate_move(board, move):
    # Evaluate the move using a more balanced approach
    evaluation = 0
    if board.is_capture(move):
        evaluation += 0.5  # Capturing a piece
    if board.gives_check(move):
        evaluation += 0.3  # Giving check
    if board.is_check():
        evaluation -= 0.2  # Being in check is not ideal
    if board.is_attacked_by(not board.turn, move.to_square):
        evaluation -= 0.1  # Moving to a square under attack
    return evaluation

def analyze_game(pgn_file):
    # Load the PGN file
    try:
        with open(pgn_file) as f:
            game = chess.pgn.read_game(f)
    except IOError:
        print(f"Error: Unable to open file '{pgn_file}'")
        return

    if game is None:
        print("Error: No game found in the PGN file.")
        return

    # Initialize a chess engine for move evaluation
    engine = chess.engine.SimpleEngine.popen_uci(engine_path)

    board = game.board()
    for move in game.mainline_moves():
        # Make the move on the board
        board.push(move)
        # Evaluate the move
        evaluation = evaluate_move(board, move)
        if evaluation >= 1:
            print(f"Blunder: {move} - Evaluation: {evaluation}")
        elif evaluation > 0:
            print(f"Brilliant: {move} - Evaluation: {evaluation}")
        elif evaluation == 0:
            print(f"Miss: {move} - Evaluation: {evaluation}")

        # Get the best move from the engine
        result = engine.play(board, chess.engine.Limit(time=0.1))
        print(f"Best move: {result.move}")

    best_move = engine.play(board, chess.engine.Limit(time=0.1)).move
    print(f"Overall best move: {best_move}")

    engine.quit()

if __name__ == "__main__":
    pgn_file = "example.pgn"  # Change this to your PGN file
    analyze_game(pgn_file)
