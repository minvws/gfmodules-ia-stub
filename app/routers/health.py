import logging
from typing import Annotated, Any

from fastapi import APIRouter, Depends
from max_core.models.health_checker_collection import HealthCheckerCollection

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/health")
def health(
    health_checker: Annotated[
        HealthCheckerCollection, Depends(HealthCheckerCollection)
    ],
) -> dict[str, Any]:
    logger.info("Checking health")

    return health_checker[0].to_dict()
