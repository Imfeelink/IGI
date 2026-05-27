import pandas as pd
import os
from abc import ABC, abstractmethod

class BasePandasAnalyzer(ABC):
    def __init__(self, filepath: str):
        self.filepath = filepath
        self._df = self._load_data()

    @property
    def df(self) -> pd.DataFrame:
        """Getter for the dataframe."""
        return self._df

    def _load_data(self) -> pd.DataFrame:
        """
        Loads data from CSV
        """
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"File {self.filepath} not found.")
        return pd.read_csv(self.filepath)

    @abstractmethod
    def perform_task_a(self):
        """Abstract method for Task A execution."""
        pass

    @abstractmethod
    def perform_task_b(self):
        """Abstract method for Task B execution."""
        pass


class MelbourneHousingAnalyzer(BasePandasAnalyzer):
    def __init__(self, filepath: str):
        super().__init__(filepath)

    def perform_task_a(self) -> pd.Series:
        """
        Task A: Creates a MultiIndex Series with price values and renames index levels.
        """
        required_cols = ['Suburb', 'Type', 'Price']
        if not all(col in self.df.columns for col in required_cols):
            raise KeyError(f"Dataset must contain columns: {required_cols}")

        multi_idx_df = self.df.set_index(['Suburb', 'Type'])
        
        multi_series = multi_idx_df['Price']
        
        multi_series.index.names = ['Location_Name', 'Property_Type']
        
        return multi_series

    def perform_task_b(self) -> float:
        """
        Task B: Calculates ratio between avg price of max rooms and min rooms (>0).
        """
        if 'Rooms' not in self.df.columns or 'Price' not in self.df.columns:
            raise KeyError("Dataset must contain 'Rooms' and 'Price' columns.")

        max_rooms = self.df['Rooms'].max()
        print("MAX ROOMS: ", max_rooms)
        
        min_rooms = self.df[self.df['Rooms'] > 0]['Rooms'].min()
        print("MIN ROOMS: ", min_rooms)

        avg_price_max = self.df[self.df['Rooms'] == max_rooms]['Price'].mean()
        print("AVERAGE MAX PRICE: ", avg_price_max)

        avg_price_min = self.df[self.df['Rooms'] == min_rooms]['Price'].mean()
        print("AVERAGE MIN PRICE:", round(avg_price_min, 2))

        if avg_price_min == 0 or pd.isna(avg_price_min):
            return 0.0

        ratio = avg_price_max / avg_price_min
        return round(ratio, 2)
    