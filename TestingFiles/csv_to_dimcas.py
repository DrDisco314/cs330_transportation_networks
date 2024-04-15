import pandas as pd

name = "Surat"


def csv_to_dimacs(csv_filename, output_gr_filename, output_co_filename):
    df = pd.read_csv(csv_filename)

    with open(output_gr_filename, "w") as gr_file:

        gr_file.write(f"p sp {df['START_NODE'].nunique()} {len(df)}\n")
        for _, row in df.iterrows():

            gr_file.write(
                f"a {int(row['START_NODE'])} {int(row['END_NODE'])} {int(row['LENGTH'])}\n"
            )

    with open(output_co_filename, "w") as co_file:

        co_file.write(f"p aux sp co {df['START_NODE'].nunique()}\n")
        nodes = (
            df[["START_NODE", "XCoord", "YCoord"]]
            .drop_duplicates("START_NODE")
            .sort_values("START_NODE")
        )
        for _, node in nodes.iterrows():
            co_file.write(
                f"v {int(node['START_NODE'])} {node['XCoord']} {node['YCoord']}\n"
            )


csv_to_dimacs(
    f"Data/{name}_Edgelist.csv", f"Data/DIMCAS/{name}.gr", f"Data/DIMCAS/{name}.co"
)
