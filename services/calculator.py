import pandas as pd

class DiscrepancyCalculator:
    @staticmethod
    def merge_and_calculate(internal_df, external_df):
        """
        Joins two DataFrames on Date and calculates % difference.
        Formula: (Internal - External) / Internal * 100
        """
        # Standardize dates
        internal_df['Date'] = pd.to_datetime(internal_df['Date'])
        external_df['Date'] = pd.to_datetime(external_df['Date'])
        
        # Merge
        merged = pd.merge(
            internal_df, 
            external_df, 
            on='Date', 
            suffixes=('_int', '_ext')
        )
        
        # Rename for DB model
        merged = merged.rename(columns={
            'Date': 'date',
            'Impressions_int': 'internal_imps',
            'Revenue_int': 'internal_rev',
            'Impressions_ext': 'external_imps',
            'Revenue_ext': 'external_rev'
        })
        
        # Calculate Logic
        merged['discrepancy_imps'] = (
            (merged['internal_imps'] - merged['external_imps']) / merged['internal_imps'] * 100
        ).round(2)
        
        merged['discrepancy_rev'] = (
            (merged['internal_rev'] - merged['external_rev']) / merged['internal_rev'] * 100
        ).round(2)
        
        merged['partner_name'] = "Demo Partner" # Placeholder
        
        return merged
