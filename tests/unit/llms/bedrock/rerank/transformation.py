import json

import pytest
from fastapi.testclient import TestClient

from unittest.mock import MagicMock, patch

from linten import rerank
from linten.llms.custom_httpx.http_handler import HTTPHandler
