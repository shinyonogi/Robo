#!/usr/bin/env python3

import unittest
from planet import Direction, Planet


class ExampleTestPlanet(unittest.TestCase):
    def setUp(self):
        """
        Instantiates the planet data structure and fills it with paths

        +--+
        |  |
        +-0,3------+
           |       |
          0,2-----2,2 (target)
           |      /
        +-0,1    /
        |  |    /
        +-0,0-1,0
           |
        (start)

        """
        # Initialize your data structure here
        self.planet = Planet()
        self.planet.add_path(((0, 0), Direction.NORTH), ((0, 1), Direction.SOUTH), 1)
        self.planet.add_path(((0, 1), Direction.WEST), ((0, 0), Direction.WEST), 1)

    @unittest.skip('Example test, should not count in final test results')
    def test_target_not_reachable_with_loop(self):
        """
        This test should check that the shortest-path algorithm does not get stuck in a loop between two points while
        searching for a target not reachable nearby

        Result: Target is not reachable
        """
        self.assertIsNone(self.planet.shortest_path((0, 0), (1, 2)))


class RoboLabPlanetTests(unittest.TestCase):

    #Funktioniert nur mit Planet (1) Klasse 

    def setUp(self):
        """
        Instantiates the planet data structure and fills it with paths

        MODEL YOUR TEST PLANET HERE (if you'd like):

        (loop2)(1, 6) -  +   -   +
                                   |
              (1, 5)    +   -    (3, 5)
                 |      |        |
                 +      +        (3, 4)
                 |      |        |
        (loop)(1, 3) - (2, 3)    +
                        |        |
              (1, 2) - +       (3, 2)
                 |               |
              (1, 1) - (2, 1) -  +
                 |
                 (start)

        """
        # Initialize your data structure here
        self.planet = Planet()
        # self.planet.add_path(...)

        self.planet.add_path(((1, 1), Direction.EAST), ((2, 1), Direction.WEST), 1)
        self.planet.add_path(((1, 1), Direction.NORTH), ((1, 2), Direction.SOUTH), 1)
        self.planet.add_path(((2, 1), Direction.EAST), ((3, 2), Direction.SOUTH), 2)
        self.planet.add_path(((3, 2), Direction.NORTH), ((3, 4), Direction.SOUTH), 2)
        self.planet.add_path(((3, 4), Direction.NORTH), ((3, 5), Direction.SOUTH), 1)
        self.planet.add_path(((3, 5), Direction.NORTH), ((1, 6), Direction.EAST), 3)
        self.planet.add_path(((1, 6), Direction.WEST), ((1, 6), Direction.SOUTH), 2)
        self.planet.add_path(((1, 2), Direction.EAST), ((2, 3), Direction.SOUTH), 2)
        self.planet.add_path(((2, 3), Direction.WEST), ((1, 3), Direction.EAST), 1)
        self.planet.add_path(((1, 3), Direction.WEST), ((1, 3), Direction.SOUTH), 1)
        self.planet.add_path(((2, 3), Direction.NORTH), ((3, 5), Direction.WEST), 3)
        self.planet.add_path(((1, 3), Direction.NORTH), ((1, 5), Direction.SOUTH), 2)

    def test_add_get_paths(self):
        # print(self.planet.get_paths()) #prints all the paths (for us)
        return

    def test_shortest_path_opposite_path_1(self):
        #checks if two opposite ways return the same (opposite) shortest path 
        shortest_path = self.planet.shortest_path((1, 6), (1, 1))
        self.assertEqual(shortest_path[0], ((1, 6), Direction.EAST))
        self.assertEqual(shortest_path[1], ((3, 5), Direction.SOUTH))
        self.assertEqual(shortest_path[2], ((3, 4), Direction.SOUTH))
        self.assertEqual(shortest_path[3], ((3, 2), Direction.SOUTH))
        self.assertEqual(shortest_path[4], ((2, 1), Direction.WEST))


        shortest_path = self.planet.shortest_path((1, 1), (1, 6))
        self.assertEqual(shortest_path[0], ((1, 1), Direction.EAST))
        self.assertEqual(shortest_path[1], ((2, 1), Direction.EAST))
        self.assertEqual(shortest_path[2], ((3, 2), Direction.NORTH))
        self.assertEqual(shortest_path[3], ((3, 4), Direction.NORTH))
        self.assertEqual(shortest_path[4], ((3, 5), Direction.NORTH))

    def test_start_with_loop(self):
        #checks if the search for the shortest path doesn't stuck when it begins with a loop
        shortest_path = self.planet.shortest_path((1, 5), (2, 3))
        self.assertEqual(shortest_path[0], ((1, 5), Direction.SOUTH))
        self.assertEqual(shortest_path[1], ((1, 3), Direction.EAST))

        try:
            if shortest_path[2] is tuple:  # checks if there's a third element
                self.fail("FAIL")
        except:
            return

    def test_end_with_loop(self):
        #checks if the search for the shortest path doesn't stuck in a loop when it ends with a loop
        shortest_path = self.planet.shortest_path((2, 3), (1, 5))
        self.assertEqual(shortest_path[0], ((2, 3), Direction.WEST))
        self.assertEqual(shortest_path[1], ((1, 3), Direction.NORTH))

        try:
            if shortest_path[2] is tuple:  # checks if the loop stops
                self.fail("FAIL")
        except:
            return

    def test_integrity(self):
        """
        This test should check that the dictionary returned by "planet.get_paths()" matches the expected structure
        """
        test_get_paths = self.planet.get_paths()
        integrity = True
        direction_type = type(test_get_paths[(1, 1)][Direction.EAST][1])

        for i in test_get_paths:
            if type(i) is tuple:
                for j in test_get_paths[i]:
                    if ((type(j) is direction_type)
                            and (type(test_get_paths[i][j][0]) is tuple)
                            and (type(test_get_paths[i][j][1]) is direction_type)
                            and (type(test_get_paths[i][j][2]) is int)):
                        continue
                    else:
                        integrity = False
            else:
                integrity = False

        self.assertEqual(integrity, True)

    def test_empty_planet(self):
        """
        This test should check that an empty planet really is empty
        """
        empty_planet = Planet() #initializes an empty planet 

        self.assertEqual(empty_planet.get_paths(), {})

    def test_target(self):
        """
        This test should check that the shortest-path algorithm implemented works.

        Requirement: Minimum distance is three nodes (two paths in list returned)
        """
        test_shortest_path = self.planet.shortest_path((1, 1), (3, 4))

        if ((test_shortest_path[0] != ((1, 1), Direction.EAST))
                or (test_shortest_path[1] != ((2, 1), Direction.EAST))
                or (test_shortest_path[2] != ((3, 2), Direction.NORTH))):
            self.fail("FAIL")
    
    def test_target_not_reachable(self):
        """
        This test should check that a target outside the map or at an unexplored node is not reachable
        """
        test_shortest_path = self.planet.shortest_path((1, 1), (6, 5))

        self.assertIsNone(test_shortest_path)

    def test_same_length(self):
        """
        This test should check that the shortest-path algorithm implemented also can return alternatives with the
        same cost (weights)

        Requirement: Minimum of two paths with same cost exists, only one is returned by the logic implemented
        """

        test_shortest_path_1 = self.planet.shortest_path((1, 1), (3, 5))

        self.assertEqual(test_shortest_path_1[0], ((1, 1), Direction.EAST))     
        self.assertEqual(test_shortest_path_1[1], ((2, 1), Direction.EAST))
        self.assertEqual(test_shortest_path_1[2], ((3, 2), Direction.NORTH))
        self.assertEqual(test_shortest_path_1[3], ((3, 4), Direction.NORTH))


    def test_target_with_loop(self):
        """
        This test should check that the shortest-path algorithm does not get stuck in a loop between two points while
        searching for a target nearby

        Result: Target is reachable
        """
        test_shortest_path = self.planet.shortest_path((2, 3), (1, 5))

        if ((test_shortest_path[0] != ((2, 3), Direction.WEST))
                or (test_shortest_path[1] != ((1, 3), Direction.NORTH))):
            self.fail("FAIL")

    def test_target_not_reachable_with_loop(self):
        """
        This test should check that the shortest-path algorithm does not get stuck in a loop between two points while
        searching for a target not reachable nearby

        Result: Target is not reachable
        """
        test_shortest_path = self.planet.shortest_path((1, 5), (6, 5))

        self.assertIsNone(test_shortest_path)


    def test_depth_first_search(self):

        test_planet = Planet()

        test_planet.depth_first_add_stack((300, 300), Direction.NORTH)

        #print(test_planet.depth_first_stack)

        test = (test_planet.depth_first_search((300, 300)))

        #print(test)
        
        test_planet.depth_first_add_reached((300, 300), Direction.NORTH)

        test_planet.add_path(((300, 300), Direction.NORTH), ((300, 301), Direction.SOUTH), 1)

        test_planet.depth_first_add_stack((300, 301), Direction.NORTH)
        test_planet.depth_first_add_stack((300, 301), Direction.EAST)
        test_planet.depth_first_add_stack((300, 301), Direction.WEST)
        test_planet.depth_first_add_stack((300, 301), Direction.SOUTH)

        test_planet.add_path(((300, 301), Direction.NORTH),  ((300, 301), Direction.EAST), 1)

        test = test_planet.depth_first_search((300, 301))
        test_planet.depth_first_add_reached((300, 301), Direction.WEST)

        #print(test)

        test_planet.add_path(((300, 301), Direction.WEST), ((301, 300), Direction.EAST), 1)

        test_planet.depth_first_add_stack((301, 300), Direction.WEST)
        test_planet.depth_first_add_stack((301, 300), Direction.SOUTH)
        test_planet.depth_first_add_stack((301, 300), Direction.NORTH)
        test_planet.depth_first_add_stack((301, 300), Direction.EAST)

        test = test_planet.depth_first_search((301, 300))
        test_planet.depth_first_add_reached((301, 300), Direction.SOUTH)
        
        #print(test)


    def test_andre(self):

        """
        PLANET: HASSELHOFF

        (loop1) (0, 3)   -   +   -   +
                                     |
                    +    - (1, 2) -  (2, 2)
                    |                |
                (0, 1)   - (1, 1)    +
                    |        |       |
                (0, 0)       +   -  (2, 0)
                                     |
                                    (BLOCKED)
                    
        """

        test_planet = Planet()

        #First point (0, 0)
        test_planet.depth_first_add_stack((0, 0), Direction.NORTH)
        test_planet.add_andre((0, 0))

        select_path = test_planet.depth_first_search((0, 0))
        self.assertEqual(select_path, [((0, 0), Direction.NORTH)])
        test_planet.depth_first_add_reached((0, 0), Direction.NORTH)

        test_planet.add_path(((0, 0), Direction.NORTH), ((0, 1), Direction.SOUTH), 4)


        #Second point (0, 1)
        test_planet.depth_first_add_stack((0, 1), Direction.NORTH)
        test_planet.depth_first_add_stack((0, 1), Direction.SOUTH)
        test_planet.depth_first_add_stack((0, 1), Direction.EAST)
        test_planet.add_andre((0, 1))

        select_path = test_planet.depth_first_search((0, 1))
        self.assertEqual(select_path, [((0, 1), Direction.NORTH)])
        test_planet.depth_first_add_reached((0, 1), Direction.NORTH)

        test_planet.add_path(((0, 1), Direction.NORTH), ((1, 2), Direction.WEST), 10)


        #Third point (1, 2)
        test_planet.depth_first_add_stack((1, 2), Direction.EAST)
        test_planet.depth_first_add_stack((1, 2), Direction.WEST)
        test_planet.add_andre((1, 2))

        select_path = test_planet.depth_first_search((1, 2))
        self.assertEqual(select_path, [((1, 2), Direction.EAST)])
        test_planet.depth_first_add_reached((1, 2), Direction.EAST)

        test_planet.add_path(((1, 2), Direction.EAST), ((2, 2), Direction.WEST), 7)


        #Fourth point (2, 2)
        test_planet.depth_first_add_stack((2, 2), Direction.NORTH)
        test_planet.depth_first_add_stack((2, 2), Direction.SOUTH)
        test_planet.add_andre((2, 2))

        select_path = test_planet.depth_first_search((2, 2))
        self.assertEqual(select_path, [((2, 2), Direction.NORTH)])
        test_planet.depth_first_add_reached((2, 2), Direction.NORTH)

        test_planet.add_path(((2, 2), Direction.NORTH), ((0, 3), Direction.EAST), 3)



        #Fifth point (0, 3)
        test_planet.depth_first_add_stack((0, 3), Direction.SOUTH)
        test_planet.depth_first_add_stack((0, 3), Direction.WEST)
        test_planet.add_andre((0, 3))

        test_planet.add_path(((0, 1), Direction.EAST), ((1, 1), Direction.WEST), 1)
        test_planet.add_path(((1, 1), Direction.SOUTH), ((2, 0), Direction.WEST), 1)
        test_planet.add_path(((2, 0), Direction.NORTH), ((2, 2), Direction.SOUTH), 2)

        select_path = test_planet.depth_first_search((0, 3))
        self.assertEqual(select_path, [((0, 3), Direction.SOUTH)])
        test_planet.depth_first_add_reached((0, 3), Direction.SOUTH)


        #Sixth point (3, 0)
        test_planet.add_path(((0, 3), Direction.SOUTH), ((0, 3), Direction.WEST), 4)
        
        select_path = test_planet.depth_first_search((0, 3))
        self.assertEqual(select_path[0], ((0, 3), Direction.EAST))
        self.assertEqual(select_path[1], ((2, 2), Direction.SOUTH))
        self.assertEqual(select_path[2], ((2, 0), Direction.WEST))
        test_planet.depth_first_add_reached((0, 3), Direction.EAST)

        #Seventh point (2, 0)

        test_planet.depth_first_add_stack((2, 0), Direction.SOUTH)
        test_planet.depth_first_add_stack((2, 0), Direction.NORTH)
        test_planet.depth_first_add_stack((2, 0), Direction.WEST)
        test_planet.add_andre((2, 0))

        test_planet.add_path(((2, 2), Direction.SOUTH), ((2, 0), Direction.NORTH), 2)
        
        select_path = test_planet.depth_first_search((2, 0))
        self.assertEqual(select_path, [((2, 0), Direction.SOUTH)])
        test_planet.depth_first_add_reached((2, 0), Direction.SOUTH)


        #Eith point (2, 0):

        select_path = test_planet.depth_first_search((2, 0))
        self.assertEqual(select_path, [((2, 0), Direction.WEST)])


    
    def test_grommit(self):

        grommit = Planet()

        #First point (-1, -2):

        grommit.depth_first_add_stack((-1, -2), Direction.NORTH)
        grommit.add_andre((-1, -2))

        select_path = grommit.depth_first_search((-1, -2))
        self.assertEqual(select_path, [((-1, -2), Direction.NORTH)])

        grommit.depth_first_add_reached((-1, -2), Direction.NORTH)



        #Second point (-1, -1):

        grommit.add_path(((-1, -2), Direction.NORTH), ((-1, -1), Direction.SOUTH), 1)

        grommit.depth_first_add_stack((-1, -1), Direction.NORTH)
        grommit.depth_first_add_stack((-1, -1), Direction.SOUTH)
        grommit.add_andre((-1, -1))

        select_path = grommit.depth_first_search((-1, -1))
        self.assertEqual(select_path, [((-1, -1), Direction.NORTH)])

        grommit.depth_first_add_reached((-1, -1), Direction.NORTH)

        #Third point (-1, 1):

        grommit.add_path(((-1, -1), Direction.NORTH), ((-1, 1), Direction.SOUTH), 1)

        grommit.depth_first_add_stack((-1, 1), Direction.NORTH)
        grommit.depth_first_add_stack((-1, 1), Direction.SOUTH)
        grommit.add_andre((-1, 1))

        select_path = grommit.depth_first_search((-1, 1))
        self.assertEqual(select_path, [((-1, 1), Direction.NORTH)])

        grommit.depth_first_add_reached((-1, 1), Direction.NORTH)

        #Fourth point (-2, 2):

        grommit.add_path(((-1, 1), Direction.NORTH), ((-2, 2), Direction.EAST), 1)

        grommit.depth_first_add_stack((-2, 2), Direction.WEST)
        grommit.depth_first_add_stack((-2, 2), Direction.SOUTH)
        grommit.depth_first_add_stack((-2, 2), Direction.EAST)
        grommit.add_andre((-2, 2))

        select_path = grommit.depth_first_search((-2, 2))
        self.assertEqual(select_path, [((-2, 2), Direction.SOUTH)])

        grommit.add_path(((-3, -1), Direction.NORTH), ((-3, -1), Direction.WEST), 1)

        grommit.depth_first_add_reached((-2, 2), Direction.SOUTH)

        #Fifth point (-2, 1):

        grommit.add_path(((-2, 2), Direction.SOUTH), ((-2, 1), Direction.NORTH), 1)

        grommit.depth_first_add_stack((-2, 1), Direction.SOUTH)
        grommit.depth_first_add_stack((-2, 1), Direction.NORTH)
        grommit.depth_first_add_stack((-2, 1), Direction.WEST)
        grommit.add_andre((-2, 1))

        select_path = grommit.depth_first_search((-2, 1))
        self.assertEqual(select_path, [((-2, 1), Direction.SOUTH)])

        grommit.depth_first_add_reached((-2, 1), Direction.SOUTH)

        #Sixth point (-2, 0):

        grommit.add_path(((-2, 1), Direction.SOUTH), ((-2, 0), Direction.NORTH), 1)

        grommit.depth_first_add_stack((-2, 0), Direction.SOUTH)
        grommit.depth_first_add_stack((-2, 0), Direction.NORTH)
        grommit.depth_first_add_stack((-2, 0), Direction.WEST)
        grommit.add_andre((-2, 0))

        select_path = grommit.depth_first_search((-2, 0))
        self.assertEqual(select_path, [((-2, 0), Direction.SOUTH)])

        grommit.depth_first_add_reached((-2, 0), Direction.SOUTH)


        #Seventh point (-2, -1):

        grommit.add_path(((-2, 0), Direction.SOUTH), ((-2, -1), Direction.NORTH), 1)

        grommit.depth_first_add_stack((-2, -1), Direction.SOUTH)
        grommit.depth_first_add_stack((-2, -1), Direction.NORTH)
        grommit.depth_first_add_stack((-2, -1), Direction.WEST)
        grommit.add_andre((-2, -1))

        select_path = grommit.depth_first_search((-2, -1))
        self.assertEqual(select_path, [((-2, -1), Direction.SOUTH)])

        grommit.depth_first_add_reached((-2, -1), Direction.WEST)

        #Eighth (-3, -1):

        grommit.add_path(((-2, -1), Direction.WEST), ((-3, -1), Direction.EAST), 1)
        
        grommit.depth_first_add_stack((-3, -1), Direction.NORTH)
        grommit.depth_first_add_stack((-3, -1), Direction.EAST)
        grommit.depth_first_add_stack((-3, -1), Direction.WEST)
        grommit.depth_first_add_stack((-3, -1), Direction.SOUTH)
        grommit.add_andre((-3, -1))

        #print(grommit.depth_first_stack)
        #print(grommit.depth_first_reached)

        #for i in grommit.depth_first_stack:
            #print(i)

        select_path = grommit.depth_first_search((-3, -1))
        #elf.assertEqual(select_path, [((-3, -1), Direction.NORTH)])
        self.assertEqual(select_path, [((-3, -1), Direction.SOUTH)])

        #print(grommit.shortest_path((-3, -1), (-2, -1)))




        """
        paths = {
            (-1, -2): {0: ((-1, -1), 180, 1)},
            (-1, -1): {180: ((-1, -2), 0, 1), 0: ((-1, 1), 180, 1)},
            (-1, 1): {180: ((-1, -1), 0, 1), 0: ((-2, 2), 90, 1)},
            (-2, 2): {90: ((-1, 1), 0, 1), 180: ((-2, 1), 0, 1)},
            (-2, 1): {0: ((-2, 2), 180, 1), 180: ((-2, 0), 0, 1)},
            (-2, 0): {0: ((-2, 1), 180, 1), 180: ((-2, -1), 0, 1)},
            (-3, -1): {0: ((-3, -1), 270, 1), 270: ((-3, -1), 0, 1)},
            (-2, -1): {0: ((-2, 0), 180, 1), 180: ((-2, -2), 0, 1)},
            (-2, -2): {0: ((-2, -1), 180, 1), 180: ((-2, -2), 180, -1)}
        }

        andre = [
            (-1, -2),
            (-1, -1),
            (-1, 1),
            (-2, 2),
            (-2, 1),
            (-2, 0),
            (-2, -1),
            (-2, -2)
        ]

        dfs_stack = {
            (-1, -2): [0],
            (-1, -1): [180, 0],
            (-1, 1): [180, 0],
            (-2, 2): [90, 270, 180],
            (-2, 1): [0, 180, 270],
            (-2, 0): [0, 180, 270],
            (-3, -1): [0, 270],
            (-2, -1): [0, 180, 270],
            (-2, -2): [0, 180, 270]
        }

        dfs_searched = {
            (-1, -2): [0],
            (-1, -1): [180, 0],
            (-1, 1): [180, 0],
            (-2, 2): [90, 180],
            (-2, 1): [0, 180],
            (-2, 0): [0, 180],
            (-3, -1): [0, 270],
            (-2, -1): [0, 180],
            (-2, -2): [0, 180, 270]
        }

        """

if __name__ == "__main__":
    unittest.main()
