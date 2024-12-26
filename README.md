# Thinky castle

castle that makes you go hmm

## Usage

- `conda env create -f environment.yml`
- `conda activate thinky-castle`
- `python main.py` for a shitty little demo

## Classes

- A `Level` holds one or more layers (`game.level.Layer`). These are vertically arranged.
  - A `Level` can be restricted or open in size
- `Layer(n)` creates a `Layer` with `n` x `n` nodes (`game.level.Node`) (the squares from the original game).
- Add walls between two nodes with `m.add_wall(a: Square, b: Square)`.
  - `Square(4, 3)` corresponds to e4, `Square(0,0)` to a1.
- A `Node` can contain zero or one props (`game.props.Prop`) like a `Ladder` that takes the player one `Layer` further up.

## OpenGL

- aaaaah
