# Thinky castle

castle that makes you go hmm

## Usage

- `conda env create -f environment.yml`
- `conda activate thinky-castle`
- Make `MapLayer`s with `m = MapLayer(n)`.
  - `m` then contains `n` x `n` `Node`s (which the squares from the original game).
- Add walls between squares with `m.add_wall(a, b)`.
  - `a` and `b` are `Square`s, which are used to index into a `MapLayer`s `Node`s so we don't have to pass around x and y coords a billion times
    - `Square(4, 3)` corresponds to e4, `Square(0,0)` to a1.
- `Node`s might want to contain stuff at some point, though they currently are too stupid to do so.
