"""Database connection and operations service."""

from typing import Dict, Any, List, Optional, Generator
from contextlib import contextmanager
import logging

import psycopg2
from psycopg2.extras import execute_batch
from psycopg2 import sql

from app.config import DATABASE_CONFIG, BATCH_SIZE
from app.models.layout import FileConfig


logger = logging.getLogger("cad_loader")


class DatabaseService:
    """Service for database operations."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize database service.
        
        Args:
            config: Database configuration dict. Uses default if None.
        """
        self.config = config or DATABASE_CONFIG
        self._connection = None
    
    @contextmanager
    def get_connection(self):
        """
        Context manager for database connections.
        
        Yields:
            Database connection
        """
        conn = None
        try:
            conn = psycopg2.connect(
                host=self.config["host"],
                port=self.config["port"],
                database=self.config["database"],
                user=self.config["user"],
                password=self.config["password"]
            )
            yield conn
        finally:
            if conn:
                conn.close()
    
    def test_connection(self) -> bool:
        """
        Test database connectivity.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT 1")
                    logger.info("Database connection successful")
                    return True
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            return False
    
    def execute_sql_file(self, file_path: str) -> bool:
        """
        Execute SQL statements from a file.
        
        Args:
            file_path: Path to SQL file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(file_path, 'r') as f:
                sql_content = f.read()
            
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(sql_content)
                conn.commit()
            
            logger.info(f"Executed SQL file: {file_path}")
            return True
        except Exception as e:
            logger.error(f"Error executing SQL file: {e}")
            return False
    
    def truncate_table(self, table_name: str, schema: str = "cad") -> bool:
        """
        Truncate a table.
        
        Args:
            table_name: Name of table to truncate
            schema: Schema name
            
        Returns:
            True if successful
        """
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        sql.SQL("TRUNCATE TABLE {}.{} CASCADE").format(
                            sql.Identifier(schema),
                            sql.Identifier(table_name)
                        )
                    )
                conn.commit()
            logger.info(f"Truncated table: {schema}.{table_name}")
            return True
        except Exception as e:
            logger.error(f"Error truncating table: {e}")
            return False
    
    def insert_records(
        self,
        records: List[Dict[str, Any]],
        file_config: FileConfig,
        schema: str = "cad",
        batch_size: int = BATCH_SIZE
    ) -> int:
        """
        Insert records into database table.
        
        Args:
            records: List of record dictionaries
            file_config: File configuration with table info
            schema: Database schema
            batch_size: Records per batch
            
        Returns:
            Number of records inserted
        """
        if not records:
            return 0
        
        # Get active column names (not skipped)
        columns = [col.name for col in file_config.active_columns]
        table_name = file_config.tableName
        
        # Build INSERT statement
        insert_sql = sql.SQL("INSERT INTO {}.{} ({}) VALUES ({})").format(
            sql.Identifier(schema),
            sql.Identifier(table_name),
            sql.SQL(", ").join(map(sql.Identifier, columns)),
            sql.SQL(", ").join(sql.Placeholder() * len(columns))
        )
        
        inserted = 0
        
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    # Process in batches
                    for i in range(0, len(records), batch_size):
                        batch = records[i:i + batch_size]
                        values = [
                            tuple(record.get(col) for col in columns)
                            for record in batch
                        ]
                        execute_batch(cur, insert_sql.as_string(conn), values)
                        inserted += len(batch)
                        
                        if inserted % 10000 == 0:
                            logger.info(f"Inserted {inserted} records into {table_name}")
                
                conn.commit()
            
            logger.info(f"Completed inserting {inserted} records into {schema}.{table_name}")
            return inserted
            
        except Exception as e:
            logger.error(f"Error inserting records: {e}")
            raise
    
    def insert_records_streaming(
        self,
        records_generator: Generator[Dict[str, Any], None, None],
        file_config: FileConfig,
        schema: str = "cad",
        batch_size: int = BATCH_SIZE
    ) -> int:
        """
        Insert records from a generator (memory efficient).
        
        Args:
            records_generator: Generator yielding record dicts
            file_config: File configuration
            schema: Database schema
            batch_size: Records per batch
            
        Returns:
            Number of records inserted
        """
        columns = [col.name for col in file_config.active_columns]
        table_name = file_config.tableName
        
        insert_sql = sql.SQL("INSERT INTO {}.{} ({}) VALUES ({})").format(
            sql.Identifier(schema),
            sql.Identifier(table_name),
            sql.SQL(", ").join(map(sql.Identifier, columns)),
            sql.SQL(", ").join(sql.Placeholder() * len(columns))
        )
        
        inserted = 0
        skipped = 0
        batch = []
        
        with self.get_connection() as conn:
            sql_str = insert_sql.as_string(conn)
            
            for record in records_generator:
                batch.append(
                    tuple(record.get(col) for col in columns)
                )
                
                if len(batch) >= batch_size:
                    try:
                        with conn.cursor() as cur:
                            execute_batch(cur, sql_str, batch)
                        conn.commit()
                        inserted += len(batch)
                    except Exception as e:
                        conn.rollback()
                        # Try inserting one by one to skip bad records
                        for row in batch:
                            try:
                                with conn.cursor() as cur:
                                    cur.execute(sql_str, row)
                                conn.commit()
                                inserted += 1
                            except Exception:
                                conn.rollback()
                                skipped += 1
                    batch = []
                    
                    if inserted % 10000 == 0:
                        logger.info(f"Inserted {inserted} records into {table_name}")
            
            # Insert remaining records
            if batch:
                try:
                    with conn.cursor() as cur:
                        execute_batch(cur, sql_str, batch)
                    conn.commit()
                    inserted += len(batch)
                except Exception:
                    conn.rollback()
                    for row in batch:
                        try:
                            with conn.cursor() as cur:
                                cur.execute(sql_str, row)
                            conn.commit()
                            inserted += 1
                        except Exception:
                            conn.rollback()
                            skipped += 1
        
        if skipped > 0:
            logger.warning(f"Skipped {skipped} bad records")
        logger.info(f"Completed inserting {inserted} records into {schema}.{table_name}")
        return inserted
    
    def get_table_count(self, table_name: str, schema: str = "cad") -> int:
        """
        Get record count for a table.
        
        Args:
            table_name: Table name
            schema: Schema name
            
        Returns:
            Record count
        """
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        sql.SQL("SELECT COUNT(*) FROM {}.{}").format(
                            sql.Identifier(schema),
                            sql.Identifier(table_name)
                        )
                    )
                    return cur.fetchone()[0]
        except Exception as e:
            logger.error(f"Error getting table count: {e}")
            return -1
    
    def log_data_load(
        self,
        file_name: str,
        table_name: str,
        records_loaded: int,
        status: str,
        error_message: Optional[str] = None,
        schema: str = "cad"
    ) -> None:
        """
        Log a data load operation.
        
        Args:
            file_name: Source file name
            table_name: Target table
            records_loaded: Number of records
            status: Load status (SUCCESS, FAILED, etc.)
            error_message: Error message if failed
            schema: Database schema
        """
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        sql.SQL("""
                            INSERT INTO {}.data_load_log 
                            (file_name, table_name, records_loaded, status, error_message, load_end)
                            VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                        """).format(sql.Identifier(schema)),
                        (file_name, table_name, records_loaded, status, error_message)
                    )
                conn.commit()
        except Exception as e:
            logger.warning(f"Could not log data load: {e}")
