# AGENTS

## Project Overview
- Python/Pygame Tetris implementation in `tetris/` package.
- Entry point: `python -m tetris.main`.
- Dependencies: `pip install -r requirements.txt`.

## Architecture Notes
- Core gameplay logic is in `tetris/core` and is Pygame-free for board/piece/score.
- Rendering and UI are isolated in `tetris/systems` and `tetris/ui`.
- Fixed timestep loop lives in `tetris/main.py`.
