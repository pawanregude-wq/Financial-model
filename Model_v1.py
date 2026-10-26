# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 16:49:18 2026

@author: Arjun
"""

import pandas as pd

class FinancialModel:

    def __init__(self, name, industry, ticker, file_path):
        self.name = name
        self.industry = industry
        self.ticker = ticker
        self.file_path = file_path
        self.data = None
        self.ratios = None

    def load_data(self):
        self.data = pd.read_excel(
            self.file_path,
            sheet_name=None,
            index_col=0
        )

    def ratio_analysis(self):

        ratio_definitions = {
            "EBITDA_Margin": ("IS_EBITDA", "IS_Revenue"),
            "EBIT_Margin": ("IS_EBIT", "IS_Revenue"),
            "Net_Profit_Margin": ("IS_NetIncome", "IS_Revenue"),
            "ROE": ("IS_NetIncome", "BS_Equity"),
            "Debt_to_Equity": ("BS_debt", "BS_Equity"),
        }

        # Combine the financial statement rows from all sheets
        financial_data = pd.concat(self.data.values())

        # Clean the row labels
        financial_data.index = (
            financial_data.index.astype(str).str.strip()
        )

        results = {}

        for ratio_name, (numerator_label, denominator_label) in ratio_definitions.items():

            numerator = financial_data.loc[numerator_label]
            denominator = financial_data.loc[denominator_label]

            results[ratio_name] = numerator / denominator

        self.ratios = pd.DataFrame(results).T

        return self.ratios