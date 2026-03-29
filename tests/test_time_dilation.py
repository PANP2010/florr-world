import pytest
from src.physics.exotic.time_dilation import TimeDilationField

def test_time_dilation_inside():
    td = TimeDilationField((0, 0, 100, 100), 0.5)
    dt = td.get_effective_dt(1.0, 50, 50)
    assert abs(dt - 0.5) < 0.001
    
def test_time_dilation_outside():
    td = TimeDilationField((0, 0, 100, 100), 0.5)
    dt = td.get_effective_dt(1.0, 200, 200)
    assert dt == 1.0
