"""Generic fixed-width file reader service."""

from pathlib import Path
from typing import Generator, Dict, Any, List, Optional
import logging

from app.models.layout import FileConfig, ColumnConfig, LayoutConfig


logger = logging.getLogger("cad_loader")


def parse_value(value: str, column: ColumnConfig) -> Any:
    """
    Parse a string value based on column data type.
    
    Args:
        value: Raw string value from file
        column: Column configuration with data type info
        
    Returns:
        Parsed value in appropriate Python type
    """
    # Strip whitespace
    value = value.strip()
    
    # Handle empty values
    if not value:
        return None
        
    # Apply code mappings if available
    if column.codeMappings and value in column.codeMappings:
        value = column.codeMappings[value]
    
    data_type = column.dataType.upper()
    
    try:
        if data_type in ('INTEGER', 'INT'):
            return int(value)
        elif data_type == 'BIGINT':
            return int(value)
        elif data_type == 'DECIMAL':
            # Handle implied decimal places if precision specified
            if column.precision and '.' not in value:
                divisor = 10 ** column.precision
                return float(value) / divisor
            return float(value)
        elif data_type in ('VARCHAR', 'CHAR', 'TEXT'):
            return value
        else:
            return value
    except (ValueError, TypeError):
        logger.debug(f"Could not parse '{value}' as {data_type} for {column.name}")
        return value if data_type in ('VARCHAR', 'CHAR', 'TEXT') else None


def parse_line(line: str, file_config: FileConfig) -> Dict[str, Any]:
    """
    Parse a single line from a fixed-width file.
    
    Args:
        line: Raw line from the file
        file_config: File configuration with column definitions
        
    Returns:
        Dictionary mapping column names to parsed values
    """
    record = {}
    position = 0
    
    for column in file_config.columns:
        # Determine start and end positions
        if column.start is not None:
            # Use explicit start position (convert 1-based to 0-based)
            start_position = column.start - 1
            end_position = start_position + column.length
            # Update current position pointer for subsequent sequential columns if mixed
            position = end_position
        else:
            # Use sequential positioning
            start_position = position
            end_position = position + column.length
            position = end_position

        # Extract the field value
        # Handle case where line is shorter than expected
        if len(line) >= end_position:
            raw_value = line[start_position:end_position]
        elif len(line) > start_position:
            raw_value = line[start_position:]
        else:
            raw_value = ""
        
        # Skip columns marked as skip
        if column.skip:
            continue
        
        # Parse and store the value
        record[column.name] = parse_value(raw_value, column)
    
    return record


def read_fixed_width_file(
    file_path: Path,
    file_config: FileConfig,
    encoding: str = "utf-8",
    skip_header: bool = False,
    max_records: Optional[int] = None
) -> Generator[Dict[str, Any], None, None]:
    """
    Read a fixed-width file and yield parsed records.
    
    Args:
        file_path: Path to the data file
        file_config: Configuration for this file type
        encoding: File encoding
        skip_header: Whether to skip the first line
        max_records: Maximum number of records to read (None for all)
        
    Yields:
        Parsed record dictionaries
    """
    logger.info(f"Reading file: {file_path.name}")
    
    record_count = 0
    
    with open(file_path, 'r', encoding=encoding, errors='replace') as f:
        for line_num, line in enumerate(f, start=1):
            # Skip header if requested
            if skip_header and line_num == 1:
                continue
            
            # Skip empty lines
            if not line.strip():
                continue
            
            try:
                record = parse_line(line, file_config)
                record_count += 1
                yield record
                
                # Check max records limit
                if max_records and record_count >= max_records:
                    logger.info(f"Reached max records limit: {max_records}")
                    break
                    
            except Exception as e:
                logger.warning(f"Error parsing line {line_num}: {e}")
                continue
    
    logger.info(f"Processed {record_count} records from {file_path.name}")


def read_all_records(
    file_path: Path,
    file_config: FileConfig,
    encoding: str = "utf-8",
    max_records: Optional[int] = None
) -> List[Dict[str, Any]]:
    """
    Read all records from a fixed-width file into a list.
    
    Args:
        file_path: Path to the data file
        file_config: Configuration for this file type
        encoding: File encoding
        max_records: Maximum number of records to read (None for all)
        
    Returns:
        List of parsed record dictionaries
    """
    return list(read_fixed_width_file(
        file_path, 
        file_config, 
        encoding, 
        max_records=max_records
    ))


def get_file_path(
    data_dir: Path,
    file_prefix: str,
    file_name: str
) -> Path:
    """
    Construct the full file path for a data file.
    
    Args:
        data_dir: Directory containing data files
        file_prefix: Common file prefix
        file_name: File type name (e.g., 'INFO')
        
    Returns:
        Full path to the file
    """
    return data_dir / f"{file_prefix}{file_name}.TXT"


def discover_data_files(data_dir: Path, file_prefix: str) -> List[str]:
    """
    Discover available data files in a directory.
    
    Args:
        data_dir: Directory to search
        file_prefix: File prefix pattern
        
    Returns:
        List of file type names found
    """
    file_types = []
    
    for file_path in data_dir.glob(f"{file_prefix}*.TXT"):
        # Extract file type from name
        file_type = file_path.stem.replace(file_prefix, "")
        file_types.append(file_type)
    
    logger.info(f"Discovered {len(file_types)} data files")
    return sorted(file_types)
