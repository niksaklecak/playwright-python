"""
This module contains shared api fixtures.
"""
import pytest
from typing import Generator
from helpers.graphql_client import GraphQLClient



# ------------------------------------------------------------
# SpaceX api project fixtures
# ------------------------------------------------------------

@pytest.fixture(scope='session')
def execute_graphql_query() -> Generator[GraphQLClient, None, None]:
    graphQLClient = GraphQLClient()
    yield graphQLClient
    graphQLClient.close()

    
