# Monte Carlo Simulator

## Metadata

### Author: Payton Turner
### Project Name: Monte Carlo Simulator

## Synopsis

This project simulates rolling N-sided dice with W-weights a number of times in a game, as well as derives metrics for that game.

Included:
* A *Die* class to create'N' sided die with 'W' weights, and can be rolled to select a face. 
* A *Game* class to play a game of rolling one or more similar dice, one or more times.
* An *Analyzer* class to take the results of a single game and compute various descriptive statistical properties about it.


### Installation

Install the package locally with pip.

```bash
pip install .
```

### Import

Import NumpPy (required to pass NumPy array of die faces) and Monte Carlo.

```python
import numpy as np
from montecarlo.montecarlo import Die, Game, Analyzer
```

### Create Dice

Pass a NumPy array to instantiate the Die class and create die objects.

* In this case, two die were created to have 6 sides, each with equal weight.
* Using the weigh() method, die2's face 6 was weighted to 5.
* The current sides and respective weights can be checked with the state() method.

```python
sides = np.array([1, 2, 3, 4, 5, 6])
die1 = Die(sides)
die2 = Die(sides)
die2.weigh(6, 5)
die2.state
```

### Play Game

Pass a list of the two die to instantiate the Game class and create a game object.
* Using the play() method on the game, the die will be rolled 1000 times and results saved.
* The game results can be viewed with the results() method, defaulting to 'wide' view, but can be passed 'narrow' if preferred by the user.

```python
dice = [die1, die2]
game = Game(dice)
game.play(1000)
game.results()
```

### Analyze Game

Pass a game to instantiate the Analyzer class and create an analyzer object.
* Using the jackpot() method on the game, it will count the number of times the game resulted in a jackpot where all faces are the same.
* Using the face_count() method on the game, it will compute how many times a given face is rolled in each event.
* Using the combo_count() method on the game, it will compute the distinct combinations of faces rolled, along with their counts.
* Using the permutation_count() method on the game, it will compute the distinct permutations of faces rolled, along with their counts.
* jackpot() returns a number while face_count(), combo_count(), and permutation_count() return data frames.

```python
analyzer = Analyzer(game)
jackpot_count = analyzer.jackpot()
face_count = analyzer.face_count()
combo_count = analyzer.combo_count()
permutation_count = analyzer.permutation_count()
```