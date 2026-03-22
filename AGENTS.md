# Agent Guidelines for track-sorter

This is a Python CLI tool for sorting and concatenating audio tracks using tracklists.

## Build/Development Commands

This project uses `uv` for dependency management and package building.

```bash
# Install dependencies
uv sync

# Install with dev dependencies
uv sync --dev

# Build the package
uv build

# Run the CLI
uv run track-sorter --help

# Run the module directly
uv run python -m track_sorter --help
```

## Testing Commands

No test framework is currently configured. To add tests:

```bash
# Install pytest
uv add --dev pytest

# Run all tests (after adding pytest)
uv run pytest

# Run a single test file
uv run pytest tests/test_specific.py

# Run a single test function
uv run pytest tests/test_specific.py::test_function_name -v
```

## Linting and Type Checking

No linting tools are currently configured. Recommended setup:

```bash
# Install linting tools
uv add --dev ruff mypy

# Run ruff linter
uv run ruff check src/

# Run ruff formatter
uv run ruff format src/

# Run type checker
uv run mypy src/
```

## Code Style Guidelines

### Imports
- Group imports: standard library, third-party, local
- Use absolute imports for project modules
- Use `from module import specific_name` for returns library types

Example:
```python
import pathlib
import ffmpeg
from returns.result import Result, Failure, Success
```

### Type Hints
- Use type hints for all function parameters and return types
- Use `Result[SuccessType, FailureType]` from returns library for error handling
- Prefer `list[T]` over `List[T]` (Python 3.13+)

### Naming Conventions
- `snake_case` for functions and variables
- `PascalCase` for classes (if any)
- Descriptive names for clarity

### Error Handling
- Use `returns.result.Result` for functional error handling
- Use `Success(value)` for success cases
- Use `Failure(error_message)` for failure cases
- Check Result types with `isinstance(result, Failure)`
- Unwrap successful values with `result.unwrap()`

Example:
```python
def find_target(track: str, audio_dir: pathlib.Path) -> Result[pathlib.Path, str]:
    if not_found:
        return Failure(f"Error message: {track}")
    return Success(matched_path)
```

### CLI Development
- Use `argparse` for command-line interfaces
- Provide helpful descriptions in Chinese for user-facing messages
- Use `pathlib.Path` for all file path operations
- Set sensible defaults for optional arguments

### String Formatting
- Use f-strings for string formatting
- User-facing messages are in Chinese
- Error messages should be descriptive

### Functional Programming
- Leverage the `returns` library for functional patterns
- Chain operations using Result types
- Avoid exceptions for control flow; use Result types instead

## Project Structure

```
src/
  track_sorter/
    __init__.py      # Exports main functions
    __main__.py      # Entry point for `python -m track_sorter`
    track_sorter.py  # Main implementation
```

## Dependencies

- Python >= 3.13
- ffmpeg-python: FFmpeg Python bindings
- returns: Functional programming primitives

## CLI Usage

```bash
# Basic usage
uv run track-sorter -d /path/to/audio -l tracklist.txt -o output.flac

# Use defaults (current directory, tracklist.txt)
uv run track-sorter
```

## Notes for Agents

1. This codebase uses functional programming patterns with the `returns` library
2. All user-facing output is in Chinese
3. FFmpeg is required for audio concatenation operations
4. The tool renames audio files based on tracklist order before concatenating
5. No existing tests or linting configuration - add these if modifying code significantly
