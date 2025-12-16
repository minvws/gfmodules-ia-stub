import logging
from typing import Any
from max_core.models.health_checker_collection import HealthCheckerCollection

from fastapi import APIRouter, Depends

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/health")
def health(
    health_checker: HealthCheckerCollection = Depends(HealthCheckerCollection),
) -> dict[str, Any]:
    logger.info("Checking health")

    return health_checker[0].to_dict()
