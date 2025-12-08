"""Data models for file layout configuration."""

from dataclasses import dataclass, field
from typing import List, Optional
import json
from pathlib import Path


@dataclass
class ColumnConfig:
    """Configuration for a single column in a fixed-width file."""
    
    index: int
    name: str
    description: str
    dataType: str
    length: int
    nullable: bool = True
    precision: Optional[int] = None
    skip: bool = False
    start: Optional[int] = None
    codeMappings: Optional[dict] = None
    
    def __post_init__(self):
        """Validate column configuration."""
        if self.length <= 0:
            raise ValueError(f"Column length must be positive: {self.name}")


@dataclass
class FileConfig:
    """Configuration for a single file type."""
    
    fileName: str
    tableName: str
    description: str
    columns: List[ColumnConfig]
    primaryKey: Optional[List[str]] = None
    
    @property
    def total_width(self) -> int:
        """Calculate total record width from columns."""
        return sum(col.length for col in self.columns)
    
    @property
    def active_columns(self) -> List[ColumnConfig]:
        """Get columns that should be loaded (not skipped)."""
        return [col for col in self.columns if not col.skip]


@dataclass
class LayoutConfig:
    """Root configuration containing all file layouts."""
    
    description: str
    version: str
    source: str
    taxYear: int
    filePrefix: str
    encoding: str
    files: List[FileConfig]
    
    def get_file_config(self, file_name: str) -> Optional[FileConfig]:
        """
        Get configuration for a specific file type.
        
        Args:
            file_name: File type name (e.g., 'INFO', 'ENTITY')
            
        Returns:
            FileConfig if found, None otherwise
        """
        for file_config in self.files:
            if file_config.fileName == file_name:
                return file_config
        return None
    
    @property
    def file_names(self) -> List[str]:
        """Get list of all file type names."""
        return [f.fileName for f in self.files]


def load_layout_config(config_path: Path) -> LayoutConfig:
    """
    Load layout configuration from JSON file.
    
    Args:
        config_path: Path to the configuration JSON file
        
    Returns:
        LayoutConfig object
        
    Raises:
        FileNotFoundError: If config file doesn't exist
        json.JSONDecodeError: If JSON is invalid
    """
    with open(config_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Parse files
    files = []
    for file_data in data.get('files', []):
        columns = [
            ColumnConfig(**col_data) 
            for col_data in file_data.get('columns', [])
        ]
        file_config = FileConfig(
            fileName=file_data['fileName'],
            tableName=file_data['tableName'],
            description=file_data['description'],
            columns=columns,
            primaryKey=file_data.get('primaryKey')
        )
        files.append(file_config)
    
    return LayoutConfig(
        description=data['description'],
        version=data['version'],
        source=data['source'],
        taxYear=data['taxYear'],
        filePrefix=data['filePrefix'],
        encoding=data['encoding'],
        files=files
    )
