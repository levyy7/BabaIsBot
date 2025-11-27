def step(state: State, action: Action) -> State:
    dx, dy = {
        Action.STILL: (0, 0),
        Action.UP: (-1, 0),
        Action.DOWN: (1, 0),
        Action.LEFT: (0, -1),
        Action.RIGHT: (0, 1),
    }[action]
    
    # Get all blocks with the 'you' property
    you_blocks = get_blocks_by_property('you')
    
    # Get all blocks with the 'win' property
    win_blocks = get_blocks_by_property('win')
    
    # Check for win condition
    for you_block in you_blocks:
        for win_block in win_blocks:
            if you_block.x == win_block.x and you_block.y == win_block.y:
                state.outcome = Outcome.WIN
                return state
    
    # Get all blocks with the 'push' property
    push_blocks = get_blocks_by_property('push')
    
    # Get all blocks with the 'stop' property
    stop_blocks = get_blocks_by_property('stop')
    
    # Get all blocks with the 'you' property
    you_blocks = get_blocks_by_property('you')
    
    # Process movement for 'you' blocks
    for you_block in you_blocks:
        new_x = you_block.x + dx
        new_y = you_block.y + dy
        
        # Check if the new position is blocked by a 'stop' block
        blocked = False
        for stop_block in stop_blocks:
            if stop_block.x == new_x and stop_block.y == new_y:
                blocked = True
                break
        
        if not blocked:
            # Check if there's a 'push' block in the new position
            for push_block in push_blocks:
                if push_block.x == new_x and push_block.y == new_y:
                    # Calculate the new position for the push block
                    push_new_x = push_block.x + dx
                    push_new_y = push_block.y + dy
                    
                    # Check if the push block's new position is blocked
                    push_blocked = False
                    for stop_block in stop_blocks:
                        if stop_block.x == push_new_x and stop_block.y == push_new_y:
                            push_blocked = True
                            break
                    
                    if not push_blocked:
                        # Move the push block
                        move_block(push_block, push_new_x, push_new_y)
                    else:
                        blocked = True
                        break
            
            if not blocked:
                # Move the 'you' block
                move_block(you_block, new_x, new_y)
    
    return state