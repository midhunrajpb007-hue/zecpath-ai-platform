def test_environment():
    print('Testing Day 3 Setup...')
    import os
    assert os.path.exists('data'), 'data folder missing'
    assert os.path.exists('parsers'), 'parsers folder missing'
    assert os.path.exists('tests'), 'tests folder missing'
    print('✅ All tests passed!')
    
if __name__ == '__main__':
    test_environment()
