import pytest
from src.building.tech_tree import TechTree, Era

def test_tech_tree_init():
    tree = TechTree()
    assert len(tree.techs) > 0
    assert "basic_tools" in tree.techs
    assert "quantum_core" in tree.techs
    
def test_can_unlock_first_tech():
    tree = TechTree()
    assert tree.can_unlock("basic_tools") == True
    
def test_can_unlock_requires():
    tree = TechTree()
    assert tree.can_unlock("gear") == False  # 需要 wheel
    
def test_unlock_sequence():
    tree = TechTree()
    tree.unlock("basic_tools")
    assert "basic_tools" in tree.unlocked
    assert tree.can_unlock("wheel") == True
