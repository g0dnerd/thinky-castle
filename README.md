# Thinky castle

castle that makes you go hmm

## Usage

- `conda env create -f environment.yml`
- `conda activate thinky-castle`
- Make a `MapLayer` with `m = MapLayer(n)`.
  - `m` then contains `n` x `n` `Node` (those are the squares from the original game).
- Add walls between two nodes with `m.add_wall(a: Square, b: Square)`.
  - We use `Square` to index into `MapLayer.nodes` so we don't have to pass around x and y coords a billion times
    - `Square(4, 3)` corresponds to e4, `Square(0,0)` to a1.
  - there's probably a much smarter graph-like implementation of this but I'm lazy and dumb
- A `Node` might want to contain stuff at some point, though it is currently too stupid to do so.
