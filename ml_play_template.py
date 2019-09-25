"""The template of the main script of the machine learning process
"""

import games.arkanoid.communication as comm
import numpy as np
from games.arkanoid.communication import ( \
    SceneInfo, GameInstruction, GameStatus, PlatformAction
)

def ml_loop():
    """The main loop of the machine learning process

    This loop is run in a separate process, and communicates with the game process.

    Note that the game process won't wait for the ml process to generate the
    GameInstruction. It is possible that the frame of the GameInstruction
    is behind of the current frame in the game process. Try to decrease the fps
    to avoid this situation.
    """

    # === Here is the execution order of the loop === #
    # 1. Put the initialization code here.

    # 2. Inform the game process that ml process is ready before start the loop.
    ball_location = [0,0]
    plat_location = [0,0]
    comm.ml_ready()
    # 3. Start an endless loop.
    while True:
        # 3.1. Receive the scene information sent from the game process.
        scene_info = comm.get_scene_info()
		
		
        # 3.2. If the game is over or passed, the game process will reset
        #      the scene and wait for ml process doing resetting job.
        if scene_info.status == GameStatus.GAME_OVER or \
            scene_info.status == GameStatus.GAME_PASS:
            # Do some stuff if needed
            # 3.2.1. Inform the game process that ml process is ready
            comm.ml_ready()
            continue
        last_ball_location = ball_location
        ball_location = scene_info.ball
        plat_location = scene_info.platform
        
        
        if(int(ball_location[0]) + int(ball_location[1]) != 0):
            if(int(ball_location[1]) - int(last_ball_location[1]) > 0):
                # dowing
                delta_x = int(ball_location[0]) - int(last_ball_location[0])
                delta_y = int(ball_location[1]) - int(last_ball_location[1])
                
                #get Slope
                m = delta_y/delta_x
                
                #calculat next x
                next_x = (400-int(ball_location[1]))/m + int(ball_location[0])
                
                if(next_x>200):
                    next_x = 200*2-next_x
                if(next_x<0):
                    if(next_x>-200):
                        next_x = np.abs(next_x)
                    else:
                        next_x = next_x+400
            
            else:
                print("")
    
            
        # 3.3. Put the code here to handle the scene information

        # 3.4. Send the instruction for this frame to the game process
        #if(ball_location[1]<350):
        
        #plat_location拿到的位置是平板的最左
        #平板中心為 平板長度/2 + plat_location
        if(int(plat_location[0])+20>next_x):
            comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
        elif(int(plat_location[0])+20<next_x):
            comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
        else:
            comm.send_instruction(scene_info.frame, PlatformAction.NONE)
    
            

