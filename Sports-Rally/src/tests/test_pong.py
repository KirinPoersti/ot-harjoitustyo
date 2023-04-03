import pytest
from Pong_test import increase_ball_speed, calculate_opponent_target_y, adjust_opponent_paddle_y, handle_stamina

def test_increase_ball_speed():
    initial_speed = 4
    increased_speed = increase_ball_speed(initial_speed)
    assert increased_speed == pytest.approx(4.4, 0.1)

def test_calculate_opponent_target_y():
    ball_y = 250
    paddle_height = 100
    ball_height = 20
    target_y = calculate_opponent_target_y(ball_y, paddle_height, ball_height)
    assert target_y == 235

def test_adjust_opponent_paddle_y():
    # Test moving paddle up
    paddle_y = 250
    target_y = 200
    speed = 5
    new_paddle_y = adjust_opponent_paddle_y(paddle_y, target_y, speed)
    assert new_paddle_y == 245

    # Test moving paddle down
    paddle_y = 200
    target_y = 250
    new_paddle_y = adjust_opponent_paddle_y(paddle_y, target_y, speed)
    assert new_paddle_y == 205

    # Test not moving paddle
    paddle_y = 200
    target_y = 200
    new_paddle_y = adjust_opponent_paddle_y(paddle_y, target_y, speed)
    assert new_paddle_y == 200

@pytest.mark.parametrize(
    "keys, stamina_blocks, stamina_recharge_timer, stamina_consume_timer, expected_boost_active, expected_stamina_blocks, expected_stamina_recharge_timer, expected_stamina_consume_timer",
    [
        ({"K_LSHIFT": True}, 2, 0, 0, True, 0, 0, 0),
        ({"K_LSHIFT": True}, 0, 0, 0, False, 0, 0, 0),
        ({"K_LSHIFT": False}, 2, 0, 0, False, 2, 0, 0),
    ],
)
def test_handle_stamina(
    keys,
    stamina_blocks,
    stamina_recharge_timer,
    stamina_consume_timer,
    expected_boost_active,
    expected_stamina_blocks,
    expected_stamina_recharge_timer,
    expected_stamina_consume_timer,
):
    boost_active, new_stamina_blocks, new_stamina_recharge_timer, new_stamina_consume_timer = handle_stamina(
        keys, stamina_blocks, stamina_recharge_timer, stamina_consume_timer, "K_LSHIFT"
    )

    assert boost_active == expected_boost_active
    assert new_stamina_blocks == expected_stamina_blocks
    assert new_stamina_recharge_timer == expected_stamina_recharge_timer
    assert new_stamina_consume_timer == expected_stamina_consume_timer
