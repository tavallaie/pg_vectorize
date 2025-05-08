from pgvectorzie import PgVectorize, VectorizeConfig

cfg = VectorizeConfig(
    host="127.0.0.1",
    port=5432,
    dbname="postgres",
    user="postgres",
    password="postgres",
)

pgv = PgVectorize(cfg)

# Cluster-wide override (affects bg workers too):
pgv.set_embedding_service_url("http://localhost:3000/v1/embeddings")
pgv.set_openai_service_url("http://localhost:1234/v1")
pgv.set_openai_key("sk-5456454efasdfsfasdf54df5asasdfsdfsdf")

# Now use the core API:
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
print(results)

answer = pgv.rag("product_chat", "What is a pencil?")
print(answer)
