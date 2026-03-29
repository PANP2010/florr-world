import pytest
from src.player.particle import PlayerParticle, Vector2

def test_player_particle_init():
    p = PlayerParticle(100, 200)
    assert abs(p.position.x - 100) < 0.001
    assert abs(p.position.y - 200) < 0.001
    assert p.mass == 1.0
    assert p.charge == 0.0
    
def test_player_particle_movement():
    p = PlayerParticle(0, 0)
    p.velocity = Vector2(10, 0)
    p.update(1.0)
    assert abs(p.position.x - 10) < 0.001
