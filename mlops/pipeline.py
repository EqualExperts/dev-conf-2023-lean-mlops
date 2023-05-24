from abc import ABC, abstractmethod
from dataclasses import dataclass
import duckdb
from typing import Callable
import mlflow
from mlops.featurestore import duck_db_conn
from mlops.utils import get_logger

@dataclass
class MLProduct(object):
    ml_product_name: str


@dataclass
class MLProductVariant(object):
    ml_product: MLProduct
    variant_name: str


class MLPipeline(object):

    def __init__(self, product_name: str, variant_name: str= "baseline"):
        self._duck_db :duckdb.DuckDBPyConnection = duck_db_conn()
        self._info = MLProductVariant(MLProduct("california_housing"), variant_name="location_features")

    @abstractmethod
    def run(self):
        raise NotImplemented("implement in derived pipelines")