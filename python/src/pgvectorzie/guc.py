from enum import Enum


class VectorizeGuc(Enum):
    OPENAI_KEY = "vectorize.openai_key"
    OPENAI_SERVICE_URL = "vectorize.openai_service_url"
    EMBEDDING_SERVICE_URL = "vectorize.embedding_service_url"
    EMBEDDING_SERVICE_API_KEY = "vectorize.embedding_service_api_key"
    OLLAMA_SERVICE_URL = "vectorize.ollama_service_url"
    TEMBO_SERVICE_URL = "vectorize.tembo_service_url"
    TEMBO_JWT = "vectorize.tembo_jwt"
    COHERE_API_KEY = "vectorize.cohere_api_key"
    PORTKEY_SERVICE_URL = "vectorize.portkey_service_url"
    PORTKEY_API_KEY = "vectorize.portkey_api_key"
    PORTKEY_VIRTUAL_KEY = "vectorize.portkey_virtual_key"
    VOYAGE_SERVICE_URL = "vectorize.voyage_service_url"
    VOYAGE_API_KEY = "vectorize.voyage_api_key"
    BATCH_SIZE = "vectorize.batch_size"
    NUM_BGW_PROC = "vectorize.num_bgw_proc"
    EMBEDDING_REQ_TIMEOUT = "vectorize.embedding_req_timeout_sec"
    SEMANTIC_WEIGHT = "vectorize.semantic_weight"
    FTS_INDEX_TYPE = "vectorize.experimental_fts_index_type"
