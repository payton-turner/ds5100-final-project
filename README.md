# Monte Carlo Simulator

## Metadata

Author: Payton Turner
Project Name: Monte Carlo Simulator

## Synopsis

This project simulates rolling N-sided dice with W-weights a number of times in a game, as well as derives metrics for that game.

Included:
* A `Die` class to create'N' sided die with 'W' weights, and can be rolled to select a face. 
* A `Game` class to play a game of rolling one or more similar dice, one or more times.
* An `Analyzer` class to take the results of a single game and compute various descriptive statistical properties about it.


### Installation

Install the package locally with pip.

```bash
pip install .
```

### Import

Import NumPy (required to pass NumPy array of die faces) and Monte Carlo.

```python
import numpy as np
from montecarlo.montecarlo import Die, Game, Analyzer
```

### Create Dice

Pass a NumPy array to instantiate the Die class and create dice objects.

* In this case, two dice were created to have 6 sides, each with equal weight.
* Using the weigh() method, die2's face 6 was weighted to 5.
* The current sides and respective weights can be checked with the state() method.
git 
```python
sides = np.array([1, 2, 3, 4, 5, 6])
die1 = Die(sides)
die2 = Die(sides)
die2.weigh(6, 5)
die2.state()
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
* Using the jackpot() method, it will count the number of times the game resulted in a jackpot where all faces are the same.
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

## API Description

### Class: `Die`

A class representing a 'N' sided die with 'W' weights, and can be rolled to select a face.

For example, a fair “die” with N=2 is a coin, and a one with N=6 is a standard die. An unfair die is one where the weights are unequal.

#### Attributes:

* `sides` (NumPy array): Array of sides passed during initialization (can be strings or numbers).

#### Methods:

`__init__(sides: np.ndarray)`

- Docstring:  
    * Initializes the die with sides from a NumPy array and sets initial weights to 1.0 for each side.

- Parameters:
    * `sides` (`np.ndarray`): Array of sides as an argument, with data type as strings or numbers.

- Returns:  
    * Initializes the die object with sides and equal initial weights.

`weigh(side: Union[int, float, str], weight: Union[int, float])`

- Docstring:  
    * Change the weight of a single side.

- Parameters:
    * `side` (`int`, `float`, or `str`): The side value to be changed.
    * `weight` (`int` or `float`): The new weight for the given side.

- Returns:  
    * Nothing. Changes the weight of a single side.

`roll(rolls: int = 1)`

- Docstring:  
    * Roll the die one or more times.

- Parameters:
    * `rolls` (`int`, default=1): Number of times the die is to be rolled; defaults to  1.

- Returns:  
    * Returns a list of outcomes from the rolls.

`state()`

- Docstring:  
    * Show the die’s current state.

- Parameters:  
    * None.

- Returns:  
    * A copy of the private die data frame.

---

### Class: `Game`

Play a game of rolling one or more similar dice, one or more times.

Similar dice means that each die in a given game has the same number of sides and associated faces, but each die object may have its own weights. Game objects have a behavior to play a game, i.e. to roll all of the dice a given number of times.

#### Attributes:

* `dice` (Python list): List of already instantiated similar dice from the Die Class.

#### Methods:

`__init__(dice: list)`

- Docstring:  
    * Initializes the game with a list of Die objects.

- Parameters:
    * `dice` (`list`): A list of Die objects.

- Returns:  
    * Initializes a new game object.

`play(plays: int)`

- Docstring:  
    * A method to play a number of games with the die.

- Parameters:
    * `plays` (`int`): Takes an integer parameter to specify how many times the dice should be rolled.

- Returns:  
    * Nothing. Updates the data frame with the game results.

`results(display: str = 'wide')`

- Docstring:  
    * Show the user the results of the most recent play.

- Parameters:
    * `display` (`str`, default='wide'): Takes a parameter ('narrow' or 'wide') to return the data frame in narrow or wide form.

- Returns:  
    * A copy of the private game data frame.

---

### Class: `Analyzer`

Takes the results of a single game and computes various descriptive statistical properties about it.

#### Attributes:

* `results` (Pandas DataFrame): Takes a game object already instantiated as its input parameter and saves a copy of the results.

#### Methods:

`__init__(game: Game)`

- Docstring:  
    * Initializes the Analyzer with the results of a Game.

- Parameters:
    * `game` (`Game`): A Game object that has already been played.

- Returns:  
    * Initializes the Analyzer object.

`jackpot()`

- Docstring:  
    * Computes how many times the game resulted in a jackpot where a jackpot is a result in which all faces are the same, e.g., all ones for a six-sided die.

- Parameters:
    * None.

- Returns:  
    * Returns an integer for the number of jackpots.

`face_count()`

- Docstring:  
    * Computes how many times a given face is rolled in each event.

- Parameters:
    * None.

- Returns:  
    * Returns a DataFrame with the index as the roll number, face values as columns, and count values in the cells.

`combo_count()`

- Docstring:  
    * Computes the distinct combinations of faces rolled, along with their counts.

- Parameters:
    * None.

- Returns:  
    * Returns a DataFrame of the MultiIndex of distinct combinations and a column for the associated counts. Returns all faces, even if zero.

`permutation_count()`

- Docstring:  
    * Computes the distinct permutations of faces rolled, along with their counts.

- Parameters:
    * None.

- Returns:  
    * Returns a DataFrame of the MultiIndex of distinct permutations and a column for the associated counts.