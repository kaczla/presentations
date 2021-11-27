#!/usr/bin/env python3

"""Simple script for sorting elements in README.md sections"""

import logging
from pathlib import Path
from typing import Set, List, Tuple

LOGGER = logging.getLogger(__name__)

ELEMENT_SEPARATOR = ' - '
ELEMENT_PREFIX = '- '


def sort_elements(elements: List[str]) -> List[str]:
    """
    Sort elements.

    Example element:
    ```
    - Transformer - [Attention Is All You Need](https://arxiv.org/abs/1706.03762)
    ```

    Args:
        elements: elements to sort

    Returns:
        sorted elements

    """
    uniq_elements: Set[Tuple[str, str, str]] = set()

    # Parse elements to sort
    for element in elements:
        # Skip invalid elements
        if not element.startswith(ELEMENT_PREFIX):
            logging.error(f'Cannot parse element: {repr(element)}')
            continue

        element = element[2:].strip()
        # Parse into name and metadata (url)
        try:
            element_name, element_metadata = element.split(ELEMENT_SEPARATOR, maxsplit=1)
        except ValueError:
            logging.error(f'Cannot parse element - invalid format: {repr(element)}')
            continue

        # Normalize name for better sorting
        element_name_normalized = element.strip().lower()

        # Skip duplicates
        if (element_name, element_metadata) in uniq_elements:
            continue
        uniq_elements.add((element_name_normalized, element_name, element_metadata))

    # Sort elements - will be sorted elements in tuple
    sorted_elements: List[str] = [
        f'{ELEMENT_PREFIX}{x}{ELEMENT_SEPARATOR}{y}' for _, x, y in sorted(uniq_elements)
    ]

    logging.info(f'Sorted {len(elements)}')

    # Add empty line at the beginning and empty line with horizontal line at the end
    sorted_elements.append('')
    sorted_elements.append('---')
    sorted_elements.insert(0, '')

    return sorted_elements


def main(readme_path: Path) -> None:
    """
    Sort elements in README file.

    Args:
        readme_path: README file path

    """
    if not readme_path.exists():
        raise RuntimeError(f'Not found README file in: {readme_path}')

    LOGGER.info(f'Processing README file from: {readme_path}')

    readme_text: List[str] = []
    elements_to_sort: List[str] = []
    sections_to_sort: Set[str] = {'# Models', '# Benchmarks'}
    is_section_text = False

    for line in readme_path.read_text().split('\n'):
        # print(line)

        # Sort given elements
        if is_section_text:
            # Sort collected elements
            if line == '---' or line in sections_to_sort:
                is_section_text = False
                readme_text.extend(sort_elements(elements_to_sort))
                elements_to_sort = []
                continue

            # Skip empty line
            line = line.strip()
            if not line:
                continue

            elif not line.startswith('- '):
                logging.error(f'Skip invalid element to sort: {repr(line)}')
                continue

            elements_to_sort.append(line)
            continue

        if line in sections_to_sort:
            logging.info(f'Found section to sort: {line.strip()}')
            is_section_text = True

        readme_text.append(line)

    if elements_to_sort:
        is_section_text = False
        readme_text.extend(sort_elements(elements_to_sort))
        elements_to_sort = []

    back_up_file_name = readme_path.name + '.bak'
    logging.info(f'Back up: {readme_path} into {back_up_file_name}')
    readme_path.rename(back_up_file_name)

    logging.info(f'Saving changes in: {readme_path}')
    readme_path.write_text('\n'.join(readme_text))

    logging.info('DONE')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main(Path('README.md'))
