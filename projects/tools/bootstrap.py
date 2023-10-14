import matplotlib.pyplot as plt
import pandas as pd
from pandas import ReadCsvBuffer
from tqdm import tqdm
from os import PathLike
from typing import Any, Optional

def bootstrap(data: Any, file_out: str | PathLike[str], plot_result: bool = False):
    df = pd.DataFrame(data)
    raise NotImplementedError

def bootstrap_csv(file_in: str | PathLike[str] | ReadCsvBuffer[bytes] | ReadCsvBuffer[str], column_name: Optional[str] = None, n_iterations: int = 10_000, verbose: bool = False, plot_result: bool = False) -> pd.DataFrame:
    df = pd.read_csv(file_in)
    # Size of a bootstrap sample (using the same size as original sample).
    n_size = len(df)
    means = []

    for _ in tqdm(range(n_iterations)):
        # Bootstrap sample: random sample **with replacement** or you're going to have a rough time.
        sample = df.sample(n_size, replace=True)

        # Calculate mean of this sample and append to the list of means.
        if column_name is None:
            mean = sample.mean()
        else:
            mean = sample[column_name].mean()

        means.append(mean)

    # Converting means to a DataFrame for further analysis, if needed.
    column_key = f"mean_{column_name}"
    means_df = pd.DataFrame(means, columns=[column_key])

    # Print summary statistics of the bootstrapped means.
    if verbose:
        print(means_df[column_key].describe(percentiles=[0.025, 0.975]))

    n, bins, patches = plt.hist(means, bins=80, color="blue") #edgecolor='black')
    # alternatively, could write
    # n, bins, patches = np.histogram(means, bins=80)
    if plot_result:
        plt.title("Histogram of Bootstrapped Mean Download Speeds")
        plt.xlabel("Mean Download Speed (Mb/s)")
        plt.ylabel("Count")
        plt.grid(axis="y", alpha=0.75)
        plt.show()

    # Save histogram to CSV
    return pd.DataFrame({"bin_left": bins[:-1], "bin_right": bins[1:], "count": n})
    # hist_df.to_csv("/Users/matthewturk/Desktop/speed-test/wifi-samples/hist.csv", index=False)
    # might also try a beta uniform prior
    # plt.hist(means, bins=200, color="blue", edgecolor="black", density=True)
    # plt.title("Probability Density Function of Bootstrapped Mean Download Speeds")
    # plt.xlabel("Mean Download Speed (Mb/s)")
    # plt.ylabel("Probability Density")
    # plt.grid(axis="y", alpha=0.75)
    # plt.show()
