# infrastructure/database/session.py
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
# from sqlalchemy.pool import AsyncAdapterPool
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class DatabaseSessionManager:
    _instance= None
    _engine = None
    _session_maker = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, pool_size: int = 20, max_overflow: int = 10,
                 pool_timeout: float = 30, pool_recycle: int = 1800, echo: bool = False):
        # Only initialize if it hasn't been initialized
        if not hasattr(self, '_initialized'):
            self._database_url = "mysql+aiomysql://myuser:mypassword@localhost:3306/mydatabase"
            self._pool_size = pool_size
            self._max_overflow = max_overflow
            self._pool_timeout = pool_timeout
            self._pool_recycle = pool_recycle
            self._echo = echo
            self._initialized = True
            self._setup_engine()
    
    def _setup_engine(self) -> None:
        """Initialize the SQLAlchemy engine with the given configuration"""
        if not self._engine:
            try:
                self._engine = create_async_engine(
                    self._database_url,
                    pool_size=self._pool_size,
                    max_overflow=self._max_overflow,
                    pool_timeout=self._pool_timeout,
                    pool_recycle=self._pool_recycle,
                    echo=self._echo
                )
                
                self._session_maker = async_sessionmaker(
                    bind=self._engine,
                    class_=AsyncSession,
                    expire_on_commit=False,
                    autoflush=False
                )
                
                logger.info("Database engine initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize database engine: {str(e)}")
                raise
    
    async def get_session(self) -> AsyncSession:
        """Get a new database session"""
        if not self._session_maker:
            raise RuntimeError("Database session maker not initialized")
        return self._session_maker()
    
    async def close(self) -> None:
        """Close the database engine and all connections"""
        if self._engine:
            try:
                await self._engine.dispose()
                self._engine = None
                self._session_maker = None
                logger.info("Database engine closed successfully")
            except Exception as e:
                logger.error(f"Error closing database engine: {str(e)}")
                raise
    
    @property
    def engine(self):
        """Get the current engine instance"""
        return self._engine
    
    @property
    def pool(self):
        """Get the connection pool"""
        if not self._engine:
            raise RuntimeError("Database engine not initialized")
        return self._engine.pool

# # Example usage in FastAPI dependency
# async def get_db_session() -> AsyncSession:
#     """FastAPI dependency for database session"""
#     db_manager = DatabaseSessionManager(database_url="your_database_url_here")
#     async with db_manager.get_session() as session:
#         try:
#             yield session
#         finally:
#             await session.close()