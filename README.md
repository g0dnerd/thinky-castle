# Thinky castle

castle that makes you go hmm

## Usage

- `conda env create -f environment.yml`
- `conda activate thinky-castle`
- `python main.py` for a shitty little demo

## Classes

- A `Level` can hold one or more `MapLayer`s. These are vertically arranged.
  - A `Level` can be restricted or open in size
- `MapLayer(n)` creates a `MapLayer` with `n` x `n` `Node`s (the squares from the original game).
- Add walls between two `Node`s with `m.add_wall(a: Square, b: Square)`.
  - `Square(4, 3)` corresponds to e4, `Square(0,0)` to a1.
- A `Node` can contain zero or one `Prop`s like a `Ladder` that takes the player one `MapLayer` further up.
- A `Player` is currently technically an existent class.
