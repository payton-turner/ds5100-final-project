import numpy as np
import pandas as pd
from typing import Union

class Die():
    """
    A class representing a 'N' sided die with 'W' weights, and can be rolled to select a face.
    
    For example, a fair “die” with N=2 is a coin, and a one with N=6 is a standard die. An unfair die is one where the weights are unequal.
    
    Attributes:
        sides (NumPy array): Array of sides as an argument, with data type as strings or numbers.
        __weightings (Pandas Data Frame): Data Frame with each of the sides of the die as the index and initializes the weights to  1.0 for each face but can be changed after the object is created. The weights are just positive numbers (integers or floats, including 0).
        
    Methods:
        weigh(): Change the weight of a single side.
        roll(): Roll the die one or more times.
        state(): Show the die’s current state.
    """
    
    def __init__(self, sides: np.ndarray):
        if not isinstance(sides, np.ndarray):
            raise TypeError(f"Takes a NumPy array of faces as an argument, got {type(sides)}.")
        if len(np.unique(sides)) != len(sides):
            raise ValueError("The array’s values must be distinct.")

        self.__weightings = pd.DataFrame({
            'Weights': np.ones(len(sides))},
        index=sides)
        
    def weigh(self, side: Union[int, float, str], weight: Union[int, float]):
        """
        Change the weight of a single side.
        
        Args:
            face (int, float, or str): The side value to be changed.
            weight (integer or float): The new weight for the given side.
        
        Returns:
            Changes the weight of a single side, nothing returned.
        """
        
        if side not in self.__weightings.index:
            raise IndexError(f"{side} is not one of the die's sides.")
        try:
            weight = float(weight)
        except (ValueError, TypeError):
            raise TypeError(f"Takes a numeric or castable to numeric value as an argument, got {type(weight)}.")
        
        self.__weightings.at[side, 'Weights'] = weight
        
    def roll(self, rolls: int = 1):
        """
        Roll the die one or more times.
        
        Args:
            rolls (int): Number of times the die is to be rolled; defaults to  1.
        
        Returns:
            Returns a list of outcomes.
        """
        
        if not isinstance(rolls, int):
            raise TypeError(f"Takes an integer as an argument, got {type(rolls)}.")
        if rolls < 1:
            raise ValueError("Number of rolls must be at least 1.")

        results = np.random.choice(
            self.__weightings.index,
            size=rolls,
            replace=True,
            p=self.__weightings['Weights'] / self.__weightings['Weights'].sum()
        ).tolist()
        return results
        
    def state(self):
        """
        Show the die’s current state.

        Args:
            None.
        
        Returns:
            Returns a copy of the private die data frame.
        """       
        return self.__weightings.copy()
        
    
class Game():
    """
    Play a game of rolling one or more similar dice, one or more times.
    
    Similar dice means that each die in a given game has the same number of sides and associated faces, but each die object may have its own weights. Game objects have a behavior to play a game, i.e. to roll all of the dice a given number of times.
    
    Attributes:
        dice (Python list): List of already instantiated similar dice from  the Die Class.
        __games (Pandas Data Frame): Saves the results from the play.
        
    Methods:
        play(): A method to play a number of games with the die.
        results(): Show the user the results of the most recent play.
    """
    def __init__(self, dice: list):
        if not isinstance(dice, list):
            raise TypeError(f"Takes a list as an argument, got {type(dice)}.")
        if not all(isinstance(i, Die) for i in dice):
            raise ValueError(f"Expected all list contents to be Die objects.")
        
        self.dice = dice
        self.__games = pd.DataFrame()
        
    
    def play(self, plays: int):
        """
        A method to play a number of games with the die.

        Args:
            plays (int): Takes an integer parameter to specify how many times the dice should be rolled.
        
        Returns:
            Updates the data frame with the game results, nothing returned.
        """     
        
        if not isinstance(plays, int):
            raise TypeError(f"Takes an integer as an argument, got {type(plays)}.")
        
        self.__games = pd.DataFrame(index=range(plays))
        self.__games.index.name = 'Roll Number'
        for i, die in enumerate(self.dice):
            rolls = die.roll(plays)
            self.__games[f'Die {i}'] = rolls
            

    def results(self, display: str = 'wide'):
        """
        Show the user the results of the most recent play.

        Args:
            display (str): Takes a parameter ('narrow' or 'wide') to return the data frame in narrow or wide form which defaults to wide form.
        
        Returns:
            Returns a copy of the private game data frame.
        """     
        if display not in ['wide', 'narrow']:
            raise ValueError("The user can only request 'narrow' or 'wide' Data Frame format.")
        
        if display.lower() == 'wide':
            wide = self.__games.copy().index.name
            return self.__games.copy()
        if display.lower() == 'narrow':
            narrow = self.__games.stack().to_frame('Face Rolled')
            narrow.index.names = ['Roll Number', 'Die']
            return narrow

class Analyzer():
    """
     Takes the results of a single game and computes various descriptive statistical properties about it.
        
    Attributes:
        game (object): Takes a game object already instanciated as its input parameter.
        
    Methods:
        jackpot(): Computes how many times the game resulted in a jackpot where a jackpot is a result in which all faces are the same.
        face_count(): Computes how many times a given face is rolled in each event.
        combo_count(): Computes the distinct combinations of faces rolled, along with their counts.
        permutation_count(): Computes the distinct permutations of faces rolled, along with their counts.
    """  
    def __init__(self, game):
        if not isinstance(game, Game):
            raise ValueError(f"Must be a game object. Got {type(game)} instead.")
        
        self.results = game.results()
    
    def jackpot(self):
        """
        Computes how many times the game resulted in a jackpot where a jackpot is a result in which all faces are the same, e.g. all ones for a six-sided die.
        
        Args:
            None.
        
        Returns:
            Returns an integer for the number of jackpots.
        """  
        return (self.results.nunique(axis=1) == 1).sum()
        
        # jackpot_count = 0
        # for i, row in self.results.iterrows():
        #     if row.nunique() == 1:
        #         jackpot_count += 1
        # return jackpot_count
        
    def face_count(self): # does this need to create columns for things that were never rolled???
        """
        Computes how many times a given face is rolled in each event.
        
        Args:
            None.
        
        Returns:
            Returns a data frame with the index as the roll number, face values as columns, and count values in the cells.
        """  
        face_counts = self.results.apply(pd.value_counts, axis=1)
        face_counts = face_counts.fillna(0).astype(int)
        face_counts.index.name = 'Roll Number'
        return face_counts
        
    def combo_count(self):
        """
        Computes the distinct combinations of faces rolled, along with their counts.
        
        Args:
            None.
        
        Returns:
            Returns a data frame of the MultiIndex of distinct combinations and a column for the associated counts.
        """  
        
        combinations = self.results.apply(lambda row: tuple(sorted(row)), axis=1)
        combo_counts = combinations.value_counts()
        return combo_counts.to_frame('Count')
        
    def permutation_count(self):
        """
        Computes the distinct permutations of faces rolled, along with their counts.
        
        Args:
            None.
        
        Returns:
            Returns a data frame of the MultiIndex of distinct permutations and a column for the associated counts.
        """  
        
        permutations = self.results.apply(lambda row: tuple(row), axis=1)
        permutations_counts = permutations.value_counts()
        return permutations_counts.to_frame('Count')