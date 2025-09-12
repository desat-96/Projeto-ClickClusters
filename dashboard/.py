import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa
import math

input_file = "./data/dash_final_prod.parquet"

df = pd.read_parquet(input_file)

target_mb = 50
target_bytes = target_mb * 1024 * 1024

table = pa.Table.from_pandas(df)
total_size = table.nbytes

n_parts = math.ceil(total_size / target_bytes)

print(f"Tamanho total: {total_size/1024/1024:.2f} MB")
print(f"Quebrando em {n_parts} arquivos...")

rows_per_part = math.ceil(len(df) / n_parts)

for i in range(n_parts):
    start = i * rows_per_part
    end = (i + 1) * rows_per_part
    df_part = df.iloc[start:end]

    output_file = f"./data/output_part{i+1}.parquet"
    df_part.to_parquet(output_file, index=False)
    print(f"Salvo {output_file} com {len(df_part)} linhas")