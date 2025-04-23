import polars as pl
import pyarrow as pa
import mckp


# Create test data with more customers and smaller numbers

treatment_ids = pa.array([
    [0, 1, 2, 3], 
    [0, 1, 2], 
    [0, 1, 2], 
    [0, 1, 2], 
    [0, 1, 2]
], type=pa.list_(pa.uint32()))

rewards = pa.array([
    [0, 15, 22, 30], 
    [0, 18, 32], 
    [0, 10, 19], 
    [0, 17, 28], 
    [0, 8, 18]
], type=pa.list_(pa.float64()))

costs = pa.array([
    [0, 10, 20, 21], 
    [0, 15, 25], 
    [0, 8, 16], 
    [0, 12, 22], 
    [0, 7, 14]
], type=pa.list_(pa.float64()))

table = pl.DataFrame({
    'treatment_id': treatment_ids,
    'reward': rewards,
    'cost': costs
})

# table = pa.Table.from_arrays(
#     [treatment_ids, rewards, costs],
#     names=["treatment_id", "reward", "cost"]
# )

# (
#     pl.from_arrow(table)
#         .select(pl.col("treatment_id").explode().unique())
#         .with_columns(pl.col('treatment_id').rank('dense', descending=True)) # dns should be 0 -- TODO: deal with this explicitly
# )

budget_constraint = 50

print("Python ListArray:", treatment_ids)
print("\nC++ Analysis:")

solver = mckp.Solver()

results = solver.fit(
    table,
    budget_constraint,
)

assert results['spend'][-2] == 47.
assert results['gain'][-2] == 65.

print(results)

print(f"{results['spend'][-2]=}")
print(f"{results['gain'][-2]=}")

