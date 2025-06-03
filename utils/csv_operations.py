import pandas as pd
import io

class CSVOperations:
    @staticmethod
    def split_csv(df: pd.DataFrame, rows_per_file: int) -> list:
        """拆分CSV文件"""
        total_rows = len(df)
        split_dfs = []
        
        for i in range(0, total_rows, rows_per_file):
            split_df = df.iloc[i:i + rows_per_file].copy()
            split_dfs.append(split_df)
            
        return split_dfs
    
    @staticmethod
    def merge_csvs(dfs: list, sort_column: str = None, ascending: bool = True) -> pd.DataFrame:
        """合并CSV文件"""
        merged_df = pd.concat(dfs, ignore_index=True)
        if sort_column and sort_column in merged_df.columns:
            merged_df.sort_values(by=sort_column, ascending=ascending, inplace=True)
        return merged_df
    
    @staticmethod
    def deduplicate_csv(df: pd.DataFrame, sort_column: str = None, ascending: bool = True) -> pd.DataFrame:
        """CSV去重"""
        df_dedup = df.drop_duplicates()
        if sort_column and sort_column in df_dedup.columns:
            df_dedup.sort_values(by=sort_column, ascending=ascending, inplace=True)
        return df_dedup