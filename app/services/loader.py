"""Data loader service - orchestrates file reading and database loading."""

from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging

from app.models.layout import LayoutConfig, load_layout_config
from app.services.file_reader import (
    read_fixed_width_file,
    get_file_path,
    discover_data_files
)
from app.services.database import DatabaseService
from app.config import DATA_DIR, CONFIG_DIR, BATCH_SIZE


logger = logging.getLogger("cad_loader")


class DataLoader:
    """Orchestrates loading of CAD data files into the database."""
    
    def __init__(
        self,
        config_path: Optional[Path] = None,
        data_dir: Optional[Path] = None,
        db_service: Optional[DatabaseService] = None
    ):
        """
        Initialize the data loader.
        
        Args:
            config_path: Path to layout config JSON
            data_dir: Directory containing data files
            db_service: Database service instance
        """
        self.config_path = config_path or CONFIG_DIR / "file_layouts.json"
        self.data_dir = data_dir or DATA_DIR
        self.db_service = db_service or DatabaseService()
        self._layout_config = None
    
    @property
    def layout_config(self) -> LayoutConfig:
        """Lazy load layout configuration."""
        if self._layout_config is None:
            self._layout_config = load_layout_config(self.config_path)
            logger.info(f"Loaded layout config: {self._layout_config.description}")
        return self._layout_config
    
    def load_file(
        self,
        file_type: str,
        truncate: bool = True,
        max_records: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Load a single file type into the database.
        
        Args:
            file_type: File type name (e.g., 'INFO', 'ENTITY')
            truncate: Whether to truncate table before loading
            max_records: Maximum records to load (None for all)
            
        Returns:
            Dict with load results
        """
        start_time = datetime.now()
        result = {
            "file_type": file_type,
            "status": "FAILED",
            "records_loaded": 0,
            "error": None
        }
        
        try:
            # Get file configuration
            file_config = self.layout_config.get_file_config(file_type)
            if not file_config:
                raise ValueError(f"No configuration found for file type: {file_type}")
            
            # Build file path
            file_path = get_file_path(
                self.data_dir,
                self.layout_config.filePrefix,
                file_type
            )
            
            if not file_path.exists():
                raise FileNotFoundError(f"Data file not found: {file_path}")
            
            # Truncate if requested
            if truncate:
                self.db_service.truncate_table(file_config.tableName)
            
            # Read and insert records using streaming
            records_gen = read_fixed_width_file(
                file_path,
                file_config,
                self.layout_config.encoding,
                max_records=max_records
            )
            
            records_loaded = self.db_service.insert_records_streaming(
                records_gen,
                file_config,
                batch_size=BATCH_SIZE
            )
            
            result["status"] = "SUCCESS"
            result["records_loaded"] = records_loaded
            
        except Exception as e:
            logger.error(f"Error loading {file_type}: {e}")
            result["error"] = str(e)
        
        # Calculate duration
        duration = (datetime.now() - start_time).total_seconds()
        result["duration_seconds"] = duration
        
        # Log to database
        self.db_service.log_data_load(
            file_name=f"{self.layout_config.filePrefix}{file_type}.TXT",
            table_name=file_config.tableName if file_config else file_type,
            records_loaded=result["records_loaded"],
            status=result["status"],
            error_message=result.get("error")
        )
        
        return result
    
    def load_all_files(
        self,
        truncate: bool = True,
        file_types: Optional[List[str]] = None,
        max_records: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Load all configured file types.
        
        Args:
            truncate: Whether to truncate tables before loading
            file_types: Specific file types to load (None for all)
            max_records: Maximum records per file (None for all)
            
        Returns:
            List of load results
        """
        results = []
        
        # Get file types to process
        types_to_load = file_types or self.layout_config.file_names
        
        # Define load order (reference tables first)
        priority_order = [
            "HEADER",
            "STATE_CODE",
            "COUNTRY_CODE",
            "ABSTRACT_SUBDV",
            "AGENT",
            "ENTITY",
            "ENTITY_TOTALS",
            "INFO",
            "ENTITY_INFO",
            "LAND_DETAIL",
            "IMPROVEMENT_INFO",
            "IMPROVEMENT_DETAIL",
            "IMPROVEMENT_DETAIL_ATTR",
            "LAWSUIT",
            "MOBILE_HOME_INFO",
            "TAX_DEFERRAL_INFO",
            "UDI"
        ]
        
        # Sort types by priority
        ordered_types = []
        for ft in priority_order:
            if ft in types_to_load:
                ordered_types.append(ft)
        
        # Add any remaining types not in priority list
        for ft in types_to_load:
            if ft not in ordered_types:
                ordered_types.append(ft)
        
        logger.info(f"Loading {len(ordered_types)} file types")
        
        for file_type in ordered_types:
            logger.info(f"Processing: {file_type}")
            result = self.load_file(
                file_type,
                truncate=truncate,
                max_records=max_records
            )
            results.append(result)
            
            if result["status"] == "SUCCESS":
                logger.info(
                    f"Loaded {result['records_loaded']} records "
                    f"in {result['duration_seconds']:.2f}s"
                )
            else:
                logger.warning(f"Failed to load {file_type}: {result['error']}")
        
        return results
    
    def get_available_files(self) -> List[str]:
        """
        Get list of available data files.
        
        Returns:
            List of file type names found in data directory
        """
        return discover_data_files(self.data_dir, self.layout_config.filePrefix)
    
    def get_load_summary(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate summary of load results.
        
        Args:
            results: List of load results from load_all_files
            
        Returns:
            Summary dictionary
        """
        successful = [r for r in results if r["status"] == "SUCCESS"]
        failed = [r for r in results if r["status"] == "FAILED"]
        
        return {
            "total_files": len(results),
            "successful": len(successful),
            "failed": len(failed),
            "total_records": sum(r["records_loaded"] for r in successful),
            "total_duration": sum(r.get("duration_seconds", 0) for r in results),
            "failed_files": [r["file_type"] for r in failed]
        }
