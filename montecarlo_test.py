import unittest
import numpy as np
import pandas as pd
from montecarlo.montecarlo import Die, Game, Analyzer
    
class DieTestSuite(unittest.TestCase):
    
    def test_1_weigh_change(self): 
        # create a six-sided die and change on of the side's weight
        array = np.array([1, 2, 3, 4, 5, 6])
        test_object = Die(array)
        test_object.weigh(6, 5)
        expected_weights = [1, 1, 1, 1, 1, 5]
        self.assertEqual(test_object.state()['Weights'].tolist(), expected_weights)
        
    def test_2_weigh_change_castable(self): 
        # create a six-sided die and change on of the side's weight with a castable string 
        array = np.array([1, 2, 3, 4, 5, 6])
        test_object = Die(array)
        test_object.weigh(6, "5")
        expected_weights = [1, 1, 1, 1, 1, 5]
        self.assertEqual(test_object.state()['Weights'].tolist(), expected_weights)

    def test_3_weigh_change_nonexistent(self): 
        # create a six-sided die and try to change a non-existent side's  weight
        array = np.array([1, 2, 3, 4, 5, 6])
        test_object = Die(array)
        self.assertRaises(IndexError, test_object.weigh, 10, 5)

    def test_4_weigh_change_noncastable(self): 
        # create a six-sided die and change on of the side's weight with a non-castable string 
        array = np.array([1, 2, 3, 4, 5, 6])
        test_object = Die(array)
        self.assertRaises(TypeError, test_object.weigh, 6, 'five')
    
    def test_5_roll_die(self): 
        # check length of list is equal to number of rolls
        array = np.array([1, 2, 3, 4, 5, 6])
        test_object = Die(array)
        self.assertEqual(len(test_object.roll(5)), 5)
   
    def test_6_roll_die_noninteger(self): 
        # try to roll a die a non-integer number of times
        array = np.array([1, 2, 3, 4, 5, 6])
        test_object = Die(array)
        self.assertRaises(TypeError, test_object.roll, 5.5)

    def test_7_roll_die_zero(self): 
        # try to roll a die 0 times
        array = np.array([1, 2, 3, 4, 5, 6])
        test_object = Die(array)
        self.assertRaises(ValueError, test_object.roll, 0)

    def test_8_state_type(self): 
        # make sure state returns a DataFrame
        array = np.array([1, 2, 3, 4, 5, 6])
        test_object = Die(array)
        self.assertIsInstance(test_object.state(), pd.DataFrame)
    
    def test_9_state_shape(self): 
        # make sure state returns a DataFrame of the right shape
        array = np.array([1, 2, 3, 4, 5, 6])
        test_object = Die(array)
        self.assertEqual(test_object.state().shape, (len(array), 1))


class GameTestSuite(unittest.TestCase):
    
    def test_1_init_not_list(self): 
        # create a game with a non-list
        array = np.array([1, 2, 3, 4, 5, 6])
        self.assertRaises(TypeError, Game, Die(array))
    
    def test_2_init_not_die(self): 
        # create a game with a list of non-die objects
        self.assertRaises(ValueError, Game, [1, 2, 3])
    
    def test_3_play_right_shape(self): 
        # create a game and check if it is the right shape
        array = np.array([1, 2, 3, 4, 5, 6])
        test_dice = [Die(array), Die(array)]
        test_game = Game(test_dice)
        plays = 10
        test_game.play(plays)
        self.assertEqual(test_game._Game__games.shape, (plays, len(test_dice)))
        
    def test_4_play_valid_faces(self): 
        # create a game and check that all rolls are valid faces
        array = np.array([1, 2, 3, 4, 5, 6])
        test_dice = [Die(array), Die(array)]
        test_game = Game(test_dice)
        plays = 3
        test_game.play(plays)
        for roll in test_game._Game__games['Die 0']:
            self.assertIn(roll, array)
 
    def test_5_results_invalid_format(self): 
        # check a result with an invalid format (not wide or narrow)
        array = np.array([1, 2, 3, 4, 5, 6])
        test_dice = [Die(array), Die(array)]
        test_game = Game(test_dice)
        plays = 5
        test_game.play(plays)
        self.assertRaises(ValueError, test_game.results, 'thin')

    def test_6_results_wide(self): 
        # check that wide result returns the right length and width data frame
        array = np.array([1, 2, 3, 4, 5, 6])
        test_dice = [Die(array), Die(array)]
        test_game = Game(test_dice)
        plays = 5
        test_game.play(plays)
        self.assertEqual(test_game.results('wide').shape, (plays, len(test_dice)))

  
    def test_7_results_narrow(self): 
        # check that narrow result returns the right length and width data frame
        array = np.array([1, 2, 3, 4, 5, 6])
        test_dice = [Die(array), Die(array)]
        test_game = Game(test_dice)
        plays = 5
        test_game.play(plays)
        self.assertEqual(test_game.results('narrow').shape, (plays*len(test_dice), 1))
      
class AnalyzerTestSuite(unittest.TestCase):

    def test_1_init_not_game(self): 
        # create analyzer with a non game
        self.assertRaises(ValueError, Analyzer, [1, 2, 3])
    
    def test_2_init_results_shape(self):
        # check analyzer results is the right size data frame
        array = np.array([1, 2, 3, 4, 5, 6])
        test_dice = [Die(array), Die(array)]
        test_game = Game(test_dice)
        plays = 5
        test_game.play(plays)
        test_analyzer = Analyzer(test_game)
        self.assertEqual(test_game.results().shape, test_analyzer.results.shape)

##
    def test_3_jackpot(self):
        # check analyzer results is the right size data frame
        array = np.array([1, 2, 3, 4, 5, 6])
        test_dice = [Die(array), Die(array)]
        test_game = Game(test_dice)
        plays = 5
        test_game.play(plays)
        test_analyzer = Analyzer(test_game)
        test_analyzer.results = pd.DataFrame({'Die 0': [1, 1, 3, 3, 5], 'Die 1': [1, 1, 2, 4, 5]})
        self.assertEqual(test_analyzer.jackpot(), 3)
        
    def test_4_face_count(self):
        # check face count is the right size data frame given faces rolled and number of rolls
        array = np.array([1, 2, 3, 4, 5, 6])
        test_dice = [Die(array), Die(array)]
        test_game = Game(test_dice)
        plays = 5
        test_game.play(plays)
        test_analyzer = Analyzer(test_game)
        test_analyzer.results = pd.DataFrame({'Die 0': [1, 1, 3, 3, 5], 'Die 1': [1, 1, 2, 4, 5]})
    #     expected_face_counts = pd.DataFrame({1: [2, 2, 0, 0, 0], 2: [0, 2, 0, 0], 3: [0, 0, 1, 1, 0], 4: [0, 0, 0, 0, 2], 5: [0, 0, 0, 0, 2], 6: [0, 0, 0, 0, 0]
    # })
        self.assertEqual(test_analyzer.face_count().shape, (plays, len(test_analyzer.results.stack().unique())))
        self.assertIsInstance(test_analyzer.face_count(), pd.DataFrame)

    def test_5_combo_count(self):
        # check combo count is the right size data frame given faces rolled and number of rolls, as well as right data type
        array = np.array([1, 2, 3, 4, 5, 6])
        test_dice = [Die(array), Die(array)]
        test_game = Game(test_dice)
        plays = 5
        test_game.play(plays)
        test_analyzer = Analyzer(test_game)
        test_analyzer.results = pd.DataFrame({'Die 0': [2, 3, 4, 3, 1], 'Die 1': [3, 2, 3, 2, 1]})
        expected_combos = {(1, 1): 1, (2, 3): 3, (3, 4): 1}
        self.assertEqual(test_analyzer.combo_count().shape, (len(expected_combos), 1))
        self.assertIsInstance(test_analyzer.combo_count(), pd.DataFrame)

    def test_6_permutation_count(self):
        # check permutation count is the right size data frame given faces rolled and number of rolls, as well as right data type
        array = np.array([1, 2, 3, 4, 5, 6])
        test_dice = [Die(array), Die(array)]
        test_game = Game(test_dice)
        plays = 5
        test_game.play(plays)
        test_analyzer = Analyzer(test_game)
        test_analyzer.results = pd.DataFrame({'Die 0': [2, 3, 4, 3, 1], 'Die 1': [3, 2, 3, 2, 1]})
        expected_permutations = {(2, 3): 1, (3, 2): 2, (1, 1): 1, (4, 3): 1}
        self.assertEqual(test_analyzer.permutation_count().shape, (len(expected_permutations), 1))
        self.assertIsInstance(test_analyzer.permutation_count(), pd.DataFrame)

        
if __name__ == '__main__': 
    unittest.main(verbosity=3)