from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime
import time
import logging
from memory import RedisMemory

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """Base class for all agents with retry logic and error handling."""
    
    def __init__(self, name: str, memory: RedisMemory):
        self.name = name
        self.memory = memory
        self.status = "idle"
        self.max_retries = 3
        self.retry_delay = 1  # seconds
        
    @abstractmethod
    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the agent's primary task. Must be implemented by subclasses."""
        pass
    
    def _retry_wrapper(self, func, *args, **kwargs):
        """Wrapper to add retry logic to any function."""
        last_error = None
        for attempt in range(self.max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_error = e
                logger.warning(
                    f"{self.name}: Attempt {attempt + 1}/{self.max_retries} failed: {str(e)}"
                )
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))  # Exponential backoff
        
        raise last_error
    
    def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process a task with error handling and context management."""
        task_id = task.get("task_id", f"{self.name}_{int(time.time())}")
        
        try:
            self.status = "processing"
            logger.info(f"{self.name}: Processing task {task_id}")
            
            # Store task in memory
            self.memory.set(f"task:{task_id}:status", "processing")
            self.memory.set(f"task:{task_id}:agent", self.name)
            self.memory.set(f"task:{task_id}:started_at", datetime.now().isoformat())
            
            # Execute with retry logic
            result = self._retry_wrapper(self.execute, task)
            
            # Store result
            self.memory.set(f"task:{task_id}:status", "completed")
            self.memory.set(f"task:{task_id}:result", result)
            self.memory.set(f"task:{task_id}:completed_at", datetime.now().isoformat())
            
            self.status = "idle"
            logger.info(f"{self.name}: Task {task_id} completed successfully")
            
            return {
                "status": "success",
                "task_id": task_id,
                "agent": self.name,
                "result": result
            }
            
        except Exception as e:
            self.status = "error"
            error_msg = str(e)
            logger.error(f"{self.name}: Task {task_id} failed: {error_msg}")
            
            # Store error
            self.memory.set(f"task:{task_id}:status", "failed")
            self.memory.set(f"task:{task_id}:error", error_msg)
            self.memory.set(f"task:{task_id}:failed_at", datetime.now().isoformat())
            
            return {
                "status": "error",
                "task_id": task_id,
                "agent": self.name,
                "error": error_msg
            }
    
    def get_status(self) -> Dict[str, str]:
        """Get current agent status."""
        return {
            "agent": self.name,
            "status": self.status,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_context(self, key: str) -> Optional[Any]:
        """Retrieve shared context from memory."""
        return self.memory.get(f"context:{key}")
    
    def set_context(self, key: str, value: Any) -> bool:
        """Store shared context in memory."""
        return self.memory.set(f"context:{key}", value)
