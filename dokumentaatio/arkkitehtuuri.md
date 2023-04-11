# main.py
       main()
        |
        |--> pygame.init()
        |--> pygame.display.set_mode(size)
        |--> pygame.display.set_caption("Pong Menu")
        |--> font = pygame.font.SysFont('Calibri', 50)
        |--> small_font = pygame.font.SysFont('Calibri', 30)
        |--> title_text = font.render("PONG", True, WHITE)
        |--> practice_text = small_font.render("Practice Mode", True, WHITE)
        |--> pvp_text = small_font.render("PvP", True, WHITE)
        |--> exit_text = small_font.render("Exit", True, WHITE)
        |--> title_rect = title_text.get_rect()
        |--> practice_rect = practice_text.get_rect()
        |--> pvp_rect = pvp_text.get_rect()
        |--> exit_rect = exit_text.get_rect()
        |--> open_file(file_name)
        |     |
        |     |--> subprocess.Popen(['py', file_name])
        |
        |--> while not done (main loop)
              |
              |--> for event in pygame.event.get()
              |     |
              |     |--> if event.type == pygame.QUIT
              |     |
              |     |--> elif event.type == pygame.MOUSEBUTTONDOWN
              |           |
              |           |--> if practice_rect.collidepoint(event.pos)
              |           |     |
              |           |     |--> open_file('src/pong_practice.py')
              |           |
              |           |--> elif pvp_rect.collidepoint(event.pos)
              |           |     |
              |           |     |--> open_file('src/pong_pvp.py')
              |           |
              |           |--> elif exit_rect.collidepoint(event.pos)
              |
              |--> screen.fill(BLACK)
              |--> screen.blit(title_text, title_rect)
              |--> screen.blit(practice_text, practice_rect)
              |--> screen.blit(pvp_text, pvp_rect)
              |--> screen.blit(exit_text, exit_rect)
              |--> pygame.display.flip()
        |
        |--> pygame.quit()
        |--> sys.exit()
# pong_practice.py
     main()
      |
      +----> pygame.init()
      |
      +----> pygame.display.set_mode()
      |
      +----> pygame.display.set_caption()
      |
      +----> pygame.time.Clock()
      |
      +----> pygame.font.Font()
      |
      +----> reset_ball()
      |
      |      Main game loop
      +----> clock.tick()
      |
      +----> pygame.event.get()
      |          |
      |          +----> pygame.quit() (if QUIT event)
      |          |
      |          +----> sys.exit() (if QUIT event)
      |          |
      |          +----> pygame.quit() (if MOUSEBUTTONDOWN event and exit button clicked)
      |          |
      |          +----> sys.exit() (if MOUSEBUTTONDOWN event and exit button clicked)
      |
      +----> move_paddle()
      |
      +----> move_ball()
      |
      +----> draw_objects()
      |
      +----> pygame.display.flip()
 # pong_pvp.py
     Init
      |-- pygame.init()
      |-- pygame.display.set_mode()
      |-- pygame.display.set_caption()
      |-- pygame.time.Clock()
      |-- pygame.font.Font()
    
    Main Loop
      |-- Event Handling
            |-- pygame.event.get()
            |-- handle_stamina() for left player
            |-- handle_stamina() for right player
    
      |-- Game Logic
            |-- move_paddles()
            |-- move_ball()
            |-- update_stamina()
    
      |-- Drawing
            |-- draw_objects()
            |-- draw_stamina()
            |-- pygame.display.flip()
    
    End of Game
      |-- Display winning message
      |-- pygame.time.delay()
      |-- pygame.quit()
      |-- sys.exit()

