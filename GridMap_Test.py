from __future__ import print_function

import copy
import unittest

import GridMap

class TestGridMap2D(unittest.TestCase):
    def setUp(self):
        self.rows = 10
        self.cols = 20
        self.map = GridMap.GridMap2D(self.rows, self.cols, outOfBoundValue=-200)
        self.map.initialize()

        # Overwrite blocks.
        self.map.set_starting_point((0, 0))
        self.map.set_ending_point((9, 19))
        self.map.add_obstacle((4, 10))
        self.map.add_obstacle((5, 10))
        self.map.add_obstacle((6, 10))

        # # Describe the map.
        # print(gm2d)

    def test_evaluate_coordinates(self):
        print("test_evaluate_coordinates")

        self.assertEqual( self.map.evaluate_coordinate( (    0,    0) ), -200 )
        self.assertEqual( self.map.evaluate_coordinate( (19.99, 9.99) ),  100 )
        self.assertEqual( self.map.evaluate_coordinate( (19.99, 0.01) ),    1 )
        self.assertEqual( self.map.evaluate_coordinate( ( 0.01, 9.99) ),    1 )
        self.assertEqual( self.map.evaluate_coordinate( (   10,    4) ), -100 )
        self.assertEqual( self.map.evaluate_coordinate( (   10,    5) ), -100 )
        self.assertEqual( self.map.evaluate_coordinate( (   10,    6) ), -100 )
        self.assertEqual( self.map.evaluate_coordinate( (   10,  5.5) ), -100 )
        self.assertEqual( self.map.evaluate_coordinate( ( 10.5,    5) ), -100 )
        self.assertEqual( self.map.evaluate_coordinate( (10.99, 5.99) ), -100 )
        self.assertEqual( self.map.evaluate_coordinate( (   -1,   -1) ), -200 )
        self.assertEqual( self.map.evaluate_coordinate( (    9,-0.01) ), -200 )
        self.assertEqual( self.map.evaluate_coordinate( (    9,10.01) ), -200 )
        self.assertEqual( self.map.evaluate_coordinate( (-0.01,    5) ), -200 )
        self.assertEqual( self.map.evaluate_coordinate( (20.01,    5) ), -200 )

    def test_get_block(self):
        print("test_get_block")

        index = GridMap.BlockIndex( 0, 0 )
        self.assertTrue( isinstance(self.map.get_block(index), GridMap.StartingPoint) )

        index.r = self.rows - 1
        index.c = self.cols - 1
        self.assertTrue( isinstance(self.map.get_block(index), GridMap.EndingPoint) )
        
        index.r = 5; index.c = 10
        self.assertTrue( isinstance(self.map.get_block(index), GridMap.ObstacleBlock) )

    def test_get_step_size(self):
        print("test_get_step_size")

        self.assertEqual( self.map.get_step_size(), [1, 1] )

    def test_get_index_starting_point(self):
        print("test_get_index_starting_point")

        self.assertEqual( self.map.get_index_starting_point().r, 0 )
        self.assertEqual( self.map.get_index_starting_point().c, 0 )

    def test_get_index_ending_point(self):
        print("test_get_index_ending_point")

        self.assertEqual( self.map.get_index_ending_point().r, self.rows-1 )
        self.assertEqual( self.map.get_index_ending_point().c, self.cols-1 )

    def test_set_starting_point(self):
        print("test_set_starting_point")

        # Get the index of the original starting point.
        idxOri = self.map.get_index_starting_point()

        # Set new starting point.
        idxNew = GridMap.BlockIndex( 1, 2 )
        self.map.set_starting_point( idxNew )

        # Test the new set starting point.
        idxNew2 = self.map.get_index_starting_point()
        self.assertEqual( idxNew2.r, idxNew.r )
        self.assertEqual( idxNew2.c, idxNew.c )

        # The original point must be a NormalBlock.
        # import ipdb; ipdb.set_trace()
        self.assertTrue( isinstance( self.map.get_block(idxOri), GridMap.NormalBlock ) )

        # Recover the original staring point.
        self.map.set_starting_point( idxOri )

        # The idxNew point now should be a NormalBlock.
        self.assertTrue( isinstance( self.map.get_block(idxNew), GridMap.NormalBlock ) )

    def test_set_ending_point(self):
        print("test_set_ending_point")

        # Get the index of the original ending point.
        idxOri = self.map.get_index_ending_point()

        # Set new ending point.
        idxNew = GridMap.BlockIndex( self.rows - 2, self.cols - 3 )
        self.map.set_ending_point( idxNew )

        # Test the new set ending point.
        idxNew2 = self.map.get_index_ending_point()
        self.assertEqual( idxNew2.r, idxNew.r )
        self.assertEqual( idxNew2.c, idxNew.c )

        # The original point must be a NormalBlock.
        # import ipdb; ipdb.set_trace()
        self.assertTrue( isinstance( self.map.get_block(idxOri), GridMap.NormalBlock ) )

        # Recover the original ending point.
        self.map.set_ending_point( idxOri )

        # The idxNew point now should be a NormalBlock.
        self.assertTrue( isinstance( self.map.get_block(idxNew), GridMap.NormalBlock ) )

    def test_is_out_of_boundary(self):
        print("test_is_out_of_boundary")

        coor   = GridMap.BlockCoor( 0.01, 0.01 )
        coorIn = copy.deepcopy( coor )

        # In boundaries.
        self.assertFalse( self.map.is_out_of_boundary( coorIn ) )

        # Out of the east boundary.
        coor.x = self.cols*self.map.get_step_size()[GridMap.GridMap2D.I_X]
        self.assertTrue( self.map.is_out_of_boundary(coor) )

        coor.y = self.rows * self.map.get_step_size()[GridMap.GridMap2D.I_X] - \
            0.5 * self.map.get_step_size()[GridMap.GridMap2D.I_Y]
        self.assertTrue( self.map.is_out_of_boundary(coor) )

        coorIn.x = coor.x - 0.5 * self.map.get_step_size()[GridMap.GridMap2D.I_X]
        coorIn.y = 0.01
        self.assertFalse( self.map.is_out_of_boundary(coorIn) )

        coorIn.y = coor.y
        self.assertFalse( self.map.is_out_of_boundary(coorIn) )

        # Out of the north boundary.
        coor.x = self.map.corners[2][GridMap.GridMap2D.I_X] - \
            0.5 * self.map.get_step_size()[GridMap.GridMap2D.I_X]
        coor.y = self.rows * self.map.get_step_size()[GridMap.GridMap2D.I_X]
        self.assertTrue( self.map.is_out_of_boundary(coor) )

        coor.x = 0.01
        self.assertTrue( self.map.is_out_of_boundary(coor) )

        coorIn.x = coor.x
        coorIn.y = coor.y - 0.5 * self.map.get_step_size()[GridMap.GridMap2D.I_Y]
        self.assertFalse( self.map.is_out_of_boundary(coorIn) )

        coorIn.x = 0.01
        self.assertFalse( self.map.is_out_of_boundary(coorIn) )
        
        # Out of the west boundary.
        coor.x = -0.5 * self.map.get_step_size()[GridMap.GridMap2D.I_X]
        coor.y = self.map.corners[3][GridMap.GridMap2D.I_Y] - \
            0.5 * self.map.get_step_size()[GridMap.GridMap2D.I_Y]
        self.assertTrue( self.map.is_out_of_boundary(coor) )

        coor.y = 0.01
        self.assertTrue( self.map.is_out_of_boundary(coor) )

        coorIn.x = coor.x + 0.5 * self.map.get_step_size()[GridMap.GridMap2D.I_X] + 0.01
        coorIn.y = coor.y
        self.assertFalse( self.map.is_out_of_boundary(coorIn) )

        coorIn.y = 0.01
        self.assertFalse( self.map.is_out_of_boundary(coorIn) )

        # Out of the south boundary.
        coor.x = 0.5 * self.map.get_step_size()[GridMap.GridMap2D.I_X]
        coor.y = -0.5 * self.map.get_step_size()[GridMap.GridMap2D.I_Y]
        self.assertTrue( self.map.is_out_of_boundary(coor) )

        coor.x = self.map.corners[1][GridMap.GridMap2D.I_X] - \
            0.5 * self.map.get_step_size()[GridMap.GridMap2D.I_X]
        self.assertTrue( self.map.is_out_of_boundary(coor) )

        coorIn.x = 0.5 * self.map.get_step_size()[GridMap.GridMap2D.I_X]
        coorIn.y = coor.y + 0.5 * self.map.get_step_size()[GridMap.GridMap2D.I_Y] + 0.01
        self.assertFalse( self.map.is_out_of_boundary(coorIn) )

        coorIn.x = coor.x
        self.assertFalse( self.map.is_out_of_boundary(coorIn) )

    def test_get_index_by_coordinates(self):
        print("test_get_index_by_coordinates")

        # (0, 0) should be [0, 0]
        coor = GridMap.BlockCoor( 0, 0 )

        index = self.map.get_index_by_coordinates( coor )
        self.assertEqual( index.r, 0 )
        self.assertEqual( index.c, 0 )

        # (0.5, 0.5) * step_size should be [0, 0]
        coor.x = 0.5 * self.map.get_step_size()[GridMap.GridMap2D.I_X]
        coor.y = 0.5 * self.map.get_step_size()[GridMap.GridMap2D.I_Y]
        index = self.map.get_index_by_coordinates( coor )
        self.assertEqual( index.r, 0 )
        self.assertEqual( index.c, 0 )

        # corner - ( 0.5, 0.5 ) * step_size should be the upper right corner.
        coor.x = self.map.corners[2][GridMap.GridMap2D.I_X] - \
            0.5 * self.map.get_step_size()[GridMap.GridMap2D.I_X]
        coor.y = self.map.corners[2][GridMap.GridMap2D.I_Y] - \
            0.5 * self.map.get_step_size()[GridMap.GridMap2D.I_Y]
        index = self.map.get_index_by_coordinates( coor )
        self.assertEqual( index.r, self.rows - 1 )
        self.assertEqual( index.c, self.cols - 1 )

    def test_convert_to_coordinates(self):
        print("test_convert_to_coordinates")

        # [0, 0] should be (0.0, 0.0)
        index = GridMap.BlockIndex( 0, 0 )

        coor = self.map.convert_to_coordinates(index)
        self.assertEqual( coor.x, 0.0 )
        self.assertEqual( coor.y, 0.0 )

        # [ rows-1, cols-1 ] should be upper right corner - step_size.
        index.r = self.rows - 1
        index.c = self.cols - 1
        coor = self.map.convert_to_coordinates(index)
        self.assertEqual( coor.x, \
            self.map.corners[2][GridMap.GridMap2D.I_X] - self.map.get_step_size()[GridMap.GridMap2D.I_X] )
        self.assertEqual( coor.y, \
            self.map.corners[2][GridMap.GridMap2D.I_Y] - self.map.get_step_size()[GridMap.GridMap2D.I_Y] )
        
    def test_is_xxx_boundary(self):
        print("test_is_xxx_boundary")

        coorNB = GridMap.BlockCoor(0, 0)

        # East boundary.
        coor = GridMap.BlockCoor( \
            self.map.corners[1][GridMap.GridMap2D.I_X], \
            self.map.corners[1][GridMap.GridMap2D.I_Y] )
        self.assertTrue( self.map.is_east_boundary( coor ) )

        coor.y = 0.5 * ( \
            self.map.corners[1][GridMap.GridMap2D.I_Y] + \
            self.map.corners[2][GridMap.GridMap2D.I_Y] )
        self.assertTrue( self.map.is_east_boundary( coor ) )        

        coor.y = self.map.corners[2][GridMap.GridMap2D.I_Y]
        self.assertTrue( self.map.is_east_boundary( coor ) )

        coorNB.x = coor.x - 0.01
        coorNB.y = coor.y
        self.assertFalse( self.map.is_east_boundary( coorNB ) )

        # North boundary.
        coor = GridMap.BlockCoor( \
            self.map.corners[2][GridMap.GridMap2D.I_X], \
            self.map.corners[2][GridMap.GridMap2D.I_Y] )
        self.assertTrue( self.map.is_north_boundary( coor ) )

        coor.x = 0.5 * ( \
            self.map.corners[2][GridMap.GridMap2D.I_X] + \
            self.map.corners[3][GridMap.GridMap2D.I_X] )
        self.assertTrue( self.map.is_north_boundary( coor ) )        

        coor.x = self.map.corners[3][GridMap.GridMap2D.I_X]
        self.assertTrue( self.map.is_north_boundary( coor ) )

        coorNB.x = coor.x
        coorNB.y = coor.y - 0.01
        self.assertFalse( self.map.is_north_boundary( coorNB ) )

        # West boundary.
        coor = GridMap.BlockCoor( \
            self.map.corners[3][GridMap.GridMap2D.I_X], \
            self.map.corners[3][GridMap.GridMap2D.I_Y] )
        self.assertTrue( self.map.is_west_boundary( coor ) )

        coor.y = 0.5 * ( \
            self.map.corners[0][GridMap.GridMap2D.I_Y] + \
            self.map.corners[3][GridMap.GridMap2D.I_Y] )
        self.assertTrue( self.map.is_west_boundary( coor ) )        

        coor.y = self.map.corners[0][GridMap.GridMap2D.I_Y]
        self.assertTrue( self.map.is_west_boundary( coor ) )

        coorNB.x = coor.x + 0.01
        coorNB.y = coor.y
        self.assertFalse( self.map.is_west_boundary( coorNB ) )

        # South boundary.
        coor = GridMap.BlockCoor( \
            self.map.corners[0][GridMap.GridMap2D.I_X], \
            self.map.corners[0][GridMap.GridMap2D.I_Y] )
        self.assertTrue( self.map.is_south_boundary( coor ) )

        coor.x = 0.5 * ( \
            self.map.corners[0][GridMap.GridMap2D.I_X] + \
            self.map.corners[1][GridMap.GridMap2D.I_X] )
        self.assertTrue( self.map.is_south_boundary( coor ) )        

        coor.x = self.map.corners[1][GridMap.GridMap2D.I_X]
        self.assertTrue( self.map.is_south_boundary( coor ) )

        coorNB.x = coor.x
        coorNB.y = coor.y + 0.01
        self.assertFalse( self.map.is_south_boundary( coorNB ) )

    def test_is_corner_or_principle_line(self):
        print("test_is_corner_or_principle_line")

        # (0, 0).
        coor = GridMap.BlockCoor(0, 0)

        loc = self.map.is_corner_or_principle_line(coor)
        self.assertTrue( loc[0] )
        self.assertTrue( loc[1] )
        self.assertTrue( loc[2] )
        self.assertEqual( loc[3].r, 0 )
        self.assertEqual( loc[3].c, 0 )

        # Upper right corner.
        coor.x = self.map.corners[2][GridMap.GridMap2D.I_X] - \
            self.map.get_step_size()[GridMap.GridMap2D.I_X]
        coor.y = self.map.corners[2][GridMap.GridMap2D.I_Y] - \
            self.map.get_step_size()[GridMap.GridMap2D.I_Y]
        loc = self.map.is_corner_or_principle_line( coor )
        self.assertTrue( loc[0] )
        self.assertTrue( loc[1] )
        self.assertTrue( loc[2] )
        self.assertEqual( loc[3].r, self.rows-1 )
        self.assertEqual( loc[3].c, self.cols-1 )

        # Upper left corner.
        coor.x = self.map.corners[3][GridMap.GridMap2D.I_X] + \
            self.map.get_step_size()[GridMap.GridMap2D.I_X]
        coor.y = self.map.corners[3][GridMap.GridMap2D.I_Y] - \
            0.5 * self.map.get_step_size()[GridMap.GridMap2D.I_Y]

        loc = self.map.is_corner_or_principle_line( coor )
        self.assertFalse( loc[0] )
        self.assertFalse( loc[1] )
        self.assertTrue( loc[2] )
        self.assertEqual( loc[3].r, self.rows-1 )
        self.assertEqual( loc[3].c, 1 )

        # Lower right corner.
        coor.x = self.map.corners[1][GridMap.GridMap2D.I_X] - \
            0.5 * self.map.get_step_size()[GridMap.GridMap2D.I_X]
        coor.y = self.map.corners[1][GridMap.GridMap2D.I_Y] + \
            self.map.get_step_size()[GridMap.GridMap2D.I_Y]

        loc = self.map.is_corner_or_principle_line( coor )
        self.assertFalse( loc[0] )
        self.assertTrue( loc[1] )
        self.assertFalse( loc[2] )
        self.assertEqual( loc[3].r, 1 )
        self.assertEqual( loc[3].c, self.cols-1 )

class TestGridMapEnv(unittest.TestCase):
    def setUp(self):
        self.rows = 10
        self.cols = 20
        gridMap = GridMap.GridMap2D(self.rows, self.cols, outOfBoundValue=-200)
        gridMap.initialize()
        # Overwrite blocks.
        gridMap.set_starting_point((0, 0))
        gridMap.set_ending_point((9, 19))
        gridMap.add_obstacle((4, 10))
        gridMap.add_obstacle((5,  9))
        gridMap.add_obstacle((5, 10))
        gridMap.add_obstacle((5, 11))
        gridMap.add_obstacle((6, 10))

        self.gme = GridMap.GridMapEnv( gridMap = gridMap )

        # # Describe the map.
        # print(self.gme.map)

        # Predefined points to be tested.
        self.points = []
        self.points.append( GridMap.BlockCoor( 12.0, 5.5 ) )
        self.points.append( GridMap.BlockCoor( 12.0, 6.0 ) )
        self.points.append( GridMap.BlockCoor( 11.5, 6.0 ) )
        self.points.append( GridMap.BlockCoor( 11.0, 6.0 ) )
        self.points.append( GridMap.BlockCoor( 11.0, 6.5 ) )
        self.points.append( GridMap.BlockCoor( 11.0, 7.0 ) )
        self.points.append( GridMap.BlockCoor( 10.5, 7.0 ) )
        self.points.append( GridMap.BlockCoor( 10.0, 7.0 ) )
        self.points.append( GridMap.BlockCoor( 10.0, 6.5 ) )
        self.points.append( GridMap.BlockCoor( 10.0, 6.0 ) )
        self.points.append( GridMap.BlockCoor(  9.5, 6.0 ) )
        self.points.append( GridMap.BlockCoor(  9.0, 6.0 ) )
        self.points.append( GridMap.BlockCoor(  9.0, 5.5 ) )
        self.points.append( GridMap.BlockCoor(  9.0, 5.0 ) )
        self.points.append( GridMap.BlockCoor(  9.5, 5.0 ) )
        self.points.append( GridMap.BlockCoor( 10.0, 5.0 ) )
        self.points.append( GridMap.BlockCoor( 10.0, 4.5 ) )
        self.points.append( GridMap.BlockCoor( 10.0, 4.0 ) )
        self.points.append( GridMap.BlockCoor( 10.5, 4.0 ) )
        self.points.append( GridMap.BlockCoor( 11.0, 4.0 ) )
        self.points.append( GridMap.BlockCoor( 11.0, 4.5 ) )
        self.points.append( GridMap.BlockCoor( 11.0, 5.0 ) )
        self.points.append( GridMap.BlockCoor( 11.5, 5.0 ) )
        self.points.append( GridMap.BlockCoor( 12.0, 5.0 ) )

        self.boundaryPoints = []
        self.boundaryPoints.append( GridMap.BlockCoor( 20.0,  0.0 ) )
        self.boundaryPoints.append( GridMap.BlockCoor( 20.0,  5.0 ) )
        self.boundaryPoints.append( GridMap.BlockCoor( 20.0, 10.0 ) )
        self.boundaryPoints.append( GridMap.BlockCoor( 10.0, 10.0 ) )
        self.boundaryPoints.append( GridMap.BlockCoor(  0.0, 10.0 ) )
        self.boundaryPoints.append( GridMap.BlockCoor(  0.0,  5.0 ) )
        self.boundaryPoints.append( GridMap.BlockCoor(  0.0,  0.0 ) )
        self.boundaryPoints.append( GridMap.BlockCoor(  5.0,  0.0 ) )

    def test_dummy(self):
        print("test_dummy")

        self.gme.render(1)

        self.assertTrue( True )
    
    def test_can_move_to_east(self):
        print("test_can_move_to_east")

        # East direction.
        dx = 1.0
        dy = 0.0

        self.assertEqual( self.gme.can_move( self.points[ 0].x, self.points[ 0].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[ 1].x, self.points[ 1].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[ 2].x, self.points[ 2].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 3].x, self.points[ 3].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 4].x, self.points[ 4].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[ 5].x, self.points[ 5].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[ 6].x, self.points[ 6].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 7].x, self.points[ 7].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 8].x, self.points[ 8].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 9].x, self.points[ 9].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[10].x, self.points[10].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[11].x, self.points[11].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[12].x, self.points[12].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[13].x, self.points[13].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[14].x, self.points[14].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[15].x, self.points[15].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[16].x, self.points[16].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[17].x, self.points[17].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[18].x, self.points[18].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[19].x, self.points[19].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[20].x, self.points[20].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[21].x, self.points[21].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[22].x, self.points[22].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[23].x, self.points[23].y, dx, dy ),  True )

        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 0].x, self.boundaryPoints[ 0].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 1].x, self.boundaryPoints[ 1].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 2].x, self.boundaryPoints[ 2].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 3].x, self.boundaryPoints[ 3].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 4].x, self.boundaryPoints[ 4].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 5].x, self.boundaryPoints[ 5].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 6].x, self.boundaryPoints[ 6].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 7].x, self.boundaryPoints[ 7].y, dx, dy ), False )
    
    def test_can_move_to_northeast(self):
        print("test_can_move_to_northeast")

        # Northeast direction.
        dx = 1.0
        dy = 1.0

        self.assertEqual( self.gme.can_move( self.points[ 0].x, self.points[ 0].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[ 1].x, self.points[ 1].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[ 2].x, self.points[ 2].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[ 3].x, self.points[ 3].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[ 4].x, self.points[ 4].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[ 5].x, self.points[ 5].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[ 6].x, self.points[ 6].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[ 7].x, self.points[ 7].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[ 8].x, self.points[ 8].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 9].x, self.points[ 9].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[10].x, self.points[10].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[11].x, self.points[11].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[12].x, self.points[12].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[13].x, self.points[13].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[14].x, self.points[14].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[15].x, self.points[15].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[16].x, self.points[16].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[17].x, self.points[17].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[18].x, self.points[18].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[19].x, self.points[19].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[20].x, self.points[20].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[21].x, self.points[21].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[22].x, self.points[22].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[23].x, self.points[23].y, dx, dy ),  True )

        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 0].x, self.boundaryPoints[ 0].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 1].x, self.boundaryPoints[ 1].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 2].x, self.boundaryPoints[ 2].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 3].x, self.boundaryPoints[ 3].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 4].x, self.boundaryPoints[ 4].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 5].x, self.boundaryPoints[ 5].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 6].x, self.boundaryPoints[ 6].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 7].x, self.boundaryPoints[ 7].y, dx, dy ),  True )

    def test_can_move_to_north(self):
        print("test_can_move_to_north")

        # Nort direction.
        dx = 0.0
        dy = 1.0

        self.assertEqual( self.gme.can_move( self.points[ 0].x, self.points[ 0].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 1].x, self.points[ 1].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[ 2].x, self.points[ 2].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[ 3].x, self.points[ 3].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 4].x, self.points[ 4].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 5].x, self.points[ 5].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[ 6].x, self.points[ 6].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[ 7].x, self.points[ 7].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[ 8].x, self.points[ 8].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 9].x, self.points[ 9].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[10].x, self.points[10].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[11].x, self.points[11].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[12].x, self.points[12].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[13].x, self.points[13].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[14].x, self.points[14].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[15].x, self.points[15].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[16].x, self.points[16].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[17].x, self.points[17].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[18].x, self.points[18].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[19].x, self.points[19].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[20].x, self.points[20].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[21].x, self.points[21].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[22].x, self.points[22].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[23].x, self.points[23].y, dx, dy ), False )

        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 0].x, self.boundaryPoints[ 0].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 1].x, self.boundaryPoints[ 1].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 2].x, self.boundaryPoints[ 2].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 3].x, self.boundaryPoints[ 3].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 4].x, self.boundaryPoints[ 4].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 5].x, self.boundaryPoints[ 5].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 6].x, self.boundaryPoints[ 6].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 7].x, self.boundaryPoints[ 7].y, dx, dy ),  True )

    def test_can_move_to_northwest(self):
        print("test_can_move_to_northwest")

        # Northwest direction.
        dx = -1.0
        dy =  1.0

        self.assertEqual( self.gme.can_move( self.points[ 0].x, self.points[ 0].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 1].x, self.points[ 1].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[ 2].x, self.points[ 2].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[ 3].x, self.points[ 3].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 4].x, self.points[ 4].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 5].x, self.points[ 5].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[ 6].x, self.points[ 6].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[ 7].x, self.points[ 7].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[ 8].x, self.points[ 8].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[ 9].x, self.points[ 9].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[10].x, self.points[10].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[11].x, self.points[11].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[12].x, self.points[12].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[13].x, self.points[13].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[14].x, self.points[14].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[15].x, self.points[15].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[16].x, self.points[16].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[17].x, self.points[17].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[18].x, self.points[18].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[19].x, self.points[19].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[20].x, self.points[20].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[21].x, self.points[21].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[22].x, self.points[22].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[23].x, self.points[23].y, dx, dy ), False )

        # import ipdb; ipdb.set_trace()

        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 0].x, self.boundaryPoints[ 0].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 1].x, self.boundaryPoints[ 1].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 2].x, self.boundaryPoints[ 2].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 3].x, self.boundaryPoints[ 3].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 4].x, self.boundaryPoints[ 4].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 5].x, self.boundaryPoints[ 5].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 6].x, self.boundaryPoints[ 6].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 7].x, self.boundaryPoints[ 7].y, dx, dy ),  True )

    def test_can_move_to_west(self):
        print("test_can_move_to_west")

        # West direction.
        dx = -1.0
        dy =  0.0

        self.assertEqual( self.gme.can_move( self.points[ 0].x, self.points[ 0].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 1].x, self.points[ 1].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 2].x, self.points[ 2].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 3].x, self.points[ 3].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 4].x, self.points[ 4].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 5].x, self.points[ 5].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 6].x, self.points[ 6].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 7].x, self.points[ 7].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[ 8].x, self.points[ 8].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[ 9].x, self.points[ 9].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[10].x, self.points[10].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[11].x, self.points[11].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[12].x, self.points[12].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[13].x, self.points[13].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[14].x, self.points[14].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[15].x, self.points[15].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[16].x, self.points[16].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[17].x, self.points[17].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[18].x, self.points[18].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[19].x, self.points[19].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[20].x, self.points[20].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[21].x, self.points[21].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[22].x, self.points[22].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[23].x, self.points[23].y, dx, dy ), False )

        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 0].x, self.boundaryPoints[ 0].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 1].x, self.boundaryPoints[ 1].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 2].x, self.boundaryPoints[ 2].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 3].x, self.boundaryPoints[ 3].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 4].x, self.boundaryPoints[ 4].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 5].x, self.boundaryPoints[ 5].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 6].x, self.boundaryPoints[ 6].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 7].x, self.boundaryPoints[ 7].y, dx, dy ), False )

    def test_can_move_to_southwest(self):
        print("test_can_move_to_southwest")

        # Southwest direction.
        dx = -1.0
        dy = -1.0

        self.assertEqual( self.gme.can_move( self.points[ 0].x, self.points[ 0].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 1].x, self.points[ 1].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 2].x, self.points[ 2].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 3].x, self.points[ 3].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 4].x, self.points[ 4].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 5].x, self.points[ 5].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 6].x, self.points[ 6].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 7].x, self.points[ 7].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[ 8].x, self.points[ 8].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[ 9].x, self.points[ 9].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[10].x, self.points[10].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[11].x, self.points[11].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[12].x, self.points[12].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[13].x, self.points[13].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[14].x, self.points[14].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[15].x, self.points[15].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[16].x, self.points[16].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[17].x, self.points[17].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[18].x, self.points[18].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[19].x, self.points[19].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[20].x, self.points[20].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[21].x, self.points[21].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[22].x, self.points[22].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[23].x, self.points[23].y, dx, dy ),  True )

        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 0].x, self.boundaryPoints[ 0].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 1].x, self.boundaryPoints[ 1].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 2].x, self.boundaryPoints[ 2].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 3].x, self.boundaryPoints[ 3].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 4].x, self.boundaryPoints[ 4].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 5].x, self.boundaryPoints[ 5].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 6].x, self.boundaryPoints[ 6].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 7].x, self.boundaryPoints[ 7].y, dx, dy ), False )

    def test_can_move_to_south(self):
        print("test_can_move_to_south")

        # South direction.
        dx =  0.0
        dy = -1.0

        self.assertEqual( self.gme.can_move( self.points[ 0].x, self.points[ 0].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 1].x, self.points[ 1].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 2].x, self.points[ 2].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 3].x, self.points[ 3].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 4].x, self.points[ 4].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 5].x, self.points[ 5].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 6].x, self.points[ 6].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 7].x, self.points[ 7].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 8].x, self.points[ 8].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 9].x, self.points[ 9].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[10].x, self.points[10].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[11].x, self.points[11].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[12].x, self.points[12].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[13].x, self.points[13].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[14].x, self.points[14].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[15].x, self.points[15].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[16].x, self.points[16].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[17].x, self.points[17].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[18].x, self.points[18].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[19].x, self.points[19].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[20].x, self.points[20].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[21].x, self.points[21].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[22].x, self.points[22].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[23].x, self.points[23].y, dx, dy ),  True )

        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 0].x, self.boundaryPoints[ 0].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 1].x, self.boundaryPoints[ 1].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 2].x, self.boundaryPoints[ 2].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 3].x, self.boundaryPoints[ 3].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 4].x, self.boundaryPoints[ 4].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 5].x, self.boundaryPoints[ 5].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 6].x, self.boundaryPoints[ 6].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 7].x, self.boundaryPoints[ 7].y, dx, dy ), False )

    def test_can_move_to_southeast(self):
        print("test_can_move_to_southeast")

        # Southeast direction.
        dx =  1.0
        dy = -1.0

        self.assertEqual( self.gme.can_move( self.points[ 0].x, self.points[ 0].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[ 1].x, self.points[ 1].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[ 2].x, self.points[ 2].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 3].x, self.points[ 3].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 4].x, self.points[ 4].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[ 5].x, self.points[ 5].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[ 6].x, self.points[ 6].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 7].x, self.points[ 7].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 8].x, self.points[ 8].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[ 9].x, self.points[ 9].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[10].x, self.points[10].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[11].x, self.points[11].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[12].x, self.points[12].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[13].x, self.points[13].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[14].x, self.points[14].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[15].x, self.points[15].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[16].x, self.points[16].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.points[17].x, self.points[17].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[18].x, self.points[18].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[19].x, self.points[19].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[20].x, self.points[20].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[21].x, self.points[21].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[22].x, self.points[22].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.points[23].x, self.points[23].y, dx, dy ),  True )

        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 0].x, self.boundaryPoints[ 0].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 1].x, self.boundaryPoints[ 1].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 2].x, self.boundaryPoints[ 2].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 3].x, self.boundaryPoints[ 3].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 4].x, self.boundaryPoints[ 4].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 5].x, self.boundaryPoints[ 5].y, dx, dy ),  True )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 6].x, self.boundaryPoints[ 6].y, dx, dy ), False )
        self.assertEqual( self.gme.can_move( self.boundaryPoints[ 7].x, self.boundaryPoints[ 7].y, dx, dy ), False )

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase( TestGridMap2D )
    suite.addTest( unittest.TestLoader().loadTestsFromTestCase( TestGridMapEnv ) )
    unittest.TextTestRunner().run( suite )