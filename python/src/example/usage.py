from pgvectorzie import PgVectorize, VectorizeConfig
from pgvectorzie.guc import VectorizeGuc

# 1. Connection config only holds DB params
cfg = VectorizeConfig(
    host="127.0.0.1",
    port=5432,
    dbname="postgres",
    user="postgres",
    password="postgres",
)

# 2. Instantiate your client
pgv = PgVectorize(cfg)

# 3. Cluster-wide overrides for any GUC
pgv.set_guc(VectorizeGuc.EMBEDDING_SERVICE_URL, "http://localhost:3000/v1/embeddings")
pgv.set_guc(VectorizeGuc.OPENAI_SERVICE_URL, "http://localhost:1234/v1")
pgv.set_guc(VectorizeGuc.OPENAI_KEY, "sk-5456454efasdfsfasdf54df5asasdfsdfsdf")

# 4. Verify your overrides via SHOW
print("Embedding URL:", pgv.get_guc(VectorizeGuc.EMBEDDING_SERVICE_URL))
print("OpenAI URL:   ", pgv.get_guc(VectorizeGuc.OPENAI_SERVICE_URL))
print("OpenAI Key:   ", pgv.get_guc(VectorizeGuc.OPENAI_KEY))

# 5. Now use the core APIs as before
pgv.init_table(
    job_name="product_search",
    relation="products",
    primary_key="product_id",
    columns=["product_name", "description"],
    transformer="openai/all-MiniLM-L6-v2",
)

results = pgv.search(
    "product_search", "wireless earbuds", ["product_id", "product_name"], num_results=3
)
print("Search results:", results)

answer = pgv.rag("product_chat", "What is a pencil?")
print("RAG answer:", answer)
