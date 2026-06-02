from dataclasses import dataclass
import threading
import secrets as _secrets

@dataclass(slots=True)
class ActiveGeneration:
    user_id: int
    conversation_id: int
    cancel_event: threading.Event


class ActiveGenerationTracker:
    """
    Thread-safe registry for tracking active model generations, allowing for cancellation and cleanup. 
    Each active generation is associated with a unique request ID, user ID, conversation ID
    """

    def __init__(self) -> None:
        self._active_generations: dict[str, ActiveGeneration] = {}
        self._lock = threading.Lock()
    
    def _request_id(self) -> str:
        """Generate a new unique request ID for tracking an active generation."""
        return _secrets.token_urlsafe(32)
    
    def _register_active_generation(self, request_id: str, user_id: int, conversation_id: int,) -> threading.Event:
        """ Register a new active generation and return its cancellation event. """
        cancel_event = threading.Event()
        generation = ActiveGeneration(user_id=user_id, 
                                      conversation_id=conversation_id, 
                                      cancel_event=cancel_event)
        
        with self._lock:
            self._active_generations[request_id] = generation
        
        return cancel_event

    def _get_active_generation(self, request_id: str) -> dict | None:
        """ Retrieve the active generation associated with the given request ID, if it exists. """
        with self._lock:
            return self._active_generations.get(request_id)

    def _unregister_active_generation(self, request_id: str) -> None:
        """ Unregister generation after completion or cancellation to free up resources. """
        with self._lock:
            self._active_generations.pop(request_id, None)

tracker = ActiveGenerationTracker()