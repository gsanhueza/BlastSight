# MineVis

MineVis is a 3D visualization software designed to aid in Mining research.

## Testing

Create a `.coveragerc` file with the following content:

```python
[coverage:run]
branch = True

[coverage:report]
show_missing = True
omit = 
    main.py
    example.py
    # tests/*

```

Run the following command: `python -m pytest --cov=. tests/`

