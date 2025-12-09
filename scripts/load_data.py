#!/usr/bin/env python3
"""
Kaufman CAD Data Loader
Loads fixed-width CAD data files into PostgreSQL database
"""

import sys
from pathlib import Path
import time
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.utils.logging_config import setup_logger
from app.models.layout import load_layout_config
from app.services.database import DatabaseService
from app.services.loader import DataLoader
from app.config import DATA_DIR, CONFIG_DIR, DATABASE_CONFIG

def print_banner():
    """Print startup banner"""
    print("=" * 70)
    print("  KAUFMAN CAD DATA LOADER")
    print("  Kaufman County Central Appraisal District")
    print("=" * 70)
    print(f"  Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Data Directory: {DATA_DIR}")
    print(f"  Config Directory: {CONFIG_DIR}")
    print("=" * 70)
    print()

def load_tables(loader, logger):
    """Load all data tables in the correct order"""
    
    # Define loading order: reference tables first, then main tables
    loading_order = [
        {
            "name": "Reference Tables",
            "tables": ["HEADER", "STATE_CODE", "COUNTRY_CODE", "ABSTRACT_SUBDV", "AGENT", "ENTITY"]
        },
        {
            "name": "Main Property Tables",
            "tables": ["INFO", "LAND_DETAIL", "IMPROVEMENT_INFO", "IMPROVEMENT_DETAIL", 
                      "IMPROVEMENT_DETAIL_ATTR"]
        },
        {
            "name": "Entity and Relationship Tables",
            "tables": ["ENTITY_INFO", "ENTITY_TOTALS"]
        },
        {
            "name": "Additional Tables",
            "tables": ["LAWSUIT", "MOBILE_HOME_INFO", "TAX_DEFERRAL_INFO", "UDI"]
        }
    ]
    
    overall_start = time.time()
    total_records = 0
    total_tables = sum(len(group["tables"]) for group in loading_order)
    tables_loaded = 0
    
    for group in loading_order:
        logger.info(f"\n{'='*70}")
        logger.info(f"Loading {group['name']}")
        logger.info(f"{'='*70}")
        
        for table in group["tables"]:
            tables_loaded += 1
            logger.info(f"\n[{tables_loaded}/{total_tables}] Loading {table}...")
            
            try:
                result = loader.load_file(table)
                
                if result["status"] == "SUCCESS":
                    duration = result.get('duration_seconds', 0)
                    records = result['records_loaded']
                    total_records += records
                    
                    logger.info(f"✅ {table}: {records:,} records in {duration:.1f}s")
                    
                    if duration > 0:
                        rate = records / duration
                        logger.info(f"   Rate: {rate:,.0f} records/second")
                else:
                    logger.error(f"❌ {table}: {result.get('error', 'Unknown error')}")
                    
            except Exception as e:
                logger.error(f"❌ {table}: Error - {str(e)}")
    
    overall_duration = time.time() - overall_start
    
    logger.info(f"\n{'='*70}")
    logger.info("LOADING SUMMARY")
    logger.info(f"{'='*70}")
    logger.info(f"Tables loaded: {tables_loaded}")
    logger.info(f"Total records: {total_records:,}")
    logger.info(f"Total time: {overall_duration:.1f}s ({overall_duration/60:.1f} minutes)")
    logger.info(f"Average rate: {total_records/overall_duration:,.0f} records/second")
    logger.info(f"{'='*70}\n")

def verify_data(db_service, logger):
    """Verify loaded data with record counts"""
    logger.info("\n" + "="*70)
    logger.info("VERIFICATION - Table Record Counts")
    logger.info("="*70)
    
    tables = [
        "appraisal_header",
        "appraisal_info",
        "appraisal_entity",
        "appraisal_entity_info",
        "appraisal_entity_totals",
        "appraisal_land_detail",
        "appraisal_improvement_info",
        "appraisal_improvement_detail"
    ]
    
    total = 0
    for table in tables:
        try:
            count = db_service.get_table_count(table)
            total += count
            logger.info(f"  {table:40} {count:>10,}")
        except Exception as e:
            logger.warning(f"  {table:40} {'ERROR':>10}")
    
    logger.info("-" * 70)
    logger.info(f"  {'TOTAL':40} {total:>10,}")
    logger.info("="*70 + "\n")

def main():
    """Main entry point"""
    print_banner()
    
    # Setup logging
    logger = setup_logger("data_loader", level="INFO")
    
    try:
        # Load configuration
        logger.info("Loading configuration...")
        layout_config = load_layout_config(CONFIG_DIR / "file_layouts.json")
        logger.info(f"✅ Configuration loaded (Tax Year: {layout_config.taxYear})")
        logger.info(f"   File types configured: {len(layout_config.files)}")
        
        # Connect to database
        logger.info("\nConnecting to database...")
        db_service = DatabaseService(DATABASE_CONFIG)
        logger.info(f"✅ Database connected: {DATABASE_CONFIG['database']}@{DATABASE_CONFIG['host']}")
        
        # Initialize loader
        loader = DataLoader(
            config_path=CONFIG_DIR / "file_layouts.json",
            data_dir=DATA_DIR,
            db_service=db_service
        )
        
        # Load all tables
        load_tables(loader, logger)
        
        # Verify data
        verify_data(db_service, logger)
        
        logger.info("✅ Data loading completed successfully!")
        return 0
        
    except Exception as e:
        logger.error(f"\n❌ Fatal error: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return 1

if __name__ == "__main__":
    sys.exit(main())
